# SQLite Database - Complete Setup & Usage Guide

## 🎯 Project Overview

This guide covers the complete SQLite database setup for the Ennovar retail forecasting project. The database contains **6.4M+ transactions** across **35 stores** and **17,940 products**.

---

## 📦 What You Get

### ✓ Database File
- **database.db** (79 MB) - Production-ready SQLite database
- 4 interconnected tables
- 6,434,983 total records
- Foreign key relationships

### ✓ Setup Scripts
- **setup_database.py** - Initialize and load data
- **query_database.py** - Example queries
- **database_utils.py** - Utility functions

### ✓ Documentation
- **DATABASE_SETUP.md** - Complete reference
- **DATABASE_SETUP_REPORT.md** - Implementation summary
- **This file** - Quick start guide

---

## 🚀 Quick Start (5 minutes)

### Step 1: Verify Database Exists
```bash
cd c:\Users\kingd\Ennovar
dir database.db
# Output: database.db 82,817,024 bytes
```

### Step 2: Run Example Queries
```bash
python .venv\Scripts\python.exe query_database.py
```

### Step 3: Use Database Manager
```bash
python .venv\Scripts\python.exe database_utils.py
```

---

## 📊 Database Structure

### Quick Reference

```
database.db (79 MB)
├── products (17,940 rows)
│   └── id, category, sub_category, description, price
├── discounts (181 rows)
│   └── start_date, end_date, discount_rate, category, sub_category
├── stores (35 rows)
│   └── id, name, city, country, employees, latitude, longitude
└── transactions (6,416,827 rows)
    └── product_id → products.id
    └── store_id → stores.id
```

### Table Details

| Table | Records | Primary Keys | Foreign Keys |
|-------|---------|--------------|--------------|
| products | 17,940 | id | None |
| discounts | 181 | auto | None |
| stores | 35 | id | None |
| transactions | 6,416,827 | None | product_id, store_id |

---

## 💻 Usage Examples

### Python with Pandas

```python
import sqlite3
import pandas as pd

# Connect
conn = sqlite3.connect('database.db')

# Simple query
df = pd.read_sql_query("SELECT * FROM products LIMIT 5", conn)
print(df)

# Join query
query = """
SELECT p.description, COUNT(t.product_id) as sales
FROM transactions t
JOIN products p ON t.product_id = p.id
GROUP BY p.id
ORDER BY sales DESC
LIMIT 10
"""
df = pd.read_sql_query(query, conn)
print(df)

conn.close()
```

### Using Database Manager

```python
from database_utils import DatabaseManager

# Create manager
db = DatabaseManager()
db.connect()

# Get database summary
db.print_database_summary()

# Get top products
top_products = db.get_top_products(10)
print(top_products)

# Get store stats
store_stats = db.get_store_stats()
print(store_stats)

db.disconnect()
```

### Command Line (SQLite CLI)

```bash
sqlite3 database.db

# View products
sqlite> SELECT * FROM products LIMIT 5;

# Count transactions
sqlite> SELECT COUNT(*) FROM transactions;

# Find store info
sqlite> SELECT name, city FROM stores WHERE country='United States';

# Exit
sqlite> .exit
```

---

## 🔍 Common Queries

### 1. Top Products
```sql
SELECT p.id, p.description, COUNT(*) as sales_count
FROM transactions t
JOIN products p ON t.product_id = p.id
GROUP BY p.id
ORDER BY sales_count DESC
LIMIT 20;
```

### 2. Store Performance
```sql
SELECT s.name, s.city, COUNT(*) as transactions
FROM transactions t
JOIN stores s ON t.store_id = s.id
GROUP BY s.id
ORDER BY transactions DESC;
```

### 3. Active Discounts
```sql
SELECT * FROM discounts
WHERE start_date <= date('now') 
AND end_date >= date('now')
ORDER BY discount_rate DESC;
```

### 4. Product by Category
```sql
SELECT category, sub_category, COUNT(*) as product_count
FROM products
GROUP BY category, sub_category
ORDER BY category;
```

### 5. Sales by Geography
```sql
SELECT s.country, s.city, COUNT(*) as total_sales
FROM transactions t
JOIN stores s ON t.store_id = s.id
GROUP BY s.country, s.city
ORDER BY total_sales DESC;
```

---

## 🛠️ Utility Functions

### DatabaseManager Class

```python
# Initialize
db = DatabaseManager('database.db')
db.connect()

# Available methods:
db.get_table_info('products')          # Show table schema
db.get_all_tables()                    # List all tables
db.get_table_count('transactions')     # Count rows
db.execute_query("SELECT * FROM...")   # Run custom query
db.get_top_products(limit=10)          # Get best sellers
db.get_store_stats()                   # Store performance
db.get_database_stats()                # Overall stats
db.export_to_csv(query, 'output.csv')  # Export data
db.print_database_summary()            # Print summary
db.disconnect()                        # Close connection
```

---

## 📈 Data Analysis

### Key Metrics

```python
from database_utils import DatabaseManager

db = DatabaseManager()
db.connect()

# Total transactions
total_tx = pd.read_sql_query(
    "SELECT COUNT(*) as count FROM transactions", db.conn
)["count"][0]
print(f"Total Transactions: {total_tx:,}")

# Total unique products sold
unique_products = pd.read_sql_query(
    "SELECT COUNT(DISTINCT product_id) as count FROM transactions", 
    db.conn
)["count"][0]
print(f"Unique Products Sold: {unique_products:,}")

# Average transactions per store
avg_per_store = total_tx / 35
print(f"Average per Store: {avg_per_store:,.0f}")

db.disconnect()
```

---

## 🔗 Integration Guide

### With Django Backend

```python
# views.py
from django.db import connection
import pandas as pd

def forecast_data(request):
    query = """
    SELECT s.name, COUNT(*) as transaction_count
    FROM transactions t
    JOIN stores s ON t.store_id = s.id
    WHERE DATE(transaction_date) >= date('now', '-30 days')
    GROUP BY s.id
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    
    return JsonResponse({'stores': data})
```

### With Flask Backend

```python
# app.py
from flask import jsonify
import sqlite3

@app.route('/api/sales/top-products', methods=['GET'])
def top_products():
    conn = sqlite3.connect('database.db')
    query = """
    SELECT p.description, COUNT(*) as sales
    FROM transactions t
    JOIN products p ON t.product_id = p.id
    GROUP BY p.id
    ORDER BY sales DESC
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return jsonify(df.to_dict('records'))
```

### With React Frontend

```javascript
// fetchSalesData.js
async function getSalesData() {
  const response = await fetch('/api/sales/summary');
  const data = await response.json();
  return data;
}

// Use in component
useEffect(() => {
  getSalesData().then(data => {
    setSalesData(data);
  });
}, []);
```

---

## 🎯 Use Cases

### 1. Sales Forecasting
- Train ML models on historical transaction data
- Predict future sales by product/store
- Identify seasonal trends

### 2. Inventory Optimization
- Determine optimal stock levels
- Predict stockout risks
- Manage discounts based on inventory

### 3. Store Performance Analysis
- Compare stores by transaction volume
- Analyze geographic performance
- Identify top/bottom performers

### 4. Product Analytics
- Find best-selling products
- Analyze product lifecycle
- Track discount effectiveness

### 5. Customer Insights
- Store-specific preferences
- Category performance
- Discount impact analysis

---

## ⚡ Performance Tips

### Query Optimization

```sql
-- Create indexes for faster queries
CREATE INDEX idx_transaction_product ON transactions(product_id);
CREATE INDEX idx_transaction_store ON transactions(store_id);
CREATE INDEX idx_product_category ON products(category);

-- Check query plan
EXPLAIN QUERY PLAN 
SELECT * FROM transactions WHERE store_id = 1;
```

### Pagination for Large Results

```python
# Fetch in chunks
limit = 10000
offset = 0

query = f"""
SELECT * FROM transactions 
LIMIT {limit} OFFSET {offset}
"""

while True:
    df = pd.read_sql_query(query, conn)
    if len(df) == 0:
        break
    # Process df
    offset += limit
```

---

## 🔐 Backup & Maintenance

### Backup Database
```bash
# Create backup copy
copy database.db database_backup.db

# Or from Python
import shutil
shutil.copy('database.db', 'database_backup.db')
```

### Reset Database
```bash
# Delete and recreate
del database.db
python setup_database.py
```

### Check Database Integrity
```sql
PRAGMA integrity_check;
```

---

## 🐛 Troubleshooting

### Error: "database is locked"
**Solution**: Ensure no other processes are accessing the file.
```python
# Add timeout
conn = sqlite3.connect('database.db', timeout=30)
```

### Error: "no such table"
**Solution**: Run setup_database.py to recreate tables.
```bash
python setup_database.py
```

### Slow Queries
**Solution**: Create indexes or optimize query.
```sql
CREATE INDEX idx_name ON table_name(column);
```

### Connection Issues
**Solution**: Check file permissions and path.
```bash
# Verify file exists
ls -la database.db
# Check permissions
chmod 644 database.db
```

---

## 📚 Additional Resources

- **SQLite Official**: https://www.sqlite.org/
- **SQLite Commands**: https://www.sqlite.org/cli.html
- **Pandas SQL**: https://pandas.pydata.org/docs/user_guide/io.html#sql-queries
- **Python sqlite3**: https://docs.python.org/3/library/sqlite3.html

---

## 📋 Checklist

- [x] Database created (database.db)
- [x] 4 tables created and populated
- [x] Foreign keys established
- [x] 6.4M+ records loaded
- [x] Setup scripts working
- [x] Query examples provided
- [x] Utility functions created
- [x] Documentation complete
- [x] Integration guides provided
- [x] Ready for production

---

## 🎉 Summary

Your SQLite database is **production-ready** with:
- ✓ 79 MB database with 6.4M+ records
- ✓ Proper schema with relationships
- ✓ Utility functions for easy access
- ✓ Example queries for common tasks
- ✓ Integration guides for backends
- ✓ Complete documentation

**Status: READY FOR USE** ✓

---

## 📞 Need Help?

Refer to the comprehensive documentation:
- **DATABASE_SETUP.md** - Full reference guide
- **database_utils.py** - Source code with comments
- **setup_database.py** - Setup implementation
- **query_database.py** - Query examples

