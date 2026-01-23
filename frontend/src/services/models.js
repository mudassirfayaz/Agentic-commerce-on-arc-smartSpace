/**
 * Model service - handles model data fetching and caching.
 */

import { fetchModels, fetchModel, fetchProviders, fetchCategories } from './api'
import modelsData from '../data/models.json'

// Client-side cache
let modelsCache = null
let providersCache = null
let categoriesCache = null
let cacheTimestamp = null
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes

/**
 * Get models with fallback to static data if API fails.
 * @param {Object} filters - Filter options
 * @param {boolean} useCache - Whether to use cached data
 * @returns {Promise<Array>} Array of models
 */
export const getModels = async (filters = {}, useCache = true) => {
  // Check cache first
  if (useCache && modelsCache && cacheTimestamp && (Date.now() - cacheTimestamp) < CACHE_DURATION) {
    return applyFilters(modelsCache, filters)
  }
  
  try {
    // Try to fetch from API
    const models = await fetchModels(filters)
    modelsCache = models
    cacheTimestamp = Date.now()
    return models
  } catch (error) {
    console.warn('API fetch failed, using static data:', error)
    // Fallback to static JSON data
    const staticModels = modelsData.models || []
    modelsCache = staticModels
    cacheTimestamp = Date.now()
    return applyFilters(staticModels, filters)
  }
}

/**
 * Apply filters to model array (client-side filtering).
 * @param {Array} models - Array of models
 * @param {Object} filters - Filter options
 * @returns {Array} Filtered models
 */
const applyFilters = (models, filters) => {
  let filtered = [...models]
  
  if (filters.provider) {
    filtered = filtered.filter(model => model.provider === filters.provider)
  }
  
  if (filters.category) {
    filtered = filtered.filter(model => model.category === filters.category)
  }
  
  if (filters.search) {
    const query = filters.search.toLowerCase()
    filtered = filtered.filter(model =>
      model.name.toLowerCase().includes(query) ||
      model.provider.toLowerCase().includes(query) ||
      model.description.toLowerCase().includes(query) ||
      (model.capabilities && model.capabilities.some(cap => cap.toLowerCase().includes(query)))
    )
  }
  
  return filtered
}

/**
 * Get a single model by ID.
 * @param {string} modelId - Model ID
 * @returns {Promise<Object>} Model object
 */
export const getModel = async (modelId) => {
  try {
    return await fetchModel(modelId)
  } catch (error) {
    console.warn('API fetch failed, using static data:', error)
    // Fallback to static data
    const model = modelsData.models?.find(m => m.id === modelId)
    if (!model) {
      throw new Error('Model not found')
    }
    return model
  }
}

/**
 * Get list of providers.
 * @param {boolean} useCache - Whether to use cached data
 * @returns {Promise<Array>} Array of provider names
 */
export const getProviders = async (useCache = true) => {
  if (useCache && providersCache) {
    return providersCache
  }
  
  try {
    const providers = await fetchProviders()
    providersCache = providers
    return providers
  } catch (error) {
    console.warn('API fetch failed, extracting from static data:', error)
    // Fallback: extract from static data
    const providers = [...new Set(modelsData.models?.map(m => m.provider) || [])].sort()
    providersCache = providers
    return providers
  }
}

/**
 * Get list of categories.
 * @param {boolean} useCache - Whether to use cached data
 * @returns {Promise<Array>} Array of category names
 */
export const getCategories = async (useCache = true) => {
  if (useCache && categoriesCache) {
    return categoriesCache
  }
  
  try {
    const categories = await fetchCategories()
    categoriesCache = categories
    return categories
  } catch (error) {
    console.warn('API fetch failed, extracting from static data:', error)
    // Fallback: extract from static data
    const categories = [...new Set(modelsData.models?.map(m => m.category) || [])].sort()
    categoriesCache = categories
    return categories
  }
}

/**
 * Clear the cache.
 */
export const clearCache = () => {
  modelsCache = null
  providersCache = null
  categoriesCache = null
  cacheTimestamp = null
}

