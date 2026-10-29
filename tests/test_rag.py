import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from rag import answer_question, ensure_index, extract_chunks, retrieve


class FakeModels:
    def generate_content(self, model, contents, config):
        return SimpleNamespace(text="Signaling security is discussed [p. 1].")


class FakeClient:
    def __init__(self):
        self.models = FakeModels()


class RagTests(unittest.TestCase):
    def test_extract_chunks_preserves_pages_and_splits_long_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = Path(directory) / "sample.pdf"
            pdf_path.write_bytes(b"mock pdf")
            pages = [
                SimpleNamespace(extract_text=lambda: "Telecom security and signaling. " * 8),
                SimpleNamespace(extract_text=lambda: "Incident response guidance. " * 6),
            ]
            with patch("pypdf.PdfReader") as reader:
                reader.return_value.pages = pages
                chunks = extract_chunks(pdf_path, chunk_size=50, overlap=10)

            self.assertGreater(len(chunks), 2)
            self.assertEqual({chunk["page"] for chunk in chunks}, {1, 2})
            self.assertTrue(all(chunk["content"] for chunk in chunks))

    def test_index_reuse_and_retrieval(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = Path(directory) / "source.pdf"
            db_path = Path(directory) / "index.sqlite3"
            pdf_path.write_bytes(b"mock pdf")
            pages = [
                SimpleNamespace(extract_text=lambda: "Telecom security and signalling risks."),
                SimpleNamespace(extract_text=lambda: "Incident response guidance for operators."),
            ]
            with patch("pypdf.PdfReader") as reader:
                reader.return_value.pages = pages
                self.assertTrue(ensure_index(pdf_path, db_path))
                self.assertFalse(ensure_index(pdf_path, db_path))

            results = retrieve("telecom question", db_path, top_k=1)
            self.assertEqual(results[0]["page"], 1)
            self.assertEqual(retrieve("signaling", db_path, top_k=1)[0]["page"], 1)

            client = FakeClient()
            answer, sources = answer_question("telecom question", db_path, client, top_k=1)
            self.assertIn("[p. 1]", answer)
            self.assertEqual(sources[0]["page"], 1)

            pdf_path.write_bytes(b"updated pdf")
            updated_pages = [
                SimpleNamespace(extract_text=lambda: "Telecom security and signaling risks."),
                SimpleNamespace(extract_text=lambda: "Incident response guidance for operators."),
            ]
            with patch("pypdf.PdfReader") as reader:
                reader.return_value.pages = updated_pages
                self.assertTrue(ensure_index(pdf_path, db_path))
            refreshed = retrieve("incident", db_path, top_k=1)
            self.assertEqual(refreshed[0]["page"], 2)

    def test_no_match_does_not_call_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = Path(directory) / "source.pdf"
            db_path = Path(directory) / "index.sqlite3"
            pdf_path.write_bytes(b"mock pdf")
            with patch("pypdf.PdfReader") as reader:
                reader.return_value.pages = [
                    SimpleNamespace(extract_text=lambda: "Telecom signaling security.")
                ]
                ensure_index(pdf_path, db_path)

            class UnexpectedGeneration:
                def generate_content(self, **kwargs):
                    raise AssertionError("Generation must not run without matching evidence")

            answer, sources = answer_question(
                "volcanic geology", db_path, SimpleNamespace(models=UnexpectedGeneration())
            )
            self.assertIn("couldn't find relevant evidence", answer)
            self.assertEqual(sources, [])

    def test_empty_extraction_fails_clearly(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = Path(directory) / "blank.pdf"
            pdf_path.write_bytes(b"mock pdf")
            with patch("pypdf.PdfReader") as reader:
                reader.return_value.pages = [
                    SimpleNamespace(extract_text=lambda: "  \n ")
                ]
                with self.assertRaisesRegex(ValueError, "No extractable text"):
                    extract_chunks(pdf_path)


if __name__ == "__main__":
    unittest.main()
