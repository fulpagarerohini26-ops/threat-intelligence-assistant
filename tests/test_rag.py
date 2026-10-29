import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from rag import answer_question, cosine_similarity, ensure_index, extract_chunks, retrieve


class FakeModels:
    def __init__(self):
        self.embed_calls = 0
        self.embed_tasks = []

    def embed_content(self, model, contents, config):
        self.embed_calls += 1
        self.embed_tasks.append(config["task_type"])
        if isinstance(contents, str):
            contents = [contents]
        vectors = []
        for content in contents:
            text = content.lower()
            vectors.append(
                SimpleNamespace(
                    values=[
                        float("telecom" in text or "question" in text),
                        float("incident" in text),
                    ]
                )
            )
        return SimpleNamespace(embeddings=vectors)

    def generate_content(self, model, contents, config):
        return SimpleNamespace(text="Signaling security is discussed [p. 1].")


class FakeClient:
    def __init__(self):
        self.models = FakeModels()


class RagTests(unittest.TestCase):
    def test_cosine_similarity(self):
        self.assertAlmostEqual(cosine_similarity([1.0, 0.0], [1.0, 1.0]), 2**-0.5)
        self.assertEqual(cosine_similarity([0.0, 0.0], [1.0, 0.0]), 0.0)
        with self.assertRaises(ValueError):
            cosine_similarity([1.0], [1.0, 0.0])

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
                SimpleNamespace(extract_text=lambda: "Telecom security and signaling risks."),
                SimpleNamespace(extract_text=lambda: "Incident response guidance for operators."),
            ]
            client = FakeClient()
            with patch("pypdf.PdfReader") as reader:
                reader.return_value.pages = pages
                self.assertTrue(ensure_index(pdf_path, db_path, client))
                calls_after_build = client.models.embed_calls
                self.assertFalse(ensure_index(pdf_path, db_path, client))

            self.assertEqual(client.models.embed_calls, calls_after_build)
            results = retrieve("telecom question", db_path, client, top_k=1)
            self.assertEqual(results[0]["page"], 1)
            self.assertEqual(client.models.embed_tasks, ["RETRIEVAL_DOCUMENT", "RETRIEVAL_QUERY"])

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
                self.assertTrue(ensure_index(pdf_path, db_path, client))
            refreshed = retrieve("incident", db_path, client, top_k=1)
            self.assertEqual(refreshed[0]["page"], 2)

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
