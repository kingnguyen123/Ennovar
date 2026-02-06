import sqlite3
import pandas as pd
from typing import Optional
from datetime import date, timedelta
import calendar

DB_PATH = "database/database.db"

def query_db(sql, params=()):
    """
    Execute a SELECT query and return pandas DataFrame
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql=sql, con=conn, params=params)
        conn.close()
        return df
    except Exception as e:
        print(f"Database error {e}")
        return pd.DataFrame()

def get_categories():
    """Get all unique categories from products table"""
    sql = "SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category"
    df = query_db(sql)
    # Rename column to match expected format
    df.rename(columns={'category': 'category_name'}, inplace=True)
    return df


def get_products():
    """Get all products from products table"""
    sql = "SELECT DISTINCT product_name FROM products ORDER BY product_name"
    return query_db(sql)


def get_products_by_category(category):
    """Get the products based on category"""
    sql = "SELECT DISTINCT product_name FROM products WHERE category = ? ORDER BY product_name"
    return query_db(sql, (category,))


def get_year_range():
    """Get min and max years from sales table"""
    sql = """
        SELECT 
            CAST(strftime('%Y', MIN(date)) AS INTEGER) AS min_year,
            CAST(strftime('%Y', MAX(date)) AS INTEGER) AS max_year
        FROM sales
    """
    return query_db(sql)


def get_the_total_product_sales_based_on_category(category, product, start_date, end_date):
    """return the total quantity sold, total revenue and price of that product"""
    query = """
        SELECT 
            p.product_name,
            p.category AS category_name,
            SUM(s.quantity) AS total_quantity_sold,
            p.default_price AS price,
            SUM(s.net_revenue) AS total_revenue
        FROM sales s
        INNER JOIN products p ON s.sku_id = p.sku_id
        WHERE p.category = ? 
            AND p.product_name = ?
            AND s.date >= ?
            AND s.date <= ?
        GROUP BY p.sku_id, p.product_name, p.category, p.default_price
    """
    return query_db(query, (category, product, start_date, end_date))


def get_sales_pattern_by_date(category, product, start_date, end_date):
    """
    Get daily sales pattern for a specific product within a date range.
    Returns sales aggregated by date for time series visualization.
    """
    query = """
        SELECT
            s.date AS sale_date,
            SUM(s.net_revenue) AS total_sales,
            SUM(s.quantity) AS total_quantity
        FROM sales s
        INNER JOIN products p ON s.sku_id = p.sku_id
        WHERE p.category = ?
            AND p.product_name = ?
            AND s.date >= ?
            AND s.date <= ?
        GROUP BY s.date
        ORDER BY s.date
    """
    return query_db(query, (category, product, start_date, end_date))