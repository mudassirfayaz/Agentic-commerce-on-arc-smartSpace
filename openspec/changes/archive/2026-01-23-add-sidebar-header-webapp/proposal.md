# Change: Add Sidebar and Header to Web Application

## Why
The web application needs consistent navigation and header components across all authenticated pages to provide a unified user experience. While Sidebar and Header components exist in the Dashboard components folder, they need to be properly integrated and styled according to the Frontend Design System guidelines. This ensures users have clear navigation, consistent branding, and easy access to key features like wallet balance and logout functionality.

## What Changes
- Ensure Sidebar component is properly implemented with navigation links for all dashboard routes
- Ensure Header component displays page title and wallet balance information
- Verify Sidebar and Header follow the Frontend Design System color system and design rules
- Ensure all authenticated pages (Dashboard, Projects, Agents, Usage, Billing) use DashboardLayout which includes Sidebar and Header
- Verify responsive behavior for mobile devices
- Ensure active route highlighting works correctly in Sidebar navigation

## Impact
- Affected specs: webapp-layout (new capability)
- Affected code:
  - `frontend/src/components/Dashboard/Sidebar.jsx` - Navigation component
  - `frontend/src/components/Dashboard/Sidebar.css` - Sidebar styling
  - `frontend/src/components/Dashboard/Header.jsx` - Header component
  - `frontend/src/components/Dashboard/Header.css` - Header styling
  - `frontend/src/components/Dashboard/DashboardLayout.jsx` - Layout wrapper
  - `frontend/src/components/Dashboard/DashboardLayout.css` - Layout styling
  - All dashboard pages that use DashboardLayout

