# State Transition Rules

## Status
DRAFT

## Purpose

Defines how VOS System State changes over time.

State transitions must be driven by Decision Artifacts.

Direct state modification is prohibited.

---

# Core Principle

State is derived.

State is not manually edited.

The only valid transition path is:

Venture Artifact
    ↓
Evaluation Artifact
    ↓
Decision Artifact
    ↓
State Transition

---

# State Transition Model

## Transition Inputs

Required:

- Source State
- Decision Artifact
- Supporting Evaluation Artifacts

Optional:

- Additional Evidence
- Validation Results

---

# Transition Rules

## Rule ST-01

Decision: CONTINUE

Effect:

Current state remains active.

Additional validation or execution is required.

Transition:

STATE_A → STATE_A

---

## Rule ST-02

Decision: ADVANCE

Effect:

Progression to the next defined state.

Transition:

STATE_A → STATE_B

Requirements:

- Critical evaluations PASS
- No blocking FAIL conditions

---

## Rule ST-03

Decision: REFRAME

Effect:

Return to an earlier state or redefine venture assumptions.

Transition:

STATE_B → STATE_A

or

STATE_X → REFRAME_REQUIRED

Requirements:

- Critical evaluation FAIL
- Structural inconsistency detected

---

# State Integrity Rules

## SI-01

Every transition must reference a Decision Artifact.

---

## SI-02

Every Decision Artifact must reference Evaluation Artifacts.

---

## SI-03

Every Evaluation Artifact must reference one or more Venture Artifacts.

---

## SI-04

Untraceable transitions are invalid.

---

# Readiness Gates

State advancement requires:

- Evidence
- Evaluation
- Decision

Missing any gate blocks progression.

---

# Governance

State Transition Rules apply to all ventures operating under VOS.

Exceptions require Governance approval.
