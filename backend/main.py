"""
voter.ai - ELECTION GUIDE
Main FastAPI application serving the unified frontend and backend.
Handles chat orchestration, user state management, and audit logging.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import datetime
import traceback
import os
import logging
import re

# --- Structured Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("voter.ai")

from backend.agents.orchestrator import ElectionAgentOrchestrator
from backend.services.firestore import FirestoreService
from backend.services.gcs import GCSService
from backend.services.audit_logging import AuditLogger

# --- Application Setup ---
app = FastAPI(
    title="voter.ai - ELECTION GUIDE",
    description="AI-powered election guide for Indian democracy",
    version="2.0.0",
)

# Security: Restrict CORS to known origins in production
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Efficiency: GZip compression for responses > 1KB
app.add_middleware(GZipMiddleware, minimum_size=1000)

# --- Service Initialization (Keyless ADC) ---
orchestrator = ElectionAgentOrchestrator()
db_service = FirestoreService()
gcs_service = GCSService()
audit_logger = AuditLogger()


# --- Request / Response Models ---
class ChatRequest(BaseModel):
    """Incoming chat request from the frontend."""
    user_id: str = Field(..., min_length=1, max_length=128)
    query: str = Field(..., min_length=1, max_length=1000)

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Sanitize user_id to prevent injection attacks."""
        if not re.match(r"^[a-zA-Z0-9_\-]+$", v):
            raise ValueError("user_id contains invalid characters")
        return v


class ChatResponse(BaseModel):
    """Structured response returned to the frontend."""
    response: str
    level: str
    intent: str
    quiz: Optional[List] = None
    myth_check: Optional[dict] = None


# --- API Endpoints ---
@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run probes."""
    return {
        "status": "healthy",
        "mode": "unified-keyless",
        "brand": "voter.ai",
        "version": "2.0.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint. Orchestrates the full pipeline:
    1. Classify user intent via Vertex AI
    2. Retrieve/update user state in Firestore
    3. Generate adaptive response via Gemini
    4. Log interaction for audit trail
    5. Archive conversation to GCS
    """
    try:
        # 1. Classify User (Vertex AI)
        classification = await orchestrator.classify_user(request.query)

        # 2. Get/Update User State (Firestore Keyless)
        user_state = {"level": "beginner", "location": "India"}
        try:
            user_state = db_service.get_user_state(request.user_id)
        except Exception as e:
            logger.warning("Firestore read failed for %s: %s", request.user_id, e)

        if classification.get("confidence", 0) > 0.7:
            user_state["level"] = classification.get("level", "beginner")
            try:
                db_service.update_user_state(
                    request.user_id, {"level": user_state["level"]}
                )
            except Exception as e:
                logger.error("Firestore write failed: %s", e)

        # 3. Handle Intents
        quiz_data = None
        myth_data = None
        intent = classification.get("intent", "learn")

        if intent == "myth_check":
            myth_data = await orchestrator.check_myth(request.query)
            response_text = myth_data.get("correction", "Verification unavailable.")
        elif intent == "quiz_request":
            quiz_data = await orchestrator.generate_quiz(
                classification.get("topic", "voting")
            )
            response_text = "Let's test your knowledge with a quick quiz!"
        else:
            response_text = await orchestrator.get_adaptive_response(
                request.query, user_state
            )

        # 4. Audit Log (Cloud Logging Keyless)
        try:
            audit_logger.log_interaction(
                request.user_id,
                user_state.get("level", "unknown"),
                intent
            )
        except Exception as e:
            logger.error("Audit logging failed: %s", e)

        # 5. Archive (GCS Keyless)
        try:
            chat_entry = {
                "user_id": request.user_id,
                "query": request.query,
                "response": response_text,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
            gcs_service.archive_chat(request.user_id, chat_entry)
        except Exception as e:
            logger.error("GCS archival failed: %s", e)

        return ChatResponse(
            response=response_text,
            level=user_state.get("level", "beginner"),
            intent=intent,
            quiz=quiz_data,
            myth_check=myth_data,
        )
    except ValueError as e:
        logger.warning("Validation error: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Chat endpoint error: %s", e, exc_info=True)
        return ChatResponse(
            response="I'm sorry, I'm experiencing a temporary disconnect. Please try again soon!",
            level="beginner",
            intent="error",
        )


# --- Unified Frontend Serving ---
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """Serve the React SPA for any non-API route."""
    if full_path.startswith("chat") or full_path == "health":
        return None
    index_path = os.path.join("dist", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "voter.ai backend is running. Frontend build not found."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        workers=2,
    )
