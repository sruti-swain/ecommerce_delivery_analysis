
from pathlib import Path
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. SET UP PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "orders.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

DB_FILE = OUTPUT_DIR / "ecommerce_orders.db"


# --------------------------------------------------
# 2. LOAD THE RAW DATA
# --------------------------------------------------

print("=" * 55)
print(" E-COMMERCE ORDER & DELIVERY ANALYSIS")
print("=" * 55)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {DATA_FILE.name}. "
        "Place orders.csv in the same folder as main.py."
    )

df = pd.read_csv(DATA_FILE)

required_columns = [
    "Order_ID",
    "Order_Date",
    "Delivery_Date",
    "City",
    "Category",
    "Order_Status",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("\nSTEP 1: RAW DATA LOADED")
print(f"Total records: {len(df)}")
print("\nFirst five records:")
print(df.head())


# --------------------------------------------------
# 3. CLEAN AND STANDARDIZE THE DATA
# --------------------------------------------------

print("\nSTEP 2: CLEANING DATA")

# Standardize text columns
text_columns = ["City", "Category", "Order_Status"]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Treat blank text as missing
for column in text_columns:
    df[column] = df[column].replace("", pd.NA)

# Convert dates into proper datetime values
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"], errors="coerce"
)

df["Delivery_Date"] = pd.to_datetime(
    df["Delivery_Date"], errors="coerce"
)

# Convert order IDs to numeric values for validation
df["Order_ID"] = pd.to_numeric(
    df["Order_ID"], errors="coerce"
)

# Count missing values before removing duplicates
missing_values = df.isna().sum()

# Identify duplicate order IDs
duplicate_mask = df["Order_ID"].duplicated(keep="first")
duplicate_count = int(duplicate_mask.sum())

# Remove duplicate order IDs, keeping the first occurrence
df = df.loc[~duplicate_mask].copy()

print(f"Duplicate records removed: {duplicate_count}")


# --------------------------------------------------
# 4. VALIDATE RECORDS AND DELIVERY DATES
# --------------------------------------------------

print("\nSTEP 3: VALIDATING DATA")

# Identify records without a valid order ID or order date
invalid_order_mask = (
    df["Order_ID"].isna()
    | df["Order_Date"].isna()
)

invalid_order_count = int(invalid_order_mask.sum())

# A delivery date before the order date is invalid
invalid_delivery_mask = (
    df["Delivery_Date"].notna()
    & df["Order_Date"].notna()
    & (df["Delivery_Date"] < df["Order_Date"])
)

invalid_delivery_count = int(invalid_delivery_mask.sum())

# Keep invalid records for auditing, but flag them
df["Data_Quality_Status"] = "Valid"

df.loc[invalid_order_mask, "Data_Quality_Status"] = (
    "Invalid Order Data"
)

df.loc[
    invalid_delivery_mask,
    "Data_Quality_Status"
] = "Invalid Delivery Date"

# Missing delivery dates are not automatically considered late
df["Delivery_Days"] = (
    df["Delivery_Date"] - df["Order_Date"]
).dt.days

# Exclude invalid delivery durations from analysis
df.loc[invalid_delivery_mask, "Delivery_Days"] = pd.NA

# Mark whether a completed delivery took more than 3 days
df["Delivery_Performance"] = "Not Delivered"

valid_delivery_mask = (
    df["Delivery_Date"].notna()
    & ~invalid_delivery_mask
    & ~invalid_order_mask
)

df.loc[valid_delivery_mask, "Delivery_Performance"] = (
    "On Time"
)

df.loc[
    valid_delivery_mask
    & (df["Delivery_Days"] > 3),
    "Delivery_Performance"
] = "Delayed"

# Missing dates for orders not yet delivered remain pending
pending_mask = (
    df["Delivery_Date"].isna()
    & ~invalid_order_mask
)

df.loc[pending_mask, "Delivery_Performance"] = "Pending"

# Invalid date sequences are explicitly flagged
df.loc[
    invalid_delivery_mask,
    "Delivery_Performance"
] = "Invalid Date"

print(f"Invalid order records: {invalid_order_count}")
print(f"Invalid delivery dates: {invalid_delivery_count}")
print(f"Records remaining after deduplication: {len(df)}")


# --------------------------------------------------
# 5. SAVE THE CLEANED DATASET
# --------------------------------------------------

print("\nSTEP 4: SAVING CLEANED DATA")

cleaned_file = OUTPUT_DIR / "cleaned_orders.csv"

df.to_csv(cleaned_file, index=False)

print(f"Cleaned data saved to: {cleaned_file}")


# --------------------------------------------------
# 6. LOAD DATA INTO SQLITE
# --------------------------------------------------

print("\nSTEP 5: LOADING SQLITE DATABASE")

# Replace the database table each time the script runs
with sqlite3.connect(DB_FILE) as connection:
    df.to_sql(
        "orders",
        connection,
        if_exists="replace",
        index=False
    )

print(f"Database saved to: {DB_FILE}")


# --------------------------------------------------
# 7. RUN SQL ANALYTICS
# --------------------------------------------------

print("\nSTEP 6: SQL ANALYSIS")

with sqlite3.connect(DB_FILE) as connection:

    # Query 1: Overall order and delivery statistics
    overall_query = """
        SELECT
            COUNT(*) AS total_orders,
            ROUND(AVG(Delivery_Days), 2)
                AS average_delivery_days
        FROM orders
        WHERE Delivery_Days IS NOT NULL
          AND Data_Quality_Status = 'Valid';
    """

    overall = pd.read_sql_query(
        overall_query, connection
    )

    print("\nOverall Statistics:")
    print(overall.to_string(index=False))

    # Query 2: Delivery performance by city
    city_query = """
        SELECT
            City,
            COUNT(*) AS total_orders,
            ROUND(AVG(Delivery_Days), 2)
                AS average_delivery_days,
            SUM(
                CASE
                    WHEN Delivery_Performance = 'Delayed'
                    THEN 1 ELSE 0
                END
            ) AS delayed_orders
        FROM orders
        WHERE City IS NOT NULL
          AND Data_Quality_Status = 'Valid'
        GROUP BY City
        ORDER BY average_delivery_days DESC;
    """

    city_summary = pd.read_sql_query(
        city_query, connection
    )

    print("\nCity-Wise Delivery Analysis:")
    print(city_summary.to_string(index=False))

    # Query 3: Number of orders in each category
    category_query = """
        SELECT
            Category,
            COUNT(*) AS total_orders
        FROM orders
        WHERE Category IS NOT NULL
        GROUP BY Category
        ORDER BY total_orders DESC;
    """

    category_summary = pd.read_sql_query(
        category_query, connection
    )

    print("\nCategory-Wise Order Analysis:")
    print(category_summary.to_string(index=False))

    # Save SQL results for review
    city_summary.to_csv(
        OUTPUT_DIR / "city_delivery_summary.csv",
        index=False
    )

    category_summary.to_csv(
        OUTPUT_DIR / "category_summary.csv",
        index=False
    )


# --------------------------------------------------
# 8. CREATE VISUALIZATIONS
# --------------------------------------------------

print("\nSTEP 7: CREATING CHARTS")

# Chart 1: Average delivery time by city
chart_data = city_summary.dropna(
    subset=["average_delivery_days"]
)

if not chart_data.empty:
    plt.figure(figsize=(8, 5))

    plt.bar(
        chart_data["City"],
        chart_data["average_delivery_days"]
    )

    plt.title("Average Delivery Time by City")
    plt.xlabel("City")
    plt.ylabel("Average Delivery Time (Days)")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "average_delivery_by_city.png",
        dpi=150
    )

    plt.close()

# Chart 2: Order counts by category
category_chart = category_summary.dropna(
    subset=["Category"]
)

if not category_chart.empty:
    plt.figure(figsize=(8, 5))

    plt.bar(
        category_chart["Category"],
        category_chart["total_orders"]
    )

    plt.title("Number of Orders by Category")
    plt.xlabel("Product Category")
    plt.ylabel("Number of Orders")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "orders_by_category.png",
        dpi=150
    )

    plt.close()


# --------------------------------------------------
# 9. GENERATE A DATA QUALITY REPORT
# --------------------------------------------------

report_file = OUTPUT_DIR / "data_quality_report.txt"

report_lines = [
    "E-COMMERCE DATA QUALITY REPORT",
    "=" * 35,
    f"Raw records: {len(pd.read_csv(DATA_FILE))}",
    f"Duplicate order IDs removed: {duplicate_count}",
    f"Records after deduplication: {len(df)}",
    f"Invalid order records: {invalid_order_count}",
    f"Invalid delivery dates: {invalid_delivery_count}",
    "",
    "Missing values in raw data:",
    missing_values.to_string(),
    "",
    "Final delivery performance counts:",
    df["Delivery_Performance"].value_counts(
        dropna=False
    ).to_string(),
]

report_file.write_text(
    "\n".join(report_lines),
    encoding="utf-8"
)

print(f"Data quality report saved to: {report_file}")


# --------------------------------------------------
# 10. FINISH
# --------------------------------------------------

print("\n" + "=" * 55)
print("PROJECT COMPLETED SUCCESSFULLY!")
print("=" * 55)

print(f"Cleaned CSV: {cleaned_file}")
print(f"SQLite database: {DB_FILE}")
print(f"Charts and reports: {OUTPUT_DIR}")
