## ADDED Requirements

### Requirement: Consistent Dashboard Layout
All dashboard pages SHALL use the DashboardLayout component to provide consistent sidebar navigation and header across the application.

#### Scenario: Dashboard page uses DashboardLayout
- **WHEN** a user navigates to the Dashboard page
- **THEN** the page SHALL display the Sidebar component on the left side
- **AND** the page SHALL display the Header component at the top
- **AND** the page SHALL use the DashboardLayout component wrapper
- **AND** the layout SHALL match the layout used by other dashboard pages (Projects, Agents, Usage, Billing)

#### Scenario: All dashboard pages have consistent navigation
- **WHEN** a user navigates between dashboard pages (Dashboard, Projects, Agents, Usage, Billing)
- **THEN** all pages SHALL display the same Sidebar component
- **AND** all pages SHALL display the same Header component structure
- **AND** the active route SHALL be highlighted in the Sidebar navigation
- **AND** the Header SHALL display the appropriate page title for each route

