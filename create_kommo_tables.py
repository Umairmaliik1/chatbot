#!/usr/bin/env python3
"""
Database Migration Script for Kommo CRM Integration
Creates all necessary tables for Kommo CRM integration.
This script can be run safely multiple times.
"""

import sys
from pathlib import Path

# Add project root to the Python path
sys.path.append(str(Path(__file__).parent.resolve()))

from app.database import SessionLocal, engine
from app import models

def create_kommo_tables():
    """Create all Kommo CRM integration tables"""
    print("🚀 Creating Kommo CRM integration tables...")
    
    try:
        # Create all tables (this will only create new ones)
        models.Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # Verify tables exist
        db = SessionLocal()
        try:
            # Check if Kommo tables exist
            from sqlalchemy import inspect
            inspector = inspect(engine)
            
            kommo_tables = [
                'kommo_integrations',
                'kommo_leads', 
                'kommo_contacts',
                'kommo_deals',
                'kommo_chat_sessions',
                'kommo_webhook_logs'
            ]
            
            existing_tables = inspector.get_table_names()
            
            print("\n📊 Table Status:")
            for table in kommo_tables:
                if table in existing_tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ❌ {table} - NOT CREATED")
            
            print(f"\n🎯 Total Kommo tables: {len([t for t in kommo_tables if t in existing_tables])}/{len(kommo_tables)}")
            
        finally:
            db.close()
            
        print("\n🎉 Kommo CRM integration tables are ready!")
        print("\n📋 Next steps:")
        print("  1. Start your application: uvicorn app.main:app --reload")
        print("  2. Go to /dashboard/kommo to configure integration")
        print("  3. Set up webhooks in Kommo CRM pointing to: /api/kommo/webhook/{your_integration_key}")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_kommo_tables()
