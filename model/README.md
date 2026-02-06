# Demand Forecasting Pipeline - Production Ready

A production-ready time-series forecasting system with separate training and inference phases.

## Overview

This pipeline uses XGBoost for demand forecasting with a strict separation between training and production inference phases. The trained model can be saved and reused without retraining.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TRAINING PHASE                           │
│  (Run once or when retraining is needed)                    │
├─────────────────────────────────────────────────────────────┤
│  1. Load historical data                                    │
│  2. Feature engineering & preprocessing                     │
│  3. Train XGBoost model                                     │
│  4. Validate performance                                    │
│  5. Save model artifacts                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
                   Model Artifacts
                  (saved_models/)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  PRODUCTION INFERENCE                       │
│  (Run anytime with saved model)                             │
├─────────────────────────────────────────────────────────────┤
│  1. Load trained model (no retraining)                      │
│  2. Select forecast horizon (7/14/30 days)                  │
│  3. Generate predictions                                    │
│  4. Save forecasts                                          │
└─────────────────────────────────────────────────────────────┘
```

## Files

### Core Model
- `demand_forecasting_model.py` - Model class with save/load capabilities

### Scripts
- `train_model.py` - Training phase script
- `predict.py` - Production inference script

### Directories
- `saved_models/` - Trained model artifacts (created during training)
- `forecasts/` - Generated forecast outputs (created during inference)

## Usage

### Phase 1: Training (One-Time Setup)

Train the model on historical data and save it:

```bash
cd model
python train_model.py
```

**What happens:**
- Loads data from `C:\Users\kingd\Ennovar\data\xg_df.csv`
- Creates time-based train/val/test splits
- Engineers features and trains XGBoost model
- Evaluates performance on all sets
- Saves model artifacts to `saved_models/`

**Saved artifacts:**
- `xgboost_model.json` - Trained model
- `feature_columns.json` - Feature list
- `label_encoders.pkl` - Categorical encoders
- `target_transformer.pkl` - Target transformation
- `model_metadata.json` - Training metadata

**Expected output:**
```
Training Set   - MAE: X.XXXX, RMSE: X.XXXX, R²: X.XXXX
Validation Set - MAE: X.XXXX, RMSE: X.XXXX, R²: X.XXXX
Test Set       - MAE: X.XXXX, RMSE: X.XXXX, R²: X.XXXX

✓ Model artifacts saved to saved_models/
```

### Phase 2: Production Inference (Repeatable)

Generate forecasts using the saved model:

```bash
cd model
python predict.py
```

**Interactive menu:**
```
SELECT FORECAST HORIZON
Available forecast horizons:
  1. 7 days  (1 week)
  2. 14 days (2 weeks)
  3. 30 days (1 month)
  4. All horizons (7, 14, and 30 days)

Enter your choice (1-4):
```

**What happens:**
1. Loads the pre-trained model (no retraining!)
2. User selects forecast horizon
3. Generates predictions for selected horizon
4. Saves forecasts to `forecasts/forecast_Xday_YYYYMMDD_HHMMSS.csv`

**Output format:**
```csv
Date,sku_id,product_type,category,forecast_horizon,actual_quantity,predicted_quantity
2019-09-22,SKU0108578252,Lip Balm,Beauty,7,1.0,1.2345
...
```

## Model Features

### Engineered Features
- **Lag features**: 7, 14, 28, 56, 84 days
- **Rolling statistics**: Mean, std, min, max (7, 14, 28, 56 day windows)
- **Trend features**: Momentum, percent change
- **Price features**: Price changes, elasticity proxies
- **Promotional features**: Promo flags, intensity, frequency
- **Seasonal features**: Month/day sin/cos transformations
- **Interaction features**: Price×promo, weekend×promo, etc.

### Model Configuration
- **Algorithm**: XGBoost (Gradient Boosting)
- **Objective**: Regression (squared error)
- **Target transformation**: Log1p (handles count data)
- **Early stopping**: 100 rounds on validation set
- **Regularization**: L1 (alpha=1.0), L2 (lambda=5.0)

## Performance Metrics

The model is evaluated using:
- **MAE** (Mean Absolute Error) - Average prediction error
- **RMSE** (Root Mean Squared Error) - Penalizes large errors
- **R²** (R-squared) - Variance explained by model
- **MAPE** (Mean Absolute Percentage Error) - Relative error %

## Workflow Best Practices

### When to Retrain
- New historical data available
- Model performance degrades
- Business logic changes
- Seasonal patterns shift

### Production Deployment
1. Train model once using `train_model.py`
2. Deploy `saved_models/` directory with your application
3. Use `predict.py` or integrate `DemandForecastingModel.load_model()` + `.predict()` into your pipeline
4. No retraining needed for daily/weekly forecasts

### Integration Example

```python
from demand_forecasting_model import DemandForecastingModel
import pandas as pd

# Load model once
model = DemandForecastingModel()
model.load_model("saved_models")

# Generate predictions (repeatable, fast)
new_data = pd.read_csv("your_data.csv")
predictions = model.predict(new_data)
```

## Requirements

- Python 3.7+
- pandas
- numpy
- xgboost
- scikit-learn

Install dependencies:
```bash
pip install pandas numpy xgboost scikit-learn
```

## Data Requirements

The input CSV must contain these columns:
- `Date` - Date column
- `sku_id` - Product SKU identifier
- `quantity` - Target variable (demand/sales quantity)
- Feature columns: `unit_price`, `promo_flag`, `category`, `sub_category`, lag features, rolling statistics, etc.

## Troubleshooting

### "No trained model found"
Run `python train_model.py` first to create model artifacts.

### "Missing feature columns"
Ensure inference data has the same features as training data.

### Poor performance
- Check data quality
- Verify date range alignment
- Consider retraining with more recent data

## License

MIT License - Feel free to use in production systems.
