from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import datetime
import logging
import re

# Internal imports
from backend.agents.orchestrator import ElectionAgentOrchestrator
from backend.services.firestore import FirestoreService
from backend.services.gcs import GCSService
from backend.services.audit_logging import AuditLogger

router = APIRouter()
logger = logging.getLogger("voter.ai.api")

from backend.core.config import settings
from backend.core.mocks import MockOrchestrator, MockFirestore, MockGCS

# Global Singletons
_orchestrator = ElectionAgentOrchestrator()
_db_service = FirestoreService()
_gcs_service = GCSService()
_audit_logger = AuditLogger()

# Dependency Functions with Mock Support
def get_orchestrator(): 
    if os.getenv("TESTING") == "True":
        return MockOrchestrator()
    return _orchestrator

def get_db(): 
    if os.getenv("TESTING") == "True":
        return MockFirestore()
    return _db_service

def get_gcs(): 
    if os.getenv("TESTING") == "True":
        return MockGCS()
    return _gcs_service

def get_audit(): return _audit_logger

@router.get("/health")
async def v1_health():
    return {"status": "v1_healthy", "version": "2.0.0"}

class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=128)
    query: str = Field(..., min_length=1, max_length=1000)

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_\-]+$", v):
            raise ValueError("user_id contains invalid characters")
        return v

class ChatResponse(BaseModel):
    response: str
    level: str
    intent: str
    quiz: Optional[List] = None
    myth_check: Optional[dict] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    orchestrator: ElectionAgentOrchestrator = Depends(get_orchestrator),
    db_service: FirestoreService = Depends(get_db),
    gcs_service: GCSService = Depends(get_gcs),
    audit_logger: AuditLogger = Depends(get_audit)
):
    """
    Modularized Chat Controller. 
    Handles intent classification, state retrieval, and archival.
    """
    try:
        # 1. AI Orchestration
        classification = await orchestrator.classify_user(request.query)
        
        # 2. State Management
        user_state = await db_service.get_user_state(request.user_id)
        if classification.get("confidence", 0) > 0.7:
            user_state["level"] = classification.get("level", "beginner")
            await db_service.update_user_state(request.user_id, {"level": user_state["level"]})

        # 3. Intent Routing
        intent = classification.get("intent", "learn")
        quiz_data, myth_data = None, None
        
        if intent == "myth_check":
            myth_data = await orchestrator.check_myth(request.query)
            response_text = myth_data.get("correction", "Verification unavailable.")
        elif intent == "quiz_request":
            quiz_data = await orchestrator.generate_quiz(classification.get("topic", "voting"))
            response_text = "Let's test your knowledge with a quick quiz!"
        else:
            response_text = await orchestrator.get_adaptive_response(request.query, user_state)

        # 4. Asynchronous Archival & Logging
        audit_logger.log_interaction(request.user_id, user_state.get("level", "unknown"), intent)
        
        chat_entry = {
            "user_id": request.user_id,
            "query": request.query,
            "response": response_text,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        gcs_service.archive_chat(request.user_id, chat_entry)

        return ChatResponse(
            response=response_text,
            level=user_state.get("level", "beginner"),
            intent=intent,
            quiz=quiz_data,
            myth_check=myth_data
        )
    except Exception as e:
        logger.error(f"Router Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal processing error")
