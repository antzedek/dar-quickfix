from dar import DAR_QuickFix
from openai import OpenAI

client = OpenAI()
dar = DAR_QuickFix(lambda prompt, **kw: client.chat.completions.create(
    model="gpt-4o", messages=[{"role": "user", "content": prompt}], **kw
).choices[0].message.content)

print(dar.run("Napisz bardzo długą, chaotyczną powieść o kotach i AI w kosmosie. Min 5000 słów."))