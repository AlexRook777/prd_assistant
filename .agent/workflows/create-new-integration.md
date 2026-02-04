---
description: Create a new integration workspace
---

1. Ask the user for the Jira link with the business development requirements.
    - Example valid link: `https://4billio.atlassian.net/browse/IN-1137`

2. Validate the provided Jira link.
    - The link MUST point to the Jira **Integration** space (look for the project key `IN-`).
    - If the link is not valid (e.g., doesn't contain `/browse/IN-`), explain the error to the user and ask them to provide a correct link. Repeat this step until a valid link is provided.

3. Fetch the Jira issue details.
   - Use the `mcp_atlassian-mcp-server_getJiraIssue` tool to fetch the issue details using the Issue Key or ID from the URL (e.g., `IN-1137`).
   - Ensure you get the description, summary, and comments.

4. Extract and confirm the integration name from the Jira Issue Summary.
   - The naming convention MUST be: `Integration_<ProviderName> <Country> <Currency> <Flow>` (e.g., `Integration_SmartFastPay Ecuador USD Payin HPP`).
   - Propose a name based on the Jira Issue Summary, formatting it to match the convention.
   - Confirm the proposed name with the user before proceeding. Allow them to edit it if needed.

5. Check if the integration directory already exists to prevent accidental overwrites.
   - Run the command appropriate for your OS (replace `<Integration_Name>` with the user's provided name).

     **Linux / macOS (Bash/Zsh):**
     ```bash
     if [ -d "integrations/<Integration_Name>" ]; then
         echo "❌ Error: Directory 'integrations/<Integration_Name>' already exists. Please choose a different name or remove the existing directory."
         exit 1
     else
         echo "✅ Directory is available. Proceeding..."
     fi
     ```

     **Windows (PowerShell):**
     ```powershell
     if (Test-Path "integrations\<Integration_Name>") {
         Write-Host "❌ Error: Directory 'integrations\<Integration_Name>' already exists. Please choose a different name or remove the existing directory." -ForegroundColor Red
         exit 1
     } else {
         Write-Host "✅ Directory is available. Proceeding..." -ForegroundColor Green
     }
     ```

6. Create the folder structure for the new integration.
   - Run the command appropriate for your OS (replace `<Integration_Name>` with the user's provided name).

     **Linux / macOS (Bash/Zsh):**
     ```bash
     mkdir -p "integrations/<Integration_Name>/0_initial_docs_and_config"
     mkdir -p "integrations/<Integration_Name>/1_result"

     ```

     **Windows (PowerShell):**
     ```powershell
     $subfolders = "0_initial_docs_and_config", "1_result"
     foreach ($folder in $subfolders) {
         New-Item -ItemType Directory -Path "integrations\<Integration_Name>\$folder" -Force
     }
     ```

7. Generate the `bizdev_request` file using the Jira Requirement Extraction Skill.
   - **Action**: Use the `view_file` tool to read and follow the instructions in `.agent/skills/jira_requirement_extraction/SKILL.md`.
   - **Goal**: Generate comprehensive documentation including tables, transaction limits, and comments without manual parsing.
   - **Inputs**:
     - `Issue Key`: The Jira issue key (e.g., `IN-1137`).
     - `Target File`: `integrations/<Integration_Name>/0_initial_docs_and_config/bizdev_request_<IssueKey>.md`.
   - **Note**: This skill handles formatting of ADF content, extraction of Q&A tables, and aggregation of comments automatically.


8. ALWAYS Create the `integration_config` file.
   - create file `integrations/<Integration_Name>/0_initial_docs_and_config/integration_config` with the following content:
     ```
     # Configuration file for payment provider integration

     # Provider API Documentation
     PROVIDER_API_DOCUMENTATION_URL=https://docs.provider.com/api/v1

     # Provider API Credentials (from provider's dashboard)
     CLIENT_ID=your_client_id_here
     CLIENT_SECRET=your_client_secret_here
     ```

9. ALWAYS Create the `project_rules.md` file.
   - create file `integrations/<Integration_Name>/0_initial_docs_and_config/project_rules.md` with the following content:
     ```markdown
     # Integration-Specific Rules

     Local overrides and specific context for this integration.
     ```

10. Verify that the folders and files have been created correctly.
   - List the contents of the new integration directory.