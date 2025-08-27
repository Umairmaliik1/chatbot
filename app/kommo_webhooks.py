# app/kommo_webhooks.py
"""
Kommo CRM Webhook Handler
Processes incoming webhooks from Kommo CRM and syncs data to local database.
This is completely separated from the main application and can be easily removed.
"""

import json
import logging
import hashlib
import hmac
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from . import models
from .kommo_client import KommoClient

logger = logging.getLogger(__name__)

class KommoWebhookHandler:
    """Handles webhook events from Kommo CRM"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verify_webhook_signature(self, payload: str, signature: str, webhook_secret: str) -> bool:
        """Verify webhook signature for security (using HMAC-SHA1 as per Kommo documentation)"""
        try:
            # Kommo uses HMAC-SHA1 according to their documentation
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha1
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {e}")
            return False
    
    def process_webhook(self, user_id: int, webhook_data: Dict[str, Any], webhook_secret: str = None) -> bool:
        """Process incoming webhook from Kommo CRM (handles both CRM and Chat API webhooks)"""
        try:
            # Determine webhook type based on structure (as per Kommo documentation)
            webhook_id = webhook_data.get('id', webhook_data.get('account_id', 'unknown'))
            
            # Check if this is a Chat API webhook (has 'message' or 'action' field)
            if 'message' in webhook_data:
                event_type = 'chat_message'
                entity_type = 'message'
                entity_id = webhook_data['message'].get('id', 0)
            elif 'action' in webhook_data:
                action = webhook_data['action']
                if 'typing' in action:
                    event_type = 'typing'
                    entity_type = 'typing'
                    entity_id = action['typing']['conversation']['id']
                elif 'reaction' in action:
                    event_type = 'reaction'
                    entity_type = 'reaction'
                    entity_id = action['reaction']['message']['id']
                else:
                    event_type = 'unknown_action'
                    entity_type = 'action'
                    entity_id = 0
            else:
                # Traditional CRM webhook
                event_type = webhook_data.get('type', 'unknown')
                entity_type = webhook_data.get('entity_type', 'unknown')
                entity_id = webhook_data.get('entity_id', 0)
            
            logger.info(f"Processing webhook: {webhook_id}, type: {event_type}, entity: {entity_type}:{entity_id}")
            
            # Store webhook log
            webhook_log = models.KommoWebhookLog(
                user_id=user_id,
                webhook_id=str(webhook_id),
                event_type=event_type,
                entity_type=entity_type,
                entity_id=entity_id,
                payload=webhook_data
            )
            self.db.add(webhook_log)
            
            # Process based on event type
            success = False
            if event_type == 'chat_message':
                success = self._process_chat_message(user_id, webhook_data)
            elif event_type == 'typing':
                success = self._process_typing_event(user_id, webhook_data)
            elif event_type == 'reaction':
                success = self._process_reaction_event(user_id, webhook_data)
            elif event_type == 'add_lead':
                success = self._process_add_lead(user_id, webhook_data)
            elif event_type == 'update_lead':
                success = self._process_update_lead(user_id, webhook_data)
            elif event_type == 'add_contact':
                success = self._process_add_contact(user_id, webhook_data)
            elif event_type == 'update_contact':
                success = self._process_update_contact(user_id, webhook_data)
            elif event_type == 'add_deal':
                success = self._process_add_deal(user_id, webhook_data)
            elif event_type == 'update_deal':
                success = self._process_update_deal(user_id, webhook_data)
            else:
                logger.warning(f"Unknown webhook event type: {event_type}")
                success = True  # Don't fail on unknown events
            
            # Update webhook log
            webhook_log.processed = True
            webhook_log.processed_at = datetime.now()
            if not success:
                webhook_log.error_message = "Failed to process webhook"
            
            self.db.commit()
            return success
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            if 'webhook_log' in locals():
                webhook_log.processed = True
                webhook_log.processed_at = datetime.now()
                webhook_log.error_message = str(e)
                self.db.commit()
            return False
    
    def _process_chat_message(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process chat message webhook from Kommo Chat API"""
        try:
            message = webhook_data.get('message', {})
            if not message:
                logger.warning("No message data in chat webhook")
                return True  # Don't fail on missing message
            
            logger.info(f"Received chat message from {message.get('sender', {}).get('name', 'Unknown')} "
                       f"to {message.get('receiver', {}).get('name', 'Unknown')}")
            
            # Here you can implement logic to:
            # 1. Store the message in your chat system
            # 2. Trigger AI response generation
            # 3. Link message to existing CRM entities
            
            # For now, just log the message
            logger.info(f"Message text: {message.get('message', {}).get('text', 'No text')}")
            
            return True
                
        except Exception as e:
            logger.error(f"Error processing chat message webhook: {e}")
            return False
    
    def _process_typing_event(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process typing event webhook from Kommo Chat API"""
        try:
            action = webhook_data.get('action', {})
            typing = action.get('typing', {})
            
            logger.info(f"User {typing.get('user', {}).get('id', 'unknown')} is typing in conversation "
                       f"{typing.get('conversation', {}).get('id', 'unknown')}")
            
            # Here you can implement logic to show typing indicators in your chat UI
            
            return True
                
        except Exception as e:
            logger.error(f"Error processing typing event webhook: {e}")
            return False
    
    def _process_reaction_event(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process reaction event webhook from Kommo Chat API"""
        try:
            action = webhook_data.get('action', {})
            reaction = action.get('reaction', {})
            
            logger.info(f"Reaction {reaction.get('type', 'unknown')} "
                       f"with emoji {reaction.get('emoji', 'none')} "
                       f"on message {reaction.get('message', {}).get('id', 'unknown')}")
            
            # Here you can implement logic to handle reactions in your chat system
            
            return True
                
        except Exception as e:
            logger.error(f"Error processing reaction event webhook: {e}")
            return False
    
    def _process_add_lead(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process new lead webhook"""
        try:
            lead_data = webhook_data.get('lead', {})
            if not lead_data:
                logger.warning("No lead data in webhook")
                return False
            
            # Use KommoClient to sync lead
            kommo_client = KommoClient(user_id, self.db)
            lead = kommo_client.sync_lead(lead_data)
            
            if lead:
                logger.info(f"Successfully synced new lead: {lead.name} (ID: {lead.kommo_id})")
                return True
            else:
                logger.error("Failed to sync lead")
                return False
                
        except Exception as e:
            logger.error(f"Error processing add lead webhook: {e}")
            return False
    
    def _process_update_lead(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process lead update webhook"""
        try:
            lead_data = webhook_data.get('lead', {})
            if not lead_data:
                logger.warning("No lead data in webhook")
                return False
            
            # Use KommoClient to sync lead (will update if exists)
            kommo_client = KommoClient(user_id, self.db)
            lead = kommo_client.sync_lead(lead_data)
            
            if lead:
                logger.info(f"Successfully updated lead: {lead.name} (ID: {lead.kommo_id})")
                return True
            else:
                logger.error("Failed to update lead")
                return False
                
        except Exception as e:
            logger.error(f"Error processing update lead webhook: {e}")
            return False
    
    def _process_add_contact(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process new contact webhook"""
        try:
            contact_data = webhook_data.get('contact', {})
            if not contact_data:
                logger.warning("No contact data in webhook")
                return False
            
            # Check if contact already exists
            existing_contact = self.db.query(models.KommoContact).filter(
                models.KommoContact.user_id == user_id,
                models.KommoContact.kommo_id == contact_data['id']
            ).first()
            
            if existing_contact:
                # Update existing contact
                existing_contact.name = contact_data.get('name', '')
                existing_contact.first_name = contact_data.get('first_name', '')
                existing_contact.last_name = contact_data.get('last_name', '')
                existing_contact.email = contact_data.get('email', '')
                existing_contact.phone = contact_data.get('phone', '')
                existing_contact.position = contact_data.get('position', '')
                existing_contact.company_name = contact_data.get('company_name', '')
                existing_contact.company_id = contact_data.get('company_id')
                existing_contact.tags = contact_data.get('tags', [])
                existing_contact.custom_fields = contact_data.get('custom_fields', {})
                existing_contact.kommo_updated_at = datetime.now()
                
                contact = existing_contact
            else:
                # Create new contact
                contact = models.KommoContact(
                    user_id=user_id,
                    kommo_id=contact_data['id'],
                    name=contact_data.get('name', ''),
                    first_name=contact_data.get('first_name', ''),
                    last_name=contact_data.get('last_name', ''),
                    email=contact_data.get('email', ''),
                    phone=contact_data.get('phone', ''),
                    position=contact_data.get('position', ''),
                    company_name=contact_data.get('company_name', ''),
                    company_id=contact_data.get('company_id'),
                    tags=contact_data.get('tags', []),
                    custom_fields=contact_data.get('custom_fields', {}),
                    kommo_created_at=datetime.now(),
                    kommo_updated_at=datetime.now()
                )
                self.db.add(contact)
            
            self.db.commit()
            self.db.refresh(contact)
            
            logger.info(f"Successfully synced contact: {contact.name} (ID: {contact.kommo_id})")
            return True
                
        except Exception as e:
            logger.error(f"Error processing add contact webhook: {e}")
            self.db.rollback()
            return False
    
    def _process_update_contact(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process contact update webhook"""
        try:
            contact_data = webhook_data.get('contact', {})
            if not contact_data:
                logger.warning("No contact data in webhook")
                return False
            
            # Use the same logic as add_contact (will update if exists)
            return self._process_add_contact(user_id, webhook_data)
                
        except Exception as e:
            logger.error(f"Error processing update contact webhook: {e}")
            return False
    
    def _process_add_deal(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process new deal webhook"""
        try:
            deal_data = webhook_data.get('deal', {})
            if not deal_data:
                logger.warning("No deal data in webhook")
                return False
            
            # Check if deal already exists
            existing_deal = self.db.query(models.KommoDeal).filter(
                models.KommoDeal.user_id == user_id,
                models.KommoDeal.kommo_id == deal_data['id']
            ).first()
            
            if existing_deal:
                # Update existing deal
                existing_deal.name = deal_data.get('name', '')
                existing_deal.price = deal_data.get('price', 0)
                existing_deal.status_id = deal_data.get('status_id')
                existing_deal.status_name = deal_data.get('status_name', '')
                existing_deal.pipeline_id = deal_data.get('pipeline_id')
                existing_deal.pipeline_name = deal_data.get('pipeline_name', '')
                existing_deal.contact_id = deal_data.get('contact_id')
                existing_deal.lead_id = deal_data.get('lead_id')
                existing_deal.tags = deal_data.get('tags', [])
                existing_deal.custom_fields = deal_data.get('custom_fields', {})
                existing_deal.kommo_updated_at = datetime.now()
                
                deal = existing_deal
            else:
                # Create new deal
                deal = models.KommoDeal(
                    user_id=user_id,
                    kommo_id=deal_data['id'],
                    name=deal_data.get('name', ''),
                    price=deal_data.get('price', 0),
                    status_id=deal_data.get('status_id'),
                    status_name=deal_data.get('status_name', ''),
                    pipeline_id=deal_data.get('pipeline_id'),
                    pipeline_name=deal_data.get('pipeline_name', ''),
                    contact_id=deal_data.get('contact_id'),
                    lead_id=deal_data.get('lead_id'),
                    tags=deal_data.get('tags', []),
                    custom_fields=deal_data.get('custom_fields', {}),
                    kommo_created_at=datetime.now(),
                    kommo_updated_at=datetime.now()
                )
                self.db.add(deal)
            
            self.db.commit()
            self.db.refresh(deal)
            
            logger.info(f"Successfully synced deal: {deal.name} (ID: {deal.kommo_id})")
            return True
                
        except Exception as e:
            logger.error(f"Error processing add deal webhook: {e}")
            self.db.rollback()
            return False
    
    def _process_update_deal(self, user_id: int, webhook_data: Dict[str, Any]) -> bool:
        """Process deal update webhook"""
        try:
            deal_data = webhook_data.get('deal', {})
            if not deal_data:
                logger.warning("No deal data in webhook")
                return False
            
            # Use the same logic as add_deal (will update if exists)
            return self._process_add_deal(user_id, webhook_data)
                
        except Exception as e:
            logger.error(f"Error processing update deal webhook: {e}")
            return False
    
    def get_webhook_stats(self, user_id: int) -> Dict[str, Any]:
        """Get webhook processing statistics for a user"""
        try:
            total_webhooks = self.db.query(models.KommoWebhookLog).filter(
                models.KommoWebhookLog.user_id == user_id
            ).count()
            
            processed_webhooks = self.db.query(models.KommoWebhookLog).filter(
                models.KommoWebhookLog.user_id == user_id,
                models.KommoWebhookLog.processed == True
            ).count()
            
            failed_webhooks = self.db.query(models.KommoWebhookLog).filter(
                models.KommoWebhookLog.user_id == user_id,
                models.KommoWebhookLog.processed == True,
                models.KommoWebhookLog.error_message.isnot(None)
            ).count()
            
            return {
                'total_webhooks': total_webhooks,
                'processed_webhooks': processed_webhooks,
                'failed_webhooks': failed_webhooks,
                'success_rate': (processed_webhooks - failed_webhooks) / total_webhooks * 100 if total_webhooks > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting webhook stats: {e}")
            return {
                'total_webhooks': 0,
                'processed_webhooks': 0,
                'failed_webhooks': 0,
                'success_rate': 0
            }
