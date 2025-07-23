#!/usr/bin/env python3
"""
Debug script to examine the structure of the Notion database entries
to understand how files are referenced in the first column.
"""

import os
import json
from notion_client import Client

def debug_database_structure():
    """Debug the database structure to understand file references."""
    
    api_token = os.getenv("NOTION_API_TOKEN")
    if not api_token:
        print("ERROR: NOTION_API_TOKEN not set")
        return
    
    client = Client(auth=api_token)
    database_id = "2346c988-6db2-807f-99ba-f5e379774c1c"
    
    print("=== Database Structure Debug ===")
    
    print("\n1. Database Schema:")
    db_response = client.databases.retrieve(database_id=database_id)
    properties = db_response.get("properties", {})
    
    for prop_name, prop_config in properties.items():
        print(f"   - {prop_name}: {prop_config.get('type', 'unknown')}")
    
    print("\n2. Sample Entries Structure:")
    response = client.databases.query(database_id=database_id, page_size=5)
    entries = response.get("results", [])
    
    for i, entry in enumerate(entries[:3]):
        print(f"\n--- Entry {i+1} ---")
        properties = entry.get("properties", {})
        
        first_prop_key = list(properties.keys())[0] if properties else None
        if first_prop_key:
            first_prop = properties[first_prop_key]
            print(f"First column '{first_prop_key}' type: {first_prop.get('type')}")
            print(f"First column content: {json.dumps(first_prop, indent=2, ensure_ascii=False)}")
        
        print("All properties:")
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get('type', 'unknown')
            print(f"   - {prop_name} ({prop_type})")
            
            if prop_type == 'title':
                title_text = ''.join([t.get('plain_text', '') for t in prop_data.get('title', [])])
                print(f"     Content: '{title_text}'")
            elif prop_type == 'rich_text':
                rich_text = ''.join([t.get('plain_text', '') for t in prop_data.get('rich_text', [])])
                print(f"     Content: '{rich_text}'")
            elif prop_type == 'url':
                print(f"     URL: {prop_data.get('url', 'None')}")
            elif prop_type == 'files':
                files = prop_data.get('files', [])
                print(f"     Files count: {len(files)}")
                for file_obj in files:
                    print(f"       - {file_obj}")

if __name__ == "__main__":
    debug_database_structure()
