# backend-api-endpoints Specification

## Purpose
TBD - created by archiving change add-facility-api-endpoints. Update Purpose after archive.
## Requirements
### Requirement: Facility-Specific API Endpoints
The backend SHALL provide facility-specific API endpoints that allow external users to make API requests using a unified, intuitive interface similar to OpenAI's API pattern.

#### Scenario: User makes text completion request
- **WHEN** a user makes a POST request to `/v1/text/completion` with a valid API key
- **THEN** the system SHALL authenticate the request using the API key
- **AND** the system SHALL validate the request format (model, text, optional parameters)
- **AND** the system SHALL resolve the model name (e.g., "openai/gpt-4") to provider and model
- **AND** the system SHALL transform the request to agentic brain format
- **AND** the system SHALL process the request through the agentic brain (decision, payment, API call)
- **AND** the system SHALL return the response in a format consistent with the request type

#### Scenario: User makes audio/speech request
- **WHEN** a user makes a POST request to `/v1/audio/speech` with a valid API key
- **THEN** the system SHALL authenticate the request using the API key
- **AND** the system SHALL validate the request format (model, text, voice, optional parameters)
- **AND** the system SHALL resolve the model name to provider and model
- **AND** the system SHALL transform the request to agentic brain format with operation_type "audio"
- **AND** the system SHALL process the request through the agentic brain
- **AND** the system SHALL return the audio response

#### Scenario: User makes image generation request
- **WHEN** a user makes a POST request to `/v1/images/generate` with a valid API key
- **THEN** the system SHALL authenticate the request using the API key
- **AND** the system SHALL validate the request format (model, prompt, optional size/parameters)
- **AND** the system SHALL resolve the model name to provider and model
- **AND** the system SHALL transform the request to agentic brain format with operation_type "image"
- **AND** the system SHALL process the request through the agentic brain
- **AND** the system SHALL return the generated image

#### Scenario: User makes embeddings request
- **WHEN** a user makes a POST request to `/v1/embeddings` with a valid API key
- **THEN** the system SHALL authenticate the request using the API key
- **AND** the system SHALL validate the request format (model, input text)
- **AND** the system SHALL resolve the model name to provider and model
- **AND** the system SHALL transform the request to agentic brain format with operation_type "embedding"
- **AND** the system SHALL process the request through the agentic brain
- **AND** the system SHALL return the embedding vector

#### Scenario: User makes vision analysis request
- **WHEN** a user makes a POST request to `/v1/vision/analyze` with a valid API key
- **THEN** the system SHALL authenticate the request using the API key
- **AND** the system SHALL validate the request format (model, image, prompt)
- **AND** the system SHALL resolve the model name to provider and model
- **AND** the system SHALL transform the request to agentic brain format with operation_type "vision"
- **AND** the system SHALL process the request through the agentic brain
- **AND** the system SHALL return the vision analysis result

### Requirement: Model Name Resolution
The backend SHALL support model names in the format `{provider}/{model}` and automatically resolve them to provider and model components.

#### Scenario: Model name resolution
- **WHEN** a request includes a model name like "openai/tts-1"
- **THEN** the system SHALL parse the model name to extract provider ("openai") and model ("tts-1")
- **AND** the system SHALL validate that the provider is supported
- **AND** the system SHALL validate that the model exists for that provider
- **AND** if the model name is invalid, the system SHALL return a clear error message

#### Scenario: Invalid model name format
- **WHEN** a request includes an invalid model name format (e.g., "tts-1" without provider)
- **THEN** the system SHALL return a 400 Bad Request error
- **AND** the error message SHALL indicate the expected format (`{provider}/{model}`)

#### Scenario: Unsupported provider or model
- **WHEN** a request includes a model name with an unsupported provider or model
- **THEN** the system SHALL return a 400 Bad Request error
- **AND** the error message SHALL indicate which provider/model is not supported

### Requirement: Request Format Transformation
The backend SHALL transform facility-specific request formats to the agentic brain format while preserving all necessary information.

#### Scenario: Text completion request transformation
- **WHEN** a text completion request is received with format `{model, text, max_tokens, temperature}`
- **THEN** the system SHALL transform it to agentic brain format with:
  - `operation_type: "completion"`
  - `request_params` containing text, max_tokens, temperature
  - Resolved provider and model from model name

#### Scenario: Audio/speech request transformation
- **WHEN** an audio/speech request is received with format `{model, text, voice}`
- **THEN** the system SHALL transform it to agentic brain format with:
  - `operation_type: "audio"`
  - `request_params` containing text and voice
  - Resolved provider and model from model name

#### Scenario: Image generation request transformation
- **WHEN** an image generation request is received with format `{model, prompt, size}`
- **THEN** the system SHALL transform it to agentic brain format with:
  - `operation_type: "image"`
  - `request_params` containing prompt and size
  - Resolved provider and model from model name

### Requirement: API Authentication
All facility-specific endpoints SHALL require API key authentication using the same mechanism as existing endpoints.

#### Scenario: Request with valid API key
- **WHEN** a request is made with a valid API key in the Authorization header
- **THEN** the system SHALL authenticate the user
- **AND** the system SHALL proceed with request processing

#### Scenario: Request without API key
- **WHEN** a request is made without an API key
- **THEN** the system SHALL return a 401 Unauthorized error
- **AND** the error message SHALL indicate that an API key is required

#### Scenario: Request with invalid API key
- **WHEN** a request is made with an invalid or revoked API key
- **THEN** the system SHALL return a 401 Unauthorized error
- **AND** the error message SHALL indicate that the API key is invalid

### Requirement: Error Handling
The backend SHALL provide clear, user-friendly error messages for all error conditions.

#### Scenario: Validation error
- **WHEN** a request fails validation (missing required fields, invalid format)
- **THEN** the system SHALL return a 400 Bad Request error
- **AND** the error message SHALL clearly indicate what validation failed

#### Scenario: Agentic brain rejection
- **WHEN** the agentic brain rejects a request (budget exceeded, policy violation, etc.)
- **THEN** the system SHALL return an appropriate error response
- **AND** the error message SHALL include the reason for rejection

#### Scenario: Provider API error
- **WHEN** the provider API call fails
- **THEN** the system SHALL return a 502 Bad Gateway error
- **AND** the error message SHALL indicate the provider API failure

