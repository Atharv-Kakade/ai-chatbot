import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(timeout=30, max_retries=0)

SKIP = ("embed", "rerank", "vision", "code", "translate", "guard",
        "safety", "reward", "parse", "clip", "asr", "tts", "image", "diffusion")

ids = sorted(m.id for m in client.models.list())
ids = [i for i in ids if not any(word in i.lower() for word in SKIP)]
print(f"Testing {len(ids)} models, please wait...\n")


def check(model):
    start = time.time()
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello in one sentence."}],
            max_tokens=30,
        )
        text = (r.choices[0].message.content or "").strip()
        return model, True, time.time() - start, text
    except Exception as e:
        return model, False, time.time() - start, type(e).__name__


failures = {}
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(check, m) for m in ids]
    for f in as_completed(futures):
        model, ok, secs, info = f.result()
        if ok:
            print(f"OK   {model} ({secs:.1f}s): {info or '(empty reply)'}")
        else:
            failures[info] = failures.get(info, 0) + 1

print("\nFailures by type:", failures)
print("Done.")