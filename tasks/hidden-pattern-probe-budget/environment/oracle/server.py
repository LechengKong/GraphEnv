"""Oracle service. Holds the hidden instance; the agent reaches it only through this HTTP API.

POST /status                      -> start node, budget, calls used
POST /neighbors  {"node": id}     -> neighbour IDs (node must already be known); the first
                                     lookup of each item counts against the neighbors budget
POST /evaluate   {"nodes": [...]} -> similarity score in [0, 1]; counts against the budget
POST /submit     {"nodes": [...]} -> records the final answer; only once

Every request is appended to /state/log.jsonl and the submission is written to
/state/submission.json. The verifier reads those files after the agent finishes.
"""
from __future__ import annotations

import json
import math
import os
import threading
import time
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

INSTANCE = json.load(open(os.environ.get("INSTANCE", "/oracle/instance.json")))
STATE = os.environ.get("STATE_DIR", "/state")
MAX_SET = 200

G = nx.Graph()
G.add_nodes_from(INSTANCE["nodes"])
G.add_edges_from(INSTANCE["edges"])
S = INSTANCE["start"]
BUDGET = INSTANCE["eval_budget"]
ITERS = INSTANCE["wl_iterations"]
NB_BUDGET = INSTANCE.get("neighbors_budget")  # None = unlimited

lock = threading.Lock()
known = {S}
expanded = set()
evals_used = 0
submitted = False


def shape(nodes):
    g = G.subgraph(nodes).copy()
    for v in g:
        g.nodes[v]["root"] = v == S
    return g


def wl(g):
    lab = {v: "R" if g.nodes[v]["root"] else "N" for v in g}
    feat = defaultdict(int)
    for x in lab.values():
        feat[x] += 1
    for _ in range(ITERS):
        lab = {v: lab[v] + "(" + ",".join(sorted(lab[u] for u in g[v])) + ")" for v in g}
        for x in lab.values():
            feat[x] += 1
    return feat


T_SHAPE = shape(INSTANCE["target"])
T_FEAT = wl(T_SHAPE)
T_NORM = math.sqrt(sum(c * c for c in T_FEAT.values()))


def score(nodes):
    g = shape(nodes)
    f = wl(g)
    dot = sum(c * T_FEAT.get(k, 0) for k, c in f.items())
    cos = dot / (math.sqrt(sum(c * c for c in f.values())) * T_NORM)
    if cos > 1 - 1e-9 and len(g) == len(T_SHAPE):
        gm = GraphMatcher(g, T_SHAPE, node_match=lambda a, b: a["root"] == b["root"])
        return 1.0 if gm.is_isomorphic() else 0.99
    return round(min(cos, 0.99), 4)


def log(entry):
    entry["t"] = time.time()
    with open(os.path.join(STATE, "log.jsonl"), "a") as fh:
        fh.write(json.dumps(entry) + "\n")


class Err(Exception):
    pass


def node_list(body):
    nodes = body.get("nodes")
    if not isinstance(nodes, list) or not all(isinstance(x, str) for x in nodes):
        raise Err("'nodes' must be a list of node IDs")
    nodes = sorted(set(nodes))
    if not 1 <= len(nodes) <= MAX_SET:
        raise Err(f"a selection must contain between 1 and {MAX_SET} distinct nodes")
    unknown = [x for x in nodes if x not in known]
    if unknown:
        raise Err(f"{len(unknown)} node(s) have not been discovered yet, e.g. {unknown[0]!r}")
    return nodes


def handle(path, body):
    global evals_used, submitted
    with lock:
        if path == "/status":
            return {"start": S, "evaluate_budget": BUDGET, "evaluate_used": evals_used,
                    "neighbors_budget": NB_BUDGET, "neighbors_used": len(expanded),
                    "submitted": submitted}
        if path == "/neighbors":
            v = body.get("node")
            if v not in known:
                raise Err("unknown or undiscovered node")
            new = v not in expanded
            if new and NB_BUDGET is not None and len(expanded) >= NB_BUDGET:
                raise Err(f"neighbors budget exhausted ({NB_BUDGET} distinct items)")
            expanded.add(v)
            nb = sorted(G[v])
            known.update(nb)
            log({"op": "neighbors", "node": v, "new": new})
            return {"node": v, "neighbors": nb, "neighbors_used": len(expanded),
                    "neighbors_budget": NB_BUDGET}
        if path == "/evaluate":
            if submitted:
                raise Err("already submitted")
            nodes = node_list(body)
            if evals_used >= BUDGET:
                raise Err(f"evaluate budget exhausted ({BUDGET} calls)")
            evals_used += 1
            sc = score(nodes)
            log({"op": "evaluate", "n": len(nodes), "score": sc, "i": evals_used})
            return {"score": sc, "evaluate_used": evals_used, "evaluate_budget": BUDGET}
        if path == "/submit":
            if submitted:
                raise Err("already submitted")
            nodes = node_list(body)
            submitted = True
            with open(os.path.join(STATE, "submission.json.tmp"), "w") as fh:
                json.dump({"nodes": nodes, "evaluate_used": evals_used, "t": time.time()}, fh)
            os.replace(os.path.join(STATE, "submission.json.tmp"),
                       os.path.join(STATE, "submission.json"))
            log({"op": "submit", "n": len(nodes)})
            return {"accepted": True, "size": len(nodes)}
    raise Err("unknown endpoint")


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            if n > 1_000_000:
                raise Err("request too large")
            body = json.loads(self.rfile.read(n) or b"{}")
            if not isinstance(body, dict):
                raise Err("body must be a JSON object")
            out, code = handle(self.path, body), 200
        except Err as e:
            out, code = {"error": str(e)}, 400
        except Exception:  # never leak internals
            out, code = {"error": "bad request"}, 400
        data = json.dumps(out).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    do_GET = do_POST

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    os.makedirs(STATE, exist_ok=True)
    ThreadingHTTPServer(("0.0.0.0", 8080), H).serve_forever()
