# Data Model: Telecom Threat Intelligence Assistant

## Document

The configured source PDF.

| Field | Type | Meaning |
|---|---|---|
| `path` | local path | Location of the supplied ITU-T PDF |
| `sha256` | text | Fingerprint used to invalidate stale indexes |

## Passage

An extracted page-aware text chunk.

| Field | Type | Meaning |
|---|---|---|
| `id` | integer | Local SQLite key |
| `page` | integer | One-based page in the PDF |
| `content` | text | Extracted text for retrieval and evidence display |
| `embedding` | JSON array of floats | Gemini semantic representation |

## Index Metadata

Stored in SQLite alongside passages.

| Field | Type | Meaning |
|---|---|---|
| `source_sha256` | text | Fingerprint of indexed PDF |
| `embedding_model` | text | Model used for passage embeddings |

## Query and Answer

Ephemeral request data; not persisted.

| Field | Type | Meaning |
|---|---|---|
| `question` | text | User's question |
| `answer` | text | Generated evidence-grounded response |
| `sources` | Passage list | Ranked excerpts shown with page numbers |

## Relationships and Invariants

- One index belongs to exactly one source fingerprint and embedding model.
- Every passage has a positive page number and non-empty content.
- Each answer is generated from its displayed retrieved passages.
- API credentials are configuration only and are never stored in the database.
