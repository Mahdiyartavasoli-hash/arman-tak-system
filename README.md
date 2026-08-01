# Arman Tak Factory Management System 🏗️

An enterprise-grade, high-performance Backend REST API system engineered for managing industrial machinery operations, logging daily production metrics, and processing asynchronous background tasks.

Designed and optimized following modern European enterprise software standards (**FastAPI, PostgreSQL, Redis, Celery, Docker, Pytest**).

---

## ✨ Key Features

- **Object-Oriented Programming (OOP):** Modular domain architecture for managing industrial machine models and operations.
- **System Logging & File Handling:** Live operational status logging and historical tracking system.
- **External API Integration:** Asynchronous external API connection (e.g., Crypto market metrics for dynamic pricing factors).
- **RESTful API Engineering:** High-performance asynchronous routes using FastAPI and Pydantic V2 validation.
- **Relational Database Management:** Production-ready PostgreSQL database with structural schema constraints and indexing.
- **Authentication & Security:** OAuth2 authentication pipeline with JWT bearer tokens and password hashing.
- **Asynchronous Task Architecture:** Distributed background job processing with **Celery** and **Redis** for heavy analytics computations.
- **Automated Testing:** Comprehensive behavioral unit and integration test coverage powered by **Pytest**.
- **Containerized Infrastructure:** Production environment orchestration via **Docker** and **Docker Compose**.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python 3.14+)
- **Database:** PostgreSQL (Production) / SQLite (Dev/Testing)
- **Task Queue & Broker:** Celery + Redis
- **Containerization:** Docker & Docker Compose
- **Testing Suite:** Pytest
- **Security:** Passlib (Bcrypt), PyJWT

---

## 🚀 Quick Start & Installation

### Option 1: Production Setup (Docker Compose)
Launch the entire system (API, database, Redis broker) in isolated containers:
```bash
docker compose up -d --build
```

### Option 2: Development Setup (Local)

1. **Clone the repository and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Redis & PostgreSQL infrastructure via Docker:**
   ```bash
   docker compose up -d db redis
   ```

4. **Run Celery Worker (In a separate terminal):**
   ```bash
   # Linux / macOS:
   celery -A celery_app.celery_app worker --loglevel=info

   # Windows:
   celery -A celery_app.celery_app worker --loglevel=info -P threads
   ```

5. **Run the FastAPI Development Server:**
   ```bash
   uvicorn server:server --reload
   ```

---

## 🧪 Running Automated Tests

Execute the full automated test suite using `pytest`:
```bash
pytest -vv
```

---

## 📑 Interactive API Documentation

Once the server is running, access the live interactive OpenAPI/Swagger documentation at:
- **Swagger UI:** `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`
- **ReDoc:** `[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)`
