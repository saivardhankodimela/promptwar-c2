from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import datetime
import traceback
import os

from backend.agents.orchestrator import ElectionAgentOrchestrator
from backend.services.firestore import FirestoreService
from backend.services.gcs import GCSService
from backend.services.audit_logging import AuditLogger

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="VOTER.AI - UNIFIED EDITION")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services with Keyless Identity
# All services use ADC (Application Default Credentials)
orchestrator = ElectionAgentOrchestrator()
db_service = FirestoreService()
gcs_service = GCSService()
audit_logger = AuditLogger()

class ChatRequest(BaseModel):
    user_id: str
    query: str

class ChatResponse(BaseModel):
    response: str
    level: str
    intent: str
    quiz: Optional[List] = None
    myth_check: Optional[dict] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Classify User (Vertex AI)
        classification = await orchestrator.classify_user(request.query)
        
        # 2. Get/Update User State (Firestore Keyless)
        user_state = {"level": "beginner", "location": "India"} # Default
        try:
            user_state = db_service.get_user_state(request.user_id)
        except Exception: pass
        
        if classification.get("confidence", 0) > 0.7:
            user_state["level"] = classification.get("level", "beginner")
            try:
                db_service.update_user_state(request.user_id, {"level": user_state["level"]})
            except Exception: pass

        # 3. Handle Intents
        quiz_data = None
        myth_data = None
        intent = classification.get("intent", "learn")
        
        if intent == "myth_check":
            myth_data = await orchestrator.check_myth(request.query)
            response_text = myth_data.get("correction", "Verification unavailable.")
        elif intent == "quiz_request":
            quiz_data = await orchestrator.generate_quiz(classification.get("topic", "voting"))
            response_text = "Let's test your knowledge with a quick quiz!"
        else:
            response_text = await orchestrator.get_adaptive_response(request.query, user_state)

        # 4. Audit Log (Cloud Logging Keyless)
        try:
            audit_logger.log_interaction(request.user_id, user_state.get("level", "unknown"), intent)
        except Exception: pass

        # 5. Archive (GCS Keyless)
        try:
            chat_entry = {
                "user_id": request.user_id,
                "query": request.query,
                "response": response_text,
                "timestamp": datetime.datetime.now().isoformat()
            }
            gcs_service.archive_chat(request.user_id, chat_entry)
        except Exception: pass

        return ChatResponse(
            response=response_text,
            level=user_state.get("level", "beginner"),
            intent=intent,
            quiz=quiz_data,
            myth_check=myth_data
        )
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        traceback.print_exc()
        return ChatResponse(
            response="I'm sorry, I'm experiencing a temporary disconnect. Please try again soon!",
            level="beginner",
            intent="error"
        )

# --- UNIFIED FRONTEND SERVING ---
# Mount the static files (compiled React app)
# Note: In the container, these will be in /app/dist
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Serve index.html for any route not caught by the API (SPA support)
    if full_path.startswith("chat") or full_path == "health":
        return None # Let FastAPI handle API routes
    
    index_path = os.path.join("dist", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "VOTER.AI Backend is running. Frontend build not found."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "unified-keyless"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 9191))
    uvicorn.run(app, host="0.0.0.0", port=port)
