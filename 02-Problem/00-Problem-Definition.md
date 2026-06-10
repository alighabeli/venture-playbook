# Problem Definition

## 1. Purpose of this Layer
The Problem layer formalizes how a venture problem is defined, separated from ideas, solutions, or implementations.

It converts ambiguous venture intent into a structured, analyzable problem space.

---

## 2. Problem Definition Principle
A problem is valid in this system only if it:
- Exists independently of any proposed solution
- Can be expressed without reference to implementation
- Is observable as a form of uncertainty or unmet need

---

## 3. Problem Structure
Every problem must be represented through:

### 3.1 Problem Statement
A concise description of the core uncertainty or unmet need.

### 3.2 Affected Domain
The context in which the problem exists (market, user group, system environment).

### 3.3 Observable Symptoms
External signals indicating the presence of the problem.

### 3.4 Root Cause Hypothesis (Optional)
Initial hypothesis about why the problem exists. Must remain testable and non-implementation-based.

---

## 4. Problem Validation Rules
A problem is invalid if:
- It prescribes a solution implicitly or explicitly
- It depends on a specific product or implementation
- It cannot be observed or reasoned about independently

---

## 5. Boundary Constraint
The Problem layer MUST NOT include:
- Solution design
- Product specification
- Architecture or system design
- Execution planning

---

## 6. Role of This Layer in OS
This layer acts as the first transformation of Vision intent into structured uncertainty.
It is the foundation for all downstream validation and solution exploration layers.
