import os
import google.cloud.logging
import logging

class AuditLogger:
    def __init__(self):
        project_id = os.getenv("GCP_PROJECT_ID")
        self.logger = logging.getLogger("election_guide_audit")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            sh = logging.StreamHandler()
            self.logger.addHandler(sh)

        try:
            if project_id:
                client = google.cloud.logging.Client(project=project_id)
                # Avoid setup_logging() which might be global/aggressive
                # client.setup_logging() 
        except Exception as e:
            print(f"Cloud Logging setup failed: {e}")

    def log_interaction(self, user_id, level, intent):
        try:
            self.logger.info(f"Interaction - User: {user_id}, Level: {level}, Intent: {intent}")
        except Exception:
            print(f"Local Log: User {user_id}, Level {level}, Intent {intent}")

    def log_error(self, error_msg):
        try:
            self.logger.error(f"Error: {error_msg}")
        except Exception:
            print(f"Local Error: {error_msg}")
