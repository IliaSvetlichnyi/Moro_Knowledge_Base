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