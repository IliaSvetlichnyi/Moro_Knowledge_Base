from typing import List, Tuple
import numpy as np
from sqlalchemy import text
from sqlalchemy.engine import Engine

# Insert chunk with placeholder embedding
INSERT_SQL = text(
    """
    INSERT INTO docs (doc_id, chunk_id, content, embedding, meta, text_tsv)
    VALUES (:doc_id, :chunk_id, :content, :embedding, :meta, to_tsvector('english', :content))
    RETURNING id
    """
)

# Update embedding for a row
UPDATE_EMB_SQL = text(
    "UPDATE docs SET embedding = :embedding WHERE id = :id"
)

# Dense retrieval (IP distance)
DENSE_SQL = text(
    """
    SELECT id, doc_id, chunk_id, content, meta, (embedding <-> :qvec) AS dist
    FROM docs
    ORDER BY embedding <-> :qvec
    LIMIT :k
    """
)

# BM25-ish full-text retrieval
BM25_SQL = text(
    """
    SELECT id, doc_id, chunk_id, content, meta,
           ts_rank_cd(text_tsv, plainto_tsquery('english', :q)) AS rank
    FROM docs
    WHERE plainto_tsquery('english', :q) @@ text_tsv
    ORDER BY rank DESC
    LIMIT :k
    """
)


def insert_chunk(engine: Engine, doc_id: str, chunk_id: int, content: str, embedding: np.ndarray, meta: dict) -> int:
    with engine.begin() as conn:
        rid = conn.execute(INSERT_SQL, {
            "doc_id": doc_id,
            "chunk_id": chunk_id,
            "content": content,
            "embedding": embedding.tolist(),
            "meta": meta
        }).scalar_one()
        return rid


def update_embedding(engine: Engine, row_id: int, embedding: np.ndarray):
    with engine.begin() as conn:
        conn.execute(UPDATE_EMB_SQL, {
                     "id": row_id, "embedding": embedding.tolist()})


def dense_search(engine: Engine, qvec: np.ndarray, k: int):
    with engine.begin() as conn:
        rows = conn.execute(
            DENSE_SQL, {"qvec": qvec.tolist(), "k": k}).mappings().all()
        return [dict(r) for r in rows]


def bm25_search(engine: Engine, q: str, k: int):
    with engine.begin() as conn:
        rows = conn.execute(BM25_SQL, {"q": q, "k": k}).mappings().all()
        return [dict(r) for r in rows]

