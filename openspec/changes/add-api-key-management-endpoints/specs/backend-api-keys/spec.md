## MODIFIED Requirements

### Requirement: API Key Generation
The backend SHALL generate secure, unique API keys for users that can be used to authenticate external API requests.

#### Scenario: System generates API key for user
- **WHEN** a user requests an API key to be generated
- **THEN** the system SHALL generate a cryptographically secure random token
- **AND** the token SHALL be prefixed with `sk-` (e.g., `sk-AbCdEf1234567890XyZwVuTsRqPoNmLkJiHgFeDcBa`)
- **AND** the token SHALL be approximately 48 characters in length (4 character prefix + 44 character base64-encoded token)
- **AND** the token SHALL be base64 URL-safe encoded (no padding)
- **AND** the system SHALL hash the API key using SHA256 before storage
- **AND** the system SHALL store the hashed key in the database with user association
- **AND** the system SHALL return the plaintext key only once (for user to copy)
- **AND** the system SHALL never store the plaintext key

#### Scenario: API key is unique
- **WHEN** the system generates an API key
- **THEN** the system SHALL verify the key does not already exist in the database
- **AND** if a collision is detected, the system SHALL generate a new key
- **AND** the system SHALL continue until a unique key is generated

#### Scenario: User already has active API key
- **WHEN** a user requests API key generation and already has an active API key
- **THEN** the system SHALL return an appropriate response indicating an existing key
- **AND** the system SHALL allow the user to regenerate the key (revoking the old one)
- **OR** the system SHALL return the existing key metadata without generating a new key

## ADDED Requirements

### Requirement: API Key Management Endpoints
The backend SHALL provide HTTP endpoints for authenticated users to create, view, and manage their API keys through the web application.

#### Scenario: User retrieves API key metadata
- **WHEN** an authenticated user makes a GET request to `/api/v1/api-keys`
- **THEN** the system SHALL verify the user's authentication
- **AND** if the user has an active API key, the system SHALL return the key metadata (id, created_at, last_used_at, usage_count, status)
- **AND** the response SHALL NOT include the plaintext API key
- **AND** if the user has no API key, the system SHALL return HTTP 404 Not Found
- **AND** the response SHALL be in JSON format

#### Scenario: User generates new API key via endpoint
- **WHEN** an authenticated user makes a POST request to `/api/v1/api-keys`
- **THEN** the system SHALL verify the user's authentication
- **AND** the system SHALL check if the user already has an active API key
- **AND** if no active key exists, the system SHALL generate a new API key
- **AND** the system SHALL return the plaintext API key in the response (only time it's returned)
- **AND** the system SHALL return the key metadata along with the plaintext key
- **AND** if the user already has an active key, the system SHALL either:
  - Return HTTP 409 Conflict with existing key metadata, OR
  - Automatically revoke the old key and generate a new one
- **AND** the response SHALL be in JSON format with structure: `{"api_key": "sk-...", "metadata": {...}}`

#### Scenario: User revokes API key via endpoint
- **WHEN** an authenticated user makes a DELETE request to `/api/v1/api-keys`
- **THEN** the system SHALL verify the user's authentication
- **AND** if the user has an active API key, the system SHALL revoke it (set status to "revoked")
- **AND** the system SHALL return HTTP 200 OK with success message
- **AND** if the user has no active API key, the system SHALL return HTTP 404 Not Found
- **AND** after revocation, the API key SHALL no longer be valid for authentication

#### Scenario: Unauthenticated request to API key endpoints
- **WHEN** a request is made to `/api/v1/api-keys` without proper authentication
- **THEN** the system SHALL return HTTP 401 Unauthorized
- **AND** the response SHALL include an error message indicating authentication is required

#### Scenario: Invalid user ID in authentication
- **WHEN** a request includes an invalid or non-existent user ID in authentication
- **THEN** the system SHALL return HTTP 401 Unauthorized or HTTP 403 Forbidden
- **AND** the response SHALL indicate the authentication failed

### Requirement: User Authentication for API Key Management
The backend SHALL authenticate users for API key management endpoints using a mechanism that identifies the user making the request.

#### Scenario: User authentication via header
- **WHEN** a request is made to an API key management endpoint
- **THEN** the system SHALL extract the user identifier from the request (e.g., `X-User-ID` header for MVP)
- **AND** the system SHALL validate the user identifier
- **AND** if valid, the system SHALL proceed with the API key operation
- **AND** if invalid or missing, the system SHALL return HTTP 401 Unauthorized

#### Scenario: Authentication placeholder for MVP
- **WHEN** implementing MVP version of API key management endpoints
- **THEN** the system SHALL use a simple authentication mechanism (e.g., `X-User-ID` header)
- **AND** the system SHALL document this as a placeholder for proper session-based authentication
- **AND** the system SHALL be designed to allow easy replacement with proper authentication later

