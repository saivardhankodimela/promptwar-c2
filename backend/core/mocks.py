import logging

logger = logging.getLogger("voter.ai.mocks")

class MockOrchestrator:
    """
    Simulated AI Brain for local testing.
    Prevents test failures due to missing cloud credentials.
    """
    async def classify_user(self, query: str) -> dict:
        return {
            "level": "beginner",
            "intent": "learn",
            "topic": "voting",
            "confidence": 0.9
        }

    async def get_adaptive_response(self, query: str, user_state: dict) -> str:
        return f"MOCK RESPONSE: As a {user_state.get('level', 'beginner')}, here is what you need to know about {query}."

    async def check_myth(self, statement: str) -> dict:
        return {
            "is_myth": False,
            "correction": "MOCK FACT: This is a verified electoral fact.",
            "source_reference": "ECI Handbook"
        }

    async def generate_quiz(self, topic: str) -> list:
        return [{
            "question": "Mock Question?",
            "options": ["A", "B", "C", "D"],
            "answer": "A",
            "explanation": "Because it's a mock."
        }]

class MockFirestore:
    """Simulated database for testing."""
    async def get_user_state(self, user_id: str) -> dict:
        return {"level": "beginner", "location": "India"}
    async def update_user_state(self, user_id: str, state_updates: dict) -> None:
        pass

class MockGCS:
    """Simulated archival for testing."""
    def archive_chat(self, user_id: str, chat_data: dict) -> None:
        pass
