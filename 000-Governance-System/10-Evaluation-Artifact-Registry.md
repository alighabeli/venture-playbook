# Evaluation Artifact Registry

## Status
DRAFT

## Purpose

Defines the official Evaluation Artifact types supported by VOS.

Evaluation Artifacts assess the quality, completeness, readiness, and validity of Venture Artifacts.

They are inputs to Decision Artifacts and State Transitions.

---

# Evaluation Artifact Structure

All Evaluation Artifacts must contain:

## Metadata

- Artifact ID
- Artifact Type
- Source Artifact(s)
- Evaluation Date
- Evaluator

## Assessment Dimensions

- Criterion
- Result
- Evidence
- Confidence

## Outcome

- PASS
- PARTIAL
- FAIL
- UNKNOWN

## Progression Recommendation

- CONTINUE
- ADVANCE
- REFRAME

---

# Registered Evaluation Artifacts

## Problem Assessment

Evaluates:

- Clarity
- Severity
- Evidence Quality
- Segment Alignment
- Testability

---

## Hypothesis Assessment

Evaluates:

- Problem-Solution Fit
- Assumption Quality
- Falsifiability
- Validation Coverage

---

## Domain Assessment

Evaluates:

- Actor Completeness
- Relationship Completeness
- Value Flow Consistency
- Boundary Clarity

---

## Validation Assessment

Evaluates:

- Assumption Coverage
- Experiment Design
- Signal Quality
- Decision Readiness

---

## MVP Readiness Assessment

Evaluates:

- Scope Clarity
- Testability
- Dependency Completeness
- Execution Readiness

---

## GTM Assessment

Evaluates:

- Channel Logic
- Acquisition Assumptions
- Activation Design
- Retention Logic

---

## Execution Readiness Assessment

Evaluates:

- Execution Units
- Dependencies
- Success Metrics
- Failure Signals

---

## PMF Readiness Assessment

Evaluates:

- Retention Signals
- Unit Economics
- Customer Pull
- Scaling Readiness

---

# Confidence Model

## Evidence State

- CONFIRMED
- INFERRED
- UNCERTAIN

## Confidence Level

- LOW
- MEDIUM
- HIGH

---

# Evaluation → Decision Mapping

PASS → ADVANCE

PARTIAL → CONTINUE

FAIL → REFRAME

UNKNOWN → CONTINUE

---

# Registry Governance

New Evaluation Artifact types must be added through Governance review.

Changes to assessment dimensions require version updates.
