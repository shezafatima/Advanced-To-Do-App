# API Documentation: Todo Full-Stack Web Application

## Overview

This document describes the RESTful API for the secure, multi-user todo application with authentication and data isolation. The API follows standard REST conventions and uses JSON for request/response payloads.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://api.todoapp.example.com`

## Authentication

Most endpoints require authentication using JWT (JSON Web Tokens). Include the token in the Authorization header:

```
Authorization: Bearer {your-jwt-token}
```

## Endpoints

### Authentication

#### POST `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
- `200`: User successfully registered
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "is_active": true
}
```

- `400`: Invalid input or user already exists
- `422`: Validation error

#### POST `/auth/login`

Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
- `200`: Successful login
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer"
}
```

- `401`: Invalid credentials

#### GET `/auth/me`

Get information about the currently authenticated user.

**Headers:**
```
Authorization: Bearer {your-jwt-token}
```

**Response:**
- `200`: Current user information
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "is_active": true
}
```

- `401`: Authentication required or invalid credentials

### Todos

#### GET `/todos/`

Get all todos for the current user.

**Headers:**
```
Authorization: Bearer {your-jwt-token}
```

**Response:**
- `200`: List of todos for the current user
```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Optional description",
    "completed": false,
    "user_id": "user-uuid-string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

- `401`: Authentication required or invalid credentials

#### POST `/todos/`

Create a new todo for the authenticated user.

**Headers:**
```
Authorization: Bearer {your-jwt-token}
```

**Request Body:**
```json
{
  "title": "New task",
  "description": "Optional description"
}
```

**Response:**
- `200`: Todo successfully created
```json
{
  "id": "uuid-string",
  "title": "New task",
  "description": "Optional description",
  "completed": false,
  "user_id": "user-uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

- `401`: Authentication required or invalid credentials
- `422`: Validation error

#### GET `/todos/{todo_id}`

Get details of a specific todo.

**Headers:**
```
Authorization: Bearer {your-jwt-token}
```

**Path Parameters:**
- `todo_id`: UUID of the todo to retrieve

**Response:**
- `200`: Todo details
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

- `401`: Authentication required or invalid credentials
- `404`: Todo not found

#### PUT `/todos/{todo_id}`

Update details of a specific todo.

**Headers:**
```
Authorization: Bearer {your-jwt-token}
```

**Path Parameters:**
- `todo_id`: UUID of the todo to update

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
- `200`: Todo successfully updated
```json
{
  "id": "uuid-string",
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

- `401`: Authentication required or invalid credentials
- `404`: Todo not found
- `422`: Validation error

#### DELETE `/todos/{todo_id}`

Delete a specific todo.

**Headers:**
```
Authorization: Bearer {your-jwt-token}
```

**Path Parameters:**
- `todo_id`: UUID of the todo to delete

**Response:**
- `204`: Todo successfully deleted
- `401`: Authentication required or invalid credentials
- `404`: Todo not found

#### PATCH `/todos/{todo_id}/toggle`

Toggle the completion status of a specific todo.

**Headers:**
```
Authorization: Bearer {your-jwt-token}
```

**Path Parameters:**
- `todo_id`: UUID of the todo to toggle

**Request Body:**
```json
{
  "completed": true
}
```

**Response:**
- `200`: Todo completion status successfully toggled
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "completed": true,
  "user_id": "user-uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

- `401`: Authentication required or invalid credentials
- `404`: Todo not found
- `422`: Validation error

## Error Responses

All error responses follow the same structure:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Exceeding the rate limit will result in a `429 Too Many Requests` response.

## Security

- All sensitive data is transmitted over HTTPS
- Passwords are securely hashed using BCrypt
- JWT tokens have configurable expiration times
- All API requests are logged for security monitoring