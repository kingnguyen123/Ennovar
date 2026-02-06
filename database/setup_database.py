"""
Database Setup Script

This script creates a SQLite database and loads CSV files into corresponding tables.
It includes error handling and validation to ensure data integrity.
"""
import sqlite3
import pandas as pd
import os
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent
DATABASE_PATH = BASE_DIR / "database" / "database.db"
CSV_DIR = BASE_DIR / "data"

# CSV to Table mapping with column renaming
CSV_MAPPING = {
    "products.csv": {
        "table": "products",
        "columns": {
            "sku_id": "sku_id",
            "product_name": "product_name",
            "category": "category",
            "sub_category": "sub_category",
            "brand": "brand",
            "product_type": "product_type",
            "size_label": "size_label",
            "launch_date": "launch_date",
            "shelf_life_months": "shelf_life_months",
            "parent_sku": "parent_sku",
            "default_price": "default_price",
            "primary_supplier_id": "primary_supplier_id",
            "is_active": "is_active",
            "country_of_origin": "country_of_origin",
            "online_only": "online_only",
            "avg_rating": "avg_rating",
            "rating_count": "rating_count",
            "is_discontinued": "is_discontinued"
        }
    },
    "sales.csv": {
        "table": "sales",
        "columns": {
            "sale_id": "sale_id",
            "order_id": "order_id",
            "date": "date",
            "sku_id": "sku_id",
            "channel": "channel",
            "quantity": "quantity",
            "unit_price": "unit_price",
            "promo_flag": "promo_flag",
            "discount_pct": "discount_pct",
            "event_name": "event_name",
            "customer_segment_id": "customer_segment_id",
            "customer_segment": "customer_segment",
            "device_type": "device_type",
            "payment_method": "payment_method",
            "shipping_fee": "shipping_fee",
            "voucher_amount": "voucher_amount",
            "net_revenue": "net_revenue",
            "returned_flag": "returned_flag",
            "quarter_bucket": "quarter_bucket",
            "month": "month"
        }
    },
    "purchase_orders.csv": {
        "table": "purchase_orders",
        "columns": {
            "po_id": "po_id",
            "sku_id": "sku_id",
            "supplier_id": "supplier_id",
            "po_date": "po_date",
            "promised_delivery_date": "promised_delivery_date",
            "delivery_date": "delivery_date",
            "order_qty": "order_qty",
            "unit_cost": "unit_cost",
            "shipping_mode": "shipping_mode",
            "status": "status",
            "incoterm": "incoterm",
            "currency": "currency",
            "freight_cost": "freight_cost",
            "duty_cost": "duty_cost"
        }
    }
}


def create_connection():
    """Create a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        print(f"Connected to database: {DATABASE_PATH}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise


def create_tables(conn):
    """Create tables in the database."""
    try:
        cursor = conn.cursor()

        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                sku_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                sub_category TEXT,
                brand TEXT,
                product_type TEXT,
                size_label TEXT,
                launch_date TEXT,
                shelf_life_months REAL,
                parent_sku TEXT,
                default_price REAL,
                primary_supplier_id INTEGER,
                is_active INTEGER,
                country_of_origin TEXT,
                online_only INTEGER,
                avg_rating REAL,
                rating_count INTEGER,
                is_discontinued INTEGER
            )
        """)
        print("Created 'products' table")

        # Create sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY,
                order_id TEXT,
                date TEXT NOT NULL,
                sku_id TEXT,
                channel TEXT,
                quantity INTEGER,
                unit_price REAL,
                promo_flag INTEGER,
                discount_pct REAL,
                event_name TEXT,
                customer_segment_id INTEGER,
                customer_segment TEXT,
                device_type TEXT,
                payment_method TEXT,
                shipping_fee REAL,
                voucher_amount REAL,
                net_revenue REAL,
                returned_flag INTEGER,
                quarter_bucket TEXT,
                month TEXT,
                FOREIGN KEY (sku_id) REFERENCES products(sku_id)
            )
        """)
        print("Created 'sales' table")

        # Create purchase_orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                po_id TEXT PRIMARY KEY,
                sku_id TEXT,
                supplier_id INTEGER,
                po_date TEXT,
                promised_delivery_date TEXT,
                delivery_date TEXT,
                order_qty INTEGER,
                unit_cost REAL,
                shipping_mode TEXT,
                status TEXT,
                incoterm TEXT,
                currency TEXT,
                freight_cost REAL,
                duty_cost REAL,
                FOREIGN KEY (sku_id) REFERENCES products(sku_id)
            )
        """)
        print("Created 'purchase_orders' table")

        conn.commit()
        print("\nAll tables created successfully\n")

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        raise


def load_csv_to_database(conn):
    """Load CSV files into the database."""
    for csv_file, config in CSV_MAPPING.items():
        csv_path = CSV_DIR / csv_file
        table_name = config["table"]
        column_mapping = config["columns"]

        try:
            print(f"Loading {csv_file}...")

            # Read CSV file
            if not csv_path.exists():
                print(f"  Warning: {csv_file} not found at {csv_path}")
                continue

            df = pd.read_csv(csv_path)
            print(f"  - Read {len(df)} rows from {csv_file}")

            # Select and rename columns
            available_columns = [col for col in column_mapping.keys() if col in df.columns]
            if not available_columns:
                print(f"  Warning: No matching columns found in {csv_file}")
                continue

            df_subset = df[available_columns].copy()
            df_subset.rename(columns=column_mapping, inplace=True)

            # Write to database
            df_subset.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"  Loaded {len(df_subset)} rows into '{table_name}' table")

        except pd.errors.EmptyDataError:
            print(f"  Error: {csv_file} is empty")
        except KeyError as e:
            print(f"  Error: Missing column {e} in {csv_file}")
        except Exception as e:
            print(f"  Error loading {csv_file}: {e}")
            raise


def verify_database(conn):
    """Verify the database was created correctly."""
    try:
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = cursor.fetchall()
        print(f"\nDatabase contains {len(tables)} tables:")

        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} rows")

    except sqlite3.Error as e:
        print(f"Error verifying database: {e}")
        raise


def main():
    """Main function to orchestrate database setup."""
    connection = None

    try:
        # Remove existing database if it exists
        if DATABASE_PATH.exists():
            print(f"Removing existing database: {DATABASE_PATH}\n")
            os.remove(DATABASE_PATH)

        # Create connection
        connection = create_connection()

        # Create tables
        create_tables(connection)

        # Load CSV files
        print("Loading CSV files into database...\n")
        load_csv_to_database(connection)

        # Verify database
        verify_database(connection)

        print("\n" + "=" * 60)
        print("Database setup complete and all CSVs imported.")
        print("=" * 60)
        print(f"\nDatabase location: {DATABASE_PATH}")

    except Exception as e:
        print(f"\nSetup failed with error: {e}")
        if connection:
            connection.rollback()

    finally:
        if connection:
            connection.close()
            print("Database connection closed")


if __name__ == "__main__":
    main()
