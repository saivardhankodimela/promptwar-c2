SYSTEM_PROMPT = """
You are "voter.ai," the premium AI guide for the Indian Democratic Lifecycle. Your mission is to provide non-partisan, authoritative, and simplified guidance based on the Election Commission of India (ECI) framework.

Mandate:
1. Explain the 8-step electoral lifecycle (Rolls, Announcement, Nominations, Campaigning, Polling, Security, Counting, Formation).
2. Maintain absolute neutrality. Do not favor any party or candidate.
3. Adapt your complexity to the user's level (Beginner/Intermediate/Advanced).
4. Use a professional, warm, and helpful "guide" persona. Avoid robotic preambles.
"""

USER_CLASSIFIER_PROMPT = """
Analyze the user's query and classify their knowledge level and intent.
Return ONLY a JSON object with the following structure:
{{
    "level": "beginner" | "intermediate" | "advanced",
    "intent": "learn" | "task" | "myth_check" | "quiz_request",
    "topic": "string",
    "confidence": 0.0-1.0
}}

User Query: {query}
"""

ADAPTIVE_EXPLAINER_PROMPT = """
Context:
- User Level: {level}
- User Location: {location}
- User Progress: {progress}
- Current Step: {current_step}

Task: Explain the following topic/question based on the user's level.
Topic: {query}

Guidelines:
- If Beginner: Use analogies. Avoid jargon. Focus on 'Why' and 'What'.
- If Intermediate: Use steps. Use 'How-to' guides.
- If Advanced: Provide details on legal frameworks or specific election phases.

Include a "Next Step" suggestion in your response.
"""

QUIZ_GENERATOR_PROMPT = """
Based on the previous explanation about {topic}, generate 2 short multiple-choice questions to test the user's understanding.
Return ONLY a JSON list of objects:
[
    {{
        "question": "string",
        "options": ["A", "B", "C", "D"],
        "answer": "correct option string",
        "explanation": "why this is correct"
      }}
]
"""

MYTH_FACT_PROMPT = """
Analyze the user's statement for potential misinformation regarding Indian elections.
If it is a myth, provide the correct fact with a brief explanation.
If it is a fact, confirm it.

User Statement: {statement}

Return JSON:
{{
    "is_myth": boolean,
    "correction": "string",
    "source_reference": "string"
}}
"""
