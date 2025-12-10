import React from 'react'

export default function NewsPanel() {
  const articles = [
    { id: 1, title: 'Market Trends Q4 2025', date: '2 hours ago', category: 'Market' },
    { id: 2, title: 'Supply Chain Updates', date: '5 hours ago', category: 'Supply' },
    { id: 3, title: 'Consumer Behavior Shift', date: '1 day ago', category: 'Consumer' },
    { id: 4, title: 'New Retail Regulations', date: '2 days ago', category: 'Regulations' },
  ]

  return (
    <div className="sidebar-panel">
      <div className="border-b border-gray-200 p-4">
        <h3 className="text-lg font-bold text-gray-900">📰 News & Updates</h3>
      </div>

      <div className="flex-1 overflow-y-auto">
        {articles.map((article) => (
          <div key={article.id} className="border-b border-gray-100 p-4 hover:bg-gray-50 cursor-pointer transition-colors">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="font-medium text-gray-900 text-sm hover:text-blue-600">
                  {article.title}
                </p>
                <p className="text-xs text-gray-500 mt-1">{article.date}</p>
              </div>
              <span className="ml-2 px-2 py-1 text-xs font-semibold bg-blue-100 text-blue-700 rounded">
                {article.category}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="border-t border-gray-200 p-4">
        <button className="button-secondary w-full text-sm">View All News</button>
      </div>
    </div>
  )
}
