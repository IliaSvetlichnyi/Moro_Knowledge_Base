import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import settings


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBED_MODEL)

    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True)

    def encode_one(self, text: str) -> np.ndarray:
        return self.encode([text])[0]

