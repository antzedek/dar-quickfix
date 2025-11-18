# ================================
# dar/utils.py — Final v1.0.1
# ================================
# • lazy-load SentenceTransformer (szybszy import)
# • czyste funkcje pomocnicze
# • stabilne i przewidywalne API
# • zoptymalizowane wyciąganie streszczeń i dystansu semantycznego
# ================================

import re
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

# ----------------------------------------------------
# Lazy-load model (duży boost szybkości przy imporcie)
# ----------------------------------------------------

_emb_model = None

def _get_emb_model():
    global _emb_model
    if _emb_model is None:
        _emb_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    return _emb_model


# ----------------------------------------------------
# SEMANTIC DISTANCE
# ----------------------------------------------------

def semantic_distance(a: str, b: str = None) -> float:
    """
    Zwraca wartość 0–1:
    • 0 → identyczne
    • 1 → maksymalnie różne

    Używane do detekcji: drift, identity alignment.
    """

    b = b or a

    if not a.strip() or not b.strip():
        return 1.0

    model = _get_emb_model()
    texts = [a[-1024:], b[-1024:]]  # limit, żeby nie mielić 100k tokenów
    embeds = model.encode(texts, convert_to_tensor=False)

    norm_a = np.linalg.norm(embeds[0])
    norm_b = np.linalg.norm(embeds[1])

    if norm_a == 0 or norm_b == 0:
        return 1.0

    return 1 - np.dot(embeds[0], embeds[1]) / (norm_a * norm_b)


# ----------------------------------------------------
# REPETITION SCORE — detekcja pętli
# ----------------------------------------------------

def repetition_score(text: str, ngram: int = 6) -> int:
    """
    Zwraca maksymalną liczbę powtórzeń 6-gramów.
    Służy do wykrywania pętli typu "model kręci w kółko".
    """

    words = re.findall(r"\w+", text.lower())

    if len(words) < ngram * 3:
        return 0

    ngrams = [" ".join(words[i:i+ngram]) for i in range(len(words) - ngram + 1)]
    counts = {}

    for g in ngrams:
        counts[g] = counts.get(g, 0) + 1

    return max(counts.values(), default=0)


# ----------------------------------------------------
# STRUCTURE NORMALIZATION — lekkie porządkowanie outputu
# ----------------------------------------------------

def enforce_structure(text: str) -> str:
    """
    Czyści powtórzenia linii i usuwa zbędne whitespace.
    Zostawia ostatnie 150 linii (wystarczające dla dużych promptów).
    """

    lines = [l.rstrip() for l in text.split("\n") if l.strip()]
    return "\n".join(lines[-150:])


# ----------------------------------------------------
# EXTRACTIVE SUMMARY — skracanie outputu do najważniejszych zdań
# ----------------------------------------------------

def extractive_summary(text: str, top_k: int = 6) -> str:
    """
    Bardzo lekka ekstrakcja najważniejszych zdań.
    Nie używa żadnej logiki generacyjnej — 100% deterministyczne.
    """

    # dzielimy bezpiecznie po . ! ?
    sentences = re.split(r"[.!?]\s+", text.strip())

    if len(sentences) <= top_k:
        return text

    model = _get_emb_model()
    embeds = model.encode(sentences)

    centroid = embeds.mean(axis=0)
    distances = np.linalg.norm(embeds - centroid, axis=1)

    top_idx = np.argsort(distances)[-top_k:][::-1]
    selected = [sentences[i] for i in sorted(top_idx)]

    return " ".join(selected)
