#!/usr/bin/env node
// TypeScript version of the simple MCP-like server (stdio, newline-delimited JSON)

import readline from 'readline';

type Tool = {
  name: string;
  description?: string;
  params?: Record<string, { type: string; description?: string }>;
};

const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: false });

function send(obj: unknown) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

const tools: Tool[] = [
  {
    name: 'echo',
    description: 'Echoes received message back in the result',
    params: { message: { type: 'string', description: 'Message to echo' } },
  },
  {
    name: 'sum',
    description: 'Sums an array of numbers',
    params: { numbers: { type: 'array', description: 'Array of numbers' } },
  },
  {
    name: 'ask_llm',
    description: 'Ask an LLM (OpenAI Chat) to generate a short response for a prompt',
    params: { prompt: { type: 'string', description: 'Prompt to send to the LLM' }, model: { type: 'string', description: 'Optional model id (default: gpt-4o)' } },
  },
];

rl.on('line', async (line: string) => {
  const l = line.trim();
  if (!l) return;

  let msg: Record<string, any> | undefined;
  try {
    msg = JSON.parse(l);
  } catch (e: any) {
    send({ type: 'error', message: 'invalid_json', detail: e?.message });
    return;
  }

  if (!msg) {
    send({ type: 'error', message: 'empty_message' });
    return;
  }

  if (msg.type === 'list_tools') {
    send({ type: 'tools_list', tools });
    return;
  }

  if (msg.type === 'call_tool') {
    const { call_id, tool, args } = msg;
    if (!call_id) {
      send({ type: 'error', message: 'missing_call_id' });
      return;
    }

    if (tool === 'echo') {
      const message = args?.message ? String(args.message) : '';
      send({ type: 'call_result', call_id, result: { output: `Echo: ${message}` } });
      return;
    }

    if (tool === 'sum') {
      const nums: number[] = Array.isArray(args?.numbers) ? args.numbers.map((n: any) => Number(n)) : [];
      const total = nums.reduce((a: number, b: number) => a + (Number.isNaN(b) ? 0 : b), 0);
      send({ type: 'call_result', call_id, result: { total, count: nums.length } });
      return;
    }

    if (tool === 'ask_llm') {
      const prompt = args?.prompt ? String(args.prompt) : '';
      const model = args?.model || process.env.OPENAI_MODEL || 'gpt-4o';

      if (!process.env.OPENAI_API_KEY) {
        send({ type: 'call_error', call_id, error: 'missing OPENAI_API_KEY in server environment' });
        return;
      }

      try {
        const res = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          },
          body: JSON.stringify({ model, messages: [{ role: 'user', content: prompt }], max_tokens: 300 }),
        });

        if (!res.ok) {
          const text = await res.text();
          send({ type: 'call_error', call_id, error: `llm_error:${res.status}`, detail: text });
          return;
        }

        const payload = await res.json();
        const content = payload.choices?.[0]?.message?.content;
        send({ type: 'call_result', call_id, result: { content, raw: payload } });
      } catch (e: any) {
        send({ type: 'call_error', call_id, error: 'llm_exception', detail: String(e) });
      }

      return;
    }

    send({ type: 'call_error', call_id, error: `unknown_tool:${tool}` });
    return;
  }

  if (msg.type === 'ping') {
    send({ type: 'pong' });
    return;
  }

  send({ type: 'error', message: 'unknown_message_type', received: msg.type });
});

process.stdin.on('end', () => process.exit(0));
