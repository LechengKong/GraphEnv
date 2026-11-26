"""Near miss: right idea (shortest paths to a hidden end item) but only ONE path per end item."""
from common import *
s = probe("status")["start"]; adj = explore(s); d = bfs(adj, s)
def one_path(t):
    p = [t]
    while p[-1] != s:
        v = p[-1]; p.append(min(u for u in adj[v] if d.get(u, 1e9) == d[v] - 1))
    return set(p)
# a path's shape depends only on its length: one evaluate per distance
best = (-1, None)
for k in range(1, 30):
    t = min(v for v, x in d.items() if x == k)
    sc = evaluate(one_path(t))["score"]; print(k, sc); best = max(best, (sc, t))
print(submit(one_path(best[1])))
