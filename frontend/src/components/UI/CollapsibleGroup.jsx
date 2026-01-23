import { useState, useEffect } from 'react'
import { HiOutlineChevronDown } from 'react-icons/hi2'
import './CollapsibleGroup.css'

/**
 * CollapsibleGroup - A reusable component for creating collapsible content sections
 * 
 * @param {ReactNode} header - Content to display in the collapsible header
 * @param {ReactNode} children - Content to show/hide when expanded/collapsed
 * @param {boolean} defaultExpanded - Initial expanded state (default: false)
 * @param {boolean} isExpanded - Controlled expanded state (overrides defaultExpanded)
 * @param {function} onToggle - Callback function called when toggled (receives new state)
 * @param {string} className - Additional CSS classes
 */
const CollapsibleGroup = ({ 
  header, 
  children, 
  defaultExpanded = false,
  isExpanded: controlledExpanded,
  onToggle,
  className = ''
}) => {
  const [internalExpanded, setInternalExpanded] = useState(defaultExpanded)
  
  // Use controlled state if provided, otherwise use internal state
  const isExpanded = controlledExpanded !== undefined ? controlledExpanded : internalExpanded
  
  // Sync internal state when controlled prop changes
  useEffect(() => {
    if (controlledExpanded !== undefined) {
      setInternalExpanded(controlledExpanded)
    }
  }, [controlledExpanded])

  const handleToggle = () => {
    const newState = !isExpanded
    if (controlledExpanded === undefined) {
      // Only update internal state if not controlled
      setInternalExpanded(newState)
    }
    if (onToggle) {
      onToggle(newState)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleToggle()
    }
  }

  const groupId = `collapsible-group-${Math.random().toString(36).substr(2, 9)}`
  const contentId = `${groupId}-content`

  return (
    <div className={`collapsible-group ${className}`}>
      <button
        className="collapsible-header"
        onClick={handleToggle}
        onKeyDown={handleKeyDown}
        aria-expanded={isExpanded}
        aria-controls={contentId}
        type="button"
      >
        <span className="collapsible-header-content">{header}</span>
        <span 
          className={`collapsible-chevron ${isExpanded ? 'expanded' : ''}`}
          aria-hidden="true"
        >
          <HiOutlineChevronDown />
        </span>
      </button>
      <div
        id={contentId}
        className={`collapsible-content ${isExpanded ? 'expanded' : ''}`}
        role="region"
        aria-hidden={!isExpanded}
      >
        <div className="collapsible-content-inner">
          {children}
        </div>
      </div>
    </div>
  )
}

export default CollapsibleGroup

