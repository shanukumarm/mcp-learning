My MCP server (TypeScript)

This folder contains a minimal MCP-like server implemented in TypeScript. It communicates over stdio using newline-delimited JSON and exposes three demo tools: `echo`, `sum`, and `ask_llm`.

Files
- `src/server.ts` — TypeScript server source
- `dist/server.js` — built server (after running `npm run build`)
- `test_client.py`, `local-mcp-server.py` — small Python clients that demonstrate usage
- `package.json` — scripts for building and running

Quick start

1. Install dependencies (one time):

```powershell
cd d:\project\mcp-learning\my-mcp-server
npm install
```

2. Build and run the server:

```powershell
npm run build
node dist/server.js
```

3. Run the Python client (from the repository root) to exercise the tools:

```powershell
# run the demo client and point it to the built server
python local-mcp-server.py --mode local --script d:\project\mcp-learning\my-mcp-server\dist\server.js
```

Development (live-run)

Use `tsx` to run the TypeScript file directly (fast iteration):

```powershell
npm run dev
# or
npx tsx src/server.ts
```

Environment

- Node 18+ is recommended (native fetch + modern runtime features).
- If you want the `ask_llm` tool to call OpenAI, set `OPENAI_API_KEY` in the environment before spawning the server:

```powershell
$env:OPENAI_API_KEY = 'sk-...'
node dist/server.js
```

Testing without OpenAI

If you don't set `OPENAI_API_KEY`, `ask_llm` will return a `call_error` telling you the key is missing — useful for offline testing.

Notes

- This server is intentionally tiny and intended for local development and learning. A production MCP server should add robust schemas, streaming support, authentication, and error handling.
