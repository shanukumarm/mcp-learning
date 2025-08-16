My MCP server scaffold

This is a minimal, local MCP-like server that communicates over stdio using newline-delimited JSON. It's intended as a starting point for building your own MCP server for development or testing with the Python MultiServerMCPClient.

Files:
- `server.js` - Node.js server that implements a tiny JSON protocol (list_tools / call_tool / ping)
- `test_client.py` - Python script that spawns `server.js` and demonstrates the request/response
- `package.json` - metadata and start script

How to run (PowerShell):

# from d:\project\mcp-learning\my-mcp-server
node --version; npm --version
node server.js

In another PowerShell window (or use the included test client):

python test_client.py

Using with `MultiServerMCPClient` in Python

You can point the client to spawn `node` with the server script as the argument. Example (pseudo-code):

client = MultiServerMCPClient({
  "local": {
    "command": "node",
    "args": ["server.js"],
    "transport": "stdio"
  }
})

Notes
- This scaffold is intentionally tiny. A production MCP server will need to implement the full MCP protocol expected by your client (tool schemas, streaming, approvals, auth, error handling, etc.).
- Use this to iterate locally and add features until your client integration works.
