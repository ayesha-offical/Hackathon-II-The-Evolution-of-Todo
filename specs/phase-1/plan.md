# Implementation Plan: Todo In-Memory Python Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-01-08 | **Spec**: `specs/001-todo-console-app/spec.md`
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

**Note**: This plan implements the 5 core features (Add, List, Complete, Update, Delete) for a console-based todo app using Python 3.13+ with in-memory storage.

## Summary

Build a single-session, in-memory todo application with a CLI interface supporting 5 core features: task creation with metadata (title, description, timestamps), task listing with status indicators, task completion toggles, title/description updates, and deletion. Architecture uses modular design: `models.py` (Task entity), `storage.py` (in-memory TaskStorage), `cli.py` (command dispatcher), and `main.py` (entry point). Test-first approach (TDD) ensures 80% code coverage via pytest. All code references Task IDs for traceability per Principle XIII of Constitution v1.1.0.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**:
- ✅ `rich` — Terminal formatting for colored output, tables, progress bars
- ✅ `pytest` — Unit/integration test framework
- ✅ `pytest-cov` — Code coverage measurement

**Storage**: In-memory (Python dictionary/list, no persistence across sessions)
**Testing**: pytest with TDD (test-first discipline)
**Target Platform**: Linux/macOS/Windows console (CLI-only)
**Project Type**: Single console application (CLI)
**Performance Goals**: <100ms response for all operations (add, list, update, delete, complete)
**Constraints**: <50MB memory footprint, no external dependencies beyond pre-approved list
**Scale/Scope**: Single-user, single-session, supports up to 10,000 tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitutional Principle Compliance

| Principle | Status | Details |
|-----------|--------|---------|
| **I. Spec-Driven Development** | ✅ PASS | Spec approved; plan follows; tasks will reference spec sections |
| **II. Zero Manual Coding Policy** | ✅ PASS | All code generation via Claude Code based on approved tasks |
| **III. Python 3.13+ with UV** | ✅ PASS | Python 3.13+ confirmed; UV for dependency management |
| **IV. In-Memory Storage (Phase 1)** | ✅ PASS | No database/persistence; reset on process restart |
| **V. PEP 8 Compliance** | ✅ PASS | 100-char max lines, type hints, descriptive naming |
| **VI. Single-File Architecture** | ✅ PASS | `src/main.py` + modular utilities (`models.py`, `storage.py`, `cli.py`) |
| **VII. Test-First (TDD)** | ✅ PASS | Red-Green-Refactor discipline; 80% coverage target via pytest-cov |
| **VIII. Basic Features Only** | ✅ PASS | Exactly 5 features: Add, Delete, Update, List, Complete |
| **IX. Console/CLI Interface** | ✅ PASS | CLI-only; no GUI or web frontend |
| **X. Documentation-First** | ✅ PASS | Spec → Plan → Tasks → Implement (in progress) |
| **XI. Simplicity Over Flexibility** | ✅ PASS | No premature abstractions; YAGNI principle applied |
| **XII. Error Handling & UX** | ✅ PASS | Input validation, clear error messages, graceful edge cases |
| **XIII. Code Traceability** | ✅ PASS | All code will have `[T-###]` task ID comments |
| **XIV. Dependency Management** | ✅ PASS | Only pre-approved libraries used; see below |

### Dependency Validation *(per Constitution Principle XIV)*

**Pre-Approved Libraries for Phase 1**:
- ✅ `rich` — CLI formatting and output (tables, colors, styles)
- ✅ `pytest` — Testing framework
- ✅ `pytest-cov` — Code coverage measurement

**Dependencies for this feature**: ALL PRE-APPROVED
- ✅ `rich` — Required for user-friendly CLI output (colored text, task table display)
- ✅ `pytest` — Required for TDD implementation
- ✅ `pytest-cov` — Required for 80% coverage validation

**No new dependencies required** — All functionality achievable with Python standard library + pre-approved libs.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── spec.md              # Feature requirements (approved ✓)
├── plan.md              # This file (implementation architecture)
├── tasks.md             # Task breakdown (to be created by /sp.tasks)
├── data-model.md        # Entity definitions (to be created)
├── quickstart.md        # Setup & usage guide (to be created)
└── checklists/
    └── requirements.md
```

### Source Code Structure (Single Console Application)

```text
Memory Python Console App/
├── src/
│   ├── main.py              # Entry point; CLI loop
│   ├── models.py            # Task entity (id, title, description, completed, timestamps)
│   ├── storage.py           # In-memory TaskStorage (add, get, list, update, delete, toggle)
│   ├── cli.py               # Command dispatcher (add, list, complete, update, delete, help)
│   └── __init__.py
│
├── tests/
│   ├── test_models.py       # Unit tests for Task model
│   ├── test_storage.py      # Unit tests for TaskStorage
│   ├── test_cli.py          # Integration tests for CLI commands
│   ├── test_acceptance.py   # End-to-end acceptance scenarios
│   └── __init__.py
│
├── pyproject.toml           # Project metadata + dependencies (UV-managed)
├── uv.lock                  # Locked dependency versions (auto-generated)
├── .gitignore               # Ignore __pycache__, .pytest_cache, .coverage
├── README.md                # Setup & usage instructions
└── CLAUDE.md                # SDD workflow guidelines
```

**Structure Decision**: Single Python console application (Option 1).
- Rationale: Phase 1 MVP is a CLI tool, not a distributed system
- `src/` contains modular components for testability
- `tests/` organized by unit/integration/acceptance per Constitution
- Simplicity over flexibility (Principle XI)

## Complexity Tracking

**No violations detected.** All 14 Constitutional Principles pass validation. No complexity justification needed.

## Design Artifacts (Phase 1 Outputs)

### Data Model (to be generated)

**Task Entity**:
```python
class Task:
    id: str                  # UUID (auto-generated)
    title: str               # Required, non-empty
    description: str         # Optional
    completed: bool          # Default False
    created_at: datetime     # ISO 8601 format
    updated_at: datetime     # ISO 8601 format
```

### CLI Command Interface (to be generated)

```
add <title> [description]       # Add new task
list                            # List all tasks with status
complete <task_id>              # Toggle task completion status
update <task_id> <title> [desc] # Update task details
delete <task_id>                # Delete task by ID
help                            # Show available commands
```

### API Contracts (to be generated)

```text
specs/001-todo-console-app/contracts/
├── task.schema.json       # Task entity JSON schema
├── commands.schema.json   # CLI command specifications
└── responses.schema.json  # Response format definitions
```

### Quickstart Guide (to be generated)

```text
specs/001-todo-console-app/quickstart.md
- Installation instructions (uv sync)
- Running the app (uv run src/main.py)
- Example workflows
- Troubleshooting
```

## Next Steps

1. ✅ **Plan Complete** — Constitution check passed; architecture finalized
2. ⏳ **Task Generation** — Run `/sp.tasks` to break plan into T-001, T-002, ... tasks
3. ⏳ **Implementation** — Run `/sp.implement` to generate code per task
4. ⏳ **Commit** — Each task generates a `[T-###]` commit with traceability
