# Change: Standardize Dashboard Layout with Sidebar and Header

## Why
Currently, the Dashboard page directly includes Sidebar and Header components, while other dashboard pages (Projects, Agents, Usage, Billing) use the DashboardLayout component. This inconsistency creates maintenance overhead and makes it harder to ensure all dashboard pages have consistent navigation and layout. Standardizing all dashboard pages to use DashboardLayout ensures a unified user experience and simplifies future layout changes.

## What Changes
- Refactor Dashboard page to use DashboardLayout component instead of directly including Sidebar and Header
- Ensure all dashboard routes consistently use the same layout pattern
- Maintain existing functionality while improving code consistency

## Impact
- Affected specs: webapp-layout (new capability)
- Affected code: 
  - `frontend/src/pages/Dashboard.jsx` - Refactor to use DashboardLayout
  - No breaking changes to user-facing functionality

