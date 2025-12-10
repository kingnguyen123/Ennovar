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
            "Product ID": "product_id",
            "Category": "category",
            "Sub Category": "sub_category",
            "Production Cost": "price",
        }
    },
    "discounts.csv": {
        "table": "discounts",
        "columns": {
            "Start": "start_date",
            "End": "end_date",
            "Discount": "discount_rate",
            "Description": "description",
            "Category": "category",
            "Sub Category": "sub_category",
        }
    },
    "stores.csv": {
        "table": "stores",
        "columns": {
            "Store ID": "Store ID",
            "Store Name": "Store Name",
            "Country": "Country",
            "City": "City"
        }
    },
    "transactions.csv": {
        "table": "transactions",
        "columns": {
            "Transaction ID": "id",
            "Product ID": "product_id",
            "Size":"Size",
            "Unit Price":"Unit Price",
            "Date":"Date",
            "Discount":"Discount",
            "Line Total":"Line Total",
            "Store ID":"Store ID",
            "Currency":"Currency",
            "SKU":"SKU",
            "Invoice Total":"Invoice Total",
            }
    }
}


def create_connection():
    """Create a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        print(f"✓ Connected to database: {DATABASE_PATH}")
        return conn
    except sqlite3.Error as e:
        print(f"✗ Error connecting to database: {e}")
        raise


def create_tables(conn):
    """Create tables in the database."""
    try:
        cursor = conn.cursor()

        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                category TEXT,
                sub_category TEXT,
                description TEXT,
                price REAL
            )
        """)
        print("✓ Created 'products' table")

        # Create discounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_date TEXT,
                end_date TEXT,
                discount_rate REAL,
                description TEXT,
                category TEXT,
                sub_category TEXT
            )
        """)
        print("✓ Created 'discounts' table")

        # Create stores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY,
                name TEXT,
                country TEXT,
                city TEXT,
                num_employees INTEGER,
                latitude REAL,
                longitude REAL
            )
        """)
        print("✓ Created 'stores' table")

        # Create transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                store_id INTEGER,
                quantity INTEGER,
                total_amount REAL,
                transaction_date TEXT,
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (store_id) REFERENCES stores(id)
            )
        """)
        print("✓ Created 'transactions' table")

        conn.commit()
        print("\n✓ All tables created successfully\n")

    except sqlite3.Error as e:
        print(f"✗ Error creating tables: {e}")
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
                print(f" Warning: {csv_file} not found at {csv_path}")
                continue

            df = pd.read_csv(csv_path)
            print(f"  - Read {len(df)} rows from {csv_file}")

            # Select and rename columns
            available_columns = [col for col in column_mapping.keys() if col in df.columns]
            if not available_columns:
                print(f" Warning: No matching columns found in {csv_file}")
                continue

            df_subset = df[available_columns].copy()

            # Filter transactions table for specific sizes and USD currency
            if table_name == "transactions":
                allowed_sizes = ['M', 'L', 'S', 'XL', 'XXL']
                original_count = len(df_subset)
                df_subset = df_subset[
                    (df_subset['Size'].isin(allowed_sizes)) &
                    (df_subset['Currency'] == 'USD')
                ]
                print(f"  - Filtered transactions: {original_count} -> {len(df_subset)} rows (Size in {allowed_sizes}, Currency=USD)")

            df_subset.rename(columns=column_mapping, inplace=True)

            # Write to database
            df_subset.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f" Loaded {len(df_subset)} rows into '{table_name}' table")

        except pd.errors.EmptyDataError:
            print(f" Error: {csv_file} is empty")
        except KeyError as e:
            print(f" Error: Missing column {e} in {csv_file}")
        except Exception as e:
            print(f" Error loading {csv_file}: {e}")
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
        print(f"\n✓ Database contains {len(tables)} tables:")

        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} rows")

    except sqlite3.Error as e:
        print(f"✗ Error verifying database: {e}")
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
        print("✓ Database setup complete and all CSVs imported.")
        print("=" * 60)
        print(f"\nDatabase location: {DATABASE_PATH}")

    except Exception as e:
        print(f"\n✗ Setup failed with error: {e}")
        if connection:
            connection.rollback()

    finally:
        if connection:
            connection.close()
            print("✓ Database connection closed")


if __name__ == "__main__":
    main()
