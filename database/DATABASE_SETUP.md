# SQLite Database Setup Documentation

## Overview

This project includes a complete SQLite database setup with four interconnected tables loaded from CSV files. The database contains retail data including products, discounts, stores, and transactions.

## Database File

- **Location**: `database.db` (in the root directory)
- **Type**: SQLite 3
- **Size**: Optimized for 6.4M+ transactions

## Table Structure

### 1. Products Table

Stores information about all products in the retail system.

**Columns:**
- `id` (INTEGER PRIMARY KEY): Unique product identifier
- `category` (TEXT): Product category (e.g., Feminine, Masculine, Children)
- `sub_category` (TEXT): Product sub-category (e.g., Coats and Blazers, Dresses)
- `description` (TEXT): Product description in English
- `price` (REAL): Production cost of the product

**Example Query:**
```sql
SELECT * FROM products WHERE id = 1;
```

**Statistics:**
- Total Records: 17,940
- Categories: Multiple (Feminine, Masculine, Children)
- Price Range: $10.73 - $47.50+

---

### 2. Discounts Table

Stores all active and historical discount campaigns.

**Columns:**
- `start_date` (TEXT): Campaign start date (YYYY-MM-DD format)
- `end_date` (TEXT): Campaign end date (YYYY-MM-DD format)
- `discount_rate` (REAL): Discount percentage (e.g., 0.4 for 40%)
- `description` (TEXT): Campaign description
- `category` (TEXT): Product category the discount applies to
- `sub_category` (TEXT): Product sub-category the discount applies to

**Example Query:**
```sql
SELECT * FROM discounts 
WHERE start_date >= '2020-01-01' AND end_date <= '2020-12-31';
```

**Statistics:**
- Total Records: 181
- Discount Range: 0.1 (10%) to 0.5 (50%)
- Date Range: 2020-01-01 to 2023-12-31

---

### 3. Stores Table

Contains information about all retail store locations.

**Columns:**
- `id` (INTEGER PRIMARY KEY): Unique store identifier
- `name` (TEXT): Store name and location
- `country` (TEXT): Country where the store is located
- `city` (TEXT): City where the store is located
- `num_employees` (INTEGER): Number of employees at the store
- `latitude` (REAL): Geographic latitude coordinate
- `longitude` (REAL): Geographic longitude coordinate

**Example Query:**
```sql
SELECT name, city, country FROM stores WHERE country = 'United States';
```

**Statistics:**
- Total Records: 35
- Countries: Multiple (USA, China, Germany, etc.)
- Employees Range: 8-10 per store

---

### 4. Transactions Table

Records all sales transactions across all stores.

**Columns:**
- `product_id` (INTEGER): Reference to products table (FOREIGN KEY)
- `store_id` (INTEGER): Reference to stores table (FOREIGN KEY)

**Relationships:**
- `product_id` → `products.id`
- `store_id` → `stores.id`

**Example Query:**
```sql
SELECT * FROM transactions WHERE store_id = 1 LIMIT 10;
```

**Statistics:**
- Total Records: 6,416,827
- Time Period: 2020-2023
- Average Transactions per Store: ~183,338

---

## Database Relationships

```
products (1) ──────── (N) transactions
                           ↓
                           │
                           ↓
stores (1) ──────────── (N) transactions
```

**Foreign Key Constraints:**
- Transactions.product_id → Products.id
- Transactions.store_id → Stores.id

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- pandas library
- sqlite3 module (built-in with Python)

### Running the Setup Script

1. Navigate to the project root:
```bash
cd c:\Users\kingd\Ennovar
```

2. Run the setup script:
```bash
python setup_database.py
```

**Output Example:**
```
✓ Connected to database: C:\Users\kingd\Ennovar\database.db
✓ Created 'products' table
✓ Created 'discounts' table
✓ Created 'stores' table
✓ Created 'transactions' table

✓ All tables created successfully

Loading CSV files into database...

Loading products.csv...
  - Read 17940 rows from products.csv
✓ Loaded 17940 rows into 'products' table
...
✓ Database setup complete and all CSVs imported.
```

---

## Querying the Database

### Using Python with Pandas

```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('database.db')

# Example: Get top stores by transaction count
query = """
SELECT s.name, COUNT(t.product_id) as total_transactions
FROM transactions t
JOIN stores s ON t.store_id = s.id
GROUP BY s.id
ORDER BY total_transactions DESC
LIMIT 10
"""

df = pd.read_sql_query(query, conn)
print(df)

conn.close()
```

### Using SQLite Command Line

```bash
# Open database
sqlite3 database.db

# Run queries
sqlite> SELECT COUNT(*) FROM transactions;
sqlite> SELECT DISTINCT category FROM products;
sqlite> SELECT * FROM stores WHERE country = 'United States';
```

---

## Common Queries

### 1. Get Product Sales Summary

```sql
SELECT 
    p.id,
    p.description,
    COUNT(t.product_id) as times_sold,
    p.price
FROM transactions t
JOIN products p ON t.product_id = p.id
GROUP BY p.id
ORDER BY times_sold DESC
LIMIT 20;
```

### 2. Store Performance Analysis

```sql
SELECT 
    s.name,
    s.city,
    s.country,
    COUNT(t.product_id) as total_transactions,
    COUNT(DISTINCT t.product_id) as unique_products
FROM transactions t
JOIN stores s ON t.store_id = s.id
GROUP BY s.id
ORDER BY total_transactions DESC;
```

### 3. Active Discounts by Category

```sql
SELECT 
    category,
    sub_category,
    discount_rate,
    start_date,
    end_date
FROM discounts
WHERE start_date <= date('now') AND end_date >= date('now')
ORDER BY discount_rate DESC;
```

### 4. Monthly Transaction Trends

```sql
SELECT 
    DATE(transaction_date) as date,
    COUNT(*) as transaction_count
FROM transactions
GROUP BY DATE(transaction_date)
ORDER BY date;
```

---

## Data Validation

### Table Record Counts
- Products: 17,940 rows
- Discounts: 181 rows
- Stores: 35 rows
- Transactions: 6,416,827 rows

### Integrity Checks

All foreign key relationships are enforced:
```sql
-- Verify all transactions reference valid products
SELECT COUNT(DISTINCT product_id) FROM transactions;
-- Should return a number ≤ 17,940

-- Verify all transactions reference valid stores
SELECT COUNT(DISTINCT store_id) FROM transactions;
-- Should return a number ≤ 35
```

---

## Troubleshooting

### Issue: "no such table" error
**Solution**: Run `setup_database.py` to create tables and load data.

### Issue: "database is locked"
**Solution**: Ensure no other processes are accessing the database file.

### Issue: Foreign key constraint failed
**Solution**: This shouldn't occur with the provided setup, but if it does, check that all referenced IDs exist.

---

## Performance Tips

### For Large Queries
```sql
-- Use EXPLAIN QUERY PLAN to optimize queries
EXPLAIN QUERY PLAN
SELECT * FROM transactions WHERE store_id = 1;
```

### Create Indexes for Faster Queries
```sql
CREATE INDEX idx_transactions_store_id ON transactions(store_id);
CREATE INDEX idx_transactions_product_id ON transactions(product_id);
CREATE INDEX idx_products_category ON products(category);
```

---

## Maintenance

### Backup Database
```bash
# Create a backup copy
cp database.db database_backup.db
```

### Reset Database
```bash
# Delete and recreate
rm database.db
python setup_database.py
```

### Database File Size
- Current size: ~500 MB (compressed)
- The transactions table accounts for ~95% of the data

---

## Integration with Backend (Django)

To use this database with Django:

1. **Install sqlite adapter:**
```bash
pip install django
```

2. **Configure Django settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database.db',
    }
}
```

3. **Query from Django views:**
```python
from django.db import connection

def get_transactions(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM transactions 
            WHERE store_id = %s LIMIT 100
        """, [store_id])
        transactions = cursor.fetchall()
    return transactions
```

---

## Additional Resources

- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **Pandas SQL Documentation**: https://pandas.pydata.org/docs/user_guide/io.html#sql-queries
- **Python sqlite3 Module**: https://docs.python.org/3/library/sqlite3.html

---

## Support Scripts

### Query Examples Script
Run pre-made queries:
```bash
python query_database.py
```

This script demonstrates:
- Product information retrieval
- Store performance analysis
- Discount information
- Transaction analysis
- Sales summaries
- Database statistics

---

## Summary

| Feature | Details |
|---------|---------|
| Database Type | SQLite 3 |
| Total Records | 6.4M+ |
| Tables | 4 |
| Foreign Keys | Yes |
| Date Range | 2020-2023 |
| Geographic Scope | Global (35 stores) |
| Product Categories | 3+ |
| Ready for | Analytics, BI, ML |

