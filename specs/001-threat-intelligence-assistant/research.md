# Research: Telecom Threat Intelligence Assistant

## Decisions

### Use local BM25 retrieval and Gemini generation

- **Decision**: Use SQLite FTS5/BM25 locally for indexing and retrieval; use `google-genai` with `gemini-3.8-flash` only for generated answers.
- **Reason**: The free Gemini embedding quota is limited and embedding the full reference during app loading caused `429 RESOURCE_EXHAUSTED`. Local BM25 removes embedding API requests, makes startup repeatable, and uses the SQLite FTS5 support already available in the Python runtime.
- **Trade-off**: Lexical BM25 can miss synonyms that semantic embeddings might retrieve. Users can rephrase when the index reports no relevant evidence.
- **Alternative considered**: Keep Gemini embeddings and add retry/throttling. This would still require multiple quota windows for a large document and make first launch fragile.

### Use a small local SQLite FTS5 index

- **Decision**: Store searchable passage text, page numbers, and source/index metadata in a local SQLite database.
- **Reason**: SQLite FTS5 provides BM25 ranking without an external service or additional dependency. A source fingerprint makes index reuse straightforward.

### Preserve page numbers in passage records

- **Decision**: Extract each PDF page separately and attach its one-based page number to every chunk.
- **Reason**: Page references are required for traceability and can be verified against the source PDF.

### Keep the UI local and minimal

- **Decision**: Use a single Streamlit page for question submission, answer display, and expandable evidence.
- **Reason**: A browser-based demo is easy to run and avoids an API server and separate frontend.

### Keep secrets out of the repository

- **Decision**: Load `GOOGLE_API_KEY` from environment variables or a local `.env` file.
- **Reason**: This supports local setup without committing credentials. The `.env` file is ignored by Git.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| PDF content changes and stale citations survive | Store the source SHA-256 in SQLite and rebuild on mismatch |
| Provider unavailable, generation quota exceeded, or key invalid | Surface configuration/API errors; local indexing/search continue without embedding requests and never substitute an ungrounded answer |
| Retrieved evidence is incomplete or misleading | Instruct the model to cite retrieved pages and state evidence gaps; show passages for user verification |
| PDF is scanned or extraction returns little text | Fail with a clear message; OCR is explicitly outside v1 |
| Security guidance becomes outdated | Identify the source/version and warn that the app is not a real-time advisory feed |

## Open Limitations

- The index is local to one machine and is not multi-user storage.
- The supplied PDF is the only initial source; no live vulnerability feed or web retrieval is included.
- Lexical BM25 can miss semantically related terms; model output quality and retrieval relevance require a live, human-reviewed evaluation.
