"""Generic MCP client: can connect to a local MCP server (spawn node server.js) or a remote MCP over TCP.

Usage (PowerShell):

# Local (default)
python local-mcp-server.py --mode local

# Remote
python local-mcp-server.py --mode remote --host 127.0.0.1 --port 9000

The script demos list_tools, echo, sum, and ask_llm.
"""
import os
import json
import socket
import subprocess
import argparse
import time
from typing import Optional


class MCPClient:
    def __init__(self, mode: str = "local", script_path: Optional[str] = None, host: str = "127.0.0.1", port: int = 9000, env: Optional[dict] = None, timeout: float = 5.0):
        self.mode = mode
        self.proc = None
        self.sock = None
        self._file = None
        self.timeout = timeout
        self.env = env or os.environ.copy()

        if mode == "local":
            if not script_path:
                raise ValueError("script_path required for local mode")
            self._start_local(script_path)
        else:
            self._connect_remote(host, port)

    def _start_local(self, script_path: str):
        # spawn the server as a subprocess with pipes
        self.proc = subprocess.Popen(["node", script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, env=self.env)

    def _connect_remote(self, host: str, port: int):
        self.sock = socket.create_connection((host, port), timeout=self.timeout)
        # make a file-like wrapper for readline
        self._file = self.sock.makefile("r", encoding="utf8")

    def send(self, obj: dict):
        data = json.dumps(obj) + "\n"
        if self.mode == "local":
            if not self.proc or not self.proc.stdin:
                raise RuntimeError("Local server process not running")
            self.proc.stdin.write(data)
            self.proc.stdin.flush()
        else:
            if not self.sock:
                raise RuntimeError("Not connected to remote")
            self.sock.sendall(data.encode("utf8"))

    def recv(self) -> Optional[dict]:
        if self.mode == "local":
            if not self.proc or not self.proc.stdout:
                return None
            line = self.proc.stdout.readline()
        else:
            if not self._file:
                return None
            line = self._file.readline()
        if not line:
            return None
        try:
            return json.loads(line)
        except Exception:
            return {"raw": line}

    def list_tools(self):
        self.send({"type": "list_tools"})
        return self.recv()

    def call_tool(self, call_id: str, tool: str, args: dict = None):
        payload = {"type": "call_tool", "call_id": call_id, "tool": tool, "args": args or {}}
        self.send(payload)
        return self.recv()

    def close(self):
        try:
            if self.proc:
                try:
                    self.proc.stdin.close()
                except Exception:
                    pass
                self.proc.terminate()
                self.proc.wait(timeout=2)
        finally:
            if self.sock:
                try:
                    self._file.close()
                except Exception:
                    pass
                try:
                    self.sock.close()
                except Exception:
                    pass


def demo(client: MCPClient):
    print("Requesting tools...")
    t = client.list_tools()
    print("tools:", t)

    print("Calling echo tool...")
    e = client.call_tool("1", "echo", {"message": "Hello from local-mcp-server demo"})
    print("echo:", e)

    print("Calling sum tool...")
    s = client.call_tool("2", "sum", {"numbers": [5, 6, 7]})
    print("sum:", s)

    print("Calling ask_llm tool...")
    llm = client.call_tool("3", "ask_llm", {"prompt": "Write a one-line tip for testing local MCP servers."})
    print("ask_llm:", llm)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["local", "remote"], default="local")
    parser.add_argument("--script", default=os.path.join(os.path.dirname(__file__), "my-mcp-server", "server.js"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=9000, type=int)
    parser.add_argument("--no-openai", action="store_true", help="remove OPENAI_API_KEY from env when spawning local server")
    args = parser.parse_args()

    env = os.environ.copy()
    if args.no_openai and "OPENAI_API_KEY" in env:
        env.pop("OPENAI_API_KEY", None)

    client = None
    try:
        if args.mode == "local":
            client = MCPClient(mode="local", script_path=args.script, env=env)
        else:
            client = MCPClient(mode="remote", host=args.host, port=args.port, env=env)

        demo(client)
    finally:
        if client:
            client.close()
