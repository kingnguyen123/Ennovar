"""
Training Script for Demand Forecasting Model

This script trains the XGBoost demand forecasting model on historical data
and saves the trained model artifacts for production use.

Usage:
    python train_model.py
"""

import sys
import os
from demand_forecasting_model import DemandForecastingModel


def train_and_save_model(data_path: str, model_dir: str = "saved_models", 
                         test_days: int = 30, val_days: int = 14):
    """
    Train the demand forecasting model and save it for production use.
    
    Args:
        data_path: Path to the training data CSV
        model_dir: Directory to save model artifacts
        test_days: Number of days for test set (default: 30 days for comprehensive testing)
        val_days: Number of days for validation set
    """
    print("="*70)
    print("DEMAND FORECASTING MODEL - TRAINING PHASE")
    print("="*70)
    
    # Initialize model
    model = DemandForecastingModel()
    
    # Load training data
    print("\n[1/5] Loading training data...")
    df = model.load_data(data_path)
    
    # Create time-based splits
    print(f"\n[2/5] Creating train/validation/test splits...")
    print(f"  Test period: {test_days} days (for comprehensive evaluation)")
    print(f"  Validation period: {val_days} days")
    train_df, val_df, test_df = model.create_time_splits(df, test_days=test_days, val_days=val_days)
    
    # Prepare features
    print("\n[3/5] Preparing features and encoding...")
    X_train, y_train, X_val, y_val, X_test, y_test = model.prepare_model_data(
        train_df, val_df, test_df
    )
    
    # Train model
    print("\n[4/5] Training XGBoost model...")
    print("-" * 70)
    model.train(X_train, y_train, X_val, y_val)
    
    # Evaluate on all sets
    print("\n[5/5] Evaluating model performance...")
    print("-" * 70)
    train_results = model.evaluate(X_train, y_train, "TRAINING SET")
    val_results = model.evaluate(X_val, y_val, "VALIDATION SET")
    test_results = model.evaluate(X_test, y_test, "TEST SET")
    
    # Print summary
    print("\n" + "="*70)
    print("TRAINING COMPLETE - PERFORMANCE SUMMARY")
    print("="*70)
    print(f"Training Set   - MAE: {train_results['mae']:.4f}, RMSE: {train_results['rmse']:.4f}, R²: {train_results['r2']:.4f}")
    print(f"Validation Set - MAE: {val_results['mae']:.4f}, RMSE: {val_results['rmse']:.4f}, R²: {val_results['r2']:.4f}")
    print(f"Test Set       - MAE: {test_results['mae']:.4f}, RMSE: {test_results['rmse']:.4f}, R²: {test_results['r2']:.4f}")
    
    # Save model
    print("\n" + "-"*70)
    print("Saving trained model...")
    print("-" * 70)
    model.save_model(model_dir)
    
    print("\n" + "="*70)
    print("TRAINING PHASE COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"\nModel artifacts saved to: {os.path.abspath(model_dir)}/")
    print("\nThe trained model is now ready for production inference.")
    print("Use 'python predict.py' to make predictions with the saved model.")
    
    return model, {
        'train': train_results,
        'validation': val_results,
        'test': test_results
    }


if __name__ == "__main__":
    # Configuration
    DATA_PATH = r"C:\Users\kingd\Ennovar\data\xg_df.csv"
    MODEL_DIR = "saved_models"
    
    # Train and save model
    try:
        model, results = train_and_save_model(
            data_path=DATA_PATH,
            model_dir=MODEL_DIR,
            test_days=30,  # Use 30 days for comprehensive testing
            val_days=14
        )
        
        print("\nTraining script completed successfully!")
        
    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
