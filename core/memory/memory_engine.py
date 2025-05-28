# core/memory/memory_engine.py

import numpy as np
from typing import List, Dict
from openai import OpenAI

client = OpenAI()

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def calculate_alignment_score(memory: List[Dict[str, str]]) -> float:
    if not memory:
        return 0.0

    similarities = []
    for entry in memory:
        thought = entry.get("thought", "").strip()
        response = entry.get("response", "").strip()
        if not thought or not response:
            continue
        try:
            thought_emb = client.embeddings.create(input=thought, model="text-embedding-3-small").data[0].embedding
            response_emb = client.embeddings.create(input=response, model="text-embedding-3-small").data[0].embedding
            similarity = cosine_similarity(thought_emb, response_emb)
            similarities.append(similarity)
        except Exception:
            continue

    if not similarities:
        return 0.0

    return round(float(np.mean(similarities)), 3)
