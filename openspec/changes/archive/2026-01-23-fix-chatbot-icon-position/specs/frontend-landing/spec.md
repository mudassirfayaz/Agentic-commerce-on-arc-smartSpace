## MODIFIED Requirements

### Requirement: Landing Page Chatbot
The landing page SHALL provide a Gemini-powered chatbot that guides users based on SmartSpace.md documentation. SmartSpace.md serves as the starting point and primary context source for the chatbot. The chatbot icon/button SHALL be positioned in the right-bottom corner of the viewport, fixed to the viewport using CSS `position: fixed`, and SHALL be visible above all other page elements including the header/navigation bar (z-index higher than header).

#### Scenario: User opens chatbot on landing page
- **WHEN** user visits the landing page
- **THEN** a chatbot icon/button is visible in the right-bottom corner of the viewport
- **AND** the chatbot icon/button is fixed to the viewport using CSS `position: fixed` (remains in position when scrolling)
- **AND** the chatbot icon/button has a z-index value higher than the header/navigation bar (header uses `z-index: 1020`, chatbot should use `z-index: 1100` or higher)
- **AND** the chatbot icon/button is visible above all other page elements including the header/navigation bar
- **AND** user can click to open the chatbot interface

#### Scenario: User asks chatbot a question
- **WHEN** user opens chatbot and types a question
- **THEN** the question is sent to backend API
- **AND** backend loads SmartSpace.md as the starting point and primary context source
- **AND** backend provides SmartSpace.md content to Gemini API as context for the query
- **AND** backend calls Gemini API with user query and SmartSpace.md context
- **AND** chatbot displays the response to the user based on SmartSpace.md documentation

#### Scenario: Chatbot provides contextual guidance
- **WHEN** user asks about SmartSpace features, usage, or troubleshooting
- **THEN** backend uses SmartSpace.md as the starting point and primary context source
- **AND** chatbot responds based on SmartSpace.md documentation
- **AND** responses are relevant and helpful, derived from SmartSpace.md content
- **AND** chatbot can answer questions about getting started, API usage, payments, models, etc. based on SmartSpace.md

#### Scenario: Chatbot error handling
- **WHEN** Gemini API call fails or times out
- **THEN** chatbot displays an error message to user
- **AND** user can retry the request
- **AND** chatbot remains functional for subsequent queries

#### Scenario: Chatbot icon visibility
- **WHEN** user scrolls the landing page
- **THEN** the chatbot icon/button remains fixed in the right-bottom corner of the viewport
- **AND** the chatbot icon/button remains visible above the header/navigation bar at all times
- **AND** the chatbot icon/button is not obscured by any other page elements
- **AND** the chatbot icon/button maintains its position relative to the viewport (not the page content)

