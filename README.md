# AI Chatbot

A terminal chatbot in Python that remembers the conversation, streams replies word by word, and saves chat history to a file. Built with the OpenAI Python library against an OpenAI-compatible API (NVIDIA's free endpoints).

## Features
- Conversation memory (sends recent history on every request)
- Streaming responses
- Chat history saved to `history.json` and reloaded on restart
- Friendly handling of timeouts, bad keys, rate limits, and unavailable models
- Configurable personality through a system prompt
- `/reset` command to clear memory

## Setup
```bash
git clone https://github.com/Atharv-Kakade/ai-chatbot.git
cd ai-chatbot
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env    # then add your API key and model name
python chatbot.py
```

## Usage
Type a message and press Enter. Type `/reset` to clear memory and `quit` to exit.

## Helper scripts
The `tools/` folder has scripts for finding which free models are currently available (`scan_models.py`, `list_models.py`, `test_models.py`). Free endpoints change often, so these are handy when a model stops working.

## Tech
Python 3.12, openai, python-dotenv, uv