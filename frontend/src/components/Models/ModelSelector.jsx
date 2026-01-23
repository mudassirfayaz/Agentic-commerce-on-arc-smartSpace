import { useState, useMemo } from 'react'
import './ModelSelector.css'

const ModelSelector = ({ models, onSelect, selectedModel, disabled = false }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const filteredModels = useMemo(() => {
    if (!searchQuery) return models
    
    const query = searchQuery.toLowerCase()
    return models.filter(model => 
      model.name.toLowerCase().includes(query) ||
      model.provider.toLowerCase().includes(query) ||
      model.description.toLowerCase().includes(query) ||
      model.capabilities.some(cap => cap.toLowerCase().includes(query))
    )
  }, [models, searchQuery])

  const groupedModels = useMemo(() => {
    const grouped = {}
    filteredModels.forEach(model => {
      if (!grouped[model.provider]) {
        grouped[model.provider] = []
      }
      grouped[model.provider].push(model)
    })
    return grouped
  }, [filteredModels])

  const handleSelect = (model) => {
    onSelect(model)
    setIsOpen(false)
    setSearchQuery('')
  }

  return (
    <div className="model-selector">
      <div 
        className={`model-selector-trigger ${disabled ? 'disabled' : ''}`}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        style={{ cursor: disabled ? 'not-allowed' : 'pointer', opacity: disabled ? 0.6 : 1 }}
      >
        <span className="selector-label">Model</span>
        <span className="selector-value">
          {selectedModel ? selectedModel.name : 'Select a model...'}
        </span>
        <span className="selector-arrow">{isOpen ? '▲' : '▼'}</span>
      </div>
      
      {isOpen && (
        <div className="model-selector-dropdown">
          <div className="selector-search">
            <input
              type="text"
              className="selector-search-input"
              placeholder="Search models..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onClick={(e) => e.stopPropagation()}
            />
          </div>
          
          <div className="selector-options">
            {Object.keys(groupedModels).length === 0 ? (
              <div className="selector-empty">No models found</div>
            ) : (
              Object.entries(groupedModels).map(([provider, providerModels]) => (
                <div key={provider} className="selector-provider-group">
                  <div className="provider-group-header">{provider}</div>
                  {providerModels.map(model => (
                    <div
                      key={model.id}
                      className={`selector-option ${selectedModel?.id === model.id ? 'selected' : ''}`}
                      onClick={() => handleSelect(model)}
                    >
                      <div className="option-content">
                        <span className="option-icon">{model.icon}</span>
                        <div className="option-info">
                          <span className="option-name">{model.name}</span>
                          <span className="option-category">{model.category}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default ModelSelector

