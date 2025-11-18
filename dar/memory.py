# ================================
# dar/memory.py — Final v1.0.1
# ================================
# • lekka, deterministyczna pamięć fraktalna
# • format zgodny z core.py (merge + kontekst)
# • zapis 10 ostatnich decyzji — idealnie pod stabilne LLM
# ================================

from collections import deque
from typing import Dict, List

class FractalMemory:
    """
    Minimalistyczna pamięć fraktalna (stateless → stateful).

    Każdy wpis ma:
    • goal — cel gałęzi
    • decision — skrót decyzji gałęzi
    • exit — sposób zakończenia (merge / rewind / stabilize)

    Pamięć działa jak rolling window (maxlen=25).
    """

    def __init__(self, max_items: int = 25):
        self.memory = deque(maxlen=max_items)

    # ----------------------------------------------------
    # PUSH — dodanie nowego wpisu
    # ----------------------------------------------------
    def push(self, goal: str, decision: str = "", exit_point: str = "merge"):
        self.memory.append({
            "goal": str(goal).strip()[:300],
            "decision": str(decision).strip()[:800],
            "exit": exit_point
        })

    # ----------------------------------------------------
    # RECONSTRUCT — odbudowa kontekstu
    # ----------------------------------------------------
    def reconstruct(self) -> str:
        """
        Zwraca czytelny blok pamięci:

        ### FRACTAL MEMORY — CONTEXT REBUILD ###
        GOAL: ...
        DECISION: ...
        EXIT: ...
        """

        if not self.memory:
            return ""

        lines = ["### FRACTAL MEMORY — CONTEXT REBUILD ###"]

        # ostatnie 10 wpisów → w pełni wystarcza modelowi
        for item in list(self.memory)[-10:]:
            lines.append(f"GOAL: {item['goal']}")
            if item["decision"]:
                lines.append(f"DECISION: {item['decision']}")
            lines.append(f"EXIT: {item['exit']}\n")

        return "\n".join(lines)
