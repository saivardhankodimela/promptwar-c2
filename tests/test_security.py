import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_security_headers_present():
    """
    Ensures all 100% Security Score headers are injected.
    """
    response = client.get("/health")
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in response.headers
    assert "Strict-Transport-Security" in response.headers

def test_rate_limiting_trigger():
    """
    Simulates a rapid burst of requests to verify the 429 protector.
    """
    # We trigger 31 requests (limit is 30 in main.py)
    for _ in range(30):
        client.get("/health")
    
    response = client.get("/health")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.text

def test_api_v1_isolation():
    """
    Verifies the new modular routing is functional.
    """
    response = client.get("/api/v1/health") # New route through router
    # We didn't explicitly add /health to router, but we should test the prefix
    # Actually let's test a chat POST
    response = client.post("/api/v1/chat", json={
        "user_id": "test_user",
        "query": "hello"
    })
    assert response.status_code == 200
