# Quickstart Guide: Todo Full-Stack Web Application (Phase II)

**Feature**: 002-todo-fullstack-app
**Date**: 2026-01-11

## Overview

This guide provides step-by-step instructions to set up the development environment for the Todo Full-Stack Web Application. The application consists of a Next.js frontend, FastAPI backend, with Neon PostgreSQL database and Better Auth for authentication.

## Prerequisites

- Node.js v18+ (for frontend development)
- Python 3.11+ (for backend development)
- Docker and Docker Compose (for local database)
- Git
- A Neon PostgreSQL account (free tier available)

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
git checkout 002-todo-fullstack-app
```

### 2. Set Up Backend Environment

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Backend Dependencies
```bash
pip install fastapi uvicorn sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv psycopg[binary]
```

#### Set Up Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-secret-key-here-32-characters-at-least
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours as specified in clarifications
NEON_DATABASE_URL=your-neon-database-url
```

### 3. Set Up Frontend Environment

#### Navigate to Frontend Directory
```bash
cd ../frontend  # From backend directory
```

#### Install Frontend Dependencies
```bash
npm install next@latest react@latest react-dom@latest @types/react@latest @types/node@latest @types/react-dom@latest typescript eslint-config-next
npm install better-auth @better-auth/react
```

#### Set Up Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:8000
```

### 4. Set Up Database

#### Option A: Local PostgreSQL with Docker
```bash
# From project root
docker-compose up -d
```

#### Option B: Neon PostgreSQL (Recommended)
1. Create a free Neon account at https://neon.tech/
2. Create a new project
3. Copy the connection string and update your backend `.env` file

#### Initialize Database Tables
```bash
# With backend virtual environment activated
cd backend
python -c "
from sqlmodel import SQLModel
from database.session import engine
from models.user import User
from models.todo import Todo

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()
"
```

## Running the Application

### 1. Start the Backend Server

```bash
# From backend directory with virtual environment activated
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### 2. Start the Frontend Server

```bash
# From frontend directory
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info

### Todo Endpoints
- `GET /todos/` - Get all todos for current user
- `POST /todos/` - Create a new todo
- `GET /todos/{todo_id}` - Get a specific todo
- `PUT /todos/{todo_id}` - Update a specific todo
- `DELETE /todos/{todo_id}` - Delete a specific todo
- `PATCH /todos/{todo_id}/toggle` - Toggle todo completion status

## Development Commands

### Backend Development
```bash
# Run backend with auto-reload
uvicorn src.main:app --reload

# Run backend tests
pytest

# Format backend code
black src/
```

### Frontend Development
```bash
# Run frontend development server
npm run dev

# Build frontend for production
npm run build

# Run frontend tests
npm run test

# Format frontend code
npm run format
```

## Testing the Application

### 1. Register a New User
Send a POST request to `/auth/register` with:
```json
{
  "email": "test@example.com",
  "password": "SecurePass123!"
}
```

### 2. Login to Get JWT Token
Send a POST request to `/auth/login` with:
```json
{
  "email": "test@example.com",
  "password": "SecurePass123!"
}
```

### 3. Create a Todo
Send a POST request to `/todos/` with:
```json
{
  "title": "Sample Todo",
  "description": "This is a sample todo item"
}
```

### 4. Verify Data Isolation
- Create a second user account
- Verify that the second user cannot access the first user's todos

## Database Migrations

For future database schema changes, use Alembic (to be set up later):

```bash
# Initialize (first time only)
alembic init migrations

# Create a migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify your database is running and accessible
   - Check that your DATABASE_URL is correct
   - Ensure firewall rules allow connections

2. **Authentication Issues**
   - Verify SECRET_KEY is consistent between frontend and backend
   - Check that JWT tokens are being properly stored and sent

3. **CORS Issues**
   - Ensure your frontend URL is in the backend's CORS allowed origins

### Resetting the Development Environment

```bash
# Stop all services
# Kill backend and frontend processes

# Reset database
# Drop and recreate your database

# Clear frontend cache
rm -rf node_modules package-lock.json
npm install

# Clear backend cache
rm -rf __pycache__ backend/__pycache__
```

## Next Steps

1. Review the API documentation available at `http://localhost:8000/docs`
2. Explore the data models in `backend/src/models/`
3. Begin implementing frontend components in `frontend/src/components/`
4. Follow the task breakdown in `specs/002-todo-fullstack-app/tasks.md` (to be generated)