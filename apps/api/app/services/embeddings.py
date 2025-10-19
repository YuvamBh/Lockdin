from typing import Iterable, List
from openai import OpenAI
from ..core.config import settings

_client = None
if settings.openai_api_key:
    _client = OpenAI(api_key=settings.openai_api_key)

def embed_texts(texts: Iterable[str]) -> List[List[float]]:
    texts = [t.strip() for t in texts if t and t.strip()]
    if not texts:
        return []
    if not _client:
        # Safe fallback in dev if key is missing: return zero-vectors (same dim expected later).
        return [[0.0] * 1536 for _ in texts]
    resp = _client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in resp.data]
