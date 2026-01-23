import { useState, useEffect, useRef } from 'react'
import { debounce } from '../../utils/debounce'
import './ModelSearch.css'

const ModelSearch = ({ onSearch, onFilterChange, providers, categories, disabled = false }) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedProvider, setSelectedProvider] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  
  // Debounced search function
  const debouncedSearch = useRef(
    debounce((query) => {
      onSearch(query)
    }, 300)
  ).current

  const handleSearchChange = (e) => {
    const query = e.target.value
    setSearchQuery(query)
    debouncedSearch(query)
  }

  const handleProviderFilter = (provider) => {
    const newProvider = selectedProvider === provider ? '' : provider
    setSelectedProvider(newProvider)
    onFilterChange({ provider: newProvider, category: selectedCategory })
  }

  const handleCategoryFilter = (category) => {
    const newCategory = selectedCategory === category ? '' : category
    setSelectedCategory(newCategory)
    onFilterChange({ provider: selectedProvider, category: newCategory })
  }

  const clearFilters = () => {
    setSearchQuery('')
    setSelectedProvider('')
    setSelectedCategory('')
    onSearch('')
    onFilterChange({ provider: '', category: '' })
  }

  const activeFilterCount = (selectedProvider ? 1 : 0) + (selectedCategory ? 1 : 0) + (searchQuery ? 1 : 0)

  return (
    <div className="model-search">
      <div className="search-bar-container">
        <input
          type="text"
          className="search-input"
          placeholder="Search models by name, provider, or description..."
          value={searchQuery}
          onChange={handleSearchChange}
          disabled={disabled}
        />
        {activeFilterCount > 0 && (
          <button className="clear-filters-btn" onClick={clearFilters}>
            Clear filters ({activeFilterCount})
          </button>
        )}
      </div>
      
      <div className="filter-chips">
        <div className="filter-group">
          <span className="filter-label">Provider:</span>
          <div className="chip-container">
            {providers.map(provider => (
              <button
                key={provider}
                className={`filter-chip ${selectedProvider === provider ? 'active' : ''}`}
                onClick={() => handleProviderFilter(provider)}
                disabled={disabled}
              >
                {provider}
              </button>
            ))}
          </div>
        </div>
        
        <div className="filter-group">
          <span className="filter-label">Category:</span>
          <div className="chip-container">
            {categories.map(category => (
              <button
                key={category}
                className={`filter-chip ${selectedCategory === category ? 'active' : ''}`}
                onClick={() => handleCategoryFilter(category)}
                disabled={disabled}
              >
                {category}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ModelSearch

