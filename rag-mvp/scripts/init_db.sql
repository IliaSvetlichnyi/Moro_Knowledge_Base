CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS docs (
  id BIGSERIAL PRIMARY KEY,
  doc_id TEXT,
  chunk_id INT,
  content TEXT,
  embedding VECTOR(384), -- 384 dims for bge-small-en; adjust if you change model
  meta JSONB,
  text_tsv tsvector
);

-- HNSW index (IP = inner product for cosine)
CREATE INDEX IF NOT EXISTS idx_docs_embed ON docs USING hnsw (embedding vector_ip_ops);
CREATE INDEX IF NOT EXISTS idx_docs_tsv ON docs USING GIN (text_tsv);

-- Simple RLS skeleton (optional; enable when you add users)
-- ALTER TABLE docs ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY p_all ON docs FOR SELECT USING (true);

