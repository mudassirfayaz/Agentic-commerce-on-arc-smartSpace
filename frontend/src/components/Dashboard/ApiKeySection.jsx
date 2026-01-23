import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import './ApiKeySection.css'

const ApiKeySection = ({ onApiKeyChange }) => {
  const [apiKey, setApiKey] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isMasked, setIsMasked] = useState(true)
  const [copySuccess, setCopySuccess] = useState(false)

  useEffect(() => {
    fetchApiKey()
  }, [])

  const fetchApiKey = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/v1/api-keys', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        const key = data.api_key || data.key || null
        setApiKey(key)
        if (onApiKeyChange) onApiKeyChange(key)
      } else if (response.status === 404) {
        setApiKey(null)
        if (onApiKeyChange) onApiKeyChange(null)
      }
    } catch (err) {
      console.error('Error fetching API key:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCopy = async () => {
    if (!apiKey) return

    try {
      await navigator.clipboard.writeText(apiKey)
      setCopySuccess(true)
      setTimeout(() => setCopySuccess(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const maskApiKey = (key) => {
    if (!key) return ''
    if (key.length <= 8) return '••••••••'
    return `${key.substring(0, 4)}${'•'.repeat(key.length - 8)}${key.substring(key.length - 4)}`
  }

  if (isLoading) {
    return (
      <div className="api-key-section">
        <div className="api-key-loading">Loading API key...</div>
      </div>
    )
  }

  if (!apiKey) {
    return (
      <div className="api-key-section">
        <div className="api-key-empty">
          <h3>API Key</h3>
          <p>Generate your API key to start using SmartSpace</p>
          <Link to="/dashboard/api-keys" className="btn btn-primary">
            Generate API Key
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="api-key-section">
      <div className="api-key-header">
        <h3>Your API Key</h3>
        <Link to="/dashboard/api-keys" className="link-text">
          Manage Keys →
        </Link>
      </div>
      <div className="api-key-display">
        <code className={`api-key-value ${isMasked ? 'masked' : ''}`}>
          {isMasked ? maskApiKey(apiKey) : apiKey}
        </code>
        <div className="api-key-actions">
          <button
            onClick={() => setIsMasked(!isMasked)}
            className="btn btn-outline"
            aria-label={isMasked ? 'Show API key' : 'Hide API key'}
          >
            {isMasked ? 'Show' : 'Hide'}
          </button>
          <button
            onClick={handleCopy}
            className={`btn btn-primary ${copySuccess ? 'copied' : ''}`}
            disabled={isMasked}
          >
            {copySuccess ? '✓ Copied!' : 'Copy'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ApiKeySection

