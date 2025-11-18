# ================================
# dar/__init__.py — Final v1.0.1
# ================================
# Public API DAR QuickFix
# ================================

from .core import DAR_QuickFix
from .branching import split_basic
from .stability import StabilityCore
from .memory import FractalMemory

__version__ = "1.0.1"
__all__ = [
    "DAR_QuickFix",
    "split_basic",
    "StabilityCore",
    "FractalMemory",
]

