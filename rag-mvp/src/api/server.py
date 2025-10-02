from fastapi import FastAPI
from pydantic import BaseModel
from src.retriever.hybrid import HybridRetriever
from src.llm.generate import generate_answer

app = FastAPI(title="RAG MVP (Mac + OpenRouter)")
retriever = HybridRetriever()


class AskRequest(BaseModel):
    query: str


@app.post("/ask")
def ask(req: AskRequest):
    cands = retriever.retrieve(req.query)
    result = generate_answer(req.query, cands)
    return result


@app.get("/health")
def health():
    return {"ok": True}

