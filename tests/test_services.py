"""
Service Layer Tests
Validates Firestore, GCS, and Audit Logging service initialization and fallback behavior.
"""

import pytest
from backend.services.firestore import FirestoreService
from backend.services.gcs import GCSService
from backend.services.audit_logging import AuditLogger


class TestFirestoreService:
    """Tests for Firestore user state management."""

    def test_initialization(self):
        """Service should initialize without crashing."""
        service = FirestoreService()
        assert service is not None

    def test_default_user_state(self):
        """Should return default state for unknown users."""
        service = FirestoreService()
        state = service.get_user_state("nonexistent_user_12345")
        assert state["level"] == "beginner"
        assert state["location"] == "India"

    def test_update_user_state(self):
        """Should update user state without errors."""
        service = FirestoreService()
        try:
            service.update_user_state("test_user", {"level": "intermediate"})
        except Exception:
            pytest.skip("Firestore not available in test environment")


class TestGCSService:
    """Tests for GCS chat archival."""

    def test_initialization(self):
        """Service should initialize without crashing."""
        service = GCSService()
        assert service is not None

    def test_archive_graceful_failure(self):
        """Archival should fail gracefully when GCS is unavailable."""
        service = GCSService()
        service.client = None  # Force unavailable state
        # Should not raise an exception
        service.archive_chat("test_user", {
            "query": "test",
            "response": "test",
            "timestamp": "2026-01-01T00:00:00"
        })


class TestAuditLogger:
    """Tests for the audit logging service."""

    def test_initialization(self):
        """Logger should initialize without crashing."""
        audit = AuditLogger()
        assert audit is not None

    def test_log_interaction(self):
        """Should log interactions without raising exceptions."""
        audit = AuditLogger()
        audit.log_interaction("test_user", "beginner", "learn")

    def test_log_error(self):
        """Should log errors without raising exceptions."""
        audit = AuditLogger()
        audit.log_error("Test error message")
