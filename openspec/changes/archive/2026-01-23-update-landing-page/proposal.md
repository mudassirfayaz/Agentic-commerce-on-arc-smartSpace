# Change: Update Frontend Landing Page with Chatbot and Design System

## Why
The landing page needs to be enhanced with:
1. **Gemini Chatbot Integration**: Users need contextual guidance based on SmartSpace.md documentation directly on the landing page
   - **SmartSpace.md as Knowledge Base**: SmartSpace.md serves as the starting point and primary context source for the chatbot
   - Backend loads SmartSpace.md content and provides it to Gemini API as context for all user queries
2. **Design System Application**: The landing page must follow the new Frontend Design System guidelines for consistent, premium aesthetics
3. **Improved User Experience**: A chatbot provides instant help and reduces friction for new users exploring SmartSpace

Currently, the landing page exists but lacks the chatbot feature and may not fully comply with the Frontend Design System color scheme and design rules.

## What Changes
- Add Gemini-powered chatbot component to landing page
- **SmartSpace.md Integration**: Backend loads SmartSpace.md as the starting point and primary context source for chatbot
  - SmartSpace.md content is provided to Gemini API as context for all user queries
  - Ensures chatbot responses are based on official SmartSpace documentation
- Apply Frontend Design System colors and design rules to landing page
- Ensure chatbot is accessible and provides contextual guidance
- Update landing page styling to match design system (`#080808`, `#212121`, `#F2F2F2`, `#BB4EEF`)
- Maintain all existing landing page functionality and content

## Impact
- Affected specs: frontend-landing (new capability)
- Affected code:
  - `frontend/src/pages/LandingPage.jsx` - Add chatbot component
  - `frontend/src/pages/LandingPage.css` - Apply design system styling
  - `frontend/src/components/Chatbot/` - New chatbot component (to be created)
  - Backend API endpoint for chatbot integration (if needed)
- No breaking changes to existing functionality

