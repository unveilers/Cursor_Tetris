#!/usr/bin/env python3
"""
Debug script to examine the actual page content of database entries
to find where files are stored (in page blocks rather than properties).
"""

import os
import json
from notion_client import Client

def debug_page_content():
    """Debug the page content of database entries to find file references."""
    
    api_token = os.getenv("NOTION_API_TOKEN")
    if not api_token:
        print("ERROR: NOTION_API_TOKEN not set")
        return
    
    client = Client(auth=api_token)
    database_id = "2346c988-6db2-807f-99ba-f5e379774c1c"
    
    print("=== Page Content Debug ===")
    
    response = client.databases.query(database_id=database_id, page_size=5)
    entries = response.get("results", [])
    
    for i, entry in enumerate(entries[:3]):
        page_id = entry["id"]
        
        properties = entry.get("properties", {})
        name_prop = properties.get("Name", {})
        title_text = ''.join([t.get('plain_text', '') for t in name_prop.get('title', [])])
        
        print(f"\n--- Entry {i+1}: {title_text} ---")
        print(f"Page ID: {page_id}")
        
        try:
            blocks_response = client.blocks.children.list(block_id=page_id)
            blocks = blocks_response.get("results", [])
            
            print(f"Found {len(blocks)} blocks in page content:")
            
            for j, block in enumerate(blocks):
                block_type = block.get("type", "unknown")
                print(f"  Block {j+1}: {block_type}")
                
                if block_type == "file":
                    file_info = block.get("file", {})
                    if file_info.get("type") == "file":
                        print(f"    File URL: {file_info.get('file', {}).get('url', 'N/A')}")
                    elif file_info.get("type") == "external":
                        print(f"    External URL: {file_info.get('external', {}).get('url', 'N/A')}")
                
                elif block_type == "embed":
                    embed_info = block.get("embed", {})
                    print(f"    Embed URL: {embed_info.get('url', 'N/A')}")
                
                elif block_type == "link_to_page":
                    link_info = block.get("link_to_page", {})
                    if link_info.get("type") == "page_id":
                        print(f"    Linked Page ID: {link_info.get('page_id', 'N/A')}")
                
                elif block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item"]:
                    rich_text = block.get(block_type, {}).get("rich_text", [])
                    for text_obj in rich_text:
                        if text_obj.get("href"):
                            print(f"    Link in text: {text_obj.get('href')}")
                        plain_text = text_obj.get("plain_text", "")
                        if "http" in plain_text:
                            print(f"    URL in text: {plain_text}")
                
                if j < 2:  # Only show first 2 blocks in detail
                    print(f"    Full block: {json.dumps(block, indent=4, ensure_ascii=False)}")
        
        except Exception as e:
            print(f"Error getting page content: {e}")

if __name__ == "__main__":
    debug_page_content()
