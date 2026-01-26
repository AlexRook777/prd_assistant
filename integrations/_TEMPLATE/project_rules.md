# Integration-Specific Rules

This file is **optional**. Only create it if this integration requires rules that **override** or **supplement** the global rules in `.gemini.md`.

## When to Use This File
- Provider has unusual requirements (e.g., "Must use ISO-8859-1 encoding")
- Need to skip certain standard steps (e.g., "No webhook support, skip webhook testing")
- Temporary exceptions during pilot phase

## Example Overrides

### Custom Encoding
```
This provider requires ISO-8859-1 encoding for all request bodies, not UTF-8.
```

### Skip Steps
```
This integration does not support webhooks. Skip webhook testing in Step 3 and Step 4.
```

### Custom Field Mappings
```
Provider requires "cpf" field instead of "document_id" for Brazil.
Map customer.document → cpf
```

## Hierarchy Reminder
Rules in this file have **highest priority** and will override:
- BetterBro standards in `.gemini.md`
- Master PRD schema
- Provider documentation

**Delete this file** if no custom rules are needed.
