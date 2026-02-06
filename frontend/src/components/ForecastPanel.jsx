import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ForecastPanel = () => {
  const [categories, setCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedProduct, setSelectedProduct] = useState('');
  const [horizon, setHorizon] = useState(7);
  const [loading, setLoading] = useState(false);
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState('');
  const [modelStatus, setModelStatus] = useState(null);

  // Load categories on mount
  useEffect(() => {
    fetchCategories();
    checkModelStatus();
  }, []);

  // Load products when category changes
  useEffect(() => {
    if (selectedCategory) {
      fetchProducts(selectedCategory);
    } else {
      setProducts([]);
      setSelectedProduct('');
    }
  }, [selectedCategory]);

  const checkModelStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/forecast/status');
      const data = await response.json();
      setModelStatus(data);
    } catch (err) {
      console.error('Error checking model status:', err);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/products/categories');
      const data = await response.json();
      setCategories(data);
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  };

  const fetchProducts = async (category) => {
    try {
      const response = await fetch(`http://localhost:5000/api/products/products/${encodeURIComponent(category)}`);
      const data = await response.json();
      setProducts(data);
    } catch (err) {
      console.error('Error fetching products:', err);
    }
  };

  const generateForecast = async () => {
    if (!selectedCategory) {
      setError('Please select a category');
      return;
    }

    setLoading(true);
    setError('');
    setForecast(null);

    try {
      const response = await fetch('http://localhost:5000/api/forecast/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          category: selectedCategory,
          product: selectedProduct || null,
          horizon: horizon
        })
      });

      const data = await response.json();

      if (data.success) {
        setForecast(data);
      } else {
        setError(data.error || 'Failed to generate forecast');
      }
    } catch (err) {
      setError('Error generating forecast: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatChartData = () => {
    if (!forecast || !forecast.forecast) return [];
    
    return forecast.forecast.map(item => ({
      date: new Date(item.date).toLocaleDateString(),
      actual: item.actual_quantity,
      predicted: item.predicted_quantity
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">📊 Demand Forecast</h2>
        {modelStatus && modelStatus.status === 'available' && (
          <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
            ✓ Model Ready
          </span>
        )}
      </div>

      {/* Selection Controls */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Category Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Category *
          </label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select Category</option>
            {categories.map((cat, idx) => (
              <option key={idx} value={cat.category_name}>
                {cat.category_name}
              </option>
            ))}
          </select>
        </div>

        {/* Product Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Product (Optional)
          </label>
          <select
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
            disabled={!selectedCategory}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          >
            <option value="">All Products</option>
            {products.map((prod, idx) => (
              <option key={idx} value={prod.product_name}>
                {prod.product_name}
              </option>
            ))}
          </select>
        </div>

        {/* Horizon Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Forecast Horizon
          </label>
          <select
            value={horizon}
            onChange={(e) => setHorizon(parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value={7}>7 Days (1 Week)</option>
            <option value={14}>14 Days (2 Weeks)</option>
            <option value={30}>30 Days (1 Month)</option>
          </select>
        </div>
      </div>

      {/* Generate Button */}
      <button
        onClick={generateForecast}
        disabled={loading || !selectedCategory}
        className="w-full md:w-auto px-6 py-3 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generating Forecast...
          </span>
        ) : (
          '🔮 Generate Forecast'
        )}
      </button>

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      {/* Forecast Results */}
      {forecast && (
        <div className="mt-6 space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-sm text-blue-600 font-medium">Total Predicted</p>
              <p className="text-2xl font-bold text-blue-900">
                {forecast.summary.total_predicted?.toFixed(0)}
              </p>
            </div>
            
            {forecast.summary.total_actual !== undefined && (
              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-sm text-green-600 font-medium">Total Actual</p>
                <p className="text-2xl font-bold text-green-900">
                  {forecast.summary.total_actual?.toFixed(0)}
                </p>
              </div>
            )}
          </div>

          {/* Forecast Info */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Category:</span>
                <span className="ml-2 font-medium">{forecast.category}</span>
              </div>
              <div>
                <span className="text-gray-600">Product:</span>
                <span className="ml-2 font-medium">{forecast.product || 'All'}</span>
              </div>
              <div>
                <span className="text-gray-600">Horizon:</span>
                <span className="ml-2 font-medium">{forecast.horizon} days</span>
              </div>
              <div>
                <span className="text-gray-600">Predictions:</span>
                <span className="ml-2 font-medium">{forecast.forecast.length}</span>
              </div>
            </div>
          </div>

          {/* Chart */}
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Forecast Visualization
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={formatChartData()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tick={{ fontSize: 12 }}
                  angle={-45}
                  textAnchor="end"
                  height={80}
                />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="actual" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  name="Actual Demand"
                  dot={{ r: 4 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="predicted" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  name="Predicted Demand"
                  dot={{ r: 4 }}
                  strokeDasharray="5 5"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Data Table */}
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto max-h-96">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50 sticky top-0">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actual</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Predicted</th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Difference</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {forecast.forecast.map((item, idx) => {
                    const diff = item.actual_quantity !== null 
                      ? item.predicted_quantity - item.actual_quantity 
                      : null;
                    return (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-4 py-2 text-sm text-gray-900">{item.date}</td>
                        <td className="px-4 py-2 text-sm text-gray-600">{item.product_name || '-'}</td>
                        <td className="px-4 py-2 text-sm text-right font-medium">
                          {item.actual_quantity !== null ? item.actual_quantity.toFixed(0) : '-'}
                        </td>
                        <td className="px-4 py-2 text-sm text-right font-medium text-blue-600">
                          {item.predicted_quantity.toFixed(0)}
                        </td>
                        <td className={`px-4 py-2 text-sm text-right font-medium ${
                          diff === null ? '' : diff > 0 ? 'text-red-600' : 'text-green-600'
                        }`}>
                          {diff !== null ? (diff > 0 ? '+' : '') + diff.toFixed(0) : '-'}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Model Status Footer */}
      {modelStatus && modelStatus.status === 'available' && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            Model: {modelStatus.model_type} | Trained: {new Date(modelStatus.trained_at).toLocaleDateString()}
          </p>
        </div>
      )}
    </div>
  );
};

export default ForecastPanel;
