import argparse
import json
import os
from pathlib import Path
from typing import List

from src.config import settings

# naive token-approx by characters; replace with tiktoken if needed


def chunk_text(text: str, max_chars: int, overlap_ratio: float) -> List[str]:
    if not text:
        return []
    step = int(max_chars * (1 - overlap_ratio))
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+max_chars]
        chunks.append(chunk)
        i += step if step > 0 else max_chars
    return chunks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True,
                    help="dir with *.json from parse")
    ap.add_argument("--output", required=True,
                    help="output jsonl file of chunks")
    args = ap.parse_args()

    os.makedirs(Path(args.output).parent, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as out:
        for f in Path(args.input).glob("*.json"):
            rec = json.loads(Path(f).read_text())
            doc_id = rec["doc_id"]
            text = rec.get("text", "")
            chunks = chunk_text(
                text, max_chars=settings.CHUNK_TOKENS*4, overlap_ratio=settings.CHUNK_OVERLAP)
            for idx, c in enumerate(chunks):
                out.write(json.dumps({
                    "doc_id": doc_id,
                    "chunk_id": idx,
                    "content": c,
                    "meta": {"source_path": rec.get("source_path"), "acl": "all"}
                }) + "\n")
    print("wrote chunks to", args.output)


if __name__ == "__main__":
    main()

