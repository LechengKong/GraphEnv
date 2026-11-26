"""Summarize interval-target results."""
import json
import sys
from collections import defaultdict

import numpy as np

rows = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else "results_interval.jsonl")]


def table(keyf, title):
    g = defaultdict(list)
    for r in rows:
        g[keyf(r)].append(r)
    print(f"\n== {title}")
    print(f"{'group':<42}{'n':>4}{'solved':>8}{'calls p50':>11}{'calls p90':>11}"
          f"{'best (unsolved)':>17}")
    for k in sorted(g, key=str):
        rs = g[k]
        sol = [r["calls"] for r in rs if r["solved"]]
        uns = [r["best"] for r in rs if not r["solved"]]
        p = lambda q: f"{np.percentile(sol, q):.0f}" if sol else "-"
        print(f"{str(k):<42}{len(rs):>4}{len(sol) / len(rs):>8.0%}{p(50):>11}{p(90):>11}"
              f"{(f'{np.median(uns):.3f}' if uns else '-'):>17}")


table(lambda r: (r["solver"], r["rounding"]), "solver x rounding")
table(lambda r: (r["solver"], r["rounding"], r["band"]), "by target size band")
table(lambda r: (r["solver"], r["rounding"], r["host"]), "by host family")

inst = {(r["host"], r["seed"]): r for r in rows}.values()
print("\n== instance properties")
print(f"is_path: {np.mean([r['is_path'] for r in inst]):.0%}   "
      f"d(s,t) median {np.median([r['dist'] for r in inst]):.0f}   "
      f"width median {np.median([r['width'] for r in inst]):.0f} (max {max(r['width'] for r in inst)})")
ex = [r["expanded"] for r in rows if r["solver"] == "interval_enum" and r["solved"]]
print(f"interval_enum nodes expanded (ball up to d(s,t)): median {np.median(ex):.0f}, p90 {np.percentile(ex, 90):.0f}")
