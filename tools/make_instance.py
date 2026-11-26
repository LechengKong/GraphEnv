"""Generate one hidden instance for the probe task and write it to the oracle and verifier dirs.

Instance = perturbed-grid host graph with opaque node IDs, a start node s, hidden end node(s), and
  --rule interval : T = Interval(s, t)            (every node on some shortest s-t path)
  --rule union2   : T = Interval(s, t1) | Interval(s, t2)

Usage: uv run --project prototype python tools/make_instance.py --task tasks/<slug> [--seed N]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prototype"))
from core import depth_width, interval, perturbed_grid  # noqa: E402


def rooted_hash(h, s, nodes):
    g = h.subgraph(nodes).copy()
    for v in g:
        g.nodes[v]["r"] = str(v == s)
    return nx.weisfeiler_lehman_graph_hash(g, node_attr="r", iterations=4)


def canonical_calls(h, s, t_target, T):
    """evaluate calls the reference solver needs: distinct interval shapes, by distance then id."""
    ds = nx.single_source_shortest_path_length(h, s)
    want = rooted_hash(h, s, T)
    seen = set()
    for u in sorted(ds, key=lambda v: (ds[v], str(v))):
        if ds[u] == 0:
            continue
        key = rooted_hash(h, s, interval(h, s, u, ds))
        if key in seen:
            continue
        seen.add(key)
        if key == want:
            return len(seen)
    raise RuntimeError("target not reachable by enumeration")


def pick(seed: int, args):
    rng = random.Random(seed)
    h = perturbed_grid(args.side, p_delete=0.15, p_diag=0.10, rng=rng)
    # Opaque IDs: random, unguessable, no geometry.
    pool = set()
    while len(pool) < h.number_of_nodes():
        pool.add(f"{rng.getrandbits(40):010x}")
    pool = sorted(pool)
    rng.shuffle(pool)
    ids = dict(zip(sorted(h), pool))
    for _ in range(2000):
        s = rng.choice(sorted(h))
        ds = nx.single_source_shortest_path_length(h, s)
        if len(ds) < 0.95 * h.number_of_nodes() or max(ds.values()) < args.dmax + 8:
            continue
        # keep s away from the boundary: the ball of radius dmax+3 must look interior
        if sum(1 for d in ds.values() if d <= args.dmax + 3) < 1.6 * (args.dmax + 3) ** 2:
            continue
        cands = [v for v, d in ds.items() if args.dmin <= d <= args.dmax]
        rng.shuffle(cands)
        if args.rule == "union2":
            got = pick_union(h, s, ds, cands, args)
            if got:
                t, T = got
                depth, width = depth_width(h, s, T)
                return h, ids, s, t, T, depth, width, None
            continue
        for t in cands[:200]:
            T = interval(h, s, t, ds)
            depth, width = depth_width(h, s, T)
            if not (args.kmin <= len(T) <= args.kmax and width >= args.wmin):
                continue
            n_calls = canonical_calls(h, s, t, T)
            return h, ids, s, t, T, depth, width, n_calls
    return None


def pick_union(h, s, ds, cands, args):
    """Two end nodes whose intervals branch apart: small overlap, neither end inside the other's
    interval, each interval non-trivial (not a bare path)."""
    good = []
    for t in cands[:300]:
        I = interval(h, s, t, ds)
        if 12 <= len(I) <= args.kmax and depth_width(h, s, I)[1] >= 3:
            good.append((t, I))
    for i, (t1, I1) in enumerate(good):
        for t2, I2 in good[i + 1:]:
            if t1 in I2 or t2 in I1:
                continue
            U = I1 | I2
            if not (args.kmin <= len(U) <= args.kmax):
                continue
            if len(I1 & I2) > 0.35 * min(len(I1), len(I2)):
                continue
            if depth_width(h, s, U)[1] < args.wmin:
                continue
            return (t1, t2), U
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--seed", type=int, default=20261125)
    ap.add_argument("--side", type=int, default=40)
    ap.add_argument("--dmin", type=int, default=8)
    ap.add_argument("--dmax", type=int, default=11)
    ap.add_argument("--kmin", type=int, default=20)
    ap.add_argument("--kmax", type=int, default=40)
    ap.add_argument("--wmin", type=int, default=4)
    ap.add_argument("--budget", type=int, default=150, help="evaluate-call budget")
    ap.add_argument("--rule", choices=["interval", "union2"], default="interval")
    a = ap.parse_args()

    got = None
    seed = a.seed
    while got is None:
        got = pick(seed, a)
        seed += 1
    h, ids, s, t, T, depth, width, n_calls = got
    if n_calls is not None and n_calls > a.budget // 2:
        print(f"warning: reference needs {n_calls} calls, more than half the budget {a.budget}")

    inst = {
        "start": ids[s],
        "rule": a.rule,
        "hidden_ends": [ids[x] for x in (t if isinstance(t, tuple) else (t,))],
        "target": sorted(ids[v] for v in T),
        "nodes": sorted(ids[v] for v in h),
        "edges": sorted(sorted((ids[u], ids[v])) for u, v in h.edges()),
        "eval_budget": a.budget,
        "wl_iterations": 3,
        "meta": {"n": h.number_of_nodes(), "m": h.number_of_edges(), "d_st": depth,
                 "target_size": len(T), "target_width": width,
                 "reference_eval_calls": n_calls, "generator_seed": seed - 1},
    }
    task = Path(a.task)
    for p in [task / "environment/oracle/instance.json", task / "tests/instance.json"]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(inst))
    print(json.dumps(inst["meta"], indent=1))


if __name__ == "__main__":
    main()
