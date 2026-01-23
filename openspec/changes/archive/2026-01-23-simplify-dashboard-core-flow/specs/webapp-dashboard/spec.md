## ADDED Requirements

### Requirement: Simplified Dashboard Core Flow
The web application SHALL provide a simplified dashboard that focuses on the core user flow: API key management, making test requests, and viewing code examples.

#### Scenario: User views simplified dashboard
- **WHEN** a user navigates to the Dashboard page
- **THEN** the page SHALL display the DashboardLayout component
- **AND** the page SHALL display an API Key section at the top
- **AND** the page SHALL display a simple chatbot interface for testing API requests
- **AND** the page SHALL display code examples showing how to use the API
- **AND** the page SHALL NOT display unnecessary components (stats cards, quick actions, analytics, getting started guide)

#### Scenario: User manages API key from dashboard
- **WHEN** a user views the Dashboard page
- **THEN** the API Key section SHALL display the user's current API key (masked by default)
- **AND** the section SHALL provide quick actions to copy the API key
- **AND** the section SHALL provide a link to the full API Keys page for detailed management
- **AND** if no API key exists, the section SHALL prompt the user to generate one

#### Scenario: User makes test request from dashboard
- **WHEN** a user enters text in the chatbot interface and selects a model
- **AND** the user clicks the send button
- **THEN** the system SHALL send the request to the appropriate backend API endpoint
- **AND** the system SHALL display a loading state while processing
- **AND** the system SHALL display the response when received
- **AND** the system SHALL display payment information if applicable
- **AND** the system SHALL display any errors that occur

#### Scenario: User views code examples
- **WHEN** a user views the Dashboard page
- **THEN** the page SHALL display code examples showing how to use the SmartSpace API
- **AND** the code examples SHALL include the user's API key (masked by default)
- **AND** the code examples SHALL include the selected model
- **AND** the code examples SHALL show Python and JavaScript examples
- **AND** the code examples SHALL update based on the current request/model selection
- **AND** the code examples SHALL provide copy-to-clipboard functionality

### Requirement: Simple Chatbot Interface
The dashboard SHALL provide a simple chatbot interface for testing API requests directly from the dashboard.

#### Scenario: User interacts with chatbot
- **WHEN** a user views the Dashboard page
- **THEN** the page SHALL display a chatbot interface with:
  - A model selector dropdown
  - A text input area
  - A send button
  - A response display area
- **AND** the interface SHALL be simple and focused on testing API requests
- **AND** the interface SHALL NOT include complex chat history or conversation management

#### Scenario: Chatbot processes request
- **WHEN** a user enters text and clicks send
- **THEN** the chatbot SHALL validate the input
- **AND** the chatbot SHALL send the request to the backend API endpoint
- **AND** the chatbot SHALL display a loading state
- **AND** the chatbot SHALL display the response when received
- **AND** the chatbot SHALL handle errors gracefully with user-friendly messages

#### Scenario: Chatbot displays request history
- **WHEN** a user makes requests through the chatbot
- **THEN** the chatbot SHALL maintain a simple list of recent requests (last 5-10)
- **AND** each request SHALL show the model used, timestamp, and status
- **AND** users SHALL be able to view request details

### Requirement: Code Example Display
The dashboard SHALL display code examples that show users how to use the SmartSpace API in their applications.

#### Scenario: Code examples are displayed
- **WHEN** a user views the Dashboard page
- **THEN** the page SHALL display code examples in multiple languages (Python, JavaScript)
- **AND** the code examples SHALL include the user's API key (masked by default, with option to show full key)
- **AND** the code examples SHALL include the currently selected model
- **AND** the code examples SHALL show the correct request format for the selected facility/endpoint

#### Scenario: Code examples update dynamically
- **WHEN** a user selects a different model
- **OR** a user makes a request
- **THEN** the code examples SHALL update to reflect the current model and request format
- **AND** the code examples SHALL show the appropriate endpoint and parameters

#### Scenario: Code examples are copyable
- **WHEN** a user views code examples
- **THEN** each code example SHALL have a copy-to-clipboard button
- **AND** clicking the button SHALL copy the code to the clipboard
- **AND** the button SHALL provide visual feedback when copied

