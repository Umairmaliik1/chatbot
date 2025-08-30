#!/usr/bin/env python3
"""
Database migration to add AI settings and customization fields to user_profiles table.

This migration adds:
- response_delay_seconds: Response delay in seconds (0-40)
- ai_provider: AI provider choice ('gemini' or 'openai')
- custom_logo_url: User's custom logo URL
- custom_favicon_url: User's custom favicon URL  
- custom_website_name: User's custom website name

Run with: python -m app.migrations.add_user_ai_settings
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from sqlalchemy import text
from app.database import engine

def run_migration():
    """Add new fields to user_profiles table."""
    
    migrations = [
        # Add AI settings fields
        "ALTER TABLE user_profiles ADD COLUMN response_delay_seconds INTEGER DEFAULT 0",
        "ALTER TABLE user_profiles ADD COLUMN ai_provider VARCHAR DEFAULT 'gemini'",
        
        # Add user customization fields
        "ALTER TABLE user_profiles ADD COLUMN custom_logo_url VARCHAR",
        "ALTER TABLE user_profiles ADD COLUMN custom_favicon_url VARCHAR", 
        "ALTER TABLE user_profiles ADD COLUMN custom_website_name VARCHAR",
    ]
    
    with engine.connect() as connection:
        for migration in migrations:
            try:
                print(f"Executing: {migration}")
                connection.execute(text(migration))
                connection.commit()
                print("✅ Success")
            except Exception as e:
                if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                    print(f"⚠️  Column already exists, skipping: {e}")
                else:
                    print(f"❌ Error: {e}")
                    raise
    
    print("\n🎉 Migration completed successfully!")
    print("New fields added to user_profiles:")
    print("  - response_delay_seconds (INTEGER, default 0)")
    print("  - ai_provider (VARCHAR, default 'gemini')")
    print("  - custom_logo_url (VARCHAR)")
    print("  - custom_favicon_url (VARCHAR)")
    print("  - custom_website_name (VARCHAR)")

if __name__ == "__main__":
    run_migration()
