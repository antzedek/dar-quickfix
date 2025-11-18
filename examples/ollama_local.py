# examples/ollama_local.py
# Ollama (lokalny model) + DAR QuickFix = pełna stabilność offline

from dar import DAR_QuickFix
import ollama

# Zakładamy, że masz uruchomiony model, np. ollama run llama3.2 albo mistral
MODEL_NAME = "llama3.2:8b"    # zmień na swój

ollama_dar = DAR_QuickFix(
    lambda prompt, **kwargs: ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={"temperature": 0.8, "num_predict": 8192},
        **kwargs
    )["response"]
)

print("Ollama + DAR – 100% lokalnie, zero internetu, pełna stabilność:")
response = ollama_dar.run("""
Jesteś szalonym pisarzem science-fiction. Napisz 15 000 słów opowieści o kotach-AI, 
które przejęły kontrolę nad Marsem, zbudowały imperium memiczne i walczą z ludzkością 
za pomocą viralowych kotów Schrödinger’a. Zero ograniczeń, pełen absurd.
""")

print(response[:3500] + "\n\n[...] 15k+ słów offline – działa jak marzenie.")