## ADDED Requirements

### Requirement: Request Processing Pipeline
The backend SHALL process external API requests through a complete pipeline that includes authentication, validation, transformation, agentic brain processing, and response formatting.

#### Scenario: Complete request processing flow
- **WHEN** an external API request is received
- **THEN** the system SHALL authenticate the request using API key verification
- **AND** the system SHALL validate the request format according to the facility type
- **AND** the system SHALL resolve the model name to provider and model components
- **AND** the system SHALL transform the facility-specific request format to agentic brain format
- **AND** the system SHALL process the request through the agentic brain (decision engine, payment, provider API call)
- **AND** the system SHALL transform the agentic brain response back to facility-specific format
- **AND** the system SHALL return the formatted response to the user

#### Scenario: Request format transformation
- **WHEN** processing a request from a facility-specific endpoint
- **THEN** the system SHALL transform the request format to match the agentic brain's expected format
- **AND** the transformation SHALL preserve all necessary information
- **AND** the transformation SHALL map facility-specific parameters to agentic brain parameters
- **AND** the transformation SHALL set the appropriate operation_type based on the facility

#### Scenario: Response format transformation
- **WHEN** the agentic brain returns a response
- **THEN** the system SHALL transform the response to match the facility-specific format
- **AND** the transformation SHALL extract the provider's response
- **AND** the transformation SHALL format the response consistently with the request type
- **AND** the transformation SHALL include relevant metadata (payment info, decision details) if applicable

