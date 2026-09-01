# Task CRUD API with Supabase Authentication

A simple FastAPI Task CRUD API with Supabase authentication, JWT-protected endpoints, reusable authentication dependencies, and Swagger Bearer authentication.

## Features

* User signup with Supabase Auth
* User login with email and password
* JWT access-token authentication
* Reusable authentication dependency
* Protected task CRUD endpoints
* User-specific task ownership
* Protected `/auth/logout` endpoint
* Public and protected example endpoints
* Swagger UI Bearer authentication
* HTTP 401 responses for missing or invalid tokens
* HTTP 400 validation responses
* Environment variables for Supabase configuration

## Tech Stack

* Python
* FastAPI
* Supabase
* PyJWT
* Uvicorn

## Project Structure

```text
FL04-task-crud-api/
├── auth.py
├── dependencies.py
├── main.py
├── protected.py
├── supabase_client.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Veduisback/FL04-task-crud-api.git
cd FL04-task-crud-api
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from `.env.example`.

```powershell
Copy-Item .env.example .env
```

Add your Supabase project credentials to `.env`.

Example:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

**Never commit `.env` or real Supabase credentials to GitHub.**

### 5. Start the API

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Authentication Flow

### Signup

```http
POST /auth/signup
```

Request:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

### Login

```http
POST /auth/login
```

Request:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

A successful login returns a Bearer access token.

Use the token in protected requests:

```http
Authorization: Bearer <access_token>
```

### Logout

```http
POST /auth/logout
```

Requires a valid Bearer token and returns:

```text
204 No Content
```

## API Endpoints

### Public

| Method | Endpoint       | Description        |
| ------ | -------------- | ------------------ |
| GET    | `/`            | API information    |
| GET    | `/health`      | Health check       |
| GET    | `/public/info` | Public information |

### Authentication

| Method | Endpoint       | Authentication        |
| ------ | -------------- | --------------------- |
| POST   | `/auth/signup` | Not required          |
| POST   | `/auth/login`  | Not required          |
| POST   | `/auth/logout` | Bearer token required |

### Protected

| Method | Endpoint             | Authentication        |
| ------ | -------------------- | --------------------- |
| GET    | `/protected/profile` | Bearer token required |
| GET    | `/tasks`             | Bearer token required |
| GET    | `/tasks/{task_id}`   | Bearer token required |
| POST   | `/tasks`             | Bearer token required |
| PUT    | `/tasks/{task_id}`   | Bearer token required |
| DELETE | `/tasks/{task_id}`   | Bearer token required |

## Swagger Authentication

Open:

```text
http://localhost:8000/docs
```

Click the **Authorize** button.

Enter the access token obtained from:

```text
POST /auth/login
```

Swagger will then send the Bearer token automatically when calling protected endpoints.

## Error Handling

The API uses:

* `400 Bad Request` for invalid request data
* `401 Unauthorized` for missing, invalid, or expired authentication tokens
* `404 Not Found` when a requested task does not exist
* `201 Created` when a task or user is successfully created
* `204 No Content` for successful logout and task deletion

## Security

Secrets are stored in environment variables and `.env` is excluded through `.gitignore`.

The repository contains only `.env.example` with placeholder values.

Do not publish:

```text
.env
```

or real Supabase keys.

## Running Tests Manually

The API can be tested through Swagger UI at:

```text
http://localhost:8000/docs
```

Recommended authentication checks:

1. Access a protected endpoint without a token → `401`
2. Access a protected endpoint with an invalid token → `401`
3. Login and obtain a valid access token
4. Authorize Swagger with the token
5. Access protected endpoints → successful response
6. Logout using the token → `204`

## Author

Vedang Jaiswal

Bangalore Institute of Technology — Computer Science & Engineering
