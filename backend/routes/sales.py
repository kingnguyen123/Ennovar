from flask import Blueprint, request, jsonify
from backend.utils.database import (
    get_year_range,
    get_the_total_product_sales_based_on_category,
    get_sales_pattern_by_date
)
import logging

logger = logging.getLogger(__name__)
sales_bp = Blueprint("sales", __name__, url_prefix="/api/sales")


@sales_bp.route("/year-range", methods=['GET'])
def api_get_year_range():
    """
    Get the year range available in the database.
    
    Returns:
        JSON object with min_year and max_year
        {
            "min_year": int - Earliest year in database
            "max_year": int - Latest year in database
        }
    """
    df = get_year_range()
    return jsonify(df.to_dict(orient='records')[0])


@sales_bp.route("/product-sales", methods=['POST'])
def api_get_product_sales():
    """
    Get total sales data for a specific product within a category and date range.
    
    Expected JSON payload:
        {
            "category": str - Product category name
            "product": str - Product name
            "start_date": str - Start date for sales data (YYYY-MM-DD)
            "end_date": str - End date for sales data (YYYY-MM-DD)
        }
    
    Returns:
        JSON list with product sales summary including:
        - product_name
        - category_name
        - total_quantity_sold
        - price
        - total_revenue
    """
    data = request.get_json()
    category = data.get('category')
    product = data.get('product')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    df = get_the_total_product_sales_based_on_category(
        category=category,
        product=product,
        start_date=start_date,
        end_date=end_date
    )
    return jsonify(df.to_dict(orient='records'))


@sales_bp.route("/sales-pattern", methods=['POST'])
def api_get_sales_pattern():
    """
    Get daily sales pattern for a specific product within a date range.
    
    Expected JSON payload:
        {
            "category": str - Product category name
            "product": str - Product name
            "start_date": str - Start date for sales data (YYYY-MM-DD)
            "end_date": str - End date for sales data (YYYY-MM-DD)
        }
    
    Returns:
        JSON list of daily sales records with:
        - sale_date
        - total_sales (revenue)
        - total_quantity
    """
    data = request.get_json()
    category = data.get('category')
    product = data.get('product')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    df = get_sales_pattern_by_date(
        category=category,
        product=product,
        start_date=start_date,
        end_date=end_date
        
    )
    
    return jsonify(df.to_dict(orient='records'))
 