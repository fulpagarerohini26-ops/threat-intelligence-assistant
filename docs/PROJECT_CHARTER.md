# Project Charter

## Project Title

Telecom Threat Intelligence Retrieval & Analysis Assistant

## Purpose

Help telecom security teams locate and understand relevant threat intelligence in the supplied ITU-T *Security in Telecommunications and Information Technology* reference. The assistant uses retrieval-augmented generation to return concise, page-cited explanations.

## Problem

Telecommunications security teams must analyze lengthy reports, advisories, and technical references covering threats, vulnerabilities, incident response, and network protections. Manually searching these documents is time-consuming and can delay understanding. This capstone demonstrates a conversational way to retrieve and summarize the supplied reference.

## Target Users

- Telecom security analysts
- Network security engineers
- Incident-response and risk teams
- Cybersecurity leaders seeking concise briefings

## Scope

### In scope

- Natural-language question answering over the supplied ITU-T PDF.
- Threat explanations, summaries, evidence-based recommendations, comparisons, and executive-style briefings.
- Semantic retrieval and displayed source excerpts with PDF page references.
- Local reusable index and reproducible offline unit tests.

### Out of scope

- Live threat feeds, vulnerability databases, or additional documents.
- Automated scans, configuration changes, or incident-response actions on telecom systems.
- Authentication, multi-user query history, production hosting, and legal or professional advice.

## Data

The initial source is `project-requirement/T-TUT-ICTSS-2020-4-PDF-E.pdf`, provided with the project requirements. The accompanying problem statement identifies it as *Security in Telecommunications and Information Technology (7th Edition)*. Page citations refer to the supplied PDF's page numbering.

## Deliverable

A Python Streamlit application using Gemini embeddings and generation, a local SQLite retrieval cache, focused tests, Specify artifacts, setup instructions, and this capstone report.

## Limitations and Responsible Use

The assistant reflects only the supplied reference and may omit context or produce errors. It is not a real-time advisory service or a substitute for current vendor advisories, official sources, or qualified review. Users must verify important conclusions against the source and current guidance. The system does not execute actions against networks.

## Success Measures

- Successful answers show the retrieved passages and page numbers.
- Insufficient evidence is disclosed rather than filled with invented facts.
- The unchanged reference uses the cached index on later launches.
- Deterministic retrieval and chunking tests pass without network access.

Detailed functional requirements and acceptance scenarios are in the [Specify feature](../specs/001-threat-intelligence-assistant/spec.md).
