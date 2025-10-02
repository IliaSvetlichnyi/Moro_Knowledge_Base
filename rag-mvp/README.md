# RAG MVP (Mac + OpenRouter)

## Prereqs
- macOS with Python 3.10+
- Docker Desktop
- OpenRouter API key: https://openrouter.ai/

## 1. Bootstrap services
```bash
docker compose up -d
# wait ~5–10s, then initialize schema
psql postgres://postgres:postgres@localhost:5432/rag -f scripts/init_db.sql
```

## 2. Create Python venv & install deps
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure environment
```bash
cp .env.sample .env
# edit .env and set OPENROUTER_API_KEY
```

## 4. Ingest & index your docs

Place PDFs/DOCX/HTML in ./data_raw (create folder). Then:
```bash
python -m src.ingest.parse --input ./data_raw --output ./data_parsed
python -m src.ingest.chunk --input ./data_parsed --output ./data_chunks.jsonl
python -m src.ingest.index --chunks ./data_chunks.jsonl
```

## 5. Run API
```bash
uvicorn src.api.server:app --reload --port 8001
```

## 6. Ask a question
```bash
curl -X POST http://localhost:8001/ask \
  -H 'Content-Type: application/json' \
  -d '{"query":"What are the key points from the information security policy?"}'
```

## Notes
- Embeddings default: BAAI/bge-small-en (fast on CPU). You can switch to BAAI/bge-base-en-v1.5.
- Reranker is optional; disable with RERANKER_ENABLED=false in .env if slow.
- If unstructured needs system deps on macOS: `brew install libmagic poppler tesseract`.

