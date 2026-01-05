from flask import Blueprint, request, jsonify
from backend.utils.database import (
    get_categories,
    get_products,
    get_products_by_category
)

products_bp = Blueprint("products", __name__, url_prefix="/api/products")


# GET endpoints for filters
@products_bp.route("/categories", methods=["GET"])
def api_get_categories():
    """Get all unique categories"""
    df = get_categories()
    return jsonify(df.to_dict(orient="records"))


@products_bp.route("/products", methods=["GET"])
def api_get_products():
    """Get all products"""
    df = get_products()
    return jsonify(df.to_dict(orient="records"))


@products_bp.route("/products/<category>", methods=["GET"])
def api_get_products_by_category(category):
    """Get products filtered by category"""
    df = get_products_by_category(category=category)
    return jsonify(df.to_dict(orient="records"))
