# Design Principles — Venture Playbook OS

## 1. Purpose

These principles define the structural constraints of the Venture Playbook OS.

They are not guidelines.
They are execution rules.

All stages, templates, and AI agents must comply with them without exception.

---

## 2. System Design Philosophy

The system is designed as:

> A constraint-driven execution system for venture creation under uncertainty.

It prioritizes structure over creativity, and validation over intuition.

---

## 3. Core Principles

### 3.1 Clarity over completeness

If a concept cannot be expressed clearly, it is not ready for inclusion.

Ambiguity is treated as a failure state, not a natural condition.

---

### 3.2 Evidence over opinion

No decision is valid without one of the following:

- Empirical evidence
- Explicit assumption labeling
- Documented uncertainty

---

### 3.3 Stage boundary integrity

Each stage must operate independently with:

- Defined inputs
- Defined outputs
- Explicit exit criteria

Cross-stage reasoning is prohibited during execution.

---

### 3.4 Separation of concerns

The system strictly separates:

- Lifecycle stages (execution flow)
- Capabilities (cross-cutting functions)
- Governance (system rules)

No overlap is allowed.

---

### 3.5 AI determinism principle

AI agents operating in this system must:

- Follow stage context strictly
- Avoid inference beyond provided data
- Explicitly label assumptions
- Never skip validation requirements

---

### 3.6 Artifact minimalism

Only artifacts that support a decision or validation are allowed.

Documentation for its own sake is considered system debt.

---

### 3.7 Traceability requirement

Every output must be traceable to:

- A stage input
- An experiment
- An assumption
- Or external evidence

Untraceable outputs are invalid.

---

### 3.8 No premature optimization

The system must prioritize:

- Validation before scaling
- Learning before architecture
- Evidence before design complexity

---

### 3.9 Controlled complexity growth

System complexity must increase only when:

- A new validated requirement emerges
- A structural limitation is discovered
- A capability gap is proven

Not based on theoretical design preferences.

---

### 3.10 Reversibility awareness

All decisions must be classified as:

- Reversible (can be changed cheaply)
- Semi-reversible (moderate cost)
- Irreversible (requires ADR)

Irreversible decisions require formal documentation.

---

## 4. AI System Constraints

AI agents must adhere to the following constraints:

### MUST
- Operate within a single stage context
- Distinguish assumption vs fact
- Request missing inputs before proceeding
- Maintain structural consistency

### MUST NOT
- Jump across stages
- Merge multiple stages logic
- Assume validation has occurred
- Generate undocumented decisions

---

## 5. Failure Modes

The system explicitly rejects the following behaviors:

### 5.1 Stage leakage
Mixing logic across lifecycle stages.

### 5.2 False certainty
Treating assumptions as validated facts.

### 5.3 Artifact inflation
Creating outputs without decision necessity.

### 5.4 Capability confusion
Using Sales/Marketing/Analytics as stages.

### 5.5 Hidden decision making
Making architectural decisions without ADR.

---

## 6. System Integrity Rule

If a principle is violated:

> The output is considered structurally invalid, regardless of correctness.

---

## 7. Design Intent Summary

This system is designed to:

- Reduce ambiguity in venture creation
- Enforce structured reasoning under uncertainty
- Enable AI-native execution of venture building
- Prevent uncontrolled complexity growth
- Create repeatable venture outcomes

---

## 8. Final Principle

> A system without enforceable constraints is not an operating system — it is documentation.