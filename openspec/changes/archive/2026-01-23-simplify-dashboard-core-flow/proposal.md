# Change: Simplify Dashboard to Core API Flow

## Why
The current dashboard has many components (StatsCards, QuickActions, RecentActivity, UsageAnalytics, GettingStarted) that add complexity without providing immediate value. The core user flow should be simple: create API key → make request → see code example → use in application. Users need a streamlined interface focused on the essential workflow: managing their API key and making test requests with code examples. The dashboard should be a simple, focused tool that helps users get started quickly and understand how to use the SmartSpace API.

## What Changes
- Simplify Dashboard page to focus on core flow:
  - API Key management section (link to API Keys page or inline)
  - Simple chatbot/request interface for testing API calls
  - Code example display showing how to use the API
  - Request history/results display
- Remove or consolidate unnecessary components:
  - Remove StatsCards (move to Usage page if needed)
  - Remove QuickActions (functionality integrated into main interface)
  - Remove RecentActivity (simplify or remove)
  - Remove UsageAnalytics (move to Usage page)
  - Remove GettingStarted (integrate key steps into main interface)
  - Remove WelcomeSection (simplify header)
- Add simple chatbot interface:
  - Text input for API requests
  - Model selection dropdown
  - Send button that triggers backend request
  - Response display
  - Code example generation based on request
- Add code example display:
  - Show Python/JavaScript code examples for making requests
  - Include user's API key in examples
  - Show request/response format
  - Copy-to-clipboard functionality
- Integrate with backend:
  - Connect chatbot to facility-specific API endpoints
  - Process requests through agentic brain
  - Display results and payment information
  - Show request status and errors

## Impact
- Affected specs: webapp-dashboard (new capability), webapp-layout (MODIFIED - simplified dashboard)
- Affected code:
  - `frontend/src/pages/Dashboard.jsx` - Simplify to core components
  - `frontend/src/components/Dashboard/SimpleChatbot.jsx` - New simple chatbot component
  - `frontend/src/components/Dashboard/CodeExample.jsx` - New code example display component
  - `frontend/src/components/Dashboard/ApiKeySection.jsx` - New API key section component
  - Remove or archive: StatsCards, QuickActions, RecentActivity, UsageAnalytics, GettingStarted, WelcomeSection
  - `backend/src/routes/v1/chatbot.py` - May need updates for dashboard chatbot integration
- Breaking changes: Dashboard layout changes significantly (simplified)

