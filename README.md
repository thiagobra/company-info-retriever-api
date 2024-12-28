# 🚀 Batch API Company Info Retriever

## 🌟 Overview
This repository contains a Python script that retrieves the **official website** 🌐 and **main product** 🏷️ information for a list of companies using the Perplexity API. The script processes companies in **batches** 📦, queries the API for live data, and writes the results to a CSV file 📄.

## ✨ Features
- 🔄 Queries the Perplexity API in **batches of 6** to minimize costs and improve efficiency.
- 🌐 Retrieves **official website** and **main product** (or most well-known product if unavailable).
- 🛠️ Handles **malformed data**, **missing fields**, and other edge cases gracefully.
- ✍️ Writes results to a CSV file with columns: `CompanyName`, `Website`, and `MainProduct`.
- 🛡️ Includes robust error handling and debugging for seamless operation.

## 📋 Prerequisites
1. 🐍 Python 3.7 or higher.
2. 🔑 A Perplexity API key.

## ⚙️ Setup
1. Clone this repository:
git clone https://github.com/thiagobra/company-info-retriever-api.git cd company-info-retriever-api

markdown
Copy code
3. Install required Python packages:
pip install requests

vbnet
Copy code
3. Set your Perplexity API key as an environment variable:
export PERPLEXITYAI_API_KEY="your_api_key_here"

markdown
Copy code

## 🚦 Usage
1. Prepare an input CSV file (`companies.csv`) with at least one column:
- `CompanyName`: List of company names to query.

Example:
CompanyName Google Microsoft Apple

markdown
Copy code

2. Run the script:
python main.py

markdown
Copy code

3. 🏁 Output CSV (`companies_with_website_and_product.csv`) will contain:
- 🏢 `CompanyName`: Original company name from input.
- 🌐 `Website`: Official website of the company.
- 🏷️ `MainProduct`: Main or most well-known product.

## 📝 Notes
- ❓ Missing or unavailable information is filled with `N/A`.
- ⚡ Errors in one API response line do not affect the rest of the batch.
- 📊 Ensure that the Perplexity API key has sufficient permissions and quota for the queries.

## 🤝 Contributing
Contributions are welcome! 🛠️ Feel free to submit a pull request or open an issue for discussion.

## 📜 License
This project is licensed under the MIT License. 🖋️
