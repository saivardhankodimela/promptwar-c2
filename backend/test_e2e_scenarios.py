import requests
import json

BASE_URL = "http://localhost:9191"
USER_ID = "test_user_e2e"

scenarios = [
    {
        "name": "Beginner Persona",
        "query": "What is voting? Explain like I'm 5.",
        "expected_intent": "learn",
        "expected_level": "beginner"
    },
    {
        "name": "Intermediate Persona",
        "query": "How do I register for a voter ID card? Give me steps.",
        "expected_intent": "learn",
        "expected_level": "intermediate"
    },
    {
        "name": "Advanced Persona",
        "query": "Analyze the impact of the model code of conduct on the 2024 general elections phases.",
        "expected_intent": "learn",
        "expected_level": "advanced"
    },
    {
        "name": "Myth Check",
        "query": "Is it true that I can't vote without an Aadhaar card?",
        "expected_intent": "myth_check",
        "expected_level": None
    },
    {
        "name": "Quiz Request",
        "query": "Can you test my knowledge with a quiz about registration?",
        "expected_intent": "quiz_request",
        "expected_level": None
    }
]

def run_tests():
    print("Starting End-to-End Testing for Adaptive Election Guide Agent\n")
    
    for scenario in scenarios:
        print(f"--- Testing Scenario: {scenario['name']} ---")
        payload = {
            "user_id": USER_ID,
            "query": scenario['query']
        }
        
        try:
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            if response.status_code != 200:
                print(f"[ERROR] API returned {response.status_code}: {response.text}")
                continue
                
            data = response.json()
            
            print(f"Query: {scenario['query']}")
            print(f"Intent Detected: {data['intent']}")
            print(f"Level Adapted: {data['level']}")
            # print(f"Response Snippet: {data['response'][:100]}...")
            
            if scenario['expected_intent'] and data['intent'] == scenario['expected_intent']:
                print("[OK] Intent Match Success")
            
            if scenario['expected_level'] and data['level'] == scenario['expected_level']:
                print("[OK] Level Adaptation Success")
                
            if data['myth_check']:
                print(f"[CHECK] Myth Check Result: {data['myth_check']['is_myth']}")
                
            if data['quiz']:
                print(f"[QUIZ] Quiz Generated: {len(data['quiz'])} questions")
            
        except Exception as e:
            print(f"[ERROR] Test Failed: {e}")
        
        print("\n")

if __name__ == "__main__":
    run_tests()
