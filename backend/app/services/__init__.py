"""
Services Package
Author: Sharmeen Asif
"""

# Optional qdrant import - only if dependencies are available
try:
    from .qdrant import qdrant_service
    __all__ = ["qdrant_service"]
except (ImportError, ModuleNotFoundError):
    qdrant_service = None
    __all__ = []
