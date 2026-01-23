## 1. Chatbot Component Development
- [x] 1.1 Create Chatbot component directory structure (`frontend/src/components/Chatbot/`)
- [x] 1.2 Create `Chatbot.jsx` component with chat interface (messages, input, send button)
- [x] 1.3 Create `Chatbot.css` with design system colors and styling
- [x] 1.4 Implement chat state management (messages array, input handling)
- [x] 1.5 Add chatbot toggle button/icon (minimize/maximize functionality)
- [x] 1.6 Style chatbot to match Frontend Design System (dark theme, accent colors)

## 2. Gemini API Integration
- [x] 2.1 Create backend API endpoint for chatbot requests (or use existing if available)
- [x] 2.2 Load SmartSpace.md as the starting point and primary context source
  - Backend loads SmartSpace.md content from `SMARTSPACE_DOC_PATH` environment variable
  - SmartSpace.md content is provided to Gemini API as context for all queries
- [x] 2.3 Integrate Gemini API to process user queries with SmartSpace.md as primary context
  - Ensure SmartSpace.md content is included in every Gemini API call
  - Responses are based on official SmartSpace documentation
- [x] 2.4 Handle API errors and loading states in chatbot
- [x] 2.5 Implement message streaming or response handling

## 3. Landing Page Integration
- [x] 3.1 Import and add Chatbot component to LandingPage.jsx
- [x] 3.2 Position chatbot (fixed bottom-right corner or similar)
- [x] 3.3 Ensure chatbot doesn't interfere with existing landing page content
- [x] 3.4 Test chatbot visibility and interaction on all landing page sections

## 4. Design System Application
- [x] 4.1 Update LandingPage.css to use design system colors:
  - Primary background: `#080808`
  - Secondary background: `#212121` (for cards/sections)
  - Primary text: `#F2F2F2`
  - Accent color: `#BB4EEF` (for CTAs, active states)
- [x] 4.2 Apply design system rules to all landing page elements:
  - Cards: subtle elevation, soft shadows, rounded corners
  - Icons: monochrome `#F2F2F2`, accent `#BB4EEF` for active states
  - Typography: clear hierarchy and readability
  - States: hover, focus, active states clearly defined
- [x] 4.3 Ensure accessibility (contrast ratios, keyboard navigation)
- [x] 4.4 Audit entire landing page for visual consistency

## 5. Testing & Validation
- [x] 5.1 Test chatbot functionality (send message, receive response)
- [x] 5.2 Verify SmartSpace.md is loaded as starting point and primary context source
  - Verify backend loads SmartSpace.md content correctly
  - Verify SmartSpace.md content is provided to Gemini API for all queries
  - Test that chatbot responses are based on SmartSpace.md documentation
- [x] 5.3 Test chatbot on different screen sizes (responsive design)
- [x] 5.4 Verify design system colors are applied consistently
- [x] 5.5 Test all interactive elements (buttons, links, forms)
- [x] 5.6 Verify no visual inconsistencies or alignment issues

