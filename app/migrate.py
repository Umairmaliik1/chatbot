import sys
from pathlib import Path
from sqlalchemy import inspect, text
import sqlite3
import os
from datetime import datetime

# Add project root to the Python path.
# The script is inside 'app', so we need to go up one level to the project root.
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from app.database import engine
from app import models

def run_migration():
    """
    A robust migration script that automatically detects and adds missing
    columns to all tables defined in models.py.
    This script is idempotent and safe to run multiple times.
    """
    print("--- Starting Database Migration ---")

    # First, ensure all tables exist. This is safe to run even if they do.
    print("Ensuring database tables exist...")
    models.Base.metadata.create_all(bind=engine)
    print("✅ Tables checked.")

    inspector = inspect(engine)

    with engine.connect() as connection:
        # Use a transaction to ensure all or no changes are made
        with connection.begin():
            print("🔬 Inspecting database schema for missing columns...")
            # Get all tables defined in our models
            for table_name, table in models.Base.metadata.tables.items():
                print(f"   - Checking table: '{table_name}'")
                
                # Get existing columns from the database for this table
                existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
                
                # Get expected columns from our SQLAlchemy model and find what's missing
                for column in table.columns:
                    if column.name not in existing_columns:
                        # Construct and execute the ALTER TABLE statement
                        col_type = column.type.compile(engine.dialect)
                        alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {column.name} {col_type}"
                        print(f"     ⚠️ Found missing column '{column.name}'. Adding it now...")
                        connection.execute(text(alter_sql))
                        print(f"     ✅ Column '{column.name}' added successfully.")

    print("✅ Migration check complete. Database schema is up to date.")

def migrate_database():
    """Run database migrations."""
    db_path = "app.db"
    
    if not os.path.exists(db_path):
        print("Database not found. Please run the application first to create it.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if updated_at column exists in chat_sessions
        cursor.execute("PRAGMA table_info(chat_sessions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'updated_at' not in columns:
            print("Adding updated_at column to chat_sessions table...")
            
            # Add updated_at column with default value
            cursor.execute("""
                ALTER TABLE chat_sessions 
                ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            """)
            
            # Update existing records to have updated_at = created_at
            cursor.execute("""
                UPDATE chat_sessions 
                SET updated_at = created_at 
                WHERE updated_at IS NULL
            """)
            
            print("✅ Successfully added updated_at column to chat_sessions table")
        else:
            print("✅ updated_at column already exists in chat_sessions table")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
    migrate_database()