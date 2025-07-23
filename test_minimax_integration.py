#!/usr/bin/env python3
"""
Test script to verify MiniMax M1 API integration works correctly.
Run this to test the API connection and content analysis before running the full automation.
"""

import os
import sys
import requests
import json
import re

def test_minimax_api():
    """Test the MiniMax M1 API integration with sample content."""
    
    api_key = os.getenv("AIMLAPI_KEY")
    
    if not api_key:
        print("❌ ERROR: AIMLAPI_KEY environment variable not set!")
        print("\nPlease set your AI/ML API key:")
        print("export AIMLAPI_KEY='your_api_key_here'")
        return False
    
    test_content = """
    小红书是一个生活方式平台和消费决策入口，由毛文超和瞿芳于2013年在上海创立。
    公司在2021年完成E轮融资，估值超过200亿美元，成为中国最有价值的独角兽公司之一。
    平台拥有超过4.5亿注册用户，月活跃用户超过2亿，主要用户群体为18-35岁的年轻女性。
    小红书的商业模式主要包括广告收入和电商佣金，2023年预计营收超过100亿人民币。
    中国社交电商市场规模预计在2025年将达到3万亿人民币，小红书在其中占据重要地位。
    """
    
    prompt = f"""请分析以下商业内容，并提取四个关键信息类别。请以JSON格式返回结果，包含以下字段：

1. "估值": 提取公司估值、融资金额、投资轮次等相关信息
2. "概要": 生成简洁的业务概要（不超过150字）
3. "市场规模": 提取市场规模、目标市场、行业数据等信息
4. "营收": 提取营收、销售额、财务表现等相关数据

如果某个类别的信息不存在或不明确，请返回空字符串。

内容：
{test_content}

请返回标准JSON格式：
{{"估值": "", "概要": "", "市场规模": "", "营收": ""}}"""

    try:
        print("🔗 Testing MiniMax M1 API connection...")
        
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
            
            print("✅ API connection successful!")
            print(f"\n📝 Raw API Response:")
            print(content_text)
            
            try:
                json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
                if json_match:
                    extracted_info = json.loads(json_match.group())
                    
                    print(f"\n🎯 Extracted Information:")
                    for key, value in extracted_info.items():
                        print(f"  {key}: {value}")
                    
                    required_keys = ["估值", "概要", "市场规模", "营收"]
                    if all(key in extracted_info for key in required_keys):
                        print("\n✅ JSON structure validation passed!")
                        print("🚀 MiniMax M1 API integration is working correctly!")
                        return True
                    else:
                        print(f"\n❌ Missing required keys in response")
                        return False
                else:
                    print(f"\n❌ No JSON found in API response")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ Failed to parse JSON response: {e}")
                return False
                
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MiniMax M1 API Integration Test ===")
    success = test_minimax_api()
    sys.exit(0 if success else 1)
