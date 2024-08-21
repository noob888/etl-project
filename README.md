# etl-project
An Extract Transform Load (ETL) project to extract data from different sources such as Shopify, Fishbowl Inventroy System, transform it using pandas and then load it into Google Sheets.

# 🛠️ ETL Project: Shopify & Fishbowl Integration

![ETL Process](https://img.shields.io/badge/ETL-Process-blue)
![Python Badge](https://img.shields.io/badge/Python-3.9%2B-green)
![Pandas Badge](https://img.shields.io/badge/Library-Pandas-brightgreen)
![Google Sheets Badge](https://img.shields.io/badge/Google%20Sheets-Integration-yellow)

# **Overview**
This project is designed to automate the extraction, transformation, and loading (ETL) of data from multiple sources—namely Shopify and Fishbowl Inventory System—into Google Sheets. The goal is to streamline data integration, improve reporting, and enhance decision-making processes.

# 📂 **Project Structure**

```
📦etl-project
 ┣ 📜extract.py         # Scripts for extracting data from Shopify and Fishbowl
 ┣ 📜transform.py       # Scripts for transforming data using Pandas
 ┣ 📜load.py            # Scripts for loading data into Google Sheets
 ┣ 📜requirements.txt     # Required Python libraries
 ┗ 📜README.md            # Project documentation
```
 
# 🔄 ETL Workflow
1. Extract
Shopify: Data is pulled using Shopify's REST API, focusing on orders, products, and customer data.
Fishbowl Inventory System: Data is extracted using the Fishbowl API, retrieving inventory levels, purchase orders, and supplier information.
2. Transform
Data Cleaning: Data is cleaned and normalized using Pandas.
Data Transformation: Custom transformations are applied to prepare data for analysis and reporting, including merging datasets and calculating KPIs.
3. Load
Google Sheets: Transformed data is loaded into designated Google Sheets, making it accessible for stakeholders and ensuring real-time updates.


# 🗺️ **Data Flow Diagram**

```
graph TD;
    A[Shopify] --> B[Extract];
    C[Fishbowl] --> B[Extract];
    B[Extract] --> D[Transform];
    D[Transform] --> E[Load to Google Sheets];
```

   
🚀 **Getting Started**

**Prerequisites**
Python 3.9+
Access to Shopify and Fishbowl APIs
Google Sheets API credentials


**Installation**

Clone the repository:
```
git clone https://github.com/your-username/etl-project.git
cd etl-project
```
Install the required libraries:
```
pip install -r requirements.txt
```
Configure API keys in config.py.

Running the ETL Process
```
python src/extract.py
python src/transform.py
python src/load.py
```

✨ **Features**

Automated Data Extraction: Seamlessly integrates with Shopify and Fishbowl to pull data.
Custom Data Transformations: Utilizes Pandas for powerful data manipulation.
Real-Time Reporting: Automatically updates Google Sheets with the latest data.

🛡️ Security
Ensure that API keys and sensitive information are stored securely in config.py and not hard-coded into scripts.

📄 License
This project is not licensed currently.

🧑‍💻 Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

