# Research: Telecom Threat Intelligence Assistant

## Decisions

### Use Gemini embeddings and generation

- **Decision**: Use Google's `google-genai` SDK for embedding and generated responses, with `gemini-embedding-001` and `gemini-2.5-flash`.
- **Reason**: One provider supplies both semantic retrieval and response generation, minimizing integration code and model-provider configuration.
- **Embedding roles**: Use `RETRIEVAL_DOCUMENT` for source passages and `RETRIEVAL_QUERY` for user questions; cap generated answers at 512 tokens.
- **Alternative considered**: Local TF-IDF or BM25. This removes embedding API calls but weakens semantic search for a capstone whose objective explicitly asks for relevant threat insights. It can be added later if offline operation becomes a requirement.

### Use a small local SQLite index

- **Decision**: Store each source passage and serialized embedding in a local SQLite database.
- **Reason**: SQLite is part of Python's standard library, needs no separate service, and makes a PDF fingerprint-based reusable cache straightforward.
- **Alternative considered**: Recompute embeddings on every app launch. This wastes API calls and startup time.

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
| Provider unavailable, quota exceeded, or key invalid | Surface configuration/API errors; never substitute an ungrounded answer |
| Retrieved evidence is incomplete or misleading | Instruct the model to cite retrieved pages and state evidence gaps; show passages for user verification |
| PDF is scanned or extraction returns little text | Fail with a clear message; OCR is explicitly outside v1 |
| Security guidance becomes outdated | Identify the source/version and warn that the app is not a real-time advisory feed |

## Open Limitations

- The index is local to one machine and is not multi-user storage.
- The supplied PDF is the only initial source; no live vulnerability feed or web retrieval is included.
- Model output quality and retrieval relevance require a live, human-reviewed evaluation with a configured API key.
