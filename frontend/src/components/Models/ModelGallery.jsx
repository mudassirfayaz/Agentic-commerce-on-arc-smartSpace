import { useState, useMemo, useEffect } from 'react'
import ModelCard from './ModelCard'
import CollapsibleGroup from '../UI/CollapsibleGroup'
import './ModelGallery.css'

const ModelGallery = ({ models, onModelClick }) => {
  const groupedModels = useMemo(() => {
    const grouped = {}
    models.forEach(model => {
      if (!grouped[model.provider]) {
        grouped[model.provider] = []
      }
      grouped[model.provider].push(model)
    })
    return grouped
  }, [models])

  // State management for expanded groups - all start collapsed by default
  const [expandedGroups, setExpandedGroups] = useState({})

  // Initialize all groups as collapsed when models change
  useEffect(() => {
    const providers = Object.keys(groupedModels)
    const initialState = {}
    providers.forEach(provider => {
      initialState[provider] = false
    })
    setExpandedGroups(initialState)
  }, [groupedModels])

  const handleGroupToggle = (provider) => {
    return (newState) => {
      setExpandedGroups(prev => ({
        ...prev,
        [provider]: newState
      }))
    }
  }

  const expandAll = () => {
    const providers = Object.keys(groupedModels)
    const allExpanded = {}
    providers.forEach(provider => {
      allExpanded[provider] = true
    })
    setExpandedGroups(allExpanded)
  }

  const collapseAll = () => {
    const providers = Object.keys(groupedModels)
    const allCollapsed = {}
    providers.forEach(provider => {
      allCollapsed[provider] = false
    })
    setExpandedGroups(allCollapsed)
  }

  const allExpanded = useMemo(() => {
    const providers = Object.keys(groupedModels)
    return providers.length > 0 && providers.every(provider => expandedGroups[provider])
  }, [groupedModels, expandedGroups])

  const allCollapsed = useMemo(() => {
    const providers = Object.keys(groupedModels)
    return providers.length > 0 && providers.every(provider => !expandedGroups[provider])
  }, [groupedModels, expandedGroups])

  if (models.length === 0) {
    return (
      <div className="model-gallery-empty">
        <p>No models found matching your criteria.</p>
      </div>
    )
  }

  const providers = Object.keys(groupedModels)
  const hasMultipleProviders = providers.length > 1

  return (
    <div className="model-gallery">
      {hasMultipleProviders && (
        <div className="model-gallery-controls">
          <button
            className="gallery-control-btn"
            onClick={expandAll}
            disabled={allExpanded}
            aria-label="Expand all provider groups"
          >
            Expand All
          </button>
          <button
            className="gallery-control-btn"
            onClick={collapseAll}
            disabled={allCollapsed}
            aria-label="Collapse all provider groups"
          >
            Collapse All
          </button>
        </div>
      )}
      {Object.entries(groupedModels).map(([provider, providerModels]) => (
        <CollapsibleGroup
          key={provider}
          isExpanded={expandedGroups[provider] || false}
          onToggle={handleGroupToggle(provider)}
          className="model-provider-group"
          header={
            <div className="provider-header-content">
              <span className="provider-name">{provider}</span>
              <span className="provider-count">({providerModels.length})</span>
            </div>
          }
        >
          <div className="model-grid">
            {providerModels.map(model => (
              <ModelCard
                key={model.id}
                model={model}
                onClick={onModelClick}
              />
            ))}
          </div>
        </CollapsibleGroup>
      ))}
    </div>
  )
}

export default ModelGallery

