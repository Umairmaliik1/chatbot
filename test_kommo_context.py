#!/usr/bin/env python3
"""
Test Kommo Chat Context Integration
This script tests the new context-aware chat integration
"""

import asyncio
import httpx
import json

async def test_kommo_context():
    """Test the Kommo chat context integration"""
    print("🧪 Testing Kommo Chat Context Integration...")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Chat Context Endpoint
    print("\n1️⃣ Testing Chat Context Endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/kommo/chat/context")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data.get('success')}")
                print(f"   ✅ User ID: {data.get('user_id')}")
                print(f"   ✅ Instructions Length: {data.get('instructions_length')} characters")
                print(f"   ✅ FAQs Count: {data.get('faqs_count')}")
                print(f"   ✅ Instructions Preview: {data.get('instructions_preview', '')[:100]}...")
                
                if data.get('faqs'):
                    print(f"   ✅ FAQs Found: {len(data.get('faqs', []))}")
                    for i, faq in enumerate(data.get('faqs', [])[:2]):
                        print(f"      FAQ {i+1}: {faq.get('question', '')[:50]}...")
            else:
                print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Test Chat with Context
    print("\n2️⃣ Testing Chat with Context...")
    try:
        test_message = {"message": "What are your business hours?"}
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
                print(f"   ✅ Instructions Used: {data.get('instructions_used', '')[:100]}...")
            else:
                print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎯 Context Integration Summary:")
    print("✅ If context endpoint returns 200 - Context loading is working")
    print("✅ If instructions_length > 0 - User instructions are loaded")
    print("✅ If faqs_count > 0 - User FAQs are loaded")
    print("✅ If test chat generates contextual response - AI is using instructions/FAQs")
    print("❌ If any endpoint fails - Check the error messages above")

if __name__ == "__main__":
    asyncio.run(test_kommo_context())
