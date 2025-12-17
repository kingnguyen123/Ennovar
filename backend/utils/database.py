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
    """Get sizes available for a specific category and sub_category"""
    sql= "SELECT DISTINCT t.Size FROM transactions t JOIN products p ON t.product_id = p.product_id WHERE p.category = ? AND p.sub_category= ? ORDER BY t.Size"
    return query_db(sql, (category, sub_category))


#Query for the total sales of the products
def get_category_sales(category, start_date, end_date):
    """Get the total sales of each category"""
    query = """
        SELECT
            p.category,
            SUM(t.invoice_total) AS total_sales
        FROM products p
        JOIN transactions t ON p.product_id = t.product_id
        WHERE p.category = ?
        AND t.transaction_date BETWEEN ? AND ?
        GROUP BY p.category
    """
    return query_db(query, (category, start_date, end_date))

def get_sub_category_sales(sub_category, start_date, end_date):
    """Get the total sales of each sub_category"""
    query = """
        SELECT
            p.sub_category,
            SUM(t.invoice_total) AS total_sales
        FROM products p
        JOIN transactions t ON p.product_id = t.product_id
        WHERE p.sub_category = ?
        AND t.transaction_date BETWEEN ? AND ?
        GROUP BY p.sub_category
    """
    return query_db(query, (sub_category, start_date, end_date))


def get_sub_category_sales_based_on_category(sub_category, start_date, end_date):
    query = """ \
            SELECT p.category, \
                   p.sub_category, \
                   SUM(t.invoice_total) AS total_sales \
            FROM products p \
                     JOIN transactions t ON p.product_id = t.product_id \
            WHERE p.sub_category = ? \
                AND t.transaction_date BETWEEN ? AND ? \
            GROUP BY p.category, p.sub_category \
            ORDER BY p.sub_category
    """
    return query_db(query, (sub_category, start_date, end_date))


def get_sub_category_sales_based_on_category_and_size(sub_category, size, start_date, end_date):
    query = """ \
            SELECT p.category, \
                   p.sub_category, \
                   t.Size, \
                   SUM(t.invoice_total) AS total_sales \
            FROM products p \
                     JOIN transactions t ON p.product_id = t.product_id \
            WHERE p.sub_category = ? \
                AND t.Size = ? \
                AND t.transaction_date BETWEEN ? AND ? \
            GROUP BY p.category, p.sub_category, t.Size \
            ORDER BY p.sub_category, t.Size
    """
    return query_db(query, (sub_category, size, start_date, end_date))