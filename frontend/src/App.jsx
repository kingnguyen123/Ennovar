import { useState } from 'react'
import ForecastControls from './components/ForecastControls'
import MetricsPanel from './components/MetricsPanel'
import InventoryBox from './components/InventoryBox'
import DashboardChart from './components/DashboardChart'
import NewsPanel from './components/NewsPanel'
import ChatBox from './components/ChatBox'

export default function App() {
  const [forecastRange, setForecastRange] = useState('Predicting 1 Week')
  const [category, setCategory] = useState('Apparel')
  const [subCategory, setSubCategory] = useState('Shirts')
  const [size, setSize] = useState('M')

  // Mock data - Replace with real backend data
  const mockData = {
    totalSales: 125500,
    predictedTotalSales: 140750,
    currentInventory: 234,
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Top Control Bar */}
      <ForecastControls
        forecastRange={forecastRange}
        category={category}
        subCategory={subCategory}
        size={size}
        onForecastChange={setForecastRange}
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
                      ${mockData.totalSales.toLocaleString()}
                    </p>
                  </div>
                  <div className="text-4xl text-blue-100">📊</div>
                </div>
                <div className="mt-4 text-xs text-gray-500">Last 30 days</div>
              </div>

              <div className="metric-box">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium">Predicted Total Sales</p>
                    <p className="text-3xl font-bold text-green-600 mt-2">
                      ${mockData.predictedTotalSales.toLocaleString()}
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
                      {mockData.currentInventory} units
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
