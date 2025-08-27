#!/usr/bin/env python3
"""
Database Migration Script for Kommo Chat Integration
Adds the kommo_widget_installed field to user_profiles table.
This script can be run safely multiple times.
"""

import sys
from pathlib import Path

# Add project root to the Python path
sys.path.append(str(Path(__file__).parent.resolve()))

from app.database import SessionLocal, engine
from app import models

def run_kommo_chat_migration():
    """Add Kommo chat integration fields to UserProfile table"""
    print("🚀 Running Kommo Chat Integration migration...")
    
    try:
        # Create all tables (this will only create new ones)
        models.Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # Verify the new field exists
        db = SessionLocal()
        try:
            # Check if the new field exists in user_profiles table
            from sqlalchemy import inspect, text
            inspector = inspect(engine)
            
            # Get column info for user_profiles table
            columns = inspector.get_columns('user_profiles')
            column_names = [col['name'] for col in columns]
            
            print("\n📊 User Profile Table Columns:")
            for col in columns:
                print(f"  ✅ {col['name']} ({col['type']})")
            
            # Check if kommo_widget_installed column exists
            if 'kommo_widget_installed' in column_names:
                print("\n🎉 Kommo chat integration field already exists!")
            else:
                print("\n⚠️  kommo_widget_installed field not found. Adding it...")
                
                # Add the new column
                with engine.connect() as connection:
                    connection.execute(text('ALTER TABLE user_profiles ADD COLUMN kommo_widget_installed BOOLEAN DEFAULT 0'))
                    connection.commit()
                    print("✅ Added kommo_widget_installed field successfully!")
            
            print(f"\n🎯 Total columns in user_profiles: {len(columns)}")
            
        finally:
            db.close()
            
        print("\n🎉 Kommo Chat Integration migration completed!")
        print("\n📋 Next steps:")
        print("  1. Start your application: uvicorn app.main:app --reload")
        print("  2. Go to /dashboard/kommo to configure chat integration")
        print("  3. Set up your Kommo Salesbot to use: /api/kommo/chat/webhook")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_kommo_chat_migration()
