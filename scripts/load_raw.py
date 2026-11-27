from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = ROOT / "northwind.duckdb"

SOURCES = {
    "customer": "raw/customer.csv",
    "employees": "raw/employees.csv",
    "suppliers": "raw/suppliers.csv",
    "shippers": "raw/shippers.csv",
    "products": "raw/products.csv",
    "orders": "raw/orders.csv",
    "order_details": "raw/order_details.csv",
    "legacy_orders": "legacy/orders.csv",
    "legacy_order_details": "legacy/order_details.csv",
}

con = duckdb.connect(str(DB_PATH))
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

for table, rel_path in SOURCES.items():
    csv_path = DATA_DIR / rel_path
    con.execute(
        f"CREATE OR REPLACE TABLE raw.{table} AS "
        f"SELECT * FROM read_csv_auto('{csv_path}')"
    )
    n = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
    print(f"raw.{table}: {n} rows")

con.close()
