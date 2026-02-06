import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import List, Dict, Tuple, Optional
import warnings
import os
import re
import pickle
import json
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')


class DemandForecastingModel:
    """Production-ready XGBoost demand forecasting model with save/load capabilities."""
    
    def __init__(self):
        """Initialize the demand forecasting model."""
        self.model = None
        self.feature_cols = None
        self.target_col = 'quantity'
        self.target_transformer = None
        self.label_encoders = {}
        self.model_metadata = {}
        
    def load_data(self, data_path: str) -> pd.DataFrame:
        """
        Load pre-engineered dataset.
        
        Args:
            data_path: Path to the pre-engineered CSV file
            
        Returns:
            Loaded dataframe
        """
        print(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
        
        # Drop unnamed index column if it exists
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
        
        # Convert Date to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        print(f"Loaded dataset shape: {df.shape}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Unique SKUs: {df['sku_id'].nunique()}")
        return df
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features between important variables."""
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
        if 'rolling_mean_28' in df.columns and 'sales_lag_7' in df.columns:
            df['current_vs_avg'] = df['sales_lag_7'] / (df['rolling_mean_28'] + 1e-10)
        
        # Price tier interactions
        if 'price_tier' in df.columns and 'promo_flag' in df.columns:
            df['price_tier_promo'] = df.groupby(['price_tier', 'promo_flag']).ngroup()
        
        return df
    
    def create_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced statistical and domain-specific features."""
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
                                   val_df: pd.DataFrame = None, 
                                   test_df: pd.DataFrame = None,
                                   fit: bool = True) -> Tuple:
        """
        Encode categorical features using label encoding.
        
        Args:
            train_df: Training/inference dataframe
            val_df: Validation dataframe (optional)
            test_df: Test dataframe (optional)
            fit: Whether to fit encoders (True for training, False for inference)
            
        Returns:
            Tuple of encoded dataframes
        """
        categorical_cols = ['category', 'sub_category', 'brand', 'product_type', 'size_label', 'price_tier']
        
        train_encoded = train_df.copy()
        
        for col in categorical_cols:
            if col in train_encoded.columns:
                if fit:
                    # Training mode: fit and transform
                    le = LabelEncoder()
                    train_encoded[col] = le.fit_transform(train_encoded[col].astype(str))
                    self.label_encoders[col] = le
                    print(f"    Encoded {col}: {len(le.classes_)} unique values")
                else:
                    # Inference mode: transform using existing encoder
                    if col in self.label_encoders:
                        le = self.label_encoders[col]
                        train_encoded[col] = train_encoded[col].astype(str).apply(
                            lambda x: le.transform([x])[0] if x in le.classes_ else -1
                        )
        
        # Handle validation and test sets if provided
        if val_df is not None and test_df is not None:
            val_encoded = val_df.copy()
            test_encoded = test_df.copy()
            
            for col in categorical_cols:
                if col in val_encoded.columns and col in self.label_encoders:
                    le = self.label_encoders[col]
                    val_encoded[col] = val_encoded[col].astype(str).apply(
                        lambda x: le.transform([x])[0] if x in le.classes_ else -1
                    )
                    test_encoded[col] = test_encoded[col].astype(str).apply(
                        lambda x: le.transform([x])[0] if x in le.classes_ else -1
                    )
            
            return train_encoded, val_encoded, test_encoded
        
        return train_encoded
    
    def _transform_target(self, x):
        """Transform target using log1p."""
        return np.log1p(x)
    
    def _inverse_transform_target(self, x):
        """Inverse transform target using expm1."""
        return np.expm1(x)
    
    def apply_target_transformation(self, y_train: pd.Series, y_val: pd.Series = None, 
                                   y_test: pd.Series = None) -> Tuple:
        """Apply target transformation to reduce skewness."""
        y_train_transformed = self._transform_target(y_train)
        
        # Store transformation info (not the functions themselves for pickling)
        self.target_transformer = {'method': 'log1p'}
        
        if y_val is not None and y_test is not None:
            y_val_transformed = self._transform_target(y_val)
            y_test_transformed = self._transform_target(y_test)
            return y_train_transformed, y_val_transformed, y_test_transformed, self.target_transformer
        
        return y_train_transformed, self.target_transformer
    
    def create_time_splits(self, df: pd.DataFrame, test_days: int = 14, 
                          val_days: int = 14) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Create time-based train/validation/test splits."""
        print("\nCreating time-based train/validation/test splits")
        
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        
        print(f"Data range: {min_date.date()} to {max_date.date()}")
        
        # Define cutoff dates
        test_start = max_date - pd.Timedelta(days=test_days - 1)
        val_start = test_start - pd.Timedelta(days=val_days)
        
        print(f"  Train: {min_date.date()} to {(val_start - pd.Timedelta(days=1)).date()}")
        print(f"  Validation: {val_start.date()} to {(test_start - pd.Timedelta(days=1)).date()}")
        print(f"  Test: {test_start.date()} to {max_date.date()}")
        
        # Create splits
        train_df = df[df['Date'] < val_start].copy()
        val_df = df[(df['Date'] >= val_start) & (df['Date'] < test_start)].copy()
        test_df = df[df['Date'] >= test_start].copy()
        
        print(f"  Train: {len(train_df):,} rows")
        print(f"  Validation: {len(val_df):,} rows")
        print(f"  Test: {len(test_df):,} rows")
        
        return train_df, val_df, test_df
    
    def prepare_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Prepare features for model training or inference.
        
        Args:
            df: Input dataframe
            fit: Whether to fit transformers (True for training, False for inference)
            
        Returns:
            Processed dataframe
        """
        # Add features
        df = self.create_interaction_features(df)
        df = self.create_advanced_features(df)
        
        # Handle infinite values
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)
        
        # Encode categorical features
        df = self.encode_categorical_features(df, fit=fit)
        
        return df
    
    def sanitize_feature_name(self, name: str) -> str:
        """Sanitize feature names for XGBoost compatibility."""
        return re.sub(r'[^\w\-]', '_', str(name))
    
    def prepare_model_data(self, train_df: pd.DataFrame, val_df: pd.DataFrame, 
                          test_df: pd.DataFrame) -> Tuple:
        """Prepare data for model training."""
        print("\nPreparing model data...")
        
        # Add features
        print("Creating features...")
        train_df = self.create_interaction_features(train_df)
        val_df = self.create_interaction_features(val_df)
        test_df = self.create_interaction_features(test_df)
        
        train_df = self.create_advanced_features(train_df)
        val_df = self.create_advanced_features(val_df)
        test_df = self.create_advanced_features(test_df)
        
        # Handle infinite values
        train_df = train_df.replace([np.inf, -np.inf], np.nan).fillna(0)
        val_df = val_df.replace([np.inf, -np.inf], np.nan).fillna(0)
        test_df = test_df.replace([np.inf, -np.inf], np.nan).fillna(0)
        
        # Encode categorical features
        print("Encoding categorical features...")
        train_encoded, val_encoded, test_encoded = self.encode_categorical_features(
            train_df, val_df, test_df, fit=True
        )
        
        # Define feature columns
        exclude_cols = ['sku_id', 'Date', self.target_col]
        self.feature_cols = [col for col in train_encoded.columns if col not in exclude_cols]
        
        # Sanitize feature names
        feature_name_mapping = {col: self.sanitize_feature_name(col) for col in self.feature_cols}
        
        train_encoded = train_encoded.rename(columns=feature_name_mapping)
        val_encoded = val_encoded.rename(columns=feature_name_mapping)
        test_encoded = test_encoded.rename(columns=feature_name_mapping)
        
        self.feature_cols = [self.sanitize_feature_name(col) for col in self.feature_cols]
        
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
        
        return X_train, y_train_transformed, X_val, y_val_transformed, X_test, y_test_transformed
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series, 
             X_val: pd.DataFrame, y_val: pd.Series) -> None:
        """
        Train XGBoost model.
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data
        """
        print("\nTraining XGBoost model...")
        
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
        
        # Store metadata
        self.model_metadata = {
            'trained_at': datetime.now().isoformat(),
            'num_features': len(self.feature_cols),
            'params': params
        }
        
        print("Model training complete")
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series, dataset_name: str = "Dataset") -> Dict:
        """
        Evaluate model performance.
        
        Args:
            X: Features
            y: Transformed target values
            dataset_name: Name for reporting
            
        Returns:
            Dictionary containing metrics and predictions
        """
        dmatrix = xgb.DMatrix(X)
        y_pred_transformed = self.model.predict(dmatrix)
        
        # Transform back to original space
        if self.target_transformer:
            y_pred = np.maximum(self._inverse_transform_target(y_pred_transformed), 0)
            y_true = self._inverse_transform_target(y)
        else:
            y_pred = np.maximum(y_pred_transformed, 0)
            y_true = y
        
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100
        
        print(f"\n{dataset_name} Metrics:")
        print(f"  MAE:  {mae:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  R²:   {r2:.4f}")
        print(f"  MAPE: {mape:.2f}%")
        
        return {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'mape': mape,
            'predictions': y_pred,
            'true_values': y_true
        }
    
    def save_model(self, model_dir: str = "saved_models") -> None:
        """
        Save trained model and all artifacts.
        
        Args:
            model_dir: Directory to save model artifacts
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save XGBoost model
        model_path = os.path.join(model_dir, "xgboost_model.json")
        self.model.save_model(model_path)
        print(f"Saved XGBoost model to {model_path}")
        
        # Save feature columns
        features_path = os.path.join(model_dir, "feature_columns.json")
        with open(features_path, 'w') as f:
            json.dump(self.feature_cols, f, indent=2)
        print(f"Saved feature columns to {features_path}")
        
        # Save label encoders
        encoders_path = os.path.join(model_dir, "label_encoders.pkl")
        with open(encoders_path, 'wb') as f:
            pickle.dump(self.label_encoders, f)
        print(f"Saved label encoders to {encoders_path}")
        
        # Save target transformer
        transformer_path = os.path.join(model_dir, "target_transformer.pkl")
        with open(transformer_path, 'wb') as f:
            pickle.dump(self.target_transformer, f)
        print(f"Saved target transformer to {transformer_path}")
        
        # Save metadata
        metadata_path = os.path.join(model_dir, "model_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(self.model_metadata, f, indent=2)
        print(f"Saved model metadata to {metadata_path}")
        
        print(f"\nModel successfully saved to {model_dir}/")
    
    def load_model(self, model_dir: str = "saved_models") -> None:
        """
        Load trained model and all artifacts.
        
        Args:
            model_dir: Directory containing model artifacts
        """
        print(f"Loading model from {model_dir}/...")
        
        # Load XGBoost model
        model_path = os.path.join(model_dir, "xgboost_model.json")
        self.model = xgb.Booster()
        self.model.load_model(model_path)
        print(f"Loaded XGBoost model")
        
        # Load feature columns
        features_path = os.path.join(model_dir, "feature_columns.json")
        with open(features_path, 'r') as f:
            self.feature_cols = json.load(f)
        print(f"Loaded {len(self.feature_cols)} feature columns")
        
        # Load label encoders
        encoders_path = os.path.join(model_dir, "label_encoders.pkl")
        with open(encoders_path, 'rb') as f:
            self.label_encoders = pickle.load(f)
        print(f"Loaded label encoders")
        
        # Load target transformer
        transformer_path = os.path.join(model_dir, "target_transformer.pkl")
        with open(transformer_path, 'rb') as f:
            self.target_transformer = pickle.load(f)
        print(f"Loaded target transformer")
        
        # Load metadata
        metadata_path = os.path.join(model_dir, "model_metadata.json")
        with open(metadata_path, 'r') as f:
            self.model_metadata = json.load(f)
        print(f"Loaded model metadata")
        print(f"  Model trained at: {self.model_metadata.get('trained_at', 'Unknown')}")
        
        print("\nModel successfully loaded and ready for inference")
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            df: Input dataframe with features
            
        Returns:
            Array of predictions
        """
        if self.model is None:
            raise ValueError("No model loaded. Call load_model() first.")
        
        # Prepare features (without fitting transformers)
        df_processed = self.prepare_features(df, fit=False)
        
        # Ensure we have all required features
        X = df_processed[self.feature_cols].copy()
        
        # Make predictions
        dmatrix = xgb.DMatrix(X)
        y_pred_transformed = self.model.predict(dmatrix)
        
        # Transform back to original space
        if self.target_transformer:
            y_pred = np.maximum(self._inverse_transform_target(y_pred_transformed), 0)
        else:
            y_pred = np.maximum(y_pred_transformed, 0)
        
        return y_pred
