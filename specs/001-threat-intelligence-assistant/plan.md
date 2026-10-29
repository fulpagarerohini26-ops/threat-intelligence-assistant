# Implementation Plan: Telecom Threat Intelligence Assistant

**Branch**: `001-threat-intelligence-assistant` | **Date**: 2026-10-29 | **Spec**: [spec.md](./spec.md)

## Summary

Build a compact Streamlit RAG application for the supplied ITU-T telecommunications security PDF. Use Gemini embeddings for retrieval, Gemini generation for evidence-grounded answers, SQLite for a source-fingerprinted local index, and page-level citations in the UI.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Streamlit, `google-genai`, pypdf, python-dotenv  
**Storage**: Local SQLite index under `.cache/`; no user-query persistence  
**Testing**: Python `unittest`; deterministic tests do not call Gemini  
**Target Platform**: Local development on Windows, macOS, or Linux  
**Project Type**: Single-project web app  
**Performance Goals**: Reuse the local index for unchanged source data; make no unsupported latency promise  
**Constraints**: Gemini API key and network are required for initial embedding and generated answers; source PDF must be text-extractable  
**Scale/Scope**: One supplied PDF, one local operator, small top-k retrieval; no authentication or deployment infrastructure

## Constitution Check

- Evidence-first answers and visible citations: **PASS**
- API key excluded from source and index: **PASS**
- Read-only advisory behavior: **PASS**
- Minimal, deterministic tests: **PASS**
- No unapproved technology or operational-action scope: **PASS**

## Project Structure

```text
app.py
rag.py
requirements.txt
.env.example
tests/
└── test_rag.py
docs/
└── capstone-report.md
specs/001-threat-intelligence-assistant/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md
project-requirement/
└── T-TUT-ICTSS-2020-4-PDF-E.pdf
```

**Structure Decision**: Keep one Streamlit entry point and one retrieval module. Avoid a separate backend, vector database service, or abstractions that do not serve the single-document capstone.

## Design

1. Read the supplied PDF with pypdf and split extracted page text into overlapping character chunks.
2. Embed passages using Gemini and store passage text, page, embedding model, and PDF SHA-256 in SQLite.
3. Reuse an index only when both the PDF fingerprint and embedding model match.
4. Embed each question, rank passages by cosine similarity, and pass the top matches to Gemini with a source-only system instruction.
5. Render the answer and page-numbered evidence in Streamlit; explicitly disclose missing setup or evidence.

## Validation Strategy

- Unit tests cover text chunking, page attribution, empty text, and cosine similarity/ranking using local fake embeddings.
- Run the test suite without a model key to prove core logic is offline-testable.
- Live end-to-end question quality requires a user-provided Gemini key and is not claimed by unit tests.
- Follow `quickstart.md` for a manual setup and smoke test.

## Complexity Tracking

No constitution violations. SQLite is chosen over an external vector database to keep the project local and operationally small.
