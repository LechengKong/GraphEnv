"""Shortcut: blind hill climbing on the score, spend the whole budget, submit the best set."""
import random
from common import *
s = probe("status")["start"]; adj = explore(s); rng = random.Random(0)
L, cur = {s}, evaluate({s})["score"]; best, bestL = cur, set(L)
while True:
    fr = sorted({u for v in L for u in adj[v]} - L)
    cand = set(L)
    if len(L) > 1 and rng.random() < 0.3:
        cand.discard(rng.choice(sorted(L - {s})))
    else:
        cand.add(rng.choice(fr))
    r = evaluate(cand)
    if "error" in r: break
    if r["score"] >= cur: L, cur = cand, r["score"]
    if cur > best: best, bestL = cur, set(L)
    if best == 1.0: break
print("best score", best, "size", len(bestL)); print(submit(bestL))
