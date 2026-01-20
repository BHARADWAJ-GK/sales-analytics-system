# Sales Analytics System

## Overview
This project is a modular Python-based Sales Analytics System that processes messy sales data, cleans and validates records, performs analytics, enriches transactions using a live API, and generates a professional formatted report.

## Features
- Encoding-safe file reading
- Data cleaning and validation
- Revenue and region analysis
- Product and customer performance analysis
- API integration and enrichment
- Enriched dataset export
- Full formatted sales report generation

## Project Structure
sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
└── utils/
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py

## Setup
1. Install Python 3.8+
2. Install dependencies:
   pip install -r requirements.txt
3. Run:
   python main.py

## Output
- data/enriched_sales_data.txt
- output/sales_report.txt

## Author
Bharadwaj
