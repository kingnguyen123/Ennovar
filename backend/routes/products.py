from flask import Blueprint, request, jsonify
from backend.utils.database import (
    get_sizes,
    get_categories,
    get_subcategories,
    get_subcategory_by_category,
    get_sizes_by_category_subcategory
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
