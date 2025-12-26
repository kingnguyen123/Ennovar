from flask import Blueprint, request, jsonify
from backend.utils.database import (
    get_sub_category_inventory_based_on_category,
    get_sub_category_inventory_based_on_category_and_size
)
import logging
logger = logging.getLogger(__name__)
inventory_bp = Blueprint("inventory", __name__, url_prefix="/api/inventory")

@inventory_bp.route("/subcategory-by-category-size", methods=['POST'])
def api_get_sub_category_inventory_based_on_category_and_size():
    data = request.get_json()
    category = data.get('category')
    sub_category = data.get('sub_category')
    size = data.get('size')
    
    
    # If size is empty or '0', call the function without size filter
    if not size or size == '0' or size == '':
        df = get_sub_category_inventory_based_on_category(
            category=category,
            sub_category=sub_category,
        
        )
    else:
        df = get_sub_category_inventory_based_on_category_and_size(
            category=category,
            sub_category=sub_category,
            size=size
        )
    return jsonify(df.to_dict(orient='records'))