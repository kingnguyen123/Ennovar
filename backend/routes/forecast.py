from flask import Blueprint, request, jsonify
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add model directory to path
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'model')
sys.path.insert(0, model_path)

from demand_forecasting_model import DemandForecastingModel

forecast_bp = Blueprint("forecast", __name__, url_prefix="/api/forecast")

# Global model instance (loaded once at startup)
_model = None
_model_loaded = False

def get_model():
    """Load model once and cache it."""
    global _model, _model_loaded
    if not _model_loaded:
        try:
            _model = DemandForecastingModel()
            model_dir = os.path.join(model_path, 'saved_models')
            _model.load_model(model_dir)
            _model_loaded = True
            print("✓ Forecasting model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading forecasting model: {e}")
            _model = None
    return _model


@forecast_bp.route("/predict", methods=['POST'])
def predict_demand():
    """
    Generate demand forecast for a selected product and horizon.
    
    Expected JSON payload:
        {
            "category": str - Product category name from database
            "product": str - Product name from database (optional)
            "horizon": int - Forecast horizon in days (7, 14, or 30)
        }
    
    Returns:
        JSON object with forecast results
    """
    try:
        data = request.get_json()
        category = data.get('category')
        product_name = data.get('product')
        horizon = data.get('horizon', 7)
        
        if not category:
            return jsonify({'error': 'Category is required'}), 400
        
        # Validate horizon
        if horizon not in [7, 14, 30]:
            return jsonify({'error': 'Horizon must be 7, 14, or 30 days'}), 400
        
        # Load model
        model = get_model()
        if model is None:
            return jsonify({'error': 'Forecasting model not available'}), 500
        
        # Get SKU(s) from database based on category and product selection
        import sqlite3
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               'database', 'database.db')
        
        if not os.path.exists(db_path):
            return jsonify({'error': 'Database not found'}), 500
        
        conn = sqlite3.connect(db_path)
        
        # Get SKUs and product info from database
        if product_name:
            # Specific product selected
            query = """
                SELECT sku_id, product_name, category 
                FROM products 
                WHERE product_name = ? AND category = ?
            """
            product_info_df = pd.read_sql_query(query, conn, params=(product_name, category))
        else:
            # All products in category
            query = """
                SELECT sku_id, product_name, category 
                FROM products 
                WHERE category = ?
            """
            product_info_df = pd.read_sql_query(query, conn, params=(category,))
        
        conn.close()
        
        if len(product_info_df) == 0:
            return jsonify({'error': 'No products found in database for selected category/product'}), 404
        
        # Get list of SKUs to filter training data
        sku_list = product_info_df['sku_id'].tolist()
        
        # Create SKU to product name mapping for display
        sku_to_product = dict(zip(product_info_df['sku_id'], product_info_df['product_name']))
        
        # Load the training data
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 'data', 'xg_df.csv')
        
        if not os.path.exists(data_path):
            return jsonify({'error': 'Training data not found'}), 500
        
        df = pd.read_csv(data_path)
        
        # Drop unnamed column if exists
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
        
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Filter training data by SKUs from database
        filtered_df = df[df['sku_id'].isin(sku_list)].copy()
        
        if len(filtered_df) == 0:
            return jsonify({'error': 'No training data found for selected product(s). The product may not have historical data.'}), 404
        
        # Get the most recent data for the horizon
        max_date = filtered_df['Date'].max()
        forecast_start = max_date - pd.Timedelta(days=horizon - 1)
        forecast_df = filtered_df[filtered_df['Date'] >= forecast_start].copy()
        
        if len(forecast_df) == 0:
            return jsonify({'error': f'Insufficient data for {horizon}-day forecast'}), 400
        
        # Generate predictions
        predictions = model.predict(forecast_df)
        
        # Prepare response using product names from database
        results = []
        for idx, (_, row) in enumerate(forecast_df.iterrows()):
            sku_id = row['sku_id']
            # Get actual product name from database mapping
            display_product_name = sku_to_product.get(sku_id, f"Unknown SKU: {sku_id}")
            
            results.append({
                'date': row['Date'].strftime('%Y-%m-%d'),
                'sku_id': sku_id,
                'product_name': display_product_name,
                'category': category,
                'actual_quantity': float(row['quantity']) if 'quantity' in row else None,
                'predicted_quantity': float(predictions[idx]),
                'forecast_horizon': horizon
            })
        
        # Calculate summary metrics
        if 'quantity' in forecast_df.columns:
            total_actual = float(np.sum(forecast_df['quantity'].values))
            total_predicted = float(np.sum(predictions))
            
            summary = {
                'total_actual': total_actual,
                'total_predicted': total_predicted
            }
        else:
            summary = {
                'total_predicted': float(np.sum(predictions))
            }
        
        return jsonify({
            'success': True,
            'forecast': results,
            'summary': summary,
            'horizon': horizon,
            'category': category,
            'product': product_name,
            'forecast_start': forecast_start.strftime('%Y-%m-%d'),
            'forecast_end': max_date.strftime('%Y-%m-%d')
        })
        
    except Exception as e:
        print(f"Error in forecast prediction: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@forecast_bp.route("/status", methods=['GET'])
def model_status():
    """Check if the forecasting model is loaded and available."""
    model = get_model()
    if model is not None:
        return jsonify({
            'status': 'available',
            'model_type': 'XGBoost',
            'supported_horizons': [7, 14, 30],
            'trained_at': model.model_metadata.get('trained_at', 'Unknown')
        })
    else:
        return jsonify({
            'status': 'unavailable',
            'message': 'Model not loaded. Please train the model first.'
        }), 503
