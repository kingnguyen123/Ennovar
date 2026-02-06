import React from 'react'

export default function MetricsPanel({ totalSales, predictedTotalSales }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 px-6 py-6">
      <div className="metric-box">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-600 text-sm font-medium">Total Sales</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">${totalSales.toLocaleString()}</p>
          </div>
          <div className="text-4xl text-blue-100"></div>
        </div>
        <div className="mt-4 text-xs text-gray-500">Last 30 days</div>
      </div>

      <div className="metric-box">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-600 text-sm font-medium">Predicted Total Sales</p>
            <p className="text-3xl font-bold text-green-600 mt-2">${predictedTotalSales.toLocaleString()}</p>
          </div>
          <div className="text-4xl text-green-100"></div>
        </div>
        <div className="mt-4 text-xs text-gray-500">Based on current trend</div>
      </div>
    </div>
  )
}
