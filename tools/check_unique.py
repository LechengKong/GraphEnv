"""Private: verify the target is the only induced rooted copy of its shape, and report ball sizes.
Usage: python tools/check_unique.py <instance.json>"""
import json, sys, time
from collections import Counter
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
inst = json.load(open(sys.argv[1]))
g = nx.Graph(); g.add_nodes_from(inst["nodes"]); g.add_edges_from(inst["edges"]); s = inst["start"]
T = set(inst["target"])
P = g.subgraph(T).copy()
depth = max(nx.single_source_shortest_path_length(P, s).values())
ds = nx.single_source_shortest_path_length(g, s)
B = g.subgraph([v for v, d in ds.items() if d <= depth]).copy()   # any rooted copy lies within this ball
for H in (B, P):
    for v in H: H.nodes[v]["root"] = v == s
t0 = time.time(); others = 0
for m in GraphMatcher(B, P, node_match=lambda a, b: a["root"] == b["root"]).subgraph_isomorphisms_iter():
    if set(m) != T:
        others += 1; break
print(f"|T|={len(T)} depth={depth} unique={others == 0} ({time.time()-t0:.0f}s)")
hdist = max(ds[v] for v in T)
cum = 0; layers = Counter(ds.values())
print("host distance of farthest target item:", hdist)
print("items within radius r (expansions needed to know all distances up to r+1 = items within r):",
      {r: sum(c for d, c in layers.items() if d <= r) for r in range(hdist - 2, hdist + 4)})
