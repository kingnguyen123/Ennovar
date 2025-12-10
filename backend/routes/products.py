from flask import Blueprint, request, jsonify
from backend.utils.database import (
    get_subcategory_by_category,
    get_sizes_by_category_subcategory,
    get_sizes,
    get_categories,
    get_subcategories
)

products_bp= Blueprint("products",__name__, url_prefix="/api/products")

#Set a route for get_all_categories
@products_bp.route("/categories",methods=['GET'])
def get_all_categories():
    """
    Get all available categories
    """
    try:
        df=get_categories()
        if df.empty:
            return jsonify({"Error":"No category found"}),404

        categories = df['category'].tolist()
        return jsonify({
            "status":"Success",
            "data":{
                "categories": categories,
                "count": len(categories)
            }
        }),200
    except Exception as e:
        return jsonify({"Error":str(e)}),500

@products_bp.route("/subcategories",methods=['GET'])
def get_all_sub_categories():
    """
    Get all available sub categories
    """
    try:
        df = get_subcategories()
        if df.empty:
            return jsonify({"Error": "No sub category found"}), 404

        sub_categories = df['sub_category'].tolist()
        return jsonify({
            "status": "Success",
            "data": {
                "sub_category": sub_categories,
                "count": len(sub_categories)
            }
        }), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

@products_bp.route('/sizes', methods=['GET'])
def get_all_size():
    """
    Get all available sizes
    """
    try:
        df = get_sizes()
        if df.empty:
            return jsonify({"Error": "No sizes found"}), 404

        sizes = df['Size'].tolist()
        return jsonify({
            "status": "Success",
            "data": {
                "sizes": sizes,
                "count": len(sizes)
            }
        }), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

@products_bp.route('/sizes-filtered', methods=['GET'])
def get_all_sizes_by_category_subcategory():
    """
     Get sizes available for a specific category and subcategory
    """
    category= request.args.get("category")
    sub_category=request.args.get("sub_category")

    #validate parameter
    if not category or not sub_category:
        return jsonify({
            "status":"Error",
            "Error":"Category and sub category is missing"
        }),400
    try:
        df=get_sizes_by_category_subcategory(category,sub_category)
        if df.empty:
            return jsonify({"Error": "No sizes found"}), 404

        sizes = df['Size'].tolist()
        return jsonify({
            "status": "Success",
            "data": {
                "sizes": sizes,
                "category": category,
                "subcategory": sub_category,
                "count": len(sizes)
            }
        }), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500



@products_bp.route("/subcategories-filtered",methods=['GET'])
def get_filtered_sub_categories():
    """
    Get all available sub_categories for a specific category
    """
    category = request.args.get("category")
    try:
        df = get_subcategory_by_category(category)
        if df.empty:
            return jsonify({"Error": "No sub category found"}), 404

        sub_categories = df['sub_category'].tolist()
        return jsonify({
            "status": "Success",
            "data": {
                "sub_category": sub_categories,
                "category": category,
                "count": len(sub_categories)
            }
        }), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

