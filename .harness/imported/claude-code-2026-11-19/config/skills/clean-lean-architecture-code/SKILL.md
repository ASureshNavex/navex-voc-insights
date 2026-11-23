---
name: clean-lean-architecture-code
description: Enforces lean, zero-bloat code generation with strict adherence to SOLID, DRY, YAGNI, KISS, loose coupling, concise block-level comments, and zero AI reasoning/chatter artifacts inside source files.
---

# Clean, Lean & Loosely Coupled Code — Universal Engineering Skill

When generating, refactoring, or reviewing any file across the codebase (TypeScript, React, Python, SCSS, SQL), strictly enforce minimalism, clarity, and sound software design principles.

---

## 1. Zero AI Artifacts & Concise Comment Hygiene
- **Never Leak AI Workings into Code:** Never output placeholder comments, thinking notes, TODOs for unimplemented logic, or conversational markers inside source files (e.g., strictly forbid `// ... rest of code`, `# I added this to fix...`, `// Step 1: First we...`, `// Changed per user request`). Output complete, production-ready code only.
- **High-Signal, Block-Level Comments Only:**
  - Do **not** narrate obvious syntax line-by-line (e.g., avoid `# Increment counter by 1` or `// Fetch user`).
  - Write brief, high-level comments strictly to explain **what a logical block or component achieves** or **why a non-obvious domain constraint exists** (e.g., `# Enforce RBAC data-scope filter before aggregating ARR metrics`).
  - Rely on clear function, variable, and type names so the code is self-documenting.

---

## 2. Lean Code & Zero Bloat (YAGNI & KISS)
- **Write Only Required Lines:** Deliver the minimal, simplest implementation that completely satisfies the requirement. Do not generate speculative abstractions, unused helper functions, dead flags, or premature configuration knobs (**YAGNI**).
- **Keep It Simple (KISS):** Prefer straightforward control flow, early returns (guard clauses), and flat structures over deeply nested `if/else` blocks, complex inheritance trees, or clever one-liners.
- **Small, Focused Units:**
  - Keep functions and React components small and focused on a single task. If a function exceeds ~30–40 lines or handles multiple distinct responsibilities, split it cleanly.
  - Remove unused imports, variables, and commented-out code immediately.

---

## 3. SOLID Principles (Practical Enforcement)
- **Single Responsibility (SRP):** Every module, class, React component, and FastAPI service function must have **one clear reason to change**. Separate UI rendering (JSX), data fetching (hooks/services), and pure business rules.
- **Open/Closed (OCP):** Extend behavior via composition, strategy maps/dictionaries, or interface implementations rather than modifying core orchestrators with growing `if/elif` or `switch` chains.
- **Liskov Substitution (LSP):** Subtypes, mock adapters, and swappable connectors (e.g., S3, MCP, Snowflake ports) must honor the exact input/output contracts and exceptions of their base protocol/interface.
- **Interface Segregation (ISP):** Keep TypeScript interfaces, React component props, and Python `Protocol` definitions small and client-specific. Never force a component or service to depend on massive "god objects" when it only needs two fields.
- **Dependency Inversion (DIP):** High-level domain logic must depend on abstractions (Python `Protocol` / ABCs, TypeScript interfaces, FastAPI `Depends`), never directly on low-level vendor SDKs or concrete infrastructure clients.

---

## 4. Loose Coupling & DRY (Without Over-Abstraction)
- **Strict Module Boundaries:**
  - Modules must communicate only through explicit, typed public interfaces (`schemas.py`, `types.ts`, `ports/`).
  - Never reach into another feature's internal files or private helpers.
- **Rule of Three for DRY:** Eliminate true duplication of business logic and validation rules, but do **not** prematurely merge two functions just because they look syntactically similar today. Wrong abstraction is worse than minor duplication.
- **Pure Core, Thin Edges:** Keep core business transformations pure and deterministic (easy to unit test without mocks), pushing I/O (HTTP, database, Bedrock, DOM events) to the outer edges of the module.
