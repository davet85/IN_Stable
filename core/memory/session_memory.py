import os
import json
from typing import List, Dict, Any

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory_store.json")

def load_session_memory() -> List[Dict[str, Any]]:
    """Load the session memory from disk."""
    if not os.path.exists(MEMORY_FILE):
        return []
    
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_session_memory(memory: List[Dict[str, Any]]) -> None:
    """Save the session memory to disk."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

