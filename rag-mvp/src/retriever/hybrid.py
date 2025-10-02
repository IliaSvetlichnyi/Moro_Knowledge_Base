from typing import List, Dict
import numpy as np
from src.db.connection import get_engine
from src.db import crud
from src.models.embedder import Embedder
from src.models.reranker import Reranker
from src.config import settings


class HybridRetriever:
    def __init__(self):
        self.engine = get_engine()
        self.embedder = Embedder()
        self.reranker = Reranker()

    def retrieve(self, query: str) -> List[Dict]:
        qvec = self.embedder.encode_one(query)
        dense = crud.dense_search(self.engine, qvec, settings.DENSE_TOP_K)
        bm25 = crud.bm25_search(self.engine, query, settings.BM25_TOP_K)
        # merge + dedupe by id preserving order
        by_id = {}
        for r in dense + bm25:
            by_id.setdefault(r["id"], r)
        merged = list(by_id.values())
        reranked = self.reranker.rerank(query, merged, settings.RERANK_TOP_K)
        return reranked

