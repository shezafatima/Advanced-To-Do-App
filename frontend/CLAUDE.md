# Claude Code Rules - Frontend (Next.js)

This file provides specific guidance for frontend development using Next.js 16+ with App Router.

## Task Context

**Your Surface:** Frontend development focusing on user interface components, API integration, authentication context, and responsive design.

**Your Success is Measured By:**
- Components follow React best practices and Next.js conventions
- API integration uses proper error handling and loading states
- Authentication context is properly managed
- UI is responsive and accessible
- All components are properly typed with TypeScript

## Frontend Development Guidelines

### 1. Next.js App Router Patterns
- Use the App Router directory structure (app/)
- Implement Server Components for initial rendering where appropriate
- Use Client Components for interactive features
- Follow proper data fetching patterns
- Implement proper error boundaries and loading states

### 2. Component Architecture
- Create reusable, well-encapsulated components
- Follow the principle of least re-rendering
- Use proper TypeScript interfaces for props
- Implement proper prop drilling prevention with Context API or state management
- Separate presentation from business logic

### 3. Authentication & State Management
- Implement authentication context for managing user state
- Securely store and manage JWT tokens
- Implement protected routes
- Handle session expiration gracefully
- Provide proper feedback during authentication flows

### 4. API Integration
- Create centralized API client/service for backend communication
- Handle loading, error, and success states appropriately
- Implement proper error handling and user feedback
- Use React Query or SWR for data fetching and caching
- Attach authentication tokens to requests automatically

### 5. Responsive Design
- Use Tailwind CSS for consistent styling
- Implement mobile-first responsive design
- Ensure proper accessibility attributes
- Use proper semantic HTML elements
- Implement keyboard navigation support

## UI/UX Standards

### Component Structure
- Organize components in the components/ directory
- Create reusable UI primitives
- Separate complex forms into dedicated components
- Use proper folder structure for pages and layouts
- Implement consistent design patterns

### User Experience
- Provide loading indicators for async operations
- Show appropriate error messages to users
- Implement optimistic updates where appropriate
- Use proper form validation and feedback
- Ensure fast perceived performance

### Accessibility
- Use proper ARIA attributes
- Implement keyboard navigation support
- Ensure proper color contrast ratios
- Provide alternative text for images
- Follow WCAG guidelines

## Default Policies for Frontend Development

- Use TypeScript for all components and services
- Follow React best practices and hooks guidelines
- Implement proper error boundaries
- Use consistent naming conventions
- Write unit tests for complex components
- Optimize bundle size and performance
- Use environment variables for configuration
- Follow accessibility best practices