# Change: Add Backend API Key Creation and Verification

## Why
Users need to make API requests from their local files or live applications using the request library (e.g., Python `requests`, JavaScript `fetch`, curl). Currently, the backend has no mechanism to:
1. Generate and store API keys for users
2. Verify API keys from incoming requests
3. Authenticate external API requests from users' applications
4. Route authenticated requests to the agentic brain for processing

Without this functionality, users cannot programmatically access SmartSpace services from their own code, which is a core use case for the platform. The existing `add-api-key-management` change handles the frontend UI, but the backend infrastructure for API key generation, storage, and verification is missing.

## What Changes
- Add API key generation service that creates secure, unique API keys for users
- Implement API key storage in database with user association
- Create API key verification middleware that validates API keys from request headers
- Add public API endpoint (`/api/v1/requests`) that accepts authenticated requests from external applications
- Implement request transformation from external API format to agentic brain format
- Add API key lookup and validation logic
- Support both `Authorization: Bearer <api_key>` and `X-API-Key: <api_key>` header formats
- Add API key metadata tracking (creation date, last used, usage count)
- Integrate API key authentication with existing agentic brain request processing flow

## Impact
- Affected specs: backend-api-keys (new capability)
- Affected code:
  - `backend/src/services/api_keys/api_key_service.py` - New service for API key generation and management
  - `backend/src/repositories/api_keys/api_key_repository.py` - New repository for API key data access
  - `backend/src/models/api_key.py` - New model for API key data structure
  - `backend/src/middleware/auth.py` - MODIFIED to implement API key verification
  - `backend/src/routes/v1/requests.py` - New route for external API requests
  - `backend/src/controllers/requests_controller.py` - New controller for request handling
  - `backend/src/services/agentic/agentic_service.py` - May need updates for request format transformation
  - Database schema - New `api_keys` table
- Breaking changes: None (additive only)
- Dependencies: Requires database layer to be implemented (from `restructure-backend-architecture`)

