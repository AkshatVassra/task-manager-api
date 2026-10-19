import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.services.task_service import task_service


class TestTaskManagementAPI(unittest.TestCase):
    """Test suite covering all endpoints, status codes, and validations."""

    def setUp(self):
        """Reset task store and create a fresh test client before each test."""
        task_service.clear()
        self.client = TestClient(app)

    def tearDown(self):
        """Clean up after test."""
        task_service.clear()

    def test_01_root_health_check(self):
        """Verify root endpoint returns healthy status and docs links."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "Task Management API")
        self.assertIn("endpoints", data)

    def test_02_create_task_success(self):
        """Verify successful task creation with 201 Created and full task schema."""
        payload = {
            "title": "Complete backend assignment",
            "description": "Build FastAPI Task Management API with validation",
            "status": "pending",
        }
        response = self.client.post("/api/v1/tasks", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["description"], payload["description"])
        self.assertEqual(data["status"], "pending")
        self.assertTrue(len(data["id"]) > 0)
        self.assertIn("created_at", data)

    def test_03_create_task_validation_errors(self):
        """Verify validation errors return 422 Unprocessable Entity."""
        # 1. Empty title
        resp1 = self.client.post("/api/v1/tasks", json={"title": ""})
        self.assertEqual(resp1.status_code, 422)

        # 2. Missing title
        resp2 = self.client.post("/api/v1/tasks", json={"description": "No title"})
        self.assertEqual(resp2.status_code, 422)

        # 3. Invalid status enum value
        resp3 = self.client.post(
            "/api/v1/tasks",
            json={"title": "Test Title", "status": "invalid_status_value"},
        )
        self.assertEqual(resp3.status_code, 422)

    def test_04_get_all_tasks(self):
        """Verify fetching all tasks."""
        self.client.post("/api/v1/tasks", json={"title": "Task A"})
        self.client.post("/api/v1/tasks", json={"title": "Task B"})

        response = self.client.get("/api/v1/tasks")
        self.assertEqual(response.status_code, 200)
        tasks = response.json()
        self.assertEqual(len(tasks), 2)
        titles = [t["title"] for t in tasks]
        self.assertIn("Task A", titles)
        self.assertIn("Task B", titles)

    def test_05_get_task_by_id(self):
        """Verify fetching task by ID and 404 for non-existent ID."""
        create_resp = self.client.post(
            "/api/v1/tasks",
            json={"title": "Specific Task", "description": "Details here"},
        )
        task_id = create_resp.json()["id"]

        # Valid ID -> 200 OK
        get_resp = self.client.get(f"/api/v1/tasks/{task_id}")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json()["id"], task_id)

        # Invalid ID -> 404 Not Found
        not_found_resp = self.client.get("/api/v1/tasks/non-existent-uuid-1234")
        self.assertEqual(not_found_resp.status_code, 404)
        self.assertIn("detail", not_found_resp.json())

    def test_06_update_task(self):
        """Verify partial update returns 200 and 404 for invalid ID."""
        create_resp = self.client.post(
            "/api/v1/tasks",
            json={"title": "Initial Title", "status": "pending"},
        )
        task_id = create_resp.json()["id"]

        # Partial update
        update_payload = {
            "title": "Updated Title",
            "status": "in_progress",
        }
        update_resp = self.client.put(f"/api/v1/tasks/{task_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200)
        updated = update_resp.json()
        self.assertEqual(updated["title"], "Updated Title")
        self.assertEqual(updated["status"], "in_progress")

        # 404 for updating unknown task
        missing_resp = self.client.put(
            "/api/v1/tasks/missing-id",
            json={"title": "New Title"},
        )
        self.assertEqual(missing_resp.status_code, 404)

    def test_07_delete_task(self):
        """Verify deletion returns 204 and subsequent queries return 404."""
        create_resp = self.client.post(
            "/api/v1/tasks",
            json={"title": "Task to Delete"},
        )
        task_id = create_resp.json()["id"]

        # 204 No Content on delete
        del_resp = self.client.delete(f"/api/v1/tasks/{task_id}")
        self.assertEqual(del_resp.status_code, 204)

        # Subsequent GET -> 404 Not Found
        get_resp = self.client.get(f"/api/v1/tasks/{task_id}")
        self.assertEqual(get_resp.status_code, 404)

        # Second DELETE -> 404 Not Found
        del_again = self.client.delete(f"/api/v1/tasks/{task_id}")
        self.assertEqual(del_again.status_code, 404)


if __name__ == "__main__":
    unittest.main()
