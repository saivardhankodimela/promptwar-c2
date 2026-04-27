"""
Firestore Service
Manages user state persistence using Google Cloud Firestore with ADC.
"""

import os
import logging
from google.cloud import firestore

logger = logging.getLogger("voter.ai.firestore")

# Default user state template
DEFAULT_USER_STATE = {
    "level": "beginner",
    "progress": "Start",
    "location": "India",
    "current_step": 0,
}


class FirestoreService:
    """
    Handles user state persistence in Firestore.
    Falls back to in-memory storage when Firestore is unavailable.
    """

    def __init__(self) -> None:
        """Initialize the Firestore client using ADC."""
        self.db = None
        self.local_db: dict = {}
        project_id = os.getenv("GCP_PROJECT_ID", "promptwars-c2")

        try:
            self.db = firestore.Client(project=project_id)
            logger.info("Firestore connected (project: %s)", project_id)
        except Exception as e:
            logger.warning("Firestore init failed, using local memory: %s", e)

    def get_user_state(self, user_id: str) -> dict:
        """
        Retrieve user state from Firestore or local fallback.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            Dictionary containing user level, progress, and location.
        """
        if not self.db:
            return self.local_db.get(user_id, DEFAULT_USER_STATE.copy())

        doc_ref = self.db.collection("users").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return DEFAULT_USER_STATE.copy()

    def update_user_state(self, user_id: str, state_updates: dict) -> None:
        """
        Update user state in Firestore or local fallback.

        Args:
            user_id: Unique identifier for the user.
            state_updates: Dictionary of fields to update.
        """
        if not self.db:
            current_state = self.local_db.get(user_id, DEFAULT_USER_STATE.copy())
            current_state.update(state_updates)
            self.local_db[user_id] = current_state
            return

        doc_ref = self.db.collection("users").document(user_id)
        doc_ref.set(state_updates, merge=True)
        logger.info("User state updated for %s", user_id)
