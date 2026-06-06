"""
FastAPI application for AutoStream AI Agent
Handles real-time webhook integrations and HTTP endpoints
"""
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import logging
from agent import handle_user_input
from database import create_lead, save_conversation, get_user_conversation_history, get_analytics_stats
from memory import ConversationState

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AutoStream AI Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class MessageRequest(BaseModel):
    user_id: str
    message: str
    channel: str = "whatsapp"  # whatsapp, web, api

class LeadRequest(BaseModel):
    name: str
    email: str
    platform: str
    phone: str = None

class HealthResponse(BaseModel):
    status: str
    version: str

# Store conversation states per user
conversation_states = {}

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("🚀 AutoStream AI Agent Server Started")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Port: {os.getenv('PORT', 8000)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="1.0.0")

@app.post("/chat")
async def chat_endpoint(request: MessageRequest):
    """
    Main chat endpoint for handling user messages
    Supports WhatsApp, Web, and API channels
    Real-time message processing with conversation tracking
    """
    try:
        user_id = request.user_id
        user_message = request.message
        channel = request.channel
        
        logger.info(f"[{channel}] User {user_id}: {user_message}")
        
        # Get or create conversation state for user
        if user_id not in conversation_states:
            conversation_states[user_id] = ConversationState()
        
        state = conversation_states[user_id]
        
        # Handle user input
        response = handle_user_input(user_message)
        
        # Save conversation to database
        try:
            save_conversation(
                user_id=user_id,
                channel=channel,
                message=user_message,
                response=response,
                intent=None
            )
        except Exception as db_error:
            logger.warning(f"Database save error: {db_error}")
        
        logger.info(f"[{channel}] Response: {response}")
        
        return JSONResponse({
            "status": "success",
            "user_id": user_id,
            "response": response,
            "channel": channel,
            "timestamp": str(__import__('datetime').datetime.now())
        })
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    WhatsApp webhook endpoint for Twilio integration
    Processes incoming WhatsApp messages in real-time
    Automatically responds and captures leads
    """
    try:
        data = await request.form()
        from_number = data.get("From", "")
        message_body = data.get("Body", "")
        
        logger.info(f"WhatsApp from {from_number}: {message_body}")
        
        # Process message through chat endpoint
        chat_response = await chat_endpoint(MessageRequest(
            user_id=from_number,
            message=message_body,
            channel="whatsapp"
        ))
        
        # Send WhatsApp response using Twilio
        try:
            from twilio.rest import Client
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            
            if account_sid and auth_token:
                client = Client(account_sid, auth_token)
                
                import json
                response_data = json.loads(chat_response.body)
                
                message = client.messages.create(
                    from_=os.getenv("TWILIO_WHATSAPP_FROM"),
                    body=response_data["response"],
                    to=from_number
                )
                
                logger.info(f"WhatsApp message sent: {message.sid}")
                return JSONResponse({"status": "message_sent", "sid": message.sid})
        except Exception as twilio_error:
            logger.error(f"Twilio error: {twilio_error}")
        
        return JSONResponse({"status": "processed"})
    
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.post("/lead/capture")
async def capture_lead(lead: LeadRequest):
    """
    Lead capture endpoint
    Saves lead information to database and triggers notifications
    Real-time lead tracking for sales team
    """
    try:
        logger.info(f"Capturing lead: {lead.email}")
        
        # Check if lead already exists
        from database import get_lead_by_email
        existing_lead = get_lead_by_email(lead.email)
        
        if existing_lead:
            logger.warning(f"Lead already exists: {lead.email}")
            return JSONResponse({
                "status": "already_exists",
                "lead_id": existing_lead.id,
                "message": "Lead already in system"
            })
        
        # Save to database
        lead_id = create_lead(
            name=lead.name,
            email=lead.email,
            platform=lead.platform,
            phone=lead.phone
        )
        
        logger.info(f"Lead created with ID: {lead_id}")
        
        return JSONResponse({
            "status": "success",
            "lead_id": lead_id,
            "message": "Lead captured successfully"
        })
    
    except Exception as e:
        logger.error(f"Lead capture error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/user/{user_id}/history")
async def get_conversation_history(user_id: str, limit: int = 10):
    """
    Get conversation history for a user
    Useful for context in multi-turn conversations
    """
    try:
        history = get_user_conversation_history(user_id, limit)
        
        return JSONResponse({
            "status": "success",
            "user_id": user_id,
            "conversations": [
                {
                    "message": conv.message,
                    "response": conv.response,
                    "timestamp": str(conv.created_at),
                    "channel": conv.channel
                }
                for conv in history
            ]
        })
    
    except Exception as e:
        logger.error(f"History fetch error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/analytics/summary")
async def analytics_summary():
    """
    Get conversation analytics summary
    Real-time stats on conversations and leads
    """
    try:
        stats = get_analytics_stats()
        
        return JSONResponse({
            "status": "success",
            "analytics": stats,
            "timestamp": str(__import__('datetime').datetime.now())
        })
    
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "name": "AutoStream AI Agent",
        "version": "1.0.0",
        "description": "AI conversational agent with RAG + real-time lead capture",
        "endpoints": {
            "health": {
                "path": "/health",
                "method": "GET",
                "description": "Health check"
            },
            "chat": {
                "path": "/chat",
                "method": "POST",
                "description": "Send message to AI agent"
            },
            "whatsapp": {
                "path": "/webhook/whatsapp",
                "method": "POST",
                "description": "WhatsApp webhook endpoint (Twilio)"
            },
            "lead_capture": {
                "path": "/lead/capture",
                "method": "POST",
                "description": "Capture lead information"
            },
            "conversation_history": {
                "path": "/user/{user_id}/history",
                "method": "GET",
                "description": "Get user conversation history"
            },
            "analytics": {
                "path": "/analytics/summary",
                "method": "GET",
                "description": "Get analytics summary"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=(environment == "development")
    )
