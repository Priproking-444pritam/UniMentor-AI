"""
UniMentor AI - Retrieval Layer (RAG)
====================================
Handles:
    1. Loading university documents (PDF and TXT)
    2. Splitting them into overlapping chunks
    3. Converting chunks into embeddings
    4. Storing the embeddings in a FAISS index
    5. Retrieving the most relevant chunks for a question

Each chunk keeps its metadata (file name, page, department)
so that every answer can be traced back to its source.
"""

import os
import re

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DEPARTMENTS,
    DOCUMENTS_FOLDER,
    EMBEDDING_MODEL,
    SIMILARITY_THRESHOLD,
    TOP_K,
)

# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """Collapse whitespace so chunking is predictable."""
    return re.sub(r"\s+", " ", text).strip()


# ============================================================
# DOCUMENT LOADERS
# ============================================================

def load_pdf(file_path, department):
    """Read a PDF page by page and return one record per page."""
    reader = PdfReader(file_path)
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text:
            continue

        text = clean_text(text)

        if text:
            documents.append(
                {
                    "text": text,
                    "source": os.path.basename(file_path),
                    "page": page_number,
                    "department": department,
                }
            )

    return documents


def load_txt(file_path, department):
    """Read a plain text document as a single record."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = clean_text(file.read())

    if not text:
        return []

    return [
        {
            "text": text,
            "source": os.path.basename(file_path),
            "page": 1,
            "department": department,
        }
    ]


def load_documents(base_folder=DOCUMENTS_FOLDER):
    """
    Walk through documents/<department>/ and load every
    supported file found there.
    """
    all_documents = []

    for department in DEPARTMENTS:
        folder = os.path.join(base_folder, department)

        if not os.path.exists(folder):
            continue

        for filename in sorted(os.listdir(folder)):
            path = os.path.join(folder, filename)
            lower_name = filename.lower()

            if lower_name.endswith(".pdf"):
                all_documents.extend(load_pdf(path, department))

            elif lower_name.endswith(".txt"):
                all_documents.extend(load_txt(path, department))

    return all_documents


# ============================================================
# CHUNKING
# ============================================================

def create_chunks(
    documents,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP,
):
    """
    Split each document into overlapping character windows.
    The overlap prevents a sentence from being cut in half
    across two chunks and losing its meaning.
    """
    chunks = []
    metadata = []

    for document in documents:
        text = document["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)
                metadata.append(
                    {
                        "source": document["source"],
                        "page": document["page"],
                        "department": document["department"],
                    }
                )

            start += chunk_size - overlap

    return chunks, metadata


# ============================================================
# VECTOR INDEX
# ============================================================

def build_index(chunks):
    """
    Encode all chunks and store them in a FAISS index.

    Embeddings are normalised, so inner product search
    (IndexFlatIP) is equivalent to cosine similarity.
    """
    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(
    question,
    chunks,
    metadata,
    index,
    department=None,
    top_k=TOP_K,
):
    """
    Return the most relevant chunks for a question.

    If a department is supplied, only chunks belonging to that
    department are returned. Extra candidates are searched
    first because the department filter removes some of them.
    """
    if not chunks:
        return []

    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    search_size = min(top_k * 4, len(chunks))
    scores, indices = index.search(question_embedding, search_size)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        if score < SIMILARITY_THRESHOLD:
            continue

        item_metadata = metadata[idx]

        if department and item_metadata["department"] != department:
            continue

        results.append(
            {
                "text": chunks[idx],
                "metadata": item_metadata,
                "score": float(score),
            }
        )

        if len(results) >= top_k:
            break

    return results


# ============================================================
# CONTEXT BUILDER
# ============================================================

def build_context(results):
    """
    Convert retrieved chunks into a single labelled context
    string, plus a de-duplicated list of sources for the UI.
    """
    context_parts = []
    sources = []
    seen = set()

    for result in results:
        item = result["metadata"]

        context_parts.append(
            f"Source: {item['source']} | "
            f"Page: {item['page']} | "
            f"Department: {item['department']}\n"
            f"Content: {result['text']}"
        )

        key = (item["source"], item["page"])

        if key not in seen:
            seen.add(key)
            sources.append(item)

    return "\n\n---\n\n".join(context_parts), sources
