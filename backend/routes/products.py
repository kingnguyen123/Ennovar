from flask import Blueprint, request, jsonify
from backend.utils.database import (
    get_sizes,
    get_categories,
    get_subcategories,
    get_subcategory_by_category,
    get_sizes_by_category_subcategory,
    get_category_sales,
    get_sub_category_sales,
    get_sub_category_sales_based_on_category,
    get_sub_category_sales_based_on_category_and_size
)

products_bp= Blueprint("products",__name__, url_prefix="/api/products")


#GET endpoints for filters
@products_bp.route("/categories",methods=["GET"])
def api_get_categories():
    df=get_categories()
    return jsonify(df.to_dict(orient="records"))


@products_bp.route("/sub_categories",methods=["GET"])
def api_get_subcategories():
    df=get_subcategories()
    return jsonify(df.to_dict(orient="records"))


@products_bp.route("/size",methods=["GET"])
def api_get_size():
    df=get_sizes()
    return jsonify(df.to_dict(orient="records"))

@products_bp.route("/subcategories/<category>",methods=["GET"])
def api_get_subcategory_by_category(category):
    df=get_subcategory_by_category(category=category)
    return  jsonify(df.to_dict(orient="records"))

@products_bp.route("/sizes/<category>/<sub_category>",methods=["GET"])
def api_get_sizes_by_category_subcategory(category, sub_category):
    df=get_sizes_by_category_subcategory(category=category,sub_category=sub_category)
    return jsonify(df.to_dict(orient="records"))


#GET endpoints for sales
@products_bp.route("/sales/category",methods=['POST'])
def api_get_category_sales():
    data=request.json
    category=data.get("category")
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    df=get_category_sales(category=category,start_date=start_date,end_date=end_date)
    return jsonify(df.to_dict(orient='records'))

@products_bp.route("/sales/subcategory", methods=['POST'])
def api_get_sub_category_sales():
    data = request.get_json()
    sub_category = data.get('sub_category')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    df = get_sub_category_sales(sub_category=sub_category, start_date=start_date, end_date=end_date)
    return jsonify(df.to_dict(orient='records'))


@products_bp.route("/sales/subcategory-by-category", methods=['POST'])
def api_get_sub_category_sales_based_on_category():
    data = request.get_json()
    sub_category = data.get('sub_category')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    df = get_sub_category_sales_based_on_category(sub_category=sub_category, start_date=start_date, end_date=end_date)
    return jsonify(df.to_dict(orient='records'))


@products_bp.route("/sales/subcategory-by-category-size", methods=['POST'])
def api_get_sub_category_sales_based_on_category_and_size():
    data = request.get_json()
    sub_category = data.get('sub_category')
    size = data.get('size')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    df = get_sub_category_sales_based_on_category_and_size(sub_category=sub_category, size=size, start_date=start_date,
                                                           end_date=end_date)
    return jsonify(df.to_dict(orient='records'))
