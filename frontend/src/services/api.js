/**
 * API service for making HTTP requests to the backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

/**
 * Fetch models from the backend API.
 * @param {Object} filters - Filter options (provider, category, search)
 * @returns {Promise<Array>} Array of model objects
 */
export const fetchModels = async (filters = {}) => {
  try {
    const params = new URLSearchParams()
    if (filters.provider) params.append('provider', filters.provider)
    if (filters.category) params.append('category', filters.category)
    if (filters.search) params.append('search', filters.search)
    
    const url = `${API_BASE_URL}/models${params.toString() ? `?${params.toString()}` : ''}`
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch models: ${response.statusText}`)
    }
    
    const data = await response.json()
    // Backend returns: { success: true, data: { models: [...], total: N }, message: "..." }
    if (data.success && data.data) {
      return data.data.models || data.data
    }
    // Fallback for different response formats
    return data.data?.models || data.models || data.data || data
  } catch (error) {
    console.error('Error fetching models:', error)
    throw error
  }
}

/**
 * Fetch a single model by ID.
 * @param {string} modelId - Model ID
 * @returns {Promise<Object>} Model object
 */
export const fetchModel = async (modelId) => {
  try {
    const url = `${API_BASE_URL}/models/${modelId}`
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Model not found')
      }
      throw new Error(`Failed to fetch model: ${response.statusText}`)
    }
    
    const data = await response.json()
    return data.data || data
  } catch (error) {
    console.error('Error fetching model:', error)
    throw error
  }
}

/**
 * Fetch list of providers.
 * @returns {Promise<Array>} Array of provider names
 */
export const fetchProviders = async () => {
  try {
    const url = `${API_BASE_URL}/models/providers/list`
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch providers: ${response.statusText}`)
    }
    
    const data = await response.json()
    // Backend returns: { success: true, data: { providers: [...] }, message: "..." }
    if (data.success && data.data) {
      return data.data.providers || data.data
    }
    return data.data || data
  } catch (error) {
    console.error('Error fetching providers:', error)
    throw error
  }
}

/**
 * Fetch list of categories.
 * @returns {Promise<Array>} Array of category names
 */
export const fetchCategories = async () => {
  try {
    const url = `${API_BASE_URL}/models/categories/list`
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch categories: ${response.statusText}`)
    }
    
    const data = await response.json()
    // Backend returns: { success: true, data: { categories: [...] }, message: "..." }
    if (data.success && data.data) {
      return data.data.categories || data.data
    }
    return data.data || data
  } catch (error) {
    console.error('Error fetching categories:', error)
    throw error
  }
}

