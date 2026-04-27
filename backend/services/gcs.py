import os
import json
from google.cloud import storage

class GCSService:
    def __init__(self):
        self.client = None
        project_id = os.getenv("GCP_PROJECT_ID", "promptwars-c2")
        self.bucket_name = os.getenv("GCS_BUCKET_NAME", f"voter-ai-logs-{project_id}")
        
        if not project_id:
            return

        try:
            self.client = storage.Client(project=project_id)
        except Exception as e:
            print(f"GCS Client setup failed: {e}")

    def archive_chat(self, user_id, chat_data):
        if not self.client:
            return
        
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(f"chats/{user_id}/{chat_data['timestamp']}.json")
            blob.upload_from_string(json.dumps(chat_data))
        except Exception as e:
            print(f"Error uploading to GCS: {e}")
            # Silently fail for GCS in this demo to avoid 500s
