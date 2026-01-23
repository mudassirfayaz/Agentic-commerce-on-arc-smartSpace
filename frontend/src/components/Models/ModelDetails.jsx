import './ModelDetails.css'

const ModelDetails = ({ model, onClose }) => {
  if (!model) return null

  return (
    <div className="model-details-overlay" onClick={onClose}>
      <div className="model-details-modal" onClick={(e) => e.stopPropagation()}>
        <button className="model-details-close" onClick={onClose}>×</button>
        
        <div className="model-details-header">
          <span className="details-icon">{model.icon}</span>
          <div className="details-title">
            <h2>{model.name}</h2>
            <span className="details-provider">{model.provider}</span>
          </div>
        </div>
        
        <div className="model-details-content">
          <p className="details-description">{model.description}</p>
          
          <div className="details-section">
            <h3>Category</h3>
            <span className="details-category">{model.category}</span>
          </div>
          
          <div className="details-section">
            <h3>Pricing Tier</h3>
            <span className={`details-pricing pricing-${model.pricing_tier}`}>
              {model.pricing_tier}
            </span>
          </div>
          
          <div className="details-section">
            <h3>Capabilities</h3>
            <div className="details-capabilities">
              {model.capabilities.map((cap, idx) => (
                <span key={idx} className="capability-badge">{cap}</span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ModelDetails

