# Frontend Documentation

This document provides comprehensive documentation for the Ennovar frontend React application.

## Overview

The frontend is a modern React application built with Vite and styled with TailwindCSS. It provides an interactive dashboard for visualizing sales data and forecasts.

## Technology Stack

- **React 18.2**: UI library
- **Vite 5.0**: Build tool and development server
- **TailwindCSS 3.4**: Utility-first CSS framework
- **PostCSS**: CSS processing
- **Autoprefixer**: Automatic CSS vendor prefixes

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # React components
│   │   ├── ChatBox.jsx
│   │   ├── DashboardChart.jsx
│   │   ├── ForecastControls.jsx
│   │   ├── InventoryBox.jsx
│   │   ├── MetricsPanel.jsx
│   │   └── NewsPanel.jsx
│   ├── App.jsx           # Root component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles
├── index.html            # HTML template
├── package.json          # Dependencies
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind configuration
└── postcss.config.cjs   # PostCSS configuration
```

## Components

### App.jsx (Root Component)

The main application component that manages global state and orchestrates all child components.

**State Variables**:

```javascript
// Timeframe filters
const [timeframeType, setTimeframeType] = useState('Month')
const [year, setYear] = useState(new Date().getFullYear().toString())
const [month, setMonth] = useState((new Date().getMonth() + 1).toString())
const [quarter, setQuarter] = useState('0')
const [week, setWeek] = useState('0')

// Product filters
const [category, setCategory] = useState('0')
const [subCategory, setSubCategory] = useState('0')
const [Size, setSize] = useState('0')

// Sales data
const [salesData, setSalesData] = useState({
  totalSales: 0,
  predictedTotalSales: 0,
  currentInventory: 0,
})

// UI state
const [loading, setLoading] = useState(false)
const [yearRange, setYearRange] = useState({ min_year: 2024, max_year: 2024 })
```

**Key Functions**:

1. `getDateRangeFromTimeframe()`: Calculates start and end dates based on selected timeframe
   - Supports: Year, Quarter, Month, Week
   - Returns ISO date strings

2. `useEffect` for year range: Fetches available years from database on mount

3. `useEffect` for sales data: Fetches sales when filters change

**API Calls**:
- `GET /api/sales/year-range`: Fetch available years
- `POST /api/sales/subcategory-by-category-size`: Fetch sales data

---

### ForecastControls.jsx

Dropdown controls for filtering data by timeframe and product attributes.

**Props**:
```javascript
{
  timeframeType, year, month, quarter, week,
  category, subCategory, Size,
  onTimeframeTypeChange, onYearChange, onMonthChange,
  onQuarterChange, onWeekChange, onCategoryChange,
  onSubCategoryChange, onSizeChange,
  yearRange
}
```

**Features**:
- **Cascading Filters**: Subcategories depend on category, sizes depend on both
- **Dynamic Options**: Fetches options from API
- **Conditional Rendering**: Shows relevant controls based on timeframe type
- **Loading States**: Disables controls while data loads

**State Variables**:
```javascript
const [categories, setCategories] = useState([])
const [subCategories, setSubCategories] = useState([])
const [sizes, setSizes] = useState([])
const [loading, setLoading] = useState(false)
```

**API Calls**:
- `GET /api/products/categories`: Fetch all categories
- `GET /api/products/subcategories/<category>`: Fetch subcategories for category
- `GET /api/products/sizes/<category>/<subcategory>`: Fetch sizes for category/subcategory

**Timeframe Logic**:
- **Year**: Shows only year selector
- **Quarter**: Shows year + quarter (Q1-Q4)
- **Month**: Shows year + month (01-12)
- **Week**: Shows year + month + week number

---

### DashboardChart.jsx

Component for rendering sales and forecast charts.

**Responsibilities**:
- Display historical sales data
- Show forecast predictions
- Interactive chart visualization

**Expected Features** (based on name):
- Line/area charts for time series data
- Comparison between actual and predicted values
- Responsive design

---

### MetricsPanel.jsx

Displays key performance indicators (KPIs).

**Metrics**:
- Total sales
- Predicted total sales
- Growth rates
- Trends

---

### InventoryBox.jsx

Shows current inventory status for selected product combination.

**Data Displayed**:
- Product details (category, subcategory, size)
- Current inventory level
- Stock status (high/medium/low)
- Last updated timestamp

---

### NewsPanel.jsx

Displays news, alerts, or notifications.

**Potential Features**:
- Industry news
- System alerts
- Promotional campaigns
- Important updates

---

### ChatBox.jsx

Interactive chat interface component.

**Potential Features**:
- Customer support
- AI assistant
- FAQ
- Help system

---

## Styling with TailwindCSS

### Custom Classes

The application uses TailwindCSS utility classes along with custom classes defined in `index.css`:

```css
.metric-box {
  @apply bg-white rounded-lg shadow-sm p-6 border border-gray-100;
}

.dropdown-select {
  @apply px-3 py-2 border border-gray-300 rounded-md 
         focus:ring-2 focus:ring-blue-500 focus:border-transparent;
}
```

### Responsive Design

The layout uses Tailwind's responsive prefixes:
- `md:`: Tablets and up (768px+)
- `lg:`: Desktops and up (1024px+)

Example:
```jsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  {/* Stacks on mobile, 3 columns on tablets+ */}
</div>
```

---

## State Management

### Approach

The application uses **local component state** with **prop drilling**:
- State defined in `App.jsx`
- Passed down to child components as props
- Child components call parent functions to update state

### Data Flow

```
App.jsx (state)
    ↓
ForecastControls (receives state + setters)
    ↓
User interaction
    ↓
Calls setter function
    ↓
App.jsx state updates
    ↓
useEffect triggers
    ↓
API call
    ↓
State updates with new data
    ↓
Re-render with updated data
```

### Alternative Approaches (Future)

For larger applications, consider:
- **Context API**: Avoid prop drilling
- **Redux**: Centralized state management
- **Zustand**: Lightweight state management
- **React Query**: Server state management

---

## API Integration

### Configuration

```javascript
const API_BASE = 'http://localhost:5000/api'
```

### Fetch Pattern

```javascript
fetch(`${API_BASE}/endpoint`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})
  .then(res => res.json())
  .then(data => {
    // Update state
  })
  .catch(err => console.error(err))
  .finally(() => setLoading(false))
```

### Error Handling

Current implementation:
- Logs errors to console
- No user-facing error messages
- No retry logic

Recommended improvements:
- Display error messages to users
- Implement retry logic
- Add loading skeletons
- Handle network failures gracefully

---

## Build & Development

### Development Server

```bash
npm run dev
```
- Starts Vite dev server on port 5173
- Hot module replacement (HMR)
- Fast refresh for React components

### Production Build

```bash
npm run build
```
- Creates optimized production bundle in `dist/`
- Minifies JavaScript and CSS
- Generates sourcemaps
- Tree-shaking for smaller bundle size

### Preview Production Build

```bash
npm run preview
```
- Serves production build locally
- Test before deployment

### Linting

```bash
npm run lint
```
- Runs ESLint on .js and .jsx files
- Checks for code quality issues

---

## Performance Optimizations

### Current Optimizations

1. **Vite**: Fast build times with ESBuild
2. **React 18**: Automatic batching of state updates
3. **useMemo**: Memoizes year range calculation
4. **Conditional Rendering**: Only renders relevant controls

### Recommended Optimizations

1. **Code Splitting**: Use React.lazy() for route-based splitting
2. **Memoization**: Add React.memo() to prevent unnecessary re-renders
3. **Virtual Scrolling**: For large lists/tables
4. **Debouncing**: Debounce API calls on rapid filter changes
5. **Caching**: Cache API responses with React Query or SWR

Example with React.memo():
```javascript
const ForecastControls = React.memo(({ ... }) => {
  // Component code
})
```

Example with debouncing:
```javascript
const debouncedFetch = useMemo(
  () => debounce((filters) => fetchSalesData(filters), 300),
  []
)
```

---

## Accessibility

### Current State

- Semantic HTML elements
- Form labels for screen readers
- Keyboard navigation for dropdowns

### Recommended Improvements

1. **ARIA Labels**: Add aria-labels to interactive elements
2. **Focus Management**: Keyboard navigation for all interactions
3. **Color Contrast**: Ensure WCAG AA compliance
4. **Screen Reader Testing**: Test with NVDA/JAWS
5. **Skip Links**: Add skip-to-content links

Example:
```jsx
<select
  aria-label="Select product category"
  className="dropdown-select"
>
```

---

## Testing

### Recommended Testing Strategy

1. **Unit Tests**: Jest + React Testing Library
   - Test individual components
   - Test utility functions
   - Test hooks

2. **Integration Tests**: Test component interactions
   - Test filter cascading
   - Test API integration
   - Test state updates

3. **E2E Tests**: Playwright or Cypress
   - Test complete user flows
   - Test critical paths

Example test:
```javascript
import { render, screen, fireEvent } from '@testing-library/react'
import ForecastControls from './ForecastControls'

test('renders category dropdown', () => {
  render(<ForecastControls {...props} />)
  expect(screen.getByText('Category')).toBeInTheDocument()
})
```

---

## Environment Configuration

### Development

Create `.env.development`:
```env
VITE_API_BASE_URL=http://localhost:5000
```

### Production

Create `.env.production`:
```env
VITE_API_BASE_URL=https://api.ennovar.com
```

### Usage

```javascript
const API_BASE = import.meta.env.VITE_API_BASE_URL
```

---

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Static Hosting

The `dist/` folder can be deployed to:
- **Netlify**: Drag & drop or Git integration
- **Vercel**: Automatic deployments from Git
- **AWS S3 + CloudFront**: Static hosting with CDN
- **GitHub Pages**: Free hosting for public repos
- **Nginx**: Serve static files

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name ennovar.com;
    
    root /var/www/ennovar/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

---

## Common Issues & Solutions

### Issue: API calls fail with CORS error

**Solution**: Ensure Flask backend has CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

### Issue: Build fails with module errors

**Solution**: Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: Hot reload not working

**Solution**: Check Vite config and ensure file watching is enabled

### Issue: Styles not applying

**Solution**: Verify Tailwind config includes all content paths:
```javascript
content: [
  "./index.html",
  "./src/**/*.{js,jsx}"
]
```

---

## Future Enhancements

1. **Authentication**: Add user login/logout
2. **Dark Mode**: Toggle between light/dark themes
3. **Export Data**: Download reports as CSV/PDF
4. **Real-time Updates**: WebSocket for live data
5. **Mobile App**: React Native version
6. **Offline Support**: Service workers for offline functionality
7. **Internationalization**: Multi-language support (i18n)
8. **Advanced Charts**: More visualization types
9. **User Preferences**: Save filter preferences
10. **Notifications**: Push notifications for alerts

---

## Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [TailwindCSS Documentation](https://tailwindcss.com)
- [React Hooks Reference](https://react.dev/reference/react)
