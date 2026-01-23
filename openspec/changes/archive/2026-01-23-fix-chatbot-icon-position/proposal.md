# Change: Fix Chatbot Icon Position

## Why
The chatbot icon/button on the webpage is not properly positioned. It is currently hidden under the header/navigation bar due to z-index conflicts, and there is a CSS issue where `position: relative;` overrides `position: fixed;`, preventing the button from being properly fixed to the viewport. The icon should be visible in the right-bottom corner of the page, above all other elements including the header.

## What Changes
- Fix CSS positioning issue: Remove duplicate `position: relative;` that overrides `position: fixed;` in chatbot toggle button styles
- Increase z-index of chatbot toggle button to ensure it appears above the header (header uses `z-index: 1020`, so chatbot should use a higher value)
- Ensure chatbot toggle button remains fixed in the right-bottom corner of the viewport
- Update chatbot window z-index to maintain proper layering when open

## Impact
- Affected specs: frontend-landing (chatbot positioning requirement)
- Affected code:
  - `frontend/src/components/Chatbot/Chatbot.css` - Fix positioning and z-index values
  - No changes to component logic or structure, only CSS styling fixes

