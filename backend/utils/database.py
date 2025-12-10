import sqlite3
import pandas as pd

DB_PATH = "database/database.db"
def query_db(sql, params=()):
    """
    Execute a SELECT query and return pandas DataFrame
    """
    try:
        conn= sqlite3.connect(DB_PATH)
        df= pd.read_sql_query(sql=sql, con=conn, params=params)
        conn.close()
        return df
    except Exception as e:
        print(f"Database error {e}")
        return pd.DataFrame()

def get_categories():
    """Get all unique categories from products table"""
    sql = "SELECT DISTINCT category FROM products ORDER BY category"
    return query_db(sql)


def get_subcategories():
    """Get all subcategories"""
    sql = "SELECT DISTINCT sub_category FROM products ORDER BY sub_category"
    return query_db(sql)


def get_sizes():
    """Get all unique sizes from transactions"""
    sql = "SELECT DISTINCT Size FROM transactions WHERE Size IS NOT NULL ORDER BY Size"
    return query_db(sql)

def get_subcategory_by_category(category):
    sql = "SELECT DISTINCT sub_category FROM products WHERE category = ? ORDER BY sub_category"
    return query_db(sql, (category,))

def get_sizes_by_category_subcategory(category, sub_category):
    """
    Get sizes available for a specific category and sub_category
    """
    sql= "SELECT DISTINCT t.size FROM transactions t JOIN products p ON t.product_id = p.product_id WHERE p.category = ? AND p.sub_category= ? ORDER BY  t.size"
    return query_db(sql, (category, sub_category))

