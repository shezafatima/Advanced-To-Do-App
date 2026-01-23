# Environment Configuration

## Overview

This project uses environment-specific configurations for different deployment environments (development, staging, production). Configuration values are managed through environment variables loaded from `.env` files.

## Backend Configuration (.env files)

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

# Rate Limiting
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=60

# Security
ALLOWED_ORIGINS="https://todoapp.example.com"
SECURE_COOKIES=true
```

## Frontend Configuration (.env files)

### Development (.env.development)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=dev-secret-key-change-in-production
BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_DEBUG=true
```

### Staging (.env.staging)
```
NEXT_PUBLIC_API_BASE_URL=https://api-staging.todoapp.example.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://api-staging.todoapp.example.com
BETTER_AUTH_SECRET=staging-secret-key
BETTER_AUTH_URL=https://api-staging.todoapp.example.com
NEXT_PUBLIC_DEBUG=false
```

### Production (.env.production)
```
NEXT_PUBLIC_API_BASE_URL=https://api.todoapp.example.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://api.todoapp.example.com
BETTER_AUTH_SECRET=production-secret-key-keep-safe-and-secure
BETTER_AUTH_URL=https://api.todoapp.example.com
NEXT_PUBLIC_DEBUG=false
```

## Environment Loading Strategy

### Backend (Python/FastAPI)
The backend follows this hierarchy for loading configuration:

1. Environment variables (highest priority)
2. Environment-specific .env file based on ENVIRONMENT variable
3. Default .env file (lowest priority)

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

### Frontend (Next.js)
Next.js automatically loads environment files based on NODE_ENV:

- `development`: .env.development, .env.local, .env
- `production`: .env.production, .env.local, .env
- `test`: .env.test, .env (not .env.local)

## Configuration Management

### Docker Compose Configuration
For containerized deployments, create separate compose files:

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    build: ./backend
    env_file:
      - backend/.env.development
    environment:
      - ENVIRONMENT=development
  frontend:
    build: ./frontend
    env_file:
      - frontend/.env.development
    environment:
      - NODE_ENV=development
```

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    build: ./backend
    env_file:
      - backend/.env.production
    environment:
      - ENVIRONMENT=production
  frontend:
    build: ./frontend
    env_file:
      - frontend/.env.production
    environment:
      - NODE_ENV=production
```

## Security Best Practices

1. **Never commit secrets to version control**
   - Add all .env files to .gitignore
   - Only commit .env.example files with placeholder values

2. **Use different secrets per environment**
   - Unique JWT secrets for each environment
   - Different database credentials per environment
   - Separate API keys for different environments

3. **Regular key rotation**
   - Rotate secrets regularly, especially in production
   - Update staging secrets periodically as well
   - Use infrastructure as code to manage secrets

4. **Access control**
   - Restrict access to production environment variables
   - Use different levels of access for team members
   - Audit access to sensitive configuration values

## Environment-Specific Behavior

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