#!/usr/bin/env python3
"""
Verify Widget Installation Status
This script checks if the widget is properly marked as installed in your database
"""

import sys
from pathlib import Path

# Add project root to the Python path
sys.path.append(str(Path(__file__).parent.resolve()))

from app.database import SessionLocal
from app import models

def verify_widget_status():
    """Verify widget installation status in database"""
    print("🔍 Verifying Widget Installation Status...")
    
    try:
        db = SessionLocal()
        
        # Get all users with profiles
        users = db.query(models.User).join(models.UserProfile).all()
        
        if not users:
            print("❌ No users found in database")
            return
        
        print(f"📊 Found {len(users)} users")
        print("\n" + "="*60)
        
        for user in users:
            profile = db.query(models.UserProfile).filter(
                models.UserProfile.user_id == user.id
            ).first()
            
            integration = db.query(models.KommoIntegration).filter(
                models.KommoIntegration.user_id == user.id
            ).first()
            
            print(f"👤 User: {user.username} (ID: {user.id})")
            print(f"   📧 Email: {user.email}")
            
            if profile:
                print(f"   🎯 Widget Installed: {'✅ Yes' if profile.kommo_widget_installed else '❌ No'}")
            else:
                print(f"   🎯 Widget Installed: ❌ No Profile")
            
            if integration:
                print(f"   🔗 Kommo Integration: ✅ Active")
                print(f"   🌐 Domain: {integration.kommo_domain}")
                print(f"   🔑 Has Access Token: {'✅ Yes' if integration.access_token else '❌ No'}")
            else:
                print(f"   🔗 Kommo Integration: ❌ Not Configured")
            
            print("-" * 40)
        
        print("\n🎯 Next Steps:")
        print("1. If widget shows '✅ Yes' - Widget is marked as installed in your system")
        print("2. To see it in Kommo CRM - You need to manually install the widget files")
        print("3. Or enhance the code to call Kommo's widget API")
        
    except Exception as e:
        print(f"❌ Error verifying status: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_widget_status()
