# webapp-layout Specification

## Purpose
TBD - created by archiving change add-sidebar-header-webapp. Update Purpose after archive.
## Requirements
### Requirement: Sidebar Navigation Component
The web application SHALL provide a Sidebar component that displays navigation links for all authenticated dashboard routes, with active route highlighting and logout functionality. The Sidebar SHALL NOT have visible border lines; visual separation SHALL be achieved through background color contrast.

#### Scenario: Sidebar displays navigation links
- **WHEN** a user is on any authenticated dashboard page
- **THEN** the Sidebar SHALL be displayed on the left side of the screen
- **AND** the Sidebar SHALL display the SmartSpace logo at the top
- **AND** the Sidebar SHALL display navigation links for Dashboard, Projects, Agents, Usage, Billing, and API Keys
- **AND** the Sidebar SHALL highlight the currently active route
- **AND** the Sidebar SHALL display a logout button at the bottom
- **AND** the Sidebar SHALL NOT have visible border lines (separation achieved through background color contrast)

### Requirement: Header Component
The web application SHALL provide a Header component that displays wallet balance and key actions, positioned at the top of the content area. The Header SHALL NOT display page titles. The Header SHALL NOT have visible border lines; visual separation SHALL be achieved through background color contrast.

#### Scenario: Header displays wallet information
- **WHEN** a user is on any authenticated dashboard page
- **THEN** the Header SHALL be displayed at the top of the content area
- **AND** the Header SHALL display the USDC wallet balance
- **AND** the Header SHALL display a "Fund Wallet" button
- **AND** the Header SHALL be sticky (remain visible when scrolling)
- **AND** the Header SHALL NOT display page titles
- **AND** the Header SHALL NOT have visible border lines (separation achieved through background color contrast)

#### Scenario: Header wallet balance display
- **WHEN** the Header is displayed
- **THEN** the wallet balance SHALL show "USDC Balance" as a label
- **AND** the balance amount SHALL be displayed in a prominent format
- **AND** the balance SHALL be formatted as currency (e.g., "$0.00")

#### Scenario: Header responsive behavior
- **WHEN** the viewport width is less than 768px
- **THEN** the Header SHALL adjust its layout to stack elements vertically if needed
- **AND** the Header SHALL remain functional and accessible

### Requirement: DashboardLayout Component
The web application SHALL provide a DashboardLayout component that wraps page content with Sidebar and Header components to ensure consistent layout across all authenticated pages. The DashboardLayout SHALL NOT pass page title props to the Header component.

#### Scenario: DashboardLayout provides consistent structure
- **WHEN** a dashboard page uses the DashboardLayout component
- **THEN** the page SHALL display the Sidebar component on the left side
- **AND** the page SHALL display the Header component at the top of the content area
- **AND** the page content SHALL be displayed in the main content area below the Header
- **AND** the layout SHALL maintain consistent spacing and structure
- **AND** the DashboardLayout SHALL NOT pass page title props to the Header component

#### Scenario: All dashboard pages use DashboardLayout
- **WHEN** a user navigates between dashboard pages (Dashboard, Projects, Agents, Usage, Billing)
- **THEN** all pages SHALL use the DashboardLayout component
- **AND** all pages SHALL display the same Sidebar component
- **AND** all pages SHALL display the same Header component structure
- **AND** the layout SHALL be visually consistent across all pages

### Requirement: Design System Compliance
The Sidebar and Header components SHALL follow the Frontend Design System guidelines for colors, typography, spacing, and interactive states.

#### Scenario: Color system compliance
- **WHEN** the Sidebar and Header are rendered
- **THEN** the components SHALL use the primary background color (#080808) for the main layout
- **AND** the components SHALL use the secondary background color (#212121) for cards and panels
- **AND** the components SHALL use the primary text color (#F2F2F2) for text and icons
- **AND** the components SHALL use the accent color (#BB4EEF) only for active states, CTAs, and highlights
- **AND** visual separation between components SHALL be achieved through background color contrast, not visible border lines

#### Scenario: Interactive states
- **WHEN** a user hovers over a navigation item in the Sidebar
- **THEN** the navigation item SHALL display a hover state with appropriate visual feedback
- **AND** the hover state SHALL use the hover background color from the design system
- **WHEN** a navigation item is active
- **THEN** the active state SHALL be visually distinct using the accent color
- **WHEN** a user focuses on interactive elements
- **THEN** the focus state SHALL be clearly visible with a focus ring or indicator

#### Scenario: Typography and spacing
- **WHEN** the Sidebar and Header are rendered
- **THEN** the typography SHALL follow the design system guidelines
- **AND** the spacing SHALL be consistent and follow the design system spacing scale
- **AND** the components SHALL maintain proper visual hierarchy

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

### Requirement: Dashboard Page Components
Dashboard page components SHALL focus on the core user flow and SHALL NOT include unnecessary components that add complexity without immediate value. Dashboard page components (Projects, Agents, Usage, Billing) SHALL NOT display page headers with titles and action buttons at the top. Action buttons SHALL be positioned at the bottom of the page content.

#### Scenario: Simplified dashboard layout
- **WHEN** a user navigates to the Dashboard page
- **THEN** the page SHALL display only essential components:
  - API Key management section
  - Simple chatbot interface for testing requests
  - Code example display
  - Optional: Simple recent requests list
- **AND** the page SHALL NOT display:
  - Stats cards (moved to Usage page)
  - Quick action cards (functionality integrated into main interface)
  - Complex activity logs (simplified to recent requests)
  - Usage analytics (moved to Usage page)
  - Getting started guide (key steps integrated inline)
  - Welcome section (simplified header)

#### Scenario: Dashboard focuses on core flow
- **WHEN** a user views the Dashboard page
- **THEN** the page SHALL prioritize the core user journey:
  1. API key management
  2. Making test requests
  3. Viewing code examples
  4. Understanding how to use the API
- **AND** the page SHALL provide a clean, uncluttered interface
- **AND** the page SHALL make it easy for users to get started quickly

#### Scenario: Page components without headers
- **WHEN** a user views a dashboard page (Projects, Agents, Usage, Billing)
- **THEN** the page SHALL NOT display a page-header section with title and subtitle
- **AND** the page SHALL display content directly without redundant titles
- **AND** primary action buttons (Create Project, Add Agent, etc.) SHALL be positioned at the bottom of the page content
- **AND** action buttons SHALL be visible and accessible after reviewing page content

#### Scenario: Action buttons at bottom
- **WHEN** a user views a page with action buttons (Projects, Agents, Billing)
- **THEN** the action button SHALL be positioned at the bottom of the main content area
- **AND** the button SHALL be styled appropriately for bottom placement
- **AND** the button SHALL remain accessible on all screen sizes

