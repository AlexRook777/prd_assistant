---
description: Install and configure Atlassian MCP Server with API token authentication
---

# Install Atlassian MCP Server

This workflow will guide you through installing and configuring the Atlassian MCP Server to enable direct Jira/Confluence access in Antigravity.

## Prerequisites

- Node.js and npm installed (comes with Antigravity)
- Atlassian Cloud account with admin or API access
- Internet connection

## Step 1: Generate Atlassian API Token

Before we begin configuration, you need to generate an API token from Atlassian.

**Instructions:**

1. Open this URL in your browser:
   ```
   https://id.atlassian.com/manage-profile/security/api-tokens
   ```

2. Click **"Create API token"**

3. Enter a label (e.g., "Antigravity MCP")

4. Click **"Create"**

5. **IMPORTANT:** Copy the generated token immediately (it won't be shown again!)

6. Keep this token handy - you'll need it in the next step

## Step 2: Gather Required Information

You'll need three pieces of information:

1. **ATLASSIAN_EMAIL**: Your Atlassian account email (e.g., `user@company.com`)
2. **ATLASSIAN_API_TOKEN**: The token you just generated in Step 1
3. **ATLASSIAN_DOMAIN**: Your Atlassian instance domain (e.g., `yourcompany.atlassian.net`)
   - Find this from any Jira/Confluence URL: `https://DOMAIN/...`
   - Do NOT include `https://` - just the domain name

**Please provide the following information:**

- What is your **Atlassian email**?
- What is your **Atlassian API token**?
- What is your **Atlassian domain** (without https://)?

*The agent will wait for your input before proceeding.*

## Step 3: Locate MCP Configuration File

The agent will locate the correct MCP configuration file for your system:
- Path: `~/.gemini/antigravity/mcp_config.json` (cross-platform)

## Step 4: Configure MCP Server

The agent will update the `mcp_config.json` file with the following configuration:

```json
{
  "mcpServers": {
    "atlassian-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "@xuandev/atlassian-mcp"
      ],
      "env": {
        "ATLASSIAN_EMAIL": "<your-email>",
        "ATLASSIAN_API_TOKEN": "<your-token>",
        "ATLASSIAN_DOMAIN": "<your-domain>"
      }
    }
  }
}
```

## Step 5: Restart Antigravity

**IMPORTANT:** You must restart Antigravity for the changes to take effect.

1. Close Antigravity completely
2. Reopen Antigravity
3. Return to this conversation

*The agent will wait for confirmation that you've restarted.*

## Step 6: Verify Installation

The agent will test the MCP connection by running:

```
@mcp:atlassian: List all available Jira projects.
```

**Expected Result:**
- You should see a list of all Jira projects from your Atlassian instance
- This confirms the MCP server is working correctly

**If verification fails**, the agent will:
1. Check the error message
2. Identify the issue (wrong credentials, network problem, etc.)
3. Ask you to update the information
4. Repeat from Step 4

## Step 7: Success Confirmation

Once verification succeeds, the installation is complete! 

You can now use the MCP server to:
- Fetch Jira issues automatically in workflows
- Search projects and issues
- Create and update issues
- Add comments
- And much more!

## Troubleshooting

### Common Issues:

**Issue 1: "Missing required configuration: domain"**
- **Cause:** Environment variable name is wrong
- **Solution:** Ensure you're using `ATLASSIAN_DOMAIN` (not `ATLASSIAN_BASE_URL`)
- **Solution:** Ensure domain is just the hostname (e.g., `company.atlassian.net`), not a full URL

**Issue 2: "401 Unauthorized"**
- **Cause:** Invalid API token or email
- **Solution:** Regenerate API token and ensure email is correct

**Issue 3: "404 Not Found" for package**
- **Cause:** Wrong package name
- **Solution:** Ensure using `@xuandev/atlassian-mcp` (not `@modelcontextprotocol/server-atlassian`)

**Issue 4: OAuth dialog appears**
- **Cause:** Using remote OAuth server instead of local API token server
- **Solution:** Ensure `args` includes `@xuandev/atlassian-mcp` (not `mcp-remote`)

### Platform-Specific Notes:

**Ubuntu/Linux:**
- Config file location: `~/.gemini/antigravity/mcp_config.json`
- No special permissions needed

**macOS:**
- Config file location: `~/.gemini/antigravity/mcp_config.json`
- May need to allow npm in security settings

**Windows:**
- Config file location: `%USERPROFILE%\.gemini\antigravity\mcp_config.json`
- Use PowerShell or Command Prompt for any manual verification

## Manual Verification (Optional)

If you want to manually verify the configuration:

1. Check the config file exists:
   ```bash
   cat ~/.gemini/antigravity/mcp_config.json
   ```

2. Manually test the MCP package (optional):
   ```bash
   npx -y @xuandev/atlassian-mcp --help
   ```

## Uninstallation

To remove the Atlassian MCP server:

1. Open `~/.gemini/antigravity/mcp_config.json`
2. Remove the `"atlassian-mcp-server"` section from `mcpServers`
3. Restart Antigravity

## Security Notes

- Your API token is stored locally in the config file
- The token has the same permissions as your Atlassian account
- Keep the config file secure and don't commit it to version control
- You can revoke the token anytime at: https://id.atlassian.com/manage-profile/security/api-tokens
