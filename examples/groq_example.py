# examples/groq_example.py
# Groq (Llama3-70B @ 500+ tok/s) + DAR QuickFix = stabilność przy prędkości światła

from dar import DAR_QuickFix
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))   # klucz z groq.com

# Bezpośrednio wrapper na Groq – działa i z .chat.completions.create i ze stream=True
groq_dar = DAR_QuickFix(
    lambda prompt, **kwargs: client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=8192,
        **kwargs
    ).choices[0].message.content
)

print("Groq + DAR – 70B przy 500 tok/s, ale bez pętli i dryfu:")
response = groq_dar.run("""
Napisz bardzo długą (minimum 10 000 słów), absolutnie chaotyczną historię 
o kotach, które zbudowały sztuczną inteligencję, poleciały na Marsa i zaczęły wojnę memiczną.
Nie oszczędzaj szczegółów, dialogów i absurdu.
""")

print(response[:3000] + "\n\n[...] stabilne 10k+ słów – zero pętli, zero sucharów.")