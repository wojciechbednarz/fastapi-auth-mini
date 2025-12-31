# FastAPI Auth Mini

A minimal FastAPI project demonstrating authentication, JWT access tokens, and user management with async SQLModel.

## Features
- User registration and login
- JWT-based authentication
- Password hashing (Argon2)
- Protected routes with FastAPI dependencies
- Async database access (SQLite, SQLModel)
- Alembic migrations

## Project Structure
```
app/
	__init__.py
	main.py
	auth.py
	db.py
	dependencies.py
	models.py
	schemas.py
```

## Tech Stack & Libraries
- FastAPI
- SQLModel (async)
- Alembic
- aiosqlite / asyncpg (DB drivers)
- PyJWT & jwt
- pwdlib (Argon2 password hashing)
- python-dotenv
- ruff (linting)

## Quick Start
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the application:
   ```sh
   uvicorn app.main:app --reload
   ```
3. API docs available at `/docs`.

---
This project is intended for learning and prototyping secure authentication flows with FastAPI.