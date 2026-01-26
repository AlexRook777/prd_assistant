# Workflow Commands Reference

This is a plain reference document listing all available workflows. Use this to avoid webview errors when reviewing workflow details.

---

## Available Slash Commands

### Phase-Level Commands
- `/phase1-full` - Execute all 7 research steps sequentially

### Individual Step Commands (Phase 1)
- `/step1-epic-analysis` - Analyze Epic/Jira requirements
- `/step2-docs-analysis` - Deep dive into API documentation  
- `/step3-test-page` - Create functional HTML test page
- `/step4-access-fields` - Verify credentials and field mappings
- `/step5-compatibility` - Check architectural compatibility
- `/step6-project-stories` - Fill technical specifications (7 stories)
- `/step7-field-testing` - Test edge cases and field formats

---

## How Workflows Work

1. **Don't click** on workflow files to open them (causes webview error)
2. **Instead**, just type the slash command in Antigravity chat
3. Example usage:
   ```
   You: /step1-epic-analysis
   Agent: [Executes Step 1, creates 1.epic_analysis.md]
   
   You: [Review output, if not satisfied]
   You: /step1-epic-analysis  
   Agent: [Re-runs Step 1 with improvements]
   
   You: [Satisfied] /step2-docs-analysis
   Agent: [Proceeds to Step 2]
   ```

---

## Quick Summary of Each Step

### Step 1: Epic Analysis
- Read Epic/Jira from `0_initial_docs/`
- Output: `1_research/1.epic_analysis.md`
- Contains: Summary, requirements, unclear points

### Step 2: Documentation Analysis  
- Deep dive into provider API docs
- Output: `1_research/2.docs_analysis.md`
- Contains: Auth method, endpoints, payment methods, customer fields

### Step 3: Local Test Page
- Triggers `test_page_generator` skill
- Output: `1_research/3.test_page.html` + `3.local_test_page.md`
- Contains: Functional test page with webhook testing

### Step 4: Access & Field Verification
- Verify credentials, compare field mappings
- Output: `1_research/4.access_and_fields.md`
- Contains: Access status, field comparison table

### Step 5: Compatibility Check
- Check system architecture compatibility
- Output: `1_research/5.compatibility.md`
- Contains: Component compatibility, custom logic needs, risks

### Step 6: Fill Project Stories
- Create technical specifications for all stories
- Output: `1_research/6.project_stories.md`
- Contains: 7 stories (Auth, Create TX, Response, Webhook, Status, Mappings, Errors)

### Step 7: Field Testing
- Test edge cases and field formats
- Output: `1_research/7.field_testing.md`
- Contains: Phone formats, transliteration, amount handling, QA test values

---

## Full Phase 1 Execution

**Command**: `/phase1-full`

Runs all 7 steps in sequence with user confirmation between steps.

**Prerequisites**:
- Integration folder exists in `/integrations/<name>/`
- `0_initial_docs/` contains Epic and provider docs
- `config` file filled with credentials and URLs

**Output**: All 7 files in `1_research/` folder

---

## Important Notes

### ✅ Workflows ARE Working
The webview error **only affects preview**, not functionality. When you type `/phase1-full` or `/step1-epic-analysis` in chat, they work perfectly.

### 📖 To Review Workflow Details
If you need to see the full workflow instructions:
- Use: `cat .agent/workflows/step1-epic-analysis.md` in terminal
- Or: Right-click file → "Open With" → "Text Editor"
- Or: Use this reference document

### 🔄 Iterative Execution  
You can re-run the same step multiple times:
```
/step2-docs-analysis  [first attempt]
/step2-docs-analysis  [refine and improve]  
/step2-docs-analysis  [final version]
/step3-test-page      [move to next step]
```

---

## Viewing Original Workflow Files

**Via Terminal**:
```bash
# View any workflow
cat .agent/workflows/phase1-full.md
cat .agent/workflows/step1-epic-analysis.md

# View all workflows
ls .agent/workflows/
```

**Via Text Editor**:
- Navigate to `.agent/workflows/` in file tree
- Right-click file → "Open With" → "Text Editor"

**AVOID**: Double-clicking workflow files (triggers broken webview)

---

## Next Steps

1. Create new integration from template
2. Fill `config` and `0_initial_docs/`
3. Type `/step1-epic-analysis` in Antigravity chat
4. Review output, iterate if needed
5. Continue through steps 2-7

The workflows are ready to use - just invoke them via slash commands!
