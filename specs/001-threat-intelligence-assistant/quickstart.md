# Quickstart

## Requirements

- Python 3.10 or newer
- The supplied ITU-T PDF at `project-requirement/T-TUT-ICTSS-2020-4-PDF-E.pdf`
- A Gemini API key with access to the configured generation model

## Install

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GOOGLE_API_KEY` to your own key. Do not commit `.env`.

## Run

```powershell
streamlit run app.py
```

On first run, the app extracts the PDF and builds a local SQLite FTS5/BM25 index under `.cache\`; this does not call Gemini or consume embedding quota. Later launches reuse the index unless the PDF changes. Gemini is called only to generate an answer after you submit a question.

Ask a question such as:

- `Explain the telecom security risks discussed for signaling systems.`
- `Summarize incident response recommendations in the reference.`
- `Compare the attack surfaces described for SS7 and SIP.`

The answer and source excerpts with page numbers appear in the browser. Confirm important findings in the original document.

## Test

```powershell
python -m unittest discover -s tests -v
```

Tests do not require a key or make live model requests.

## Reset the local index

Stop Streamlit and remove the specific generated file `.cache\threat_intelligence.sqlite3`; the next run builds it again. The cache is ignored by Git.
