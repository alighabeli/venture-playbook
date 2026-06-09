# Document Standards — Venture Playbook OS

## 1. Purpose

This document defines the mandatory standards for all documents within the Venture Playbook OS.

The objective is to ensure:

- Consistency
- Traceability
- AI readability
- Human readability
- Structural integrity

All documents must comply with these standards.

---

## 2. Document Classification

Documents belong to one of the following categories:

### Governance

System-level rules and controls.

Examples:

- Vision
- Design Principles
- Versioning Strategy

---

### Stage

Documents defining lifecycle execution.

Examples:

- Problem
- Validation
- Product

---

### Template

Reusable artifact definitions.

Examples:

- PRD Template
- Interview Template

---

### ADR

Architectural decision records.

Examples:

- Stage Taxonomy
- Complexity Model

---

### AI System

AI behavior and execution specifications.

Examples:

- Agent Contracts
- Handoff Protocols

---

## 3. Mandatory Document Header

All documents must begin with the following metadata block.

```yaml
Title:
Type:
Version:
Status:
Owner:
Created:
Last Updated:
Purpose:
Dependencies:
Outputs:
4. Naming Standards
Folders

Use:

NN-Name

Examples:

01-Vision
02-Problem
03-Validation
Files

Use:

NN-Document-Name.md

Examples:

00-Vision.md
03-Versioning-Strategy.md
05-Governance-Model.md
5. Writing Standards

Documents must be:

Explicit
Concise
Actionable
Unambiguous

Avoid:

marketing language
motivational language
vague recommendations
6. Traceability Standard

Every document must clearly identify:

Inputs

What it depends on.

Outputs

What it produces.

Dependencies

Which documents influence it.

7. Decision Documentation Rule

Any irreversible decision must be documented through an ADR.

No architectural decision may exist only inside discussion text.

8. Assumption Handling Rule

Assumptions must always be explicitly labeled.

Never present assumptions as facts.

Recommended notation:

ASSUMPTION:
...
9. Evidence Handling Rule

Evidence must identify:

source
date
context

Evidence without source attribution is considered weak evidence.

10. AI Readability Rule

Documents should be structured so that AI agents can reliably extract:

objectives
constraints
inputs
outputs
decisions

Avoid hidden context.

Avoid implied requirements.

11. Document Lifecycle Status

Every document must have one status:

Draft

Work in progress.

Review

Under evaluation.

Approved

Accepted as active.

Deprecated

No longer active but retained for history.

12. Final Principle

Documents exist to support decisions and execution.

A document without operational value is system debt.