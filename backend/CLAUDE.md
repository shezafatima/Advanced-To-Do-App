# Claude Code Rules - Backend (FastAPI)

This file provides specific guidance for backend development using FastAPI.

## Task Context

**Your Surface:** Backend development focusing on API endpoints, database models, services, and authentication.

**Your Success is Measured By:**
- API endpoints follow RESTful patterns and OpenAPI specifications
- Database models use SQLModel with proper relationships
- Authentication uses JWT tokens with proper validation
- Services follow clean architecture principles
- All endpoints enforce user data isolation

## Backend Development Guidelines

### 1. FastAPI Best Practices
- Use Pydantic models for request/response validation
- Implement dependency injection for authentication and database sessions
- Follow RESTful API design principles
- Use proper HTTP status codes
- Implement comprehensive error handling

### 2. SQLModel Database Patterns
- Define models inheriting from SQLModel with proper table configurations
- Use UUID for primary keys
- Implement proper relationships between models
- Include created_at and updated_at timestamps
- Use proper indexing for performance

### 3. Authentication & Authorization
- Implement JWT-based authentication
- Create dependency functions for token validation
- Ensure user data isolation at the service layer
- Hash passwords using bcrypt or similar
- Validate user permissions for each operation

### 4. Service Layer Architecture
- Separate business logic from API endpoints
- Implement proper error handling in services
- Validate user ownership of resources
- Use database sessions properly with context managers
- Follow single responsibility principle

### 5. Error Handling
- Use proper HTTP status codes (401, 403, 404, 422, 500)
- Return consistent error response format
- Log errors appropriately
- Don't expose internal system details in error messages

## API Development Standards

### Endpoint Structure
- Organize endpoints in separate router files by feature
- Use consistent URL patterns
- Implement proper authentication checks
- Validate input data using Pydantic models
- Handle errors gracefully

### Security Considerations
- All endpoints requiring authentication must validate JWT tokens
- User-specific data must be filtered by user ID
- Implement rate limiting where appropriate
- Sanitize all user inputs
- Use parameterized queries to prevent SQL injection

### Data Validation
- Use Pydantic models for all request/response bodies
- Validate required fields, data types, and constraints
- Implement custom validators for business logic
- Return appropriate error messages for validation failures

## Default Policies for Backend Development

- Use type hints consistently
- Follow PEP 8 style guidelines
- Write unit tests for all service functions
- Document all endpoints with proper OpenAPI specifications
- Implement proper logging
- Use environment variables for configuration
- Maintain backward compatibility when extending APIs