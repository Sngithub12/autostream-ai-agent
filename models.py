"""
Additional database models for advanced features
"""
from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for tracking repeat visitors"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    name = Column(String, nullable=True)
    sentiment_score = Column(Float, default=0.0)
    total_conversations = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

class EmailTemplate(Base):
    """Email templates for outreach"""
    __tablename__ = "email_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    subject = Column(String)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class CRMIntegration(Base):
    """CRM integration settings"""
    __tablename__ = "crm_integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    crm_type = Column(String)  # salesforce, hubspot, pipedrive
    api_key = Column(String)
    enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Referral(Base):
    """Referral tracking"""
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(String)
    referred_email = Column(String)
    status = Column(String, default="pending")  # pending, completed
    created_at = Column(DateTime, default=datetime.utcnow)

class SlackIntegration(Base):
    """Slack bot configuration"""
    __tablename__ = "slack_integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(String, unique=True)
    bot_token = Column(String)
    enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
