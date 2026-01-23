# Quickstart Guide for Phase 2 - Advanced Todo Features and Professional UI

## Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL-compatible database (Neon recommended)
- Git for version control

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd hackathon-2
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Then update with your database credentials
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local  # Update with your API base URL
```

### 4. Database Setup
```bash
cd backend
python -c "from sqlmodel import create_engine; from src.models.todo import Todo; from src.models.user import User; from src.database.session import engine; Todo.metadata.create_all(engine); User.metadata.create_all(engine); print('Tables created successfully')"
```

## Running the Application

### 1. Start Backend
```bash
cd backend
python -m uvicorn src.main:app --reload
```
Backend will be available at `http://localhost:8000`

### 2. Start Frontend
```bash
cd frontend
npm run dev
```
Frontend will be available at `http://localhost:3000`

## Key Endpoints

### Backend API
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `GET /todos/` - Get user's tasks
- `POST /todos/` - Create a new task
- `PUT /todos/{id}` - Update a task
- `DELETE /todos/{id}` - Delete a task
- `PATCH /todos/{id}/toggle` - Toggle task completion

### New Phase 2 Endpoints
- `GET /profiles/me` - Get user profile
- `PUT /profiles/me` - Update user profile
- `POST /todos/share` - Share a task with another user
- `GET /analytics/completion` - Get task completion stats
- `GET /todos/filter` - Filter tasks by criteria

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiry time

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL` - Backend API URL (default: http://localhost:8000)

## Development Commands

### Backend
- `pytest` - Run backend tests
- `python -m black .` - Format Python code
- `mypy .` - Run type checking

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run test` - Run frontend tests
- `npm run lint` - Lint the code

## Key Features Implementation

### 1. Advanced Task Management
Tasks now support:
- Priority levels (low, medium, high)
- Tags with color indicators
- Due dates with date picker
- Recurring tasks (daily, weekly, monthly)

### 2. User Profiles
Profile management includes:
- Display name customization
- Language preference (English/Urdu)
- Notification settings
- Avatar upload

### 3. Collaboration
- Task sharing with role-based access (Owner, Editor, Viewer)
- Visual indicators for shared tasks
- Permission enforcement at API and UI levels

### 4. Internationalization
- Runtime language switching
- RTL layout support for Urdu
- Proper text direction and spacing

### 5. Professional UI
- Dark-first theme with gradient backgrounds
- Consistent card-based layout
- Smooth animations and micro-interactions
- Responsive design across devices