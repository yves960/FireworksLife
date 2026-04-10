# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A full-stack blog system built with FastAPI (backend) and Vue 3 (frontend). Supports Markdown content, comments, likes, categories, and user authentication.

## Development Commands

### Backend (from `backend/` directory)
```bash
# Create and activate virtual environment (Python 3.11 or 3.12 recommended)
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Initialize database
python -m app.db.init_db

# Run development server (runs on http://localhost:8002)
python run.py
```

### Frontend (from `frontend/` directory)
```bash
# Install dependencies
npm install

# Run development server (runs on http://localhost:3000)
npm run dev

# Build for production
npm run build
```

### Docker
```bash
docker-compose up -d    # Start all services
docker-compose down     # Stop services
```

## Architecture

### Backend Structure (`backend/app/`)
- **api/** - FastAPI route handlers (auth, users, posts, comments, likes, categories, stats)
- **models/** - SQLAlchemy ORM models (user, post, comment, like, category)
- **schemas/** - Pydantic models for request/response validation
- **core/** - Configuration and security (JWT, password hashing)
- **db/** - Database connection, initialization, and migrations
- **services/** - Business logic (e.g., markdown_service for rendering with XSS protection)

### Frontend Structure (`frontend/src/`)
- **views/** - Page components (HomeView, PostDetailView, LoginView, RegisterView, AdminView)
- **components/** - Reusable Vue components (CommentItem, ParticleBackground)
- **router/** - Vue Router configuration with auth guard for admin route
- **store/** - Pinia stores for state management
- **api/** - Axios instance with interceptors and API functions

### Key Design Patterns
- Backend uses SQLAlchemy ORM with SQLite (WAL mode enabled for better concurrency)
- Frontend proxies `/api` requests to backend via Vite dev server
- JWT tokens stored in localStorage, attached to requests via Axios interceptor
- 401 responses trigger automatic redirect to login page
- Markdown content is sanitized with bleach before rendering

## API Endpoints

Access interactive docs at http://localhost:8002/docs when backend is running.

- **Auth**: `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`
- **Users**: `/api/users/register`
- **Posts**: `/api/posts` (CRUD with category filtering)
- **Comments**: `/api/comments/post/{post_id}`, nested replies up to 3 levels
- **Likes**: `/api/likes/like/{post_id}`, `/api/likes/status/{post_id}`
- **Categories**: `/api/categories` (CRUD)
- **Stats**: `/api/stats/dashboard`

## Environment Variables

Backend (`.env` in `backend/`):
- `DATABASE_URL` - SQLite path (default: `sqlite:///./blog.db`)
- `SECRET_KEY`, `JWT_SECRET` - Authentication secrets
- `SMTP_*` - Email configuration (optional)
- `WECHAT_*` - WeChat OAuth (optional)

Frontend (`.env` in `frontend/`):
- `VITE_API_URL` - Backend API URL

## Python Version

Use Python 3.11 or 3.12. Python 3.14 has compatibility issues. See `backend/PYTHON_VERSION.md` for details.