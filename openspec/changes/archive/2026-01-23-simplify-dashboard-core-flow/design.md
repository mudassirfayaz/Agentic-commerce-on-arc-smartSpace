# Design: Simplified Dashboard Core Flow

## Context

The current dashboard has too many components that don't directly support the core user journey. Users need:
1. A way to create/manage their API key
2. A simple interface to test API requests
3. Code examples showing how to use the API
4. See results of their requests

The simplified dashboard should focus on these core needs and remove distractions.

## Goals

1. **Focus on Core Flow**: API key → make request → see code → use in app
2. **Simple Interface**: Clean, minimal interface without clutter
3. **Immediate Value**: Users can test API immediately after getting key
4. **Code Examples**: Show users exactly how to integrate SmartSpace API
5. **Request Testing**: Allow users to test requests directly from dashboard

## Non-Goals

- Complex analytics (move to Usage page)
- Multiple action cards (consolidate into main interface)
- Detailed activity logs (simplify to recent requests only)
- Getting started guide (integrate key steps inline)

## Architecture

### Simplified Dashboard Layout

```
Dashboard
├── API Key Section (top)
│   ├── Display current API key (masked)
│   ├── Quick actions: Copy, Generate New, View Details
│   └── Link to full API Keys page
│
├── Test API Request (main section)
│   ├── Simple Chatbot Interface
│   │   ├── Model selector dropdown
│   │   ├── Text input area
│   │   ├── Send button
│   │   └── Response display area
│   │
│   └── Code Example Display
│       ├── Python example
│       ├── JavaScript example
│       ├── Copy buttons
│       └── Updates based on current request
│
└── Recent Requests (bottom, optional)
    └── Simple list of last 5-10 requests with status
```

### Simple Chatbot Interface

The chatbot should be a simple text input interface:
- **Model Selector**: Dropdown to select model (e.g., "openai/gpt-4", "ollama/qalb-urdu")
- **Text Input**: Large textarea for user input
- **Send Button**: Triggers API request
- **Response Area**: Shows response, loading state, errors
- **Payment Info**: Shows payment status if applicable

### Code Example Generation

Code examples should be generated dynamically based on:
- User's API key (from API Keys page)
- Selected model
- Request type (text, audio, image, etc.)
- Facility endpoint used

Examples should show:
- Python `requests` library example
- JavaScript `fetch` example
- cURL example (optional)

### Request Flow

```
User Input (Dashboard)
  │
  │ 1. User types message, selects model
  │
  ▼
Frontend Chatbot Component
  │
  │ 2. Validate input, prepare request
  │
  ▼
Backend API Endpoint
  │
  │ 3. POST /v1/text/completion (or appropriate facility endpoint)
  │    Authorization: Bearer <api_key>
  │
  ▼
Facility Controller
  │
  │ 4. Process through agentic brain
  │
  ▼
Agentic Brain
  │
  │ 5. Decision, payment, provider API call
  │
  ▼
Response
  │
  │ 6. Return to frontend
  │
  ▼
Dashboard Display
  │
  │ 7. Show response, update code examples
  │
  ▼
User
```

## Decisions

### Decision 1: Component Removal
**What**: Remove StatsCards, QuickActions, RecentActivity, UsageAnalytics, GettingStarted, WelcomeSection
**Why**: 
- These components add complexity without immediate value
- Users need to focus on core flow first
- Analytics can be moved to dedicated Usage page
**Alternatives considered**:
- Keep but hide: Still adds code complexity
- Make collapsible: Adds UI complexity

### Decision 2: Simple Chatbot Interface
**What**: Create a simple text input interface (not full chat history)
**Why**:
- Users want to test API quickly
- Simple interface is easier to understand
- Can show code examples alongside
**Alternatives considered**:
- Full chat interface: Too complex for testing
- Separate test page: Adds navigation complexity

### Decision 3: Code Example Display
**What**: Show code examples that update based on current request
**Why**:
- Users need to see how to use the API
- Dynamic examples are more helpful than static docs
- Copy-to-clipboard makes it easy to use
**Alternatives considered**:
- Link to documentation: Less immediate
- Static examples: Less helpful

### Decision 4: API Key Section
**What**: Show API key management inline or link to API Keys page
**Why**:
- API key is essential for using the service
- Quick access is important
- Full management can be on dedicated page
**Alternatives considered**:
- Full API key management on dashboard: Too much functionality
- Only link to API Keys page: Less convenient

## Risks / Trade-offs

### Risk 1: Too Simple
**Risk**: Dashboard might be too minimal, missing useful features
**Mitigation**: Keep essential features, move others to dedicated pages

### Risk 2: Code Example Security
**Risk**: API key shown in code examples could be exposed
**Mitigation**: Use masked API key in examples, show full key only when user explicitly requests

### Risk 3: Request History
**Risk**: Users might want to see request history
**Mitigation**: Add simple recent requests list, full history on Usage page

### Risk 4: Backend Integration
**Risk**: Chatbot needs to integrate with backend API endpoints
**Mitigation**: Use existing facility-specific endpoints, handle errors gracefully

## Implementation Plan

1. Create SimpleChatbot component
2. Create CodeExample component
3. Create ApiKeySection component
4. Simplify Dashboard.jsx
5. Remove unnecessary components
6. Integrate with backend API
7. Add code example generation
8. Test end-to-end flow

## Open Questions

- Should we keep a minimal "Recent Requests" section? (Yes, last 5-10 requests)
- Should code examples show full API key or masked? (Masked by default, option to show full)
- Should we support multiple request types (text, audio, image) in the simple interface? (Start with text, can expand)

