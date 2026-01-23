import { useState, useEffect } from 'react'
import { ModelSelector } from '../Models'
import { getModels } from '../../services/models'
import modelsData from '../../data/models.json' // Fallback
import './ApiCallInterface.css'

const ApiCallInterface = () => {
  const [selectedModel, setSelectedModel] = useState(null)
  const [allModels, setAllModels] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  
  // Load models on mount
  useEffect(() => {
    const loadModels = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const models = await getModels()
        setAllModels(models)
      } catch (err) {
        console.error('Error loading models:', err)
        setError('Failed to load models. Using cached data.')
        // Fallback to static data
        setAllModels(modelsData.models || [])
      } finally {
        setIsLoading(false)
      }
    }
    loadModels()
  }, [])
  
  const handleModelSelect = (model) => {
    setSelectedModel(model)
  }
  
  return (
    <div className="api-call-interface">
      <h3>Test API Request</h3>
      <div className="api-form-group">
        <label htmlFor="api-provider">AI Model</label>
        {isLoading ? (
          <div style={{ padding: '20px', textAlign: 'center', color: '#F2F2F2' }}>
            Loading models...
          </div>
        ) : error ? (
          <div style={{ padding: '12px', background: 'rgba(187, 78, 239, 0.1)', borderRadius: '8px', color: '#BB4EEF', marginBottom: '10px' }}>
            {error}
          </div>
        ) : null}
        <ModelSelector
          models={allModels}
          onSelect={handleModelSelect}
          selectedModel={selectedModel}
          disabled={isLoading}
        />
        {selectedModel && (
          <div className="selected-model-info">
            <span className="model-info-text">
              Selected: {selectedModel.name} ({selectedModel.provider}) - {selectedModel.category}
            </span>
          </div>
        )}
      </div>
      <div className="api-form-group">
        <label htmlFor="api-prompt">Prompt / Request</label>
        <textarea
          id="api-prompt"
          placeholder="Enter your API request here..."
        ></textarea>
      </div>
      <div className="api-form-group">
        <label htmlFor="max-tokens">Max Tokens (optional)</label>
        <input
          type="number"
          id="max-tokens"
          placeholder="1000"
          min="1"
          max="8000"
        />
      </div>
      <button className="btn btn-primary btn-block">
        Execute Request (Pay with USDC)
      </button>
      <div className="api-note">
        Estimated cost will be calculated before execution
      </div>
    </div>
  )
}

export default ApiCallInterface

