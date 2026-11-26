"""Run the reference solver offline against the instance JSON (or many generated instances)."""
import json, random, sys
from pathlib import Path
import networkx as nx
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "prototype"), str(ROOT / "tasks/hidden-pattern-probe/solution")]
import time
from core import WLScorer
from solve import solve, solve_union

class Local:
    def __init__(self, g, s, T): self.f = WLScorer(g, s, T)
    def neighbors(self, v): return list(self.g[v])
    def evaluate(self, nodes): return self.f(nodes)

def from_instance(path):
    inst = json.load(open(path))
    g = nx.Graph(); g.add_nodes_from(inst["nodes"]); g.add_edges_from(inst["edges"])
    return g, inst["start"], set(inst["target"]), inst

if __name__ == "__main__":
    g, s, T, inst = from_instance(sys.argv[1])
    c = Local(g, s, T); c.g = g
    t0 = time.time()
    fn = solve_union if inst.get("rule") == "union2" else solve
    found, calls = fn(c, s, g=g, log=lambda m: None)
    print(f"solver time {time.time() - t0:.0f}s")
    ok = found is not None and c.f.raw(found) == 1.0
    print(f"solved={ok} calls={calls} budget={inst['eval_budget']} rule={inst.get('rule')} |T|={len(T)}")
