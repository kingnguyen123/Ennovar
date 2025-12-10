import React, { useState } from 'react'

export default function ChatBox() {
  const [messages, setMessages] = useState([
    { id: 1, type: 'bot', text: 'Hello! How can I help you with your forecast today?' },
    { id: 2, type: 'user', text: 'What does the 1 Week forecast suggest?' },
    { id: 3, type: 'bot', text: 'Based on current trends, the 1 Week forecast shows a 12% increase in sales.' },
  ])
  const [inputValue, setInputValue] = useState('')

  const handleSendMessage = () => {
    if (inputValue.trim()) {
      const newMessage = {
        id: messages.length + 1,
        type: 'user',
        text: inputValue,
      }
      setMessages([...messages, newMessage])
      setInputValue('')

      // Simulate bot response
      setTimeout(() => {
        const botMessage = {
          id: messages.length + 2,
          type: 'bot',
          text: 'Thank you for your question. I am processing your request...',
        }
        setMessages((prev) => [...prev, botMessage])
      }, 500)
    }
  }

  return (
    <div className="sidebar-panel">
      <div className="border-b border-gray-200 p-4">
        <h3 className="text-lg font-bold text-gray-900">💬 Chat Assistant</h3>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-xs px-4 py-2 rounded-lg ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-gray-100 text-gray-900 rounded-bl-none'
              }`}
            >
              <p className="text-sm">{message.text}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="border-t border-gray-200 p-4 space-y-2">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type a message..."
            className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSendMessage}
            className="button-primary text-sm px-3 py-2"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
}
