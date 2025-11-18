# ================================
# dar/pwm.py — Final v1.0.1 (fixed + clean)
# ================================
# • naprawiony brakujący import re
# • czytelne heurystyki AJ‑PWM Lite
# • pełna kompatybilność z branching/core
# ================================

import re

# ----------------------------------------------------
# Szacowanie „złożoności” promptu — AJ‑PWM Lite
# ----------------------------------------------------

def estimate_complexity(prompt: str) -> int:
    """
    Funkcja ocenia przybliżoną złożoność promptu.
    Służy do określania głębokości przetwarzania (depth).

    Parametry oceniane:
    • liczba tokenów (bardzo lekka estymacja)
    • liczba linii
    • obecność elementów programistycznych
    """

    tokens = len(prompt.split())
    lines = prompt.count("\n")
    code_keywords = len(re.findall(
        r"\b(def|class|import|function|code|napisz)\b", prompt, re.I
    ))

    return tokens + 30 * lines + 150 * code_keywords


# ----------------------------------------------------
# Wyliczanie głębokości przetwarzania
# ----------------------------------------------------

def get_depth(prompt: str) -> int:
    """
    Na podstawie estimate_complexity() dobiera poziom:

    • 1 — proste
    • 2 — średnie
    • 3 — złożone
    • 4 — bardzo złożone (max)
    """

    c = estimate_complexity(prompt)

    if c < 300:
        return 1
    if c < 800:
        return 2
    if c < 2000:
        return 3
    return 4  # max depth
