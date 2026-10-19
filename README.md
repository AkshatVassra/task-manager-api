# Task Management Backend API (FastAPI)

A clean, modular RESTful backend API for Task Management built using **FastAPI** with **Pydantic** request validation and in-memory storage, developed through pair programming with an AI coding agent.

---

## 📁 Project Structure

```text
task-manager-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application, CORS, health check, router registration
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py             # Pydantic schemas, TaskStatus enum, and validation rules
│   ├── routes/
│   │   ├── __init__.py
│   │   └── task_routes.py      # RESTful API endpoints and HTTP status codes
│   └── services/
│       ├── __init__.py
│       └── task_service.py     # In-memory storage layer & CRUD business logic
├── tests/
│   ├── __init__.py
│   └── test_api.py             # Comprehensive test suite (FastAPI TestClient + unittest)
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation & prompt history
```

---

## 🚀 Getting Started

### 1. Requirements
- Python 3.10+
- Installed packages: `fastapi`, `uvicorn`, `pydantic`, `httpx`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend Server
From inside the `task-manager-api` directory:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Server URL: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc API Documentation: `http://127.0.0.1:8000/redoc`

### 4. Run Automated Tests
```bash
python -m unittest tests/test_api.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Service health check and API overview | `200 OK` |
| `POST` | `/api/v1/tasks` | Create a new task (validated) | `201 Created` |
| `GET` | `/api/v1/tasks` | Get all tasks (optional `?status=` filter) | `200 OK` |
| `GET` | `/api/v1/tasks/{id}` | Get specific task by ID | `200 OK` / `404 Not Found` |
| `PUT` | `/api/v1/tasks/{id}` | Update task details | `200 OK` / `404 Not Found` |
| `DELETE` | `/api/v1/tasks/{id}` | Delete task by ID | `204 No Content` / `404 Not Found` |

---

## 🧪 Testing with cURL / PowerShell

### 1. Create a Task
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks" \
     -H "Content-Type: application/json" \
     -d "{\"title\": \"Build Backend API\", \"description\": \"FastAPI with validation\", \"status\": \"pending\"}"
```

### 2. Get All Tasks
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/tasks"
```

### 3. Update a Task
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/tasks/<TASK_ID>" \
     -H "Content-Type: application/json" \
     -d "{\"status\": \"in_progress\"}"
```

### 4. Delete a Task
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/tasks/<TASK_ID>"
```

---

## 📝 AI Agent Prompting Process & Report

### 1. Prompts Used
- **Prompt 1 (Requirements & Architecture)**: "Design a clean folder structure and modular architecture for a Task Management backend API using FastAPI and Pydantic validation."
- **Prompt 2 (Schema & Models)**: "Create Pydantic models for Task with fields `id`, `title`, `description`, `status`, `created_at`. Include strict validations (non-empty title, status enum, max lengths) and separate schemas for creation, partial updates, and responses."
- **Prompt 3 (Service Layer)**: "Implement an in-memory CRUD service layer with thread-safe operations, status filtering, and O(1) ID lookups."
- **Prompt 4 (Routes & Error Handling)**: "Create FastAPI route controllers with standard REST status codes (201, 200, 204, 404, 422) and meaningful error responses."
- **Prompt 5 (Quality & Testing)**: "Write a comprehensive automated test suite covering all positive paths, validation errors, 404 handling, and lifecycle operations."

### 2. What Worked Well
- Using Pydantic v2 schemas gave instant automatic request validation and generated clear OpenAPI/Swagger documentation at `/docs`.
- Splitting code into clean MVC-style layers (`models`, `services`, `routes`) made each component focused, maintainable, and testable.
- The interactive `/docs` UI makes testing endpoints visually appealing for screenshots.

### 3. Issues Faced & How Agent Output Was Improved
- **Issue**: Need for strict validation without crashing on partial updates.
- **Improvement**: Created distinct schemas (`TaskCreate` requiring title vs. `TaskUpdate` with optional fields), ensuring partial updates don't wipe existing fields or require unnecessary payload data.
- **Issue**: Environment independence for testing without external tools.
- **Improvement**: Built the test suite using standard library `unittest` and `fastapi.testclient.TestClient`, eliminating the need for separate global package installations while running in sub-second time.
