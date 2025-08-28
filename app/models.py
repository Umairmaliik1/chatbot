# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    kommo_integration_key = Column(String, unique=True, index=True, nullable=True)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    instructions = relationship("UserInstruction", back_populates="user", uselist=False, cascade="all, delete-orphan")
    faqs = relationship("FAQ", back_populates="user", cascade="all, delete-orphan")

class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    xelence_x_api_key = Column(String, nullable=True)
    xelence_affiliateid = Column(String, nullable=True)
    chat_rate = Column(Float, nullable=True)
    
    # Kommo chat integration fields
    kommo_widget_installed = Column(Boolean, default=False)

    user = relationship("User", back_populates="profile")

class UserInstruction(Base):
    __tablename__ = 'user_instructions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    instructions = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="instructions")

class FAQ(Base):
    __tablename__ = 'faqs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    priority = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="faqs")

# ============================================================================
# KOMO CRM INTEGRATION MODELS - COMPLETELY SEPARATED
# ============================================================================

class KommoIntegration(Base):
    """Kommo CRM integration settings for each user"""
    __tablename__ = 'kommo_integrations'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    
    # OAuth credentials
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    token_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Kommo account info
    kommo_account_id = Column(String, nullable=True)
    kommo_domain = Column(String, nullable=True)  # e.g., "yourcompany.kommo.com"
    
    # Webhook settings
    webhook_secret = Column(String, nullable=True)
    webhook_url = Column(String, nullable=True)
    
    # Integration status
    is_active = Column(Boolean, default=False)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class KommoLead(Base):
    """Leads from Kommo CRM"""
    __tablename__ = 'kommo_leads'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Kommo CRM data
    kommo_id = Column(Integer, nullable=False, index=True)  # Lead ID in Kommo
    name = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    status_id = Column(Integer, nullable=True)
    status_name = Column(String, nullable=True)
    pipeline_id = Column(Integer, nullable=True)
    pipeline_name = Column(String, nullable=True)
    
    # Contact information
    email = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True)
    
    # Additional data
    source = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)  # Store as JSON array
    custom_fields = Column(JSON, nullable=True)  # Store custom fields as JSON
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    kommo_created_at = Column(DateTime(timezone=True), nullable=True)
    kommo_updated_at = Column(DateTime(timezone=True), nullable=True)

class KommoContact(Base):
    """Contacts from Kommo CRM"""
    __tablename__ = 'kommo_contacts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Kommo CRM data
    kommo_id = Column(Integer, nullable=False, index=True)  # Contact ID in Kommo
    name = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    
    # Contact information
    email = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True)
    position = Column(String, nullable=True)
    
    # Company information
    company_name = Column(String, nullable=True)
    company_id = Column(Integer, nullable=True)
    
    # Additional data
    tags = Column(JSON, nullable=True)
    custom_fields = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    kommo_created_at = Column(DateTime(timezone=True), nullable=True)
    kommo_updated_at = Column(DateTime(timezone=True), nullable=True)

class KommoDeal(Base):
    """Deals from Kommo CRM"""
    __tablename__ = 'kommo_deals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Kommo CRM data
    kommo_id = Column(Integer, nullable=False, index=True)  # Deal ID in Kommo
    name = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    status_id = Column(Integer, nullable=True)
    status_name = Column(String, nullable=True)
    pipeline_id = Column(Integer, nullable=True)
    pipeline_name = Column(String, nullable=True)
    
    # Related entities
    contact_id = Column(Integer, nullable=True)
    lead_id = Column(Integer, nullable=True)
    
    # Additional data
    tags = Column(JSON, nullable=True)
    custom_fields = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    kommo_created_at = Column(DateTime(timezone=True), nullable=True)
    kommo_updated_at = Column(DateTime(timezone=True), nullable=True)

class KommoChatSession(Base):
    """Chat sessions linked to Kommo CRM entities"""
    __tablename__ = 'kommo_chat_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Link to existing chat session
    chat_session_id = Column(Integer, ForeignKey('chat_sessions.id'), nullable=False)
    
    # Kommo CRM entity links
    lead_id = Column(Integer, ForeignKey('kommo_leads.id'), nullable=True)
    contact_id = Column(Integer, ForeignKey('kommo_contacts.id'), nullable=True)
    deal_id = Column(Integer, ForeignKey('kommo_deals.id'), nullable=True)
    
    # Session metadata
    session_type = Column(String, nullable=False)  # 'lead', 'contact', 'deal', 'general'
    kommo_entity_type = Column(String, nullable=True)  # Type of entity this session is for
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class KommoWebhookLog(Base):
    """Log of webhook events from Kommo CRM"""
    __tablename__ = 'kommo_webhook_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Webhook data
    webhook_id = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False)  # 'add_lead', 'update_lead', 'add_contact', etc.
    entity_type = Column(String, nullable=False)  # 'lead', 'contact', 'deal'
    entity_id = Column(Integer, nullable=False)
    
    # Webhook payload
    payload = Column(JSON, nullable=False)
    
    # Processing status
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    received_at = Column(DateTime(timezone=True), server_default=func.now())