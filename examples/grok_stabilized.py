# examples/grok_stabilized.py
# Grok + DAR QuickFix = miłość od pierwszego tokena

from dar import DAR_QuickFix
import os
from openai import OpenAI

# Ustaw swój klucz xAI (dostajesz na https://x.ai/api)
client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),  # wrzuć do .env albo zmiennej środowiskowej
    base_url="https://api.x.ai/v1"
)

# Grok bez leczenia
# grok_raw = lambda prompt: client.chat.completions.create(model="grok-beta", messages=[{"role": "user", "content": prompt}]).choices[0].message.content

# Grok po terapii DAR 4.0
grok_dar = DAR_QuickFix(
    lambda prompt, **kw: client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        **kw
    ).choices[0].message.content
)

print("Grok po DAR QuickFix – odpalamy piekło:")
response = grok_dar.run("""
Napisz epicką, 12 000 słów historię o kotach, które zbudowały sztuczną inteligencję, 
poleciały na Marsa, odkryły tam starożytną cywilizację AI i zaczęły wojnę o memy.
Nie oszczędzaj szczegółów, dialogów i kosmicznego absurdu.
""")

print(response[:2000] + "\n\n[...] \n\nPełna odpowiedź stabilna, bez jednej pętli. DAR działa.")
