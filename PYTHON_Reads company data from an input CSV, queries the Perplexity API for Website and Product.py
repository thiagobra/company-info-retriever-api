########################################################################################################
# This script reads company data from a CSV file containing company names,
# queries the Perplexity API in batches to retrieve the website and main product for each company,
# (processing up to {15} companies per batch), and writes the results to a separate output CSV file.
########################################################################################################

import csv
import time
import requests
import os

# API Key and Endpoint Configuration
API_KEY = os.getenv("PERPLEXITYAI_API_KEY")
API_URL = "https://api.perplexity.ai/chat/completions"

# Function to Query the Perplexity API in Batches
def query_perplexity_api_batch(companies):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    # Format the companies into a list with clear structure
    company_list = "\n".join([f"- {company}" for company in companies])
    messages = [
        {
            "role": "system",
            "content": "You are an assistant specializing in company data. Provide concise results."
        },
        {
            "role": "user",
            "content": (
                f"For the following companies, provide their official website and main product (or the most well-known product if the main one is unavailable). "
                "Ensure the response follows this exact format, one per line:\n"
                "CompanyName: [company name], Website: [website URL], Main Product: [product name]\n"
                "If any data cannot be found with at least 75% confidence, write 'N/A' for that field.\n"
                f"Companies:\n{company_list}"
            )
        }
    ]
    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "stream": False,
        "max_tokens": 4048,
        "frequency_penalty": 1,
        "temperature": 0.1,
        "messages": messages
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        print("API Response:", response.json())  # Debugging: inspect raw API response
        return response.json()
    else:
        response.raise_for_status()

# Function to Extract Data from Batch Response
def extract_batch_results(response, original_company_names):
    content = response['choices'][0]['message']['content']
    results = {}
    lines = content.split('\n')
    print("Raw Lines from Response:", lines)  # Debugging: check raw lines
    for line in lines:
        if ':' in line:  # Ensure the line has data
            try:
                # Carefully split the line into components
                company_name = None
                website = "N/A"
                product = "N/A"

                # Split by expected separators
                parts = line.split(': ', 1)
                if len(parts) > 1:
                    company_name_part = parts[0].strip('-').strip()
                    rest = parts[1]

                    # Extract website and product if available
                    if ", Main Product: " in rest:
                        website, product = rest.split(", Main Product: ", 1)
                        website = website.strip().strip("[]")  # Clean square brackets
                        product = product.strip()
                    else:
                        website = rest.strip()

                    # Match with original company names
                    company_name = next(
                        (name for name in original_company_names if name.lower() == company_name_part.lower()), None
                    )

                if company_name:
                    results[company_name] = (website, product)
            except Exception as e:
                # Log the error for debugging but continue processing
                print(f"Parsing Error for Line: {line} | Error: {e}")
                continue
    print("Parsed Batch Results:", results)  # Debugging: check parsed results
    return results

# Main Function to Process CSV Files in Batches
def main(input_csv, output_csv, batch_size=15):
    with open(input_csv, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        headers = reader.fieldnames
        print("Headers:", headers)  # Debug statement to check the headers
        if 'CompanyName' not in headers:
            raise KeyError("CSV file must contain a 'CompanyName' column.")
        
        # Define Output Fields
        fieldnames = ['CompanyName', 'Website', 'MainProduct']
        rows = list(reader)
    
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Process Companies in Batches
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            original_company_names = [row['CompanyName'].strip() for row in batch]
            try:
                # Query API for the Batch
                response = query_perplexity_api_batch(original_company_names)
                batch_results = extract_batch_results(response, original_company_names)
                
                # Write Results for the Batch
                for row in batch:
                    company_name = row['CompanyName'].strip()
                    website, product = batch_results.get(company_name, ('N/A', 'N/A'))
                    writer.writerow({
                        'CompanyName': company_name,
                        'Website': website,
                        'MainProduct': product
                    })
                print(f"Processed batch: {original_company_names}")
            except Exception as e:
                print(f"Error processing batch: {original_company_names}, Error: {e}")
                # Write 'Error' for each company in the batch
                for row in batch:
                    writer.writerow({
                        'CompanyName': row['CompanyName'],
                        'Website': 'Error',
                        'MainProduct': 'Error'
                    })
                time.sleep(10)  # Backoff strategy: wait before retrying
            
            time.sleep(1)  # Prevent hitting rate limits

# Entry Point
if __name__ == "__main__":
    input_csv = 'companies.csv'
    output_csv = 'companies_with_website_and_product.csv'
    main(input_csv, output_csv, batch_size=15)
    print("\n\n------------------Processing Completed!------------------\n")
    print("Check the output CSV file for the results.")
