import pytest
from agents.orchestrator import ElectionAgentOrchestrator

@pytest.mark.asyncio
async def test_classifier():
    orchestrator = ElectionAgentOrchestrator()
    # Test a simple query
    classification = await orchestrator.classify_user("What is voting?")
    assert "level" in classification
    assert "intent" in classification
    assert classification["level"] in ["beginner", "intermediate", "advanced"]

@pytest.mark.asyncio
async def test_myth_check():
    orchestrator = ElectionAgentOrchestrator()
    result = await orchestrator.check_myth("Is Aadhaar mandatory for voting?")
    assert "is_myth" in result
    assert "correction" in result
