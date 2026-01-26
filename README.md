# PRD Assistant - Payment Integration Workflow System

A systematic approach to payment provider integrations using **Antigravity** with PRD-First methodology.

## Overview
This project handles 3-4 payment provider integrations daily using a standardized, phase-based workflow. Built for **Jupyter Notebook-style execution** where you can run individual steps, iterate until satisfied, or execute entire phases at once.

## Quick Start

### 1. Create New Integration
```bash
# Copy the template
cp -r integrations/_TEMPLATE integrations/Integration_ProviderName_Country_Currency_Method

# Example: Integration_SmartFastPay_Ecuador_USD_PayinHPP
```

### 2. Prepare Integration Folder
```bash
cd integrations/Integration_ProviderName_...

# Add provider docs and Epic requirements to 0_initial_docs/
# Fill in the config file with credentials and API URLs
```

### 3. Execute Research Phase
Open the integration folder in Antigravity and run:

**Option A: Step-by-step** (iterative, Jupyter-style)
```
/step1-epic-analysis
[Review output, re-run if needed]

/step2-docs-analysis
[Review output, re-run if needed]

/step3-test-page
[Review output, test manually, re-run if needed]

... continue through step7
```

**Option B: Full phase** (automated)
```
/phase1-full
[Agent executes all 7 steps, confirms between steps]
```

## Project Structure

```
prd_assistant/
├── .gemini.md                    # Global rules (auto-loaded by Antigravity)
├── .agent/
│   ├── skills/
│   │   └── test_page_generator/  # Auto-triggered for Step 3
│   └── workflows/
│       ├── phase1-full.md        # /phase1-full
│       ├── step1-epic-analysis.md
│       ├── step2-docs-analysis.md
│       ├── step3-test-page.md
│       ├── step4-access-fields.md
│       ├── step5-compatibility.md
│       ├── step6-project-stories.md
│       └── step7-field-testing.md
├── global_rules/
│   └── master_prd.yaml           # PRD schema definition
├── integrations/
│   ├── _TEMPLATE/                # Template for new integrations
│   └── Integration_<Name>/       # Actual integration workspaces
│       ├── 0_initial_docs/       # Epic, provider docs (immutable)
│       ├── 1_research/           # Phase 1 outputs (7 files)
│       ├── 2_development/        # Phase 2 outputs
│       ├── 4_test/               # Phase 4 QA outputs
│       ├── config                # API credentials, URLs
│       └── project_rules.md      # Optional: integration-specific overrides
└── _archive/                     # Deprecated: old instruction files
```

## Workflow Commands

### Phase 1: Research (7 Steps)
| Command | Description |
|---------|-------------|
| `/phase1-full` | Execute all 7 research steps |
| `/step1-epic-analysis` | Analyze Epic/Jira requirements |
| `/step2-docs-analysis` | Deep dive into API documentation |
| `/step3-test-page` | Create functional HTML test page |
| `/step4-access-fields` | Verify credentials and field mappings |
| `/step5-compatibility` | Check architectural compatibility |
| `/step6-project-stories` | Fill technical specifications for all stories |
| `/step7-field-testing` | Test edge cases and field formats |

### Phase 2: Development (Coming Soon)
Development workflows to be added.

### Phase 4: Testing (Coming Soon)
QA and validation workflows to be added.

## Key Features

### 🎯 Jupyter Notebook Execution Style
- Execute individual steps and review results
- Re-run specific steps until results are satisfactory
- Full control over iteration speed

### 🤖 Antigravity Native Configuration
- **Rules**: `.gemini.md` loaded automatically (no manual prompting)
- **Skills**: Auto-triggered by context (e.g., test page generation)
- **Workflows**: Slash commands for step-by-step execution

### 📋 PRD-First Methodology
All integrations follow the **Hierarchy of Truth**:
1. Integration-specific `project_rules.md` (highest priority)
2. BetterBro standards
3. Master PRD schema
4. Provider documentation (validated via testing)

### 🔄 Template-Based Workflow
Create 3-4 integrations daily from standardized template:
- Consistent folder structure
- Pre-configured config file
- Ready-to-use workflows

## Global Rules

### BetterBro Standards
- H2H preferred over Redirects
- PIX = dynamic QR codes
- Webhooks must be authenticated
- Field mapping follows BetterBro schema

### Working Directory Isolation
- Research Agent → `1_research/` only
- Development Agent → `2_development/` only
- Test Agent → `4_test/` only

### Configuration Files
Every integration has:
- `config`: API credentials, documentation URL, webhook test URLs
- `project_rules.md` (optional): Integration-specific overrides

## Skills

### test_page_generator
Auto-triggered during Step 3 or when user mentions "create test page".

**Generates**:
- Functional HTML test page with credential input
- Token generation and transaction creation
- Webhook polling and display
- Request/response logging

**Output**:
- `3.test_page.html`
- `3.local_test_page.md` (with usage instructions)

## Migration from Old System

### Deprecated Files (archived in `_archive/`)
- `integrations/instruction.md` → Now `.agent/workflows/`
- `global_prompts/*.md` → Now `.gemini.md` + Skills
- `global_rules/README.md` → Merged into `.gemini.md`

### What Changed
- **Before**: Manually tell agent to "follow instruction.md"
- **After**: Antigravity auto-loads `.gemini.md` rules
- **Before**: Copy instructions for each step
- **After**: Run `/step1-epic-analysis` workflows
- **Before**: Manually create test pages
- **After**: `test_page_generator` skill auto-triggers

## Tips

### Creating New Integrations
1. Always copy from `_TEMPLATE`, don't create from scratch
2. Fill `config` before starting workflows
3. Populate `0_initial_docs/` with Epic and provider docs

### Iterative Refinement
```
You: /step2-docs-analysis
Agent: [Creates 2.docs_analysis.md]

You: The authentication section is incomplete, re-run step 2
Agent: [Re-runs step 2 with more detail]

You: Perfect! /step3-test-page
```

### Custom Rules
If an integration needs special handling:
1. Create `project_rules.md` in that integration folder
2. Document the override (e.g., "Skip webhook testing")
3. Rules apply only to that integration

### Parallel Agent Work (Advanced)
Use Antigravity's Agent Manager to:
- Set up multiple integrations in parallel
- Run different phases concurrently
- Batch process similar providers

## Support
For questions about:
- **BetterBro Standards**: See `.gemini.md` → BetterBro Standards section
- **Workflow Steps**: Read individual workflow files in `.agent/workflows/`
- **Skills**: Check `.agent/skills/<skill-name>/SKILL.md`
- **Master PRD Schema**: See `global_rules/master_prd.yaml`
