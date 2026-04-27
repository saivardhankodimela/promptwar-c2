"""
GCS Service
Archives chat interactions to Google Cloud Storage for audit compliance.
"""

import os
import json
import logging
from google.cloud import storage

logger = logging.getLogger("voter.ai.gcs")


class GCSService:
    """
    Handles chat archival to Google Cloud Storage.
    Uses ADC for authentication — no API keys required.
    """

    def __init__(self) -> None:
        """Initialize the GCS client and configure the target bucket."""
        self.client = None
        project_id = os.getenv("GCP_PROJECT_ID", "promptwars-c2")
        self.bucket_name = os.getenv(
            "GCS_BUCKET_NAME", f"voter-ai-logs-{project_id}"
        )

        try:
            self.client = storage.Client(project=project_id)
            logger.info("GCS connected (bucket: %s)", self.bucket_name)
        except Exception as e:
            logger.warning("GCS client init failed: %s", e)

    def archive_chat(self, user_id: str, chat_data: dict) -> None:
        """
        Archive a chat interaction as a JSON file in GCS.

        Args:
            user_id: The user's unique identifier.
            chat_data: Dictionary containing query, response, and timestamp.
        """
        if not self.client:
            logger.debug("GCS client not available, skipping archival")
            return

        try:
            bucket = self.client.bucket(self.bucket_name)
            timestamp = chat_data.get("timestamp", "unknown")
            blob_path = f"chats/{user_id}/{timestamp}.json"
            blob = bucket.blob(blob_path)
            blob.upload_from_string(
                json.dumps(chat_data, ensure_ascii=False),
                content_type="application/json",
            )
            logger.debug("Chat archived to %s", blob_path)
        except Exception as e:
            logger.error("GCS upload failed: %s", e)
