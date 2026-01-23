# Backend API Key Creation and Verification - Design Document

## Context

Users need to make API requests to SmartSpace from their own applications (Python scripts, web apps, command-line tools, etc.) using standard HTTP libraries. The backend must:
1. Generate secure API keys for users
2. Store API keys securely with user association
3. Verify API keys from incoming requests
4. Route authenticated requests to the agentic brain for processing

Currently, the backend has:
- Basic authentication middleware skeleton (`src/middleware/auth.py`) with TODO comments
- Agentic brain integration service (`src/services/agentic/agentic_service.py`)
- No API key generation or storage mechanism
- No public API endpoint for external requests

## Goals / Non-Goals

### Goals
- Enable users to make authenticated API requests from external applications
- Generate cryptographically secure API keys
- Store API keys securely with proper user association
- Verify API keys efficiently (low latency)
- Support standard authentication header formats
- Track API key usage for analytics and security
- Integrate seamlessly with existing agentic brain processing flow

### Non-Goals
- API key rotation/revocation UI (handled by frontend change)
- Rate limiting per API key (can be added later)
- API key scoping/permissions (single key per user for now)
- OAuth or JWT tokens (API keys only for this change)

## Decisions

### Decision 1: API Key Format
**What**: Use prefixed, URL-safe base64-encoded random tokens
- Format: `sk-<random_32_bytes_base64>` (e.g., `sk-AbCdEf1234567890XyZwVuTsRqPoNmLkJiHgFeDcBa`)
- Length: ~48 characters total (4 char prefix + 44 char token)
- Encoding: Base64 URL-safe (no padding)

**Why**:
- `sk-` prefix clearly identifies SmartSpace API keys
- 32 bytes (256 bits) provides sufficient entropy for security
- Base64 URL-safe encoding is standard and works in headers/URLs
- Short enough to be user-friendly, long enough to be secure

**Alternatives considered**:
- UUID format: Less user-friendly, no prefix for identification
- JWT tokens: Overkill for simple API key use case, requires secret management
- Opaque tokens without prefix: Harder to identify and debug

### Decision 2: API Key Storage
**What**: Store API keys in database with:
- Hashed key value (never store plaintext)
- User ID association
- Creation timestamp
- Last used timestamp
- Usage count
- Active/revoked status

**Why**:
- Database storage enables efficient lookup and user association
- Hashing prevents key exposure if database is compromised
- Metadata enables usage tracking and security monitoring
- Status field enables key revocation

**Alternatives considered**:
- Plaintext storage: Security risk if database is compromised
- External key management service: Overkill for current scale
- In-memory storage: Not persistent, doesn't scale

### Decision 3: API Key Hashing
**What**: Use bcrypt or Argon2 for hashing API keys
- Salt per key (automatic with bcrypt/Argon2)
- Cost factor appropriate for API key verification frequency
- Store hash in database, compare on verification

**Why**:
- Industry standard for password/key hashing
- Resistant to rainbow table attacks
- Configurable cost factor for security vs performance trade-off

**Alternatives considered**:
- SHA-256: Fast but vulnerable to brute force if salt is known
- Plaintext comparison: Major security risk

### Decision 4: Authentication Header Format
**What**: Support both formats:
1. `Authorization: Bearer <api_key>` (standard OAuth-style)
2. `X-API-Key: <api_key>` (explicit API key header)

**Why**:
- `Authorization: Bearer` is standard and widely supported
- `X-API-Key` is explicit and common in API key systems
- Supporting both maximizes compatibility with different client libraries

**Alternatives considered**:
- Only `Authorization: Bearer`: Less explicit, some tools expect `X-API-Key`
- Only `X-API-Key`: Non-standard, less compatible with OAuth-style tools

### Decision 5: API Key Verification Flow
**What**: Verification process:
1. Extract API key from request headers (try both formats)
2. Look up API key hash in database
3. Compare provided key with stored hash using bcrypt/Argon2
4. Check key status (active/revoked)
5. Update last used timestamp and usage count
6. Return user_id for request processing

**Why**:
- Efficient lookup by key hash (indexed database column)
- Secure comparison using constant-time hashing
- Metadata updates enable usage tracking
- Status check prevents use of revoked keys

**Alternatives considered**:
- In-memory cache: Faster but not persistent, adds complexity
- JWT verification: Requires secret management, overkill for simple keys

### Decision 6: Request Endpoint Design
**What**: Create `/api/v1/requests` endpoint that:
- Accepts POST requests with API key authentication
- Accepts request body in format compatible with agentic brain
- Transforms external request format to internal format if needed
- Returns response in consistent format with decision, payment, and API response

**Why**:
- RESTful endpoint design
- Versioned API (`/v1/`) enables future changes
- Clear separation from internal endpoints
- Compatible with standard HTTP libraries

**Alternatives considered**:
- GraphQL endpoint: Overkill for current needs
- Multiple endpoints per operation: More complex, less RESTful

### Decision 7: Request Format Transformation
**What**: Accept request body with fields:
- `provider`: API provider name (e.g., "ollama", "openai")
- `model`: Model name (e.g., "deepseek-r1", "gpt-4")
- `messages` or `prompt`: Request content
- `operation_type`: Type of operation (e.g., "chat", "completion")
- Optional: `project_id`, `agent_id`, `metadata`

Transform to agentic brain `APIRequest` format internally.

**Why**:
- Simple, intuitive format for external users
- Maps cleanly to agentic brain requirements
- Flexible enough for different use cases

**Alternatives considered**:
- Direct agentic brain format: Too complex for external users
- Provider-specific formats: Inconsistent, harder to maintain

## Architecture Flow

```
External User Application
  │
  │ POST /api/v1/requests
  │ Authorization: Bearer sk-...
  │ Body: {provider, model, messages, ...}
  │
  ▼
Backend API Layer
  │
  │ 1. Extract API key from headers
  │
  ▼
API Key Verification Middleware
  │
  │ 2. Look up key hash in database
  │ 3. Compare with bcrypt/Argon2
  │ 4. Check status (active/revoked)
  │ 5. Update last_used, usage_count
  │ 6. Return user_id
  │
  ▼
Request Controller
  │
  │ 7. Validate request body
  │ 8. Transform to agentic brain format
  │
  ▼
Agentic Service
  │
  │ 9. Call brain.process_request()
  │
  ▼
Agentic Brain
  │
  │ 10. Process request (decision, payment, API call)
  │
  ▼
Response
  │
  │ 11. Return decision, payment, response
  │
  ▼
External User Application
```

## Risks / Trade-offs

### Risk 1: API Key Security
**Risk**: API keys could be exposed or compromised
**Mitigation**:
- Hash keys in database (never store plaintext)
- Use HTTPS for all API requests
- Provide clear security documentation
- Support key revocation

### Risk 2: Performance Impact
**Risk**: Database lookup and bcrypt comparison adds latency
**Mitigation**:
- Index API key hash column for fast lookup
- Use appropriate bcrypt cost factor (balance security vs speed)
- Consider caching active keys in memory (future optimization)

### Risk 3: Key Collision
**Risk**: Two users could theoretically get the same API key
**Mitigation**:
- 32 bytes of entropy makes collision probability negligible
- Check for existing key before storing (defense in depth)

### Risk 4: Request Format Mismatch
**Risk**: External request format may not map cleanly to agentic brain format
**Mitigation**:
- Clear documentation of request format
- Validation and error messages for invalid requests
- Transformation layer handles format differences

## Migration Plan

### Phase 1: Database Schema
1. Create `api_keys` table with columns:
   - `id` (primary key)
   - `user_id` (foreign key to users)
   - `key_hash` (hashed API key)
   - `created_at` (timestamp)
   - `last_used_at` (timestamp, nullable)
   - `usage_count` (integer, default 0)
   - `status` (enum: active, revoked)
   - Index on `key_hash` for fast lookup

### Phase 2: API Key Service
1. Implement `ApiKeyService` with methods:
   - `generate_api_key(user_id)` → returns plaintext key (shown once)
   - `hash_api_key(key)` → returns hash for storage
   - `verify_api_key(key)` → returns user_id if valid, None otherwise
   - `revoke_api_key(key_hash)` → marks key as revoked
   - `get_user_api_key(user_id)` → returns key metadata

### Phase 3: Repository Layer
1. Implement `ApiKeyRepository` with database operations:
   - `create(user_id, key_hash)` → store new key
   - `find_by_hash(key_hash)` → lookup key by hash
   - `find_by_user_id(user_id)` → get user's key
   - `update_last_used(key_hash)` → update usage metadata
   - `revoke(key_hash)` → mark as revoked

### Phase 4: Authentication Middleware
1. Update `auth.py` middleware:
   - Extract API key from `Authorization: Bearer` or `X-API-Key` headers
   - Call `ApiKeyService.verify_api_key()`
   - Attach `user_id` to request context
   - Return 401 if key invalid or revoked

### Phase 5: Request Endpoint
1. Create `/api/v1/requests` route:
   - Apply authentication middleware
   - Accept POST requests with request body
   - Validate request format
   - Transform to agentic brain format
   - Call agentic service
   - Return response

### Phase 6: Integration
1. Connect to agentic brain:
   - Ensure request format compatibility
   - Handle agentic brain responses
   - Return consistent response format

## Open Questions

1. **API Key Expiration**: Should API keys expire automatically?
   - Recommendation: Not for initial implementation, add later if needed

2. **Key Regeneration**: What happens when user regenerates key?
   - Recommendation: Revoke old key, generate new one (handled by frontend change)

3. **Rate Limiting**: Should we add rate limiting per API key?
   - Recommendation: Add later if needed, focus on core functionality first

4. **Key Scoping**: Should keys have different permissions/scopes?
   - Recommendation: Single key per user for now, add scoping later if needed

5. **Request Size Limits**: Maximum request body size?
   - Recommendation: Use framework defaults (e.g., FastAPI default), document limits

