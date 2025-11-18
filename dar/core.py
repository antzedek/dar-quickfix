# ================================
# dar/core.py — Final v1.0.1 (clean + stable)
# ================================
# • stabilne API
# • czysty kod
# • pełna kompatybilność z resztą modułów
# • dopieszczona logika stabilizacyjna
# ================================

from .branching import split_basic
from .stability import StabilityCore
from .memory import FractalMemory
from .merge import merge_fractal
from .utils import extractive_summary
from typing import Callable, Generator
import uuid

class DAR_QuickFix:
    """
    Główny runtime DAR 4.0 QuickFix.

    • split_basic() → tworzy gałęzie zadania
    • StabilityCore → stabilizacja + pętle + drift
    • FractalMemory → strukturalna pamięć sesji
    • merge_fractal() → fraktalne scalanie wyników
    """

    def __init__(self, model_callable: Callable):
        self.model = model_callable
        self.stability = StabilityCore()
        self.memory = FractalMemory()
        self.session_id = str(uuid.uuid4())

    # ----------------------------------------------------
    # TRYB „RUN” — standardowa, jednorazowa odpowiedź
    # ----------------------------------------------------
    def run(self, prompt: str) -> str:
        branches = split_basic(prompt)
        results = {}

        for b in branches:
            context = b["context"]

            # Rekonstrukcja pamięci jeśli mamy historię
            if len(self.memory.memory) > 3:
                context += "\n\n" + self.memory.reconstruct()

            # Model może być funkcją albo obiektem .generate()
            raw = (
                self.model(context)
                if callable(self.model)
                else self.model.generate(context)
            )

            output = str(raw)

            # 1. Detekcja pętli → skrócenie
            if self.stability.loop_detected(output):
                output = self.stability.rewind(output)

            # 2. Drift semantyczny → porządkowanie
            if self.stability.drift_detected(output, b["context"]):
                output = self.stability.stabilize(output)

            # 3. Zachowanie tożsamości z głównym celem
            output = self.stability.realign_identity(output, prompt)

            # 4. Zapis do pamięci
            self.memory.push(goal=b["context"], decision=output[:500])
            results[b["id"]] = output

        return merge_fractal(results)

    # ----------------------------------------------------
    # TRYB "STREAM" — strumieniowanie wyników (OpenAI, Groq, Ollama)
    # ----------------------------------------------------
    def stream(self, prompt: str) -> Generator[str, None, None]:
        branches = split_basic(prompt)
        partials = {}

        for b in branches:
            context = b["context"]

            if len(self.memory.memory) > 3:
                context += "\n\n" + self.memory.reconstruct()

            partial = ""

            for chunk in self.model(context, stream=True):
                partial += chunk

                # Co X znaków sprawdzamy stabilność narastającego outputu
                if len(partial) % 256 < len(chunk):
                    if self.stability.loop_detected(partial):
                        partial = self.stability.rewind(partial)

                    if self.stability.drift_detected(partial, b["context"]):
                        partial = self.stability.stabilize(partial)

                yield chunk

            partials[b["id"]] = partial
            self.memory.push(goal=b["context"], decision=partial[:500])

        # Po zakończeniu wszystkich gałęzi można scalić wynik:
        # yield "\n\n=== FRACTAL MERGE ===\n\n" + merge_fractal(partials)
