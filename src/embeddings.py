from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Callable

MODEL_NAME = "all-MiniLM-L6-v2"

# Load model only once
_model = SentenceTransformer(MODEL_NAME)

def embed_text(text: str, normalize: bool = True) -> np.ndarray:
    """
    Returns a single text embedding for given string.
    """
    if not text:
        return np.zeros(_model.get_sentence_embedding_dimension())

    emb = _model.encode([text], convert_to_numpy=True)[0]

    if normalize:
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm

    return emb


def document_embedding(text: str, chunker: Callable, max_chunk_len: int = 300, pooling: str = "mean") -> np.ndarray:
    """
    Split long text into chunks, embed each, then combine into a single document embedding.
    """
    chunks = chunker(text, max_len=max_chunk_len)

    if not chunks:
        return np.zeros(_model.get_sentence_embedding_dimension())

    chunk_embs = _model.encode(chunks, convert_to_numpy=True)

    if pooling == "mean":
        doc_emb = np.mean(chunk_embs, axis=0)
    elif pooling == "max":
        doc_emb = np.max(chunk_embs, axis=0)
    else:
        raise ValueError("Choose 'mean' or 'max' pooling")

    norm = np.linalg.norm(doc_emb)
    if norm > 0:
        doc_emb = doc_emb / norm

    return doc_emb
