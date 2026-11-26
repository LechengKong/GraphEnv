"""Reference solution.

Hypothesis (what the agent has to discover): the target is the set of all nodes lying on
some shortest path from the start node to one hidden end node.

1. Map the network with `neighbors` (unlimited).
2. For every candidate end node u, compute Interval(start, u) locally and group candidates
   by rooted shape, so each distinct shape costs at most one `evaluate` call.
3. Treat the score as a cosine similarity over structural features (it is one, but the
   solution only needs it to be roughly angular): each evaluation rules out every candidate
   whose structural similarity to the evaluated set is inconsistent with its score.
"""
from __future__ import annotations

import json
import math
import subprocess
from collections import defaultdict, deque

import networkx as nx


class ProbeClient:
    """Talks to the oracle through the `probe` CLI, exactly as an agent would."""

    def _run(self, *args, stdin=None):
        out = subprocess.run(["probe", *args], input=stdin, capture_output=True, text=True)
        if out.returncode != 0:
            raise RuntimeError(out.stderr.strip())
        return json.loads(out.stdout)

    def start(self):
        return self._run("status")["start"]

    def neighbors(self, v):
        return self._run("neighbors", v)["neighbors"]

    def evaluate(self, nodes):
        return self._run("evaluate", "-", stdin="\n".join(nodes))["score"]

    def submit(self, nodes):
        return self._run("submit", "-", stdin="\n".join(nodes))


def explore(client, s):
    g, q, seen = nx.Graph(), deque([s]), {s}
    g.add_node(s)
    while q:
        v = q.popleft()
        for u in client.neighbors(v):
            g.add_edge(v, u)
            if u not in seen:
                seen.add(u)
                q.append(u)
    return g


def interval(g, s, u, ds):
    du = nx.single_source_shortest_path_length(g, u, cutoff=ds[u])
    return frozenset(v for v, d in du.items() if v in ds and ds[v] + d == ds[u])


def shape_key(g, s, nodes):
    sub = g.subgraph(nodes).copy()
    for v in sub:
        sub.nodes[v]["r"] = str(v == s)
    return nx.weisfeiler_lehman_graph_hash(sub, node_attr="r", iterations=4)


def wl_features(g, s, nodes, iters=3):
    """Rooted WL subtree feature counts. Labels are canonical strings, so they are comparable
    across sets without a shared dictionary."""
    sub = g.subgraph(nodes)
    lab = {v: "R" if v == s else "N" for v in sub}
    feat = defaultdict(int)
    for v in lab.values():
        feat[v] += 1
    for _ in range(iters):
        lab = {v: lab[v] + "(" + ",".join(sorted(lab[u] for u in sub[v])) + ")" for v in sub}
        for v in lab.values():
            feat[v] += 1
    return feat


def cos(a, b):
    dot = sum(c * b.get(k, 0) for k, c in a.items())
    na = math.sqrt(sum(c * c for c in a.values()))
    nb = math.sqrt(sum(c * c for c in b.values()))
    return dot / (na * nb)


def _prune_search(client, cands, feats, tol, log):
    """Best-first evaluation with angular pruning over a dict key -> node set."""
    bound = {k: 0.0 for k in cands}          # lower bound on angle(candidate, target)
    calls = 0
    while bound:
        k = min(bound, key=lambda x: (bound[x], len(cands[x])))
        if bound[k] > tol * 10:
            break
        calls += 1
        sc = client.evaluate(sorted(cands[k]))
        log(f"evaluate #{calls}: size {len(cands[k])} -> {sc}  ({len(bound)} candidates left)")
        if sc == 1.0:
            return cands[k], calls
        del bound[k]
        if sc >= 0.99:          # capped: only says the angle is small
            continue
        th = math.acos(max(-1.0, min(1.0, sc)))
        fk = feats[k]
        for o in list(bound):
            th_co = math.acos(max(-1.0, min(1.0, cos(fk, feats[o]))))
            b = abs(th - th_co) - tol
            if b > bound[o]:
                bound[o] = b
    return None, calls


def solve_union(client, s, g=None, max_dist=15, log=print, tol=2e-3):
    """Same idea for targets that are the union of two shortest-path sets from the start."""
    g = g if g is not None else explore(client, s)
    ds = nx.single_source_shortest_path_length(g, s, cutoff=max_dist)
    ends = sorted((u for u in ds if ds[u] >= 1), key=lambda v: (ds[v], v))
    I = {u: interval(g, s, u, ds) for u in ends}
    cands, feats = {}, {}
    for i, a in enumerate(ends):
        for b in ends[i + 1:]:
            U = I[a] | I[b]
            if len(U) > 200:
                continue
            f = wl_features(g, s, U)
            key = frozenset(f.items())
            if key not in cands:
                cands[key], feats[key] = U, f
    log(f"{len(ends)} end candidates, {len(cands)} distinct union shapes")
    return _prune_search(client, cands, feats, tol, log)


def solve(client, s, g=None, max_dist=25, log=print, tol=2e-3):
    """Best-first search over candidate shapes with angular pruning.

    If the score is a cosine similarity, angle(c, T) >= |angle(e, T) - angle(c, e)| for any
    evaluated set e. A candidate can only be T's shape if that lower bound is ~0, so we always
    evaluate the candidate with the smallest bound and never evaluate ruled-out ones.
    """
    g = g if g is not None else explore(client, s)
    ds = nx.single_source_shortest_path_length(g, s, cutoff=max_dist)
    cands = {}
    for u in sorted(ds, key=lambda v: (ds[v], v)):
        if ds[u] == 0:
            continue
        I = interval(g, s, u, ds)
        if len(I) <= 200:
            cands.setdefault(shape_key(g, s, I), I)
    keys = sorted(cands, key=lambda k: (len(cands[k]), k))
    feats = {k: wl_features(g, s, cands[k]) for k in keys}
    bound = {k: 0.0 for k in keys}          # lower bound on angle(c, T)
    calls = 0
    while bound:
        k = min(bound, key=lambda x: (bound[x], len(cands[x]), x))
        if bound[k] > tol * 10:
            break
        calls += 1
        sc = client.evaluate(sorted(cands[k]))
        if sc == 1.0:
            return cands[k], calls
        del bound[k]
        if sc >= 0.99:          # capped: only tells us the angle is small, skip the update
            continue
        th = math.acos(max(-1.0, min(1.0, sc)))
        for o in list(bound):
            th_co = math.acos(max(-1.0, min(1.0, cos(feats[k], feats[o]))))
            bound[o] = max(bound[o], abs(th - th_co) - tol)
    return None, calls


if __name__ == "__main__":
    import os
    c = ProbeClient()
    s = c.start()
    T, calls = (solve_union if os.environ.get("RULE") == "union2" else solve)(c, s)
    print(f"evaluate calls used: {calls}")
    if T is not None:
        print(json.dumps(c.submit(sorted(T))))
