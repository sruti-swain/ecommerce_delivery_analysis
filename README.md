
# E-Commerce Order and Delivery Analysis

## Project Overview

This project analyzes e-commerce order and delivery data using Python, SQL, and SQLite. It demonstrates data cleaning, data quality validation, data transformation, database integration, and business analytics.

The goal is to identify delivery delays, compare delivery performance across cities, and generate insights that can support data-driven business decisions.

## Objectives

- Clean and validate raw order data.
- Identify duplicate records, missing values, and invalid delivery dates.
- Calculate delivery duration for completed orders.
- Store processed data in an SQLite database.
- Analyze delivery performance using SQL queries.
- Generate visualizations and data quality reports.

## Technologies Used

- **Python** — Data processing and automation
- **Pandas** — Data cleaning and transformation
- **SQL** — Data analysis and aggregation
- **SQLite** — Database storage
- **Matplotlib** — Data visualization
- **Git and GitHub** — Version control and project sharing

## Project Structure

```text
ecommerce-delivery-analysis/
│
├── orders.csv
├── main.py
├── analysis.sql
├── README.md
│
└── output/
    ├── cleaned_orders.csv
    ├── ecommerce_orders.db
    ├── average_delivery_by_city.png
    ├── orders_by_category.png
    ├── city_delivery_summary.csv
    ├── category_summary.csv
    └── data_quality_report.txt
```

## Dataset Description

The project uses a synthetic e-commerce dataset created for learning and demonstration.

| Column | Description |
|---|---|
| Order_ID | Unique order identifier |
| Order_Date | Date the order was placed |
| Delivery_Date | Date the order was delivered |
| City | Customer delivery city |
| Category | Product category |
| Order_Status | Current order status |

The raw dataset contains examples of duplicate order IDs, missing delivery dates, and invalid date sequences to demonstrate data quality validation.

## Data Processing Workflow

### 1. Data Loading
Load the raw CSV dataset using Pandas.

### 2. Data Cleaning
- Standardize text fields.
- Handle missing values.
- Identify and remove duplicate order IDs.
- Convert date columns into datetime format.

### 3. Data Validation
- Detect invalid order dates.
- Identify delivery dates earlier than order dates.
- Flag records with data quality issues.
- Distinguish pending deliveries from completed deliveries.

### 4. Data Transformation
Calculate delivery duration in days and classify completed deliveries using a three-day threshold as a project assumption.

### 5. Database Integration
Load the processed dataset into an SQLite database for SQL-based analysis.

### 6. SQL Analytics
Use SQL queries to analyze:
- Overall order counts and data quality
- Missing and invalid delivery records
- Average delivery duration
- City-wise delivery performance
- Delayed delivery percentage
- Product category performance
- Monthly order volume

### 7. Visualization and Reporting
Generate charts showing average delivery duration by city and order volume by product category. Export summary tables and a data quality report.

## How to Run the Project

### Prerequisites

- Python 3
- pip
- VS Code or another Python editor

### Step 1: Clone the Repository

After uploading the project to GitHub, clone it using:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ecommerce-delivery-analysis
```

Alternatively, download the project ZIP and extract it.

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install pandas matplotlib
```

### Step 4: Run the Python Script

Ensure `orders.csv` is in the project root directory, then run:

```bash
python main.py
```

The script processes the dataset, creates the SQLite database, exports reports, and generates charts in the `output/` directory.

### Step 5: Execute SQL Queries

Open `output/ecommerce_orders.db` using a SQLite-compatible database browser and execute the queries in `analysis.sql`.

## Expected Deliverables

- Cleaned order dataset
- SQLite database containing processed order data
- SQL analytics queries
- City-wise delivery summary
- Category-wise order summary
- Delivery performance visualizations
- Data quality report

## Key Learnings

- Data cleaning and preprocessing using Pandas
- SQL queries using filtering, grouping, aggregation, and conditional logic
- Data quality validation and error detection
- Integration of Python with SQLite
- Data visualization and business reporting
- Organizing a reproducible data analytics project

## Limitations

- The dataset is synthetic and small, so findings are for demonstration purposes only.
- The three-day delay threshold is an illustrative assumption, not an industry standard.
- The project does not use real-time order data or production ETL infrastructure.

## Future Improvements

- Use a larger public e-commerce dataset.
- Build an interactive dashboard using Power BI.
- Add automated data quality tests.
- Schedule the pipeline to run periodically.
- Introduce logging and exception handling.

## Author

**Sruti Seekha Swain & Mousumi Panda **

Aspiring Data Engineer / Data Analyst

Skills: Python | SQL | Pandas | SQLite | Data Analytics
