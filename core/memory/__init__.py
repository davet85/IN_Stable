# core/memory/__init__.py

# This file marks the 'memory' directory as a Python package.
# It also optionally exposes key memory functions at the package level.

from .session_memory import load_session_memory, save_session_memory
from .memory_engine import calculate_alignment_score
