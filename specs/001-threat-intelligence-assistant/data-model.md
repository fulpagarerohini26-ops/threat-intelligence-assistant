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
| `terms` | SQLite FTS5 tokens | Locally indexed searchable text |

## Index Metadata

Stored in SQLite alongside passages.

| Field | Type | Meaning |
|---|---|---|
| `source_sha256` | text | Fingerprint of indexed PDF |
| `index_version` | text | Local search-index format version |

## Query and Answer

Ephemeral request data; not persisted.

| Field | Type | Meaning |
|---|---|---|
| `question` | text | User's question |
| `answer` | text | Generated evidence-grounded response |
| `sources` | Passage list | Ranked excerpts shown with page numbers |

## Relationships and Invariants

- One index belongs to exactly one source fingerprint and local index version.
- Every passage has a positive page number and non-empty content.
- Each answer is generated from its displayed retrieved passages.
- API credentials are configuration only and are never stored in the database.
