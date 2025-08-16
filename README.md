# mcp-learning

This folder contains a few example scripts that demonstrate using a local or remote MCP server
and integrating it with Python agents. The examples use environment variables (via a `.env` file)
when needed.

## Requirements

- Python 3.8+
- pip
- Node.js / npm (for `npx`) — used by the Bright Data MCP adapter
- A virtual environment is recommended
- A copy of `requirements.txt` has the Python dependencies for these examples

## Important environment variables

Create a `.env` file in this folder (the examples load it using `python-dotenv`).

- `OPENAI_API_KEY` — required if you want examples or the local server's `ask_llm` tool to call OpenAI.

Example `.env`:

```
OPENAI_API_KEY=sk-xxx
```

## Setup (PowerShell examples)

Open PowerShell in `d:\project\mcp-learning` and run:

```powershell
# create and activate venv (Windows PowerShell)
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# install Python deps
pip install -r requirements.txt

# make sure Node.js and npm are installed so `npx` can run
node --version; npm --version
```

If you don't have Node.js installed, install it from https://nodejs.org before running the local Node-based MCP server examples.

## How to run the example scripts

All examples use `python-dotenv` to load `.env` from the current directory. Run them from this folder.

- `single-mcp-server.py` — simple single-agent example that demonstrates calling a local MCP server (or configure to spawn a remote one):

```powershell
python single-mcp-server.py
```

- `multi-mcp-server-with-supervisor.py` — supervisor example that coordinates multiple agents through MCP:

```powershell
python multi-mcp-server-with-supervisor.py
```

- `local-mcp-server.py` — a generic client demo that can connect to a local spawned Node MCP or a remote TCP MCP (demo mode):

```powershell
python local-mcp-server.py --mode local
```

Notes:

Notes:
- The examples are minimal and meant for local testing and learning.
- The `ask_llm` tool calls OpenAI when `OPENAI_API_KEY` is available to the server process — set that in `.env` or pass it into the spawned process environment.
- Monitor OpenAI usage and costs when running LLM calls.

## Troubleshooting

- If Python imports fail, confirm you activated the virtualenv and installed `requirements.txt`.
- If Node is not found, install Node.js and reopen PowerShell.
 

## License / Notes

This directory contains example/demo code. Treat it as experimental and do not use the example keys in production.
