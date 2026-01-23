import { useState, useEffect } from 'react'
import DashboardLayout from '../components/Dashboard/DashboardLayout'
import './ApiKeys.css'

const ApiKeys = () => {
  const [apiKey, setApiKey] = useState(null)
  const [isMasked, setIsMasked] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState(null)
  const [showConfirmDialog, setShowConfirmDialog] = useState(false)
  const [copySuccess, setCopySuccess] = useState(false)
  const [newKeyGenerated, setNewKeyGenerated] = useState(false)

  // Fetch existing API key on component mount
  useEffect(() => {
    fetchApiKey()
  }, [])

  const fetchApiKey = async () => {
    setIsLoading(true)
    setError(null)
    try {
      // TODO: Replace with actual backend API endpoint
      const response = await fetch('/api/v1/api-keys', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // TODO: Add authentication header
        },
      })

      if (response.ok) {
        const data = await response.json()
        setApiKey(data.api_key || data.key || null)
      } else if (response.status === 404) {
        // No API key exists yet
        setApiKey(null)
      } else {
        throw new Error('Failed to fetch API key')
      }
    } catch (err) {
      console.error('Error fetching API key:', err)
      setError('Failed to load API key. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const generateApiKey = async () => {
    setIsGenerating(true)
    setError(null)
    setNewKeyGenerated(false)
    try {
      const response = await fetch('/api/v1/api-keys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // TODO: Add authentication header
        },
      })

      if (response.ok) {
        const data = await response.json()
        setApiKey(data.api_key || data.key)
        setNewKeyGenerated(true)
        setIsMasked(false) // Show the new key immediately
        setShowConfirmDialog(false)
      } else {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || 'Failed to generate API key')
      }
    } catch (err) {
      console.error('Error generating API key:', err)
      setError(err.message || 'Failed to generate API key. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleGenerateClick = () => {
    if (apiKey) {
      setShowConfirmDialog(true)
    } else {
      generateApiKey()
    }
  }

  const handleConfirmGenerate = () => {
    generateApiKey()
  }

  const handleCopy = async () => {
    if (!apiKey) return

    try {
      await navigator.clipboard.writeText(apiKey)
      setCopySuccess(true)
      setTimeout(() => setCopySuccess(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
      setError('Failed to copy API key to clipboard')
    }
  }

  const maskApiKey = (key) => {
    if (!key) return ''
    if (key.length <= 8) return '••••••••'
    return `${key.substring(0, 4)}${'•'.repeat(key.length - 8)}${key.substring(key.length - 4)}`
  }

  return (
    <DashboardLayout>
      <div className="api-keys-page">
        <div className="api-keys-header">
          <h1>API Keys</h1>
          <p className="api-keys-description">
            Manage your API keys for accessing SmartSpace services. Your API key provides unified access to all models.
          </p>
        </div>

        {error && (
          <div className="api-keys-error">
            <span>{error}</span>
            <button onClick={() => setError(null)} className="error-close">×</button>
          </div>
        )}

        {newKeyGenerated && (
          <div className="api-keys-warning">
            <strong>⚠️ Important:</strong> This API key will only be shown once. Make sure to copy and store it securely.
          </div>
        )}

        <div className="api-keys-content">
          {isLoading ? (
            <div className="api-keys-loading">
              <div className="spinner"></div>
              <p>Loading API key...</p>
            </div>
          ) : apiKey ? (
            <div className="api-key-card">
              <div className="api-key-header">
                <h2>Your API Key</h2>
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

              <div className="api-key-display">
                <code className={`api-key-value ${isMasked ? 'masked' : ''}`}>
                  {isMasked ? maskApiKey(apiKey) : apiKey}
                </code>
              </div>

              <div className="api-key-security-warning">
                <strong>🔒 Security Warning:</strong> Keep your API key secure and never share it publicly. 
                Anyone with access to your API key can make requests on your account.
              </div>

              <div className="api-key-metadata">
                <div className="metadata-item">
                  <span className="metadata-label">Status:</span>
                  <span className="metadata-value active">Active</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="api-keys-empty">
              <div className="empty-icon">🔑</div>
              <h2>No API Key</h2>
              <p>Generate your first API key to start using SmartSpace services</p>
            </div>
          )}

          <div className="api-keys-actions">
            <button
              onClick={handleGenerateClick}
              className="btn btn-primary"
              disabled={isGenerating || isLoading}
            >
              {isGenerating ? 'Generating...' : apiKey ? 'Regenerate API Key' : 'Generate API Key'}
            </button>
          </div>
        </div>

        {showConfirmDialog && (
          <div className="modal-overlay" onClick={() => setShowConfirmDialog(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h3>Regenerate API Key?</h3>
              <p>
                Generating a new API key will invalidate your current key. Any applications using the old key will stop working.
                Make sure to update all integrations with the new key.
              </p>
              <div className="modal-actions">
                <button
                  onClick={() => setShowConfirmDialog(false)}
                  className="btn btn-outline"
                >
                  Cancel
                </button>
                <button
                  onClick={handleConfirmGenerate}
                  className="btn btn-primary"
                  disabled={isGenerating}
                >
                  {isGenerating ? 'Generating...' : 'Generate New Key'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}

export default ApiKeys

