from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_run_requires_approval_then_approves():
    response = client.post(
        "/api/runs",
        json={"goal": "Research competitors and draft a launch plan for my SaaS product."},
    )
    assert response.status_code == 201
    run = response.json()
    assert run["status"] == "waiting_for_approval"
    assert run["approvals"]

    approved = client.post(f"/api/approvals/{run['id']}/approve", json={"reason": "Looks safe."})
    assert approved.status_code == 200
    assert approved.json()["status"] == "completed"


def test_register_login():
    email = "learner@example.com"
    password = "super-secret-password"
    registered = client.post("/api/auth/register", json={"email": email, "password": password})
    assert registered.status_code == 201
    assert registered.json()["access_token"]

    logged_in = client.post("/api/auth/login", json={"email": email, "password": password})
    assert logged_in.status_code == 200
    assert logged_in.json()["tenant_id"] == "demo-tenant"
