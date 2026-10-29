# Telecom Threat Intelligence Assistant

A compact Retrieval-Augmented Generation (RAG) capstone that answers telecom cybersecurity questions using the supplied ITU-T *Security in Telecommunications and Information Technology* reference PDF. Answers include retrieved excerpts and page numbers so users can verify claims in the source.

## What it does

- Extracts page-aware passages from the supplied PDF.
- Uses SQLite FTS5/BM25 to retrieve relevant passages locally without Gemini embedding requests.
- Uses Gemini to explain threats, summarize guidance, compare topics, and suggest mitigations from retrieved evidence.
- Displays source passages and page references with each answer.
- Caches a full-text index locally in SQLite and rebuilds it if the PDF changes.

The assistant is advisory and not a real-time threat feed, incident-response tool, or replacement for expert review. Questions and retrieved excerpts are sent to Gemini for answer generation; do not enter sensitive operational data.

## Run locally

Requires Python 3.10+ and a Gemini API key for answer generation. PDF indexing and retrieval are local and do not consume Gemini embedding quota.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `GOOGLE_API_KEY` in `.env`, then run:

```powershell
streamlit run app.py
```

The app indexes the provided PDF on its first run; the local cache is stored in `.cache\` and is not committed. See [the quickstart](specs/001-threat-intelligence-assistant/quickstart.md) for details.

## Tests

```powershell
python -m unittest discover -s tests -v
```

The unit tests do not require a key or make live API calls.

## Project documentation

- [Capstone report](docs/capstone-report.md)
- [Project charter](docs/PROJECT_CHARTER.md)
- [Specify feature](specs/001-threat-intelligence-assistant/spec.md)
- [Implementation plan](specs/001-threat-intelligence-assistant/plan.md)
- [Research decisions](specs/001-threat-intelligence-assistant/research.md)
- [Quickstart](specs/001-threat-intelligence-assistant/quickstart.md)

The project uses the existing Specify/Spec Kit setup; its constitution and feature artifacts define scope, requirements, design, and implementation tasks.
