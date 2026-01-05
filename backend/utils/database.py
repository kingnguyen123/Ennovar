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
    """Get all unique categories from category table"""
    sql = "SELECT DISTINCT category_name FROM category ORDER BY category_name"
    return query_db(sql)


def get_products():
    """Get all products from products table"""
    sql = "SELECT DISTINCT product_name FROM products ORDER BY product_name"
    return query_db(sql)


def get_products_by_category(category):
    """ Get the product based on category"""
    sql = "SELECT DISTINCT p.product_name FROM products p INNER JOIN category c ON p.category_id = c.category_id WHERE c.category_name = ? ORDER BY p.product_name"
    return query_db(sql, (category,))


def get_year_range():
    """Get min and max years from sales table"""
    sql = """
        SELECT 
            CAST(strftime('%Y', MIN(sale_date)) AS INTEGER) AS min_year,
            CAST(strftime('%Y', MAX(sale_date)) AS INTEGER) AS max_year
        FROM sales
    """
    return query_db(sql)


def get_the_total_product_sales_based_on_category(category, product, start_date, end_date):
    """return the total quantity sold, total revenue and price of that product"""
    query = """
        SELECT 
            p.product_name,
            c.category_name,
            SUM(s.quantity) AS total_quantity_sold,
            p.price,
            SUM(s.quantity * p.price) AS total_revenue
        FROM sales s
        INNER JOIN products p ON s.product_id = p.product_id
        INNER JOIN category c ON p.category_id = c.category_id
        WHERE c.category_name = ? 
            AND p.product_name = ?
            AND s.sale_date >= ?
            AND s.sale_date <= ?
        GROUP BY p.product_id, p.product_name, c.category_name, p.price
    """
    return query_db(query, (category, product, start_date, end_date))


def get_sales_pattern_by_date(category, product, start_date, end_date):
    """
    Get daily sales pattern for a specific product within a date range.
    Returns sales aggregated by date for time series visualization.
    """
    query = """
        SELECT
            s.sale_date,
            SUM(s.quantity * p.price) AS total_sales,
            SUM(s.quantity) AS total_quantity
        FROM sales s
        INNER JOIN products p ON s.product_id = p.product_id
        INNER JOIN category c ON p.category_id = c.category_id
        WHERE c.category_name = ?
            AND p.product_name = ?
            AND s.sale_date >= ?
            AND s.sale_date <= ?
        GROUP BY s.sale_date
        ORDER BY s.sale_date
    """
    return query_db(query, (category, product, start_date, end_date))