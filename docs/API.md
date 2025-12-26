# API Documentation

This document describes all available REST API endpoints in the Ennovar backend.

## Base URL

```
http://localhost:5000
```

## API Endpoints

### Products API

The Products API provides filtering capabilities for product categories, subcategories, and sizes.

#### Get All Categories

Get all unique product categories.

**Endpoint**: `GET /api/products/categories`

**Response**:
```json
[
  { "category": "Feminine" },
  { "category": "Masculine" },
  { "category": "Children" }
]
```

**Example**:
```bash
curl http://localhost:5000/api/products/categories
```

---

#### Get All Subcategories

Get all unique product subcategories.

**Endpoint**: `GET /api/products/sub_categories`

**Response**:
```json
[
  { "sub_category": "Coats and Blazers" },
  { "sub_category": "Dresses" },
  { "sub_category": "Shirts" }
]
```

**Example**:
```bash
curl http://localhost:5000/api/products/sub_categories
```

---

#### Get All Sizes

Get all unique product sizes.

**Endpoint**: `GET /api/products/size`

**Response**:
```json
[
  { "Size": "S" },
  { "Size": "M" },
  { "Size": "L" },
  { "Size": "XL" },
  { "Size": "XXL" }
]
```

**Example**:
```bash
curl http://localhost:5000/api/products/size
```

---

#### Get Subcategories by Category

Get all subcategories for a specific category.

**Endpoint**: `GET /api/products/subcategories/<category>`

**Parameters**:
- `category` (string, path parameter): The product category

**Response**:
```json
[
  { "sub_category": "Coats and Blazers" },
  { "sub_category": "Dresses" }
]
```

**Example**:
```bash
curl http://localhost:5000/api/products/subcategories/Feminine
```

---

#### Get Sizes by Category and Subcategory

Get all available sizes for a specific category and subcategory combination.

**Endpoint**: `GET /api/products/sizes/<category>/<sub_category>`

**Parameters**:
- `category` (string, path parameter): The product category
- `sub_category` (string, path parameter): The product subcategory

**Response**:
```json
[
  { "Size": "S" },
  { "Size": "M" },
  { "Size": "L" }
]
```

**Example**:
```bash
curl http://localhost:5000/api/products/sizes/Feminine/Dresses
```

---

### Sales API

The Sales API provides access to sales data with various filtering options.

#### Get Year Range

Get the minimum and maximum years available in the transaction database.

**Endpoint**: `GET /api/sales/year-range`

**Response**:
```json
{
  "min_year": 2020,
  "max_year": 2023
}
```

**Example**:
```bash
curl http://localhost:5000/api/sales/year-range
```

---

#### Get Subcategory Sales

Get total sales for a specific subcategory within a date range.

**Endpoint**: `POST /api/sales/subcategory`

**Request Body**:
```json
{
  "sub_category": "Dresses",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**:
```json
[
  {
    "total_sales": 125000.50
  }
]
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/sales/subcategory \
  -H "Content-Type: application/json" \
  -d '{
    "sub_category": "Dresses",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }'
```

---

#### Get Subcategory Sales by Category

Get sales for a subcategory with its parent category context.

**Endpoint**: `POST /api/sales/subcategory-by-category`

**Request Body**:
```json
{
  "sub_category": "Dresses",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**:
```json
[
  {
    "category": "Feminine",
    "sub_category": "Dresses",
    "total_sales": 125000.50
  }
]
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/sales/subcategory-by-category \
  -H "Content-Type: application/json" \
  -d '{
    "sub_category": "Dresses",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }'
```

---

#### Get Subcategory Sales by Category and Size

Get sales for a specific subcategory and size combination.

**Endpoint**: `POST /api/sales/subcategory-by-category-size`

**Request Body**:
```json
{
  "sub_category": "Dresses",
  "size": "M",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response**:
```json
[
  {
    "total_sales": 45000.25
  }
]
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/sales/subcategory-by-category-size \
  -H "Content-Type: application/json" \
  -d '{
    "sub_category": "Dresses",
    "size": "M",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }'
```

---

## Database Query Functions

These are internal functions used by the API endpoints (defined in `backend/utils/database.py`):

### Product Queries

- `get_categories()`: Get all unique categories
- `get_subcategories()`: Get all subcategories
- `get_sizes()`: Get all unique sizes
- `get_subcategory_by_category(category)`: Get subcategories for a category
- `get_sizes_by_category_subcategory(category, sub_category)`: Get sizes for category/subcategory

### Sales Queries

- `get_year_range()`: Get min and max years from transactions
- `get_category_sales(category, start_date, end_date)`: Get total sales for a category
- `get_sub_category_sales(sub_category, start_date, end_date)`: Get subcategory sales
- `get_sub_category_sales_based_on_category(sub_category, start_date, end_date)`: Get subcategory sales with category context
- `get_sub_category_sales_based_on_category_and_size(sub_category, size, start_date, end_date)`: Get sales for subcategory and size

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include a JSON body with error details:

```json
{
  "error": "Error description"
}
```

---

## Date Format

All date parameters should be in ISO format: `YYYY-MM-DD`

Examples:
- `2023-01-01`
- `2023-12-31`

---

## CORS

The API has CORS enabled to allow cross-origin requests from the frontend application.

---

## Authentication

Currently, the API does not require authentication. This should be added for production use.

---

## Rate Limiting

No rate limiting is currently implemented. Consider adding rate limiting for production deployments.
