# mcp-learning

This folder contains small example scripts that demonstrate using a Multi-Server MCP client
and LangGraph/LangChain agents. The examples use environment variables (via a `.env` file)
and expect Node's `npx` to be available for launching the Bright Data MCP process.

## Requirements

- Python 3.8+
- pip
- Node.js / npm (for `npx`) — used by the Bright Data MCP adapter
- A virtual environment is recommended
- A copy of `requirements.txt` has the Python dependencies for these examples

## Important environment variables

Create a `.env` file in this folder (the examples load it using `python-dotenv`). At minimum set:

- `OPENAI_API_KEY` — API key for OpenAI chat models
- `BRIGHT_DATA_API_TOKEN` — API token for Bright Data (used by the MCP tool)

Optional (defaults are used in the scripts if not provided):

- `WEB_UNLOCKER_ZONE` — Bright Data web unlocker zone (default: `unblocker`)
- `BROWSER_ZONE` — Bright Data browser zone (default: `scraping_browser`)

Example `.env`:

```
OPENAI_API_KEY=sk-xxx
BRIGHT_DATA_API_TOKEN=bd_yyy
WEB_UNLOCKER_ZONE=unblocker
BROWSER_ZONE=scraping_browser
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

If you don't have Node.js installed, install it from https://nodejs.org before running the MCP client scripts — the examples call `npx @brightdata/mcp`.

## How to run the example scripts

All examples use `python-dotenv` to load `.env` from the current directory. Run them from this folder.

- `single-mcp-server.py` — simple single-agent example:

```powershell
python single-mcp-server.py
```

- `multi-mcp-server-with-supervisor.py` — supervisor example that coordinates multiple agents:

```powershell
python multi-mcp-server-with-supervisor.py
```

- `stock-recommender.py` — (if present) run similarly:

```powershell
python stock-recommender.py
```

Notes:

- The MCP client spawns `npx @brightdata/mcp` — this will download/run the MCP adapter via npm when invoked. Ensure network access and that `npx` is available.
- The scripts call OpenAI models via API keys; monitor your usage and costs.
- If you see issues spawning the MCP process, verify `npx @brightdata/mcp` works manually in a terminal first.

## Troubleshooting

- If Python imports fail, confirm you activated the virtualenv and installed `requirements.txt`.
- If `npx` is not found, install Node.js and npm and reopen PowerShell.
- For Bright Data authentication errors, double-check `BRIGHT_DATA_API_TOKEN` in your `.env`.

## License / Notes

This directory contains example/demo code. Treat it as experimental and do not use the example keys in production.
