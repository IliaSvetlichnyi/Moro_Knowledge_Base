import argparse
import json
import os
from pathlib import Path
from unstructured.partition.auto import partition

"""Parse raw files into structured elements (JSON per doc)."""


def parse_file(path: Path):
    elements = partition(filename=str(path))
    text = "\n".join([el.text for el in elements if getattr(el, "text", None)])
    return {
        "doc_id": path.stem,
        "source_path": str(path),
        "text": text,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    os.makedirs(args.output, exist_ok=True)
    in_dir = Path(args.input)
    for p in in_dir.rglob("*"):
        if p.is_file():
            try:
                rec = parse_file(p)
                out = Path(args.output) / f"{p.stem}.json"
                with open(out, "w", encoding="utf-8") as f:
                    json.dump(rec, f, ensure_ascii=False)
                print("parsed:", p)
            except Exception as e:
                print("failed:", p, e)


if __name__ == "__main__":
    main()

