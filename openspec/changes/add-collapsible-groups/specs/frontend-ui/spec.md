## ADDED Requirements

### Requirement: Collapsible Group Component
The frontend SHALL provide a reusable CollapsibleGroup component that allows content sections to be expanded or collapsed with smooth animations.

#### Scenario: CollapsibleGroup renders with header and content
- **WHEN** a CollapsibleGroup component is rendered with header content and children
- **THEN** the component SHALL display a clickable header
- **AND** the component SHALL display the content section
- **AND** the header SHALL include a chevron icon indicating expand/collapse state
- **AND** the chevron SHALL point down (▼) when collapsed and up (▲) when expanded

#### Scenario: User toggles collapsible group
- **WHEN** a user clicks on the collapsible group header
- **THEN** the content section SHALL smoothly expand or collapse
- **AND** the chevron icon SHALL rotate 180 degrees
- **AND** the animation SHALL complete within 300ms
- **AND** the component SHALL update its expanded state

#### Scenario: CollapsibleGroup keyboard accessibility
- **WHEN** a user focuses on the collapsible group header using keyboard navigation
- **THEN** the header SHALL be focusable and show visible focus indicator
- **AND** pressing Enter or Space SHALL toggle the expand/collapse state
- **AND** the component SHALL include proper ARIA attributes (aria-expanded, aria-controls)

#### Scenario: CollapsibleGroup screen reader support
- **WHEN** a screen reader user interacts with a collapsible group
- **THEN** the header SHALL be announced as a button
- **AND** the aria-expanded state SHALL be announced
- **AND** the content SHALL be properly associated with the header via aria-controls

### Requirement: Model Gallery Collapsible Provider Groups
The model showcase section SHALL display provider groups in collapsible format to reduce vertical space usage.

#### Scenario: Model gallery displays collapsed provider groups by default
- **WHEN** a user views the model showcase section
- **THEN** all provider groups SHALL be displayed in collapsed state by default
- **AND** each provider group header SHALL display the provider name and model count
- **AND** each provider group header SHALL include a chevron icon pointing down (▼)
- **AND** the model cards within each group SHALL be hidden when collapsed

#### Scenario: User expands a provider group
- **WHEN** a user clicks on a provider group header
- **THEN** the group SHALL smoothly expand to reveal model cards
- **AND** the chevron icon SHALL rotate to point up (▲)
- **AND** the model cards SHALL be displayed in a grid layout
- **AND** the expanded state SHALL persist during the user's session

#### Scenario: User collapses an expanded provider group
- **WHEN** a user clicks on an expanded provider group header
- **THEN** the group SHALL smoothly collapse to hide model cards
- **AND** the chevron icon SHALL rotate to point down (▼)
- **AND** only the provider header SHALL remain visible

#### Scenario: Expand All functionality
- **WHEN** a user clicks the "Expand All" button in the model showcase section
- **THEN** all provider groups SHALL expand simultaneously
- **AND** all chevron icons SHALL update to point up (▲)
- **AND** all model cards SHALL become visible

#### Scenario: Collapse All functionality
- **WHEN** a user clicks the "Collapse All" button in the model showcase section
- **THEN** all provider groups SHALL collapse simultaneously
- **AND** all chevron icons SHALL update to point down (▼)
- **AND** all model cards SHALL become hidden

#### Scenario: Model gallery maintains state during filtering
- **WHEN** a user filters models by provider or category
- **AND** some provider groups are expanded
- **THEN** the expanded/collapsed state SHALL be preserved for visible groups
- **AND** groups with no matching models SHALL be hidden entirely
- **AND** newly visible groups SHALL default to collapsed state

### Requirement: Collapsible Group Animations
Collapsible groups SHALL use smooth, visually appealing animations for expand/collapse transitions.

#### Scenario: Smooth expand animation
- **WHEN** a collapsible group expands
- **THEN** the content SHALL fade in with opacity transition
- **AND** the content height SHALL animate smoothly from 0 to full height
- **AND** the animation duration SHALL be approximately 300ms
- **AND** the animation SHALL use CSS transitions for performance

#### Scenario: Smooth collapse animation
- **WHEN** a collapsible group collapses
- **THEN** the content SHALL fade out with opacity transition
- **AND** the content height SHALL animate smoothly from full height to 0
- **AND** the animation duration SHALL be approximately 300ms
- **AND** overflow SHALL be hidden during animation to prevent content spillover

#### Scenario: Chevron icon rotation animation
- **WHEN** a collapsible group toggles between expanded and collapsed
- **THEN** the chevron icon SHALL rotate 180 degrees smoothly
- **AND** the rotation animation SHALL complete within 300ms
- **AND** the rotation SHALL be synchronized with the content expand/collapse

### Requirement: Collapsible Group Styling
Collapsible groups SHALL follow the application's design system for colors, spacing, and interactive states.

#### Scenario: Collapsible group header styling
- **WHEN** a collapsible group header is displayed
- **THEN** the header SHALL use design system colors (#F2F2F2 for text, #BB4EEF for accent)
- **AND** the header SHALL have appropriate padding and spacing
- **AND** the header SHALL show hover state with visual feedback
- **AND** the header SHALL have a border or separator to distinguish it from content

#### Scenario: Collapsible group hover states
- **WHEN** a user hovers over a collapsible group header
- **THEN** the header SHALL show visual feedback (color change, background change, or cursor change)
- **AND** the hover state SHALL be consistent with other interactive elements
- **AND** the hover state SHALL clearly indicate the header is clickable

#### Scenario: Collapsible group focus states
- **WHEN** a collapsible group header receives keyboard focus
- **THEN** the header SHALL display a visible focus indicator
- **AND** the focus indicator SHALL meet accessibility contrast requirements
- **AND** the focus indicator SHALL be consistent with other focusable elements

### Requirement: Expand All / Collapse All Controls
The model showcase section SHALL provide bulk controls to expand or collapse all provider groups at once.

#### Scenario: Expand All / Collapse All buttons displayed
- **WHEN** a user views the model showcase section
- **THEN** the section SHALL display "Expand All" and "Collapse All" buttons
- **AND** the buttons SHALL be positioned above the model gallery
- **AND** the buttons SHALL be styled consistently with other action buttons
- **AND** the buttons SHALL be clearly labeled

#### Scenario: Expand All button functionality
- **WHEN** a user clicks the "Expand All" button
- **THEN** all provider groups SHALL expand
- **AND** all model cards SHALL become visible
- **AND** all chevron icons SHALL update to expanded state
- **AND** the button SHALL provide visual feedback on click

#### Scenario: Collapse All button functionality
- **WHEN** a user clicks the "Collapse All" button
- **THEN** all provider groups SHALL collapse
- **AND** all model cards SHALL become hidden
- **AND** all chevron icons SHALL update to collapsed state
- **AND** the button SHALL provide visual feedback on click

#### Scenario: Button states reflect current group states
- **WHEN** all provider groups are expanded
- **THEN** the "Expand All" button SHALL be disabled or show different state
- **WHEN** all provider groups are collapsed
- **THEN** the "Collapse All" button SHALL be disabled or show different state

