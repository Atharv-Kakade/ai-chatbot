import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(timeout=20, max_retries=0)

candidates = [
    "mistralai/mistral-7b-instruct-v0.3",
    "ibm/granite-3.0-8b-instruct",
    "nvidia/mistral-nemo-minitron-8b-8k-instruct",
    "nv-mistralai/mistral-nemo-12b-instruct",
]

for model in candidates:
    start = time.time()
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello in one sentence."}],
            max_tokens=50,
        )
        text = r.choices[0].message.content.strip()
        print(f"OK   {model} ({time.time() - start:.1f}s): {text}")
    except Exception as e:
        print(f"FAIL {model}: {type(e).__name__}")