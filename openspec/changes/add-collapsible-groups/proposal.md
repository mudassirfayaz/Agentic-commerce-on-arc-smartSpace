# Change: Add Collapsible Groups to Model Showcase and Similar Sections

## Why
The model showcasing section displays all provider groups expanded by default, which can occupy a large amount of vertical space on the page, especially with 100+ models across multiple providers. This creates a poor user experience where users must scroll extensively to see all content, and it's difficult to focus on specific providers. Similar sections throughout the application (FAQ sections, feature groups, etc.) also suffer from the same issue. Adding collapse/expand functionality will allow users to focus on relevant content, reduce visual clutter, and improve overall page navigation and usability.

## What Changes
- Add collapse/expand functionality to model provider groups in ModelGallery component
- Create reusable CollapsibleGroup component for consistent behavior across the application
- Add collapse/expand controls (chevron icons) to group headers
- Implement smooth expand/collapse animations
- Add "Expand All" / "Collapse All" controls for model showcase section
- Apply collapsible pattern to other sections where appropriate (FAQ items, feature groups, etc.)
- Maintain expanded/collapsed state during user session
- Ensure accessibility (keyboard navigation, ARIA attributes)
- Update styling to match design system (colors, transitions, hover states)

## Impact
- Affected specs: frontend-ui (new capability), frontend-models (MODIFIED - add collapse/expand to ModelGallery)
- Affected code:
  - `frontend/src/components/Models/ModelGallery.jsx` - MODIFIED to add collapse/expand state and controls
  - `frontend/src/components/Models/ModelGallery.css` - MODIFIED to add collapse/expand styles and animations
  - `frontend/src/components/UI/CollapsibleGroup.jsx` - NEW reusable component
  - `frontend/src/components/UI/CollapsibleGroup.css` - NEW styling for reusable component
  - `frontend/src/pages/LandingPage.jsx` - MODIFIED to add "Expand All/Collapse All" controls
  - `frontend/src/pages/LandingPage.css` - MODIFIED for new controls styling
  - Other sections (FAQ, features) - May be updated to use CollapsibleGroup pattern
- Breaking changes: None (additive only)
- Dependencies: None

