# Versioning Strategy — Venture Playbook OS

## 1. Purpose

This document defines how the Venture Playbook OS evolves over time while maintaining structural integrity, traceability, and AI-executability.

Versioning is not documentation control.
It is system control.

---

## 2. Versioning Layers

The system has three independent versioning layers:

### 2.1 System Version (Global)

Applies to the entire Playbook OS.

Example:
- v1.0 → initial architecture
- v1.1 → minor structural refinements
- v2.0 → meta-model change or taxonomy shift

---

### 2.2 Stage Version (Local)

Each Stage evolves independently.

Example:
- Validation v1.0
- Product v1.3

Stage versions must remain compatible with system version.

---

### 2.3 Template Version (Artifact Level)

Reusable templates evolve independently of stages.

Example:
- PRD Template v2
- Interview Guide v4

---

## 3. Versioning Rules

### Rule 1 — No silent changes

Any structural change must increment version.

---

### Rule 2 — ADR requirement for major changes

Any change that affects:

- Stage structure
- Meta-model
- AI contracts
- governance rules

requires an ADR before version bump.

---

### Rule 3 — Backward awareness

New versions must explicitly consider:

- compatibility impact
- migration implications
- deprecated behaviors

---

### Rule 4 — AI awareness constraint

AI agents must always:

- detect current system version
- adapt outputs accordingly
- never assume latest version without explicit context

---

## 4. Change Classification

### Minor change (patch)
- formatting
- clarification
- small rule refinement

→ v1.0 → v1.0.1

---

### Medium change (feature-level)
- adding constraint
- refining stage behavior

→ v1.0 → v1.1

---

### Major change (architecture-level)
- meta-model changes
- stage taxonomy changes

→ v1.x → v2.0

---

## 5. System Stability Principle

The system prioritizes:

> Stability over frequent evolution

Changes must be justified by:

- real execution friction
- proven limitation
- validated need

Not design preference.

---

## 6. AI Version Enforcement Rule

AI agents must:

- include system version in reasoning context
- reject ambiguous version state
- require explicit version reference in critical decisions

---

## 7. Final Principle

Versioning is not tracking change.

It is controlling system identity over time.