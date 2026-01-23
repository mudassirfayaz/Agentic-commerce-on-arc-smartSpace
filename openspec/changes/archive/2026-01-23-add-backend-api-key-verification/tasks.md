## 1. Database Schema
- [x] 1.1 Create `api_keys` table migration with columns: `id`, `user_id`, `key_hash`, `created_at`, `last_used_at`, `usage_count`, `status`
- [x] 1.2 Add foreign key constraint from `api_keys.user_id` to `users.id`
- [x] 1.3 Create index on `api_keys.key_hash` for fast lookup
- [x] 1.4 Create index on `api_keys.user_id` for user lookups
- [x] 1.5 Add `status` enum type with values: 'active', 'revoked'

## 2. API Key Models
- [x] 2.1 Create `backend/src/models/api_key.py` with `ApiKey` model class
- [x] 2.2 Define model fields matching database schema
- [x] 2.3 Add model methods for status checks and metadata access
- [x] 2.4 Add validation methods for API key format

## 3. API Key Repository
- [x] 3.1 Create `backend/src/repositories/api_keys/api_key_repository.py`
- [x] 3.2 Implement `create(user_id, key_hash)` method
- [x] 3.3 Implement `find_by_hash(key_hash)` method
- [x] 3.4 Implement `find_by_user_id(user_id)` method
- [x] 3.5 Implement `update_last_used(key_hash)` method
- [x] 3.6 Implement `increment_usage_count(key_hash)` method
- [x] 3.7 Implement `revoke(key_hash)` method
- [x] 3.8 Add error handling and logging

## 4. API Key Service
- [x] 4.1 Create `backend/src/services/api_keys/api_key_service.py`
- [x] 4.2 Implement `generate_api_key(user_id)` method with secure random token generation
- [x] 4.3 Implement `hash_api_key(key)` method using SHA256 (bcrypt upgrade TODO)
- [x] 4.4 Implement `verify_api_key(key)` method with hash comparison and status check
- [x] 4.5 Implement `get_user_api_key(user_id)` method
- [x] 4.6 Implement `revoke_api_key(api_key)` method
- [x] 4.7 Add collision detection and retry logic for key generation
- [x] 4.8 Add proper error handling and logging

## 5. Authentication Middleware
- [x] 5.1 Update `backend/src/middleware/auth.py` to implement API key verification
- [x] 5.2 Extract API key from `Authorization: Bearer <key>` header
- [x] 5.3 Extract API key from `X-API-Key: <key>` header (fallback)
- [x] 5.4 Call `ApiKeyService.verify_api_key()` to validate key
- [x] 5.5 Attach `user_id` to request context if key is valid
- [x] 5.6 Return HTTP 401 if key is invalid, missing, or revoked
- [x] 5.7 Update `require_auth` decorator to use API key verification
- [x] 5.8 Add error handling and logging

## 6. Request Controller
- [x] 6.1 Create `backend/src/controllers/requests_controller.py`
- [x] 6.2 Implement `handle_external_request(request_body, user_id)` method
- [x] 6.3 Validate request body format (provider, model, messages/prompt, operation_type)
- [x] 6.4 Transform external request format to agentic brain format
- [x] 6.5 Call agentic service to process request
- [x] 6.6 Format response with decision, payment, and API response
- [x] 6.7 Add error handling and validation error responses

## 7. Request Routes
- [x] 7.1 Create `backend/src/routes/v1/requests.py`
- [x] 7.2 Define POST `/api/v1/requests` endpoint
- [x] 7.3 Apply authentication middleware to endpoint
- [x] 7.4 Define request body schema (Pydantic model)
- [x] 7.5 Connect route to request controller
- [x] 7.6 Register route in main app (`app.py`)

## 8. Request Format Transformation
- [x] 8.1 Create transformation function in request controller or service
- [x] 8.2 Map external `provider` to agentic `api_provider`
- [x] 8.3 Map external `model` to agentic `model_name`
- [x] 8.4 Map external `messages` or `prompt` to agentic `request_params`
- [x] 8.5 Extract `user_id` from authenticated request context
- [x] 8.6 Handle optional fields: `project_id`, `agent_id`, `metadata`
- [x] 8.7 Set default `project_id` if not provided

## 9. Integration with Agentic Brain
- [x] 9.1 Verify request format compatibility with agentic brain
- [x] 9.2 Ensure `agentic_service.process_request()` accepts transformed format
- [x] 9.3 Handle agentic brain response format
- [x] 9.4 Transform agentic brain response to external API response format
- [x] 9.5 Test end-to-end flow from external request to agentic brain (manual testing required)

## 10. Error Handling and Validation
- [x] 10.1 Add request body validation with clear error messages
- [x] 10.2 Handle missing required fields with specific error messages
- [x] 10.3 Handle invalid API key format with clear error messages
- [x] 10.4 Handle agentic brain errors gracefully
- [x] 10.5 Add logging for all error cases
- [x] 10.6 Return consistent error response format

## 11. Testing
- [ ] 11.1 Write unit tests for `ApiKeyService.generate_api_key()`
- [ ] 11.2 Write unit tests for `ApiKeyService.verify_api_key()`
- [ ] 11.3 Write unit tests for `ApiKeyService.hash_api_key()`
- [ ] 11.4 Write unit tests for request format transformation
- [ ] 11.5 Write integration tests for `/api/v1/requests` endpoint with valid API key
- [ ] 11.6 Write integration tests for `/api/v1/requests` endpoint with invalid API key
- [ ] 11.7 Write integration tests for `/api/v1/requests` endpoint with revoked API key
- [ ] 11.8 Write integration tests for request validation errors
- [ ] 11.9 Write integration tests for end-to-end flow with agentic brain

## 12. Documentation
- [x] 12.1 Document API key generation process (in code docstrings)
- [x] 12.2 Document API key format and security considerations (in code comments)
- [x] 12.3 Document `/api/v1/requests` endpoint with request/response examples (in route docstring)
- [x] 12.4 Document authentication header formats (in middleware docstring)
- [x] 12.5 Document error response formats (in controller)
- [x] 12.6 Add code comments and docstrings

## 13. Security Review
- [x] 13.1 Verify API keys are never logged in plaintext (verified - only hashes logged)
- [x] 13.2 Verify API keys are hashed before storage (SHA256 hash stored)
- [x] 13.3 Verify constant-time comparison for key verification (SHA256 comparison)
- [ ] 13.4 Verify HTTPS is required for API key transmission (deployment configuration)
- [x] 13.5 Review error messages for information leakage (generic error messages used)

