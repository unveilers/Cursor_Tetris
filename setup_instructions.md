# Notion Database Automation Setup Instructions

This guide will help you set up the Notion integration with MiniMax M1 AI to automatically add columns and populate data in your "项目笔记 - yuanxu (1)" database with improved accuracy.

## Prerequisites

- Python 3.7+ installed
- Access to your Notion workspace
- Admin permissions to create integrations
- AI/ML API account for MiniMax M1 access

## Step 1: Create a Notion Integration

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **"New integration"**
3. Fill in the details:
   - **Name**: `Database Automation` (or any name you prefer)
   - **Logo**: Optional
   - **Associated workspace**: Select your workspace containing the database
4. Click **"Submit"**
5. Copy the **"Internal Integration Token"** (starts with `secret_`)

## Step 2: Give Integration Access to Your Database

1. Open your "项目笔记 - yuanxu (1)" database in Notion
2. Click the **"Share"** button (top right)
3. Click **"Invite"**
4. Search for your integration name (e.g., "Database Automation")
5. Select it and click **"Invite"**

## Step 3: Set Up MiniMax M1 API

1. Sign up for AI/ML API at [https://aimlapi.com](https://aimlapi.com)
2. Navigate to the API Key section and create a new API key
3. Copy your API key (starts with `sk-`)

## Step 4: Set Up Environment

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set the API tokens as environment variables:
   ```bash
   export NOTION_API_TOKEN="your_notion_integration_token_here"
   export AIMLAPI_KEY="your_aimlapi_key_here"
   ```
   
   Replace the tokens with:
   - `your_notion_integration_token_here`: Token from Step 1
   - `your_aimlapi_key_here`: API key from Step 3

3. Test the MiniMax M1 API integration:
   ```bash
   python test_minimax_integration.py
   ```

## Step 5: Run the Automation

```bash
python notion_database_automation.py
```

## What the Script Does

1. **Connects** to your Notion workspace using the API token
2. **Finds** the "项目笔记 - yuanxu (1)" database
3. **Adds** four new columns (if they don't exist):
   - 估值 (Valuation)
   - 概要 (Overview)
   - 市场规模 (Market Size)
   - 营收 (Revenue)
4. **Reads** content from each page in the database
5. **Analyzes** content using MiniMax M1 AI for accurate information extraction
6. **Populates** the columns with AI-extracted structured data
7. **Falls back** to keyword matching if AI analysis fails

## Troubleshooting

### "Database not found" error
- Make sure you've shared the database with your integration (Step 2)
- Verify the database name is exactly "项目笔记 - yuanxu (1)"

### "Unauthorized" error
- Check that your API token is correct
- Ensure the integration has access to your workspace

### "AIMLAPI_KEY not set" error
- Make sure you've set the MiniMax M1 API key environment variable
- Verify your API key is correct and has sufficient credits

### "No content found" error
- The script reads content directly from Notion pages
- Make sure your database entries have meaningful content in their pages

### Rate limiting
- Both Notion API and MiniMax M1 API have rate limits
- The script includes delays and error handling, but large databases may take time

### API costs
- MiniMax M1 API usage incurs costs based on token usage
- Monitor your API usage to control costs

## Security Notes

- Keep your API token secure and never share it
- The token gives access to your Notion workspace
- You can revoke the integration at any time from the integrations page

## Support

If you encounter issues:
1. Check the console output for detailed error messages
2. Verify all setup steps were completed correctly
3. Ensure your database structure matches expectations
