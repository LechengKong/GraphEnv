"""Shared helpers for negative / shortcut attempts. They talk to the oracle through `probe`."""
import json, subprocess, sys
from collections import deque
sys.path.insert(0, "/solution")

def probe(*args, stdin=None, ok=True):
    r = subprocess.run(["probe", *args], input=stdin, capture_output=True, text=True)
    if ok and r.returncode:
        raise RuntimeError(r.stderr)
    return (json.loads(r.stdout) if r.returncode == 0 else {"error": r.stderr.strip()})

def evaluate(nodes): return probe("evaluate", "-", stdin="\n".join(sorted(nodes)), ok=False)
def submit(nodes): return probe("submit", "-", stdin="\n".join(sorted(nodes)), ok=False)

def explore(s):
    adj, q = {s: None}, deque([s])
    while q:
        v = q.popleft()
        adj[v] = probe("neighbors", v)["neighbors"]
        for u in adj[v]:
            if u not in adj:
                adj[u] = None; q.append(u)
    return adj

def bfs(adj, s):
    d, q = {s: 0}, deque([s])
    while q:
        v = q.popleft()
        for u in adj[v]:
            if u not in d:
                d[u] = d[v] + 1; q.append(u)
    return d
