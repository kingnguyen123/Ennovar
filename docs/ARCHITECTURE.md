# System Architecture

This document describes the overall architecture of the Ennovar retail sales forecasting system.

## Overview

Ennovar is a full-stack application that combines a Flask REST API backend with a React frontend dashboard. The system uses SQLite for data storage and AutoGluon for machine learning forecasting.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          React Application (Port 5173)                 │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │ │
│  │  │   App.jsx    │  │  Components  │  │  TailwindCSS│  │ │
│  │  │              │  │              │  │             │  │ │
│  │  │ - State Mgmt.│  │ - Controls   │  │ - Styling   │  │ │
│  │  │ - API calls  │  │ - Charts     │  │             │  │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/JSON (Fetch API)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Backend Layer                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Flask Application (Port 5000)                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │ │
│  │  │   app.py     │  │   Routes     │  │    Utils    │  │ │
│  │  │              │  │              │  │             │  │ │
│  │  │ - Flask app  │  │ - products   │  │ - database  │  │ │
│  │  │ - CORS       │  │ - sales      │  │   queries   │  │ │
│  │  │ - Blueprints │  │ - forecast   │  │             │  │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQL Queries (sqlite3)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Data Layer                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              SQLite Database (database.db)             │ │
│  │  ┌───────────┐ ┌────────────┐ ┌────────┐ ┌─────────┐  │ │
│  │  │ Products  │ │Transactions│ │ Stores │ │Discounts│  │ │
│  │  │ 17.9K rows│ │  6.4M rows │ │35 rows │ │181 rows │  │ │
│  │  └───────────┘ └────────────┘ └────────┘ └─────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Data Processing
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      ML/Analytics Layer                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Jupyter Notebooks & Models                │ │
│  │  ┌──────────────────┐  ┌──────────────────────────┐   │ │
│  │  │  Process_data    │  │    retail_model          │   │ │
│  │  │  .ipynb          │  │    .ipynb                │   │ │
│  │  │                  │  │                          │   │ │
│  │  │ - Data cleaning  │  │ - AutoGluon training     │   │ │
│  │  │ - Feature eng.   │  │ - Time series forecasting│   │ │
│  │  └──────────────────┘  └──────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Frontend (React + Vite)

**Location**: `/frontend`

**Key Technologies**:
- React 18
- Vite (build tool)
- TailwindCSS (styling)

**Main Components**:
- `App.jsx`: Root component with state management
- `ForecastControls.jsx`: Filter controls (category, date, size)
- `DashboardChart.jsx`: Sales visualization charts
- `MetricsPanel.jsx`: Key metrics display
- `NewsPanel.jsx`: News/alerts panel
- `ChatBox.jsx`: Chat interface component
- `InventoryBox.jsx`: Inventory status display

**State Management**:
- Uses React hooks (`useState`, `useEffect`)
- No external state management library
- Local component state with prop drilling

**API Communication**:
- Fetch API for HTTP requests
- Base URL: `http://localhost:5000`
- JSON data exchange

---

### 2. Backend (Flask)

**Location**: `/backend` and `app.py`

**Key Technologies**:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Pandas (data manipulation)
- SQLite3 (database driver)

**Application Structure**:

```python
app.py
├── Flask app initialization
├── CORS configuration
└── Blueprint registration
    ├── products_bp (/api/products)
    └── sales_bp (/api/sales)
```

**Routes**:

1. **Products Blueprint** (`/api/products`)
   - Category filtering
   - Subcategory filtering
   - Size filtering
   - Cascading filters

2. **Sales Blueprint** (`/api/sales`)
   - Year range retrieval
   - Sales data by subcategory
   - Sales data with filters
   - Aggregated sales metrics

**Utilities**:
- `database.py`: Centralized database query functions
- Uses Pandas DataFrames for data manipulation
- Returns JSON-serialized data

---

### 3. Data Layer (SQLite)

**Location**: `/database`

**Database File**: `database.db`

**Schema**:

```sql
-- Products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    category TEXT,
    sub_category TEXT,
    description TEXT,
    price REAL
);

-- Transactions table
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    store_id INTEGER,
    Size TEXT,
    "Unit Price" REAL,
    Date TEXT,
    Discount REAL,
    "Line Total" REAL,
    Currency TEXT,
    SKU TEXT,
    "Invoice Total" REAL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (store_id) REFERENCES stores(id)
);

-- Stores table
CREATE TABLE stores (
    id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    city TEXT,
    num_employees INTEGER,
    latitude REAL,
    longitude REAL
);

-- Discounts table
CREATE TABLE discounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_date TEXT,
    end_date TEXT,
    discount_rate REAL,
    description TEXT,
    category TEXT,
    sub_category TEXT
);
```

**Relationships**:
- Products (1) → Transactions (N)
- Stores (1) → Transactions (N)
- Transactions contain sales data linking products to stores

**Data Volume**:
- Products: ~17,940 records
- Transactions: ~6,416,827 records
- Stores: 35 records
- Discounts: 181 records

---

### 4. ML/Analytics Layer

**Location**: `/model`

**Notebooks**:

1. **Process_data.ipynb**
   - Data preprocessing
   - Feature engineering
   - Data cleaning and validation
   - Export processed data for modeling

2. **retail_model.ipynb**
   - AutoGluon model training
   - Time series forecasting
   - Model evaluation
   - Prediction generation

**ML Framework**: AutoGluon
- Automated machine learning
- Time series forecasting
- Ensemble models

---

## Data Flow

### 1. User Interaction Flow

```
User selects filters → React state updates → API request triggered
                                                    ↓
                                          Flask receives request
                                                    ↓
                                          Database query executed
                                                    ↓
                                          Pandas processes results
                                                    ↓
                                          JSON response sent
                                                    ↓
React state updated ← Frontend receives data ← API response
         ↓
UI re-renders with new data
```

### 2. Filter Cascade Flow

```
1. User selects Category
   ↓
2. API fetches subcategories for that category
   ↓
3. User selects Subcategory
   ↓
4. API fetches sizes for category + subcategory
   ↓
5. User selects Size
   ↓
6. API fetches sales data for all filters
```

### 3. Sales Data Query Flow

```
Frontend → POST /api/sales/subcategory-by-category-size
             ↓
           Request body: {
             sub_category: "Dresses",
             size: "M",
             start_date: "2023-01-01",
             end_date: "2023-12-31"
           }
             ↓
           backend/routes/sales.py
             ↓
           backend/utils/database.py
             ↓
           SQL query with JOIN on products and transactions
             ↓
           Pandas DataFrame
             ↓
           JSON response
             ↓
           Frontend updates metrics
```

---

## Security Considerations

### Current State

- No authentication implemented
- CORS enabled for all origins
- No rate limiting
- No input validation/sanitization
- Database queries use parameterized queries (SQL injection protected)

### Recommended Improvements

1. **Authentication**: Add JWT or session-based auth
2. **CORS**: Restrict to specific frontend origin
3. **Rate Limiting**: Implement request throttling
4. **Input Validation**: Validate all user inputs
5. **HTTPS**: Use SSL/TLS in production
6. **Environment Variables**: Move configuration to env files

---

## Scalability Considerations

### Current Limitations

- SQLite not suitable for high-concurrency writes
- Single-threaded Flask development server
- No caching layer
- All data loaded into memory for queries

### Scaling Recommendations

1. **Database**: Migrate to PostgreSQL or MySQL
2. **Application Server**: Use Gunicorn/uWSGI with multiple workers
3. **Caching**: Add Redis for frequently accessed data
4. **Load Balancing**: Nginx reverse proxy
5. **CDN**: Serve static frontend assets via CDN
6. **API Gateway**: Add API management layer

---

## Development Workflow

```
1. Backend Development
   - Modify routes in backend/routes/
   - Update database queries in backend/utils/database.py
   - Test with curl or Postman
   - Run: python app.py

2. Frontend Development
   - Modify components in frontend/src/
   - Update state management in App.jsx
   - Run: npm run dev
   - View at http://localhost:5173

3. Database Changes
   - Modify setup_database.py
   - Re-run database setup
   - Update queries in database.py

4. ML Model Updates
   - Work in Jupyter notebooks (model/)
   - Export models for backend integration
   - Update forecast endpoints
```

---

## Deployment Architecture

### Development

```
Local Machine
├── Backend: http://localhost:5000
├── Frontend: http://localhost:5173
└── Database: ./database/database.db
```

### Production (Recommended)

```
Cloud Infrastructure
├── Application Server (e.g., AWS EC2)
│   ├── Nginx (reverse proxy + static files)
│   ├── Gunicorn (Flask WSGI server)
│   └── Backend API
├── Database Server
│   └── PostgreSQL/MySQL
├── Object Storage (S3)
│   └── Frontend static assets
└── Load Balancer
```

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 | UI framework |
| Frontend | Vite | Build tool & dev server |
| Frontend | TailwindCSS | Styling |
| Backend | Flask | Web framework |
| Backend | Flask-CORS | CORS support |
| Database | SQLite | Data storage |
| Data Processing | Pandas | Data manipulation |
| ML | AutoGluon | Time series forecasting |
| ML | Jupyter | Interactive development |

---

## Performance Metrics

**API Response Times** (typical):
- Product filters: < 100ms
- Sales queries: 100-500ms (depending on date range)
- Year range: < 50ms

**Database Query Performance**:
- Simple filters: < 100ms
- Aggregated sales: 200-1000ms
- Joins with transactions: Varies with row count

**Frontend Rendering**:
- Initial load: < 2s
- Filter changes: < 500ms
- Chart updates: < 300ms
