"""
jaydroid — a beginner-friendly Python wrapper for simulating Android actions via ADB.

Example:
    import jaydroid

    jaydroid.tap(500, 800)
"""

from .core import *

__version__ = "0.1.0"

__all__ = ["tap"]