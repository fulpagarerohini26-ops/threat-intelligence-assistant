"""Streamlit interface for the telecom threat intelligence assistant."""

import os
import sqlite3
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

from rag import answer_question, ensure_index

ROOT = Path(__file__).resolve().parent
SOURCE_PDF = ROOT / "project-requirement" / "T-TUT-ICTSS-2020-4-PDF-E.pdf"
INDEX_DB = ROOT / ".cache" / "threat-intelligence.sqlite3"

load_dotenv(ROOT / ".env")
st.set_page_config(page_title="Telecom Threat Intelligence Assistant", page_icon="🛡️")
st.title("Telecom Threat Intelligence Assistant")
st.caption(
    "Ask questions about the supplied ITU-T reference. Answers are advisory; "
    "verify important findings in the source and current authoritative guidance. "
    "Questions and retrieved excerpts are sent to Gemini; do not enter sensitive data."
)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key or api_key == "replace-with-your-gemini-api-key":
    st.error("Set GOOGLE_API_KEY in your environment or local .env file to continue.")
    st.stop()
if not SOURCE_PDF.is_file():
    st.error(f"Reference PDF not found: {SOURCE_PDF}")
    st.stop()

client = genai.Client(api_key=api_key)
try:
    rebuilt = ensure_index(SOURCE_PDF, INDEX_DB, client)
except (APIError, OSError, ValueError, RuntimeError, sqlite3.Error) as error:
    st.error(f"Could not prepare the reference index: {error}")
    st.stop()

if rebuilt:
    st.success("Reference indexed and cached locally.")
else:
    st.caption("Using the cached index for the unchanged reference PDF.")

with st.form("question_form"):
    question = st.text_input(
        "Question",
        placeholder="How should a telecom operator assess signaling security risks?",
    )
    submitted = st.form_submit_button("Ask")

if submitted:
    try:
        answer, sources = answer_question(question, INDEX_DB, client)
    except (APIError, OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        st.error(f"Could not answer the question: {error}")
    else:
        st.subheader("Answer")
        st.markdown(answer)
        with st.expander("Retrieved evidence"):
            for source in sources:
                st.markdown(f"**Page {source['page']}**")
                st.write(source["content"])
