from typing import List
from src.llm.openrouter_client import OpenRouterClient
from src.config import settings

PROMPT_TMPL = (
    "You are a precise assistant. Use ONLY the CONTEXT to answer. "
    "If the answer is not in the context, say you don't know.\n\n"
    "CONTEXT:\n{context}\n\nQUESTION: {q}\n\nAnswer concisely."
)


def format_context(chunks: List[dict]) -> str:
    lines = []
    for i, c in enumerate(chunks, 1):
        src = c.get("meta", {}).get("source_path", "unknown")
        lines.append(
            f"[{i}] (doc={c.get('doc_id')}, chunk={c.get('chunk_id')}) {c['content']}\n-- source: {src}")
    return "\n\n".join(lines)


def generate_answer(query: str, chunks: List[dict]) -> dict:
    client = OpenRouterClient()
    ctx = format_context(chunks)
    prompt = PROMPT_TMPL.format(context=ctx, q=query)
    answer = client.chat(
        system="Answer truthfully and only with the provided context.",
        user=prompt,
        max_new_tokens=settings.MAX_NEW_TOKENS,
        temperature=settings.TEMPERATURE,
    )
    return {"answer": answer, "sources": [{"doc_id": c["doc_id"], "chunk_id": c["chunk_id"], "meta": c.get("meta", {})} for c in chunks]}

