"""
Quick test of the production inference pipeline.
This script tests all three forecast horizons automatically.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from demand_forecasting_model import DemandForecastingModel
import pandas as pd


def test_inference():
    """Test the inference pipeline with all horizons."""
    print("="*70)
    print("TESTING PRODUCTION INFERENCE PIPELINE")
    print("="*70)
    
    DATA_PATH = r"C:\Users\kingd\Ennovar\data\xg_df.csv"
    MODEL_DIR = "saved_models"
    
    # Check if model exists
    if not os.path.exists(os.path.join(MODEL_DIR, "xgboost_model.json")):
        print(f"\n✗ Error: No trained model found in '{MODEL_DIR}/'")
        return False
    
    # Load model
    print("\n[1/2] Loading trained model...")
    model = DemandForecastingModel()
    model.load_model(MODEL_DIR)
    
    # Load data
    print("\n[2/2] Testing inference on all horizons...")
    df = pd.read_csv(DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    
    horizons = [7, 14, 30]
    results = []
    
    for horizon in horizons:
        print(f"\n{'='*70}")
        print(f"Testing {horizon}-day forecast...")
        print(f"{'='*70}")
        
        # Get data for this horizon
        max_date = df['Date'].max()
        forecast_start = max_date - pd.Timedelta(days=horizon - 1)
        forecast_df = df[df['Date'] >= forecast_start].copy()
        
        print(f"  Forecast period: {forecast_start.date()} to {max_date.date()}")
        print(f"  Data points: {len(forecast_df):,}")
        
        # Make predictions
        predictions = model.predict(forecast_df)
        
        # Calculate metrics
        if 'quantity' in forecast_df.columns:
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
            import numpy as np
            
            actuals = forecast_df['quantity'].values
            mae = mean_absolute_error(actuals, predictions)
            rmse = np.sqrt(mean_squared_error(actuals, predictions))
            r2 = r2_score(actuals, predictions)
            
            print(f"\n  Performance:")
            print(f"    MAE:  {mae:.4f}")
            print(f"    RMSE: {rmse:.4f}")
            print(f"    R²:   {r2:.4f}")
            
            results.append({
                'horizon': horizon,
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'predictions': len(predictions)
            })
    
    # Print summary
    print("\n" + "="*70)
    print("✓ INFERENCE TEST COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\nSummary of all forecast horizons:")
    for result in results:
        print(f"  {result['horizon']}-day: MAE={result['mae']:.4f}, RMSE={result['rmse']:.4f}, R²={result['r2']:.4f} ({result['predictions']:,} predictions)")
    
    return True


if __name__ == "__main__":
    try:
        success = test_inference()
        if success:
            print("\n✓ All tests passed!")
            sys.exit(0)
        else:
            print("\n✗ Tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
