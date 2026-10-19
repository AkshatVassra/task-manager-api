from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.task_routes import router as task_router

app = FastAPI(
    title="Task Management API",
    description="A clean, robust Task Management REST API built with FastAPI, Pydantic validation, and in-memory storage.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for local testing and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(task_router)


@app.get("/", tags=["Health"])
def root_endpoint():
    """Root health-check endpoint providing API status and documentation links."""
    return {
        "service": "Task Management API",
        "status": "healthy",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "create_task": "POST /api/v1/tasks",
            "get_all_tasks": "GET /api/v1/tasks",
            "get_task_by_id": "GET /api/v1/tasks/{id}",
            "update_task": "PUT /api/v1/tasks/{id}",
            "delete_task": "DELETE /api/v1/tasks/{id}",
        },
    }
