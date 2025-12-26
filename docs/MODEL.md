# Machine Learning Models Documentation

This document describes the machine learning models and data processing workflows used in the Ennovar forecasting system.

## Overview

The Ennovar system uses AutoGluon for automated time series forecasting of retail sales. The ML pipeline consists of data processing, feature engineering, model training, and prediction generation.

## Notebooks

### 1. Process_data.ipynb

**Purpose**: Data preprocessing and feature engineering

**Location**: `/model/Process_data.ipynb`

**Key Responsibilities**:
- Load raw transaction data from CSV files
- Clean and validate data
- Handle missing values
- Create time-based features
- Aggregate sales data
- Prepare data for model training
- Export processed datasets

**Expected Processing Steps**:

1. **Data Loading**
   ```python
   import pandas as pd
   transactions = pd.read_csv('data/transactions.csv')
   products = pd.read_csv('data/products.csv')
   stores = pd.read_csv('data/stores.csv')
   ```

2. **Data Cleaning**
   - Remove duplicates
   - Handle missing values
   - Filter invalid transactions
   - Standardize data types

3. **Feature Engineering**
   - Date features (year, month, quarter, week, day_of_week)
   - Product features (category, subcategory, size)
   - Sales features (total_sales, quantity, discount)
   - Store features (location, country, city)
   - Holiday indicators
   - Seasonal patterns

4. **Data Aggregation**
   - Daily sales by product
   - Weekly sales by category
   - Monthly sales by subcategory
   - Quarterly trends

5. **Export**
   - Save processed data for model training
   - Create training/validation/test splits

---

### 2. retail_model.ipynb

**Purpose**: AutoGluon model training and forecasting

**Location**: `/model/retail_model.ipynb`

**Key Responsibilities**:
- Load processed data
- Configure AutoGluon for time series forecasting
- Train ensemble models
- Evaluate model performance
- Generate predictions
- Save trained models

**Expected Workflow**:

1. **Setup and Configuration**
   ```python
   from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
   import pandas as pd
   ```

2. **Data Preparation**
   ```python
   # Load processed data
   df = pd.read_csv('processed_sales_data.csv')
   
   # Convert to TimeSeriesDataFrame
   ts_df = TimeSeriesDataFrame.from_data_frame(
       df,
       id_column='product_id',
       timestamp_column='date'
   )
   ```

3. **Model Training**
   ```python
   predictor = TimeSeriesPredictor(
       prediction_length=30,  # Predict 30 days ahead
       target='sales',
       eval_metric='MAPE',
       path='models/retail_forecaster'
   )
   
   predictor.fit(
       train_data=ts_df,
       time_limit=3600,  # 1 hour training
       presets='best_quality'
   )
   ```

4. **Model Evaluation**
   ```python
   # Evaluate on validation set
   performance = predictor.evaluate(test_data)
   
   # View model leaderboard
   leaderboard = predictor.leaderboard(test_data)
   ```

5. **Generate Predictions**
   ```python
   # Forecast future sales
   predictions = predictor.predict(ts_df)
   ```

---

## AutoGluon Configuration

### Time Series Prediction

**Key Parameters**:

- `prediction_length`: Number of time steps to forecast (e.g., 30 days)
- `target`: Column name for the variable to predict (sales)
- `eval_metric`: Metric for model evaluation
  - MAPE (Mean Absolute Percentage Error)
  - RMSE (Root Mean Square Error)
  - MAE (Mean Absolute Error)

**Available Metrics**:
```python
eval_metrics = [
    'MAPE',      # Mean Absolute Percentage Error
    'sMAPE',     # Symmetric MAPE
    'RMSE',      # Root Mean Squared Error
    'MAE',       # Mean Absolute Error
    'MSE',       # Mean Squared Error
]
```

**Model Presets**:

1. **fast_training**: Quick models for prototyping
2. **medium_quality**: Balanced speed and accuracy
3. **best_quality**: Highest accuracy (longer training)
4. **high_quality**: Good accuracy with reasonable time

---

## Feature Engineering

### Time-Based Features

**Date Components**:
```python
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter
df['week'] = df['date'].dt.isocalendar().week
df['day_of_week'] = df['date'].dt.dayofweek
df['day_of_month'] = df['date'].dt.day
df['is_weekend'] = df['day_of_week'].isin([5, 6])
```

**Holiday Features**:
```python
import holidays
import numpy as np

us_holidays = holidays.US(years=range(2020, 2024))
df['is_holiday'] = df['date'].isin(us_holidays)

# TODO: Implement holiday distance calculations
# df['days_to_holiday'] = calculate_days_to_next_holiday(df['date'])
# df['days_since_holiday'] = calculate_days_since_last_holiday(df['date'])
```

**Seasonal Patterns**:
```python
# Cyclical encoding for month
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

# Cyclical encoding for day of week
df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
```

### Sales Features

**Aggregations**:
```python
# Daily sales by product
daily_sales = df.groupby(['product_id', 'date']).agg({
    'Line Total': 'sum',
    'Quantity': 'sum',
    'Discount': 'mean'
}).reset_index()

# Moving averages
df['sales_ma_7'] = df.groupby('product_id')['Line Total'].rolling(7).mean()
df['sales_ma_30'] = df.groupby('product_id')['Line Total'].rolling(30).mean()
```

**Lag Features**:
```python
# Previous sales
df['sales_lag_1'] = df.groupby('product_id')['Line Total'].shift(1)
df['sales_lag_7'] = df.groupby('product_id')['Line Total'].shift(7)
df['sales_lag_30'] = df.groupby('product_id')['Line Total'].shift(30)
```

---

## Model Architecture

### AutoGluon Ensemble

AutoGluon trains multiple models and combines them:

**Base Models**:
1. **DeepAR**: Deep learning model for probabilistic forecasting
2. **ETS**: Exponential smoothing state space model
3. **ARIMA**: AutoRegressive Integrated Moving Average
4. **Theta**: Classical forecasting method
5. **Naive**: Simple baseline (last value or seasonal naive)
6. **SeasonalNaive**: Seasonal baseline

**Ensemble Methods**:
- Simple averaging
- Weighted averaging (based on validation performance)
- Stacking (meta-learner combines predictions)

---

## Model Evaluation

### Metrics

**MAPE (Mean Absolute Percentage Error)**:
```
MAPE = (100 / n) * Σ|actual - predicted| / actual
```
- Lower is better
- Easy to interpret as percentage
- Sensitive to zero values

**RMSE (Root Mean Squared Error)**:
```
RMSE = √(Σ(actual - predicted)² / n)
```
- Penalizes large errors
- Same units as target variable

**MAE (Mean Absolute Error)**:
```
MAE = Σ|actual - predicted| / n
```
- Robust to outliers
- Easy to interpret

### Validation Strategy

**Time Series Cross-Validation**:
```python
# Split data chronologically
train_data = df[df['date'] < '2023-01-01']
validation_data = df[(df['date'] >= '2023-01-01') & (df['date'] < '2023-07-01')]
test_data = df[df['date'] >= '2023-07-01']
```

**Walk-Forward Validation**:
- Train on historical data
- Predict next period
- Add actual data to training set
- Repeat

---

## Prediction Generation

### Forecast Output

**Single Product Forecast**:
```python
# Forecast 30 days ahead for product_id=1234
forecast = predictor.predict(
    data=ts_df[ts_df['item_id'] == 1234],
    quantile_levels=[0.1, 0.5, 0.9]
)
```

**Output Format**:
```python
{
    'mean': [predicted_values],
    '0.1': [lower_bound],
    '0.9': [upper_bound]
}
```

### Batch Predictions

```python
# Forecast for all products
all_forecasts = predictor.predict(ts_df)

# Filter by category
category_forecasts = predictor.predict(
    ts_df[ts_df['category'] == 'Feminine']
)
```

---

## Model Persistence

### Save Trained Model

```python
# AutoGluon automatically saves to path
predictor = TimeSeriesPredictor(
    path='models/retail_forecaster',
    ...
)
predictor.fit(train_data)

# Model saved to models/retail_forecaster/
```

### Load Trained Model

```python
from autogluon.timeseries import TimeSeriesPredictor

# Load model
predictor = TimeSeriesPredictor.load('models/retail_forecaster')

# Generate predictions
predictions = predictor.predict(new_data)
```

---

## Integration with Backend

### Future Integration

To integrate forecasts with the Flask API:

1. **Load Model in Backend**:
```python
from autogluon.timeseries import TimeSeriesPredictor

predictor = TimeSeriesPredictor.load('model/retail_forecaster')
```

2. **Create Forecast Endpoint**:
```python
@forecast_bp.route('/predict', methods=['POST'])
def predict_sales():
    data = request.get_json()
    product_id = data['product_id']
    days_ahead = data.get('days_ahead', 30)
    
    # Prepare input data
    ts_data = prepare_timeseries_data(product_id)
    
    # Generate prediction
    forecast = predictor.predict(ts_data)
    
    return jsonify(forecast.to_dict())
```

3. **Cache Predictions**:
```python
import redis

r = redis.Redis()

# Cache forecast for 24 hours
r.setex(f'forecast:{product_id}', 86400, forecast.to_json())
```

---

## Performance Optimization

### Training Optimization

1. **Sample Data**: Train on subset for faster iteration
2. **Time Limit**: Set reasonable time_limit parameter
3. **Presets**: Use 'fast_training' for prototyping
4. **Parallel Training**: AutoGluon uses multiple cores

### Prediction Optimization

1. **Batch Predictions**: Predict multiple items at once
2. **Cache Results**: Store recent predictions
3. **Incremental Updates**: Only retrain when necessary
4. **Quantile Selection**: Request only needed quantiles

---

## Monitoring & Maintenance

### Model Monitoring

**Track Performance Over Time**:
```python
# Compare predictions vs actuals
actuals = get_actual_sales(date_range)
predictions = get_cached_predictions(date_range)

mae = mean_absolute_error(actuals, predictions)
mape = mean_absolute_percentage_error(actuals, predictions)

# Log metrics
logger.info(f"MAE: {mae}, MAPE: {mape}")
```

### Retraining Schedule

**When to Retrain**:
- Quarterly: Incorporate new sales data
- Performance degradation: MAPE increases significantly
- New products: Add to training data
- Seasonal changes: Before major seasons

**Retraining Process**:
1. Collect new transaction data
2. Run data processing notebook
3. Retrain model with updated data
4. Validate on holdout set
5. Deploy updated model

---

## Data Requirements

### Input Data Format

**Required Columns**:
- `item_id` or `product_id`: Unique identifier
- `timestamp` or `date`: Date/datetime of observation
- `target` or `sales`: Value to predict

**Optional Columns**:
- `category`, `subcategory`: Product attributes
- `store_id`: Location identifier
- `price`: Product price
- `discount`: Discount applied
- `holiday`: Holiday indicator

### Data Quality Checks

```python
# Check for missing values
df.isnull().sum()

# Check for duplicates
df.duplicated(['product_id', 'date']).sum()

# Check date range
print(f"Date range: {df['date'].min()} to {df['date'].max()}")

# Check for negative values
assert (df['sales'] >= 0).all(), "Negative sales found"
```

---

## Troubleshooting

### Common Issues

**Issue**: Model training fails with memory error

**Solution**: 
- Reduce training data size
- Use sample for prototyping
- Increase system memory
- Use cloud instance with more RAM

**Issue**: Poor prediction accuracy

**Solutions**:
- Add more relevant features
- Increase training time
- Use 'best_quality' preset
- Check for data leakage
- Validate feature engineering

**Issue**: Predictions too slow

**Solutions**:
- Cache predictions
- Batch predictions
- Use lighter models
- Reduce prediction_length

---

## Resources

- [AutoGluon Timeseries Documentation](https://auto.gluon.ai/stable/tutorials/timeseries/index.html)
- [Time Series Forecasting Guide](https://otexts.com/fpp3/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Holidays Package](https://pypi.org/project/holidays/)
