# API Implementation Guide: Todo Full-Stack Web Application

## Overview

This document provides technical details about the API implementation, including the technologies used, architecture, and internal structure.

## Tech Stack

- **Framework**: FastAPI
- **Database**: Neon PostgreSQL with SQLModel ORM
- **Authentication**: JWT tokens with Better Auth
- **Documentation**: Automatic OpenAPI/Swagger documentation
- **Validation**: Pydantic models

## Architecture

The API follows a clean architecture pattern with the following layers:

```
Controllers (API Endpoints) → Services → Models → Database
```

### Models Layer

Located in `backend/src/models/`

- `user.py`: Defines the User model with fields like id, email, hashed_password, etc.
- `todo.py`: Defines the Todo model with fields like id, title, description, completed, etc.

### Services Layer

Located in `backend/src/services/`

- `user_service.py`: Handles user-related operations like registration, retrieval, etc.
- `todo_service.py`: Handles todo-related operations like CRUD operations with user ownership validation.

### API Layer

Located in `backend/src/api/`

- `auth.py`: Contains authentication endpoints (register, login, get current user)
- `todos.py`: Contains todo endpoints (create, read, update, delete, toggle completion)
- `deps.py`: Contains dependency injection utilities (like JWT validation)

## Authentication Flow

1. User registers/login through `/auth/register` or `/auth/login`
2. Server validates credentials and returns JWT token
3. Client includes token in Authorization header for protected endpoints
4. Server validates JWT and extracts user context for each request
5. Services verify user ownership of resources before operations

## Data Validation

### Request Validation
- Pydantic models validate all incoming request data
- Field constraints: email format, password requirements, title length limits
- Type checking and required field validation

### Response Validation
- Pydantic models ensure consistent response structure
- Field serialization controls what data is exposed
- Error responses follow standard format

## Security Measures

### Authentication
- JWT tokens with configurable expiration
- Secure password hashing (BCrypt or similar)
- Rate limiting to prevent brute force attacks

### Authorization
- User ownership validation for all todo operations
- Row-level security through user ID filtering
- Input sanitization to prevent injection attacks

### Data Isolation
- All queries filtered by authenticated user context
- Database constraints enforce referential integrity
- Cascade delete for user account cleanup

## Error Handling

### HTTP Status Codes
- `200`: Success (with response body)
- `204`: Success (no response body, e.g., DELETE)
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (authentication required)
- `404`: Not Found (resource doesn't exist)
- `422`: Validation Error (request validation failed)
- `429`: Too Many Requests (rate limit exceeded)

### Error Response Format
```json
{
  "detail": "Human-readable error message"
}
```

## Database Schema

### Users Table
- `id`: UUID primary key with auto-generation
- `email`: VARCHAR(255) unique, indexed
- `hashed_password`: VARCHAR(255) not null
- `is_active`: BOOLEAN with default true
- `created_at`: TIMESTAMP with timezone, auto-generated
- `updated_at`: TIMESTAMP with timezone, auto-generated

### Todos Table
- `id`: UUID primary key with auto-generation
- `title`: VARCHAR(500) not null
- `description`: TEXT nullable
- `completed`: BOOLEAN with default false
- `user_id`: UUID foreign key to users(id) with cascade delete
- `created_at`: TIMESTAMP with timezone, auto-generated
- `updated_at`: TIMESTAMP with timezone, auto-generated

### Indexes
- `idx_users_email`: For efficient email lookups
- `idx_users_created_at`: For time-based queries
- `idx_todos_user_id`: For user-specific todo filtering
- `idx_todos_completed`: For completion status queries
- `idx_todos_created_at`: For time-based queries
- `idx_todos_updated_at`: For time-based queries

## API Documentation

The API automatically generates OpenAPI documentation available at:
- `/docs`: Interactive Swagger UI
- `/redoc`: ReDoc documentation
- `/openapi.json`: Raw OpenAPI specification

## Environment Configuration

The API uses environment variables for configuration:

- `DATABASE_URL`: Database connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT encoding (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `RATE_LIMIT_REQUESTS`: Number of requests allowed
- `RATE_LIMIT_WINDOW`: Time window in seconds

## Performance Considerations

- Database connection pooling for efficient resource usage
- Proper indexing for query optimization
- Pagination for large result sets (future enhancement)
- Caching for frequently accessed data (future enhancement)
- Efficient serialization with Pydantic