import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key = os.environ.get("OPENAI_API_KEY", "")
print("Key loaded:", key[:6] + "..." if key else "NO KEY FOUND")
print("Base URL:", os.environ.get("OPENAI_BASE_URL"))
print("Model:", os.environ.get("MODEL_NAME"))

client = OpenAI(timeout=30)

try:
    response = client.chat.completions.create(
        model=os.environ["MODEL_NAME"],
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
        max_tokens=100,
    )
    print(response.choices[0].message.content)
except Exception as e:
    print("ERROR:", type(e).__name__, "-", e)