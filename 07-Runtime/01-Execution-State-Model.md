# Execution State Model

## 1. Purpose
Defines the lifecycle state machine of a venture within the Venture Operating System (VOS), describing how a system transitions from idea to execution readiness and beyond.

This model provides a consistent interpretation of "where the system is" at any point in time.

---

## 2. Core Principle
A venture is always in exactly one **execution state** at any given time.

State is not inferred informally; it is derived from validated artifacts across upstream layers.

---

## 3. State Set

### 3.1 Conceptual States

- **IDEA**
  - No validated problem or structure exists

- **PROBLEM_DEFINED**
  - Problem layer is complete and validated

- **PRODUCT_HYPOTHESIS_DEFINED**
  - Product layer exists and is aligned with problem

- **DOMAIN_MODEL_DEFINED**
  - Domain structure is explicitly modeled

- **ARCHITECTURE_DEFINED**
  - System architecture is complete and validated

- **READY_FOR_EXECUTION**
  - Execution layer can begin without structural gaps

- **IN_EXECUTION**
  - Execution blocks are actively being processed

- **READY_FOR_MVP**
  - Execution has produced MVP-ready structure

- **IN_MVP**
  - MVP stage is active and being validated in real conditions

- **POST_MVP_ITERATION**
  - Feedback loop active and system is iterating

---

## 4. State Transition Rules

Transitions MUST follow strict dependency order:

IDEA → PROBLEM_DEFINED → PRODUCT_HYPOTHESIS_DEFINED → DOMAIN_MODEL_DEFINED → ARCHITECTURE_DEFINED → READY_FOR_EXECUTION → IN_EXECUTION → READY_FOR_MVP → IN_MVP → POST_MVP_ITERATION

No backward or skipping transitions are valid unless explicitly revalidating upstream artifacts.

---

## 5. State Derivation Rule
State is derived from:

- Problem validation status
- Product hypothesis completeness
- Domain model completeness
- Architecture validation status
- Execution readiness criteria

State cannot be manually set without artifact evidence.

---

## 6. Invalid States
The system must never be in:

- MIXED_STATE (multiple active states)
- UNDEFINED_STATE (no traceable artifacts)
- SKIPPED_STATE (missing intermediate validation layers)

---

## 7. Role in VOS
This layer is the **temporal backbone** of the Venture Operating System.

It connects static structure (architecture) to dynamic progression (execution and MVP evolution).