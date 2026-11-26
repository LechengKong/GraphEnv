"""How many other t' give an interval with the same rooted shape as the hidden target?"""
import json, random, sys
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
from core import make_host, interval, interval_target

def rooted(h, s, nodes):
    g = h.subgraph(nodes).copy()
    for v in g: g.nodes[v]["r"] = str(v == s)
    return g

rows = [json.loads(l) for l in open("results_interval.jsonl")]
inst = {(r["host"], r["seed"]): r for r in rows if r["solver"] == "interval_enum" and r["rounding"] == 0}
out = []
for (host, seed), r in sorted(inst.items()):
    rng = random.Random(seed); h = make_host(host, rng)
    kmin, kmax = map(int, r["band"].split("-"))
    while True:
        s = rng.choice(sorted(h)); got = interval_target(h, s, rng, kmin, kmax)
        if got: break
    T, t = got
    gT = rooted(h, s, T); hT = nx.weisfeiler_lehman_graph_hash(gT, node_attr="r", iterations=4)
    ds = nx.single_source_shortest_path_length(h, s)
    same = 0
    for u in ds:
        if u == t or ds[u] != ds[t]: continue
        I = interval(h, s, u, ds)
        if len(I) != len(T): continue
        g = rooted(h, s, I)
        if nx.weisfeiler_lehman_graph_hash(g, node_attr="r", iterations=4) == hT and \
           GraphMatcher(g, gT, node_match=lambda a, b: a["r"] == b["r"]).is_isomorphic():
            same += 1
    out.append((host, r["band"], same))
    print(host, r["band"], "other t' with same shape:", same, flush=True)
import collections
u = sum(1 for o in out if o[2] == 0)
print(f"\nunique among intervals: {u}/{len(out)}")
for k in ["grid", "geo"]:
    print(k, collections.Counter(min(o[2], 5) for o in out if o[0] == k))
