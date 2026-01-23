# backend-api-keys Specification

## Purpose
TBD - created by archiving change add-backend-api-key-verification. Update Purpose after archive.
## Requirements
### Requirement: API Key Generation
The backend SHALL generate secure, unique API keys for users that can be used to authenticate external API requests.

#### Scenario: System generates API key for user
- **WHEN** a user requests an API key to be generated
- **THEN** the system SHALL generate a cryptographically secure random token
- **AND** the token SHALL be prefixed with `sk-` (e.g., `sk-AbCdEf1234567890XyZwVuTsRqPoNmLkJiHgFeDcBa`)
- **AND** the token SHALL be approximately 48 characters in length (4 character prefix + 44 character base64-encoded token)
- **AND** the token SHALL be base64 URL-safe encoded (no padding)
- **AND** the system SHALL hash the API key using bcrypt or Argon2 before storage
- **AND** the system SHALL store the hashed key in the database with user association
- **AND** the system SHALL return the plaintext key only once (for user to copy)
- **AND** the system SHALL never store the plaintext key

#### Scenario: API key is unique
- **WHEN** the system generates an API key
- **THEN** the system SHALL verify the key does not already exist in the database
- **AND** if a collision is detected, the system SHALL generate a new key
- **AND** the system SHALL continue until a unique key is generated

### Requirement: API Key Storage
The backend SHALL store API keys securely in the database with proper user association and metadata.

#### Scenario: API key stored with user association
- **WHEN** an API key is generated for a user
- **THEN** the system SHALL store the hashed key in the `api_keys` table
- **AND** the record SHALL include the `user_id` as a foreign key
- **AND** the record SHALL include a `created_at` timestamp
- **AND** the record SHALL include `last_used_at` timestamp (initially NULL)
- **AND** the record SHALL include `usage_count` (initially 0)
- **AND** the record SHALL include `status` field set to "active"
- **AND** the `key_hash` column SHALL be indexed for fast lookup

#### Scenario: API key metadata tracking
- **WHEN** an API key is used for authentication
- **THEN** the system SHALL update the `last_used_at` timestamp
- **AND** the system SHALL increment the `usage_count` counter
- **AND** the updates SHALL be atomic to prevent race conditions

### Requirement: API Key Verification
The backend SHALL verify API keys from incoming requests and authenticate users based on valid keys.

#### Scenario: API key extracted from Authorization header
- **WHEN** a request includes `Authorization: Bearer <api_key>` header
- **THEN** the system SHALL extract the API key from the header
- **AND** the system SHALL look up the key hash in the database
- **AND** the system SHALL compare the provided key with the stored hash using bcrypt/Argon2
- **AND** if the key matches and status is "active", the system SHALL authenticate the request
- **AND** the system SHALL attach the associated `user_id` to the request context

#### Scenario: API key extracted from X-API-Key header
- **WHEN** a request includes `X-API-Key: <api_key>` header
- **THEN** the system SHALL extract the API key from the header
- **AND** the system SHALL perform the same verification process as Authorization header
- **AND** the system SHALL support both header formats for compatibility

#### Scenario: Invalid API key rejected
- **WHEN** a request includes an invalid API key (wrong format, not found, or revoked)
- **THEN** the system SHALL return HTTP 401 Unauthorized
- **AND** the response SHALL include an error message indicating authentication failed
- **AND** the system SHALL NOT process the request further

#### Scenario: Revoked API key rejected
- **WHEN** a request includes an API key with status "revoked"
- **THEN** the system SHALL return HTTP 401 Unauthorized
- **AND** the response SHALL indicate the key has been revoked
- **AND** the system SHALL NOT process the request

### Requirement: External API Request Endpoint
The backend SHALL provide a public API endpoint that accepts authenticated requests from external applications and processes them through the agentic brain.

#### Scenario: External request with valid API key
- **WHEN** a POST request is made to `/api/v1/requests` with a valid API key
- **AND** the request body includes required fields: `provider`, `model`, `messages` (or `prompt`), `operation_type`
- **THEN** the system SHALL authenticate the request using the API key
- **AND** the system SHALL validate the request body format
- **AND** the system SHALL transform the external request format to agentic brain format
- **AND** the system SHALL call the agentic brain `process_request()` method
- **AND** the system SHALL return the response with decision, payment details, and API response

#### Scenario: External request format validation
- **WHEN** a POST request is made to `/api/v1/requests` with invalid or missing required fields
- **THEN** the system SHALL return HTTP 400 Bad Request
- **AND** the response SHALL include error details indicating which fields are invalid or missing
- **AND** the system SHALL NOT process the request

#### Scenario: External request response format
- **WHEN** an external request is successfully processed
- **THEN** the response SHALL include:
  - `success`: boolean indicating if request was approved
  - `decision`: object with outcome, reasoning, confidence
  - `response`: API response from provider (if approved)
  - `payment`: payment details including transaction hash, amount, variance
  - `message`: human-readable status message
- **AND** the response SHALL be in JSON format
- **AND** the response SHALL use consistent structure for all requests

#### Scenario: External request error handling
- **WHEN** an external request fails due to agentic brain error, network error, or other system error
- **THEN** the system SHALL return HTTP 500 Internal Server Error
- **AND** the response SHALL include an error message (without exposing internal details)
- **AND** the system SHALL log the full error details for debugging

### Requirement: Request Format Transformation
The backend SHALL transform external API request format to the internal agentic brain format.

#### Scenario: Transform external request to agentic format
- **WHEN** an external request is received with format:
  ```json
  {
    "provider": "ollama",
    "model": "deepseek-r1",
    "messages": [{"role": "user", "content": "Hello"}],
    "operation_type": "chat"
  }
  ```
- **THEN** the system SHALL transform it to agentic brain `APIRequest` format
- **AND** the system SHALL extract `user_id` from authenticated API key context
- **AND** the system SHALL set `project_id` from request or user default
- **AND** the system SHALL map `provider` to `api_provider`
- **AND** the system SHALL map `model` to `model_name`
- **AND** the system SHALL map `messages` or `prompt` to `request_params`
- **AND** the system SHALL set `operation_type` appropriately

#### Scenario: Handle optional fields in external request
- **WHEN** an external request includes optional fields: `project_id`, `agent_id`, `metadata`
- **THEN** the system SHALL include these fields in the transformed request
- **AND** if `project_id` is not provided, the system SHALL use the user's default project
- **AND** if `agent_id` is not provided, the system SHALL set it to NULL

### Requirement: API Key Service Interface
The backend SHALL provide a service interface for API key operations that can be used by other services and controllers.

#### Scenario: Generate API key via service
- **WHEN** `ApiKeyService.generate_api_key(user_id)` is called
- **THEN** the service SHALL generate a secure random token
- **AND** the service SHALL hash the token
- **AND** the service SHALL store the hash in the database via repository
- **AND** the service SHALL return the plaintext key (for one-time display)
- **AND** the service SHALL return key metadata (creation date, etc.)

#### Scenario: Verify API key via service
- **WHEN** `ApiKeyService.verify_api_key(api_key)` is called
- **THEN** the service SHALL look up the key hash in the database
- **AND** the service SHALL compare the provided key with stored hash
- **AND** the service SHALL check the key status (active/revoked)
- **AND** if valid, the service SHALL update `last_used_at` and `usage_count`
- **AND** the service SHALL return the associated `user_id` if valid, or `None` if invalid

#### Scenario: Get user API key via service
- **WHEN** `ApiKeyService.get_user_api_key(user_id)` is called
- **THEN** the service SHALL look up the user's active API key in the database
- **AND** the service SHALL return key metadata (creation date, last used, usage count, status)
- **AND** the service SHALL NOT return the plaintext key (security)
- **AND** if no key exists, the service SHALL return `None`

#### Scenario: Revoke API key via service
- **WHEN** `ApiKeyService.revoke_api_key(api_key)` is called
- **THEN** the service SHALL look up the key in the database
- **AND** the service SHALL update the key status to "revoked"
- **AND** the service SHALL prevent future use of the revoked key
- **AND** the service SHALL return success status

