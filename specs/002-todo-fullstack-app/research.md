# Research: Todo Full-Stack Web Application (Phase II)

**Feature**: 002-todo-fullstack-app
**Date**: 2026-01-11

## Architectural Decision Research

### 1. Monorepo vs Multi-repo Structure

**Decision**: Monorepo structure
**Rationale**: Aligns with specification requirement for monorepo structure and clean separation between frontend and backend. Facilitates easier coordination between components while maintaining clear boundaries. Matches modern web application development practices.
**Alternatives considered**:
- Multi-repo: Would complicate deployment and coordination between frontend and backend
- Single unified repo: Would not provide clean separation required by specification

### 2. API Design Approach for User-Scoped Task Operations

**Decision**: RESTful API with user context in JWT claims
**Rationale**: Provides clear separation of concerns while ensuring users can only access their own tasks. Leverages JWT claims to identify the requesting user without additional database lookups. Follows standard REST patterns familiar to developers.
**Alternatives considered**:
- GraphQL: More complex for basic CRUD operations required in Phase II
- RPC-style endpoints: Less discoverable and standardized than REST
- Resource-based with user ID in path: Would require additional validation to ensure data isolation

### 3. JWT Validation Strategy in FastAPI

**Decision**: Dependency injection approach using FastAPI dependencies
**Rationale**: Clean separation of concerns, reusable across endpoints, integrates well with FastAPI's design patterns, allows for easy testing. Dependencies can be injected at the router or individual endpoint level.
**Alternatives considered**:
- Middleware: Would apply to all routes uniformly, less flexibility for public endpoints
- Decorator approach: Would scatter auth logic across multiple files
- Manual validation in each endpoint: Would duplicate code and violate DRY principle

### 4. Strategy for Sharing Authentication Context Between Frontend and Backend

**Decision**: JWT tokens stored in httpOnly cookies with proper CSRF protection
**Rationale**: Provides security against XSS and CSRF attacks, aligns with Better Auth's recommended practices, keeps sensitive tokens away from JavaScript. Backend can validate tokens directly while frontend makes API calls seamlessly.
**Alternatives considered**:
- LocalStorage: Vulnerable to XSS attacks
- Session storage: Lost on page refresh, less convenient for users
- Headers with Bearer tokens: Vulnerable to interception if not properly secured

### 5. Database Schema Design for Users and Tasks with Future Extensibility

**Decision**: SQLModel with explicit foreign key relationships and extensible field patterns
**Rationale**: Meets specification requirement for SQLModel ORM, provides clear relationships between users and tasks, allows for future extensions (tags, priorities, due dates) without major schema changes. Neon PostgreSQL supports the required features.
**Schema outline**:
- Users table: id, email, hashed_password, created_at, updated_at
- Todos table: id, title, description, completed, user_id (FK), created_at, updated_at
**Alternatives considered**:
- NoSQL database: Would not meet SQLModel requirement from specification
- Separate tables per user: Would complicate queries and not leverage relational features
- Single table with user_id: Basic approach but with proper indexing and constraints for performance

### 6. Error Handling Strategy for Auth Failures and Invalid Requests

**Decision**: Standard HTTP status codes with JSON error responses
**Rationale**: Follows REST API best practices, easily understood by frontend clients, consistent with specification requirement for JSON error responses. Proper error categorization helps with debugging and monitoring.
**Error mapping**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Valid token but insufficient permissions (shouldn't occur with proper JWT validation)
- 404 Not Found: Requested resource doesn't exist for the authenticated user
- 422 Unprocessable Entity: Validation errors for requests
- 500 Internal Server Error: Unexpected server errors
**Alternatives considered**:
- Custom error codes: Less standard and harder to integrate with existing tools
- XML responses: Contradicts specification requirement for JSON responses
- Generic error responses: Would not provide sufficient information for debugging

### 7. Frontend Data-Fetching Strategy (Server Components vs Client Components)

**Decision**: Hybrid approach using Next.js App Router with Server Components for initial load and Client Components for interactivity
**Rationale**: Leverages Next.js 16+ capabilities, provides SEO benefits with server rendering, enables interactive features with client components. Authentication state can be managed at the boundary between server and client components.
**Strategy**:
- Server Components: Initial page rendering, user data fetching with auth context
- Client Components: Interactive elements like toggling todo completion, adding/deleting todos
- React Server Components: For non-interactive UI that needs to be server-rendered
**Alternatives considered**:
- Pure Client-Side Rendering: Slower initial load, worse SEO
- Pure Server-Side Rendering: Less interactive, requires full page refreshes
- Traditional SPA: Would not leverage Next.js App Router benefits mentioned in specification

## Technology Stack Decisions

### Backend Technologies
- **FastAPI**: Selected for its excellent performance, automatic API documentation, and strong typing support
- **SQLModel**: Chosen to meet specification requirements for ORM while providing SQLAlchemy's power and Pydantic's validation
- **Neon PostgreSQL**: Serverless PostgreSQL option that meets specification requirements for Neon Serverless PostgreSQL
- **Better Auth**: Authentication library that works well with Next.js and provides JWT-based authentication as required

### Frontend Technologies
- **Next.js 16+**: Selected to meet specification requirements and for its App Router capabilities
- **TypeScript**: For type safety and better development experience
- **Tailwind CSS**: For rapid, consistent UI development
- **React Query/SWR**: For data fetching and caching

### Security Considerations
- JWT tokens with 24-hour expiration (as specified in clarifications)
- HttpOnly cookies for secure token storage
- Proper CORS configuration
- Input validation and sanitization
- Rate limiting (100 requests per hour per user as specified)

## Integration Patterns

### Frontend-Backend Communication
- RESTful API endpoints for all todo operations
- JWT-based authentication for all protected endpoints
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Consistent error response format

### Authentication Flow
- User registers/signs up via frontend
- Better Auth handles registration/login
- JWT tokens stored securely in httpOnly cookies
- Backend validates JWT and extracts user context
- Frontend makes API calls with automatic cookie inclusion

## Future Extensibility Considerations

The architecture is designed to accommodate future features without major refactoring:
- Additional user preferences can be added to the User model
- New todo properties (tags, priorities, due dates) can be added to Todo model
- New API endpoints can follow the same patterns established
- Authentication system can be extended for social logins if needed
- Database schema supports indexing and performance optimizations for scaling