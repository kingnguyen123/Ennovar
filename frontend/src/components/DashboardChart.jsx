import React from 'react'

export default function DashboardChart() {
  return (
    <div className="chart-container h-96">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900">Sales Forecast</h2>
          <p className="text-sm text-gray-600 mt-1">Visual representation of forecasted sales trend</p>
        </div>
        <div className="flex gap-2">
          <button className="button-secondary text-sm">1D</button>
          <button className="button-secondary text-sm">1W</button>
          <button className="button-primary text-sm">1M</button>
        </div>
      </div>

      <div className="w-full h-80 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-dashed border-gray-300 flex items-center justify-center">
        <div className="text-center">
          <div className="text-5xl mb-4">📈</div>
          <p className="text-gray-600 font-medium">Chart Placeholder</p>
          <p className="text-gray-500 text-sm mt-2">Connect to backend data source to display forecasts</p>
          <div className="mt-6 text-xs text-gray-400">
            <p>Ready for chart library integration (Chart.js, Recharts, etc.)</p>
          </div>
        </div>
      </div>
    </div>
  )
}
