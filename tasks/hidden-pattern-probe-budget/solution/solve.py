"""Reference solution.

Finding: the target is the set of all items that lie on some shortest path between the start
item and one other (unknown) item.

1. Explore outward from the start, nearest items first, within the `neighbors` budget. Only items
   inside the fully explored radius R have exactly known distances, so candidates are limited
   to end items within R (the target turns out to be well inside the affordable radius).
2. For every candidate end item u, compute that shortest-path set locally. Group candidates by
   rooted shape, so each distinct shape costs at most one `evaluate` call.
3. The score behaves like a cosine similarity over structural features. Each evaluation
   therefore bounds the angle between the target and every other candidate:
       angle(c, T) >= |angle(e, T) - angle(c, e)|
   Always evaluate the candidate with the smallest bound, and skip candidates ruled out.
   This usually needs fewer than 10 evaluate calls.
"""
from __future__ import annotations

import json
import math
import subprocess
from collections import defaultdict, deque

import networkx as nx


class ProbeClient:  # noqa: D101
    """Talks to the service through the `probe` CLI, exactly as an agent would."""

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


def explore(client, s, budget):
    """Breadth-first expansion of at most `budget` items. Returns the graph seen and the largest
    radius R such that every item within distance R of the start was expanded."""
    g, q, dist = nx.Graph(), deque([s]), {s: 0}
    g.add_node(s)
    expanded = 0
    complete_radius = -1
    while q and expanded < budget:
        v = q.popleft()
        if dist[v] > complete_radius + 1:
            complete_radius = dist[v] - 1
        for u in client.neighbors(v):
            g.add_edge(v, u)
            if u not in dist:
                dist[u] = dist[v] + 1
                q.append(u)
        expanded += 1
    if not q:
        complete_radius = max(dist.values())
    elif all(dist[x] > dist[v] for x in q):
        complete_radius = dist[v]
    return g, complete_radius


def shortest_path_set(g, u, ds):
    """All items on some shortest path between the start and u."""
    du = nx.single_source_shortest_path_length(g, u, cutoff=ds[u])
    return frozenset(v for v, d in du.items() if v in ds and ds[v] + d == ds[u])


def features(g, s, nodes, iters=3):
    """Rooted Weisfeiler-Lehman subtree feature counts of the induced subgraph."""
    sub = g.subgraph(nodes)
    lab = {v: "R" if v == s else "N" for v in sub}
    feat = defaultdict(int)
    for x in lab.values():
        feat[x] += 1
    for _ in range(iters):
        lab = {v: lab[v] + "(" + ",".join(sorted(lab[u] for u in sub[v])) + ")" for v in sub}
        for x in lab.values():
            feat[x] += 1
    return feat


def cos(a, b):
    dot = sum(c * b.get(k, 0) for k, c in a.items())
    return dot / (math.sqrt(sum(c * c for c in a.values())) *
                  math.sqrt(sum(c * c for c in b.values())))


def solve(client, s, budget, tol=2e-3):
    g, R = explore(client, s, budget)
    print(f"explored {budget} items; every item within distance {R} of the start is expanded")
    # Distances are exact up to R + 1; a shortest-path set to u is fully known when d(u) <= R.
    ds = nx.single_source_shortest_path_length(g, s, cutoff=R)
    cands, feats = {}, {}
    for u in sorted(ds, key=lambda v: (ds[v], v)):
        if ds[u] == 0:
            continue
        I = shortest_path_set(g, u, ds)
        if len(I) > 200:
            continue
        f = features(g, s, I)
        key = frozenset(f.items())
        if key not in cands:
            cands[key], feats[key] = I, f
    print(f"{len(cands)} distinct candidate shapes")

    bound = {k: 0.0 for k in cands}       # lower bound on angle(candidate, target)
    calls = 0
    while bound:
        k = min(bound, key=lambda x: (bound[x], len(cands[x])))
        if bound[k] > 10 * tol:
            break
        calls += 1
        sc = client.evaluate(sorted(cands[k]))
        print(f"evaluate #{calls}: {len(cands[k])} items -> {sc}")
        if sc == 1.0:
            return cands[k], calls
        del bound[k]
        if sc >= 0.99:                     # capped value: only says the angle is small
            continue
        th = math.acos(max(-1.0, min(1.0, sc)))
        for o in list(bound):
            th_co = math.acos(max(-1.0, min(1.0, cos(feats[k], feats[o]))))
            bound[o] = max(bound[o], abs(th - th_co) - tol)
    return None, calls


if __name__ == "__main__":
    c = ProbeClient()
    st = c._run("status")
    T, calls = solve(c, st["start"], st["neighbors_budget"])
    print(f"evaluate calls used: {calls}")
    if T is not None:
        print(json.dumps(c.submit(sorted(T))))
