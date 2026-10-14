import json
import os

from dotenv import load_dotenv
from openai import (
    OpenAI,
    APITimeoutError,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIStatusError,
)

load_dotenv()
client = OpenAI(timeout=60)
MODEL = os.environ["MODEL_NAME"]
HISTORY_FILE = "history.json"
MAX_MESSAGES = 20   # only send the latest 20 messages to the model


def load_history():
    """Read the saved chat from the file, or start fresh."""
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_reply(history):
    """Send the chat to the model and return its answer as text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=history[-MAX_MESSAGES:],
    )
    return (response.choices[0].message.content or "").strip()


def main():
    history = load_history()
    print("Chatbot ready. Type 'quit' to exit, '/reset' to clear memory.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if user_input == "/reset":
            history = []
            save_history(history)
            print("Memory cleared.\n")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            reply = get_reply(history)
        except APITimeoutError:
            print("Bot: The model took too long. Please try again.\n")
            history.pop()
            continue
        except APIConnectionError:
            print("Bot: Can't reach the server. Check your internet.\n")
            history.pop()
            continue
        except AuthenticationError:
            print("Bot: Your API key was rejected. Check your .env file.\n")
            history.pop()
            continue
        except RateLimitError:
            print("Bot: Too many requests. Wait a minute and try again.\n")
            history.pop()
            continue
        except NotFoundError:
            print("Bot: That model isn't available. Pick another MODEL_NAME.\n")
            history.pop()
            continue
        except APIStatusError as e:
            print(f"Bot: Server error ({e.status_code}). Try again.\n")
            history.pop()
            continue

        if not reply:
            print("Bot: (empty reply, please try again)\n")
            history.pop()
            continue

        print("Bot:", reply)
        print()
        history.append({"role": "assistant", "content": reply})
        save_history(history)


if __name__ == "__main__":
    main()