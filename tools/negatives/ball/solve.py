"""Plausible wrong hypothesis: the target is a ball {v : d(start, v) <= r}."""
from common import *
s = probe("status")["start"]; adj = explore(s); d = bfs(adj, s)
best = (-1, None)
for r in range(0, 30):
    B = {v for v, x in d.items() if x <= r}
    if len(B) > 200: break
    sc = evaluate(B)["score"]; print(r, len(B), sc)
    best = max(best, (sc, r))
r = best[1]; print("submit radius", r, submit({v for v, x in d.items() if x <= r}))
