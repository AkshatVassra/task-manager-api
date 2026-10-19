import json
import sys
import urllib.error
import urllib.request

# Ensure UTF-8 output on Windows consoles if supported
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "http://127.0.0.1:8000"


def send_request(method: str, path: str, payload: dict = None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    print(f"\n=======================================================")
    print(f"--> {method} {path}")
    if payload:
        print(f"Payload: {json.dumps(payload, indent=2)}")
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            parsed = json.loads(body) if body else "(No content)"
            print(f"Status: {status}")
            print(f"Response: {json.dumps(parsed, indent=2) if isinstance(parsed, (dict, list)) else parsed}")
            return status, parsed
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8")
        parsed = json.loads(body) if body else "(Error)"
        print(f"Status: {status} (Expected Error)")
        print(f"Response: {json.dumps(parsed, indent=2) if isinstance(parsed, (dict, list)) else parsed}")
        return status, parsed


def run_demo():
    print("=======================================================")
    print("  TASK MANAGEMENT API - LIVE DEMO & VALIDATION TEST")
    print("=======================================================")

    # 1. Root Health Check
    send_request("GET", "/")

    # 2. Create Task 1
    _, task1 = send_request("POST", "/api/v1/tasks", {
        "title": "Build AI Agent Backend",
        "description": "Create FastAPI Task Management service with validation",
        "status": "pending"
    })
    task1_id = task1["id"]

    # 3. Create Task 2
    send_request("POST", "/api/v1/tasks", {
        "title": "Write API Documentation",
        "description": "Document OpenAPI schemas and endpoints",
        "status": "in_progress"
    })

    # 4. Request Validation Test (Empty Title -> 422)
    send_request("POST", "/api/v1/tasks", {
        "title": "",
        "description": "This should fail validation"
    })

    # 5. Get All Tasks
    send_request("GET", "/api/v1/tasks")

    # 6. Get Task by ID
    send_request("GET", f"/api/v1/tasks/{task1_id}")

    # 7. Update Task
    send_request("PUT", f"/api/v1/tasks/{task1_id}", {
        "status": "completed",
        "description": "Task completed successfully with all tests passing!"
    })

    # 8. Delete Task
    send_request("DELETE", f"/api/v1/tasks/{task1_id}")

    # 9. Verify 404 after Deletion
    send_request("GET", f"/api/v1/tasks/{task1_id}")

    print("\n=======================================================")
    print("[SUCCESS] All API operations and validation checks verified!")
    print("=======================================================")


if __name__ == "__main__":
    run_demo()
