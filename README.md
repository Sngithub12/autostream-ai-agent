# autostream-ai-agent
AI conversational agent with RAG + lead capture
# AutoStream AI Agent 🚀

This project is a conversational AI agent for AutoStream, a SaaS platform for automated video editing.

## 🔹 Features
- Intent Detection (LLM + fallback)
- RAG-based Knowledge Retrieval (local JSON)
- Multi-turn Conversation Memory
- Lead Capture Tool Execution
- Gemini / Claude Integration

## 🔹 Tech Stack
- Python
- Gemini / Claude (LLM)
- FastAPI (optional for webhook)
- JSON-based RAG

## 🔹 How to Run

```bash
git clone <repo-link>
cd autostream-agent
pip install -r requirements.txt
python main.py
Architecture

The system uses a modular architecture with separate components for intent detection, knowledge retrieval (RAG), state management, and tool execution.

Intent detection is handled using an LLM with rule-based fallback to improve reliability. The RAG system retrieves information from a local JSON knowledge base. Conversation state is maintained using a custom class to support multi-turn interactions. When high intent is detected, the agent collects user details and triggers a lead capture function.

🔹 WhatsApp Integration

The agent can be integrated with WhatsApp using the WhatsApp Business API and webhooks. Incoming messages are received via a webhook endpoint, processed by the AI agent, and responses are sent back using the WhatsApp API. Conversation state can be stored in a database for multi-user support.
# 🚀 STEP 6: Demo Video
https://drive.google.com/file/d/1MNK6LqlJPpbfeAbd0lWQOe9ytD3HNzzr/view?usp=sharing


---

# 🚀 STEP 7: Final Push (after README)

```bash id="gitpush2"
git add .
git commit -m "Added README and documentation"
git push
