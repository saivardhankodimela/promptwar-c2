import os
from google.cloud import secretmanager

class SecretService:
    def __init__(self):
        self.client = None
        try:
            self.client = secretmanager.SecretManagerServiceClient()
        except Exception:
            pass

    def get_secret(self, secret_id):
        if not self.client:
            return os.getenv(secret_id)
        
        project_id = os.getenv("GCP_PROJECT_ID")
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception:
            return os.getenv(secret_id)
