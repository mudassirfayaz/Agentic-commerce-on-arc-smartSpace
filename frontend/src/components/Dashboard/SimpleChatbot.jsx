import { useState, useEffect } from 'react'
import './SimpleChatbot.css'

const SimpleChatbot = ({ apiKey, onRequestComplete, onModelChange, onTextChange }) => {
  const [selectedModel, setSelectedModel] = useState('ollama/qalb-urdu')
  const [inputText, setInputText] = useState('')
  const [response, setResponse] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [recentRequests, setRecentRequests] = useState([])

  // Common models for dropdown
  const models = [
    { value: 'ollama/qalb-urdu', label: 'Qalb (Urdu LLM)' },
    { value: 'ollama/deepseek-r1', label: 'DeepSeek R1' },
    { value: 'ollama/llama2', label: 'LLaMA-2' },
    { value: 'openai/gpt-4', label: 'OpenAI GPT-4' },
    { value: 'openai/gpt-3.5-turbo', label: 'OpenAI GPT-3.5 Turbo' },
    { value: 'anthropic/claude-3', label: 'Anthropic Claude 3' },
  ]

  const handleSend = async () => {
    if (!inputText.trim() || !apiKey || isLoading) return

    setIsLoading(true)
    setError(null)
    setResponse(null)

    const requestData = {
      model: selectedModel,
      text: inputText.trim(),
    }

    try {
      const response = await fetch('/v1/text/completion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify(requestData),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error?.message || errorData.message || `HTTP ${response.status}`)
      }

      const data = await response.json()
      setResponse(data)
      
      // Add to recent requests
      const newRequest = {
        id: data.id || Date.now().toString(),
        model: selectedModel,
        text: inputText.trim(),
        response: data,
        timestamp: new Date().toISOString(),
        status: 'success',
      }
      setRecentRequests(prev => [newRequest, ...prev].slice(0, 10))
      
      // Notify parent component
      if (onRequestComplete) {
        onRequestComplete(newRequest)
      }
    } catch (err) {
      console.error('Error making request:', err)
      setError(err.message || 'Failed to process request. Please try again.')
      
      // Add failed request to history
      const failedRequest = {
        id: Date.now().toString(),
        model: selectedModel,
        text: inputText.trim(),
        error: err.message,
        timestamp: new Date().toISOString(),
        status: 'error',
      }
      setRecentRequests(prev => [failedRequest, ...prev].slice(0, 10))
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSend()
    }
  }

  return (
    <div className="simple-chatbot">
      <div className="chatbot-header">
        <h3>Test API Request</h3>
        <p className="chatbot-subtitle">Send a request to test your API key</p>
      </div>

      <div className="chatbot-controls">
        <div className="model-selector-group">
          <label htmlFor="model-select">Model</label>
          <select
            id="model-select"
            value={selectedModel}
            onChange={(e) => {
              setSelectedModel(e.target.value)
              if (onModelChange) onModelChange(e.target.value)
            }}
            className="model-select"
            disabled={isLoading}
          >
            {models.map((model) => (
              <option key={model.value} value={model.value}>
                {model.label}
              </option>
            ))}
          </select>
        </div>

        <div className="input-group">
          <label htmlFor="chatbot-input">Your Message</label>
          <textarea
            id="chatbot-input"
            value={inputText}
            onChange={(e) => {
              setInputText(e.target.value)
              if (onTextChange) onTextChange(e.target.value)
            }}
            onKeyDown={handleKeyPress}
            placeholder="Enter your message here... (Ctrl+Enter to send)"
            className="chatbot-input"
            rows={6}
            disabled={isLoading || !apiKey}
          />
        </div>

        <button
          onClick={handleSend}
          className="btn btn-primary btn-block"
          disabled={!inputText.trim() || !apiKey || isLoading}
        >
          {isLoading ? 'Sending...' : 'Send Request'}
        </button>

        {!apiKey && (
          <div className="chatbot-warning">
            ⚠️ Please generate an API key first to make requests
          </div>
        )}
      </div>

      {error && (
        <div className="chatbot-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {response && (
        <div className="chatbot-response">
          <div className="response-header">
            <h4>Response</h4>
            {response.payment && (
              <div className="payment-info">
                <span className="payment-label">Payment:</span>
                <span className="payment-status success">✓ Processed</span>
                {response.payment.transaction_hash && (
                  <span className="payment-hash">
                    TX: {response.payment.transaction_hash.substring(0, 16)}...
                  </span>
                )}
              </div>
            )}
          </div>
          <div className="response-content">
            {response.choices && response.choices.length > 0 ? (
              response.choices.map((choice, index) => (
                <div key={index} className="choice-item">
                  {choice.message && (
                    <div className="message-content">
                      {choice.message.content}
                    </div>
                  )}
                  {choice.text && (
                    <div className="message-content">{choice.text}</div>
                  )}
                  {choice.audio && (
                    <div className="audio-response">
                      <audio controls src={choice.audio} />
                    </div>
                  )}
                </div>
              ))
            ) : (
              <div className="message-content">
                {JSON.stringify(response, null, 2)}
              </div>
            )}
          </div>
        </div>
      )}

      {recentRequests.length > 0 && (
        <div className="recent-requests">
          <h4>Recent Requests</h4>
          <div className="requests-list">
            {recentRequests.map((request) => (
              <div key={request.id} className={`request-item ${request.status}`}>
                <div className="request-header">
                  <span className="request-model">{request.model}</span>
                  <span className="request-time">
                    {new Date(request.timestamp).toLocaleTimeString()}
                  </span>
                  <span className={`request-status ${request.status}`}>
                    {request.status === 'success' ? '✓' : '✗'}
                  </span>
                </div>
                <div className="request-preview">
                  {request.text.substring(0, 50)}
                  {request.text.length > 50 ? '...' : ''}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default SimpleChatbot

