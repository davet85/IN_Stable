# core/memory/memory_engine.py

import numpy as np
from typing import List, Dict
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    if not vec1 or not vec2:
        return 0.0
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

def calculate_entry_alignment(thought: str, response: str) -> float:
    """
    Calculate RCA alignment score between a single thought and response
    using OpenAI text-embedding-3-small vectors.
    """
    try:
        if not thought.strip() or not response.strip():
            return 0.0

        thought_emb = client.embeddings.create(
            input=thought,
            model="text-embedding-3-small"
        ).data[0].embedding

        response_emb = client.embeddings.create(
            input=response,
            model="text-embedding-3-small"
        ).data[0].embedding

        return round(cosine_similarity(thought_emb, response_emb), 3)

    except Exception:
        return 0.0

def calculate_alignment_score(memory: List[Dict[str, str]]) -> float:
    """
    Calculate average RCA alignment score for all memory entries.
    Ignores empty or malformed entries.
    """
    if not memory:
        return 0.0

    scores = []
    for entry in memory:
        thought = entry.get("thought", "").strip()
        response = entry.get("response", "").strip()
        score = calculate_entry_alignment(thought, response)
        if score > 0:
            scores.append(score)

    if not scores:
        return 0.0

    return round(float(np.mean(scores)), 3)
