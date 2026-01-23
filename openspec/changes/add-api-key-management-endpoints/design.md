## Context

The frontend has an API Keys management page that needs to communicate with backend endpoints to:
1. Fetch existing API key metadata (GET)
2. Generate new API keys (POST)
3. Revoke API keys (DELETE, optional)

The backend already has:
- `ApiKeyService` with `generate_api_key()`, `get_user_api_key()`, and `revoke_api_key()` methods
- `ApiKeyRepository` for database operations
- API key verification middleware for authenticating external requests

What's missing:
- HTTP endpoints for the web application to call
- User authentication mechanism for web application requests (different from API key auth)

## Goals / Non-Goals

### Goals
- Provide RESTful endpoints for API key management
- Integrate with existing `ApiKeyService` and `ApiKeyRepository`
- Support frontend API Keys page functionality
- Return plaintext key only once during generation
- Return metadata (not plaintext) for GET requests

### Non-Goals
- Implement full session-based authentication system (use placeholder for MVP)
- Support multiple API keys per user (single key per user for MVP)
- Implement API key rotation or expiration policies
- Add rate limiting or advanced security features (deferred)

## Decisions

### Decision: User Authentication Placeholder
**What**: Use a simple `X-User-ID` header for MVP authentication of API key management endpoints.

**Why**: 
- Full session-based authentication is a larger change that should be implemented separately
- MVP needs a way to identify the user making the request
- Simple header-based approach allows frontend to pass user ID from session/cookie
- Can be replaced with proper JWT/session auth later without changing endpoint signatures

**Alternatives considered**:
1. **JWT tokens**: More secure but requires implementing JWT infrastructure
2. **Session cookies**: Requires session management middleware
3. **API key auth**: Circular dependency (need API key to get API key)

**Implementation**: 
- Add `get_user_id_from_header()` dependency in `auth.py`
- Extract `X-User-ID` header from requests
- Validate user exists (optional for MVP)
- Pass `user_id` to controller methods

### Decision: Single API Key Per User
**What**: Allow only one active API key per user.

**Why**: 
- Simpler implementation for MVP
- Matches SmartSpace value proposition ("one API key for all models")
- `ApiKeyService.generate_api_key()` already checks for existing keys

**Implementation**: 
- `ApiKeyService` returns `(None, metadata)` if user already has active key
- Controller checks for existing key and returns appropriate response
- Frontend can show "regenerate" option if key exists

### Decision: Plaintext Key Return Strategy
**What**: Return plaintext API key only in POST response, never in GET responses.

**Why**: 
- Security best practice: keys should only be shown once during generation
- GET requests return metadata only (creation date, last used, etc.)
- Matches frontend expectations (frontend shows warning "key will only be shown once")

**Implementation**:
- POST `/api/v1/api-keys` returns `{"api_key": "sk-...", "metadata": {...}}`
- GET `/api/v1/api-keys` returns `{"metadata": {...}}` (no `api_key` field)

## Risks / Trade-offs

### Risk: Placeholder Authentication is Insecure
**Mitigation**: 
- Document this as MVP-only approach
- Add TODO comments for proper authentication
- Implement proper session/JWT auth in separate change
- Add validation that user ID exists in database (optional for MVP)

### Risk: Frontend-Backend Authentication Mismatch
**Mitigation**: 
- Coordinate with frontend team on header name (`X-User-ID`)
- Document authentication approach in proposal
- Consider using environment variable for header name

### Trade-off: Single Key vs Multiple Keys
**Decision**: Single key for MVP, can be extended later if needed.

## Migration Plan

1. **Phase 1**: Implement endpoints with placeholder authentication
2. **Phase 2**: Test with frontend integration
3. **Phase 3**: Replace placeholder with proper session/JWT authentication (separate change)

## Open Questions

- Should we validate that the user ID exists in the database? (For MVP, can skip)
- Should we add rate limiting to prevent API key generation abuse? (Deferred)
- Should we support API key regeneration (revoke old + create new in one call)? (Deferred, can use DELETE + POST)

