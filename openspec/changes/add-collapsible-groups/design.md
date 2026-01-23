# Collapsible Groups Feature - Design Document

## Context

The model showcasing section currently displays all provider groups (OpenAI, Anthropic, Google, etc.) in an expanded state, showing all model cards at once. With 100+ models across multiple providers, this creates excessive vertical scrolling and makes it difficult for users to focus on specific providers. Similar sections throughout the application (FAQ items, feature groups) also display all content expanded, which can overwhelm users.

## Goals / Non-Goals

### Goals
- Reduce vertical space occupied by model showcase section
- Allow users to focus on specific provider groups by collapsing others
- Create a reusable collapsible group pattern for consistent UX across the application
- Maintain smooth, visually appealing expand/collapse animations
- Ensure accessibility (keyboard navigation, screen readers)
- Preserve user's expand/collapse preferences during session
- Provide bulk controls (Expand All/Collapse All) for convenience

### Non-Goals
- Persisting collapse state across page refreshes (session-only)
- Nested collapsible groups (single level only)
- Auto-collapse based on scroll position
- Different default states per provider (all start collapsed or all start expanded)

## Decisions

### Decision 1: Default State
**What**: All provider groups start collapsed by default
- Users see provider names and model counts
- Users can expand groups they're interested in
- Reduces initial page load visual clutter

**Why**:
- With 100+ models, showing all expanded creates overwhelming initial view
- Collapsed state shows structure without taking space
- Users can quickly scan provider names and expand what interests them

**Alternatives considered**:
- All expanded: Too much content initially
- First group expanded: Arbitrary, doesn't solve space issue
- User preference: Complex, requires storage

### Decision 2: Collapsible Component Pattern
**What**: Create reusable `CollapsibleGroup` component
- Accepts header content, children, and optional default state
- Handles expand/collapse state internally
- Provides consistent styling and animations
- Can be used for model groups, FAQ items, feature sections, etc.

**Why**:
- DRY principle - avoid duplicating collapse logic
- Consistent UX across application
- Easier to maintain and update
- Reusable for future sections

**Alternatives considered**:
- Inline collapse logic: Duplicated code, inconsistent behavior
- Third-party library: Unnecessary dependency for simple feature

### Decision 3: Animation Approach
**What**: Use CSS transitions with max-height for smooth expand/collapse
- Transition max-height from 0 to auto (using large max value)
- Fade in/out for content
- Rotate chevron icon 180 degrees
- Duration: 300ms for smooth but quick feel

**Why**:
- Smooth, professional feel
- CSS transitions perform better than JavaScript animations
- Standard pattern users expect
- Fast enough to feel responsive

**Alternatives considered**:
- JavaScript animations: More complex, less performant
- Instant toggle: Jarring, poor UX
- Longer duration: Feels slow

### Decision 4: Expand/Collapse Controls
**What**: 
- Chevron icon (▼/▲) in group header, clickable to toggle
- Entire header is clickable (not just icon)
- "Expand All" / "Collapse All" buttons above model gallery
- Visual feedback on hover

**Why**:
- Clear, intuitive controls
- Large click target (entire header) improves usability
- Bulk controls save time for users exploring multiple providers
- Standard UI pattern users recognize

**Alternatives considered**:
- Plus/minus icons: Less common, chevron is clearer
- Only icon clickable: Smaller target, less accessible
- No bulk controls: Inefficient for many groups

### Decision 5: State Management
**What**: Use React useState to track expanded/collapsed state
- State stored in parent component (ModelGallery)
- State persists during session (until page refresh)
- No localStorage persistence (keeps it simple)

**Why**:
- Simple, React-native approach
- Session persistence is sufficient for this use case
- No need for complex state management
- Easy to add localStorage later if needed

**Alternatives considered**:
- localStorage persistence: Adds complexity, may not be needed
- URL state: Overkill for UI preference
- Global state: Unnecessary for component-level state

### Decision 6: Accessibility
**What**: 
- Use `<button>` for header (semantic, keyboard accessible)
- Add ARIA attributes: `aria-expanded`, `aria-controls`
- Keyboard support: Enter/Space to toggle
- Focus visible on header button

**Why**:
- WCAG compliance
- Screen reader support
- Keyboard-only navigation support
- Professional, inclusive design

**Alternatives considered**:
- Div with onClick: Less accessible
- Skip accessibility: Excludes users, non-compliant

## Architecture

### Component Structure

```
ModelGallery
├── ExpandAllControls (optional)
│   ├── Expand All button
│   └── Collapse All button
└── CollapsibleGroup[] (one per provider)
    ├── CollapsibleHeader
    │   ├── Provider name
    │   ├── Model count
    │   └── Chevron icon
    └── CollapsibleContent
        └── ModelCard[]
```

### Reusable Pattern

```
CollapsibleGroup (reusable)
├── Props: header, children, defaultExpanded, onToggle
├── State: isExpanded
└── Renders:
    ├── CollapsibleHeader (button)
    └── CollapsibleContent (animated div)
```

## Implementation Details

### CSS Animation Strategy
- Use `max-height` transition (set to large value like 5000px for "auto")
- Use `opacity` transition for fade effect
- Use `transform: rotate()` for chevron
- Use `overflow: hidden` during transition
- Set `transition` properties on content container

### State Management
```javascript
const [expandedGroups, setExpandedGroups] = useState({})
// { 'openai': true, 'anthropic': false, ... }
```

### Expand All / Collapse All
```javascript
const expandAll = () => {
  const allExpanded = {}
  providers.forEach(p => allExpanded[p] = true)
  setExpandedGroups(allExpanded)
}
```

## Risks / Trade-offs

### Risk 1: Animation Performance
**Risk**: Smooth animations may lag on low-end devices
**Mitigation**: 
- Use CSS transitions (GPU-accelerated)
- Limit animation duration (300ms)
- Test on various devices

### Risk 2: User Confusion
**Risk**: Users may not realize groups are collapsible
**Mitigation**:
- Clear visual indicators (chevron icons)
- Hover states on headers
- "Expand All" button suggests collapsible nature

### Risk 3: Accessibility Issues
**Risk**: May not work well with screen readers or keyboard navigation
**Mitigation**:
- Proper ARIA attributes
- Semantic HTML (button elements)
- Keyboard event handlers
- Test with screen readers

## Migration Plan

### Phase 1: Create Reusable Component
1. Create `CollapsibleGroup` component
2. Add CSS styling and animations
3. Add accessibility attributes
4. Test component in isolation

### Phase 2: Integrate with ModelGallery
1. Update ModelGallery to use CollapsibleGroup
2. Add state management for expanded groups
3. Add chevron icons to headers
4. Test expand/collapse functionality

### Phase 3: Add Bulk Controls
1. Add "Expand All" / "Collapse All" buttons
2. Implement bulk toggle logic
3. Style controls to match design system
4. Test bulk operations

### Phase 4: Apply to Other Sections (Optional)
1. Identify other sections that would benefit
2. Apply CollapsibleGroup pattern
3. Test and refine

## Open Questions

1. **Default State**: Should all groups start collapsed or expanded?
   - Decision: All collapsed (reduces initial clutter)

2. **Animation Duration**: How fast should expand/collapse be?
   - Decision: 300ms (smooth but quick)

3. **Bulk Controls**: Should they be always visible or toggleable?
   - Decision: Always visible when there are multiple groups

4. **Mobile Behavior**: Should behavior differ on mobile?
   - Decision: Same behavior, responsive styling

