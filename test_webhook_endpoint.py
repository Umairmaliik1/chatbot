#!/usr/bin/env python3
"""
Test script to verify the Kommo webhook endpoint is working
"""

import requests
import json

def test_webhook_endpoint():
    webhook_url = "https://9dfbf46b7e88.ngrok-free.app/api/kommo/kommo/widget-request"
    
    # Test data similar to what Kommo would send
    test_payload = {
        "token": "test_jwt_token_123",
        "data": {
            "message": "Hello from test!",
            "from": "widget",
            "chat_id": "test_chat_123",
            "lead_id": "test_lead_456",
            "visitor_id": "test_visitor_789"
        },
        "return_url": "https://test.kommo.com/api/v4/salesbot/test/continue/test"
    }
    
    print(f"🧪 Testing webhook endpoint: {webhook_url}")
    print(f"📤 Sending test payload: {json.dumps(test_payload, indent=2)}")
    
    try:
        # Send POST request to webhook
        response = requests.post(
            webhook_url,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n📥 Response received:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Webhook endpoint is working!")
            print("   Your server received and processed the request")
        else:
            print(f"❌ ERROR: Server returned status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Cannot connect to your server")
        print("   Possible issues:")
        print("   - ngrok tunnel is down")
        print("   - Server is not running")
        print("   - Firewall blocking connections")
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Server took too long to respond")
        print("   Your webhook handler might be hanging")
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

def test_server_status():
    base_url = "https://9dfbf46b7e88.ngrok-free.app"
    
    print(f"\n🔍 Testing server status: {base_url}")
    
    try:
        # Test basic server response
        response = requests.get(f"{base_url}/api/kommo/test", timeout=10)
        print(f"   Test endpoint: {response.status_code} - {response.text}")
        
        # Test if server is reachable
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Root endpoint: {response.status_code}")
        
    except Exception as e:
        print(f"   ❌ Server test failed: {e}")

if __name__ == "__main__":
    print("🚀 Kommo Webhook Endpoint Test")
    print("=" * 50)
    
    test_server_status()
    test_webhook_endpoint()
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. If webhook test fails: Check server/ngrok")
    print("2. If webhook test succeeds: Check Kommo configuration")
    print("3. Verify Salesbot is active and configured")
    print("4. Check Kommo logs for any errors")


