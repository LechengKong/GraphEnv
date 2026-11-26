"""Summarize results.jsonl: solve rates and call counts by solver x rounding x size x shape."""
import json
import sys
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rows = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else "results.jsonl")]
SHAPE = {-1.0: "wide", 0.0: "neutral", 2.0: "deep"}


def summarize(keyf, title):
    g = defaultdict(list)
    for r in rows:
        g[keyf(r)].append(r)
    print(f"\n== {title}")
    print(f"{'group':<45}{'n':>4}{'solved':>8}{'median calls (solved)':>24}{'median best (unsolved)':>25}")
    for k in sorted(g, key=str):
        rs = g[k]
        sol = [r["calls"] for r in rs if r["solved"]]
        uns = [r["best"] for r in rs if not r["solved"]]
        print(f"{str(k):<45}{len(rs):>4}{len(sol) / len(rs):>8.0%}"
              f"{(np.median(sol) if sol else float('nan')):>24.0f}"
              f"{(np.median(uns) if uns else float('nan')):>25.3f}")


summarize(lambda r: (r["solver"], r["rounding"]), "solver x rounding")
summarize(lambda r: (r["solver"], r["rounding"], r["k"]), "by target size")
summarize(lambda r: (r["solver"], r["rounding"], SHAPE[r["alpha"]]), "by target shape")
summarize(lambda r: (r["solver"], r["rounding"], r["host"]), "by host family")

# Cumulative solve rate vs budget, per solver x rounding x size.
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
budget = max(r["calls"] for r in rows)
xs = np.logspace(1, np.log10(budget), 200)
for ax, rnd in zip(axes, sorted({r["rounding"] for r in rows})):
    for solver, ls in [("hill_climb", "-"), ("tabu_steepest", "--")]:
        for k, c in zip(sorted({r["k"] for r in rows}), plt.cm.viridis(np.linspace(0, 0.85, 4))):
            rs = [r for r in rows if r["solver"] == solver and r["rounding"] == rnd and r["k"] == k]
            if not rs:
                continue
            calls = np.array([r["calls"] if r["solved"] else np.inf for r in rs])
            ax.plot(xs, [(calls <= x).mean() for x in xs], ls, color=c, label=f"{solver} |T|={k}")
    ax.set_xscale("log")
    ax.set_title(f"score rounding = {rnd or 'none'}")
    ax.set_xlabel("evaluate calls (budget)")
    ax.grid(alpha=0.3)
axes[0].set_ylabel("fraction of instances solved (f = 1)")
axes[1].legend(fontsize=7, loc="upper left")
fig.tight_layout()
fig.savefig("solve_vs_budget.png", dpi=130)
print("\nwrote solve_vs_budget.png")
