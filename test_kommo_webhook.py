#!/usr/bin/env python3
"""
Test Kommo Webhook and Logging
This script simulates Kommo webhook calls to test the logging system
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_kommo_webhook():
    """Test the Kommo webhook endpoint with logging"""
    print("🧪 Testing Kommo Webhook Endpoint...")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Basic webhook call
    print("\n1️⃣ Testing Basic Webhook Call...")
    try:
        # Simulate Kommo webhook data
        webhook_data = {
            "message[add][0][text]": "Hello, I need help with my order",
            "message[add][0][chat_id]": "12345",
            "message[add][0][contact_id]": "67890",
            "message[add][0][author][name]": "John Doe",
            "return_url": "https://example.com/kommo/callback",
            "account_id": "test_account_123"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/kommo/chat/webhook",
                data=webhook_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result}")
            else:
                print(f"   ❌ Error: {response.text}")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Webhook with invalid data
    print("\n2️⃣ Testing Webhook with Invalid Data...")
    try:
        invalid_data = {
            "invalid_field": "test",
            "message": "This should fail"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/kommo/chat/webhook",
                data=invalid_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result}")
            else:
                print(f"   ❌ Error: {response.text}")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Test chat endpoint
    print("\n3️⃣ Testing Chat Test Endpoint...")
    try:
        test_message = {
            "message": "What are your business hours?"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/kommo/chat/test",
                json=test_message,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result.get('success')}")
                print(f"   ✅ AI Response: {result.get('response', '')[:100]}...")
            else:
                print(f"   ❌ Error: {response.text}")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎯 Webhook Testing Summary:")
    print("✅ Check the console output above for immediate results")
    print("✅ Check the logs/ directory for detailed Kommo CRM logs")
    print("✅ Look for files like:")
    print("   - kommo_crm_YYYYMMDD.log (all activities)")
    print("   - kommo_crm_errors_YYYYMMDD.log (errors only)")
    print("   - kommo_webhooks_YYYYMMDD.log (webhook activities)")
    print("\n📝 To see real-time logs, run:")
    print("   tail -f logs/kommo_crm_*.log")

if __name__ == "__main__":
    asyncio.run(test_kommo_webhook())
