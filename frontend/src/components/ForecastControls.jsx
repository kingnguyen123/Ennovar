import React, { useState, useEffect, useMemo } from 'react'

export default function ForecastControls({
  timeframeType,
  year,
  month,
  quarter,
  week,
  category,
  product,
  onTimeframeTypeChange,
  onYearChange,
  onMonthChange,
  onQuarterChange,
  onWeekChange,
  onCategoryChange,
  onProductChange,
  yearRange
}) {
  const timeframeTypes = ['Year', 'Quarter', 'Month', 'Week']
  const years = useMemo(() => {
    const minYear = yearRange?.min_year || 2024
    const maxYear = yearRange?.max_year || 2024
    return Array.from(
      { length: maxYear - minYear + 1 },
      (_, i) => (maxYear - i).toString()
    )
  }, [yearRange])
  const months = Array.from({ length: 12 }, (_, i) => ((i + 1).toString().padStart(2, '0')))
  const quarters = ['Q1', 'Q2', 'Q3', 'Q4']
  const [categories, setCategories] = useState([])
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(false)
  const API_BASE = 'http://localhost:5000/api/products'

  // Calculate weeks in selected month
  const getWeeksInMonth = (yearVal, monthVal) => {
    const firstDay = new Date(parseInt(yearVal), parseInt(monthVal) - 1, 1)
    const lastDay = new Date(parseInt(yearVal), parseInt(monthVal), 0)
    const weeksInMonth = Math.ceil((lastDay.getDate() + firstDay.getDay()) / 7)
    return Array.from({ length: weeksInMonth }, (_, i) => (i + 1).toString())
  }

  // Fetch categories
  useEffect(() => {
    setLoading(true)
    fetch(`${API_BASE}/categories`)
      .then(res => res.json())
      .then(data => {
        setCategories(data.map(item => item.category_name))
      })
      .catch(err => console.error('Error fetching categories:', err))
      .finally(() => setLoading(false))
  }, [])

  // Fetch products when category changes
  useEffect(() => {
    if (category) {
      fetch(`${API_BASE}/products/${category}`)
        .then(res => res.json())
        .then(data => {
          setProducts(data.map(item => item.product_name))
        })
        .catch(err => console.error('Error fetching products:', err))
    } else {
      setProducts([])
    }
  }, [category])

  return (
    <div className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10 overflow-x-auto">
      <div className="px-6 py-4 flex flex-col md:flex-row gap-3 items-start md:items-center min-w-min">
        {/* Timeframe Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Timeframe Type</label>
          <select
            value={timeframeType}
            onChange={(e) => onTimeframeTypeChange(e.target.value)}
            className="dropdown-select w-full md:w-36"
          >
            {timeframeTypes.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        {/* Year */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Year</label>
          <select
            value={year}
            onChange={(e) => onYearChange(e.target.value)}
            className="dropdown-select w-full md:w-32"
          >
            {years.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </div>

        {/* Quarter - Show only if timeframe is Quarter */}
        {timeframeType === 'Quarter' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Quarter</label>
            <select
              value={quarter}
              onChange={(e) => onQuarterChange(e.target.value)}
              className="dropdown-select w-full md:w-32"
            >
              {quarters.map((q) => (
                <option key={q} value={q}>
                  {q}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Month - Show only if timeframe is Month */}
        {timeframeType === 'Month' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Month</label>
            <input
              type="text"
              value={month}
              onChange={(e) => {
                const val = e.target.value
                if (val === '') {
                  onMonthChange('1')
                } else if (/^\d+$/.test(val) && parseInt(val) >= 1 && parseInt(val) <= 12) {
                  onMonthChange(val)
                }
              }}
              className="dropdown-select w-full md:w-24 text-center"
              placeholder="1-12"
            />
          </div>
        )}

        {/* Week - Show if timeframe is Week */}
        {timeframeType === 'Week' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Week of Year</label>
            <input
              type="text"
              value={week}
              onChange={(e) => {
                const val = e.target.value
                if (val === '') {
                  onWeekChange('1')
                } else if (/^\d+$/.test(val) && parseInt(val) >= 1 && parseInt(val) <= 52) {
                  onWeekChange(val)
                }
              }}
              className="dropdown-select w-full md:w-24 text-center"
              placeholder="1-52"
            />
          </div>
        )}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
          <select
            value={category}
            onChange={(e) => onCategoryChange(e.target.value)}
            className="dropdown-select w-full md:w-44"
            disabled={loading || categories.length === 0}
          >
            <option value="">
              {loading ? 'Loading...' : 'Select a category'}
            </option>
            {categories.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Product</label>
          <select
            value={product}
            onChange={(e) => onProductChange(e.target.value)}
            className="dropdown-select w-full md:w-44"
            disabled={!category || products.length === 0}
          >
            <option value="">Select a product</option>
            {!category ? (
              <option disabled>Select category first</option>
            ) : null}
            {products.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  )
}