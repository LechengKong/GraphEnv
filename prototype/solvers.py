"""Blind search baselines. They see only the score; they do not know it is WL."""
from __future__ import annotations

import random

import networkx as nx

from core import WLScorer


def _frontier(h, L):
    return {u for v in L for u in h[v]} - L


def _removable(h, s, L):
    out = []
    for v in L:
        if v == s:
            continue
        rest = L - {v}
        if nx.is_connected(h.subgraph(rest)):
            out.append(v)
    return out


def hill_climb(h: nx.Graph, s: int, f: WLScorer, budget: int, rng: random.Random,
               patience: int = 400) -> dict:
    """Random-mutation hill climbing, ties accepted, random restart after `patience` stalls."""
    best_ever, L = 0.0, {s}
    cur = f(L)
    stall = 0
    while f.calls < budget:
        r = rng.random()
        cand = set(L)
        fr = sorted(_frontier(h, L))
        if r < 0.55 or len(L) == 1:
            cand.add(rng.choice(fr))
        else:
            rem = _removable(h, s, L)
            if not rem:
                continue
            cand.discard(rng.choice(rem))
            if r > 0.85:  # swap move
                cand.add(rng.choice(sorted(_frontier(h, cand))))
        if len(cand) > 200:
            continue
        val = f(cand)
        if val == 1.0:
            return dict(solved=True, calls=f.calls, best=1.0)
        if val >= cur:
            stall = 0 if val > cur else stall + 1
            L, cur = cand, val
        else:
            stall += 1
        best_ever = max(best_ever, cur)
        if stall > patience:
            L, stall = {s}, 0
            cur = f(L)
    return dict(solved=False, calls=f.calls, best=best_ever)


def tabu_steepest(h: nx.Graph, s: int, f: WLScorer, budget: int, rng: random.Random,
                  tenure: int = 7) -> dict:
    """Steepest ascent over all single add/remove moves, with a tabu list to escape optima."""
    L = {s}
    tabu: dict[int, int] = {}
    best_ever, step = 0.0, 0
    while f.calls < budget:
        step += 1
        moves = [("add", v) for v in _frontier(h, L)]
        moves += [("rem", v) for v in _removable(h, s, L)]
        rng.shuffle(moves)
        best_mv, best_val = None, -1.0
        for kind, v in moves:
            if tabu.get(v, 0) > step:
                continue
            cand = L | {v} if kind == "add" else L - {v}
            if len(cand) > 200:
                continue
            val = f(cand)
            if val == 1.0:
                return dict(solved=True, calls=f.calls, best=1.0)
            if val > best_val:
                best_mv, best_val = (kind, v), val
            if f.calls >= budget:
                break
        if best_mv is None:
            tabu.clear()
            continue
        kind, v = best_mv
        L = L | {v} if kind == "add" else L - {v}
        tabu[v] = step + tenure
        best_ever = max(best_ever, best_val)
    return dict(solved=False, calls=f.calls, best=best_ever)


def interval_enum(h: nx.Graph, s: int, f: WLScorer, budget: int, rng: random.Random) -> dict:
    """Structure-aware solver: knows T = Interval(s, t) for some unknown t.

    Enumerates t by increasing distance, groups candidate intervals by rooted WL hash
    (computed locally, free), and spends one evaluate call per distinct shape. This is
    what an agent that has inferred the hidden layer "target is a shortest-path subgraph"
    could do with a scratchpad. Also reports how many nodes it had to expand.
    """
    from core import interval
    ds = nx.single_source_shortest_path_length(h, s)
    seen: set[str] = set()
    for t in sorted(ds, key=lambda v: (ds[v], rng.random())):
        if f.calls >= budget:
            break
        I = interval(h, s, t, ds)
        if len(I) > 200:
            continue
        g = h.subgraph(I).copy()
        for v in g:
            g.nodes[v]["r"] = str(v == s)
        key = nx.weisfeiler_lehman_graph_hash(g, node_attr="r", iterations=4)
        if key in seen:
            continue
        seen.add(key)
        if f(I) == 1.0:
            expanded = sum(1 for v in ds if ds[v] <= ds[t])
            return dict(solved=True, calls=f.calls, best=1.0, expanded=expanded)
    return dict(solved=False, calls=f.calls, best=float("nan"), expanded=len(ds))


SOLVERS = {"hill_climb": hill_climb, "tabu_steepest": tabu_steepest,
           "interval_enum": interval_enum}
