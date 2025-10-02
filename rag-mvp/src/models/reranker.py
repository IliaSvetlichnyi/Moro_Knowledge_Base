from typing import List, Tuple
import torch
from sentence_transformers import CrossEncoder
from src.config import settings


class Reranker:
    def __init__(self):
        self.enabled = settings.RERANKER_ENABLED
        if self.enabled:
            self.model = CrossEncoder(settings.RERANKER_MODEL)

    def rerank(self, query: str, candidates: List[dict], top_k: int) -> List[dict]:
        if not self.enabled:
            return candidates[:top_k]
        pairs = [(query, c["content"]) for c in candidates]
        with torch.inference_mode():
            scores = self.model.predict(pairs)
        scored = [{**c, "score": float(s)} for c, s in zip(candidates, scores)]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

