# 💱 USD to INR Currency Conversion Pipeline | Data Engineering ETL Project

## 📌 Project Description

This project is a complete **Data Engineering ETL Pipeline** built using **Python, Pandas, MySQL, and REST API integration**. It takes raw transactional order data stored in **USD**, cleans and standardizes the dataset, fetches historical **USD to INR exchange rates** using a live public API, converts all financial values into INR, stores processed data into a MySQL database, generates invoice JSON files, and exports the final transformed dataset into CSV format.

The project demonstrates real-world data engineering concepts such as:

- ETL (Extract, Transform, Load)
- Data Cleaning
- API Integration
- Currency Conversion
- Relational Database Storage
- File Export Automation
- Handling Dirty Data
- Idempotent Pipeline Design

---

# 🚀 Problem Statement

Many businesses receive orders globally and store financial records in USD. However, Indian reporting systems often require values in INR.

Manual conversion creates multiple issues:

- Time consuming process
- Human errors
- Inconsistent calculations
- Difficult to repeat monthly
- No centralized storage

This project automates the complete process using a smart ETL pipeline.

---

# 🎯 Project Objectives

- Read raw CSV data automatically
- Clean duplicate and inconsistent records
- Normalize order IDs
- Parse multiple date formats
- Fetch historical USD→INR rates
- Convert Amount / Tax / Shipping to INR
- Store final output in MySQL
- Generate JSON invoices
- Export clean result CSV
- Build reusable production-style pipeline

---

# 🛠️ Tech Stack Used

| Technology | Purpose |
|------------|---------|
| Python 3 | Main programming language |
| Pandas | Data cleaning and transformation |
| Requests | API calls |
| MySQL | Structured database storage |
| mysql-connector-python | Python to MySQL connection |
| JSON | Invoice generation |
| CSV | Raw + Final file storage |
| Frankfurter API | Historical exchange rates |

---

# 🏗️ Full Pipeline Architecture

Orders.csv
   ↓
[ Bronze Layer ]
Raw Source Data

   ↓

[ Silver Layer ]
Cleaning + Standardization + Null Handling + Parsing

   ↓

[ Gold Layer ]
Currency Conversion + MySQL Load + Invoice Export

   ↓

Outputs:
- MySQL Database
- Result_Table.csv
- invoices/*.json

File Structure
currency-conversion-pipeline/
│── Orders.csv
│── pipeline.py
│── Result_Table.csv
│── README.md
│── invoices/
│    ├── ORD-001.json
│    ├── ORD-002.json
│    └── ...
