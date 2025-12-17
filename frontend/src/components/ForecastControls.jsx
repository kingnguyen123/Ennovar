import React, { useState, useEffect } from 'react'

export default function ForecastControls({
  timeframeType,
  year,
  month,
  quarter,
  week,
  category,
  subCategory,
  size,
  onTimeframeTypeChange,
  onYearChange,
  onMonthChange,
  onQuarterChange,
  onWeekChange,
  onCategoryChange,
  onSubCategoryChange,
  onSizeChange
}) {
  const timeframeTypes = ['Year', 'Quarter', 'Month', 'Week']
  const years = Array.from({ length: 5 }, (_, i) => (new Date().getFullYear() - i).toString())
  const months = Array.from({ length: 12 }, (_, i) => ((i + 1).toString().padStart(2, '0')))
  const quarters = ['Q1', 'Q2', 'Q3', 'Q4']
  const [categories, setCategories] = useState([])
  const [subCategories, setSubCategories] = useState([])
  const [sizes, setSizes] = useState([])
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
        setCategories(data.map(item => item.category))
      })
      .catch(err => console.error('Error fetching categories:', err))
      .finally(() => setLoading(false))
  }, [])

  // Fetch subcategories when category changes
  useEffect(() => {
    if (category) {
      fetch(`${API_BASE}/subcategories/${category}`)
        .then(res => res.json())
        .then(data => {
          setSubCategories(data.map(item => item.sub_category))
        })
        .catch(err => console.error('Error fetching subcategories:', err))
    } else {
      setSubCategories([])
    }
  }, [category])

  // Fetch sizes when category/subcategory changes
  useEffect(() => {
    if (category && subCategory) {
      fetch(`${API_BASE}/sizes/${category}/${subCategory}`)
        .then(res => res.json())
        .then(data => {
          setSizes(data.map(item => item.Size))
        })
        .catch(err => console.error('Error fetching sizes:', err))
    } else {
      setSizes([])
    }
  }, [category, subCategory])

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

        {/* Quarter - Show if timeframe is Quarter or Month or Week */}
        {(timeframeType === 'Quarter' || timeframeType === 'Month' || timeframeType === 'Week') && (
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

        {/* Month - Show if timeframe is Month or Week */}
        {(timeframeType === 'Month' || timeframeType === 'Week') && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Month</label>
            <select
              value={month}
              onChange={(e) => onMonthChange(e.target.value)}
              className="dropdown-select w-full md:w-32"
            >
              {months.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Week - Show if timeframe is Week */}
        {timeframeType === 'Week' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Week</label>
            <select
              value={week}
              onChange={(e) => onWeekChange(e.target.value)}
              className="dropdown-select w-full md:w-32"
            >
              {getWeeksInMonth(year, month).map((w) => (
                <option key={w} value={w}>
                  Week {w}
                </option>
              ))}
            </select>
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
            <option value="" >
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
          <label className="block text-sm font-medium text-gray-700 mb-2">Sub Category</label>
          <select
            value={subCategory}
            onChange={(e) => onSubCategoryChange(e.target.value)}
            className="dropdown-select w-full md:w-44"
            disabled={!category || subCategories.length === 0}
          >
            <option value="" >
              {!category ? 'Select category first' : 'Select a sub category'}
            </option>
            {subCategories.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Size</label>
          <select
            value={size}
            onChange={(e) => onSizeChange(e.target.value)}
            className="dropdown-select w-full md:w-44"
            disabled={!subCategory || sizes.length === 0}
          >
            <option value="" >
              {!subCategory ? 'Select subcategory first' : 'Select a size'}
            </option>
            {sizes.map((option) => (
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