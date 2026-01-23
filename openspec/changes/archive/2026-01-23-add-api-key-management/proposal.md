# Change: Add API Key Management to Webapp Frontend

## Why
Currently, users have no way to create, view, or manage their API keys through the web application. The landing page displays a hardcoded API key example, but there's no actual functionality for users to generate and manage their own API keys. According to the SmartSpace demo flow, users should receive a single API key for unified access to all models after account setup. Without a dedicated API key management interface, users cannot complete the onboarding process or access the core functionality of SmartSpace.

## What Changes
- Add new API Keys page accessible from dashboard navigation
- Create API key management UI components for viewing, generating, and copying API keys
- Add API key generation functionality that calls backend API endpoints
- Integrate API key display with secure copy-to-clipboard functionality
- Add API Keys navigation link to Sidebar component
- Update routing to include new API Keys page
- Implement API key regeneration/revocation functionality (if needed)

## Impact
- Affected specs: webapp-api-keys (new capability), webapp-layout (MODIFIED - add navigation link)
- Affected code:
  - `frontend/src/pages/ApiKeys.jsx` - New API Keys page component
  - `frontend/src/pages/ApiKeys.css` - Styling for API Keys page
  - `frontend/src/components/Dashboard/Sidebar.jsx` - Add API Keys navigation link
  - `frontend/src/App.jsx` - Add route for API Keys page
  - Backend API endpoints (to be implemented separately) for API key generation and management
- No breaking changes to existing functionality

