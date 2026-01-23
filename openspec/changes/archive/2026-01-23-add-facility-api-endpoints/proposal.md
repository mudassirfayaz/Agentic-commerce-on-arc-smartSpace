# Change: Add Facility-Specific API Endpoints for Core Request Flow

## Why
Currently, the backend only provides a generic `/api/v1/requests` endpoint that requires users to specify provider and model in a custom format. However, SmartSpace's core value proposition is providing a unified API interface similar to OpenAI's API pattern, where users can make requests to facility-specific endpoints (e.g., `/v1/text/completion`, `/v1/audio/speech`) with a simple, intuitive request format. The landing page already advertises these endpoints, but they don't exist yet. Without these facility-specific endpoints, users cannot complete the main function of the app - making API requests through the unified SmartSpace interface.

## What Changes
- Add facility-specific API endpoints matching the advertised pattern:
  - `POST /v1/text/completion` - Text completion requests
  - `POST /v1/audio/speech` - Audio/speech generation requests
  - `POST /v1/images/generate` - Image generation requests
  - `POST /v1/embeddings` - Embedding generation requests
  - `POST /v1/vision/analyze` - Vision/image analysis requests
- Implement request format transformation from facility-specific format to agentic brain format
- Add model/provider resolution logic to map model names (e.g., "openai/tts-1") to provider and model
- Ensure complete end-to-end flow: API key auth → request validation → agentic brain processing → payment → provider API call → response
- Add request validation for each facility type
- Update API documentation to reflect new endpoints
- Optionally add frontend testing interface for these endpoints

## Impact
- Affected specs: backend-api-endpoints (new capability), backend-request-processing (MODIFIED)
- Affected code:
  - `backend/src/routes/v1/text.py` - New text completion endpoint
  - `backend/src/routes/v1/audio.py` - New audio/speech endpoint
  - `backend/src/routes/v1/images.py` - New image generation endpoint
  - `backend/src/routes/v1/embeddings.py` - New embeddings endpoint
  - `backend/src/routes/v1/vision.py` - New vision endpoint
  - `backend/src/controllers/facility_controller.py` - New controller for facility-specific requests
  - `backend/src/services/model_resolver.py` - New service to resolve model names to provider/model
  - `backend/src/utils/request_transformers.py` - Request format transformers
  - `backend/app.py` - Register new routes
  - `frontend/src/components/Dashboard/ApiCallInterface.jsx` - Update to use new endpoints (optional)
- Breaking changes: None (additive only, existing `/api/v1/requests` endpoint remains)

