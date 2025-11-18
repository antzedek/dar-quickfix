# ================================
# dar/branching.py — Final v1.0.1
# ================================
# • precyzyjne wyodrębnianie podzadań
# • limit gałęzi = 4 (1 główna + 3 poboczne)
# • dopieszczone heurystyki
# • pełna kompatybilność z DAR_QuickFix
# ================================

import uuid
from typing import List, Dict, Any
import re

# ----------------------------------------------------
# Ekstrakcja podzadań z naturalnego języka
# ----------------------------------------------------
def extract_subtasks(prompt: str) -> List[str]:
    """
    Dzieli prompt na maks. 3 podzadania.
    Wyzwalacze: przecinki, średniki, „i”, „oraz”, nowe linie.
    """

    separators = [",", ";", " i ", " oraz ", "\n"]

    for sep in separators:
        if sep in prompt:
            parts = [p.strip() for p in prompt.split(sep)]
            if len(parts) > 1:
                # odfiltrowujemy śmieci i za krótkie elementy
                return [p for p in parts if len(p) > 10][:3]

    return [prompt]


# ----------------------------------------------------
# Podział zadania na gałęzie fraktalne
# ----------------------------------------------------
def split_basic(prompt: str) -> List[Dict[str, Any]]:
    """
    Tworzy listę gałęzi:
    • 1 główna
    • maks. 3 podzadania
    Każda gałąź ma własny kontekst i poziom głębokości (depth).
    """

    from .pwm import get_depth

    depth = get_depth(prompt)
    subtasks = extract_subtasks(prompt)

    branches = []

    # ---------------------
    # GŁÓWNA GAŁĄŹ
    # ---------------------
    branches.append({
        "id": str(uuid.uuid4()),
        "context": prompt,
        "goal": "main_task",
        "depth": depth
    })

    # ---------------------
    # PODGAŁĘZIE (max 3)
    # ---------------------
    for st in subtasks:
        if len(branches) >= 4:
            break

        branches.append({
            "id": str(uuid.uuid4()),
            "context": st,
            "goal": "subtask",
            "depth": max(1, depth - 1)
        })

    return branches
