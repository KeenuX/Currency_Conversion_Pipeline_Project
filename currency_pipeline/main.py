import pandas as pd
import requests
import mysql.connector
import json
import os

CSV_FILE = "Orders.csv"
INVOICE_DIR = "invoices"

os.makedirs(INVOICE_DIR, exist_ok=True)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS afterconversion_data")
conn.database = "afterconversion_data"

cursor.execute("""
CREATE TABLE IF NOT EXISTS processed_orders (order_id VARCHAR(255) PRIMARY KEY,order_date VARCHAR(50),amount_usd DECIMAL(10,2),amount_inr DECIMAL(10,2),tax_usd DECIMAL(10,2),tax_inr DECIMAL(10,2),shipping_usd DECIMAL(10,2),shipping_inr DECIMAL(10,2),exchange_rate DECIMAL(10,2))
               """)

conn.commit()

rate_cache = {}

def get_exchange_rate(order_date):

    if order_date in rate_cache:
        return rate_cache[order_date]

    try:
        url = f"https://api.frankfurter.dev/v2/rate/USD/INR?date={order_date}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            rate = data.get("rate")
        else:
            rate = 83.50

    except:
        rate = 83.50

    rate_cache[order_date] = rate
    return rate

def generate_invoice(row, rate):

    file_name = f"{INVOICE_DIR}/{row['order_id']}.json"

    if os.path.exists(file_name):
        return

    data = {
        "order_id": row["order_id"],
        "date": row["order_date"],
        "amount_usd": row["amount_usd"],
        "amount_inr": round(row["amount_usd"] * rate, 2),
        "tax_usd": row["tax_usd"],
        "tax_inr": round(row["tax_usd"] * rate, 2),
        "shipping_usd": row["shipping_usd"],
        "shipping_inr": round(row["shipping_usd"] * rate, 2)
    }

    with open(file_name, "w") as f:
        json.dump(data, f)

def transform():

    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print("CSV file not found")
        return

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    df.fillna({
        "tax_usd": 0,
        "shipping_usd": 0
    }, inplace=True)

    df.drop_duplicates(subset=["order_id"], inplace=True)

    df["order_id"] = df["order_id"].astype(str).str.upper().str.strip()
    df["order_id"] = df["order_id"].str.extract(r'(\d+)')[0]
    df["order_id"] = "ORD-" + df["order_id"].str.zfill(3)

    for col in ["amount_usd", "tax_usd", "shipping_usd"]:
        df[col] = df[col].astype(str).str.replace(r"[^\d.-]", "", regex=True)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    df.dropna(subset=["order_id", "order_date", "amount_usd"], inplace=True)

    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")

    for row in df.itertuples(index=False):

        rate = get_exchange_rate(row.order_date)

        cursor.execute(
            """
            INSERT IGNORE INTO processed_orders
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                row.order_id,
                row.order_date,
                row.amount_usd,
                round(row.amount_usd * rate, 2),
                row.tax_usd,
                round(row.tax_usd * rate, 2),
                row.shipping_usd,
                round(row.shipping_usd * rate, 2),
                rate
            )
        )

        generate_invoice(row._asdict(), rate)

    conn.commit()

def save():

    data = pd.read_sql("SELECT * FROM processed_orders", conn)
    data.to_csv("Result_Table.csv", index=False)
    print("Result_Table.csv created")

if __name__ == "__main__":
    transform()
    save()
    cursor.close()
    conn.close()