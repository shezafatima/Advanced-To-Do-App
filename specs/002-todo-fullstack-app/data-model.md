# Data Model: Todo Full-Stack Web Application (Phase II)

**Feature**: 002-todo-fullstack-app
**Date**: 2026-01-11

## Overview

This document defines the data models for the secure, multi-user todo application. The models are designed to support all five basic todo operations (add, list, update, delete, mark complete/incomplete) while ensuring user data isolation and supporting future extensibility.

## Entity Models

### User Entity

**Description**: Represents a registered user of the application

**Fields**:
- `id` (UUID/String): Unique identifier for the user (Primary Key)
- `email` (String): User's email address, used for authentication (Unique, Indexed)
- `hashed_password` (String): BCrypt or similar hashed password (Not null)
- `created_at` (DateTime): Timestamp when user account was created (Indexed, Auto-generated)
- `updated_at` (DateTime): Timestamp when user account was last updated (Auto-generated)
- `is_active` (Boolean): Whether the account is active (Default: True)

**Relationships**:
- One-to-Many: User → Todos (One user can have many todos)

**Validation Rules**:
- Email: Must be valid email format
- Email: Cannot be empty
- Password: Already validated as 8+ chars, mixed case, number, special char (from spec clarifications)

### Todo Entity

**Description**: Represents a personal task item owned by a specific user

**Fields**:
- `id` (UUID/String): Unique identifier for the todo (Primary Key)
- `title` (String): Title of the todo item (Not null, Max length: 500 chars as per spec clarifications)
- `description` (Text): Optional detailed description of the todo (Nullable)
- `completed` (Boolean): Whether the todo is completed (Default: False)
- `user_id` (UUID/String): Foreign key linking to the owning user (Not null, Indexed)
- `created_at` (DateTime): Timestamp when todo was created (Indexed, Auto-generated)
- `updated_at` (DateTime): Timestamp when todo was last updated (Auto-generated)

**Relationships**:
- Many-to-One: Todo → User (Many todos belong to one user)

**Validation Rules**:
- Title: Cannot be empty
- Title: Maximum 500 characters (from spec clarifications)
- User_id: Must reference a valid existing user
- Content: Must pass standard character validation (from spec clarifications)

## Database Schema Design

### Tables

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for todos
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_completed ON todos(completed);
CREATE INDEX idx_todos_created_at ON todos(created_at);
CREATE INDEX idx_todos_updated_at ON todos(updated_at);
```

## State Transitions

### Todo State Transitions

**Completed Status**:
- Initial state: `completed = false`
- Transition 1: `false` → `true` (when user marks as complete)
- Transition 2: `true` → `false` (when user marks as incomplete)

**Allowed Transitions**:
- Active todo → Completed todo
- Completed todo → Active todo

## Relationships and Constraints

### Referential Integrity
- Foreign key constraint ensures every todo references a valid user
- Cascade delete: When a user is deleted, all their todos are automatically removed

### Data Isolation
- All queries must filter by the authenticated user's ID to ensure data isolation
- Backend service methods will enforce user ownership checks
- Database indexes on `user_id` for efficient filtering

## Future Extensibility

### Planned Extensions
The schema is designed to accommodate future features without breaking changes:

- **Tags/Priorities**: Additional columns can be added to the todos table (nullable initially)
- **Due Dates**: `due_date` column can be added to todos table
- **Categories**: `category_id` foreign key can link to a new categories table
- **Shared Todos**: Additional relationship tables can be created for collaborative features
- **Subtasks**: Self-referencing foreign key or separate subtasks table

### Versioning Considerations
- Created/updated timestamps support audit trails
- The `is_active` field in users allows for soft deletion
- Flexible text fields (like description) allow for structured data in future versions

## Validation Requirements

### Backend Validation
All data will be validated before insertion/update:
- User authentication and authorization checks
- Input sanitization to prevent injection attacks
- Field length and format validation
- Business rule validation (e.g., users can only modify their own todos)

### Database Constraints
- NOT NULL constraints on required fields
- UNIQUE constraints where appropriate (email)
- Foreign key constraints for referential integrity
- Check constraints for data consistency where needed

## Security Considerations

### Access Control
- Row-level security enforced by application logic
- All queries filtered by authenticated user context
- No direct database access from frontend

### Data Protection
- Passwords stored with strong hashing (BCrypt or similar)
- No sensitive data stored in plaintext
- Proper indexing to prevent timing attacks on authentication

## API Representation

The models will be represented in API responses with appropriate serialization:

### User Response Object
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Todo Response Object
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "user_id": "user-uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Todo Request Object (for create/update)
```json
{
  "title": "Task title",
  "description": "Optional description",
  "completed": false
}
```