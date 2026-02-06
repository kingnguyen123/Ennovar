import React from 'react'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function DashboardChart({ salesPatternData, loading, timeRange }) {
  const hasData = salesPatternData && salesPatternData.length > 0

  // Custom tooltip for better data display
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900">{label}</p>
          <p className="text-sm text-blue-600">
            Sales: ${payload[0].value.toLocaleString()}
          </p>
          {payload[1] && (
            <p className="text-sm text-green-600">
              Quantity: {payload[1].value}
            </p>
          )}
        </div>
      )
    }
    return null
  }

  return (
    <div className="chart-container h-96">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900">Sales Pattern</h2>
          <p className="text-sm text-gray-600 mt-1">
            {hasData ? `Sales trend for selected item (${timeRange})` : 'Select an item to view sales pattern'}
          </p>
        </div>
      </div>

      {loading ? (
        <div className="w-full h-80 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <div className="text-4xl mb-4">⏳</div>
            <p className="text-gray-600 font-medium">Loading sales data...</p>
          </div>
        </div>
      ) : hasData ? (
        <ResponsiveContainer width="100%" height={320}>
          <AreaChart
            data={salesPatternData}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis 
              dataKey="sale_date" 
              tick={{ fill: '#6B7280', fontSize: 12 }}
              stroke="#9CA3AF"
            />
            <YAxis 
              tick={{ fill: '#6B7280', fontSize: 12 }}
              stroke="#9CA3AF"
              tickFormatter={(value) => `$${value.toLocaleString()}`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              wrapperStyle={{ paddingTop: '20px' }}
              iconType="line"
            />
            <Area
              type="monotone"
              dataKey="total_sales"
              name="Total Sales"
              stroke="#3B82F6"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorSales)"
            />
          </AreaChart>
        </ResponsiveContainer>
      ) : (
        <div className="w-full h-80 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <div className="text-5xl mb-4"></div>
            <p className="text-gray-600 font-medium">No Sales Data Available</p>
            <p className="text-gray-500 text-sm mt-2">
              Select category, product, and time range to view sales patterns
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
