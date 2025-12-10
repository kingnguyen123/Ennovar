"""
Database Query Examples

This script demonstrates how to query the SQLite database and work with the data.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "database.db"


def query_database_examples():
    """Run example queries on the database."""
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        print("✓ Connected to database\n")

        # Example 1: Get product information
        print("=" * 60)
        print("Example 1: Products Information")
        print("=" * 60)
        query = "SELECT id, description, price FROM products LIMIT 5"
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        print()

        # Example 2: Get store information
        print("=" * 60)
        print("Example 2: Store Information")
        print("=" * 60)
        query = "SELECT id, name, city, country, num_employees FROM stores LIMIT 5"
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        print()

        # Example 3: Get discount information
        print("=" * 60)
        print("Example 3: Active Discounts")
        print("=" * 60)
        query = """
            SELECT category, sub_category, discount_rate, 
                   start_date, end_date FROM discounts LIMIT 5
        """
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        print()

        # Example 4: Get transaction information
        print("=" * 60)
        print("Example 4: Recent Transactions")
        print("=" * 60)
        query = """
            SELECT product_id, store_id FROM transactions LIMIT 5
        """
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        print()

        # Example 5: Sales summary by store
        print("=" * 60)
        print("Example 5: Total Transactions by Store")
        print("=" * 60)
        query = """
            SELECT s.name, COUNT(t.product_id) as total_transactions
            FROM transactions t
            JOIN stores s ON t.store_id = s.id
            GROUP BY s.id
            ORDER BY total_transactions DESC
            LIMIT 10
        """
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        print()

        # Example 6: Top selling products
        print("=" * 60)
        print("Example 6: Top 10 Most Frequent Products in Transactions")
        print("=" * 60)
        query = """
            SELECT p.id, p.description, COUNT(t.product_id) as times_sold
            FROM transactions t
            JOIN products p ON t.product_id = p.id
            GROUP BY p.id
            ORDER BY times_sold DESC
            LIMIT 10
        """
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        print()

        # Example 7: Database statistics
        print("=" * 60)
        print("Example 7: Database Statistics")
        print("=" * 60)
        stats = {
            "Total Products": pd.read_sql_query("SELECT COUNT(*) as count FROM products", conn)["count"][0],
            "Total Stores": pd.read_sql_query("SELECT COUNT(*) as count FROM stores", conn)["count"][0],
            "Total Transactions": pd.read_sql_query("SELECT COUNT(*) as count FROM transactions", conn)["count"][0],
            "Active Discounts": pd.read_sql_query("SELECT COUNT(*) as count FROM discounts", conn)["count"][0],
        }
        for key, value in stats.items():
            print(f"{key}: {value:,}")

    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
    finally:
        if conn:
            conn.close()
            print("✓ Database connection closed")


if __name__ == "__main__":
    query_database_examples()
