"""
Pytest configuration and shared fixtures.
Provides reusable test fixtures for API testing and orchestrator testing.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.agents.orchestrator import ElectionAgentOrchestrator


@pytest.fixture
def client():
    """Provide a FastAPI test client for API integration tests."""
    return TestClient(app)


@pytest.fixture
def orchestrator():
    """Provide an ElectionAgentOrchestrator instance for unit tests."""
    return ElectionAgentOrchestrator()
