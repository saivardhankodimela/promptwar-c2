import os
import json
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, HarmCategory, HarmBlockThreshold
from .prompts import (
    SYSTEM_PROMPT,
    USER_CLASSIFIER_PROMPT,
    ADAPTIVE_EXPLAINER_PROMPT,
    QUIZ_GENERATOR_PROMPT,
    MYTH_FACT_PROMPT
)
from dotenv import load_dotenv

load_dotenv()

class ElectionAgentOrchestrator:
    def __init__(self):
        # 100% PURE IDENTITY-BASED AUTHENTICATION (ADC)
        # No API keys or JSON files are used.
        # --- AGENT STUDIO SYNC ---
        # Using the exact model and location active in your dashboard
        project_id = "promptwars-c2"
        location = "us-central1"
        
        try:
            vertexai.init(project=project_id, location=location)
            # Upgrading to Gemini 2.5 Flash as seen in your settings!
            self.model = GenerativeModel("gemini-2.5-flash")
            print(f"ELECTION GUIDE: Brain Synced with Gemini 2.5 Flash (US-Central)")
        except Exception as e:
            print(f"Vertex AI Identity Init failed: {e}")
            self.model = None

    async def _generate(self, prompt, is_json=False):
        if not self.model:
            return "I'm having trouble connecting to my cloud brain. Ensure you've run 'gcloud auth application-default login'."
        
        try:
            # Identity-based generation
            response = self.model.generate_content(
                f"{SYSTEM_PROMPT}\n\n{prompt}",
                generation_config={"temperature": 0.2, "top_p": 0.8, "top_k": 40}
            )
            return response.text
        except Exception as e:
            print(f"Vertex Generation Error: {e}")
            return "My cloud connection is currently blocked. Please check your GCP permissions."

    async def classify_user(self, query):
        prompt = USER_CLASSIFIER_PROMPT.format(query=query)
        res_text = await self._generate(prompt, is_json=True)
        try:
            start = res_text.find('{')
            end = res_text.rfind('}') + 1
            return json.loads(res_text[start:end])
        except:
            return {"level": "beginner", "intent": "learn", "topic": "general", "confidence": 0.5}

    async def get_adaptive_response(self, query, user_state):
        classification = await self.classify_user(query)
        prompt = ADAPTIVE_EXPLAINER_PROMPT.format(
            level=classification.get("level", "beginner"),
            location="India",
            progress="N/A",
            current_step="N/A",
            query=query
        )
        return await self._generate(prompt)

    async def generate_quiz(self, topic):
        prompt = QUIZ_GENERATOR_PROMPT.format(topic=topic)
        res_text = await self._generate(prompt, is_json=True)
        try:
            start = res_text.find('[')
            end = res_text.rfind(']') + 1
            return json.loads(res_text[start:end])
        except:
            return []

    async def check_myth(self, statement):
        prompt = MYTH_FACT_PROMPT.format(statement=statement)
        res_text = await self._generate(prompt, is_json=True)
        try:
            start = res_text.find('{')
            end = res_text.rfind('}') + 1
            return json.loads(res_text[start:end])
        except:
            return {"is_myth": False, "correction": "Verification unavailable.", "source_reference": ""}
