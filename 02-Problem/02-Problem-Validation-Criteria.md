# Problem Validation Criteria

## 1. Purpose
This file defines the criteria used to determine whether a defined problem is valid within the Venture Operating System (VOS).

It ensures that problems are not assumed, but explicitly validated before progression to downstream layers.

---

## 2. Valid Problem Criteria
A problem is considered valid only if all the following conditions are met:

### 2.1 Independence from Solution
- The problem can be described without referencing any solution or product
- No implicit implementation is embedded in the statement

### 2.2 Observability
- There exist observable signals (symptoms) that indicate the problem exists
- The problem can be grounded in real-world evidence or behavior

### 2.3 Affected Agent Clarity
- The affected user or entity is clearly identifiable
- The problem is anchored in a specific user or stakeholder context

### 2.4 Repeatability
- The problem occurs with sufficient frequency or consistency to justify analysis

### 2.5 Meaningful Impact
- The problem causes measurable or meaningful negative impact (time, cost, inefficiency, friction)

---

## 3. Invalid Problem Conditions
A problem is invalid if any of the following apply:
- It prescribes or implies a solution
- It is purely speculative without observable grounding
- It cannot be tied to a real agent or context
- It has no meaningful impact or relevance

---

## 4. Validation Principle
Validation is not opinion-based.
It must be grounded in observable evidence, structured reasoning, and artifact traceability.

---

## 5. Role in System
This layer acts as a gate between problem definition/structuring and downstream validation and solution exploration layers.
