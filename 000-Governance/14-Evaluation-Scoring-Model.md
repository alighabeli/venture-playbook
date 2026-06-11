# Evaluation Scoring Model

## Status
DRAFT

## Purpose

Defines the scoring rules used by Evaluation Artifacts.

The objective is to improve consistency, repeatability, and traceability across evaluations.

---

# Standard Outcome Values

- PASS
- PARTIAL
- FAIL
- UNKNOWN

---

# Standard Confidence Values

- HIGH
- MEDIUM
- LOW

---

# Problem Assessment Scoring

## Clarity

PASS
- Problem is specific, bounded, and operationally understandable.

PARTIAL
- Problem exists but boundaries are unclear.

FAIL
- Problem cannot be clearly identified.

UNKNOWN
- Insufficient information.

---

## Evidence Quality

PASS
- Direct evidence exists.
- Customer interviews.
- Transactions.
- Behavioral data.
- Validated research.

PARTIAL
- Indirect evidence only.

FAIL
- No supporting evidence.

UNKNOWN
- Evidence unavailable.

---

## Segment Alignment

PASS
- Explicit target segment defined.

PARTIAL
- Broad segment only.

FAIL
- No segment definition.

UNKNOWN
- Insufficient information.

---

## Testability

PASS
- Validation path exists.

PARTIAL
- Validation path partially defined.

FAIL
- Cannot be practically tested.

UNKNOWN
- Insufficient information.

---

# Aggregation Rules

## PASS

- No FAIL
- No UNKNOWN
- PASS criteria >= 75%

## PARTIAL

- At least one PASS
- No critical FAIL

## FAIL

- Any critical criterion FAIL

## UNKNOWN

- Insufficient evidence to produce evaluation.

---

# Decision Mapping

PASS -> ADVANCE

PARTIAL -> CONTINUE

FAIL -> REFRAME

UNKNOWN -> CONTINUE

---

# Governance Rule

Evaluation outcomes must be derived from scoring criteria.

Evaluator discretion may not override scoring results.
