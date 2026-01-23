## Context
The landing page needs to be enhanced with a Gemini chatbot for user guidance and updated to follow the Frontend Design System. SmartSpace.md serves as the starting point and primary context source for the chatbot. The backend loads SmartSpace.md content and provides it to Gemini API as context for all user queries, ensuring responses are based on official SmartSpace documentation.

## Goals / Non-Goals

### Goals
- Add Gemini chatbot to landing page for instant user guidance
- **SmartSpace.md as Knowledge Base**: Ensure SmartSpace.md serves as the starting point and primary context source
  - Backend loads SmartSpace.md content and provides it to Gemini API for all queries
  - Chatbot responses are based on official SmartSpace documentation
- Apply Frontend Design System consistently across landing page
- Maintain all existing landing page functionality
- Ensure chatbot is accessible and responsive

### Non-Goals
- Changing landing page content or structure (only styling updates)
- Adding chatbot to other pages (separate change if needed)
- Backend infrastructure changes beyond chatbot API endpoint
- Modifying SmartSpace.md content

## Decisions

### Decision: Chatbot Component Architecture
**What**: Create a reusable Chatbot component that can be embedded in landing page
**Why**: 
- Reusability for future pages (dashboard, etc.)
- Separation of concerns (chatbot logic separate from landing page)
- Easier maintenance and testing

**Alternatives considered**:
- Inline chatbot code in LandingPage.jsx → Rejected: less maintainable
- Third-party chatbot widget → Rejected: need custom integration with SmartSpace.md

### Decision: Chatbot Positioning
**What**: Fixed position (bottom-right corner) with minimize/maximize functionality
**Why**:
- Doesn't interfere with landing page content
- Always accessible without scrolling
- Common UX pattern users expect

**Alternatives considered**:
- Embedded in page content → Rejected: takes up valuable space
- Modal overlay → Rejected: blocks content, less accessible

### Decision: Gemini API Integration Pattern
**What**: Backend API endpoint that receives user query, loads SmartSpace.md as starting point/context, calls Gemini API
**Why**:
- Keeps Gemini API key secure (never exposed to frontend)
- SmartSpace.md serves as the primary context source - backend loads it and provides to Gemini API
- Allows preprocessing of SmartSpace.md content
- Centralized error handling and rate limiting
- Ensures all chatbot responses are based on official SmartSpace documentation

**Alternatives considered**:
- Direct frontend Gemini API calls → Rejected: exposes API key, cannot load SmartSpace.md securely
- Server-side rendering → Rejected: needs real-time interaction
- Using only Gemini's general knowledge → Rejected: SmartSpace.md is the authoritative source

### Decision: Design System Application Scope
**What**: Apply design system to entire landing page, not just new chatbot
**Why**:
- Consistency across entire frontend
- Premium, enterprise-grade aesthetic
- Matches project.md requirements

**Alternatives considered**:
- Only apply to chatbot → Rejected: inconsistent user experience
- Gradual rollout → Rejected: better to do complete update

## Risks / Trade-offs

### Risk: Chatbot API Costs
**Mitigation**: 
- Implement rate limiting per user session
- Cache common queries/responses
- Monitor API usage and costs

### Risk: Design System Breaking Existing Styles
**Mitigation**:
- Test thoroughly on all landing page sections
- Maintain existing functionality
- Use CSS variables for easy theme updates

### Risk: Chatbot Performance
**Mitigation**:
- Implement loading states
- Handle API timeouts gracefully
- Consider response streaming for better UX

## Migration Plan
1. Create chatbot component in isolation
2. Test chatbot independently
3. Integrate into landing page
4. Apply design system styling incrementally
5. Test complete landing page
6. Deploy and monitor

## Open Questions
- Should chatbot be available on all pages or just landing page? (Decision: Landing page only for this change)
- Should chatbot remember conversation history? (Decision: Session-based, no persistence for MVP)
- What's the fallback if Gemini API is unavailable? (Decision: Show error message, allow retry)

