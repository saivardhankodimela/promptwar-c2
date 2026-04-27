"""
Audit Logging Service
Provides structured audit logging via Google Cloud Logging.
"""

import os
import logging

logger = logging.getLogger("voter.ai.audit")


class AuditLogger:
    """
    Structured audit logger for tracking user interactions.
    Uses Google Cloud Logging when available, falls back to stdout.
    """

    def __init__(self) -> None:
        """Initialize Cloud Logging integration if available."""
        project_id = os.getenv("GCP_PROJECT_ID", "promptwars-c2")

        try:
            import google.cloud.logging as cloud_logging

            client = cloud_logging.Client(project=project_id)
            client.setup_logging()
            logger.info("Cloud Logging initialized (project: %s)", project_id)
        except Exception as e:
            logger.info("Cloud Logging unavailable, using stdout: %s", e)

    def log_interaction(
        self, user_id: str, level: str, intent: str
    ) -> None:
        """
        Log a user interaction for audit compliance.

        Args:
            user_id: The user's unique identifier.
            level: Detected knowledge level (beginner/intermediate/advanced).
            intent: Detected intent (learn/task/myth_check/quiz_request).
        """
        logger.info(
            "Interaction | user=%s | level=%s | intent=%s",
            user_id, level, intent,
        )

    def log_error(self, error_msg: str) -> None:
        """
        Log an error event.

        Args:
            error_msg: Description of the error.
        """
        logger.error("Error | %s", error_msg)
