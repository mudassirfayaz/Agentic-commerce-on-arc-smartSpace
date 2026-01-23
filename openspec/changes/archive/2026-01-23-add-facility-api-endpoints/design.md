# Design: Facility-Specific API Endpoints

## Context

SmartSpace needs to provide facility-specific API endpoints that match the pattern advertised on the landing page. Users should be able to make requests like:

```python
import requests

url = "https://smartspace.ai/v1/text/completion"
headers = {
    "Authorization": "Bearer smartspace234lkjpoij;lkjljasdfij234ljkls"
}
payload = {
    "model": "openai/tts-1",
    "text": "Hello, world!",
    "voice": "nova"
}

response = requests.post(url, headers=headers, json=payload)
```

This is different from the current generic `/api/v1/requests` endpoint which requires:
```json
{
  "provider": "openai",
  "model": "tts-1",
  "operation_type": "audio",
  "request_params": {...}
}
```

## Goals

1. **Unified API Interface**: Provide OpenAI-like API endpoints that are intuitive and familiar
2. **Facility-Specific Endpoints**: Each AI capability (text, audio, images, embeddings, vision) has its own endpoint
3. **Model Name Resolution**: Support model names like "openai/tts-1" that automatically resolve to provider and model
4. **Backward Compatibility**: Keep existing `/api/v1/requests` endpoint for advanced users
5. **Complete Flow**: Ensure full end-to-end processing through agentic brain

## Non-Goals

- Changing the agentic brain processing logic (it already works)
- Modifying the payment or decision engine (they're already functional)
- Supporting all possible OpenAI API parameters (start with core ones)

## Architecture

### Request Flow

```
External User Application
  │
  │ POST /v1/text/completion
  │ Authorization: Bearer sk-...
  │ Body: {model: "openai/tts-1", text: "...", voice: "nova"}
  │
  ▼
Facility-Specific Route (e.g., /v1/text/completion)
  │
  │ 1. Extract API key from headers
  │
  ▼
API Key Verification Middleware
  │
  │ 2. Verify API key → user_id
  │
  ▼
Facility Controller
  │
  │ 3. Validate facility-specific request format
  │ 4. Resolve model name (e.g., "openai/tts-1" → provider: "openai", model: "tts-1")
  │ 5. Transform to agentic brain format
  │
  ▼
Agentic Service
  │
  │ 6. Call brain.process_request()
  │
  ▼
Agentic Brain
  │
  │ 7. Process request (decision, payment, API call)
  │
  ▼
Facility Controller
  │
  │ 8. Transform response to facility-specific format
  │
  ▼
External User Application
```

### Model Name Resolution

Model names follow the pattern: `{provider}/{model}`

Examples:
- `openai/tts-1` → provider: `openai`, model: `tts-1`
- `anthropic/claude-3` → provider: `anthropic`, model: `claude-3`
- `ollama/qalb-urdu` → provider: `ollama`, model: `qalb-urdu`

The resolver:
1. Splits on `/` to extract provider and model
2. Validates provider is supported
3. Validates model exists for that provider
4. Returns structured provider/model info

### Request Format Transformation

Each facility has its own request format that needs to be transformed to the agentic brain format:

**Text Completion** (`/v1/text/completion`):
```json
{
  "model": "openai/gpt-4",
  "text": "Hello, world!",
  "max_tokens": 100,
  "temperature": 0.7
}
```
→ Transforms to agentic format with `operation_type: "completion"`

**Audio/Speech** (`/v1/audio/speech`):
```json
{
  "model": "openai/tts-1",
  "text": "Hello, world!",
  "voice": "nova"
}
```
→ Transforms to agentic format with `operation_type: "audio"`

**Images** (`/v1/images/generate`):
```json
{
  "model": "openai/dall-e-3",
  "prompt": "A beautiful sunset",
  "size": "1024x1024"
}
```
→ Transforms to agentic format with `operation_type: "image"`

**Embeddings** (`/v1/embeddings`):
```json
{
  "model": "openai/text-embedding-ada-002",
  "input": "Hello, world!"
}
```
→ Transforms to agentic format with `operation_type: "embedding"`

**Vision** (`/v1/vision/analyze`):
```json
{
  "model": "openai/gpt-4-vision",
  "image": "base64_encoded_image",
  "prompt": "What's in this image?"
}
```
→ Transforms to agentic format with `operation_type: "vision"`

## Decisions

### Decision 1: Endpoint Structure
**What**: Use `/v1/{facility}/{operation}` pattern
**Why**: 
- Matches OpenAI's pattern (familiar to users)
- Clear separation of concerns
- Easy to extend with new facilities
**Alternatives considered**:
- Single endpoint with facility parameter: Less intuitive, harder to document
- `/api/v1/{facility}`: Redundant `/api` prefix

### Decision 2: Model Name Format
**What**: Use `{provider}/{model}` format
**Why**:
- Clear and unambiguous
- Easy to parse
- Supports multiple providers
**Alternatives considered**:
- Provider in header: Less discoverable
- Separate provider field: More verbose

### Decision 3: Request Transformation Layer
**What**: Transform facility-specific format to agentic brain format in controller
**Why**:
- Keeps agentic brain interface stable
- Allows different request formats per facility
- Centralized transformation logic
**Alternatives considered**:
- Modify agentic brain to accept multiple formats: Breaks separation of concerns
- Transform in route handler: Less reusable

### Decision 4: Response Format
**What**: Return facility-specific response format (similar to OpenAI)
**Why**:
- Familiar to users
- Consistent with request format
- Easy to integrate
**Alternatives considered**:
- Return agentic brain format directly: Too complex for external users

## Risks / Trade-offs

### Risk 1: Model Name Ambiguity
**Risk**: Same model name could exist for multiple providers
**Mitigation**: Use `{provider}/{model}` format to disambiguate

### Risk 2: Provider/Model Validation
**Risk**: Invalid provider/model combinations
**Mitigation**: Validate against known provider/model mappings

### Risk 3: Request Format Complexity
**Risk**: Different facilities have different required fields
**Mitigation**: Use Pydantic models for validation per facility

### Risk 4: Backward Compatibility
**Risk**: Existing users using `/api/v1/requests` might break
**Mitigation**: Keep existing endpoint, new endpoints are additive

## Implementation Plan

1. Create model resolver service
2. Create request transformers for each facility
3. Create facility-specific routes
4. Create facility controller
5. Integrate with existing agentic service
6. Add validation and error handling
7. Update API documentation

## Open Questions

- Should we support all OpenAI API parameters or just core ones? (Start with core)
- How to handle provider-specific parameters? (Pass through in metadata)
- Should responses match OpenAI format exactly? (Start similar, can evolve)

