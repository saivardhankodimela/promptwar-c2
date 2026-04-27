import os
from google.cloud import firestore
from google.oauth2 import service_account

class FirestoreService:
    def __init__(self):
        self.db = None
        project_id = os.getenv("GCP_PROJECT_ID")
        
        # Check for service account path or use default credentials
        sa_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        try:
            if sa_path and os.path.exists(sa_path):
                self.db = firestore.Client.from_service_account_json(sa_path)
            elif project_id:
                self.db = firestore.Client(project=project_id)
            else:
                # Fallback for local dev without Firestore
                print("Firestore not initialized. Using local memory.")
                self.local_db = {}
        except Exception as e:
            print(f"Error initializing Firestore: {e}")
            self.local_db = {}

    def get_user_state(self, user_id):
        if not self.db:
            return self.local_db.get(user_id, {"level": "beginner", "progress": "Start", "location": "India", "current_step": 0})
        
        doc_ref = self.db.collection("users").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return {"level": "beginner", "progress": "Start", "location": "India", "current_step": 0}

    def update_user_state(self, user_id, state_updates):
        if not self.db:
            current_state = self.local_db.get(user_id, {"level": "beginner", "progress": "Start", "location": "India", "current_step": 0})
            current_state.update(state_updates)
            self.local_db[user_id] = current_state
            return
        
        doc_ref = self.db.collection("users").document(user_id)
        doc_ref.set(state_updates, merge=True)
