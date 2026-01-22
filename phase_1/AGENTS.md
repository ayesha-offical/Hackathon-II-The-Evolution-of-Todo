# AGENTS.md

## 🎯 Phase 1: Hackathon Core Mandate
This project is a **Todo In-Memory Python Console App**.
- **Tech Stack:** Python 3.13+ and UV package manager.
- **Data:** Strictly in-memory (no databases).
- **Process:** Follow the lifecycle: Specify → Plan → Tasks → Implement.
- **Rule:** Every line of code must be written by Claude Code. **No manual coding.**

---

## 🧠 Spec-Driven Development (SDD) Workflow
This project uses **Spec-Driven Development** — no agent is allowed to write code until the specification is complete and approved.

### 1. Constitution (WHY) 
File: `.specify/memory/constitution.md`
Project’s non-negotiables: architecture, tech stack, and patterns allowed.

### 2. Specify (WHAT)
File: `specs/<feature>/spec.md`
User journeys, Requirements, and Acceptance criteria. Do not infer missing info.

### 3. Plan (HOW)
File: `specs/<feature>/plan.md`
Architecture, components, and high-level sequencing.

### 4. Tasks (BREAKDOWN)
File: `specs/<feature>/tasks.md`
Atomic, testable work units. **No task = No code.**

---

## 🛠 Technical Guidelines (PHR & ADR System)

### 1. Knowledge Capture (PHR)
You **MUST** create a Prompt History Record (PHR) after **EVERY** user message.
- **Location:** `history/prompts/` (sub-folders: `constitution`, `<feature-name>`, or `general`).
- **Process:** Detect stage, generate title, resolve route, and fill the PHR template.
- **Constraint:** Do not truncate `PROMPT_TEXT`. Record verbatim.

### 2. Architectural Decision Records (ADR)
When significant decisions are made:
- Suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`."
- Never auto-create ADRs; require user consent.

### 3. Authoritative Source Mandate
- Prioritize MCP tools and CLI commands.
- Never assume solutions from internal knowledge; verify everything externally.

### 4. Human as Tool Strategy
Invoke the user for input when:
- Requirements are ambiguous.
- Unforeseen dependencies arise.
- Architectural uncertainty exists.

---

## 📜 Code Standards
- Follow **PEP 8** and Clean Code principles.
- Use `uv run` for execution and testing.
- Cite existing code with references (start:end:path).
- Smallest viable diffs only.