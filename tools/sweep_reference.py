import sys, types, random, statistics
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "prototype"), str(ROOT / "tools"), str(ROOT / "tasks/hidden-pattern-probe/solution")]
import make_instance as mi
from core import WLScorer
from solve import solve, solve_union
from concurrent.futures import ProcessPoolExecutor
RULE = sys.argv[1] if len(sys.argv) > 1 else "interval"
A = types.SimpleNamespace(side=40, dmin=8, dmax=11, kmin=20, kmax=40, wmin=4, rule=RULE) if RULE == "interval" else types.SimpleNamespace(side=40, dmin=7, dmax=11, kmin=30, kmax=60, wmin=5, rule=RULE)
def one(seed):
    got = mi.pick(seed, A)
    if not got: return None
    h, ids, s, t, T, depth, width, naive = got
    class C: pass
    c = C(); f = WLScorer(h, s, T); c.evaluate = f
    found, calls = (solve_union if RULE == "union2" else solve)(c, s, g=h, log=lambda m: None)
    return (found is not None and f.raw(found) == 1.0, calls, naive)
with ProcessPoolExecutor(20) as ex:
    res = [r for r in ex.map(one, range(1000, 1040 if RULE == "interval" else 1020)) if r]
calls = sorted(r[1] for r in res)
print("solved", sum(r[0] for r in res), "/", len(res))
print("smart calls: median", statistics.median(calls), "p90", calls[int(.9*len(calls))], "max", max(calls))
if res[0][2] is not None: print("naive calls: median", statistics.median(r[2] for r in res), "max", max(r[2] for r in res))
