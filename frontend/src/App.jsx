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
  const [category, setCategory] = useState('Apparel')
  const [subCategory, setSubCategory] = useState('Shirts')
  const [size, setSize] = useState('M')
  const [salesData, setSalesData] = useState({
    totalSales: 0,
    predictedTotalSales: 140750,
    currentInventory: 234,
  })
  const [loading, setLoading] = useState(false)

  // Fetch sales data when filters change
  const API_BASE = 'http://localhost:5000/api/products'
  
  useEffect(() => {
    if (category && subCategory && size) {
      setLoading(true)
      // Get last 30 days date range
      const endDate = new Date().toISOString().split('T')[0]
      const startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]

      fetch(`${API_BASE}/sales/subcategory-by-category-size`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sub_category: subCategory,
          size: size,
          start_date: startDate,
          end_date: endDate
        })
      })
        .then(res => res.json())
        .then(data => {
          const total = data.reduce((sum, item) => sum + (item.total_sales || 0), 0)
          setSalesData(prev => ({
            ...prev,
            totalSales: total
          }))
        })
        .catch(err => console.error('Error fetching sales:', err))
        .finally(() => setLoading(false))
    }
  }, [category, subCategory, size])

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
        size={size}
        onTimeframeTypeChange={setTimeframeType}
        onYearChange={setYear}
        onMonthChange={setMonth}
        onQuarterChange={setQuarter}
        onWeekChange={setWeek}
        onCategoryChange={setCategory}
        onSubCategoryChange={setSubCategory}
        onSizeChange={setSize}
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
                    <p className="text-2xl font-semibold text-gray-900 mt-2">{category} - {subCategory} ({size})</p>
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
            <DashboardChart />
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
