# Capstone Report: Telecom Threat Intelligence Assistant

## 1. Problem Statement

Telecom networks face security threats across distributed infrastructure, signaling systems, and high-value data flows. Security teams must search lengthy technical material to understand threats, vulnerabilities, mitigation recommendations, and incident-response practices. Manual search can delay analysis.

This project builds a small Retrieval-Augmented Generation (RAG) assistant that accepts natural-language questions, retrieves relevant passages from the supplied ITU-T *Security in Telecommunications and Information Technology (7th Edition)* PDF, and generates a concise answer with traceable page references.

## 2. Objectives and Scope

- Retrieve relevant information from the supplied ITU-T reference.
- Explain and summarize complex telecom security topics.
- Provide evidence-based recommendations, comparisons, and executive-style summaries.
- Show the source passages and PDF page numbers for user verification.
- Avoid unsupported claims and clearly state when retrieved evidence is insufficient.

The prototype does not ingest live advisories, conduct network scans, or perform incident-response actions. It is an information-discovery aid, not operational security advice.

## 3. Data

| Item | Description |
|---|---|
| Source | `project-requirement/T-TUT-ICTSS-2020-4-PDF-E.pdf` |
| Document identified by the problem statement | *Security in Telecommunications and Information Technology*, 7th Edition |
| Format | PDF |
| Use | Text extraction, local full-text retrieval, and cited answer generation |
| Limitations | Only this supplied reference is indexed; scanned pages without extractable text are not OCR-processed |

The local index stores passage text and page numbers in SQLite FTS5, plus source SHA-256 and index version metadata. No embeddings, API key, or user-query history are stored.

## 4. System Architecture

```text
User question
     |
     v
Streamlit interface (app.py)
     |
     v
PDF --> pypdf page extraction --> overlapping chunks
                                     |
                           SQLite FTS5 / BM25 index
                                     ^
                                     |
                             User question
                                     |
                            BM25 top-k passages
     |
     v
Gemini grounded response
     |
     v
Answer + page-cited evidence in browser
```

The cache is rebuilt when the PDF fingerprint or local index version changes. Indexing and retrieval make no Gemini embedding requests. Retrieval and text-processing behavior are in `rag.py`; the UI is in `app.py`.

## 5. Methodology

1. Extract selectable text page by page with pypdf.
2. Normalize whitespace and split each page into overlapping 1,400-character chunks while preserving one-based page numbers.
3. Store passage text and page numbers in SQLite FTS5.
4. Rank matching passages with BM25 and select the top five; the local index is reused for an unchanged PDF.
5. Ask `gemini-3.8-flash` to answer only from the retrieved excerpts, cite page markers, identify evidence gaps, and avoid claiming to perform network actions.
7. Display the generated answer and retrieved source text together for verification.

The API key is loaded from `GOOGLE_API_KEY` in the environment or local `.env` file. `.env` and `.cache/` are excluded from Git. Source excerpts and questions are sent to Gemini for answer generation; users must not submit sensitive operational data unless that use is approved. Loading and searching the PDF do not call the embedding endpoint.

## 6. Implementation and Testing

The implementation is a single-page Streamlit app, a compact retrieval module, and a standard-library `unittest` suite. Tests cover PDF page attribution/chunking, empty extraction, BM25 ranking, spelling aliases, no-match handling, and index reuse. They do not call the Gemini service.

### Experimental results

| Experiment | Procedure | Result |
|---|---|---|
| Offline unit tests | `python -m unittest discover -s tests -v` | 4 tests passed, including extraction, page attribution, ranking, index reuse, and source-change rebuild |
| Streamlit startup | Start the app without an API key and request the health and home endpoints | Both endpoints returned HTTP 200; app displays setup guidance until `GOOGLE_API_KEY` is configured |
| Live retrieval quality | Ask a reviewed set of telecom-security questions and inspect citations against the PDF | Not run in this environment; requires a user-provided Gemini API key |
| Latency and API cost | Measure indexing and question-answer calls with a configured key | Not measured; depends on model service, quota, network, and document extraction |

No live model accuracy, latency, or cost measurements are claimed. For a formal evaluation, record per-query relevance, citation correctness, groundedness, latency, and API cost for a small human-reviewed question set.

### Suggested evaluation questions

1. Explain a signaling threat described in the reference.
2. Summarize the document's incident-response guidance.
3. Compare two attack surfaces only if both are covered by retrieved passages.
4. Ask about a topic absent from the source and verify the assistant identifies the evidence gap.

For each query, record retrieved page numbers, whether the excerpt supports the answer, unsupported statements, and reviewer notes. Do not treat generated answers as ground truth.

## 7. Threat Analysis and Recommendation Behavior

The assistant is designed to retrieve source material that can support threat explanations, mitigation suggestions, comparisons, and concise briefings. Actual threat findings are query-dependent and must be checked against the retrieved excerpts and current authoritative guidance. This report does not invent example findings or claim that a live Gemini evaluation has been performed.

Recommendations are presented as informational summaries of the supplied document. They are not validated against a telecom operator's specific architecture or current threat environment, and the application cannot enact them.

## 8. Screenshots and Demo Evidence

No configured Gemini key was supplied for this project session, so no live answer screenshot is included. To produce reproducible screenshots:

1. Follow [the quickstart](../specs/001-threat-intelligence-assistant/quickstart.md).
2. Run `streamlit run app.py` and submit a question from the evaluation list.
3. Capture the answer and expanded **Retrieved evidence** section, ensuring page references are visible.
4. Save screenshots in `docs/screenshots/` and record the question and date in the evaluation table.

This avoids presenting a fabricated or unverified model response as experimental evidence.

## 9. Limitations and Future Work

- One PDF only; no real-time advisories, vendor bulletins, or source freshness checks.
- PDF text extraction may omit scanned/image-only pages or complex table layouts.
- Embedding similarity may retrieve incomplete context; no benchmarked relevance threshold is applied.
- Generated answers can be incomplete or incorrect despite grounding instructions.
- Gemini access requires network connectivity, an API key, and available quota.
- Future evaluation should use a curated question/answer set, human citation review, retrieval precision/recall, and measured latency/cost.

## 10. Run and Verify

- Setup and run: [quickstart](../specs/001-threat-intelligence-assistant/quickstart.md)
- Tests: `python -m unittest discover -s tests -v`
- Scope and acceptance criteria: [feature specification](../specs/001-threat-intelligence-assistant/spec.md)
