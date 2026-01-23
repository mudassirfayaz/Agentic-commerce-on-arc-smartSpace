# Add 100+ AI Models Showcase - Design Document

## Context

The SmartSpace landing page currently:
- Mentions "100+ AI models" in marketing copy
- Only shows 4 provider cards (OpenAI, Anthropic, Google, Other Providers)
- No actual list of models displayed
- No search or filter capabilities

The dashboard API call interface:
- Has hardcoded dropdown with only 5 model options
- No comprehensive model selection
- No model details or metadata

Users need to:
- See the actual models available
- Search and filter models by provider, capability, use case
- Understand model capabilities and pricing
- Select models easily from a comprehensive list

## Goals / Non-Goals

### Goals
- Display 100+ famous AI models in an organized, searchable format
- Group models by provider for easy navigation
- Enable search and filtering (by provider, capability, use case)
- Show model metadata (name, provider, capabilities, pricing tier)
- Make models discoverable on landing page
- Improve model selection in dashboard
- Create reusable model components

### Non-Goals
- Real-time model availability checking (assume all listed models are available)
- Model performance metrics or benchmarks
- User reviews or ratings
- Model comparison tool (future feature)
- Backend integration for actual model execution (handled by existing agentic brain)

## Decisions

### Decision 1: Model Data Structure
**What**: Create a comprehensive model catalog with structured metadata:
- Model ID (unique identifier)
- Display name
- Provider (OpenAI, Anthropic, Google, etc.)
- Category (text, vision, audio, embeddings, etc.)
- Capabilities (list of features)
- Pricing tier (free, low, medium, high)
- Description
- Icon/emoji

**Why**:
- Enables filtering and search
- Provides rich metadata for display
- Easy to extend with more fields
- Can be stored in JSON or database

**Alternatives considered**:
- Simple list: Too limited, no metadata
- Database-driven: Overkill for static catalog initially

### Decision 2: Landing Page Showcase Design
**What**: Create a searchable, filterable model gallery section:
- Search bar at top
- Filter chips (Provider, Category)
- Grid layout with model cards
- Group by provider with expandable sections
- "Show more" pagination for large lists

**Why**:
- Makes models discoverable
- Professional appearance
- Easy to navigate
- Scales to 100+ models

**Alternatives considered**:
- Simple list: Hard to navigate with 100+ items
- Tabs per provider: Too many tabs, less discoverable

### Decision 3: Dashboard Model Selection
**What**: Replace hardcoded dropdown with:
- Searchable select component
- Grouped by provider
- Shows model metadata in dropdown
- Recent/favorite models at top

**Why**:
- Better UX than long dropdown
- Easier to find models
- Consistent with landing page

**Alternatives considered**:
- Keep simple dropdown: Too limited for 100+ models
- Modal picker: More clicks, less convenient

### Decision 4: Model Data Source
**What**: Start with static JSON file, can migrate to database later:
- `frontend/src/data/models.json` - Initial model catalog
- Backend API endpoint to serve model data
- Can be cached or moved to database later

**Why**:
- Fast to implement
- Easy to update
- No database dependency initially
- Can migrate to database when needed

**Alternatives considered**:
- Database from start: More complexity, slower to implement
- Hardcoded in components: Not maintainable

### Decision 5: Model Categories
**What**: Organize models by:
- **Text Generation**: GPT-4, Claude, Gemini, etc.
- **Vision**: GPT-4 Vision, Claude Vision, Gemini Vision, DALL-E, Midjourney, Stable Diffusion
- **Audio**: Whisper, TTS models, Audio generation
- **Embeddings**: text-embedding models
- **Code**: Code-specific models
- **Multimodal**: Models supporting multiple modalities

**Why**:
- Matches common use cases
- Easy for users to understand
- Aligns with API endpoint types

**Alternatives considered**:
- Provider-only grouping: Less useful for discovery
- Single flat list: Hard to navigate

## Architecture Structure

### Frontend Components
```
frontend/src/
├── components/
│   └── Models/
│       ├── ModelCard.jsx          # Individual model card
│       ├── ModelGallery.jsx       # Grid of model cards
│       ├── ModelSearch.jsx         # Search and filter bar
│       ├── ModelSelector.jsx      # Dashboard model picker
│       └── ModelDetails.jsx       # Model detail modal/view
├── data/
│   └── models.json                # Model catalog data
└── pages/
    └── LandingPage.jsx            # Updated with showcase
```

### Backend API
```
backend/src/
├── routes/
│   └── v1/
│       └── models.py              # GET /api/v1/models
├── services/
│   └── models/
│       └── model_catalog_service.py
└── models/
    └── model_catalog.py           # Model catalog data model
```

## Model List (100+ Models)

### OpenAI (20+ models)
- GPT-4, GPT-4 Turbo, GPT-4 Vision
- GPT-3.5 Turbo, GPT-3.5 Turbo 16k
- DALL-E 2, DALL-E 3
- Whisper (various sizes)
- text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large
- TTS-1, TTS-1-HD
- Codex models
- Moderation models

### Anthropic (10+ models)
- Claude 3 Opus, Sonnet, Haiku
- Claude 2, Claude 2.1
- Claude Vision models
- Claude Instant

### Google (15+ models)
- Gemini Pro, Gemini Pro Vision
- Gemini Ultra
- PaLM 2, PaLM 2 for Chat
- Vertex AI models
- Imagen, Imagen 2
- Text-to-Speech models

### Meta (10+ models)
- LLaMA 2 (various sizes)
- LLaMA 3
- Code Llama
- Segment Anything Model (SAM)

### Cohere (8+ models)
- Command, Command Light
- Command R, Command R+
- Embed models
- Rerank models

### Stability AI (10+ models)
- Stable Diffusion XL
- Stable Diffusion 2, 2.1
- Stable Diffusion 1.5
- Stable Video Diffusion
- Stable Audio

### Hugging Face (15+ models)
- Mistral 7B, Mixtral 8x7B
- Falcon models
- BLOOM models
- StarCoder
- Various specialized models

### Other Providers (10+ models)
- Perplexity models
- Together AI models
- Replicate models
- Anyscale models
- Various open-source models

## Risks / Trade-offs

### Risk 1: Performance with 100+ Models
**Risk**: Rendering 100+ model cards may be slow
**Mitigation**: 
- Implement pagination or virtual scrolling
- Lazy load model cards
- Use React.memo for optimization

### Risk 2: Data Maintenance
**Risk**: Model catalog needs regular updates
**Mitigation**:
- Structure data for easy updates
- Consider admin interface later
- Version control for model data

### Risk 3: Information Overload
**Risk**: Too many models may overwhelm users
**Mitigation**:
- Good search and filtering
- Group by provider/category
- Highlight popular/recommended models

## Migration Plan

### Phase 1: Data Structure (Day 1)
1. Create model catalog JSON structure
2. Populate with 100+ models
3. Create model data models in backend

### Phase 2: Landing Page Showcase (Day 2-3)
1. Create ModelCard component
2. Create ModelGallery component
3. Create ModelSearch component
4. Integrate into landing page
5. Add styling

### Phase 3: Dashboard Integration (Day 4)
1. Create ModelSelector component
2. Update ApiCallInterface
3. Add search/filter functionality

### Phase 4: Backend API (Day 5)
1. Create model catalog service
2. Create API endpoint
3. Connect frontend to API

### Phase 5: Polish & Testing (Day 6)
1. Add model details view
2. Performance optimization
3. Testing and refinement

## Open Questions

1. **Model Availability**: Should we show availability status?
   - Recommendation: Start without, add later if needed

2. **Pricing Display**: Show exact pricing or just tiers?
   - Recommendation: Show pricing tiers initially, exact pricing later

3. **Model Images/Icons**: Use provider logos or model-specific icons?
   - Recommendation: Provider logos with model name

4. **Favorites/Recent**: Track user's favorite or recently used models?
   - Recommendation: Add later as enhancement

