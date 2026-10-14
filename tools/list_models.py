from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(timeout=30)

try:
    ids = sorted(m.id for m in client.models.list())
    print("Total models:", len(ids))
    for model_id in ids:
        if "instruct" in model_id.lower():
            print(model_id)
except Exception as e:
    print("ERROR:", type(e).__name__, "-", e)