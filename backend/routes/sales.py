from flask import Blueprint, request, jsonify
from backend.utils.database import (
    # get_category_sales,
    # get_sub_category_sales,
    get_sub_category_sales_based_on_category,
    get_sub_category_sales_based_on_category_and_size,
    get_year_range
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

# ## check the logic:Because we follow on the SKU architecture, so the sales is only focus on each sub_category
# @sales_bp.route('/api/sales/category-sales', methods=['POST'])
# def get_category_sales_endpoint():
#     """Get total sales for a specific category"""
#     data = request.json
#     logger.info(f"Request received: {data}")
    
#     try:
#         result = get_category_sales(
#             data['category'],           
#             data['start_date'],
#             data['end_date']
#         )
#         logger.info(f"Query result: {result.to_dict()}")
#         return result.to_json(orient='records')
#     except Exception as e:
#         logger.error(f"Error in get_category_sales: {e}", exc_info=True)
#         return {'error': str(e)}, 500


# @sales_bp.route("/subcategory", methods=['POST'])
# def api_get_sub_category_sales():
#     """
#     Get sales data for a specific sub-category within a date range.
    
#     Expected JSON payload:
#         {
#             "sub_category": str - Product sub-category name
#             "start_date": str - Start date for sales data
#             "end_date": str - End date for sales data
#         }
    
#     Returns:
#         JSON list of sales records for the specified sub-category
#     """
#     data = request.get_json()
#     sub_category = data.get('sub_category')
#     start_date = data.get('start_date')
#     end_date = data.get('end_date')
#     df = get_sub_category_sales(sub_category=sub_category, start_date=start_date, end_date=end_date)
#     return jsonify(df.to_dict(orient='records'))


# @sales_bp.route("/subcategory-by-category", methods=['POST'])
# def api_get_sub_category_sales_based_on_category():
#     """
#     Get sales data for a specific sub-category filtered by its parent category within a date range.
#     
#     Expected JSON payload:
#         {
#             "sub_category": str - Product sub-category name
#             "start_date": str - Start date for sales data
#             "end_date": str - End date for sales data
#         }
#     
#     Returns:
#         JSON list of sales records for the specified sub-category with category context
#     """
#     data = request.get_json()
#     category = data.get('category')
#     sub_category = data.get('sub_category')
#     start_date = data.get('start_date')
#     end_date = data.get('end_date')
#     df = get_sub_category_sales_based_on_category(category=category,sub_category=sub_category, start_date=start_date, end_date=end_date)
#     return jsonify(df.to_dict(orient='records'))


@sales_bp.route("/subcategory-by-category-size", methods=['POST'])
def api_get_sub_category_sales_based_on_category_and_size():
    """
    Get sales data for a specific sub-category and size combination filtered by category within a date range.
    If size is empty or '0', returns sales for all sizes in the sub-category.
    
    Expected JSON payload:
        {
            "sub_category": str - Product sub-category name
            "size": str - Product size (optional, if empty/'0' returns all sizes)
            "start_date": str - Start date for sales data
            "end_date": str - End date for sales data
        }
    
    Returns:
        JSON list of sales records for the specified sub-category and size with category context
    """
    data = request.get_json()
    category = data.get('category')
    sub_category = data.get('sub_category')
    size = data.get('size')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    # If size is empty or '0', call the function without size filter
    if not size or size == '0' or size == '':
        df = get_sub_category_sales_based_on_category(
            category=category,
            sub_category=sub_category,
            start_date=start_date,
            end_date=end_date
        )
    else:
        df = get_sub_category_sales_based_on_category_and_size(
            category=category,
            sub_category=sub_category,
            size=size,
            start_date=start_date,
            end_date=end_date
        )
    return jsonify(df.to_dict(orient='records'))
 