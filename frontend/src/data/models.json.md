# Model Catalog JSON Structure

This document describes the structure of the model catalog JSON file.

## File Location
`frontend/src/data/models.json`

## Root Structure
```json
{
  "models": [
    // Array of model objects
  ]
}
```

## Model Object Structure

Each model object in the `models` array has the following structure:

```json
{
  "id": "string",              // Unique model identifier (e.g., "gpt-4")
  "name": "string",            // Display name (e.g., "GPT-4")
  "provider": "string",         // Provider name (e.g., "openai", "anthropic")
  "category": "string",        // Category (e.g., "text", "vision", "audio", "embeddings", "code", "multimodal")
  "capabilities": ["string"],  // Array of capability strings (e.g., ["text-generation", "conversation"])
  "pricing_tier": "string",    // Pricing tier: "free", "low", "medium", or "high"
  "description": "string",     // Model description
  "icon": "string"             // Icon/emoji for the model (e.g., "🤖")
}
```

## Field Descriptions

### id
- **Type**: String
- **Required**: Yes
- **Description**: Unique identifier for the model. Used for API calls and model lookup.
- **Example**: `"gpt-4"`, `"claude-3-opus"`

### name
- **Type**: String
- **Required**: Yes
- **Description**: Human-readable display name of the model.
- **Example**: `"GPT-4"`, `"Claude 3 Opus"`

### provider
- **Type**: String
- **Required**: Yes
- **Description**: Provider name (lowercase, kebab-case). Used for grouping and filtering.
- **Examples**: `"openai"`, `"anthropic"`, `"google"`, `"meta"`, `"cohere"`, `"stability-ai"`, `"hugging-face"`, `"ollama"`

### category
- **Type**: String
- **Required**: Yes
- **Description**: Model category. Used for filtering and organization.
- **Valid Values**: `"text"`, `"vision"`, `"audio"`, `"embeddings"`, `"code"`, `"multimodal"`

### capabilities
- **Type**: Array of Strings
- **Required**: Yes
- **Description**: List of capabilities the model supports. Used for search and filtering.
- **Examples**: `["text-generation", "conversation", "reasoning"]`, `["vision", "image-analysis"]`

### pricing_tier
- **Type**: String
- **Required**: Yes
- **Description**: Pricing tier indicator.
- **Valid Values**: `"free"`, `"low"`, `"medium"`, `"high"`

### description
- **Type**: String
- **Required**: Yes
- **Description**: Brief description of the model's capabilities and use cases. Used in search.

### icon
- **Type**: String
- **Required**: Yes
- **Description**: Emoji or icon string to represent the model visually.
- **Examples**: `"🤖"`, `"👁️"`, `"💬"`, `"🎨"`

## Example Model Entry

```json
{
  "id": "gpt-4",
  "name": "GPT-4",
  "provider": "openai",
  "category": "text",
  "capabilities": ["text-generation", "conversation", "reasoning"],
  "pricing_tier": "high",
  "description": "Most capable GPT-4 model, optimized for complex tasks requiring deep understanding and reasoning.",
  "icon": "🤖"
}
```

## Data Validation

The model catalog should:
- Contain at least 100 models
- Have unique `id` values
- Use consistent provider names (lowercase, kebab-case)
- Use valid category values
- Include all required fields for each model

## Usage

The model catalog is:
- Loaded by the frontend on page load
- Served by the backend API at `/api/v1/models`
- Cached client-side for 5 minutes
- Used for search, filtering, and model selection

