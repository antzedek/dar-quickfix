# ================================
# dar/stability.py — Final v1.0.1
# ================================
# • w pełni dopieszczony moduł stabilizacyjny
# • wyraźniejsza logika drift/loop/identity
# • język komunikatów dostosowany pod ENG runtime
# • pełna kompatybilność z core.py
# ================================

from .utils import (
    semantic_distance,
    repetition_score,
    enforce_structure,
    extractive_summary,
)

class StabilityCore:
    """
    Główny moduł stabilizacyjny DAR 4.0 QuickFix.

    Odpowiada za:
    • detekcję pętli (Anti‑Loop)
    • detekcję dryfu semantycznego
    • zachowanie tożsamości celu (Identity Alignment)
    • lekką normalizację struktury
    • skracanie odpowiedzi (Rewind Logic)
    """

    def __init__(self):
        self.drift_threshold = 0.38    # >38% odejścia od celu → drift
        self.loop_threshold = 4        # powtarzalność n-gramów >4 → loop
        self.identity_threshold = 0.62 # >62% rozjazdu od celu → przypomnienie

    # ----------------------------------------------------
    # DRIFT DETECTION
    # ----------------------------------------------------
    def drift_detected(self, output: str, reference: str = None) -> bool:
        return semantic_distance(output, reference) > self.drift_threshold

    # ----------------------------------------------------
    # LOOP DETECTION (n-gram)
    # ----------------------------------------------------
    def loop_detected(self, output: str) -> bool:
        return repetition_score(output) > self.loop_threshold

    # ----------------------------------------------------
    # STABILIZATION — light structural cleanup
    # ----------------------------------------------------
    def stabilize(self, output: str) -> str:
        return enforce_structure(output)

    # ----------------------------------------------------
    # REWIND — extractive summarization of the loop
    # ----------------------------------------------------
    def rewind(self, output: str) -> str:
        return extractive_summary(output, top_k=8)

    # ----------------------------------------------------
    # IDENTITY REALIGNMENT — przypomnienie celu głównego
    # ----------------------------------------------------
    def realign_identity(self, output: str, original_goal: str) -> str:
        """
        Jeśli model zaczyna odjeżdżać od celu, dołączamy
        "przypomnienie celu" i kompresujemy output.
        """

        if semantic_distance(output, original_goal) < self.identity_threshold:
            return output

        prefix = (
            "\n\nREMINDER OF MAIN GOAL:\n"
            f"{original_goal}\n"
            "Continue consistently with the stated goal:\n"
        )

        aligned = extractive_summary(output, top_k=5)
        return prefix + aligned
