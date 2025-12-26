import { useState, useEffect } from 'react'
import ForecastControls from './components/ForecastControls'
import MetricsPanel from './components/MetricsPanel'
import InventoryBox from './components/InventoryBox'
import DashboardChart from './components/DashboardChart'
import NewsPanel from './components/NewsPanel'
import ChatBox from './components/ChatBox'

export default function App() {
  const [timeframeType, setTimeframeType] = useState('Month')
  const [year, setYear] = useState(new Date().getFullYear().toString())
  const [month, setMonth] = useState((new Date().getMonth() + 1).toString())
  const [quarter, setQuarter] = useState('Q1')
  const [week, setWeek] = useState('1')
  const [category, setCategory] = useState('0')
  const [subCategory, setSubCategory] = useState('0')
  const [Size, setSize] = useState('0')
  const [salesData, setSalesData] = useState({
    totalSales: 0,
    predictedTotalSales: 0,
    currentInventory: 0,
  })
  const [salesPatternData, setSalesPatternData] = useState([])
  const [loading, setLoading] = useState(false)
  const [chartLoading, setChartLoading] = useState(false)
  const [yearRange, setYearRange] = useState({ min_year: 2024, max_year: 2024 })

  // Fetch year range from database on component mount
  useEffect(() => {
    console.log('[App] Fetching year range from API...')
    fetch('http://localhost:5000/api/sales/year-range')
      .then(res => res.json())
      .then(data => {
        console.log('[App] Year range fetched:', data)
        setYearRange(data)
        setYear(data.max_year.toString())
      })
      .catch(err => console.error('[App ERROR] Error fetching year range:', err))
  }, [])

  // Calculate date range based on timeframe
  const getDateRangeFromTimeframe = () => {
    const yearNum = parseInt(year)
    let startDate, endDate
    
    switch (timeframeType) {
      case 'Year':
        startDate = new Date(yearNum, 0, 1)
        endDate = new Date(yearNum, 11, 31)
        break
      
      case 'Quarter': {
        const quarterNum = parseInt(quarter.replace('Q', ''))
        startDate = new Date(yearNum, (quarterNum - 1) * 3, 1)
        endDate = new Date(yearNum, quarterNum * 3, 0)
        break
      }
      
      case 'Month': {
        const monthNum = parseInt(month)
        startDate = new Date(yearNum, monthNum - 1, 1)
        endDate = new Date(yearNum, monthNum, 0)
        break
      }
      
      case 'Week': {
        const weekNum = parseInt(week)
        // Calculate the start of the year
        const firstDayOfYear = new Date(yearNum, 0, 1)
        const dayOfWeek = firstDayOfYear.getDay()
        
        // Calculate the start of week 1 (first Monday of the year)
        const firstWeekStart = new Date(firstDayOfYear)
        const daysToMonday = dayOfWeek === 0 ? 1 : (8 - dayOfWeek) % 7
        firstWeekStart.setDate(firstDayOfYear.getDate() + daysToMonday)
        
        // Calculate start and end of selected week
        startDate = new Date(firstWeekStart)
        startDate.setDate(firstWeekStart.getDate() + (weekNum - 1) * 7)
        
        endDate = new Date(startDate)
        endDate.setDate(startDate.getDate() + 6)
        break
      }
      
      default:
        // Default to last 30 days
        endDate = new Date()
        startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
    }
    
    return {
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0]
    }
  }

  // Fetch sales data when filters change
  const API_BASE = 'http://localhost:5000/api/sales'
  
  useEffect(() => {
    // Only fetch if at least category and subCategory are selected
    if (!category || !subCategory) {
      setSalesData(prev => ({
        ...prev,
        totalSales: 0
      }))
      return
    }

    setLoading(true)
    const { startDate, endDate } = getDateRangeFromTimeframe()
    console.log('[App] Filters changed:', { category, subCategory, Size, timeframeType, year, month, quarter, week })
    console.log('[App] Date range:', { startDate, endDate })

    // Single endpoint handles both with and without size
    const requestBody = {
      category: category,
      sub_category: subCategory,
      size: Size || '',
      start_date: startDate,
      end_date: endDate
    }
    console.log('[App] Fetching sales data...')

    // Old logic - removed (endpoint now handles both cases):
    // let endpoint, requestBody
    // if (Size) {
    //   endpoint = `${API_BASE}/subcategory-by-category-size`
    //   requestBody = { category, sub_category: subCategory, size: Size, start_date: startDate, end_date: endDate }
    // } else {
    //   endpoint = `${API_BASE}/subcategory-by-category`
    //   requestBody = { category, sub_category: subCategory, start_date: startDate, end_date: endDate }
    // }

    fetch(`${API_BASE}/subcategory-by-category-size`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    })
      .then(res => {
        console.log('[App] API response status:', res.status)
        return res.json()
      })
      .then(data => {
        console.log('[App] Sales data received:', data)
        if (!data || data.length === 0) {
          console.warn('[App WARNING] No sales data returned')
          setSalesData(prev => ({
            ...prev,
            totalSales: 0
          }))
          return
        }
        const total = data[0]?.total_sales ?? 0
        console.log('[App] Calculated total sales:', total)
        setSalesData(prev => ({
          ...prev,
          totalSales: total
          }))
        })
        .catch(err => {
          console.error('[App ERROR] Error fetching sales:', err)
          setSalesData(prev => ({
            ...prev,
            totalSales: 0
          }))
        })
        .finally(() => {
          console.log('[App] Loading complete')
          setLoading(false)
        })
  }, [category, subCategory, Size, timeframeType, year, month, quarter, week])

  // Fetch sales pattern data for chart
  useEffect(() => {
    if (!category || !subCategory) {
      setSalesPatternData([])
      return
    }

    setChartLoading(true)
    const { startDate, endDate } = getDateRangeFromTimeframe()
    console.log('[App] Fetching sales pattern data...')

    fetch('http://localhost:5000/api/sales/sales-pattern', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        category: category,
        sub_category: subCategory,
        size: Size || '',
        start_date: startDate,
        end_date: endDate
      })
    })
      .then(res => res.json())
      .then(data => {
        console.log('[App] Sales pattern data received:', data)
        setSalesPatternData(data)
      })
      .catch(err => {
        console.error('[App ERROR] Error fetching sales pattern:', err)
        setSalesPatternData([])
      })
      .finally(() => {
        setChartLoading(false)
      })
  }, [category, subCategory, Size, timeframeType, year, month, quarter, week])

  // Fetch inventory data separately (no time range needed)
  useEffect(() => {
    if (!category || !subCategory) {
      setSalesData(prev => ({
        ...prev,
        currentInventory: 0
      }))
      return
    }

    console.log('[App] Fetching inventory data...')
    fetch('http://localhost:5000/api/inventory/subcategory-by-category-size', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        category: category,
        sub_category: subCategory,
        size: Size || ''
      })
    })
      .then(res => res.json())
      .then(data => {
        console.log('[App] Inventory data received:', data)
        const inventory = data[0]?.['Current Inventory'] ?? 0
        console.log('[App] Current inventory:', inventory)
        setSalesData(prev => ({
          ...prev,
          currentInventory: inventory
        }))
      })
      .catch(err => {
        console.error('[App ERROR] Error fetching inventory:', err)
        setSalesData(prev => ({
          ...prev,
          currentInventory: 0
        }))
      })
  }, [category, subCategory, Size])

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Top Control Bar */}
      <ForecastControls
        timeframeType={timeframeType}
        year={year}
        month={month}
        quarter={quarter}
        week={week}
        category={category}
        subCategory={subCategory}
        size={Size}
        onTimeframeTypeChange={setTimeframeType}
        onYearChange={setYear}
        onMonthChange={setMonth}
        onQuarterChange={setQuarter}
        onWeekChange={setWeek}
        onCategoryChange={setCategory}
        onSubCategoryChange={setSubCategory}
        onSizeChange={setSize}
        yearRange={yearRange}
      />

      {/* Main Content */}
      <div className="flex-1 overflow-auto flex flex-col lg:flex-row">
        {/* Left and Center Content */}
        <div className="flex-1 flex flex-col overflow-auto">
          {/* Metrics Section */}
          <div className="px-6 pt-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Dashboard Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Metrics Cards */}
              <div className="metric-box">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium">Total Sales</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">
                      ${salesData.totalSales.toLocaleString()}
                    </p>
                  </div>
                  <div className="text-4xl text-blue-100">📊</div>
                </div>
                <div className="mt-4 text-xs text-gray-500">
                  {loading ? 'Loading...' : 'Last 30 days'}
                </div>
              </div>

              <div className="metric-box">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium">Predicted Total Sales</p>
                    <p className="text-3xl font-bold text-green-600 mt-2">
                      ${salesData.predictedTotalSales.toLocaleString()}
                    </p>
                  </div>
                  <div className="text-4xl text-green-100">🎯</div>
                </div>
                <div className="mt-4 text-xs text-gray-500">Based on current trend</div>
              </div>

              {/* Current Inventory Box */}
              <div className="metric-box">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium">Current Inventory</p>
                    <p className="text-2xl font-semibold text-gray-900 mt-2">{category} - {subCategory} ({Size})</p>
                    <p className="text-3xl font-bold text-green-600 mt-2">
                      {salesData.currentInventory} units
                    </p>
                  </div>
                  <div className="text-4xl">📦</div>
                </div>
                <div className="mt-4 flex items-center justify-between">
                  <span className="text-xs font-semibold px-3 py-1 rounded-full text-green-600">
                    High Stock
                  </span>
                  <span className="text-xs text-gray-500">Last updated: today</span>
                </div>
              </div>
            </div>
          </div>

          {/* Chart Section */}
          <div className="px-6 py-6 flex-1">
            <DashboardChart 
              salesPatternData={salesPatternData}
              loading={chartLoading}
              timeRange={`${timeframeType}: ${timeframeType === 'Year' ? year : timeframeType === 'Quarter' ? `${year} ${quarter}` : timeframeType === 'Week' ? `${year} Week ${week}` : `${year}-${month}`}`}
            />
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="w-full lg:w-80 border-l border-gray-200 flex flex-col divide-y divide-gray-200 bg-white">
          {/* News Panel */}
          <div className="flex-1 min-h-96 overflow-hidden">
            <NewsPanel />
          </div>

          {/* Chat Box */}
          <div className="flex-1 min-h-96 overflow-hidden">
            <ChatBox />
          </div>
        </div>
      </div>
    </div>
  )
}
