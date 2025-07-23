# Notion Database Automation with MiniMax M1 AI

This project automates the process of adding columns to a Notion database and populating them with AI-extracted information using MiniMax M1 for improved accuracy.

## Overview

The automation script connects to Frank's Notion workspace and:

1. **Adds 4 new columns** to the "项目笔记 - yuanxu (1)" database:
   - 估值 (Valuation)
   - 概要 (Overview) 
   - 市场规模 (Market Size)
   - 营收 (Revenue)

2. **Reads content** directly from Notion pages in the database

3. **Analyzes content** using MiniMax M1 AI for intelligent information extraction

4. **Populates the new columns** with AI-extracted structured data

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Notion integration** (see `setup_instructions.md` for detailed steps):
   - Create integration at https://www.notion.so/my-integrations
   - Copy the API token
   - Share your database with the integration

3. **Set up MiniMax M1 API:**
   - Sign up at https://aimlapi.com
   - Get your API key

4. **Set environment variables:**
   ```bash
   export NOTION_API_TOKEN="your_notion_token_here"
   export AIMLAPI_KEY="your_aimlapi_key_here"
   ```

5. **Test the connections:**
   ```bash
   python test_connection.py
   python test_minimax_integration.py
   ```

6. **Run the automation:**
   ```bash
   python notion_database_automation.py
   ```

## Files

- `notion_database_automation.py` - Main automation script
- `test_connection.py` - Connection test utility
- `setup_instructions.md` - Detailed setup guide
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Features

- **AI-Powered Analysis**: Uses MiniMax M1 for intelligent content analysis and information extraction
- **Fallback System**: Falls back to keyword matching if AI analysis fails
- **Robust error handling** for network issues and API limits
- **Content Analysis**: Reads and analyzes content directly from Notion pages
- **Rate Limiting**: Respects API rate limits with appropriate delays
- **Progress logging** with detailed status updates
- **Safe operation** - only adds new columns, doesn't modify existing data

## Information Extraction

The script uses MiniMax M1 AI to intelligently extract and categorize information:

- **估值 (Valuation)**: AI-extracted funding rounds, company valuations, investment amounts
- **概要 (Overview)**: AI-generated business summaries and key highlights  
- **市场规模 (Market Size)**: AI-identified market size, TAM, industry data
- **营收 (Revenue)**: AI-extracted revenue figures, sales data, financial performance

## Security

- API tokens are handled securely through environment variables
- No sensitive data is logged or stored
- Integration permissions can be revoked at any time

## Troubleshooting

See `setup_instructions.md` for common issues and solutions.
