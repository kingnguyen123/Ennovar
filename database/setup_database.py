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
    "category.csv": {
        "table": "category",
        "columns": {
            "category_id": "category_id",
            "category_name": "category_name"
        }
    },
    "products.csv": {
        "table": "products",
        "columns": {
            "Product_ID": "product_id",
            "Product_Name": "product_name",
            "Category_ID": "category_id",
            "Launch_Date": "launch_date",
            "Price": "price"
        }
    },
    "sales.csv": {
        "table": "sales",
        "columns": {
            "sale_id": "sale_id",
            "sale_date": "sale_date",
            "store_id": "store_id",
            "product_id": "product_id",
            "quantity": "quantity"
        }
    },
    "stores.csv": {
        "table": "stores",
        "columns": {
            "Store_ID": "store_id",
            "Store_Name": "store_name",
            "City": "city",
            "Country": "country"
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

        # Create category table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                category_id INTEGER PRIMARY KEY,
                category_name TEXT NOT NULL
            )
        """)
        print("✓ Created 'category' table")

        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                category_id INTEGER,
                launch_date TEXT,
                price REAL,
                FOREIGN KEY (category_id) REFERENCES category(category_id)
            )
        """)
        print("✓ Created 'products' table")

        # Create stores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                store_id INTEGER PRIMARY KEY,
                store_name TEXT NOT NULL,
                city TEXT,
                country TEXT
            )
        """)
        print("✓ Created 'stores' table")

        # Create sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY,
                sale_date TEXT NOT NULL,
                store_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (store_id) REFERENCES stores(store_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        print("✓ Created 'sales' table")

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
            
            # Filter stores to only include United States
            if table_name == "stores" and "Country" in df.columns:
                original_count = len(df_subset)
                df_subset = df[df["Country"] == "United States"][available_columns].copy()
                print(f"  - Filtered stores: {original_count} -> {len(df_subset)} rows (Country == 'United States')")
            
            # Convert date format for sales table (DD-MM-YYYY to YYYY-MM-DD)
            if table_name == "sales" and "sale_date" in column_mapping.values():
                date_col = [k for k, v in column_mapping.items() if v == "sale_date"][0]
                if date_col in df_subset.columns:
                    df_subset[date_col] = pd.to_datetime(df_subset[date_col], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
                    print(f"  - Converted date format from DD-MM-YYYY to YYYY-MM-DD")
            
            df_subset.rename(columns=column_mapping, inplace=True)

            # Write to database
            df_subset.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"  ✓ Loaded {len(df_subset)} rows into '{table_name}' table")

        except pd.errors.EmptyDataError:
            print(f"  ✗ Error: {csv_file} is empty")
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
