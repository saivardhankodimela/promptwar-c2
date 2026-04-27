"""
Async Firestore Service
Uses google-cloud-firestore AsyncClient for non-blocking I/O.
"""

import os
import logging
from google.cloud import firestore

logger = logging.getLogger("voter.ai.firestore")

DEFAULT_USER_STATE = {
    "level": "beginner",
    "progress": "Electoral Roll",
    "location": "India",
    "current_step": 1,
}

class FirestoreService:
    """
    Handles non-blocking user state persistence.
    """
    def __init__(self) -> None:
        self.db = None
        project_id = os.getenv("GCP_PROJECT_ID", "promptwars-c2")
        try:
            # Expert Move: Using AsyncClient for non-blocking operations
            self.db = firestore.AsyncClient(project=project_id)
            logger.info(f"Async Firestore initialized for project {project_id}")
        except Exception as e:
            logger.error(f"Async Firestore initialization failed: {e}")

    async def get_user_state(self, user_id: str) -> dict:
        """
        Asynchronously retrieve user state.
        """
        if not self.db:
            return DEFAULT_USER_STATE.copy()
            
        try:
            doc_ref = self.db.collection("users").document(user_id)
            doc = await doc_ref.get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            logger.warning(f"Firestore read error: {e}")
            
        return DEFAULT_USER_STATE.copy()

    async def update_user_state(self, user_id: str, state_updates: dict) -> None:
        """
        Asynchronously update user state.
        """
        if not self.db:
            return

        try:
            doc_ref = self.db.collection("users").document(user_id)
            await doc_ref.set(state_updates, merge=True)
            logger.debug(f"User state updated for {user_id}")
        except Exception as e:
            logger.error(f"Firestore write error: {e}")
