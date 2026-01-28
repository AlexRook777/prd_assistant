---
description: Create a new integration workspace
---

1. Ask the user for the name of the new integration. 
   - Suggest the naming convention: `Integration_<ProviderName> <Country> <Currency> <Flow>` (e.g., `Integration_SmartFastPay Ecuador USD Payin HPP`).
   - Confirm the name with the user before proceeding.

2. Check if the integration directory already exists to prevent accidental overwrites.
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

3. Create the folder structure for the new integration.
   - Run the command appropriate for your OS (replace `<Integration_Name>` with the user's provided name).

     **Linux / macOS (Bash/Zsh):**
     ```bash
     mkdir -p "integrations/<Integration_Name>/0_initial_docs"
     mkdir -p "integrations/<Integration_Name>/1_research"
     mkdir -p "integrations/<Integration_Name>/2_development"
     mkdir -p "integrations/<Integration_Name>/4_test"
     ```

     **Windows (PowerShell):**
     ```powershell
     $subfolders = "0_initial_docs", "1_research", "2_development", "4_test"
     foreach ($folder in $subfolders) {
         New-Item -ItemType Directory -Path "integrations\<Integration_Name>\$folder" -Force
     }
     ```

4. ALWAYS Create the `config` file.
   - create file `integrations/<Integration_Name>/config` with the following content:
     ```
     # Configuration file for payment provider integration

     # Provider API Documentation
     PROVIDER_API_DOCUMENTATION_URL=https://docs.provider.com/api/v1

     # Provider API Credentials (from provider's dashboard)
     CLIENT_ID=your_client_id_here
     CLIENT_SECRET=your_client_secret_here
     ```

5. ALWAYS Create the `project_rules.md` file.
   - create file `integrations/<Integration_Name>/project_rules.md` with the following content:
     ```markdown
     # Integration-Specific Rules

     Local overrides and specific context for this integration.
     ```

6. Verify that the folders and files have been created correctly.
   - List the contents of the new integration directory.