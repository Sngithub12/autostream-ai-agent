"""
Database module for lead storage and conversation tracking
SQLAlchemy models and database operations
"""
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./autostream.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Lead(Base):
    """Lead model for storing captured leads"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    platform = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="new")  # new, contacted, converted

class Conversation(Base):
    """Conversation model for tracking user interactions"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    channel = Column(String, nullable=False)  # whatsapp, web, api
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    intent = Column(String, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Database operations
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_lead(name: str, email: str, platform: str, phone: str = None):
    """Create a new lead"""
    db = SessionLocal()
    try:
        lead = Lead(name=name, email=email, platform=platform, phone=phone)
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return lead.id
    finally:
        db.close()

def get_lead_by_email(email: str):
    """Get lead by email"""
    db = SessionLocal()
    try:
        return db.query(Lead).filter(Lead.email == email).first()
    finally:
        db.close()

def save_conversation(user_id: str, channel: str, message: str, response: str, intent: str = None):
    """Save conversation to database"""
    db = SessionLocal()
    try:
        conversation = Conversation(
            user_id=user_id,
            channel=channel,
            message=message,
            response=response,
            intent=intent
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation.id
    finally:
        db.close()

def get_user_conversation_history(user_id: str, limit: int = 10):
    """Get user conversation history"""
    db = SessionLocal()
    try:
        conversations = db.query(Conversation)\
            .filter(Conversation.user_id == user_id)\
            .order_by(Conversation.created_at.desc())\
            .limit(limit)\
            .all()
        return conversations
    finally:
        db.close()

def get_analytics_stats():
    """Get analytics statistics"""
    db = SessionLocal()
    try:
        total_leads = db.query(Lead).count()
        total_conversations = db.query(Conversation).count()
        new_leads = db.query(Lead).filter(Lead.status == "new").count()
        
        return {
            "total_leads": total_leads,
            "total_conversations": total_conversations,
            "new_leads": new_leads
        }
    finally:
        db.close()
