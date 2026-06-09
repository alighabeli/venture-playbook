# Anti-Patterns — Venture Playbook OS

## 1. Purpose

This document defines common failure patterns in venture creation within the Venture Playbook OS.

Anti-patterns are behaviors that appear productive but systematically degrade decision quality, validation integrity, or execution reliability.

---

## 2. Principle of Failure Awareness

Most system failures are not caused by lack of effort, but by repeated structural anti-patterns.

Identifying them early is critical for system stability.

---

## 3. Anti-Pattern: Premature Solutioning

### Description

Jumping to solutions before validating the problem.

### Effect

- wasted execution effort
- invalid product direction
- distorted validation signals

### Rule

Problem must be validated before solution design.

---

## 4. Anti-Pattern: Hidden Assumptions

### Description

Assumptions that are not explicitly declared.

### Effect

- false confidence
- invalid decisions
- broken traceability

### Rule

All assumptions must be explicitly labeled.

---

## 5. Anti-Pattern: Stage Skipping

### Description

Skipping stages in the lifecycle (e.g., moving to product without validation).

### Effect

- missing evidence
- unstable architecture
- high rework cost

### Rule

All stages are mandatory unless explicitly justified.

---

## 6. Anti-Pattern: Over-Engineering

### Description

Introducing unnecessary structure or complexity.

### Effect

- slow execution
- cognitive overload
- reduced adaptability

### Rule

Complexity must be justified by necessity.

---

## 7. Anti-Pattern: Under-Validation

### Description

Insufficient testing of assumptions before execution.

### Effect

- high failure rate
- invalid market signals
- poor product-market fit

### Rule

Validation depth must match complexity level.

---

## 8. Anti-Pattern: AI Over-Autonomy

### Description

Allowing AI to make implicit decisions or fill missing context.

### Effect

- loss of human control
- hidden assumptions
- non-traceable reasoning

### Rule

AI must remain bounded and explicit.

---

## 9. Anti-Pattern: Decision Without Traceability

### Description

Making decisions without documenting inputs, reasoning, and alternatives.

### Effect

- non-repeatable outcomes
- inability to audit decisions
- system drift

### Rule

All decisions must be traceable.

---

## 10. Anti-Pattern: Uncontrolled Complexity Growth

### Description

Complexity increasing without governance or justification.

### Effect

- system fragility
- reduced execution speed
- governance breakdown

### Rule

All complexity increases must be explicit and reviewed.

---

## 11. Anti-Pattern: Opinion-Driven Validation

### Description

Using opinions instead of evidence as validation input.

### Effect

- false positives
- misleading insights
- invalid product direction

### Rule

Only behavioral or experimental evidence is valid.

---

## 12. Anti-Pattern: Context Loss Between Stages

### Description

Losing critical information when transitioning between stages.

### Effect

- repeated work
- inconsistent decisions
- broken traceability

### Rule

Stage transitions must preserve structured context.

---

## 13. Anti-Pattern: Non-Atomic Execution

### Description

Executing large undefined tasks without decomposition.

### Effect

- low traceability
- unclear outputs
- high failure risk

### Rule

All execution must be decomposed into atomic tasks.

---

## 14. Anti-Pattern: False Completion

### Description

Marking work as complete without satisfying exit criteria.

### Effect

- hidden defects
- unstable downstream stages
- incorrect confidence levels

### Rule

Completion requires validated exit criteria.

---

## 15. Final Principle

Anti-patterns are not exceptions.

They are predictable system behaviors that must be actively prevented through governance and discipline.