---
description: Phase 1 Step 7 - Test edge cases and field handling specifics
---

# Step 7: Field Testing

Test edge cases and specific field handling requirements with the provider's API.

## Working Directory
`<current_integration>/1_research/`

## Output File
`7.field_testing.md`

## Task

Test specific field formats and edge cases to understand provider requirements.

```markdown
# Field Testing

**Integration**: [Provider Name]  
**Date**: [Current Date]

## 1. International Phone Format

### Test Cases
| Test Input | Format | Expected Result | Actual Result | Status |
|------------|--------|----------------|---------------|--------|
| `+593991234567` | E.164 | Accepted | ✅ Accepted | ✅ Pass |
| `593991234567` | No plus | ? | ❌ Rejected | ⚠️ Must use E.164 |
| `0991234567` | Local | ? | ❌ Rejected | ⚠️ Must use E.164 |

### Conclusion
- **Required Format**: E.164 with `+` prefix
- **Transformation Needed**: Yes, prepend country code if missing

---

## 2. Document ID Format

### Test Cases
| Test Input | Format | Expected Result | Actual Result | Status |
|------------|--------|----------------|---------------|--------|
| `1234567890` | Numeric | Accepted | ✅ Accepted | ✅ Pass |
| `ABC-123-456` | Alphanumeric with dashes | ? | ❌ Rejected | ⚠️ Letters not allowed |
| `12345` | Short | ? | ❌ Rejected | ⚠️ Min 10 digits |

### Conclusion
- **Required Format**: Numeric only, 10 digits minimum
- **Transformation Needed**: Strip non-numeric characters

---

## 3. Name Transliteration (Cyrillic/Special Characters)

### Test Cases
| Test Input | Character Set | Expected Result | Actual Result | Status |
|------------|---------------|----------------|---------------|--------|
| `John Doe` | ASCII | Accepted | ✅ Accepted | ✅ Pass |
| `José García` | Spanish accents | ? | ✅ Accepted | ✅ Pass |
| `Иван Петров` | Cyrillic | ? | ❌ Rejected | ⚠️ ASCII only |

### Conclusion
- **Character Set**: ASCII only, no Cyrillic
- **Transformation Needed**: Yes, transliterate Cyrillic → Latin

**Transliteration Map**:
```
А→A, Б→B, В→V, Г→G, Д→D, Е→E, Ё→E, Ж→ZH, З→Z, И→I, Й→Y,
К→K, Л→L, М→M, Н→N, О→O, П→P, Р→R, С→S, Т→T, У→U, Ф→F,
Х→KH, Ц→TS, Ч→CH, Ш→SH, Щ→SCH, Ъ→, Ы→Y, Ь→, Э→E, Ю→YU, Я→YA
```

---

## 4. Amount Handling

### Test Cases
| Test Input | Format | Expected Result | Actual Result | Status |
|------------|--------|----------------|---------------|--------|
| `10.00` | Decimal | ? | ❌ Rejected | ⚠️ Integer required |
| `1000` | Integer (cents) | Accepted | ✅ Accepted | ✅ Pass |
| `10` | Integer (dollars) | ? | ✅ Accepted as $0.10 | ⚠️ Ambiguous |

### Conclusion
- **Required Format**: Integer in cents (multiply by 100)
- **Example**: $10.00 → `1000`
- **Transformation Needed**: Yes, convert dollars to cents

---

## 5. Email Validation

### Test Cases
| Test Input | Format | Expected Result | Actual Result | Status |
|------------|--------|----------------|---------------|--------|
| `user@example.com` | Standard | Accepted | ✅ Accepted | ✅ Pass |
| `user+tag@example.com` | Plus addressing | ? | ✅ Accepted | ✅ Pass |
| `user@subdomain.example.com` | Subdomain | ? | ✅ Accepted | ✅ Pass |
| `invalid.email` | No @ sign | ? | ❌ Rejected | ✅ Pass |

### Conclusion
- **Validation**: Standard RFC 5322
- **Special Features**: Plus addressing supported

---

## 6. Currency Code

### Test Cases
| Test Input | Format | Expected Result | Actual Result | Status |
|------------|--------|----------------|---------------|--------|
| `USD` | ISO 4217 | Accepted | ✅ Accepted | ✅ Pass |
| `usd` | Lowercase | ? | ❌ Rejected | ⚠️ Uppercase required |
| `$` | Symbol | ? | ❌ Rejected | ⚠️ ISO code required |

### Conclusion
- **Required Format**: ISO 4217, uppercase
- **Supported**: [USD, EUR, etc.]

---

## 7. QA Tester Specifics

### Special Test Values from QA
| Field | Test Value | Purpose | Result |
|-------|------------|---------|--------|
| `email` | `test.success@provider.com` | Force success | ✅ Works |
| `email` | `test.fail@provider.com` | Force failure | ✅ Works |
| `amount` | `1` | Min amount test | ❌ Rejected (min $1.00) |
| `amount` | `9999999` | Max amount test | ❌ Rejected (max $10,000) |

### Amount Limits
- **Minimum**: $1.00 (100 cents)
- **Maximum**: $10,000.00 (1000000 cents)

---

## Summary of Transformations Required

| Field | Transformation | Implementation |
|-------|----------------|----------------|
| `phone` | Add country code if missing | Prepend `+593` for Ecuador |
| `document_id` | Strip non-numeric | Regex: `[^0-9]` → `` |
| `name` | Transliterate Cyrillic | Use transliteration map |
| `amount` | Convert to cents | Multiply by 100 |
| `currency` | Uppercase | `.toUpperCase()` |

---

## Next Steps
- [ ] Phase 1 Research Complete
- [ ] Proceed to Phase 2 Development
```

## Success Criteria
- All field formats tested and documented
- Transformations identified and specified
- Edge cases handled
- QA test values documented

## User Confirmation
"Field Testing complete. Review `7.field_testing.md`. This completes Phase 1 Research. Ready to move to Development?"



