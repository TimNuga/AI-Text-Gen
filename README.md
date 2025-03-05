# AI-Powered Text Generation API

This repository provides a Flask application that:
- Exposes **JWT-protected** endpoints for user registration, login, and AI-driven text generation.
- Uses **OpenAI** to generate text from a prompt.
- Stores generated texts in a **PostgreSQL** database.
- Supports **Docker** and **Docker Compose** for containerized deployment and testing.

## Table of Contents

1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [Setup & Configuration](#setup--configuration)  
4. [Database Migrations (Alembic)](#database-migrations-alembic)  
5. [Running the Application](#running-the-application)  
   - [Local (Without Docker)](#local-without-docker)  
   - [Docker Compose (Development)](#docker-compose-development)  
6. [Testing](#testing)  
   - [Local Testing With a Dedicated Test DB](#local-testing-with-a-dedicated-test-db)  
   - [Docker Compose Testing](#docker-compose-testing)  
7. [API Endpoints](#api-endpoints)  
8. [Additional Notes](#additional-notes)

---

## 1. Overview

The **AI-Powered Text Generation API** offers the following features:

- **User Registration & Login**: JWT-based auth ensures secure access to endpoints.  
- **Text Generation**: Sends prompts to OpenAI’s text completion endpoint.  
- **CRUD on Stored Texts**: Users can retrieve, update, and delete their previously generated responses.  
- **PostgreSQL Integration**: Database schemas managed via SQLAlchemy.  
- **Containerization**: Docker & Docker Compose for easy setup in various environments.  
- **Comprehensive Testing**: Pytest-based suite with optional Docker-based test environment.

---

## 2. Project Structure

A typical directory layout:

. 
├── app │ 
        ├── init.py │ 
        ├── config.py │ 
        ├── models.py │ 
        ├── validation.py │ 
        ├──routes |
                  ├──init.py
                  ├──auth_routes.py
                  ├──generated_text_routes.py
                  └──user_routes.py
        ├──services |
                    ├──init.py
                    ├──ai_service.py
                    └──user_service.py
        ├──repositories |
                        ├──init.py
                        ├──generated_text_repository.py
                        └──user_repository.py
        ├──providers |
                     ├──init.py
                     ├──base_ai_provider.py
                     └──openai_provider.py
        └── main.py 
├── tests │ 
          ├── init.py │ 
          ├── conftest.py │ 
          ├── test_api │
                       ├──test_auth_api.py
                       ├──test_generate_text.py
                       └──test_user_api.py
          ├── test_repositories |
                                ├──test_generated_text_repository.py
                                └──test_user_repository.py
          ├──test_services |
                           ├──test_ai_service.py
                           └──test_user_service.py
├── .env (example environment file for dev) 
├── .env.test (example environment file for testing) 
├── docker-compose.yml 
├── docker-compose.test.yml 
├── Dockerfile 
├── requirements.txt 
└── README.md


### Notable Files/Folders
- **`app/config.py`**: Loads environment variables and sets up Flask config.  
- **`app/models.py`**: Defines `User` and `GeneratedText` models, plus SQLAlchemy integration.  
- **`app/routes`**: All API endpoints (register, login, generate-text, CRUD).  
- **`app/main.py`**: App factory (create_app) and the main entry point.  
- **`tests/`**: Pytest-based test suite, including fixtures and test modules.  
- **`docker-compose.yml`**: Defines containers for PostgreSQL and the Flask app (dev or production usage).  
- **`docker-compose.test.yml`**: Defines containers specifically for running tests (test DB, test environment).

---

## 3. Setup & Configuration

### Environment Variables
This project depends on environment variables for database credentials, JWT secrets, and your OpenAI API key. You can specify these in:

- **`.env`** (for development/production)  
- **`.env.test`** (for testing)

#### Example `.env` File

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY=super-secret-key
JWT_SECRET_KEY=super-jwt-secret-key
OPENAI_API_KEY=your_openai_api_key
```

#### Example `.env.test` File
```bash
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_password
POSTGRES_DB=ai_test_db
POSTGRES_HOST=db_test
POSTGRES_PORT=5432

SECRET_KEY=super-secret-test-key
JWT_SECRET_KEY=super-jwt-secret-test-key
OPENAI_API_KEY=fake_test_key
```

## 4. Database Migrations (Alembic)

This project uses **Alembic** to manage database schema changes over time. Below are the key commands you’ll need:

1. **Initial Setup**  
   - Install Alembic (already in `requirements.txt`).
   - If you haven’t already, you can initialize Alembic in your local environment by running:
```bash
alembic init alembic
```
     *(This is already done in this repo, so you should see an `alembic/` folder and `alembic.ini`.)*

2. **Autogenerate New Migrations**  
   Whenever you change your SQLAlchemy models:
```bash
alembic revision --autogenerate -m "Your descriptive message"
```

   Alembic will create a new file in alembic/versions/. Inspect it to confirm it matches your intended schema changes.

3. **Apply Migrations**
   To bring your DB to the latest schema:

```bash
alembic upgrade head
```

   If you need to revert to a previous revision:

```bash
alembic downgrade <revision>
```

   or to go all the way back to an empty DB:

```bash
alembic downgrade base
```

## 5. Running the Application

### 5.1 Local (Without Docker)
1. Install PostgreSQL (if not already) and ensure it’s running.
2. Create a database (e.g., ai_text_gen_db) and user matching your .env credentials.
3. Run Alembic migrations to ensure your local DB has the latest schema:
```bash
alembic upgrade head
```
4. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
5. Run the app:
```bash
python -m app.main
```
6. Access at http://127.0.0.1:5000.

### 5.2 Docker Compose (Development)
1. Update .env with your dev environment variables.
2. Run:
```bash
docker compose up --build
```
If you’re on an older Docker version, use docker-compose up --build
3. Access at http://localhost:5000.
4. Data Persistence: By default, the Postgres container uses a named volume (e.g., db_data) defined in docker-compose.yml, preserving data across container restarts.

## 6. Testing

### 6.1 Local Testing With a Dedicated Test DB
If you prefer running tests on your host machine:

1. Create a test DB (e.g., `ai_text_gen_test_db`) in Postgres
2. Update `.env.test` with the test DB credentials.
3. Install dev dependencies (e.g., pytest):
```bash
pip install -r requirements.txt
```
4. Run:
```bash
pytest --disable-warnings -s
```
This will:
- Load `.env.test` (via `conftest.py` or `pytest-dotenv`, if configured).
- Spin up a Flask test client, connect to the test db, create tables, run all tests, then tear down.

### 6.2 Docker Compose Testing
We also provide a docker-compose.test.yml for running tests in containers, ensuring a reproducible environment (especially useful for CI/CD).

1. Check .env.test ensures credentials match what’s in docker-compose.test.yml.
2. Run:
```bash
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```
This:
- Starts a db_test container with Postgres.
- Builds a web_test container running pytest --disable-warnings -s.
- Shuts down automatically when tests finish (due to --abort-on-container-exit).

## 7. API Endpoints
Base URL: http://localhost:5000 (or http://127.0.0.1:5000 if local)

1. POST /register
   Request Body:
   ```json
   {
    "username": "myuser",
    "password": "mypassword"
   }
   ```
   Response: 201 Created on success, 400 if user exists.

2. POST /login
   Request Body:
   ```json
   {
    "username": "myuser",
    "password": "mypassword"
   }
   ```
   Response: 200 OK with { "access_token": "..." } or 401 on invalid credentials.

3. POST /generate-text (JWT Protected)
   ```json
   {
    "prompt": "Write a poem about cats."
    }
   ```
   Returns a 201 with stored data, or 500 if OpenAI errors.

4. GET /generated-text/<id> (JWT Protected)
   Retrieves a stored AI response by ID. Must belong to the user.

5. PUT /generated-text/<id> (JWT Protected)
   Updates stored prompt/response.

6. DELETE /generated-text/<id> (JWT Protected)
   Deletes the record.

### JWT Usage:
Send the token in the Authorization header:
```makefile
Authorization: Bearer <access_token>
```

## 8. Additional Notes
- Mocking OpenAI: Our tests illustrate how to mock `openai.Completion.create()` with `unittest.mock.patch` or via a fixture, avoiding real API calls.
- Production Considerations:
    - Use a secure `SECRET_KEY` and `JWT_SECRET_KEY`.
    - Serve over HTTPS.
    - Use Gunicorn or another production WSGI server for better performance.

Enjoy the AI-Powered Text Generation API! If you encounter any issues, please open an issue or contribute improvements via pull requests.