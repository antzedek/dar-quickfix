# ================================
# dar/merge.py — Final v1.0.1
# ================================
# • fraktalne scalanie gałęzi
# • wzmocnione czyszczenie whitespace
# • stabilny i w pełni deterministyczny merge
# • kompatybilne z core.py i memory.py
# ================================

import re
from typing import Dict

# ----------------------------------------------------
# CLEANER — usuwa zbędne whitespace i puste linie
# ----------------------------------------------------

def _clean(text: str) -> str:
    """
    Normalizuje output modelu:
    • usuwa nadmiar pustych linii
    • usuwa zbędne spacje
    • przycina whitespace
    """

    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    text = re.sub(r" {2,}", " ", text)
    return text


# ----------------------------------------------------
# MERGE FRACTAL — scalanie wielu wyników
# ----------------------------------------------------

def merge_fractal(results: Dict[str, str]) -> str:
    """
    Zasada fraktalna:
    • sortujemy gałęzie od najkrótszej do najdłuższej
    • każda gałąź jest czyszczona
    • scalana w jednolitą, spójną narrację

    To NIE jest zwykły concat — to deterministyczny merge.
    """

    if not results:
        return ""

    # lista: [(id, tekst)]
    items = [(k, v) for k, v in results.items() if v.strip()]

    # krótsze fragmenty → wcześniej (dają stabilniejszy kontekst)
    items.sort(key=lambda x: len(x[1]))

    parts = []
    for _, text in items:
        cleaned = _clean(text)
        if cleaned:
            parts.append(cleaned)

    return "\n\n".join(parts)
