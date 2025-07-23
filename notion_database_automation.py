#!/usr/bin/env python3
"""
Notion Database Automation Script with MiniMax M1 AI Integration
Connects to Frank's Notion workspace and modifies the "项目笔记 - yuanxu (1)" database
by adding new columns and populating them with AI-extracted information using MiniMax M1.
"""

import os
import sys
import re
import logging
import time
from typing import Dict, List, Optional, Any
from notion_client import Client
import requests
from urllib.parse import urlparse
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotionDatabaseAutomation:
    def __init__(self, api_token: str):
        """Initialize the Notion client with API token."""
        self.client = Client(auth=api_token)
        self.database_id = None
        self.target_database_name = "项目笔记 - yuanxu (1)"
        
        self.new_columns = {
            "估值": {"rich_text": {}},
            "概要": {"rich_text": {}}, 
            "市场规模": {"rich_text": {}},
            "营收": {"rich_text": {}}
        }
        
    def find_target_database(self) -> Optional[str]:
        """Find the target database by searching through all accessible databases."""
        logger.info(f"Searching for database: {self.target_database_name}")
        
        try:
            response = self.client.search(
                filter={"property": "object", "value": "database"}
            )
            
            for result in response.get("results", []):
                if result.get("object") == "database":
                    title_parts = result.get("title", [])
                    if title_parts:
                        db_title = "".join([part.get("plain_text", "") for part in title_parts])
                        logger.info(f"Found database: {db_title}")
                        
                        if self.target_database_name in db_title:
                            self.database_id = result["id"]
                            logger.info(f"Target database found! ID: {self.database_id}")
                            return self.database_id
            
            logger.error(f"Database '{self.target_database_name}' not found")
            return None
            
        except Exception as e:
            logger.error(f"Error searching for database: {e}")
            return None
    
    def get_database_schema(self) -> Dict[str, Any]:
        """Get the current database schema."""
        try:
            response = self.client.databases.retrieve(database_id=self.database_id)
            return response.get("properties", {})
        except Exception as e:
            logger.error(f"Error retrieving database schema: {e}")
            return {}
    
    def add_new_columns(self) -> bool:
        """Add the new columns to the database."""
        logger.info("Adding new columns to database...")
        
        try:
            current_properties = self.get_database_schema()
            
            for column_name, column_config in self.new_columns.items():
                if column_name not in current_properties:
                    logger.info(f"Adding column: {column_name}")
                    
                    update_data = {
                        "properties": {
                            column_name: column_config
                        }
                    }
                    
                    self.client.databases.update(
                        database_id=self.database_id,
                        **update_data
                    )
                    logger.info(f"Successfully added column: {column_name}")
                else:
                    logger.info(f"Column {column_name} already exists, skipping...")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding columns: {e}")
            return False
    
    def query_database_entries(self) -> List[Dict[str, Any]]:
        """Query all entries from the database."""
        logger.info("Querying database entries...")
        
        try:
            response = self.client.databases.query(database_id=self.database_id)
            entries = response.get("results", [])
            logger.info(f"Found {len(entries)} entries in database")
            return entries
            
        except Exception as e:
            logger.error(f"Error querying database: {e}")
            return []
    
    def extract_page_content(self, page_id: str) -> str:
        """Extract all text content from a Notion page."""
        try:
            blocks_response = self.client.blocks.children.list(block_id=page_id)
            blocks = blocks_response.get("results", [])
            
            content_parts = []
            
            for block in blocks:
                block_type = block.get("type", "")
                
                if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
                    rich_text = block.get(block_type, {}).get("rich_text", [])
                    text_content = ''.join([text_obj.get("plain_text", "") for text_obj in rich_text])
                    if text_content.strip():
                        content_parts.append(text_content.strip())
                
                elif block_type == "table":
                    try:
                        table_response = self.client.blocks.children.list(block_id=block["id"])
                        table_rows = table_response.get("results", [])
                        for row in table_rows:
                            if row.get("type") == "table_row":
                                cells = row.get("table_row", {}).get("cells", [])
                                row_text = []
                                for cell in cells:
                                    cell_text = ''.join([text_obj.get("plain_text", "") for text_obj in cell])
                                    row_text.append(cell_text.strip())
                                if any(row_text):
                                    content_parts.append(" | ".join(row_text))
                    except Exception as e:
                        self.logger.warning(f"Error extracting table content: {e}")
            
            return "\n".join(content_parts)
            
        except Exception as e:
            self.logger.error(f"Error extracting page content: {e}")
            return ""
    
    def fetch_content_from_url(self, url: str) -> str:
        """Fetch content from a URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {e}")
            return ""
    
    def get_notion_page_content(self, page_id: str) -> str:
        """Get content from a Notion page."""
        try:
            blocks_response = self.client.blocks.children.list(block_id=page_id)
            content = []
            
            for block in blocks_response.get("results", []):
                block_type = block.get("type")
                if block_type in ["paragraph", "heading_1", "heading_2", "heading_3"]:
                    rich_text = block.get(block_type, {}).get("rich_text", [])
                    text = "".join([t.get("plain_text", "") for t in rich_text])
                    if text.strip():
                        content.append(text.strip())
                elif block_type == "bulleted_list_item":
                    rich_text = block.get("bulleted_list_item", {}).get("rich_text", [])
                    text = "".join([t.get("plain_text", "") for t in rich_text])
                    if text.strip():
                        content.append(f"• {text.strip()}")
            
            return "\n".join(content)
            
        except Exception as e:
            logger.error(f"Error getting Notion page content: {e}")
            return ""
    
    def analyze_content_with_minimax(self, content: str) -> Dict[str, str]:
        """
        Analyze content using MiniMax M1 API to extract structured information.
        
        Args:
            content: The text content to analyze
            
        Returns:
            Dictionary with extracted information for each category
        """
        api_key = os.getenv("AIMLAPI_KEY")
        if not api_key:
            logger.error("AIMLAPI_KEY environment variable not set")
            return self.fallback_extraction(content)
        
        prompt = f"""请分析以下商业内容，并提取四个关键信息类别。请以JSON格式返回结果，包含以下字段：

1. "估值": 提取公司估值、融资金额、投资轮次等相关信息
2. "概要": 生成简洁的业务概要（不超过150字）
3. "市场规模": 提取市场规模、目标市场、行业数据等信息
4. "营收": 提取营收、销售额、财务表现等相关数据

如果某个类别的信息不存在或不明确，请返回空字符串。

内容：
{content[:8000]}

请返回标准JSON格式：
{{"估值": "", "概要": "", "市场规模": "", "营收": ""}}"""

        try:
            response = requests.post(
                "https://api.aimlapi.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "minimax/m1",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content_text = result["choices"][0]["message"]["content"]
                
                try:
                    json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
                    if json_match:
                        extracted_info = json.loads(json_match.group())
                        
                        required_keys = ["估值", "概要", "市场规模", "营收"]
                        if all(key in extracted_info for key in required_keys):
                            logger.info("Successfully extracted information using MiniMax M1")
                            return extracted_info
                        else:
                            logger.warning("MiniMax response missing required keys, using fallback")
                            return self.fallback_extraction(content)
                    else:
                        logger.warning("No JSON found in MiniMax response, using fallback")
                        return self.fallback_extraction(content)
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse MiniMax JSON response: {e}, using fallback")
                    return self.fallback_extraction(content)
                    
            else:
                logger.error(f"MiniMax API request failed with status {response.status_code}: {response.text}")
                return self.fallback_extraction(content)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"MiniMax API request failed: {e}")
            return self.fallback_extraction(content)
        except Exception as e:
            logger.error(f"Unexpected error in MiniMax analysis: {e}")
            return self.fallback_extraction(content)
    
    def fallback_extraction(self, content: str) -> Dict[str, str]:
        """
        Fallback extraction method using keyword matching when MiniMax API fails.
        
        Args:
            content: The text content to analyze
            
        Returns:
            Dictionary with extracted information for each category
        """
        content_lower = content.lower()
        
        valuation_keywords = [
            "valuation", "funding", "investment", "round", "million", "billion", 
            "估值", "融资", "投资", "轮", "万", "亿", "美元", "人民币", "$", "¥"
        ]
        
        market_size_keywords = [
            "market size", "tam", "industry", "sector", "market", "billion market",
            "市场规模", "市场", "行业", "领域", "规模", "市场容量"
        ]
        
        revenue_keywords = [
            "revenue", "sales", "income", "earnings", "profit", "turnover",
            "营收", "收入", "销售", "利润", "营业额", "盈利"
        ]
        
        extracted_info = {
            "估值": "",
            "概要": "",
            "市场规模": "",
            "营收": ""
        }
        
        sentences = re.split(r'[.!?。！？]', content)
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if not sentence_lower:
                continue
                
            if any(keyword in sentence_lower for keyword in valuation_keywords):
                if not extracted_info["估值"]:
                    extracted_info["估值"] = sentence.strip()[:200]
            
            if any(keyword in sentence_lower for keyword in market_size_keywords):
                if not extracted_info["市场规模"]:
                    extracted_info["市场规模"] = sentence.strip()[:200]
            
            if any(keyword in sentence_lower for keyword in revenue_keywords):
                if not extracted_info["营收"]:
                    extracted_info["营收"] = sentence.strip()[:200]
        
        if not extracted_info["概要"]:
            first_sentences = sentences[:3]
            extracted_info["概要"] = " ".join([s.strip() for s in first_sentences if s.strip()])[:300]
        
        return extracted_info
    
    def update_page_properties(self, page_id: str, extracted_info: Dict[str, str]) -> bool:
        """Update a page with the extracted information."""
        try:
            properties = {}
            
            for column_name, info in extracted_info.items():
                if info.strip():
                    properties[column_name] = {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": info.strip()}
                            }
                        ]
                    }
            
            if properties:
                self.client.pages.update(page_id=page_id, properties=properties)
                logger.info(f"Updated page {page_id} with extracted information")
                return True
            else:
                logger.info(f"No information to update for page {page_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error updating page {page_id}: {e}")
            return False
    
    def process_all_entries(self) -> bool:
        """Process all database entries and populate the new columns."""
        logger.info("Processing all database entries...")
        
        entries = self.query_database_entries()
        if not entries:
            logger.error("No entries found in database")
            return False
        
        success_count = 0
        
        for i, entry in enumerate(entries):
            logger.info(f"Processing entry {i+1}/{len(entries)}")
            
            page_id = entry["id"]
            page_content = self.extract_page_content(page_id)
            
            if not page_content.strip():
                logger.info(f"No content found in entry {i+1}")
                continue
            
            logger.info(f"Extracted {len(page_content)} characters of content from entry {i+1}")
            
            extracted_info = self.analyze_content_with_minimax(page_content)
            
            time.sleep(1)
            
            if self.update_page_properties(page_id, extracted_info):
                success_count += 1
                logger.info(f"Successfully updated entry {i+1}")
            else:
                logger.warning(f"Failed to update entry {i+1}")
        
        logger.info(f"Successfully processed {success_count}/{len(entries)} entries")
        return success_count > 0
    
    def run_automation(self) -> bool:
        """Run the complete automation process."""
        logger.info("Starting Notion database automation...")
        
        if not self.find_target_database():
            logger.error("Failed to find target database")
            return False
        
        if not self.add_new_columns():
            logger.error("Failed to add new columns")
            return False
        
        if not self.process_all_entries():
            logger.error("Failed to process entries")
            return False
        
        logger.info("Automation completed successfully!")
        return True

def main():
    """Main function to run the automation."""
    print("=== Notion Database Automation ===")
    print("This script will connect to your Notion workspace and modify the database.")
    print()
    
    api_token = os.getenv("NOTION_API_TOKEN")
    aimlapi_key = os.getenv("AIMLAPI_KEY")
    
    if not api_token:
        print("ERROR: NOTION_API_TOKEN environment variable not set!")
        print()
        print("To set up the integration:")
        print("1. Go to https://www.notion.so/my-integrations")
        print("2. Click 'New integration'")
        print("3. Give it a name (e.g., 'Database Automation')")
        print("4. Select your workspace")
        print("5. Copy the 'Internal Integration Token'")
        print("6. Set it as environment variable: export NOTION_API_TOKEN='your_token_here'")
        print("7. Give the integration access to your database by sharing it")
        print()
        sys.exit(1)
    
    if not aimlapi_key:
        print("WARNING: AIMLAPI_KEY environment variable not set!")
        print("The script will use fallback keyword extraction instead of MiniMax M1 AI.")
        print()
        print("To enable MiniMax M1 AI analysis:")
        print("1. Sign up at https://aimlapi.com")
        print("2. Get your API key")
        print("3. Set it as environment variable: export AIMLAPI_KEY='your_key_here'")
        print()
        input("Press Enter to continue with fallback extraction or Ctrl+C to exit...")
    
    automation = NotionDatabaseAutomation(api_token)
    
    try:
        success = automation.run_automation()
        if success:
            print("\n✅ Automation completed successfully!")
            print("Check your Notion database for the new columns and populated data.")
        else:
            print("\n❌ Automation failed. Check the logs for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Automation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
