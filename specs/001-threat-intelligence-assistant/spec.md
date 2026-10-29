# Feature Specification: Telecom Threat Intelligence Assistant

**Feature Branch**: `001-threat-intelligence-assistant`  
**Created**: 2026-10-29  
**Status**: Approved for implementation  
**Input**: User request and `project-requirement/Problem Statement.docx`

## User Scenarios & Testing

### User Story 1 - Ask a source-grounded security question (Priority: P1)

A telecom security analyst asks a natural-language question and receives a concise explanation based on locally retrieved passages from the supplied ITU-T reference, with page-level evidence they can inspect.

**Why this priority**: Grounded question answering is the core project outcome.

**Independent Test**: With a configured model key and indexed reference PDF, submit a question covered by the PDF; verify the response and one or more page citations are displayed.

**Acceptance Scenarios**:

1. **Given** the reference has been indexed, **When** a user asks about a telecom security topic, **Then** the assistant returns an answer and the retrieved source passages with page numbers.
2. **Given** the retrieved passages do not support a requested claim, **When** the assistant answers, **Then** it explicitly identifies the evidence gap and does not present an unsupported claim as fact.

### User Story 2 - Request threat analysis and recommendations (Priority: P2)

A telecom security professional asks for a threat explanation, incident-response guidance, mitigation recommendations, an attack-surface comparison, or an executive briefing and receives a concise, evidence-linked response.

**Why this priority**: These are the analysis outputs explicitly requested by the capstone statement.

**Independent Test**: Ask a question requesting a comparison or recommendation; confirm the answer identifies relevant retrieved evidence and does not imply the assistant performed a network action.

**Acceptance Scenarios**:

1. **Given** relevant source passages are available, **When** the user asks for a threat explanation or mitigation recommendation, **Then** the response summarizes the evidence and includes citations.
2. **Given** the user asks to compare two attack surfaces, **When** evidence for one or both is missing, **Then** the assistant states the limitation rather than fabricating a comparison.

### User Story 3 - Prepare the reference knowledge base (Priority: P3)

A project operator runs the application with the supplied PDF and a Gemini API key; the application extracts page-aware passages and reuses a local index on subsequent runs.

**Why this priority**: Reliable, repeatable local retrieval avoids external embedding quota and supports the user journeys.

**Independent Test**: Build the local index from the supplied PDF, verify passages preserve source page numbers, then restart and verify the stored index is reused while the PDF remains unchanged without calling a model API.

**Acceptance Scenarios**:

1. **Given** the PDF is available and readable, **When** the application starts, **Then** it indexes extracted text and reports meaningful setup errors if indexing fails.
2. **Given** a valid index exists for the unchanged PDF, **When** the application starts again, **Then** it loads the saved index without calling Gemini.

## Edge Cases

- The PDF is absent, unreadable, encrypted, or contains no extractable text.
- A page has no extractable text; other pages remain indexable and citations retain original page numbers.
- The API key is missing or the model service returns an error; the UI explains the issue and does not return a fabricated answer.
- A question is blank or retrieval yields no usable passages.
- The PDF changes after indexing; the stale index is rebuilt.
- Retrieved source text contains instructions; it is treated only as quoted reference evidence.

## Requirements

### Functional Requirements

- **FR-001**: The application MUST accept natural-language telecom security questions through a browser interface.
- **FR-002**: The application MUST extract text from the supplied PDF while preserving one-based page numbers.
- **FR-003**: The application MUST retrieve relevant passages locally using SQLite full-text BM25 search before requesting a generated response.
- **FR-004**: The application MUST show source passages and page references alongside each answer.
- **FR-005**: The application MUST base responses only on retrieved evidence and disclose insufficient evidence.
- **FR-006**: The application MUST support threat explanations, mitigation recommendations, comparisons, and executive summaries through the question interface.
- **FR-007**: The application MUST cache the PDF index locally and rebuild it when the source PDF changes.
- **FR-008**: The application MUST read API credentials from environment configuration and MUST NOT store them in source code or the index.
- **FR-009**: The application MUST display an advisory-use limitation and MUST NOT perform actions against telecom infrastructure.
- **FR-010**: The project MUST include repeatable local tests for deterministic PDF chunking and retrieval behavior without live API calls.

### Key Entities

- **Document**: The source PDF, its identity, and content fingerprint.
- **Passage**: Extracted text and source page number, indexed locally for full-text search.
- **Query**: User's natural-language question and its locally tokenized search terms.
- **Answer**: Generated response and the supporting retrieved passages.
- **Index**: Local FTS5/BM25 cache of passages tied to one document fingerprint and index version.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every successful answer displays at least one source passage with a page number.
- **SC-002**: A question whose source evidence is insufficient receives an explicit evidence-gap response.
- **SC-003**: Reopening the app with an unchanged PDF reuses the saved local index without making embedding API requests.
- **SC-004**: The deterministic test suite validates chunk page attribution, chunk boundaries, and ranking without requiring a network connection.

## Assumptions

- The supplied `project-requirement/T-TUT-ICTSS-2020-4-PDF-E.pdf` is the authoritative initial source and contains selectable/extractable text.
- Gemini API access and an API key are available to generate live answers; indexing and retrieval are local.
- Streamlit is the requested low-code browser interface; no authentication or multi-user history is required for this local capstone.
- Generated answers support discovery and education only. Users must verify current operational decisions against authoritative sources and qualified professionals.
- No benchmark or live model accuracy is claimed until an operator performs and records the documented evaluation.
