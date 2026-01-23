# Change: Simplify Dashboard UI Layout

## Why
The current dashboard layout has visual clutter with borders separating components and redundant page titles. The Header component displays page titles that are also shown in individual page components, creating duplication. Action buttons are positioned at the top of pages, which is less intuitive for users who typically expect primary actions at the bottom after reviewing content. Simplifying the layout by removing borders, eliminating duplicate titles, and moving buttons to the bottom will create a cleaner, more modern interface that follows better UX patterns.

## What Changes
- Remove border lines from Sidebar component (border-right, border-top, border-bottom)
- Remove border line from Header component (border-bottom)
- Remove page title display from Header component (keep only wallet balance and Fund Wallet button)
- Remove page-header sections (with titles and buttons) from all dashboard page components (Projects, Agents, Usage, Billing)
- Move action buttons (Create Project, Add Agent, Fund Wallet, etc.) from page headers to the bottom of their respective pages
- Update DashboardLayout to remove title prop passing to Header
- Adjust main content area spacing to accommodate the simplified layout

## Impact
- Affected specs: webapp-layout (MODIFIED capability)
- Affected code:
  - `frontend/src/components/Dashboard/Sidebar.css` - Remove border styles
  - `frontend/src/components/Dashboard/Header.jsx` - Remove title prop and display
  - `frontend/src/components/Dashboard/Header.css` - Remove border-bottom, adjust layout
  - `frontend/src/components/Dashboard/DashboardLayout.jsx` - Remove title prop handling
  - `frontend/src/pages/Projects.jsx` - Remove page-header, move button to bottom
  - `frontend/src/pages/Projects.css` - Update styles for button positioning
  - `frontend/src/pages/Agents.jsx` - Remove page-header, move button to bottom
  - `frontend/src/pages/Agents.css` - Update styles for button positioning
  - `frontend/src/pages/Usage.jsx` - Remove page-header section
  - `frontend/src/pages/Usage.css` - Update styles
  - `frontend/src/pages/Billing.jsx` - Remove page-header, move button to bottom
  - `frontend/src/pages/Billing.css` - Update styles for button positioning
- No breaking changes to functionality

