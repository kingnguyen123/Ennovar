"""
Production Inference Script for Demand Forecasting

This script loads the trained model and generates forecasts for user-selected horizons.
No retraining occurs - uses the pre-trained model artifacts.

Usage:
    python predict.py
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from demand_forecasting_model import DemandForecastingModel


def load_inference_data(data_path: str, forecast_horizon: int) -> pd.DataFrame:
    """
    Load data for making predictions.
    
    Args:
        data_path: Path to the data CSV
        forecast_horizon: Number of days to forecast
        
    Returns:
        Dataframe with data for the forecast period
    """
    print(f"Loading data for {forecast_horizon}-day forecast...")
    df = pd.read_csv(data_path)
    
    # Drop unnamed index column if it exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    # Convert Date to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Get the most recent data for forecasting
    max_date = df['Date'].max()
    forecast_start = max_date - pd.Timedelta(days=forecast_horizon - 1)
    
    # Filter data for the forecast period
    forecast_df = df[df['Date'] >= forecast_start].copy()
    
    print(f"Forecast period: {forecast_start.date()} to {max_date.date()}")
    print(f"Data shape: {forecast_df.shape}")
    print(f"Unique SKUs: {forecast_df['sku_id'].nunique()}")
    
    return forecast_df


def generate_forecast(model: DemandForecastingModel, forecast_df: pd.DataFrame, 
                     forecast_horizon: int) -> pd.DataFrame:
    """
    Generate forecasts using the loaded model.
    
    Args:
        model: Loaded forecasting model
        forecast_df: Dataframe with forecast period data
        forecast_horizon: Number of days being forecast
        
    Returns:
        Dataframe with predictions
    """
    print(f"\nGenerating {forecast_horizon}-day forecast...")
    
    # Make predictions
    predictions = model.predict(forecast_df)
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'Date': forecast_df['Date'],
        'sku_id': forecast_df['sku_id'],
        'product_type': forecast_df['product_type'] if 'product_type' in forecast_df.columns else '',
        'category': forecast_df['category'] if 'category' in forecast_df.columns else '',
        'actual_quantity': forecast_df['quantity'] if 'quantity' in forecast_df.columns else np.nan,
        'predicted_quantity': predictions,
        'forecast_horizon': forecast_horizon
    })
    
    # Calculate error metrics if actuals are available
    if 'quantity' in forecast_df.columns:
        actuals = forecast_df['quantity'].values
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        
        mae = mean_absolute_error(actuals, predictions)
        rmse = np.sqrt(mean_squared_error(actuals, predictions))
        r2 = r2_score(actuals, predictions)
        mape = np.mean(np.abs((actuals - predictions) / (actuals + 1e-10))) * 100
        
        print(f"\nForecast Performance ({forecast_horizon}-day horizon):")
        print(f"  MAE:  {mae:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  R²:   {r2:.4f}")
        print(f"  MAPE: {mape:.2f}%")
    
    return results_df


def save_forecast(results_df: pd.DataFrame, forecast_horizon: int, 
                 output_dir: str = "forecasts") -> str:
    """
    Save forecast results to CSV.
    
    Args:
        results_df: Dataframe with forecast results
        forecast_horizon: Number of days forecast
        output_dir: Directory to save forecasts
        
    Returns:
        Path to saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"forecast_{forecast_horizon}day_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)
    
    # Reorder columns for better readability
    column_order = ['Date', 'sku_id', 'product_type', 'category', 'forecast_horizon', 
                   'actual_quantity', 'predicted_quantity']
    available_cols = [col for col in column_order if col in results_df.columns]
    results_df = results_df[available_cols]
    
    results_df.to_csv(filepath, index=False)
    print(f"\nForecast saved to: {filepath}")
    print(f"  Total predictions: {len(results_df):,}")
    print(f"  Date range: {results_df['Date'].min()} to {results_df['Date'].max()}")
    
    return filepath


def run_production_inference():
    """Main function for production inference."""
    print("="*70)
    print("DEMAND FORECASTING - PRODUCTION INFERENCE")
    print("="*70)
    
    # Configuration
    DATA_PATH = r"C:\Users\kingd\Ennovar\data\xg_df.csv"
    MODEL_DIR = "saved_models"
    OUTPUT_DIR = "forecasts"
    
    # Check if model exists
    if not os.path.exists(os.path.join(MODEL_DIR, "xgboost_model.json")):
        print(f"\nError: No trained model found in '{MODEL_DIR}/'")
        print("Please run 'python train_model.py' first to train the model.")
        sys.exit(1)
    
    # Load the trained model
    print("\n[1/3] Loading trained model...")
    print("-" * 70)
    model = DemandForecastingModel()
    model.load_model(MODEL_DIR)
    
    # User selects forecast horizon
    print("\n" + "="*70)
    print("SELECT FORECAST HORIZON")
    print("="*70)
    print("\nAvailable forecast horizons:")
    print("  1. 7 days  (1 week)")
    print("  2. 14 days (2 weeks)")
    print("  3. 30 days (1 month)")
    print("  4. All horizons (7, 14, and 30 days)")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                horizons = [7]
                break
            elif choice == '2':
                horizons = [14]
                break
            elif choice == '3':
                horizons = [30]
                break
            elif choice == '4':
                horizons = [7, 14, 30]
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
    
    # Generate forecasts for selected horizons
    all_results = []
    
    for horizon in horizons:
        print("\n" + "="*70)
        print(f"FORECAST HORIZON: {horizon} DAYS")
        print("="*70)
        
        # Load data for this horizon
        print(f"\n[2/3] Loading data for {horizon}-day forecast...")
        forecast_df = load_inference_data(DATA_PATH, horizon)
        
        # Generate forecast
        print(f"\n[3/3] Generating predictions...")
        results_df = generate_forecast(model, forecast_df, horizon)
        
        # Save forecast
        filepath = save_forecast(results_df, horizon, OUTPUT_DIR)
        
        all_results.append({
            'horizon': horizon,
            'filepath': filepath,
            'num_predictions': len(results_df)
        })
    
    # Print summary
    print("\n" + "="*70)
    print("PRODUCTION INFERENCE COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"\nGenerated forecasts for {len(horizons)} horizon(s):")
    for result in all_results:
        print(f"  • {result['horizon']}-day forecast: {result['num_predictions']:,} predictions")
        print(f"    Saved to: {result['filepath']}")
    
    print(f"\nAll forecasts saved to: {os.path.abspath(OUTPUT_DIR)}/")


if __name__ == "__main__":
    try:
        run_production_inference()
        print("\nInference script completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
        
    except Exception as e:
        print(f"\nError during inference: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
