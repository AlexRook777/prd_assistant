# **Technical Case: PRD Assistant — AI-Augmented Payment Integration Pipeline**

**Agentic Spec-Driven Product Development System**

---

## **Table of Contents**

1. [Executive Summary](#1-executive-summary)
2. [The Business Challenge](#2-the-business-challenge)
3. [Results](#3-results)
4. [The Solution: 7-Step Agentic Pipeline](#4-the-solution-7-step-agentic-pipeline)
   - 4.1. [Two-Layer Documentation System (SIP Methodology)](#41-two-layer-documentation-system-sip-methodology)
   - 4.2. [The 7-Step Pipeline](#42-the-7-step-pipeline)
   - 4.3. [Skills — Context-Triggered Automation](#43-skills--context-triggered-automation)
   - 4.4. [Jira Integration & Automation](#44-jira-integration--automation)
   - 4.5. [Local Testing Infrastructure](#45-local-testing-infrastructure)
5. [Key Capabilities & Impact](#5-key-capabilities--impact)
6. [Technology Stack](#6-technology-stack)
7. [System Architecture Flow](#7-system-architecture-flow)
8. [Workflow Example](#8-workflow-example)
   - [Input: Jira Epic (Business Request)](#input-jira-epic-business-request)
   - [Output: Step 1 — Epic Analysis](#output-step-1--epic-analysis-1epic_analysismd)
   - [Output: Step 7 — Contract Spec](#output-step-7--contract-spec-7contract_specyaml)
9. [The Human + AI Loop](#9-the-human--ai-loop)

---

## **1. Executive Summary**

**PRD Assistant** is an agentic AI pipeline that transforms the payment provider integration process from a manual, weeks-long bottleneck into a structured, validation-driven workflow that delivers developer-ready specifications in **2 days instead of 1–2 weeks**.

Moving beyond simple document generation, the system implements a **Spec-Integrated PRD (SIP)** methodology — a two-layer approach where human-readable analysis (PRD) is synthesized into machine-executable contracts (OpenAPI 3.1 YAML). The core innovation is **Active Verification**: the agent doesn't just *read* API documentation — it builds working prototypes, tests them against live sandboxes, and debugs its own code until a transaction succeeds.

---

## **2. The Business Challenge**

The client's integration pipeline faced critical scalability constraints that directly limited revenue growth:

* **Manual Research Bottleneck:** A Business Analyst spent 3–5 days per integration reading through provider API documentation — often outdated, inconsistent, or written in broken English — before producing a first draft of a specification.
* **Specification Ambiguity:** Hand-written PRDs were prone to interpretation errors. Developers frequently discovered undocumented behaviors, incorrect field mappings, or missing edge cases only during QA — weeks after the spec was "complete."
* **Linear Scaling Trap:** The "obvious" solution was hiring more BAs. But onboarding took weeks, ramping up on internal standards took more weeks, and output quality was inconsistent. The company was scaling headcount linearly to solve what was fundamentally a process problem.
* **Revenue Impact:** Each new payment provider integration directly opens a new revenue stream — a new country, currency, or payment method. The speed of integration directly determines how fast profit grows. At 1 integration per week, the pipeline was the single biggest constraint on business growth.

---

## **3. Results**

| Metric | Before | After | Improvement |
| :---- | :---- | :---- | :---- |
| **Spec Creation Time** | 1–2 weeks | 2 days | **7x faster** |
| **Dev/QA Refinement Cycles** | 4–6 rounds | 1–2 rounds | **3–4x reduction** |
| **Integration Throughput** | 1 per week | 5–6 per week | **5–6x increase** |
| **Documentation Errors Caught Pre-Dev** | ~20% | ~90% | **4.5x improvement** |
| **Pipeline as Revenue Bottleneck** | Yes (primary constraint) | No (unblocked) | **Eliminated** |

---

## **4. The Solution: 7-Step Agentic Pipeline**

I architected **PRD Assistant** as a deterministic, re-runnable pipeline of 7 discrete steps, designed for **Human + AI iterative collaboration**. Each step produces a versioned artifact, can be re-run independently, and is validated before proceeding.

### **4.1. Two-Layer Documentation System (SIP Methodology)**

The core architectural decision was separating documentation into two distinct layers:

* **Layer 1 — Human-Readable PRD (Steps 1–6):** Markdown documents covering discovery, analysis, compatibility checks, and user stories. Audience: Product Managers, Stakeholders, Developers. Answers *"Why are we building this?"* and *"How does the provider work?"*
* **Layer 2 — Machine-Executable Contract (Step 7):** A strictly-typed OpenAPI 3.1 YAML specification with complete request/response schemas, field-level mappings, and transformation rules. Audience: Code agents, linters, test runners. Answers *"How exactly do we build this?"* with mathematical precision.

This separation ensures the PRD provides *context* (nuance, edge cases, business logic) while the Spec provides a *contract* (types, fields, endpoints) — enabling downstream code agents to generate 80%+ of the initial implementation logic.

### **4.2. The 7-Step Pipeline**

#### **Phase 1: Research & Discovery**

**Step 1 — Epic Analysis.** The system pulls the Jira ticket directly via the Atlassian API — full description, comments, attachments — with zero copy-paste and zero information loss. The agent analyzes the business request, flags ambiguities, and generates a structured list of clarification questions for the Product Owner. In one case, it caught a scope discrepancy (Peru vs. Ecuador) that would have cost days of rework.

**Step 2 — Documentation Deep-Dive.** The agent doesn't just *summarize* API docs. It cross-references documented behavior against endpoint specifications, identifies inconsistencies, and produces a structured analysis covering authentication methods, available payment methods, webhook formats, and regional restrictions.

#### **Phase 2: Active Verification — "Trust, but Verify"**

This phase is the breakthrough innovation of the system.

**Step 3 — Test Page Generator.** The agent builds a **fully functional HTML/JS payment page** from scratch — not a mockup, but a real page that authenticates via OAuth, creates transactions, captures webhooks, and logs every request/response. The page connects through a local CORS proxy server and includes a live webhook viewer.

**Step 4 — Autonomous Testing.** The agent opens its own test page in a headless browser, runs transactions against the provider's live sandbox, and **debugs its own code** iteratively until a transaction succeeds. This is the "Active Verification" step — after it completes, we don't *think* the documentation is correct; we've *proven* it with a working prototype. This single capability eliminated the majority of bugs that previously surfaced weeks later in QA.

#### **Phase 3: Specification & Handoff**

**Step 5 — Architecture Compatibility Check.** Every provider field is mapped against the internal standard schema. Transformation rules are documented (decimal → integer amounts, country code conversions, document type mappings). Blocking architectural risks are flagged before any development begins.

**Step 6 — Technical User Stories.** These aren't vague descriptions. Each story includes exact endpoint specifications, request/response schemas with concrete examples, acceptance criteria with specific scenarios, and field-level mapping tables. Stories cover: Authorization, Create Transaction, Response Parsing, Webhook Handling, Status Polling, Final Status Mapping, and Error Mapping.

**Step 7 — OpenAPI 3.1 Contract Specification.** The final deliverable: a machine-executable YAML contract that serves as the **single source of truth** for the implementation agent. It synthesizes all findings from Steps 1–6 into a lintable, validatable specification. Developers don't interpret requirements — they implement a validated contract.

### **4.3. Skills — Context-Triggered Automation**

A key architectural feature is the **Skills** system — modular, context-aware automation units that activate automatically when the pipeline detects a relevant task. Skills encapsulate domain-specific expertise and eliminate repetitive manual work.

* **Test Page Generator Skill:** Auto-triggered during Step 3 or whenever the user mentions "create test page." This skill encapsulates the full knowledge of how to build a provider-specific test page: OAuth token acquisition, transaction payload construction, CORS proxy routing, webhook polling, and request/response logging. It generates a complete, self-contained HTML file (`3.test_page.html`) with embedded JavaScript — ready to open in a browser and execute real transactions against the provider's sandbox.
* **Workflow Orchestration Skills:** Each pipeline step is defined as a standalone Markdown-based workflow file (e.g., `step1-epic-analysis.md`, `step5-compatibility.md`), invoked via slash commands (`/step1-epic-analysis`, `/phase1-full`). This design enables **Jupyter Notebook-style execution** — run any step individually, review the output, iterate until satisfied, or execute an entire phase automatically with the agent confirming between steps.
* **Contextual Rule Injection:** The system automatically loads a hierarchy of rules at every step: global standards (`.gemini.md`), internal architecture constraints, and integration-specific overrides (`project_rules.md`). This ensures every generated artifact is consistent with organizational standards without requiring the PM to manually reference documentation.
* **Skill Composability:** Skills can be chained — for example, the `/phase1-full` workflow sequentially invokes all 7 step-level skills, passing context between them. Each skill reads the artifacts produced by prior steps, ensuring the pipeline accumulates validated knowledge rather than starting from scratch.

### **4.4. Jira Integration & Automation**

A custom integration layer (`jira_fetcher.py`, `jira_parser_custom.py`) connects the pipeline directly to the project management system:

* **Automated Epic Ingestion:** Pulls full ticket descriptions, comments, and attachments via the Atlassian REST API with token-based authentication.
* **Zero-Copy Workflow:** Eliminates the error-prone manual copy-paste of requirements from Jira into analysis documents.
* **Contextual Parsing:** Extracts structured data from free-text Jira descriptions, identifying currencies, countries, payment methods, and integration types.

### **4.5. Local Testing Infrastructure**

A centralized testing server (`serve.py`) provides the infrastructure needed for Active Verification:

* **CORS Proxy:** `POST /proxy` — Routes requests from the browser-based test page to provider APIs, bypassing CORS restrictions.
* **Webhook Ingestion:** `POST /webhook` — Captures and stores provider callback notifications for inspection.
* **Webhook Viewer:** A real-time UI (`webhook_viewer.html`) for visualizing captured webhooks with full payload inspection.
* **API Layer:** `GET/DELETE /api/webhooks` — Programmatic access to captured webhooks for automated test validation.

---

## **5. Key Capabilities & Impact**

| Capability | Business Value |
| :---- | :---- |
| **7x Faster Spec Creation** | Integration specification time reduced from 1–2 weeks to **2 days**, unblocking the revenue pipeline. |
| **Active Verification** | Agent builds and tests working prototypes against live sandboxes, catching documentation errors *before* development starts. |
| **3–4x Fewer Dev/QA Cycles** | Pre-validated, machine-readable contracts eliminate ambiguity, reducing back-and-forth between PO and developers. |
| **5–6x Throughput Increase** | Team can research and spec 5–6 integrations in the time it previously took to complete 1. |
| **Re-runnable Steps** | Each of the 7 steps is independently executable and idempotent — iterate on any step without restarting the pipeline. |
| **Deterministic Handoff** | OpenAPI 3.1 YAML contract serves as an unambiguous, lintable source of truth for code generation agents. |

---

## **6. Technology Stack**

* **Orchestration:** Antigravity (AI Agent IDE with workflow engine)
* **AI Models:** Claude (Primary), Gemini (Secondary reasoning)
* **Pipeline Definition:** Markdown-based workflow files with slash-command triggers
* **Spec Format:** OpenAPI 3.1 YAML with Spectral linting
* **Testing Infrastructure:** Python 3.11+, FastAPI (CORS proxy + webhook server)
* **Jira Integration:** Custom Python scripts via Atlassian REST API
* **Browser Automation:** Headless browser agent for autonomous testing (Step 4)
* **Version Control:** Git (all artifacts are versioned Markdown/YAML)

---

## **7. System Architecture Flow**

1. **Ingestion (Jira API):** The pipeline begins when the user triggers `/create-new-integration`. The system scaffolds a standardized folder structure, and the Jira fetcher pulls the full Epic description, comments, and attachments via the Atlassian REST API. The raw business request is stored as an immutable input artifact in `0_initial_docs_and_config/`.

2. **Research Phase (Steps 1–2):** The AI agent processes the Epic and provider documentation in sequence. Each step produces a versioned Markdown artifact in `1_result/`. The agent cross-references the business request against the provider's API documentation, identifying gaps, ambiguities, and risks. The human reviews each artifact and can re-run any step with additional guidance.

3. **Active Verification Phase (Steps 3–4):** The agent generates a fully functional HTML test page that connects to the provider's sandbox environment through the local CORS proxy. It then opens the page in a headless browser, executes a real transaction, inspects the webhook response, and iteratively debugs any failures. The result is a **proven** understanding of the provider's actual behavior — not just what the docs claim.

4. **Specification Phase (Steps 5–7):** The agent synthesizes all validated findings into three artifacts: an architecture compatibility report, detailed technical user stories, and a final OpenAPI 3.1 YAML contract. The contract is linted with Spectral to ensure completeness and correctness. All artifacts are packaged into a handoff ZIP for the implementation team.

5. **Human-in-the-Loop Validation:** At every step, the human PM reviews, challenges assumptions, re-runs steps, and refines. The agent catches things the human would miss at 4pm after their third integration of the day. The human catches strategic nuances the agent can't evaluate. This is structured collaboration, not replacement.

---

## **8. Workflow Example**

### **Input: Jira Epic (Business Request)**

```
Project: IN-1137
Title: SmartFastPay Ecuador USD Payin HPP
Type: Epic

Description:
- Provider: SmartFastPay
- Country: Ecuador
- Currency: USD
- Flow: Hosted Payment Page (HPP)
- Payment Methods: Bank Transfer, Credit Card
- Documentation: https://docs.smartfastpay.com/api/v2
- Sandbox credentials provided in attachments
```

### **Output: Step 1 — Epic Analysis** (`1.epic_analysis.md`)

```markdown
# Epic Analysis: SmartFastPay Ecuador USD Payin HPP

## Summary
Integration of SmartFastPay as a payment provider for Ecuador,
supporting USD transactions via Hosted Payment Page (HPP) redirect flow.

## Scope Confirmation
- **Provider:** SmartFastPay
- **Country:** Ecuador (EC)
- **Currency:** USD
- **Flow Type:** HPP (Redirect)
- **Direction:** Payin (Deposit)

## Identified Ambiguities
1. ⚠️ Epic mentions "Ecuador" but provider docs reference
   both Ecuador AND Peru endpoints. **Clarification needed from PO.**
2. The documentation lists "Bank Transfer" but doesn't specify
   whether this is ACH, wire, or local bank network.
3. No mention of minimum/maximum transaction amounts.

## Questions for Product Owner
1. Is this integration Ecuador-only, or should Peru be included?
2. What is the expected transaction volume (for rate negotiation)?
3. Are there any specific bank transfer methods to prioritize?
```

### **Output: Step 7 — Contract Spec** (`7.contract_spec.yaml`)

```yaml
openapi: "3.1.0"
info:
  title: SmartFastPay Ecuador USD Payin HPP
  version: "1.0.0"
  description: |
    Machine-executable contract for SmartFastPay integration.
    Generated by PRD Assistant pipeline.

paths:
  /api/v2/transactions:
    post:
      operationId: createTransaction
      summary: Create a new payment transaction
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTransactionRequest'
      responses:
        '200':
          description: Transaction created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateTransactionResponse'

  /api/v2/transactions/{transactionId}/status:
    get:
      operationId: checkTransactionStatus
      summary: Poll transaction status
      parameters:
        - name: transactionId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Current transaction status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TransactionStatusResponse'

components:
  schemas:
    CreateTransactionRequest:
      type: object
      required:
        - amount
        - currency
        - document_type
        - document_number
        - customer_email
      properties:
        amount:
          type: integer
          description: "Amount in cents (e.g., 1000 = $10.00)"
          x-mapping: "internal.amount * 100"
        currency:
          type: string
          enum: ["USD"]
        document_type:
          type: string
          enum: ["CC", "CI", "PP"]
          description: |
            Document type code.
            ⚠️ VALIDATED: Docs claim "CI" but live API requires "CC"
            for Cédula de Ciudadanía.
          x-mapping: "map(internal.document_type)"
        document_number:
          type: string
          maxLength: 20
        customer_email:
          type: string
          format: email

    CreateTransactionResponse:
      type: object
      properties:
        transaction_id:
          type: string
        redirect_url:
          type: string
          format: uri
          description: "URL to redirect customer to hosted payment page"
        status:
          type: string
          enum: ["PENDING", "CREATED"]

    TransactionStatusResponse:
      type: object
      properties:
        transaction_id:
          type: string
        status:
          type: string
          enum: ["PENDING", "COMPLETED", "FAILED", "EXPIRED"]
          x-status-mapping:
            COMPLETED: "internal.SUCCESS"
            FAILED: "internal.DECLINED"
            EXPIRED: "internal.EXPIRED"
            PENDING: "internal.PENDING"

    WebhookPayload:
      type: object
      description: "Callback notification from SmartFastPay"
      properties:
        event_type:
          type: string
          enum: ["transaction.completed", "transaction.failed"]
        transaction_id:
          type: string
        status:
          type: string
        signature:
          type: string
          description: "HMAC-SHA256 signature for webhook verification"
```

---

## **9. The Human + AI Loop**

Every step in the pipeline is designed for **human-in-the-loop iteration**:

| Phase | Agent Contribution | Human Contribution |
| :---- | :---- | :---- |
| **Research** | Crawls docs, tests APIs, structures findings | Validates strategic fit, compliance, edge cases |
| **Prototyping** | Builds working test pages, debugs autonomously | Verifies business logic, confirms happy paths |
| **Specification** | Drafts OpenAPI contracts, maps fields | Refines architectural constraints, approves final spec |
| **Iteration** | Re-runs any step on demand, preserves context | Challenges assumptions, catches what the agent misses |

The PM role isn't diminished — it's **elevated**. Instead of spending days on repetitive research, the PM focuses on decisions, validation, and quality control. The agent handles the grunt work; the human handles the judgment.

