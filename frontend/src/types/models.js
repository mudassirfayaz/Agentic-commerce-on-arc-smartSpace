/**
 * Type definitions for model data structures.
 * 
 * @typedef {Object} Model
 * @property {string} id - Unique model identifier
 * @property {string} name - Display name of the model
 * @property {string} provider - Provider name (e.g., 'openai', 'anthropic')
 * @property {string} category - Model category (e.g., 'text', 'vision', 'audio')
 * @property {string[]} capabilities - Array of capability strings
 * @property {string} pricing_tier - Pricing tier ('free', 'low', 'medium', 'high')
 * @property {string} description - Model description
 * @property {string} icon - Icon/emoji for the model
 * 
 * @typedef {Object} ModelFilters
 * @property {string} [provider] - Filter by provider
 * @property {string} [category] - Filter by category
 * @property {string} [search] - Search query
 * 
 * @typedef {Object} ModelCatalog
 * @property {Model[]} models - Array of models
 */

// Export types for JSDoc usage
export const ModelType = {
  /**
   * @type {Model}
   */
  example: {
    id: 'gpt-4',
    name: 'GPT-4',
    provider: 'openai',
    category: 'text',
    capabilities: ['text-generation', 'conversation', 'reasoning'],
    pricing_tier: 'high',
    description: 'Most capable GPT-4 model',
    icon: '🤖'
  }
}

