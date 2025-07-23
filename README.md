# Notion Database Automation

This project automates the process of adding columns to a Notion database and populating them with extracted information from referenced files.

## Overview

The automation script connects to Frank's Notion workspace and:

1. **Adds 4 new columns** to the "项目笔记 - yuanxu (1)" database:
   - 估值 (Valuation)
   - 概要 (Overview) 
   - 市场规模 (Market Size)
   - 营收 (Revenue)

2. **Reads files** referenced in the first column of existing database entries

3. **Extracts relevant information** from those files using keyword matching and content analysis

4. **Populates the new columns** with the extracted data

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Notion integration** (see `setup_instructions.md` for detailed steps):
   - Create integration at https://www.notion.so/my-integrations
   - Copy the API token
   - Share your database with the integration

3. **Set environment variable:**
   ```bash
   export NOTION_API_TOKEN="your_token_here"
   ```

4. **Test the connection:**
   ```bash
   python test_connection.py
   ```

5. **Run the automation:**
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

- **Robust error handling** for network issues and API limits
- **Multiple file type support** (Notion pages, external URLs, file attachments)
- **Intelligent content extraction** using keyword matching
- **Progress logging** with detailed status updates
- **Safe operation** - only adds new columns, doesn't modify existing data

## Information Extraction

The script uses keyword matching to categorize information:

- **估值 (Valuation)**: Looks for funding, investment, valuation amounts
- **概要 (Overview)**: Creates summaries from main content and titles  
- **市场规模 (Market Size)**: Finds market size, TAM, industry data
- **营收 (Revenue)**: Extracts revenue, sales, financial performance data

## Security

- API tokens are handled securely through environment variables
- No sensitive data is logged or stored
- Integration permissions can be revoked at any time

## Troubleshooting

See `setup_instructions.md` for common issues and solutions.
