# Notion Database Automation Setup Instructions

This guide will help you set up the Notion integration to automatically add columns and populate data in your "项目笔记 - yuanxu (1)" database.

## Prerequisites

- Python 3.7+ installed
- Access to your Notion workspace
- Admin permissions to create integrations

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

## Step 3: Set Up Environment

1. Install required Python packages:
   ```bash
   pip install notion-client requests
   ```

2. Set the API token as an environment variable:
   ```bash
   export NOTION_API_TOKEN="your_integration_token_here"
   ```
   
   Replace `your_integration_token_here` with the token you copied in Step 1.

## Step 4: Run the Automation

```bash
python notion_database_automation.py
```

## What the Script Does

1. **Connects** to your Notion workspace using the API token
2. **Finds** the "项目笔记 - yuanxu (1)" database
3. **Adds** four new columns:
   - 估值 (Valuation)
   - 概要 (Overview)
   - 市场规模 (Market Size)
   - 营收 (Revenue)
4. **Reads** files referenced in the first column of each database entry
5. **Extracts** relevant information from those files
6. **Populates** the new columns with the extracted data

## Troubleshooting

### "Database not found" error
- Make sure you've shared the database with your integration (Step 2)
- Verify the database name is exactly "项目笔记 - yuanxu (1)"

### "Unauthorized" error
- Check that your API token is correct
- Ensure the integration has access to your workspace

### "No file references found"
- The script looks for files, URLs, or links in the first column
- Make sure your database entries have file references in the first column

### Rate limiting
- The Notion API has rate limits
- The script includes error handling for this, but large databases may take time

## Security Notes

- Keep your API token secure and never share it
- The token gives access to your Notion workspace
- You can revoke the integration at any time from the integrations page

## Support

If you encounter issues:
1. Check the console output for detailed error messages
2. Verify all setup steps were completed correctly
3. Ensure your database structure matches expectations
