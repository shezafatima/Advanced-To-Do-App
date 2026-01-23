# Environment Configuration Guide

## Overview

This document describes the environment-specific configurations for development, staging, and production environments.

## Environment Files

### Development (.env.development)
```
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/todo_dev"

# JWT Configuration
JWT_SECRET_KEY="dev-secret-key-change-in-production"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
SERVER_HOST="localhost"
SERVER_PORT=8000
DEBUG=true

# Frontend Configuration
FRONTEND_URL="http://localhost:3000"

# Logging
LOG_LEVEL="DEBUG"
LOG_FILE="logs/dev.log"

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Security
ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

### Staging (.env.staging)
```
# Database
DATABASE_URL="postgresql://user:password@staging-db:5432/todo_staging"

# JWT Configuration
JWT_SECRET_KEY="staging-secret-key"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Server Configuration
SERVER_HOST="0.0.0.0"
SERVER_PORT=8000
DEBUG=false

# Frontend Configuration
FRONTEND_URL="https://staging.todoapp.example.com"

# Logging
LOG_LEVEL="INFO"
LOG_FILE="logs/staging.log"

# Rate Limiting
RATE_LIMIT_REQUESTS=500
RATE_LIMIT_WINDOW=60

# Security
ALLOWED_ORIGINS="https://staging.todoapp.example.com"
```

### Production (.env.production)
```
# Database
DATABASE_URL="postgresql://user:password@prod-db:5432/todo_prod"

# JWT Configuration
JWT_SECRET_KEY="production-secret-key-keep-safe-and-secure"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15

# Server Configuration
SERVER_HOST="0.0.0.0"
SERVER_PORT=8000
DEBUG=false

# Frontend Configuration
FRONTEND_URL="https://todoapp.example.com"

# Logging
LOG_LEVEL="WARNING"
LOG_FILE="logs/prod.log"

# Rate Limiting
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=60

# Security
ALLOWED_ORIGINS="https://todoapp.example.com"
SECURE_COOKIES=true
```

## Configuration Loading Strategy

The application follows this hierarchy for loading configuration:

1. Environment variables (highest priority)
2. Environment-specific .env file
3. Default .env file (lowest priority)

### Python Configuration Loading (Backend)

```python
import os
from dotenv import load_dotenv

# Determine environment
env = os.getenv("ENVIRONMENT", "development")

# Load appropriate environment file
if env == "production":
    load_dotenv(".env.production")
elif env == "staging":
    load_dotenv(".env.staging")
else:
    load_dotenv(".env.development")

# Fallback to default if specific file doesn't exist
load_dotenv(".env", override=False)
```

### Node.js Configuration Loading (Frontend)

```javascript
// Load environment based on NODE_ENV
const env = process.env.NODE_ENV || 'development';

// Configuration object with environment-specific values
const config = {
  development: {
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    debug: process.env.NEXT_PUBLIC_DEBUG === 'true',
    // other dev configs
  },
  staging: {
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'https://api-staging.todoapp.example.com',
    debug: false,
    // other staging configs
  },
  production: {
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'https://api.todoapp.example.com',
    debug: false,
    // other prod configs
  }
};

export default config[env];
```

## Environment-Specific Features

### Development
- Debug mode enabled
- Detailed error messages
- Hot reloading
- Verbose logging
- Less restrictive rate limiting
- Local database connection

### Staging
- Debug mode disabled
- Production-like error handling
- Moderate logging
- Production-like rate limiting
- Staging database connection
- Feature flags for testing

### Production
- Debug mode disabled
- Minimal error information to users
- Security-focused logging
- Strict rate limiting
- Production database connection
- Performance optimizations
- Security headers enabled

## Deployment Configuration

### Docker Environment Files

For containerized deployments, create separate environment files:

- `docker-compose.dev.yml` - Development environment
- `docker-compose.staging.yml` - Staging environment
- `docker-compose.prod.yml` - Production environment

### Environment Variables in Docker

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    env_file:
      - .env.${ENVIRONMENT:-development}
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-development}
```

## Security Considerations

- Never commit secret keys to version control
- Use strong, unique keys for each environment
- Rotate keys regularly
- Use different database credentials per environment
- Restrict access to production environment variables
- Use infrastructure-as-code for managing secrets

## Testing Across Environments

- Unit tests should run in isolation (no external dependencies)
- Integration tests may require environment-specific setup
- End-to-end tests should run against staging environment
- Performance tests should simulate production conditions