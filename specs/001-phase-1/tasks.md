# Implementation Tasks: Phase I — Todo In-Memory Python Console Application

**Feature**: 001-phase-1
**Generated**: 2026-01-09
**Based on**: specs/001-phase-1/spec.md, plan.md, data-model.md
**Strategy**: MVP-first approach with independent user story delivery

## Dependencies

User stories are largely independent. US1 (Add) and US2 (List) should be completed before US3 (Mark), US4 (Update), and US5 (Delete) for foundational functionality.

## Parallel Execution Opportunities

- [ ] T002 [P] Create domain.py with TodoItem dataclass
- [ ] T003 [P] Create storage.py with TodoList class
- [ ] T015 [P] [US1] Implement CLI add command
- [ ] T018 [P] [US2] Implement CLI list command

## Implementation Strategy

**MVP Scope**: Complete User Story 1 (Add) and User Story 2 (List) first to establish core functionality. Then implement User Stories 3-5 in priority order.

---

## Phase 1: Setup & Project Structure

- [X] T001 Create project structure per implementation plan
  - Files: src/todo/__init__.py, src/todo/domain.py, src/todo/storage.py, src/todo/cli.py
  - Tests: tests/unit/test_domain.py, tests/unit/test_storage.py, tests/integration/test_cli.py

## Phase 2: Foundational Components

- [X] T002 Create TodoItem dataclass in src/todo/domain.py
  - Properties: id (int), description (str), completed (bool)
  - Validation: description cannot be empty/whitespace, id must be positive integer
  - Default: completed=False

- [X] T003 Create TodoList class in src/todo/storage.py
  - Methods: add_item(), list_items(), get_item(), update_item(), delete_item(), mark_complete(), mark_incomplete()
  - Storage: in-memory using Python data structures
  - ID assignment: sequential starting from 1

- [X] T004 Create CLI main loop in src/todo/cli.py
  - Command parsing: split input into command and arguments
  - Command dispatch: map commands to appropriate methods
  - Error handling: catch and display meaningful error messages

- [X] T005 Create entry point in src/main.py
  - Initialize TodoList instance
  - Start CLI loop
  - Handle graceful shutdown

## Phase 3: User Story 1 - Add Todo Items (Priority: P1)

- [X] T006 [US1] Define add command syntax and behavior
  - Command: "add <description>"
  - Action: creates new TodoItem with next available ID
  - Output: confirms successful addition with ID

- [ ] T007 [US1] Implement add_item method in TodoList class
  - Validates description is not empty/whitespace
  - Assigns next sequential ID
  - Adds item to internal storage
  - Returns the created TodoItem

- [ ] T008 [US1] Integrate add command with CLI
  - Parse description from command arguments
  - Call TodoList.add_item()
  - Display success/error message

- [ ] T009 [US1] Add validation for empty descriptions
  - Reject descriptions that are empty or only whitespace
  - Provide clear error message to user

- [ ] T010 [US1] Test add functionality
  - Verify new items are created with correct properties
  - Verify sequential ID assignment
  - Verify validation rejects empty descriptions

## Phase 4: User Story 2 - List Todo Items (Priority: P1)

- [ ] T011 [US2] Define list command syntax and behavior
  - Command: "list"
  - Action: displays all todo items with ID and status
  - Output: formatted list showing completion status

- [ ] T012 [US2] Implement list_items method in TodoList class
  - Returns all stored TodoItem objects
  - Maintains order of insertion

- [ ] T013 [US2] Implement get_item method in TodoList class
  - Returns specific TodoItem by ID
  - Raises exception if ID not found

- [ ] T014 [US2] Add empty list handling
  - Display appropriate message when no items exist

- [ ] T015 [US2] Integrate list command with CLI
  - Call TodoList.list_items()
  - Format and display results appropriately
  - Handle empty list case

- [ ] T016 [US2] Test list functionality
  - Verify all items are displayed correctly
  - Verify empty list case is handled properly
  - Verify formatting is user-friendly

## Phase 5: User Story 3 - Mark Todo Items Complete/Incomplete (Priority: P1)

- [ ] T017 [US3] Define mark commands syntax and behavior
  - Commands: "complete <id>" and "incomplete <id>"
  - Actions: updates completion status of specified item
  - Output: confirms status change

- [ ] T018 [US3] Implement mark_complete method in TodoList class
  - Finds item by ID
  - Sets completed=True
  - Returns updated item

- [ ] T019 [US3] Implement mark_incomplete method in TodoList class
  - Finds item by ID
  - Sets completed=False
  - Returns updated item

- [ ] T020 [US3] Integrate mark commands with CLI
  - Parse ID from command arguments
  - Validate ID exists
  - Call appropriate TodoList method
  - Display confirmation or error

- [ ] T021 [US3] Add error handling for invalid IDs
  - Handle case where ID doesn't exist
  - Provide clear error message

- [ ] T022 [US3] Test mark functionality
  - Verify completion status changes correctly
  - Verify error handling for invalid IDs
  - Verify changes persist in storage

## Phase 6: User Story 4 - Update Todo Items (Priority: P2)

- [ ] T023 [US4] Define update command syntax and behavior
  - Command: "update <id> <new_description>"
  - Action: updates description of specified item
  - Output: confirms update success

- [ ] T024 [US4] Implement update_item method in TodoList class
  - Finds item by ID
  - Updates description with validation
  - Returns updated item

- [ ] T025 [US4] Integrate update command with CLI
  - Parse ID and new description from arguments
  - Validate ID exists and description is valid
  - Call TodoList.update_item()
  - Display confirmation or error

- [ ] T026 [US4] Test update functionality
  - Verify descriptions are updated correctly
  - Verify validation rejects empty descriptions
  - Verify error handling for invalid IDs

## Phase 7: User Story 5 - Delete Todo Items (Priority: P2)

- [ ] T027 [US5] Define delete command syntax and behavior
  - Command: "delete <id>"
  - Action: removes specified item from storage
  - Output: confirms deletion

- [ ] T028 [US5] Implement delete_item method in TodoList class
  - Finds and removes item by ID
  - Handles case where ID doesn't exist
  - Returns success/failure status

- [ ] T029 [US5] Handle ID reassignment after deletion
  - Decide whether to maintain sequential IDs or allow gaps
  - Document behavior in specification

- [ ] T030 [US5] Integrate delete command with CLI
  - Parse ID from command arguments
  - Validate ID exists
  - Call TodoList.delete_item()
  - Display confirmation or error

- [ ] T031 [US5] Test delete functionality
  - Verify items are removed correctly
  - Verify error handling for invalid IDs
  - Verify remaining items are unaffected

## Phase 8: Error Handling & Edge Cases

- [ ] T032 Handle invalid commands
  - Provide helpful error message for unrecognized commands
  - Display available commands

- [ ] T033 Handle malformed command input
  - Validate required arguments are provided
  - Provide clear error messages for missing arguments

- [ ] T034 Add comprehensive error messages
  - User-friendly messages for all error conditions
  - Consistent error formatting

- [ ] T035 Test edge cases
  - Empty todo list scenarios
  - Invalid ID scenarios
  - Malformed command scenarios

## Phase 9: Polish & Cross-Cutting Concerns

- [X] T036 Create comprehensive test suite
  - Unit tests for domain and storage layers
  - Integration tests for CLI functionality
  - Contract tests for interface behavior

- [X] T037 Improve user experience
  - Add help command with usage instructions
  - Enhance output formatting
  - Add quit/exit command

- [X] T038 Documentation updates
  - Update quickstart.md with usage instructions
  - Add README with command reference

- [X] T039 Final integration testing
  - Test all user stories together
  - Verify no regressions between features
  - Performance testing with multiple items