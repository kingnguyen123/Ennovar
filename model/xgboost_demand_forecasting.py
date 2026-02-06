import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import List, Dict, Tuple
import warnings
import os
import re
warnings.filterwarnings('ignore')


class XGBoostDemandForecasting:
    """Simplified XGBoost-only demand forecasting model."""
    
    def __init__(self, data_path: str):
        """
        Initialize the XGBoost demand forecasting model.
        
        Args:
            data_path: Path to the pre-engineered CSV file
        """
        self.data_path = data_path
        self.model = None
        self.feature_cols = None
        self.target_col = 'quantity'
        self.target_transformer = None
        self.label_encoders = {}
        
    def load_data(self) -> pd.DataFrame:
        """
        Load pre-engineered dataset.
        
        Returns:
            Loaded dataframe
        """
        print(f"Loading data from {self.data_path}")
        df = pd.read_csv(self.data_path)
        
        # Convert Date to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        print(f"Loaded dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        return df
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features between important variables.
        
        Args:
            df: Input dataframe
            
        Returns:
            Dataframe with interaction features
        """
        df = df.copy()
        
        # Price and promotion interactions
        if 'unit_price' in df.columns and 'promo_flag' in df.columns:
            df['price_promo_interaction'] = df['unit_price'] * df['promo_flag']
        
        if 'discount_pct' in df.columns and 'promo_flag' in df.columns:
            df['discount_intensity'] = df['discount_pct'] * df['promo_flag']
        
        # Seasonal interactions
        if 'is_weekend' in df.columns and 'promo_flag' in df.columns:
            df['weekend_promo'] = df['is_weekend'] * df['promo_flag']
        
        if 'month' in df.columns and 'promo_flag' in df.columns:
            df['month_promo'] = df['month'] * df['promo_flag']
        
        # Rolling mean interactions
        if 'rolling_mean_28' in df.columns and 'sales_lag_1' in df.columns:
            df['current_vs_avg'] = df['sales_lag_1'] / (df['rolling_mean_28'] + 1e-10)
        
        # Price tier interactions
        if 'price_tier' in df.columns and 'promo_flag' in df.columns:
            df['price_tier_promo'] = df.groupby(['price_tier', 'promo_flag']).ngroup()
        
        return df
    
    def create_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create advanced statistical and domain-specific features.
        
        Args:
            df: Input dataframe
            
        Returns:
            Dataframe with advanced features
        """
        df = df.copy()
        
        # Coefficient of variation (volatility measure)
        if 'rolling_mean_28' in df.columns and 'rolling_std_28' in df.columns:
            df['cv_28'] = df['rolling_std_28'] / (df['rolling_mean_28'] + 1e-10)
        
        # Momentum features
        if 'sales_lag_7' in df.columns and 'sales_lag_14' in df.columns:
            df['momentum_7_14'] = (df['sales_lag_7'] - df['sales_lag_14']) / (df['sales_lag_14'] + 1e-10)
        
        # Inventory turnover proxy
        if 'sales_lag_7' in df.columns and 'rolling_mean_28' in df.columns:
            df['turnover_proxy'] = df['sales_lag_7'] / (df['rolling_mean_28'] + 1e-10)
        
        # Price elasticity proxy
        if 'price_change_7' in df.columns and 'pct_change_7' in df.columns:
            df['price_elasticity_proxy'] = df['pct_change_7'] / (df['price_change_7'] + 1e-10)
        
        # Seasonal decomposition features
        if 'month' in df.columns:
            df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
            df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        if 'day_of_week' in df.columns:
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        return df
    
    def encode_categorical_features(self, train_df: pd.DataFrame, 
                                   val_df: pd.DataFrame, 
                                   test_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Encode categorical features using label encoding.
        
        Args:
            train_df: Training dataframe
            val_df: Validation dataframe
            test_df: Test dataframe
            
        Returns:
            Tuple of encoded dataframes
        """
        categorical_cols = ['category', 'sub_category', 'brand', 'product_type', 'size_label', 'price_tier']
        
        train_encoded = train_df.copy()
        val_encoded = val_df.copy()
        test_encoded = test_df.copy()
        
        for col in categorical_cols:
            if col in train_encoded.columns:
                le = LabelEncoder()
                
                # Fit on train data
                train_encoded[col] = le.fit_transform(train_encoded[col].astype(str))
                
                # Transform validation and test
                val_encoded[col] = val_encoded[col].astype(str).apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else -1
                )
                test_encoded[col] = test_encoded[col].astype(str).apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else -1
                )
                
                self.label_encoders[col] = le
                print(f"    Encoded {col}: {len(le.classes_)} unique values")
        
        return train_encoded, val_encoded, test_encoded
    
    def apply_target_transformation(self, y_train: pd.Series, y_val: pd.Series, 
                                   y_test: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series, dict]:
        """
        Apply target transformation to reduce skewness and improve predictions.
        
        Args:
            y_train, y_val, y_test: Target variables
            
        Returns:
            Transformed targets and the transformer object
        """
        # Use log1p transformation for count data
        transformer = lambda x: np.log1p(x)
        inverse_transformer = lambda x: np.expm1(x)
        
        y_train_transformed = transformer(y_train)
        y_val_transformed = transformer(y_val)
        y_test_transformed = transformer(y_test)
        
        self.target_transformer = {'transform': transformer, 'inverse': inverse_transformer}
        
        return y_train_transformed, y_val_transformed, y_test_transformed, self.target_transformer
    
    def create_time_splits(self, df: pd.DataFrame, test_days: int = 14, 
                          val_days: int = 14) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Create time-based train/validation/test splits.
        Uses global date cutoffs for all SKUs.
        
        Args:
            df: Input dataframe
            test_days: Number of days for test set
            val_days: Number of days for validation set
            
        Returns:
            Tuple of train, validation, and test dataframes
        """
        print("\nTime-Based Split")
        print("Creating time-based train/validation/test splits")
        
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        
        print(f"Data range: {min_date.date()} to {max_date.date()}")
        print(f"Total days: {(max_date - min_date).days + 1}")
        
        # Define cutoff dates
        test_start = max_date - pd.Timedelta(days=test_days - 1)
        val_start = test_start - pd.Timedelta(days=val_days)
        
        print(f"\nSplit dates:")
        print(f"  Train: {min_date.date()} to {(val_start - pd.Timedelta(days=1)).date()}")
        print(f"  Validation: {val_start.date()} to {(test_start - pd.Timedelta(days=1)).date()}")
        print(f"  Test: {test_start.date()} to {max_date.date()}")
        
        # Create splits
        train_df = df[df['Date'] < val_start].copy()
        val_df = df[(df['Date'] >= val_start) & (df['Date'] < test_start)].copy()
        test_df = df[df['Date'] >= test_start].copy()
        
        print(f"\nDataset sizes:")
        print(f"  Train: {len(train_df):,} rows ({len(train_df)/len(df)*100:.1f}%)")
        print(f"  Validation: {len(val_df):,} rows ({len(val_df)/len(df)*100:.1f}%)")
        print(f"  Test: {len(test_df):,} rows ({len(test_df)/len(df)*100:.1f}%)")
        
        print(f"\nUnique SKUs in each set:")
        print(f"  Train: {train_df['sku_id'].nunique()} SKUs")
        print(f"  Validation: {val_df['sku_id'].nunique()} SKUs")
        print(f"  Test: {test_df['sku_id'].nunique()} SKUs")
        print(f"  Total unique SKUs in dataset: {df['sku_id'].nunique()} SKUs")
        
        return train_df, val_df, test_df
    
    def prepare_model_data(self, train_df: pd.DataFrame, val_df: pd.DataFrame, 
                          test_df: pd.DataFrame) -> Tuple:
        """
        Prepare data for model training.
        
        Args:
            train_df: Training dataframe
            val_df: Validation dataframe
            test_df: Test dataframe
            
        Returns:
            Tuple of X_train, y_train, X_val, y_val, X_test, y_test
        """
        print("\nPreparing model data...")
        
        # Add additional features
        print("Creating interaction features...")
        train_df = self.create_interaction_features(train_df)
        val_df = self.create_interaction_features(val_df)
        test_df = self.create_interaction_features(test_df)
        
        print("Creating advanced features...")
        train_df = self.create_advanced_features(train_df)
        val_df = self.create_advanced_features(val_df)
        test_df = self.create_advanced_features(test_df)
        
        # Handle any infinite values
        train_df = train_df.replace([np.inf, -np.inf], np.nan)
        val_df = val_df.replace([np.inf, -np.inf], np.nan)
        test_df = test_df.replace([np.inf, -np.inf], np.nan)
        
        # Fill NaN values
        train_df = train_df.fillna(0)
        val_df = val_df.fillna(0)
        test_df = test_df.fillna(0)
        
        # Encode categorical features
        print("Encoding categorical features...")
        train_encoded, val_encoded, test_encoded = self.encode_categorical_features(
            train_df, val_df, test_df
        )
        
        # Define feature columns (exclude identifiers and target)
        exclude_cols = ['sku_id', 'Date', self.target_col]
        self.feature_cols = [col for col in train_encoded.columns if col not in exclude_cols]
        
        # Sanitize feature names for XGBoost compatibility
        def sanitize_feature_name(name):
            # Replace special JSON characters with underscores
            return re.sub(r'[^\w\-]', '_', str(name))
        
        # Create mapping of old to new names
        feature_name_mapping = {col: sanitize_feature_name(col) for col in self.feature_cols}
        
        # Rename columns in all datasets
        train_encoded = train_encoded.rename(columns=feature_name_mapping)
        val_encoded = val_encoded.rename(columns=feature_name_mapping)
        test_encoded = test_encoded.rename(columns=feature_name_mapping)
        
        # Update feature_cols with sanitized names
        self.feature_cols = [sanitize_feature_name(col) for col in self.feature_cols]
        
        print(f"Number of features: {len(self.feature_cols)}")
        
        # Prepare X and y
        X_train = train_encoded[self.feature_cols].copy()
        y_train = train_encoded[self.target_col].copy()
        
        X_val = val_encoded[self.feature_cols].copy()
        y_val = val_encoded[self.target_col].copy()
        
        X_test = test_encoded[self.feature_cols].copy()
        y_test = test_encoded[self.target_col].copy()
        
        # Apply target transformation
        print("Applying target transformation...")
        y_train_transformed, y_val_transformed, y_test_transformed, _ = (
            self.apply_target_transformation(y_train, y_val, y_test)
        )
        
        print("\nDataset shapes after preprocessing:")
        print(f"X_train: {X_train.shape}, y_train: {y_train_transformed.shape}")
        print(f"X_val: {X_val.shape}, y_val: {y_val_transformed.shape}")
        print(f"X_test: {X_test.shape}, y_test: {y_test_transformed.shape}")
        
        return X_train, y_train_transformed, X_val, y_val_transformed, X_test, y_test_transformed
    
    def train_xgboost(self, X_train: pd.DataFrame, y_train: pd.Series, 
                     X_val: pd.DataFrame, y_val: pd.Series) -> xgb.Booster:
        """
        Train XGBoost model.
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data
            
        Returns:
            Trained XGBoost model
        """
        print("\nTraining XGBoost model")
        
        params = {
            'objective': 'reg:squarederror',
            'eval_metric': 'mae',
            'max_depth': 4,
            'min_child_weight': 5,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'learning_rate': 0.05,
            'reg_alpha': 1.0,
            'reg_lambda': 5.0,
            'random_state': 42,
            'n_jobs': -1
        }
        
        print("XGBoost Configuration:")
        for key, value in params.items():
            print(f"  {key}: {value}")
        
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dval = xgb.DMatrix(X_val, label=y_val)
        
        evals = [(dtrain, 'train'), (dval, 'validation')]
        
        self.model = xgb.train(
            params=params,
            dtrain=dtrain,
            num_boost_round=2000,
            evals=evals,
            early_stopping_rounds=100,
            verbose_eval=100
        )
        
        return self.model
    
    def evaluate(self, X_train: pd.DataFrame, y_train: pd.Series,
                X_val: pd.DataFrame, y_val: pd.Series,
                X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """
        Evaluate model performance.
        
        Args:
            X_train, y_train: Training data (transformed)
            X_val, y_val: Validation data (transformed)
            X_test, y_test: Test data (transformed)
            
        Returns:
            Dictionary containing metrics and predictions
        """
        print("\nEvaluating model performance...")
        
        # Make predictions
        dmatrix_train = xgb.DMatrix(X_train)
        dmatrix_val = xgb.DMatrix(X_val)
        dmatrix_test = xgb.DMatrix(X_test)
        
        y_train_pred_transformed = self.model.predict(dmatrix_train)
        y_val_pred_transformed = self.model.predict(dmatrix_val)
        y_test_pred_transformed = self.model.predict(dmatrix_test)
        
        # Transform back to original space
        if self.target_transformer:
            y_train_pred = np.maximum(self.target_transformer['inverse'](y_train_pred_transformed), 0)
            y_val_pred = np.maximum(self.target_transformer['inverse'](y_val_pred_transformed), 0)
            y_test_pred = np.maximum(self.target_transformer['inverse'](y_test_pred_transformed), 0)
            
            y_train_true = self.target_transformer['inverse'](y_train)
            y_val_true = self.target_transformer['inverse'](y_val)
            y_test_true = self.target_transformer['inverse'](y_test)
        else:
            y_train_pred = np.maximum(y_train_pred_transformed, 0)
            y_val_pred = np.maximum(y_val_pred_transformed, 0)
            y_test_pred = np.maximum(y_test_pred_transformed, 0)
            
            y_train_true = y_train
            y_val_true = y_val
            y_test_true = y_test
        
        def calculate_metrics(y_true, y_pred, dataset_name):
            """Calculate regression metrics."""
            mae = mean_absolute_error(y_true, y_pred)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            r2 = r2_score(y_true, y_pred)
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100
            
            print(f"\n{dataset_name} Metrics:")
            print(f"  MAE:  {mae:.4f}")
            print(f"  RMSE: {rmse:.4f}")
            print(f"  R2:   {r2:.4f}")
            print(f"  MAPE: {mape:.2f}%")
            
            return {'mae': mae, 'rmse': rmse, 'r2': r2, 'mape': mape}
        
        print("XGBOOST MODEL PERFORMANCE EVALUATION")
        
        train_metrics = calculate_metrics(y_train_true, y_train_pred, "TRAIN")
        val_metrics = calculate_metrics(y_val_true, y_val_pred, "VALIDATION")
        test_metrics = calculate_metrics(y_test_true, y_test_pred, "TEST")
        
        return {
            'train': train_metrics,
            'validation': val_metrics,
            'test': test_metrics,
            'predictions': {
                'train': y_train_pred,
                'validation': y_val_pred,
                'test': y_test_pred
            },
            'true_values': {
                'train': y_train_true,
                'validation': y_val_true,
                'test': y_test_true
            }
        }
    
    def save_predictions_to_csv(self, test_df: pd.DataFrame, y_test_true: np.ndarray, 
                               y_test_pred: np.ndarray, forecast_horizon: int, 
                               output_file: str = 'xgboost_predictions.csv') -> None:
        """
        Save predictions to CSV file with required format.
        
        Args:
            test_df: Test dataframe with Date, sku_id, and product_type
            y_test_true: True test values
            y_test_pred: Predicted test values
            forecast_horizon: Number of days in forecast horizon
            output_file: Output CSV file path
        """
        print(f"Saving XGBoost predictions for {forecast_horizon}-day horizon to {output_file}")
        
        # Create results dataframe
        results_df = test_df[['Date', 'sku_id', 'product_type']].copy()
        results_df['forecast_horizon'] = forecast_horizon
        results_df['actual_quantity'] = y_test_true
        results_df['predicted_quantity'] = y_test_pred
        
        # Reorder columns as requested
        results_df = results_df[['product_type', 'forecast_horizon', 'Date', 'actual_quantity', 'predicted_quantity']]
        
        # Save to CSV (append mode for multiple horizons)
        if not os.path.exists(output_file):
            results_df.to_csv(output_file, index=False)
        else:
            results_df.to_csv(output_file, index=False, mode='a', header=False)
        
        print(f"Saved {len(results_df)} XGBoost predictions for {forecast_horizon}-day horizon")
    
    def save_metrics_to_csv(self, all_metrics: Dict, output_file: str = 'xgboost_metrics.csv') -> None:
        """
        Save MAE, RMSE, R2, and MAPE metrics to CSV file.
        
        Args:
            all_metrics: Dictionary containing metrics for all forecast horizons
            output_file: Output CSV file path
        """
        print(f"Saving XGBoost model metrics to {output_file}")
        
        metrics_data = []
        for horizon, metrics in all_metrics.items():
            metrics_data.append({
                'forecast_horizon': horizon,
                'dataset': 'train',
                'mae': metrics['train']['mae'],
                'rmse': metrics['train']['rmse'],
                'r2': metrics['train']['r2'],
                'mape': metrics['train']['mape']
            })
            metrics_data.append({
                'forecast_horizon': horizon,
                'dataset': 'validation',
                'mae': metrics['validation']['mae'],
                'rmse': metrics['validation']['rmse'],
                'r2': metrics['validation']['r2'],
                'mape': metrics['validation']['mape']
            })
            metrics_data.append({
                'forecast_horizon': horizon,
                'dataset': 'test',
                'mae': metrics['test']['mae'],
                'rmse': metrics['test']['rmse'],
                'r2': metrics['test']['r2'],
                'mape': metrics['test']['mape']
            })
        
        metrics_df = pd.DataFrame(metrics_data)
        metrics_df.to_csv(output_file, index=False)
        print(f"Saved XGBoost metrics for {len(all_metrics)} forecast horizons")
    
    def run_pipeline(self, forecast_horizons: List[int] = [7, 14, 30], val_days: int = 14,
                    predictions_output: str = 'xgboost_predictions.csv',
                    metrics_output: str = 'xgboost_metrics.csv') -> Dict:
        """
        Run the complete XGBoost demand forecasting pipeline for multiple forecast horizons.
        
        Args:
            forecast_horizons: List of forecast horizons in days (default: [7, 14, 30])
            val_days: Number of days for validation set
            predictions_output: Output file for predictions CSV
            metrics_output: Output file for metrics CSV
            
        Returns:
            Dictionary containing model results and metrics for all horizons
        """
        print("XGBOOST DEMAND FORECASTING PIPELINE - MULTIPLE HORIZONS")
        print(f"Forecast horizons: {forecast_horizons} days")
        
        # Load data once
        df = self.load_data()
        
        # Remove existing output files to start fresh
        if os.path.exists(predictions_output):
            os.remove(predictions_output)
            print(f"Removed existing {predictions_output}")
        
        all_results = {}
        
        # Loop through each forecast horizon
        for horizon in forecast_horizons:
            print(f"\n{'='*60}")
            print(f"PROCESSING FORECAST HORIZON: {horizon} DAYS")
            print(f"{'='*60}")
            
            # Create time splits for this horizon
            train_df, val_df, test_df = self.create_time_splits(df, test_days=horizon, val_days=val_days)
            
            # Prepare model data
            X_train, y_train, X_val, y_val, X_test, y_test = self.prepare_model_data(
                train_df, val_df, test_df
            )
            
            # Train XGBoost model for this horizon
            self.train_xgboost(X_train, y_train, X_val, y_val)
            
            # Evaluate model
            results = self.evaluate(X_train, y_train, X_val, y_val, X_test, y_test)
            
            # Save predictions to CSV
            self.save_predictions_to_csv(
                test_df, 
                results['true_values']['test'], 
                results['predictions']['test'],
                horizon,
                predictions_output
            )
            
            # Store results
            all_results[horizon] = results
            
            print(f"\nCompleted {horizon}-day forecast horizon")
            print(f"Test MAE: {results['test']['mae']:.4f}")
            print(f"Test RMSE: {results['test']['rmse']:.4f}")
            print(f"Test R2: {results['test']['r2']:.4f}")
            print(f"Test MAPE: {results['test']['mape']:.2f}%")
        
        # Save all metrics to CSV
        self.save_metrics_to_csv(all_results, metrics_output)
        

        print("XGBOOST PIPELINE COMPLETE - ALL HORIZONS")

        print(f"Predictions saved to: {predictions_output}")
        print(f"Metrics saved to: {metrics_output}")
        
        # Print summary
        print("\nSUMMARY OF ALL FORECAST HORIZONS:")
        for horizon in forecast_horizons:
            metrics = all_results[horizon]['test']
            print(f"  {horizon}-day horizon: MAE={metrics['mae']:.4f}, RMSE={metrics['rmse']:.4f}, R2={metrics['r2']:.4f}, MAPE={metrics['mape']:.2f}%")
        
        return all_results


if __name__ == "__main__":
    data_path = r"C:\Users\kingd\PycharmProjects\Model\data\xg_df.csv"
    
    model = XGBoostDemandForecasting(data_path)
    
    # Run pipeline with multiple forecast horizons using only XGBoost
    results = model.run_pipeline(
        forecast_horizons=[7, 14, 30],        # Multiple forecast horizons
        val_days=14,                          # Number of days for validation set
        predictions_output='xgboost_predictions.csv',  # Predictions output file
        metrics_output='xgboost_metrics.csv'           # Metrics output file
    )
    
    # Print final results
    print("\nFINAL XGBOOST RESULTS SUMMARY")
    for horizon, result in results.items():
        print(f"\n{horizon}-day forecast:")
        print(f"  MAE: {result['test']['mae']:.4f}")
        print(f"  RMSE: {result['test']['rmse']:.4f}")
        print(f"  R2: {result['test']['r2']:.4f}")
        print(f"  MAPE: {result['test']['mape']:.2f}%")