import argparse
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from src.db.connection import get_engine
from src.db.crud import insert_chunk
from src.config import settings

"""Embed chunks and upsert into Postgres."""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", required=True)
    args = ap.parse_args()

    engine = get_engine()
    model = SentenceTransformer(settings.EMBED_MODEL)

    batch_texts = []
    batch_meta = []

    with open(args.chunks, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            batch_texts.append(rec["content"])
            batch_meta.append(rec)

            if len(batch_texts) >= 64:
                embs = model.encode(batch_texts, normalize_embeddings=True)
                for emb, meta in zip(embs, batch_meta):
                    insert_chunk(engine, meta["doc_id"], meta["chunk_id"], meta["content"], np.array(
                        emb, dtype=float), meta.get("meta", {}))
                batch_texts, batch_meta = [], []

    if batch_texts:
        embs = model.encode(batch_texts, normalize_embeddings=True)
        for emb, meta in zip(embs, batch_meta):
            insert_chunk(engine, meta["doc_id"], meta["chunk_id"], meta["content"], np.array(
                emb, dtype=float), meta.get("meta", {}))

    print("indexing complete")


if __name__ == "__main__":
    main()

