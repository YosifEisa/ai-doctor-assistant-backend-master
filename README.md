# AI Doctor Assistant Backend

A FastAPI-based REST API for managing patient health records and medical information.

## Features

- **Authentication** - JWT-based authentication with registration, login, and password reset via OTP
- **User Management** - User profile CRUD operations
- **Health Profile** - Lifestyle and health status tracking
- **Family Members** - Link registered users as family members
- **Medications** - Track current medications with dosage and frequency
- **Allergies** - Record known allergies
- **Chronic Diseases** - Track chronic and genetic conditions
- **Lab & Scan Tests** - Store lab and scan test records

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT (OAuth2 Password Flow)
- **Password Hashing**: Argon2

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-doctor-assistant-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
# Development
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, access the interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

1. Register a new user at `POST /auth/register`
2. Login at `POST /auth/login` (use phone number as username)
3. Use the returned `access_token` in the `Authorization` header:
   ```
   Authorization: Bearer <access_token>
   ```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /auth/register` | Register new user |
| `POST /auth/login` | Login and get access token |
| `POST /auth/forgot-password` | Request password reset OTP |
| `POST /auth/verify-otp` | Verify OTP code |
| `POST /auth/change-password` | Change password with OTP |
| `GET /users/me` | Get current user profile |
| `PUT /users/me` | Update current user profile |
| `DELETE /users/me` | Delete current user account |
| `/health-profile` | Health profile CRUD |
| `/family-members` | Family members CRUD |
| `/medications` | Medications CRUD |
| `/allergies` | Allergies CRUD |
| `/diseases` | Chronic diseases CRUD |
| `/tests` | Lab & scan tests CRUD |

## Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./doctor_assistant.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
OTP_EXPIRY_MINUTES=10
```
