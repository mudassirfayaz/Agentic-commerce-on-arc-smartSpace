## 1. Backend API Key Management Endpoints

- [ ] 1.1 Create `backend/src/controllers/api_keys_controller.py` with `ApiKeyController` class
- [ ] 1.2 Implement `get_user_api_key()` method to retrieve user's API key metadata
- [ ] 1.3 Implement `generate_api_key()` method to create new API key for user
- [ ] 1.4 Implement `revoke_api_key()` method to revoke user's API key (optional)
- [ ] 1.5 Add error handling for edge cases (user already has key, generation failures)
- [ ] 1.6 Create `backend/src/routes/v1/api_keys.py` route file
- [ ] 1.7 Add `GET /api/v1/api-keys` endpoint (requires user authentication)
- [ ] 1.8 Add `POST /api/v1/api-keys` endpoint (requires user authentication)
- [ ] 1.9 Add `DELETE /api/v1/api-keys` endpoint (optional, for future use)
- [ ] 1.10 Implement user authentication placeholder (e.g., `X-User-ID` header for MVP, or session-based auth)
- [ ] 1.11 Register API keys router in `backend/app.py`
- [ ] 1.12 Add request/response models using Pydantic for API key endpoints
- [ ] 1.13 Add proper error responses (404 for no key, 409 for conflict, etc.)

## 2. Integration and Testing

- [ ] 2.1 Test API key generation endpoint with valid user ID
- [ ] 2.2 Test API key retrieval endpoint with existing key
- [ ] 2.3 Test API key retrieval endpoint when no key exists (should return 404)
- [ ] 2.4 Test API key generation when user already has active key (should handle appropriately)
- [ ] 2.5 Test error handling for invalid user IDs
- [ ] 2.6 Verify plaintext key is only returned in POST response (not in GET)
- [ ] 2.7 Test API key revocation endpoint (if implemented)
- [ ] 2.8 Update frontend API calls to use correct endpoint URLs and authentication headers

## 3. Documentation

- [ ] 3.1 Add OpenAPI/Swagger documentation for new endpoints
- [ ] 3.2 Document authentication requirements for API key management endpoints
- [ ] 3.3 Document response formats and error codes
- [ ] 3.4 Update backend README with API key management endpoint information

