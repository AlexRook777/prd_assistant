# PRD-First Development Principles

PRD-First Development is the core methodology of the PRD Assistant. It ensures that requirements are fully defined, validated, and documented before any implementation begins. This "Source of Truth" approach is critical for maintaining consistency in agentic workflows.

## Core Principles

1. **PRD as the Source of Truth**: The PRD is not just a document; it is the definitive specification for the integration. Any discrepancy between code and PRD must be resolved in favor of the PRD.
2. **Agent Alignment**: Agents must consume the PRD to understand the context, constraints, and business logic before generating code or performing mappings.
3. **Architecture Before Implementation**: All technical components (endpoints, field mappings, state flows) must be architected in the PRD phase.
4. **Validation-Driven**: Every integration must be validated against the PRD structure defined in `master_prd.yaml`.
5. **Living Document**: The PRD is updated as new edge cases are discovered during the integration process, ensuring the documentation never falls behind the implementation.

## Workflow Description

The workflow follows a strict sequence:
1. **Discovery**: Analyze provider documentation.
2. **Drafting**: Create the initial PRD using the global template.
3. **Refinement**: Apply local rules and BetterBro standards to the PRD.
4. **Finalization**: Approve the PRD as the immutable specification for the implementation phase.
