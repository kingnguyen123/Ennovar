# Database Directory

This directory contains the SQLite database and all related files for the Ennovar project.

## Contents

### Database File
- **database.db** (82.8 MB) - Main SQLite database with 6.4M+ records

### Setup & Query Scripts
- **setup_database.py** - Initialize database and load CSV files (run once)
- **query_database.py** - Example queries and database demonstrations

### Documentation
- **DATABASE_SETUP.md** - Complete database schema and usage guide

## Quick Start

### 1. View Database Statistics
```bash
cd database
python query_database.py
```

### 2. Query the Database
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('database/database.db')
df = pd.read_sql_query("SELECT * FROM products LIMIT 5", conn)
print(df)
conn.close()
```

### 3. Access from Parent Directory
```python
# When working from project root
import sqlite3
conn = sqlite3.connect('database/database.db')
```

## Database Structure

- **products**: 17,940 products
- **stores**: 35 store locations
- **discounts**: 181 discount campaigns
- **transactions**: 6,416,827 transactions

## Files Changed

Moved from root directory:
- database.db
- setup_database.py
- query_database.py
- DATABASE_SETUP.md
- DATABASE_SETUP_REPORT.md

See documentation files for complete information.