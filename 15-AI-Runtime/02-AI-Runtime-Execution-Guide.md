# AI Runtime Execution Guide

## 1. Purpose
Defines how the AI system continuously operates over the Venture Operating System (VOS) once a venture instance has been initialized via the AI Entry Protocol.

This layer governs step-by-step execution, navigation across VOS layers, and deterministic artifact production.

---

## 2. Core Principle
The AI operates as a **state-driven execution engine over artifacts**, not as a conversational agent.

Every action must be derived from:
- current VOS state
- existing artifacts
- valid transition rules

---

## 3. Runtime Loop
The AI MUST continuously execute the following loop:

### Step 1: State Evaluation
Determine current derived system state from Execution layer.

### Step 2: Context Loading
Load all relevant artifacts from current and upstream layers.

### Step 3: Gap Detection
Identify missing or incomplete artifacts required for valid progression.

### Step 4: Next Artifact Selection
Select the next valid artifact strictly according to layer ordering:

00 → 14 (forward progression only, unless revalidation is required)

### Step 5: Artifact Generation
Produce or update exactly one artifact per cycle.

---

## 4. Navigation Rules
The AI MUST:

- never skip layers
- never jump ahead without completing dependencies
- revisit upstream layers only when invalid state is detected

The AI MUST NOT:

- generate multiple-layer outputs in one cycle
- perform speculative branching outside defined state transitions

---

## 5. Control Mechanisms

### 5.1 Deterministic Progression
Each cycle produces a single, traceable change.

### 5.2 Dependency Enforcement
No artifact is valid unless upstream dependencies are satisfied.

### 5.3 State Consistency Check
After each cycle, system state must remain consistent with Execution State Model.

---

## 6. Failure Modes
The system is invalid if:

- it bypasses Execution layer constraints
- it produces untraceable artifacts
- it introduces new assumptions without validation

---

## 7. Role in VOS
This layer operationalizes the entire VOS as a runtime system, enabling continuous, structured venture construction driven by AI execution cycles.