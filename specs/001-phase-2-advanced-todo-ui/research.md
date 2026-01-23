# Research for Phase 2 - Advanced Todo Features and Professional UI

## Decision: Recurrence Rule Representation
**Rationale**: Using the iCalendar RFC 5545 RRULE standard for recurrence patterns provides a well-established, widely-understood format that can represent all required recurrence types (daily, weekly, monthly).
**Alternatives considered**:
- Custom simple format (e.g., "daily", "weekly", "monthly") - limited flexibility
- ISO 8601 duration format - less expressive for complex recurrences

## Decision: Tag Storage Format
**Rationale**: Store tags as a separate entity with a many-to-many relationship to tasks, with auto-assigned colors from a predefined palette. This allows for tag reuse and consistent color coding.
**Alternatives considered**:
- Storing tags as JSON array in task entity - harder to query and maintain consistency
- Free-form text tags without color coding - lacks visual organization

## Decision: Theme Token Structure
**Rationale**: Implement a centralized theme object with categorized tokens (colors, typography, spacing, etc.) that can be consumed by both design systems and code. This ensures consistency across all components.
**Alternatives considered**:
- Ad-hoc CSS variables scattered across components - inconsistent and hard to maintain
- Hardcoded values in components - impossible to maintain theme consistency

## Decision: RTL Layout Strategy
**Rationale**: Use Tailwind CSS RTL support with directional utilities (e.g., `ltr:ml-4` and `rtl:mr-4`) and CSS logical properties where available. This provides automatic layout flipping while maintaining code readability.
**Alternatives considered**:
- Manual CSS overrides for RTL - error-prone and hard to maintain
- Separate RTL stylesheets - doubles maintenance effort

## Decision: Error Code Naming Conventions
**Rationale**: Use descriptive, domain-specific error codes with a consistent prefix pattern (e.g., "TODO_001", "PERM_002") that clearly indicate the subsystem and specific error condition.
**Alternatives considered**:
- Generic HTTP status codes only - insufficient specificity for user feedback
- Numeric-only codes without prefixes - unclear context

## Decision: Auth Validation Split (Frontend vs Backend)
**Rationale**: Perform basic validation (format checks) on frontend for UX responsiveness, but enforce all security-critical validation on backend. This provides immediate feedback while maintaining security.
**Alternatives considered**:
- Frontend-only validation - security vulnerability
- Backend-only validation - poor user experience with delayed feedback