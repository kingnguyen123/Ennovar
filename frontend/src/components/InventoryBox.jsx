import React from 'react'

export default function InventoryBox({ itemName, currentInventory }) {
  const inventoryStatus = currentInventory > 100 ? 'high' : currentInventory > 30 ? 'medium' : 'low'
  const statusColor = {
    high: 'text-green-600',
    medium: 'text-yellow-600',
    low: 'text-red-600'
  }
  const statusBg = {
    high: 'bg-green-50',
    medium: 'bg-yellow-50',
    low: 'bg-red-50'
  }

  return (
    <div className={`metric-box ${statusBg[inventoryStatus]}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">Current Inventory</p>
          <p className="text-2xl font-semibold text-gray-900 mt-2">{itemName}</p>
          <p className={`text-2xl font-bold mt-2 ${statusColor[inventoryStatus]}`}>
            {currentInventory} units
          </p>
        </div>
        <div className="text-4xl"></div>
      </div>
      <div className="mt-4 flex items-center justify-between">
        <span className={`text-xs font-semibold px-3 py-1 rounded-full ${statusColor[inventoryStatus]}`}>
          {inventoryStatus.charAt(0).toUpperCase() + inventoryStatus.slice(1)} Stock
        </span>
        <span className="text-xs text-gray-500">Last updated: today</span>
      </div>
    </div>
  )
}
