#!/usr/bin/env python3
"""
Test script to verify Notion API connection and find the target database.
Run this first to ensure everything is set up correctly.
"""

import os
import sys
from notion_client import Client

def test_notion_connection():
    """Test the Notion API connection and search for the target database."""
    
    api_token = os.getenv("NOTION_API_TOKEN")
    
    if not api_token:
        print("❌ ERROR: NOTION_API_TOKEN environment variable not set!")
        print("\nPlease follow the setup instructions in setup_instructions.md")
        return False
    
    try:
        print("🔗 Testing Notion API connection...")
        client = Client(auth=api_token)
        
        print("✅ Connection successful!")
        print("\n🔍 Searching for databases...")
        
        response = client.search(
            filter={"property": "object", "value": "database"}
        )
        
        databases = response.get("results", [])
        print(f"📊 Found {len(databases)} databases:")
        
        target_found = False
        target_name = "项目笔记 - yuanxu (1)"
        
        for i, db in enumerate(databases, 1):
            title_parts = db.get("title", [])
            db_title = "".join([part.get("plain_text", "") for part in title_parts])
            db_id = db["id"]
            
            print(f"  {i}. {db_title} (ID: {db_id})")
            
            if target_name in db_title:
                target_found = True
                print(f"     🎯 TARGET DATABASE FOUND!")
        
        if target_found:
            print(f"\n✅ Setup verification successful!")
            print(f"   Target database '{target_name}' is accessible.")
            print(f"   You can now run the main automation script.")
            return True
        else:
            print(f"\n❌ Target database '{target_name}' not found!")
            print(f"   Please check:")
            print(f"   1. Database name is exactly '{target_name}'")
            print(f"   2. Integration has access to the database (share it)")
            print(f"   3. Database is in the correct workspace")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPlease check:")
        print("1. API token is correct")
        print("2. Integration is properly configured")
        print("3. Network connection is working")
        return False

if __name__ == "__main__":
    print("=== Notion Connection Test ===")
    success = test_notion_connection()
    sys.exit(0 if success else 1)
