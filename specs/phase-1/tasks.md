---
description: "Task breakdown for Todo In-Memory Python Console App Phase 1 implementation"
---

# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `specs/001-todo-console-app/`
**Prerequisites**: plan.md ✓, spec.md ✓ (both approved)
**Testing Approach**: Test-First (TDD) per Constitution Principle VII - Tests BEFORE implementation

**Organization**: Tasks grouped by user story (US1-US5) to enable independent implementation and testing of each feature.

## Format: `[ID] [P?] [Story] Description`

- **[ID]**: Task identifier T-001, T-002, etc. (referenced in git commits)
- **[P]**: Can run in parallel (different files, no interdependencies)
- **[Story]**: Which user story (US1, US2, US3, US4, US5) - REQUIRED for all story phase tasks
- All descriptions include exact file paths for implementation

## Code Traceability Requirements *(per Constitution Principle XIII)*

Each task MUST produce code with traceability:

**In code comments**:
```python
# [T-001] - Spec section: FR-001 (Task model with ID generation)
class Task:
    """Model for todo task with auto-generated ID."""
```

**In file headers**:
```python
"""
Module: Task model implementation
Task ID: T-001
Specification Reference: FR-001 - System MUST support task creation with metadata
"""
```

**In git commits** (per Constitution Principle VIII):
```
[T-001] Implement Task model with ID generation and timestamps

Adds Task class to src/models.py with required attributes:
- id (auto-generated UUID)
- title (string, required)
- description (string, optional)
- completed (boolean, default False)
- created_at, updated_at (ISO timestamps)

Satisfies spec requirement FR-001.
Tests passing: test_task_creation, test_task_validation
Coverage: 80%+ maintained
```

**Coverage Requirement**: All code MUST contribute to 80% minimum coverage (measured via `pytest-cov`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for all user stories

- [ ] T-001 Create project structure: `src/`, `tests/`, `pyproject.toml`, `.gitignore`
- [ ] T-002 Initialize Python 3.13+ project with UV: `uv init` and add dependencies (rich, pytest, pytest-cov)
- [ ] T-003 [P] Create `src/__init__.py` and `tests/__init__.py` empty placeholder files

**Checkpoint**: Project structure ready - foundation in place

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure MUST be complete before ANY user story implementation

⚠️ **CRITICAL**: No user story work begins until this phase completes

- [ ] T-004 Implement Task model in `src/models.py` with all required fields (id, title, description, completed, created_at, updated_at) per FR-001 and FR-002
- [ ] T-005 [P] Implement TaskStorage class in `src/storage.py` with in-memory dictionary for task management per FR-009
- [ ] T-006 [P] Implement CLI command dispatcher in `src/cli.py` with command routing structure per FR-007
- [ ] T-007 Create `src/main.py` with CLI entry point and REPL loop structure

**Checkpoint**: Foundation complete - all 5 user stories can now proceed independently in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can create a new task with title (required) and optional description, receiving immediate feedback with unique ID

**Independent Test**: Create a task via CLI, verify it appears in list with correct metadata (FR-001, FR-002)

**Acceptance Criteria**:
- User provides "add Buy groceries" → Task created with title only
- User provides "add Buy groceries" "Need milk, eggs, bread" → Task created with title AND description
- User provides empty/whitespace title → Rejected with clear error message, no task created
- New task gets unique UUID and appears in list with timestamps

### Tests for User Story 1 (TDD: Write tests FIRST, ensure they FAIL)

- [x] T-008 [P] [US1] Write test_task_creation in `tests/test_models.py`: Test Task model instantiation, ID generation, timestamps
- [x] T-009 [P] [US1] Write test_add_task_validation in `tests/test_storage.py`: Test empty title rejection, description optional, unique IDs per FR-001 and FR-008
- [x] T-010 [P] [US1] Write test_add_task_cli in `tests/test_cli.py`: Test "add" command parsing, success/error messages

### Implementation for User Story 1

- [x] T-011 [US1] Implement Task model validation: reject empty/whitespace titles in `src/models.py` (depends on T-004)
- [x] T-012 [US1] Implement TaskStorage.add_task() method in `src/storage.py` with UUID generation (depends on T-005, T-011)
- [x] T-013 [US1] Implement "add" command handler in `src/cli.py` with arg parsing and error messages (depends on T-006, T-012)
- [x] T-014 [US1] Add error handling for invalid input in CLI command flow in `src/cli.py`
- [x] T-015 [US1] Run pytest to verify all US1 tests pass with ≥80% coverage contribution

**Checkpoint**: User Story 1 (Add Task) fully functional and independently testable ✓

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can see a list of all tasks with ID, title, status, and description (if present) in a readable format

**Independent Test**: Create 3 tasks (mixed empty/filled descriptions), list them, verify all details display correctly (FR-003)

**Acceptance Criteria**:
- Empty task list → Display user-friendly "No tasks" message
- Multiple tasks → Display all with ID, title, completed status, description (if present)
- Mixed completed/incomplete → Show status indicators clearly (completed vs incomplete)

### Tests for User Story 2 (TDD: Write tests FIRST)

- [x] T-016 [P] [US2] Write test_list_empty in `tests/test_storage.py`: Test empty task list retrieval
- [x] T-017 [P] [US2] Write test_list_all_tasks in `tests/test_storage.py`: Test listing multiple tasks with all fields
- [x] T-018 [P] [US2] Write test_list_display_cli in `tests/test_cli.py`: Test "list" command output formatting with rich table

### Implementation for User Story 2

- [x] T-019 [US2] Implement TaskStorage.get_all_tasks() method in `src/storage.py` (depends on T-005)
- [x] T-020 [US2] Implement "list" command handler with rich table formatting in `src/cli.py` (depends on T-006, T-019)
- [x] T-021 [US2] Add status indicator display (✓ for completed, ☐ for incomplete) in `src/cli.py` per FR-003
- [x] T-022 [US2] Add error handling for edge cases (empty list, display formatting) in `src/cli.py`
- [x] T-023 [US2] Run pytest to verify all US2 tests pass with ≥80% cumulative coverage

**Checkpoint**: User Stories 1 + 2 (Add & List) fully functional ✓

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P1)

**Goal**: Users can toggle task completion status (incomplete ↔ completed) and see changes reflected immediately

**Independent Test**: Create a task, mark it complete, verify status change in list, toggle back to incomplete (FR-004)

**Acceptance Criteria**:
- Mark incomplete task complete → Status changes to completed in list
- Mark completed task incomplete → Status reverts to incomplete
- Mark specific task by ID → Only that task's status changes, others unaffected
- Invalid task ID → Clear error message, no state change

### Tests for User Story 3 (TDD: Write tests FIRST)

- [x] T-024 [P] [US3] Write test_toggle_completion in `tests/test_storage.py`: Test mark_complete() toggle behavior
- [x] T-025 [P] [US3] Write test_invalid_task_id in `tests/test_storage.py`: Test error handling for non-existent task IDs
- [x] T-026 [P] [US3] Write test_complete_command_cli in `tests/test_cli.py`: Test "complete" command parsing and user feedback

### Implementation for User Story 3

- [x] T-027 [US3] Implement TaskStorage.mark_complete() method with toggle logic in `src/storage.py` (depends on T-005)
- [x] T-028 [US3] Implement "complete" command handler in `src/cli.py` with ID parsing (depends on T-006, T-027)
- [x] T-029 [US3] Add validation for task ID existence and clear error messages in `src/cli.py` per FR-007
- [x] T-030 [US3] Add timestamp update for updated_at field when status changes in `src/models.py`
- [x] T-031 [US3] Run pytest to verify all US3 tests pass with ≥80% cumulative coverage

**Checkpoint**: User Stories 1 + 2 + 3 (Add, List, Complete) all P1 features working ✓

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Users can modify task title and/or description while preserving other fields and ID

**Independent Test**: Create a task, update title, then update description, verify both changes persist (FR-005)

**Acceptance Criteria**:
- Update only title → Title changes, description unchanged
- Update only description → Description changes, title unchanged
- Update non-existent task ID → Clear error message, no changes
- Empty title in update → Rejected with error per FR-008

### Tests for User Story 4 (TDD: Write tests FIRST)

- [x] T-032 [P] [US4] Write test_update_title in `tests/test_storage.py`: Test partial update (title only)
- [x] T-033 [P] [US4] Write test_update_description in `tests/test_storage.py`: Test partial update (description only)
- [x] T-034 [P] [US4] Write test_update_nonexistent in `tests/test_storage.py`: Test error handling for invalid task ID
- [x] T-035 [P] [US4] Write test_update_command_cli in `tests/test_cli.py`: Test "update" command with various argument patterns

### Implementation for User Story 4

- [x] T-036 [US4] Implement TaskStorage.update_task() method in `src/storage.py` with partial update support (depends on T-005)
- [x] T-037 [US4] Implement "update" command handler in `src/cli.py` with flexible arg parsing (depends on T-006, T-036)
- [x] T-038 [US4] Add title validation in update (reject empty/whitespace) in `src/storage.py` per FR-008
- [x] T-039 [US4] Update timestamp (updated_at) when modifications occur in `src/models.py`
- [x] T-040 [US4] Add error messages for invalid updates in `src/cli.py` per FR-007
- [x] T-041 [US4] Run pytest to verify all US4 tests pass with ≥80% cumulative coverage

**Checkpoint**: User Stories 1-4 all working (Add, List, Complete, Update) ✓

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: Users can permanently remove tasks from the list by ID

**Independent Test**: Create 3 tasks, delete one by ID, verify it no longer appears in list but others remain (FR-006)

**Acceptance Criteria**:
- Delete task by valid ID → Task removed, others unaffected
- Delete non-existent ID → Clear error message, no changes
- Delete completed task → Task removed like any other
- Task ID never reused after deletion (unique IDs per session)

### Tests for User Story 5 (TDD: Write tests FIRST)

- [x] T-042 [P] [US5] Write test_delete_task in `tests/test_storage.py`: Test task removal by ID
- [x] T-043 [P] [US5] Write test_delete_nonexistent in `tests/test_storage.py`: Test error handling for invalid IDs
- [x] T-044 [P] [US5] Write test_delete_command_cli in `tests/test_cli.py`: Test "delete" command with ID validation feedback

### Implementation for User Story 5

- [x] T-045 [US5] Implement TaskStorage.delete_task() method in `src/storage.py` (depends on T-005)
- [x] T-046 [US5] Implement "delete" command handler in `src/cli.py` with ID parsing (depends on T-006, T-045)
- [x] T-047 [US5] Add validation and error messages for invalid task IDs in `src/cli.py` per FR-007
- [x] T-048 [US5] Ensure ID uniqueness persists across deletions (no ID reuse) - document in comments
- [x] T-049 [US5] Add confirmation prompt for destructive operation (optional user-friendly enhancement)
- [x] T-050 [US5] Run pytest to verify all US5 tests pass with ≥80% cumulative coverage

**Checkpoint**: All User Stories 1-5 complete (Add, List, Complete, Update, Delete) ✓

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, and coverage validation across all stories

- [ ] T-051 [P] Run full test suite: `uv run pytest tests/ -v` with coverage report via `pytest-cov`
- [ ] T-052 [P] Verify ≥80% code coverage: `uv run pytest tests/ --cov=src --cov-report=term-missing`
- [ ] T-053 [P] Add help command in `src/cli.py`: Display all available commands with syntax per FR-007
- [ ] T-054 [P] Add input validation summary to `src/cli.py` for all error cases per FR-007 and FR-008
- [ ] T-055 Create README.md with: Installation (uv sync), Running app (uv run src/main.py), Example commands, Troubleshooting
- [ ] T-056 Verify PEP 8 compliance: 100-character max line length, type hints on all functions in all files
- [ ] T-057 Code cleanup: Remove any debug prints, ensure consistent naming, documentation strings
- [ ] T-058 Test acceptance scenarios end-to-end: Add → List → Complete → Update → Delete workflow
- [ ] T-059 Review all commits: Verify [T-###] format throughout git log per Constitution Principle VIII
- [ ] T-060 Final validation: Run quickstart.md workflows and confirm all 5 features operational

**Checkpoint**: Phase 1 MVP Complete - All features tested, documented, ready for delivery ✓

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Setup - BLOCKS all stories - T-004 through T-007
- **Phase 3 (US1)**: Depends on Foundational - Can start after Phase 2
- **Phase 4 (US2)**: Depends on Foundational + US1 foundation (TaskStorage + CLI structure)
- **Phase 5 (US3)**: Depends on Foundational + previous phases foundation
- **Phase 6 (US4)**: Depends on Foundational + previous phases foundation
- **Phase 7 (US5)**: Depends on Foundational + previous phases foundation
- **Phase 8 (Polish)**: Depends on all user stories complete

### User Story Dependencies (After Foundational Phase 2)

- **US1 (Add Task) - P1**: No story dependencies → Can start immediately after Phase 2
- **US2 (List Tasks) - P1**: Depends on US1 foundation (needs TaskStorage.add_task) → Start after T-012
- **US3 (Complete) - P1**: Depends on US1+US2 (needs add + list working) → Start after T-020
- **US4 (Update) - P2**: Depends on US1+US2+US3 foundation → Start after Phase 5
- **US5 (Delete) - P2**: Depends on US1+US2+US3 foundation → Start after Phase 5

### Within Each User Story (Test-First Discipline)

1. **Write tests FIRST** - must FAIL before any implementation
2. **Implement models** - Task entity requirements
3. **Implement storage** - TaskStorage methods
4. **Implement CLI** - Command handlers
5. **Verify tests PASS** - with ≥80% coverage contribution
6. **Final verification** - Run full test suite

### Parallel Opportunities

**Phase 1 (Setup)**:
- T-003 can run in parallel (different files)

**Phase 2 (Foundational)**:
- T-005, T-006 can run in parallel (models independent, CLI structure independent until they merge)
- T-004 blocks the others (required foundation)

**Phase 3 (US1)**:
- T-008, T-009, T-010 can run in parallel (different test files - TDD)
- T-011 blocks T-012, T-013
- T-012, T-013 can run in parallel

**Phase 4+ (US2-5)**:
- Tests (marked [P]) can run in parallel per story
- Story implementations MUST sequence: US1 → US2 → US3 → US4 → US5

---

## Parallel Example: User Story 1 (Add Task)

```bash
# Launch all US1 tests together (TDD - should all FAIL initially):
Task T-008: test_task_creation in tests/test_models.py
Task T-009: test_add_task_validation in tests/test_storage.py
Task T-010: test_add_task_cli in tests/test_cli.py

# Then implement models + storage + CLI:
Task T-011: Task model validation
Task T-012: TaskStorage.add_task()
Task T-013: "add" command handler
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only - P1 Features)

**Fastest path to working MVP**:

1. Complete **Phase 1** (Setup) - 30 min
2. Complete **Phase 2** (Foundational) - 1.5 hrs
3. Complete **Phase 3** (US1: Add Task) - 1 hr
4. Complete **Phase 4** (US2: List Tasks) - 1 hr
5. Complete **Phase 5** (US3: Complete Task) - 1 hr
6. **STOP and VALIDATE**: Run full test suite, verify coverage ≥80%
7. **Deploy**: MVP ready with 3 core features (add, list, complete)

**Time to MVP: ~5.5 hours**

### Full Phase 1 (All 5 Features)

**Complete implementation**:

1. Setup + Foundational (same as above)
2. User Stories 1-3 (P1 - core features)
3. User Stories 4-5 (P2 - supporting features)
4. Polish & Cross-Cutting (Phase 8)
5. Full validation + documentation

**Time to Full Phase 1: ~8-10 hours**

### Parallel Team Strategy (if multiple developers available)

With 3-person team:

1. **Everyone**: Phase 1 (Setup) together - 30 min
2. **Everyone**: Phase 2 (Foundational) together - 1.5 hrs
3. Once Foundational done:
   - **Dev A**: User Story 1 (Add) + User Story 2 (List) - 2 hrs
   - **Dev B**: User Story 3 (Complete) + User Story 4 (Update) - 2 hrs
   - **Dev C**: User Story 5 (Delete) + Polish (Phase 8) - 1.5 hrs
4. Stories complete independently, then integrate
5. Final validation together - 30 min

**Parallel time to completion: ~4.5 hours**

---

## Notes for Implementation

- **[P] tasks** = Different files, safe to run in parallel without conflicts
- **[Story] label** = Maps task to specific user story (US1-US5) for traceability
- **Test-First Discipline**: Write tests BEFORE implementing (RED → GREEN → REFACTOR)
- **Coverage Validation**: Run `uv run pytest tests/ --cov=src --cov-report=term-missing` after each phase
- **Commits**: Each task or logical group gets a `[T-###]` commit with full message format
- **Acceptance Criteria**: All tasks must satisfy spec requirements (FR-001 through FR-009)
- **Stop at any checkpoint**: Can validate and deploy at US1 (MVP), US1-3 (Core P1), or Full (US1-5)
- **Avoid**: Vague task descriptions, same file conflicts, cross-story dependencies that break independence
