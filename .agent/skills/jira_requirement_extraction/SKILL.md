---
name: Jira Requirement Extraction
description: deeply fetches all data from a Jira issue (tables, comments, limits) and updates a local documentation file.
---

# Jira Requirement Extraction Skill

This skill allows you to extract comprehensive information from a Jira issue—including complex formatting like tables, lists, transaction limits, and all comments—and save it to a structured Markdown file (`bizdev_request`).

**Crucial:** This skill uses a Python script to fetch data. You (the Agent) act as the parser of the JSON output. You must read the complex JSON output and intelligently convert it into a human-readable Markdown report.

## Inputs
- **Issue Key**: The Jira ticket ID (e.g., `IN-1137`).
- **Target File**: The path to the markdown file to create or update (e.g., `integrations/.../bizdev_request_IN-1137.md`).

## Workflow

### 1. Fetch Issue Data
### 1. Fetch Issue Data
Execute the robust Python fetcher script which bypasses truncation limits:
- Command: `python3 app/jira_fetcher.py [Input Issue Key]`
- Output: The script prints the full JSON to stdout.
- **Note**: Ensure `.env` exists with valid `ATLASSIAN_EMAIL` and `ATLASSIAN_API_TOKEN`.

### 2. Parse and Analyze (Mental Step)
carefully examine the JSON output. Do NOT just read the summary. You are looking for:
- **Description Fields (ADF Format)**:
  - **Tables**: Identify `table` nodes in user descriptions. These usually contain the most critical integration Q&A. Convert them faithfully to Markdown tables.
  - **Lists**: Convert bullet/numbered lists.
  - **Formatting**: Preserve bold, italics, and code blocks.
- **Transaction Limits**:
  - Scan text for patterns like "min X", "max Y", "daily limit", "monthly limit".
  - Group these logically (e.g., per country or currency).
- **Comments**:
  - Extract ALL comments.
  - Format as: `### Comment by [Author] ([Date])` followed by the quote.
  - Look for "BetterBro" links or "Provider Docs" links shared in comments.
- **Links**:
  - Collect ALL URLs found in the description and comments.
  - Create a "Key Links" section at the bottom.
- **Other Information**:
  - If you find valuable information (e.g., specific requirements, extra tables, side notes) that does not fit into the categories above, preserve it.
  - Create an "Other" section for this content.

### 3. Generate Markdown Content
Construct a Markdown file content following this template:

```markdown
# BizDev Integration Request: [Integration Name/Summary]

- **Jira Link**: https://[domain]/browse/[Issue-Key]
- **Issue Key**: [Issue-Key]
- **Created At**: [Created Date]

## Description

[Full converted description content with all tables and rich text]

## Transaction Limits

[Extracted limits formatted as a list or table]

## Integration Details - Q&A

[The main Q&A table extracted from the description]

## Other

[Any other valuable information found in the issue that didn't fit elsewhere]

## Comments

[Chronological list of comments]

## Key Links

[Bulleted list of all important URLs found]
```

### 4. Write/Update File
Call `write_to_file` to save the content to **Target File**.
- Set `Overwrite: true` to ensure the latest data is saved.
- This creates a "sync" effect—running this skill repeatedly will always update with the latest Jira state.
