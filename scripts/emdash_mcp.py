#!/usr/bin/env python3
"""Call EmDash MCP tools for kotacom-emdash staging (curl-based, Cloudflare-safe).

Usage:
  python3 scripts/emdash_mcp.py list [filter]
  python3 scripts/emdash_mcp.py <tool_name> '<json-args>'
"""
import json
import os
import subprocess
import sys

URL = "https://staging.devk.my.id/_emdash/api/mcp"


def load_pat():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    with open(env_path) as fh:
        for line in fh:
            if line.startswith("EMDASH_PAT="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("EMDASH_PAT not found")


def rpc(token, method, params=None, _id=1):
    payload = {"jsonrpc": "2.0", "id": _id, "method": method}
    if params is not None:
        payload["params"] = params
    proc = subprocess.run(
        [
            "curl", "-s", "-X", "POST", URL,
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json, text/event-stream",
            "-H", f"Authorization: Bearer {token}",
            "--data-binary", "@-",
        ],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=120,
    )
    body = proc.stdout
    data_lines = [l[5:].strip() for l in body.splitlines() if l.startswith("data:")]
    if data_lines:
        body = data_lines[-1]
    return json.loads(body)


def parse_result(out):
    """Unwrap MCP tool result content into Python."""
    if "error" in out:
        return {"__error__": out["error"]}
    content = out.get("result", {}).get("content", [])
    for c in content:
        if c.get("type") == "text":
            txt = c["text"]
            try:
                return json.loads(txt)
            except json.JSONDecodeError:
                return txt
    return out.get("result")


def main():
    token = load_pat()
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        out = rpc(token, "tools/list")
        tools = out.get("result", {}).get("tools", [])
        needle = sys.argv[2] if len(sys.argv) > 2 else ""
        for t in tools:
            if needle and needle not in t["name"]:
                continue
            print(t["name"])
            print("    " + t.get("description", "")[:200].replace("\n", " "))
        return
    if len(sys.argv) > 2:
        tool = sys.argv[1]
        args = json.loads(sys.argv[2])
        out = rpc(token, "tools/call", {"name": tool, "arguments": args})
        res = parse_result(out)
        print(json.dumps(res, indent=2)[:12000])
        return
    print(__doc__)


if __name__ == "__main__":
    main()
