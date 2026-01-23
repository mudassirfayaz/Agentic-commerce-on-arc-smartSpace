import { memo } from 'react'
import './ModelCard.css'

const ModelCard = memo(({ model, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick(model)
    }
  }

  return (
    <div className="model-card" onClick={handleClick}>
      <div className="model-card-header">
        <span className="model-icon">{model.icon}</span>
        <div className="model-card-title">
          <h4 className="model-name">{model.name}</h4>
          <span className="model-provider">{model.provider}</span>
        </div>
      </div>
      <p className="model-description">{model.description}</p>
      <div className="model-card-footer">
        <span className={`model-pricing-tier pricing-${model.pricing_tier}`}>
          {model.pricing_tier}
        </span>
        <span className="model-category">{model.category}</span>
      </div>
      <div className="model-capabilities">
        {model.capabilities.slice(0, 3).map((cap, idx) => (
          <span key={idx} className="capability-tag">{cap}</span>
        ))}
        {model.capabilities.length > 3 && (
          <span className="capability-tag">+{model.capabilities.length - 3}</span>
        )}
      </div>
    </div>
  )
})

ModelCard.displayName = 'ModelCard'

export default ModelCard

