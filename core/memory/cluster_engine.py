# core/memory/cluster_engine.py

from openai import OpenAI
from sklearn.cluster import KMeans
from typing import List, Dict
import numpy as np

# Initialize OpenAI client
client = OpenAI()

def get_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for a given thought.
    Falls back to zero vector on error.
    """
    try:
        result = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return result.data[0].embedding
    except Exception:
        return [0.0] * 1536  # Fallback for failed embedding

def cluster_thoughts(memory: List[Dict[str, str]], num_clusters: int = 5) -> Dict[int, List[Dict[str, str]]]:
    """
    Cluster memory entries based on semantic similarity of thoughts.
    Returns a dict of {cluster_id: [entries]}.
    """
    valid_entries = [entry for entry in memory if entry.get("thought")]
    if len(valid_entries) < 2:
        return {0: valid_entries} if valid_entries else {}

    embeddings = [get_embedding(entry["thought"]) for entry in valid_entries]
    n_clusters = min(num_clusters, len(valid_entries))

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(embeddings)

    clusters = {i: [] for i in range(n_clusters)}
    for i, label in enumerate(labels):
        clusters[label].append(valid_entries[i])

    return clusters

def generate_cluster_label(thoughts: List[str]) -> str:
    """
    Generate a concise label for a semantic cluster using GPT-4.
    """
    if not thoughts:
        return "Unlabeled"

    preview = "\n- " + "\n- ".join(thoughts[:10])  # Limit input to avoid token overflow
    prompt = (
        "These are personal reflections grouped by semantic similarity:\n"
        f"{preview}\n\n"
        "Provide a single concise label or tag for this cluster (e.g., #loop, #growth, #conflict):"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a concise cluster labeling assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Unknown"
