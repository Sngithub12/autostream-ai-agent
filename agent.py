from intent import detect_intent
from rag import get_pricing_info, get_policy_info
from tools import mock_lead_capture
from memory import ConversationState
from llm import generate_text

state = ConversationState()

def generate_response(context, user_input):
    prompt = f"""
You are an AI assistant for AutoStream.

Context:
{context}

User: {user_input}

Give a helpful answer.
"""
    return generate_text(prompt)


def handle_user_input(user_input):

    intent = detect_intent(user_input)

    # Greeting
    if intent == "greeting":
        return "Hi! Welcome to AutoStream 🚀 How can I help you?"

    # Pricing → RAG + Gemini
    elif intent == "pricing":
        pricing = get_pricing_info()
        return generate_response(pricing, user_input)

    # Policies
    elif "refund" in user_input.lower() or "support" in user_input.lower():
        policies = get_policy_info()
        return generate_response(policies, user_input)

    # High Intent
    elif intent == "high_intent":
        state.stage = "lead"

        if not state.name:
            return "Awesome! Let's get you started 🚀 What's your name?"

    # Lead Flow
    if intent == "high_intent" and state.stage != "lead":
        state.stage = "lead"

        if not state.name:
            state.name = user_input
            return "Great! Please share your email."

        elif not state.email:
            state.email = user_input
            return "Which platform do you create content on? (YouTube, Instagram, etc.)"

        elif not state.platform:
            state.platform = user_input

        if state.is_complete():
            mock_lead_capture(state.name, state.email, state.platform)

        state.reset()       
        
    

        return "🎉 Done! Our team will contact you soon."
    return "Feel free to ask anything about AutoStream!"

