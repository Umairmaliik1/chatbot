#!/usr/bin/env python3
"""
Test Script for Kommo Chat Integration
This script tests the chat webhook endpoint without authentication
"""

import asyncio
import httpx
import json
from urllib.parse import urlencode

async def test_chat_webhook():
    """Test the chat webhook endpoint"""
    print("🧪 Testing Kommo Chat Webhook...")
    
    # Test data similar to what Kommo would send
    test_data = {
        "message[add][0][text]": "Hello, can you help me with my order?",
        "message[add][0][chat_id]": "12345",
        "message[add][0][contact_id]": "67890",
        "message[add][0][author][name]": "John Doe",
        "return_url": "https://test.kommo.com/api/v4/salesbot/test/continue/test",
        "account_id": "test_account_123"
    }
    
    # Convert to form-encoded data
    form_data = urlencode(test_data)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/kommo/chat/webhook",
                content=form_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30.0
            )
            
            print(f"✅ Response Status: {response.status_code}")
            print(f"✅ Response Body: {response.text}")
            
            if response.status_code == 200:
                print("🎉 Chat webhook test successful!")
            else:
                print("❌ Chat webhook test failed!")
                
    except Exception as e:
        print(f"❌ Error testing chat webhook: {e}")

async def test_chat_status():
    """Test the chat status endpoint"""
    print("\n🧪 Testing Chat Status Endpoint...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/api/kommo/chat/status",
                timeout=10.0
            )
            
            print(f"✅ Response Status: {response.status_code}")
            print(f"✅ Response Body: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing chat status: {e}")

async def main():
    """Run all tests"""
    print("🚀 Starting Kommo Chat Integration Tests...\n")
    
    await test_chat_webhook()
    await test_chat_status()
    
    print("\n✨ Tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
