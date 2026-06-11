# Decision Artifact Model

## Status
DRAFT

## Purpose

Defines how decisions are represented inside VOS.

Decision Artifacts convert Evaluation Artifacts into explicit venture progression actions.

---

# Decision Flow

Venture Artifact
    ↓
Evaluation Artifact
    ↓
Decision Artifact
    ↓
State Update

---

# Supported Decisions

## CONTINUE

Meaning:

Current direction remains valid.

Additional evidence is required before progression.

---

## ADVANCE

Meaning:

Evaluation results support movement to the next stage.

---

## REFRAME

Meaning:

Current assumptions, problem framing, solution framing, or execution approach are insufficient.

A structural revision is required.

---

# Decision Artifact Structure

## Metadata

- Decision ID
- Decision Date
- Evaluator

## Source Evaluations

List of Evaluation Artifacts used.

## Decision

- CONTINUE
- ADVANCE
- REFRAME

## Rationale

Summary of reasoning derived from evaluations.

## Evidence Summary

Supporting evidence references.

## Confidence

- LOW
- MEDIUM
- HIGH

## State Impact

Expected effect on venture state.

---

# Decision Rules

## ADVANCE

Conditions:

- Critical evaluations PASS
- No blocking FAIL conditions

---

## CONTINUE

Conditions:

- Partial validation
- Missing evidence
- Significant uncertainty remains

---

## REFRAME

Conditions:

- Critical evaluation FAIL
- Structural inconsistency detected
- Validation contradicts core assumptions

---

# Governance

All state transitions must reference a Decision Artifact.

Decisions without supporting Evaluation Artifacts are invalid.
