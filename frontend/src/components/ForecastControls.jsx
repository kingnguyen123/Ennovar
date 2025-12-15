import React, { useState, useEffect } from 'react'

export default function ForecastControls({
  forecastRange,
  category,
  subCategory,
  size,
  onForecastChange,
  onCategoryChange,
  onSubCategoryChange,
  onSizeChange
}) {
  const forecastOptions = ['Predicting 1 Week', 'Predicting 1 Month','Predicting 1 Quarter']
  const [categories, setCategories] = useState([])
  const [subCategories, setSubCategories] = useState([])
  const [sizes, setSizes] = useState([])
  const [loading, setLoading] = useState(false)
  const API_BASE = 'http://localhost:5000/api/products'

  // // Fetch categories
  // useEffect(() => {
  //   setLoading(true)
  //   fetch(`${API_BASE}/categories`)
  //     .then(res => res.json())
  //     .then(data => {
  //       if (data.status === 'Success') {
  //         setCategories(data.data.categories)
  //       }
  //     })
  //     .catch(err => console.error('Error fetching categories:', err))
  //     .finally(() => setLoading(false))
  // }, [])

  // // Fetch subcategories when category changes
  // useEffect(() => {
  //   if (category) {
  //     fetch(`${API_BASE}/subcategories-filtered?category=${category}`)
  //       .then(res => res.json())
  //       .then(data => {
  //         if (data.status === 'Success') {
  //           setSubCategories(data.data.sub_category)
  //         }
  //       })
  //       .catch(err => console.error('Error fetching subcategories:', err))
  //   } else {
  //     setSubCategories([])
  //   }
  // }, [category])
  //
  // // Fetch sizes when category/subcategory changes
  // useEffect(() => {
  //   if (category && subCategory) {
  //     fetch(`${API_BASE}/sizes-filtered?category=${category}&sub_category=${subCategory}`)
  //       .then(res => res.json())
  //       .then(data => {
  //         if (data.status === 'Success') {
  //           setSizes(data.data.sizes)
  //         }
  //       })
  //       .catch(err => console.error('Error fetching sizes:', err))
  //   } else {
  //     setSizes([])
  //   }
  // }, [category, subCategory])

  return (
    <div className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
      <div className="px-6 py-4 flex flex-col md:flex-row gap-4 items-start md:items-center">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">Forecast Range</label>
          <select
            value={forecastRange}
            onChange={(e) => onForecastChange(e.target.value)}
            className="dropdown-select w-full md:w-64"
          >
            {forecastOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
          <select
            value={category}
            onChange={(e) => onCategoryChange(e.target.value)}
            className="dropdown-select w-full md:w-64"
            disabled={loading || categories.length === 0}
          >
            {categories.length === 0 && <option value="">Loading...</option>}
            {categories.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">Sub Category</label>
          <select
            value={subCategory}
            onChange={(e) => onSubCategoryChange(e.target.value)}
            className="dropdown-select w-full md:w-64"
            disabled={!category || subCategories.length === 0}
          >
            {subCategories.length === 0 && <option value="">Select category first</option>}
            {subCategories.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">Size</label>
          <select
            value={size}
            onChange={(e) => onSizeChange(e.target.value)}
            className="dropdown-select w-full md:w-64"
            disabled={!subCategory || sizes.length === 0}
          >
            {sizes.length === 0 && <option value="">Select subcategory first</option>}
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