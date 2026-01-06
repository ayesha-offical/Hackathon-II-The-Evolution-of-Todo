<!--
=== CONSTITUTION AMENDMENT SYNC IMPACT REPORT ===
Version: 1.0.0 → 1.1.0 (MINOR: New principles + expanded guidance)
Date: 2026-01-06

PRINCIPLES ADDED:
✓ Principle XIII: Code Traceability & Task References
✓ Principle XIV: Dependency Management & Pre-Approved Libraries

SECTIONS EXPANDED:
✓ Implementation Phase: Added Git Commit Rules section
✓ Quality Gates → Code Acceptance: Added coverage requirement (80% minimum)
✓ Key Decisions: Added Decisions 5-8 rationale for new principles

CHANGES SUMMARY:
• Added 2 new core principles with enforcement mechanisms
• Extended testing discipline with specific coverage target
• Formalized git commit conventions with task ID requirement
• Created pre-approved dependency list for Phase 1
• Strengthened traceability chain: spec → task → code → commit

TEMPLATES STATUS:
⚠ .specify/templates/spec-template.md — Review for coverage metric guidance
⚠ .specify/templates/plan-template.md — Review for dependency validation check
⚠ .specify/templates/tasks-template.md — Consider task ID format guidance
⚠ README.md / CLAUDE.md — Should document new commit conventions

DEPENDENT ARTIFACTS REQUIRING REVIEW:
• Existing specifications may need dependency clarity
• Existing tasks should reference coverage targets
• Future commits must follow [T-###] format

DEFERRED PLACEHOLDERS: None
-->

# Todo In-Memory Python Console App Constitution

**Version**: 1.1.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-06

---

## Core Principles

### I. Spec-Driven Development (Agentic Dev Stack)

All development MUST follow the strict Spec-Driven Development lifecycle: **Specify → Plan → Tasks → Implement**.

No code shall be written without an approved specification. No features shall be implemented without a task assignment that traces back to the specification. Claude Code generates all implementation code; manual coding is forbidden during Phase 1.

**Rationale**: Ensures alignment between requirements and implementation, prevents scope creep, allows Claude Code to work autonomously with clear intent.

### II. Zero Manual Coding Policy

All code generation MUST be performed by Claude Code based on approved specifications and task definitions. Manual code writing is strictly prohibited.

If Claude Code fails to generate correct code, the specification or task definition MUST be refined and resubmitted, NOT manually patched.

**Rationale**: This hackathon emphasizes AI-driven development as the future of software engineering. Manual intervention defeats the purpose of mastering spec-driven development and Claude Code capabilities.

### III. Python 3.13+ with UV Dependency Management

All project code MUST use Python 3.13 or higher. Dependencies MUST be managed exclusively through UV (uv).

No pip, conda, or other package managers are permitted. No direct requirements.txt; use UV's pyproject.toml and uv.lock exclusively.

**Rationale**: UV provides deterministic, fast dependency resolution and aligns with modern Python development practices. Python 3.13+ ensures access to latest language features and performance improvements.

### IV. In-Memory Data Storage (Phase 1)

All task data MUST be stored exclusively in memory during Phase 1. No persistent database, file storage, or external state.

Application state is reset on process restart. This is intentional for Phase 1 MVP validation.

**Rationale**: Phase 1 focuses on core functionality and spec-driven development methodology, not data persistence. Persistence is introduced in Phase 2.

### V. PEP 8 Compliance & Clean Code

All code MUST adhere to PEP 8 style guidelines. Code MUST be clean, self-documenting, and maintainable.

Naming conventions: descriptive names for functions/classes/variables. Maximum line length: 100 characters. Type hints REQUIRED for all function signatures.

**Rationale**: Clean code reduces cognitive load, improves collaboration, and ensures readability for review and future enhancement.

### VI. Single-File Architecture (Phase 1)

Phase 1 implementation MUST be consolidated into a single main module (`src/main.py`) with supporting utilities in `src/` subdirectory.

No complex project structure; keep it simple and focused. All imports MUST be relative and clear.

**Rationale**: Phase 1 is a console app MVP. Complex folder hierarchies introduce unnecessary abstraction; linear clarity is preferred for specification compliance.

### VII. Test-First Discipline (Red-Green-Refactor)

Test-driven development (TDD) MUST be followed: Write tests first (RED), watch them fail, implement code (GREEN), then refactor (REFACTOR).

All acceptance criteria from specification MUST have corresponding test cases. Tests MUST be in `tests/` directory using pytest.

**Rationale**: Tests serve as executable specifications, ensuring code meets defined requirements and catches regressions early.

### VIII. Basic Level Features Only (Phase 1 Scope)

Phase 1 MUST implement ONLY the five Basic Level features:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark as Complete

No Intermediate or Advanced Level features. No feature creep.

**Rationale**: MVP clarity. Each phase has explicit scope boundaries. Strict adherence prevents burnout and ensures quality over quantity.

### IX. Console/CLI Interface

The application MUST expose functionality EXCLUSIVELY via a command-line interface (CLI). No GUI, web frontend, or other UI in Phase 1.

CLI MUST be user-friendly with clear prompts, error messages, and help documentation via `--help`.

**Rationale**: Aligns with hackathon Phase 1 deliverables. CLI is fast to implement and test, keeping focus on spec-driven methodology.

### X. Documentation-First Approach

All specifications, plans, and tasks MUST be written BEFORE code. Documentation is the source of truth; code is an implementation detail.

Every specification MUST include user scenarios, requirements, and acceptance criteria. Every plan MUST reference the specification. Every task MUST reference the plan.

**Rationale**: Prevents "vibe coding," ensures stakeholder alignment, and allows Claude Code to work with clear intent.

### XI. Simplicity Over Flexibility

Code MUST be the simplest possible solution to the stated problem. No premature generalization, no "what-if" abstractions, no unused options.

If a feature is not in the specification, do not implement it. YAGNI (You Aren't Gonna Need It) principle MUST be followed.

**Rationale**: Phase 1 is an MVP. Complexity reduces maintainability and violates the spec-driven principle.

### XII. Error Handling & User Experience

All user inputs MUST be validated. Error messages MUST be clear and actionable.

System MUST gracefully handle edge cases (empty task list, duplicate IDs, invalid input). No silent failures.

**Rationale**: Console apps live or die by their UX. Clear feedback improves usability and reduces support burden.

### XIII. Code Traceability & Task References

All generated code MUST explicitly reference the Task ID that produced it. Task ID citations MUST appear as comments in the code linking to the originating specification section.

Format for code references: `# [Task ID] - [Spec section]` at the start of each logical code block. Generated code files MUST include a header comment with the originating task ID.

Traceability enables accountability, audit trails, and clear linkage from implementation back to requirements.

**Rationale**: SDD mandates unbroken traceability from specification → plan → task → code. This principle ensures Claude Code maintains bidirectional links, enabling specification compliance validation and change impact analysis.

### XIV. Dependency Management & Pre-Approved Libraries

All dependencies MUST be added via UV's `pyproject.toml` configuration. No direct pip installations; all packages resolved through `uv lock`.

Phase 1 pre-approved libraries for CLI development:
- **rich** (for formatted output, tables, progress bars)
- **pytest** (for test framework)
- **pytest-cov** (for code coverage metrics)

New dependency additions require:
1. Specification amendment justifying the new dependency
2. Confirmation that no pre-approved alternative exists
3. UV installation via `pyproject.toml` + `uv lock` regeneration

**Rationale**: Deterministic dependency resolution prevents version drift and configuration surprises. Pre-approved list enforces discipline; new dependencies require specification change, aligning with SDD methodology.

---

## Development Workflow

### Specification Phase

1. User provides feature description or requirement
2. Claude Code generates `specs/<feature>/spec.md` with user stories, requirements, acceptance criteria
3. Specification MUST be reviewed and approved before proceeding
4. Specification MUST include all mandatory sections: User Scenarios, Requirements, Success Criteria

### Planning Phase

1. From approved specification, Claude Code generates `specs/<feature>/plan.md`
2. Plan MUST include: Technical Context, Project Structure, Architecture Decisions
3. Plan MUST reference Constitution to ensure compliance
4. Plan MUST be reviewed and approved before task generation

### Tasks Phase

1. From approved plan, Claude Code generates `specs/<feature>/tasks.md`
2. Tasks MUST be granular, independently testable, and linked back to specification
3. Tasks MUST follow format: `[ID] [P?] [Story] Description`
4. All tasks are assigned to Claude Code for implementation

### Implementation Phase

1. Claude Code reads approved task, referenced plan, and specification
2. Claude Code generates code that satisfies task acceptance criteria
3. Code MUST include references to task IDs in comments following Principle XIII
4. Tests MUST pass before code is committed (minimum 80% code coverage required)
5. Code is reviewed against specification compliance
6. Git commits MUST reference Task ID in format: `[T-###] Commit message`

### Git Commit Rules

Every commit MUST follow this format:
```
[T-###] Brief description of change

Optional detailed explanation of what was implemented and why.
References to specification sections or acceptance criteria.
```

Example:
```
[T-001] Implement Task model with ID generation and timestamps

Adds Task class to src/models.py with required attributes:
- id (auto-generated UUID)
- title (string, required)
- description (string, optional)
- completed (boolean, default False)
- created_at, updated_at (ISO timestamps)

Satisfies spec requirement FR-001: System MUST support task creation with metadata.
Tests passing: test_task_creation, test_task_validation (80% coverage maintained)
```

Task ID format: T-001, T-002, T-003, etc., matching task IDs from tasks.md.

---

## Quality Gates

### Before Coding Starts
- [ ] Specification MUST be complete and approved
- [ ] Plan MUST be reviewed for constitutional compliance
- [ ] All tasks MUST reference back to spec and plan
- [ ] No placeholder TODOs in code

### Code Acceptance
- [ ] All tests PASS
- [ ] Minimum 80% code coverage (measured via pytest-cov)
- [ ] Code adheres to PEP 8
- [ ] Type hints present on all function signatures
- [ ] Error handling implemented for edge cases
- [ ] Task ID references present in code comments (Principle XIII)
- [ ] Documentation comments match implementation

### Release Readiness (Phase 1)
- [ ] All 5 Basic Level features implemented and tested
- [ ] README.md complete with setup and usage instructions
- [ ] CLAUDE.md documents Claude Code workflow
- [ ] specs/ folder contains all specification documents
- [ ] GitHub repository public with clear folder structure

---

## Governance

### Amendment Procedure

Amendments to this Constitution require:
1. Identification of principle(s) needing change
2. Clear rationale for amendment
3. Impact analysis on dependent artifacts (specs, plans, tasks)
4. Version increment following semantic versioning

### Versioning Policy

- **MAJOR** (e.g., 2.0.0): Backward-incompatible principle removal or redefinition
- **MINOR** (e.g., 1.1.0): New principle added or significant guidance expansion
- **PATCH** (e.g., 1.0.1): Clarifications, wording improvements, non-semantic refinements

### Compliance Review

All specifications, plans, and tasks MUST be reviewed against this Constitution before approval. Constitution violations MUST be justified in writing or remedied.

---

## Project Structure

```
.
├── .specify/                 # Spec-Kit Plus framework
│   ├── memory/
│   │   └── constitution.md   # This file
│   ├── templates/            # Spec, plan, task templates
│   └── scripts/bash/         # SDD automation scripts
├── specs/                    # All specification files
│   └── phase-1/
│       ├── spec.md           # Feature specification
│       ├── plan.md           # Implementation plan
│       └── tasks.md          # Task breakdown
├── src/                      # Python source code
│   ├── main.py               # CLI entry point
│   ├── models.py             # Task model definitions
│   ├── cli.py                # CLI commands and handlers
│   └── storage.py            # In-memory storage implementation
├── tests/                    # Test files (pytest)
│   ├── test_models.py        # Unit tests for models
│   ├── test_storage.py       # Unit tests for storage
│   ├── test_cli.py           # Integration tests for CLI
│   └── test_acceptance.py    # Acceptance criteria tests
├── pyproject.toml            # UV project configuration
├── uv.lock                   # Locked dependencies (auto-generated)
├── README.md                 # User-facing documentation
├── CLAUDE.md                 # Claude Code workflow instructions
└── .gitignore                # Git ignore rules
```

---

## Success Criteria (Phase 1)

1. **All Basic Level Features Implemented**: Add, Delete, Update, View, Mark Complete
2. **All Tests Pass**: 100% of acceptance criteria covered by passing tests
3. **Code Quality**: PEP 8 compliant, type-hinted, well-documented
4. **Specification Adherence**: Zero feature creep, zero manual coding interventions
5. **User Experience**: CLI is intuitive, error messages are clear, help is available
6. **Documentation Complete**: Specs, plans, tasks, README, CLAUDE.md all present

---

## Constraints & Non-Goals

### Constraints
- Must use Python 3.13+
- Must use UV for dependencies
- Must follow Agentic Dev Stack (Spec → Plan → Tasks → Implement)
- Must be in-memory storage only (Phase 1)
- Must be CLI-only (no GUI)

### Non-Goals (Phase 1)
- Database persistence (Phase 2)
- Web frontend (Phase 2)
- User authentication (Phase 2)
- Intermediate/Advanced features (Phase 2+)
- Multi-user support (Phase 2+)
- Performance optimization (Phase 2+)

---

## Key Decisions

**Decision 1: Agentic Dev Stack as mandatory workflow**
- Rationale: Hackathon explicitly requires Spec-Driven Development and Zero Manual Coding
- Alternative: Traditional waterfall or agile → Rejected (incompatible with hackathon requirements)

**Decision 2: In-Memory Storage**
- Rationale: Phase 1 MVP focus on spec-driven methodology, not data persistence
- Alternative: Add database now → Rejected (violates YAGNI, adds unnecessary complexity)

**Decision 3: Single Main Module Architecture**
- Rationale: Phase 1 is small console app; complex structure adds overhead
- Alternative: Full MVC/layered architecture → Rejected (premature abstraction)

**Decision 4: PEP 8 + Type Hints Mandatory**
- Rationale: Clean code scales with team size; type hints catch bugs early
- Alternative: Flexible style guidelines → Rejected (quality degrades without standards)

**Decision 5: Code Traceability Requirement (Principle XIII)**
- Rationale: SDD requires unbroken chains from spec → task → code; task ID comments enable automated compliance checking and change impact analysis
- Alternative: No explicit traceability → Rejected (violates SDD principle, loses audit trail)

**Decision 6: Pre-Approved Dependency List (Principle XIV)**
- Rationale: Reduces decision fatigue, prevents dependency bloat, enforces specification discipline (new libs require spec amendment)
- Alternative: Open dependency addition → Rejected (encourages scope creep, complicates maintenance)

**Decision 7: 80% Code Coverage Minimum (Test Discipline)**
- Rationale: Catches edge cases early, ensures acceptance criteria verification, reduces regression risk
- Alternative: No coverage target → Rejected (leads to untested code paths in edge cases)

**Decision 8: Mandatory Task ID in Git Commits (Traceability)**
- Rationale: Enables blame/history traceability, links commits to tasks, supports specification compliance audits
- Alternative: Optional commit references → Rejected (loses accountability chain, complicates debugging)

---

## Related Documents

- **CLAUDE.md** - AI agent workflow and command reference
- **specs/phase-1/spec.md** - Feature specification and acceptance criteria
- **specs/phase-1/plan.md** - Technical architecture and project structure
- **specs/phase-1/tasks.md** - Granular task breakdown for implementation
- **README.md** - User-facing setup and usage guide

