# Change: Add API Key Management Endpoints to Backend

## Why
The frontend API Keys page (`frontend/src/pages/ApiKeys.jsx`) attempts to call backend endpoints (`GET /api/v1/api-keys` and `POST /api/v1/api-keys`) that do not exist. While the backend has API key generation and verification services implemented (from `add-backend-api-key-verification`), there are no HTTP endpoints for users to create, view, or manage their API keys through the web application. Without these endpoints, users cannot generate API keys through the UI, which is a core requirement for the SmartSpace platform.

## What Changes
- Add `GET /api/v1/api-keys` endpoint to retrieve user's existing API key metadata
- Add `POST /api/v1/api-keys` endpoint to generate a new API key for the authenticated user
- Add `DELETE /api/v1/api-keys` endpoint to revoke user's API key (optional, for future use)
- Create `ApiKeyController` to handle API key management operations
- Create `api_keys.py` route file in `backend/src/routes/v1/`
- Implement user authentication for API key management endpoints (placeholder for MVP, proper session auth to be implemented separately)
- Integrate with existing `ApiKeyService` and `ApiKeyRepository`
- Return API key metadata (excluding plaintext key) for GET requests
- Return plaintext API key only once during generation (POST response)
- Handle error cases (user already has active key, generation failures, etc.)

## Impact
- Affected specs: backend-api-keys (MODIFIED - add management endpoints)
- Affected code:
  - `backend/src/routes/v1/api_keys.py` - New route file for API key management
  - `backend/src/controllers/api_keys_controller.py` - New controller for API key operations
  - `backend/app.py` - MODIFIED to register new API keys router
  - `backend/src/middleware/auth.py` - May need MODIFIED to add user session authentication (or placeholder)
- Breaking changes: None (additive only)
- Dependencies: 
  - Requires `ApiKeyService` and `ApiKeyRepository` (already implemented in `add-backend-api-key-verification`)
  - Requires user authentication mechanism (to be implemented as placeholder for MVP)

