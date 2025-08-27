#!/usr/bin/env python3
"""
Test Widget Installation Endpoints
This script tests the widget installation and status endpoints
"""

import asyncio
import httpx
import json

async def test_widget_endpoints():
    """Test widget-related endpoints"""
    print("🧪 Testing Widget Installation Endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Chat Status Endpoint
    print("\n1️⃣ Testing Chat Status Endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/kommo/chat/status")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Active: {data.get('active')}")
                print(f"   ✅ Widget Installed: {data.get('widget_installed')}")
                print(f"   ✅ Salesbot Active: {data.get('salesbot_active')}")
                print(f"   ✅ Domain: {data.get('kommo_domain')}")
            else:
                print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Widget Install Endpoint
    print("\n2️⃣ Testing Widget Install Endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{base_url}/api/kommo/widget/install")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data.get('success')}")
                print(f"   ✅ Message: {data.get('message')}")
            else:
                print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Test Chat Endpoint
    print("\n3️⃣ Testing Chat Test Endpoint...")
    try:
        test_message = {"message": "Hello, can you help me test the widget?"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/kommo/chat/test",
                json=test_message
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data.get('success')}")
                print(f"   ✅ AI Response: {data.get('response', '')[:100]}...")
            else:
                print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎯 Verification Summary:")
    print("✅ If all endpoints return 200 - Widget installation is working")
    print("✅ If chat status shows widget_installed: true - Widget is marked as installed")
    print("✅ If test chat generates AI response - Chat integration is working")
    print("❌ If any endpoint fails - Check the error messages above")

if __name__ == "__main__":
    asyncio.run(test_widget_endpoints())
