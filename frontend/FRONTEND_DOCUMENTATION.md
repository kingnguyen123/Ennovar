# Frontend Documentation - Ennovar Dashboard

## Table of Contents
1. [Overview](#overview)
2. [Application Architecture](#application-architecture)
3. [Components Reference](#components-reference)
4. [State Management](#state-management)
5. [API Endpoints](#api-endpoints)
6. [Key Functions](#key-functions)
7. [Data Flow](#data-flow)
8. [User Interactions](#user-interactions)

---

## Overview

The Ennovar Dashboard is a **React-based web application** built with **Vite** and styled with **TailwindCSS**. It provides a comprehensive retail analytics interface for:
- Viewing sales data by category, sub-category, and size
- Analyzing sales patterns over time with interactive charts
- Monitoring inventory levels
- Accessing news updates and AI chat assistance

### Tech Stack
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.8
- **Styling**: TailwindCSS 3.4.1
- **Charts**: Recharts (latest)
- **Module System**: ES Modules

---

## Application Architecture

### File Structure
```
frontend/
├── src/
│   ├── App.jsx                      # Main application component
│   ├── main.jsx                     # Application entry point
│   ├── index.css                    # Global styles
│   └── components/
│       ├── ForecastControls.jsx     # Top filter/control bar
│       ├── DashboardChart.jsx       # Sales pattern chart
│       ├── MetricsPanel.jsx         # Sales metrics display
│       ├── InventoryBox.jsx         # Inventory information
│       ├── NewsPanel.jsx            # News updates sidebar
│       └── ChatBox.jsx              # AI chat assistant
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.cjs
```

### Component Hierarchy
```
App
├── ForecastControls (Top Bar)
├── Main Content (Left & Center)
│   ├── Metrics Section
│   │   ├── Total Sales Card
│   │   ├── Predicted Sales Card
│   │   └── Current Inventory Card
│   └── DashboardChart (Sales Pattern)
└── Right Sidebar
    ├── NewsPanel
    └── ChatBox
```

---

## Components Reference

### 1. **App.jsx** (Main Component)
**Location**: `src/App.jsx`  
**Purpose**: Root component that manages application state and coordinates all child components

#### State Variables
| State | Type | Purpose |
|-------|------|---------|
| `timeframeType` | string | Selected time period type ('Year', 'Quarter', 'Month', 'Week') |
| `year` | string | Selected year for filtering |
| `month` | string | Selected month (1-12) |
| `quarter` | string | Selected quarter (Q1-Q4) |
| `week` | string | Selected week (1-52) |
| `category` | string | Selected product category |
| `subCategory` | string | Selected product sub-category |
| `Size` | string | Selected product size |
| `salesData` | object | Contains totalSales, predictedTotalSales, currentInventory |
| `salesPatternData` | array | Daily sales data for chart visualization |
| `loading` | boolean | Loading state for sales data |
| `chartLoading` | boolean | Loading state for chart data |
| `yearRange` | object | Available year range from database (min_year, max_year) |

#### Key Functions

##### `getDateRangeFromTimeframe()`
**Purpose**: Converts user-selected timeframe filters into start/end dates  
**Returns**: `{ startDate: 'YYYY-MM-DD', endDate: 'YYYY-MM-DD' }`  
**Logic**:
- **Year**: January 1 to December 31 of selected year
- **Quarter**: First day of quarter to last day of quarter
- **Month**: First day to last day of selected month
- **Week**: Calculates week 1 as first Monday of year, then adds 7 days × (week - 1)

##### useEffect Hooks

**1. Fetch Year Range** (runs once on mount)
```javascript
useEffect(() => {
  // Fetches min and max years from database
  // Sets yearRange and initializes year to max_year
}, [])
```

**2. Fetch Sales Data** (runs when filters change)
```javascript
useEffect(() => {
  // Only runs if category AND subCategory are selected
  // Calls: POST /api/sales/subcategory-by-category-size
  // Updates: salesData.totalSales
}, [category, subCategory, Size, timeframeType, year, month, quarter, week])
```

**3. Fetch Sales Pattern Data** (runs when filters change)
```javascript
useEffect(() => {
  // Only runs if category AND subCategory are selected
  // Calls: POST /api/sales/sales-pattern
  // Updates: salesPatternData (array for chart)
}, [category, subCategory, Size, timeframeType, year, month, quarter, week])
```

**4. Fetch Inventory Data** (runs when category/size changes)
```javascript
useEffect(() => {
  // Calls: POST /api/inventory/subcategory-by-category-size
  // Updates: salesData.currentInventory
}, [category, subCategory, Size])
```

---

### 2. **ForecastControls.jsx**
**Location**: `src/components/ForecastControls.jsx`  
**Purpose**: Top navigation bar with all filter controls

#### Props
| Prop | Type | Description |
|------|------|-------------|
| `timeframeType` | string | Current timeframe type |
| `year`, `month`, `quarter`, `week` | string | Time period values |
| `category`, `subCategory`, `Size` | string | Product filter values |
| `onTimeframeTypeChange`, etc. | function | Callback functions to update state |
| `yearRange` | object | Available years from database |

#### Local State
| State | Type | Purpose |
|-------|------|---------|
| `categories` | array | List of available categories from API |
| `subCategories` | array | List of sub-categories for selected category |
| `sizes` | array | List of sizes for selected category + sub-category |
| `loading` | boolean | Loading state for dropdown data |

#### Key Functions

##### `getWeeksInMonth(yearVal, monthVal)`
**Purpose**: Calculates how many weeks exist in a given month  
**Returns**: Array of week numbers (e.g., ['1', '2', '3', '4'])  
**Formula**: `Math.ceil((lastDay + firstDay.getDay()) / 7)`

##### useEffect Hooks

**1. Fetch Categories** (runs once on mount)
```javascript
useEffect(() => {
  // Calls: GET /api/products/categories
  // Populates categories dropdown
}, [])
```

**2. Fetch Sub-Categories** (runs when category changes)
```javascript
useEffect(() => {
  // Calls: GET /api/products/subcategories/{category}
  // Populates subCategories dropdown
  // Clears if no category selected
}, [category])
```

**3. Fetch Sizes** (runs when category or subCategory changes)
```javascript
useEffect(() => {
  // Calls: GET /api/products/sizes/{category}/{subCategory}
  // Populates sizes dropdown
  // Clears if missing category or subCategory
}, [category, subCategory])
```

#### Conditional Rendering
- **Quarter dropdown**: Only shows when `timeframeType === 'Quarter'`
- **Month input**: Only shows when `timeframeType === 'Month'`
- **Week input**: Only shows when `timeframeType === 'Week'`
- **Year dropdown**: Always visible
- Dropdowns disable when dependent data is not loaded

---

### 3. **DashboardChart.jsx**
**Location**: `src/components/DashboardChart.jsx`  
**Purpose**: Displays interactive area chart showing sales patterns over time

#### Props
| Prop | Type | Description |
|------|------|-------------|
| `salesPatternData` | array | Daily sales data `[{Date, total_sales, total_quantity}]` |
| `loading` | boolean | Whether chart is loading |
| `timeRange` | string | Display text for selected time range |

#### Key Features
- **Chart Type**: Area chart with gradient fill (Recharts)
- **X-Axis**: Date (from transactions)
- **Y-Axis**: Total Sales (formatted as currency)
- **Tooltip**: Custom component showing Date, Sales ($), and Quantity
- **Empty State**: Shows placeholder when no data available
- **Loading State**: Shows spinner when fetching data

#### CustomTooltip Component
```javascript
const CustomTooltip = ({ active, payload, label }) => {
  // Displays formatted date and sales/quantity values
  // Only renders when hovering over chart
}
```

#### Visual Design
- **Gradient**: Blue gradient fill (#3B82F6 fading to transparent)
- **Grid**: Dashed grid lines for readability
- **Responsive**: Adapts to container width using `ResponsiveContainer`

---

### 4. **MetricsPanel.jsx**
**Location**: `src/components/MetricsPanel.jsx`  
**Purpose**: Displays total sales and predicted sales metrics

#### Props
| Prop | Type | Description |
|------|------|-------------|
| `totalSales` | number | Total sales amount |
| `predictedTotalSales` | number | Forecasted sales amount |

**Note**: This component is currently not used in App.jsx (metrics are displayed inline instead)

---

### 5. **NewsPanel.jsx**
**Location**: `src/components/NewsPanel.jsx`  
**Purpose**: Displays news and market updates in right sidebar

#### Features
- **Static Data**: Currently shows hardcoded news articles
- **Article Structure**: Each article has `id`, `title`, `date`, `category`
- **Styling**: Hover effects and category badges
- **Action Button**: "View All News" button at bottom

#### Future Enhancement Opportunity
Could be connected to news API for real-time updates

---

### 6. **ChatBox.jsx**
**Location**: `src/components/ChatBox.jsx`  
**Purpose**: Interactive chat interface for AI assistance

#### Local State
| State | Type | Purpose |
|-------|------|---------|
| `messages` | array | Chat message history `[{id, type, text}]` |
| `inputValue` | string | Current user input |

#### Key Functions

##### `handleSendMessage()`
**Purpose**: Processes user message submission  
**Process**:
1. Validates input is not empty
2. Adds user message to messages array
3. Clears input field
4. Simulates bot response after 500ms delay

#### Message Types
- **user**: Right-aligned, blue background
- **bot**: Left-aligned, gray background

#### Features
- Enter key support for sending messages
- Auto-scroll to latest message
- Message bubbles with rounded corners

---

## State Management

### State Flow Diagram
```
User Interaction
    ↓
ForecastControls onChange callback
    ↓
App state update (e.g., setCategory)
    ↓
useEffect dependency triggers
    ↓
API call (fetch)
    ↓
State update (setSalesData, setSalesPatternData, etc.)
    ↓
Component re-renders with new data
```

### State Dependencies
```
category → subCategories (in ForecastControls)
category + subCategory → sizes (in ForecastControls)
category + subCategory + Size + timeframe → totalSales
category + subCategory + Size + timeframe → salesPatternData
category + subCategory + Size → currentInventory
```

---

## API Endpoints

### Backend Base URL
```
http://localhost:5000
```

### 1. Products API

#### GET `/api/products/categories`
**Purpose**: Fetch all product categories  
**Response**: `[{category: string}]`

#### GET `/api/products/subcategories/:category`
**Purpose**: Fetch sub-categories for a category  
**Response**: `[{sub_category: string}]`

#### GET `/api/products/sizes/:category/:subCategory`
**Purpose**: Fetch sizes for category + sub-category  
**Response**: `[{Size: string}]`

### 2. Sales API

#### GET `/api/sales/year-range`
**Purpose**: Get min and max years from database  
**Response**: `{min_year: number, max_year: number}`

#### POST `/api/sales/subcategory-by-category-size`
**Purpose**: Fetch total sales for selected filters  
**Request Body**:
```json
{
  "category": "Feminine",
  "sub_category": "Sportswear",
  "size": "M",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```
**Response**: `[{total_sales: number}]`

#### POST `/api/sales/sales-pattern`
**Purpose**: Fetch daily sales data for chart  
**Request Body**:
```json
{
  "category": "Feminine",
  "sub_category": "Sportswear",
  "size": "M",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```
**Response**:
```json
[
  {"Date": "2024-01-01", "total_sales": 1500.50, "total_quantity": 25},
  {"Date": "2024-01-02", "total_sales": 2300.75, "total_quantity": 38},
  ...
]
```

### 3. Inventory API

#### POST `/api/inventory/subcategory-by-category-size`
**Purpose**: Fetch current inventory  
**Request Body**:
```json
{
  "category": "Feminine",
  "sub_category": "Sportswear",
  "size": "M"
}
```
**Response**: `[{"Current Inventory": number}]`

---

## Key Functions

### Date Calculation Functions

#### Converting Timeframes to Dates
The app uses native JavaScript `Date` objects to calculate date ranges:

```javascript
// Year: Full calendar year
new Date(2024, 0, 1)    // Jan 1, 2024
new Date(2024, 11, 31)  // Dec 31, 2024

// Quarter: 3-month periods
// Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec
const quarterNum = 2  // Q2
const startMonth = (quarterNum - 1) * 3  // 3 (April, 0-indexed)
new Date(2024, startMonth, 1)  // Apr 1, 2024
new Date(2024, quarterNum * 3, 0)  // Jun 30, 2024

// Month: First to last day of month
new Date(2024, 5, 1)   // Jun 1, 2024 (month is 0-indexed)
new Date(2024, 6, 0)   // Jun 30, 2024 (day 0 = last day of prev month)

// Week: 7-day periods starting from first Monday
// Algorithm finds first Monday of year, then adds weeks
```

### Data Formatting Functions

#### Number Formatting
```javascript
// Currency formatting
value.toLocaleString()  // 1500.50 → "1,500.50"
`$${value.toLocaleString()}`  // → "$1,500.50"

// Date formatting
date.toISOString().split('T')[0]  // Date → "2024-01-15"
```

---

## Data Flow

### Complete Request Lifecycle

#### 1. User Selects Category
```
User clicks "Feminine" in ForecastControls
    ↓
onCategoryChange('Feminine') called
    ↓
App state: category = 'Feminine'
    ↓
ForecastControls useEffect triggers
    ↓
API call: GET /api/products/subcategories/Feminine
    ↓
subCategories array populated in ForecastControls
    ↓
Dropdown enables with subcategory options
```

#### 2. User Selects Sub-Category
```
User selects "Sportswear"
    ↓
onSubCategoryChange('Sportswear') called
    ↓
App state: subCategory = 'Sportswear'
    ↓
Multiple useEffects trigger in App.jsx:
    ├─ Fetch sales data
    ├─ Fetch sales pattern data
    └─ Fetch inventory data
    ↓
ForecastControls useEffect triggers
    ↓
API call: GET /api/products/sizes/Feminine/Sportswear
    ↓
sizes dropdown populated
```

#### 3. Sales Data Fetch
```
App useEffect (sales) triggered
    ↓
getDateRangeFromTimeframe() calculates dates
    ↓
API call: POST /api/sales/subcategory-by-category-size
    ↓
Response: [{total_sales: 15000}]
    ↓
setSalesData updates totalSales
    ↓
Metrics card re-renders with new value
```

#### 4. Chart Data Fetch
```
App useEffect (sales pattern) triggered
    ↓
getDateRangeFromTimeframe() calculates dates
    ↓
API call: POST /api/sales/sales-pattern
    ↓
Response: [{Date: '2024-01-01', total_sales: 500, ...}, ...]
    ↓
setSalesPatternData updates
    ↓
DashboardChart re-renders with new data
    ↓
Recharts renders area chart
```

---

## User Interactions

### Workflow Examples

#### Scenario 1: Viewing Monthly Sales for a Product
1. **Select Timeframe Type**: User clicks "Month" dropdown
2. **Select Year**: User selects "2024"
3. **Select Month**: User enters "6" (June)
4. **Select Category**: User selects "Feminine"
5. **Select Sub-Category**: User selects "Sportswear"
6. **Select Size** (optional): User selects "M"

**Result**:
- Total Sales card shows June 2024 sales for Feminine/Sportswear/M
- Chart displays daily sales pattern for June 2024
- Inventory card shows current stock level

#### Scenario 2: Comparing Quarterly Performance
1. User selects "Quarter" timeframe
2. User selects year "2024"
3. User selects "Q1" (Jan-Mar)
4. Selects category and subcategory
5. Views sales chart for Q1
6. Changes to "Q2" to compare
7. Chart updates to show Q2 data

#### Scenario 3: Using Chat Assistant
1. User types "What does the forecast suggest?"
2. Presses Enter or clicks Send
3. Message appears on right side (user bubble)
4. After 500ms, bot responds with message
5. Conversation continues in chat history

---

## Performance Considerations

### Optimization Strategies

1. **Conditional API Calls**
   - Sales/chart data only fetches when category AND subCategory selected
   - Prevents unnecessary API calls on page load

2. **Dependency Arrays**
   - useEffect hooks carefully track dependencies
   - Prevents infinite loops and redundant fetches

3. **Loading States**
   - Separate loading states for different data sections
   - `loading` for sales metrics
   - `chartLoading` for chart data
   - Prevents UI blocking

4. **useMemo for Years**
   - Years array calculated with useMemo in ForecastControls
   - Prevents recalculation on every render

5. **Responsive Chart**
   - ResponsiveContainer ensures chart adapts to screen size
   - No hardcoded dimensions

---

## Styling System

### TailwindCSS Classes

#### Custom CSS Classes (from index.css)
```css
.metric-box         /* Card styling for metrics */
.chart-container    /* Container for chart area */
.dropdown-select    /* Styled select dropdowns */
.button-primary     /* Primary action buttons */
.button-secondary   /* Secondary action buttons */
.sidebar-panel      /* Right sidebar panels */
```

#### Responsive Layout
- **Mobile**: Single column, stacked layout
- **Tablet**: `md:` breakpoint adapts metrics to 3 columns
- **Desktop**: `lg:` breakpoint shows sidebar on right

### Color Scheme
- **Primary**: Blue (#3B82F6) - charts, primary buttons
- **Success**: Green - positive metrics, inventory
- **Gray Scale**: UI elements, borders, text hierarchy

---

## Error Handling

### API Error Handling Pattern
```javascript
fetch(url)
  .then(res => res.json())
  .then(data => {
    // Success: update state
  })
  .catch(err => {
    console.error('Error:', err)
    // Fallback: reset state to defaults
  })
```

### Defensive Coding
- Null checks: `data[0]?.total_sales ?? 0`
- Empty array defaults: `setSalesPatternData([])`
- Disabled dropdowns when dependencies not met
- Input validation for month (1-12) and week (1-52)

---

## Future Enhancement Opportunities

1. **Real-time Updates**: WebSocket connection for live data
2. **Export Functionality**: Download charts as images or data as CSV
3. **Advanced Filters**: Date range picker, multi-select categories
4. **Forecasting Model**: Integrate ML predictions with backend
5. **User Authentication**: Login system with personalized dashboards
6. **Theme Switching**: Dark mode support
7. **Mobile App**: React Native version
8. **Caching**: LocalStorage or Redux for offline capability
9. **Analytics**: Track user interactions with analytics library
10. **News API Integration**: Replace static news with real feeds

---

## Debugging Tips

### Console Logging
The app has extensive console logging with prefixes:
- `[App]` - Main component logs
- `[App ERROR]` - Error messages
- `[App WARNING]` - Warning messages

### Common Issues

**Problem**: Chart not displaying  
**Solution**: Check that category AND subCategory are selected, check browser console for API errors

**Problem**: Dropdowns disabled  
**Solution**: Ensure previous dropdown selections are made (category → subCategory → size)

**Problem**: Wrong date range  
**Solution**: Verify timeframe type matches selected period inputs (month/quarter/week)

**Problem**: API 404 errors  
**Solution**: Ensure backend is running on localhost:5000

### Development Mode
```bash
cd frontend
npm run dev
```
This starts Vite dev server with hot reload on http://localhost:5173

---

## Quick Reference

### Start Application
```bash
# Backend
cd C:\Users\kingd\Ennovar
python app.py

# Frontend
cd frontend
npm run dev
```

### Install Dependencies
```bash
cd frontend
npm install
```

### Build for Production
```bash
cd frontend
npm run build
```

---

## Component Props Summary

| Component | Required Props | Optional Props |
|-----------|---------------|----------------|
| App | None (root) | None |
| ForecastControls | All time/filter values + callbacks + yearRange | None |
| DashboardChart | salesPatternData, loading, timeRange | None |
| MetricsPanel | totalSales, predictedTotalSales | None |
| NewsPanel | None | None |
| ChatBox | None | None |

---

**Document Version**: 1.0  
**Last Updated**: December 25, 2025  
**Maintained By**: Ennovar Team
