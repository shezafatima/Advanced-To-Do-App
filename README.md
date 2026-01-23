# Todo Full-Stack Web Application (Phase II)

A secure, multi-user, full-stack todo application with persistent storage, RESTful APIs, authentication, and responsive frontend.

## Features

- **User Authentication**: Secure JWT-based authentication with registration and login
- **Todo Management**: Full CRUD operations for personal todo items
- **Data Isolation**: Each user can only access their own todos
- **Responsive UI**: Works on desktop, tablet, and mobile devices
- **Persistent Storage**: Todos stored in PostgreSQL database
- **Security**: Rate limiting, input validation, and secure authentication
- **Environment Configuration**: Separate configurations for dev/staging/prod
- **Comprehensive API Documentation**: Well-documented RESTful API

## Tech Stack

- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Authentication**: JWT tokens with secure storage
- **Database**: Neon Serverless PostgreSQL
- **Styling**: Tailwind CSS for responsive design

## Prerequisites

- Node.js v18+
- Python 3.11+
- PostgreSQL (local or Neon account)
- Git
- Docker (optional, for local PostgreSQL)

## Phase II Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
git checkout 002-todo-fullstack-app
```

### 2. Backend Setup

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
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the backend directory, or use environment-specific files:
- `.env.development` for development
- `.env.staging` for staging
- `.env.production` for production

Basic `.env` configuration:
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here-32-characters-at-least
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
SERVER_HOST=localhost
SERVER_PORT=8000
DEBUG=true

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=DEBUG

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Security
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd ../frontend  # From backend directory
```

#### Install Frontend Dependencies
```bash
npm install
```

#### Set Up Environment Variables
Create environment-specific files in the frontend directory:
- `.env.local` for local development
- `.env.development` for development builds
- `.env.staging` for staging builds
- `.env.production` for production builds

Basic `.env.local` configuration:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_DEBUG=true
```

### 4. Database Setup

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

### 3. Access API Documentation
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`
- Raw OpenAPI specification: `http://localhost:8000/openapi.json`

## API Endpoints

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
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

## Security Features

- JWT-based authentication with secure token storage
- User data isolation - users can only access their own todos
- Rate limiting to prevent abuse
- Input validation and sanitization
- Secure password hashing
- SQL injection prevention through parameterized queries

## Testing

The application includes comprehensive testing for both backend and frontend:

- Backend: Unit and integration tests using pytest
- Frontend: Component tests and integration tests

To run tests:
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## Environment Configuration

The application supports multiple environments with specific configurations:

### Development
- Debug mode enabled
- Verbose logging
- Hot reloading
- Local database connection
- Less restrictive rate limiting

### Staging
- Debug mode disabled
- Moderate logging
- Staging database connection
- Production-like rate limiting

### Production
- Debug mode disabled
- Security-focused logging
- Production database connection
- Strict rate limiting
- Performance optimizations

## Architecture

The application follows a clean architecture pattern:

- **Models**: SQLModel entities in the backend (`src/models/`)
- **Services**: Business logic separated from API endpoints (`src/services/`)
- **API**: FastAPI routers handling HTTP requests (`src/api/`)
- **Components**: Reusable React components in the frontend (`src/components/`)
- **Context**: Global state management for authentication (`src/context/`)

## API Documentation

Comprehensive API documentation is available in multiple formats:

- Interactive documentation at `/docs` (Swagger UI)
- Alternative documentation at `/redoc` (ReDoc)
- Raw OpenAPI specification at `/openapi.json`
- Detailed documentation in `backend/docs/api.md`
- Implementation guide in `backend/docs/api-implementation.md`
- Environment configuration guide in `backend/docs/environment-setup.md`

## Project Structure

```
todo-fullstack-app/
├── backend/
│   ├── docs/                 # API documentation
│   ├── src/
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   ├── api/              # API endpoints
│   │   ├── database/         # Database configuration
│   │   └── main.py           # Application entry point
│   ├── tests/                # Backend tests
│   └── .env*                 # Environment configuration
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js app router pages
│   │   ├── components/       # React components
│   │   ├── services/         # API clients
│   │   └── context/          # React context providers
│   └── .env*                 # Environment configuration
├── shared/                   # Shared types and utilities
├── specs/                    # Feature specifications
└── history/                  # Development history
```

## Deployment

For production deployment:

1. Set up environment variables for production
2. Run database migrations
3. Build the frontend application
4. Serve both backend and frontend

The application is designed to be deployed on platforms like Vercel (frontend) and Railway/Hetzner (backend) or containerized with Docker.