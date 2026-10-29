# Tasks: Telecom Threat Intelligence Assistant

**Input**: Design documents in this directory  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`

## Phase 1: Setup

- [x] T001 Add Python dependencies and local secret/cache ignore rules.
- [x] T002 Create the RAG module and deterministic unit-test skeleton.

## Phase 2: User Story 1 - Grounded Question Answering (P1)

**Goal**: Answer natural-language questions with evidence and page citations.

- [x] T003 [P] Implement page-aware PDF extraction and overlapping chunking in `rag.py`.
- [x] T004 Implement Gemini embedding, SQLite index, fingerprint invalidation, and cosine retrieval in `rag.py`.
- [x] T005 Implement evidence-only response generation with source context in `rag.py`.
- [x] T006 Implement Streamlit question form, answer, and cited source display in `app.py`.
- [x] T007 [P] Test chunking, empty pages, page numbering, and retrieval ranking in `tests/test_rag.py`.

## Phase 3: User Story 2 - Threat Analysis and Recommendations (P2)

**Goal**: Support explanations, comparisons, recommendations, and briefings with visible evidence.

- [x] T008 Ensure prompts and UI support requested analysis formats while disclosing evidence gaps.
- [x] T009 Display advisory-use warning and explain that no telecom actions are performed.

## Phase 4: User Story 3 - Reusable Knowledge Base (P3)

**Goal**: Index the provided PDF once per source/model version.

- [x] T010 Handle missing PDF, empty extraction, missing key, and API failures explicitly.
- [x] T011 Verify index reuse and rebuild logic with deterministic tests where practical.

## Phase 5: Documentation and Validation

- [x] T012 Replace stale financial-assistant README and charter with threat-intelligence project documentation.
- [x] T013 Document architecture, methodology, setup, evaluation, limitations, and screenshot instructions.
- [x] T014 Run the offline test suite and verify app startup.
