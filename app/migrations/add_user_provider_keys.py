#!/usr/bin/env python3
"""
Migration: add encrypted provider API key columns to user_profiles.

Columns:
- openai_api_key_enc VARCHAR NULL
- gemini_api_key_enc VARCHAR NULL

Run with: python -m app.migrations.add_user_provider_keys
"""

import sys
import os
from sqlalchemy import text


# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from app.database import engine


def run_migration():
    stmts = [
        "ALTER TABLE user_profiles ADD COLUMN openai_api_key_enc VARCHAR",
        "ALTER TABLE user_profiles ADD COLUMN gemini_api_key_enc VARCHAR",
    ]

    with engine.connect() as conn:
        for stmt in stmts:
            try:
                print(f"Executing: {stmt}")
                conn.execute(text(stmt))
                conn.commit()
                print("✓ Success")
            except Exception as e:
                msg = str(e).lower()
                if "already exists" in msg or "duplicate column" in msg:
                    print(f"• Column already exists, skipping: {e}")
                else:
                    print(f"✗ Error: {e}")
                    raise
    print("\nMigration completed.")


if __name__ == "__main__":
    run_migration()

