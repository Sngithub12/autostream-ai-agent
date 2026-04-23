from llm import generate_text

def detect_intent(user_input: str) -> str:
    prompt = f"""
Classify the user's intent into one of these:
[greeting, pricing, high_intent, general]

User: {user_input}

Return only one word.
"""

    intent = generate_text(prompt).strip().lower()

    if intent not in ["greeting", "pricing", "high_intent", "general"]:
        return "general"

    return intent