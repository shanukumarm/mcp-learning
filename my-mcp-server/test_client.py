"""
Quick Python test client that spawns the local Node MCP-like server and talks to it over stdio.
Run from the `mcp-learning/my-mcp-server` folder after installing Node.js.
"""
import json
import subprocess
import sys
import time

def start_server():
    # Start the Node server
    p = subprocess.Popen(["node", "server.js"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    return p

def send_and_recv(proc, obj, timeout=1.0):
    line = json.dumps(obj) + "\n"
    proc.stdin.write(line)
    proc.stdin.flush()
    # read single line response (blocking)
    out = proc.stdout.readline()
    if not out:
        return None
    return json.loads(out)

if __name__ == '__main__':
    p = start_server()
    try:
        print('Requesting tools...')
        resp = send_and_recv(p, {"type": "list_tools"})
        print('tools response:', resp)

        print('Calling echo tool...')
        resp = send_and_recv(p, {"type":"call_tool", "call_id":"1", "tool":"echo", "args":{"message":"Hello MCP"}})
        print('echo response:', resp)

        print('Calling sum tool...')
        resp = send_and_recv(p, {"type":"call_tool", "call_id":"2", "tool":"sum", "args":{"numbers":[1,2,3,4]}})
        print('sum response:', resp)

        # optional LLM test if OPENAI_API_KEY is set in this environment
        import os
        if os.getenv('OPENAI_API_KEY'):
            print('Calling ask_llm tool...')
            resp = send_and_recv(p, {"type":"call_tool", "call_id":"3", "tool":"ask_llm", "args":{"prompt":"Write a 2-line haiku about code."}})
            print('ask_llm response:', resp)

    finally:
        try:
            p.stdin.close()
        except Exception:
            pass
        p.terminate()
        p.wait(timeout=2)
