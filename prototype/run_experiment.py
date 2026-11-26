"""Calibration: how many evaluate calls do blind searches need to reach f = 1?

Usage: uv run python run_experiment.py [--per-cell N] [--budget B] [--out results.jsonl]
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from concurrent.futures import ProcessPoolExecutor

from core import WLScorer, depth_width, grow_target, interval_target, make_host
from solvers import SOLVERS

HOSTS = ["grid", "geo"]
SIZES = [10, 20, 30, 45]
ALPHAS = [-1.0, 0.0, 2.0]          # wide / neutral / deep targets (random targets)
SIZE_BANDS = [(10, 19), (20, 34), (35, 60)]   # interval targets
ROUNDINGS = [None, 0.05]


def run_one(job):
    host_kind, k, alpha, seed, budget, target = job
    rng = random.Random(seed)
    h = make_host(host_kind, rng)
    extra = {}
    if target == "random":
        s = rng.choice(sorted(h))
        T = grow_target(h, s, k, alpha, rng)
        solvers = {n: v for n, v in SOLVERS.items() if n != "interval_enum"}
    else:
        kmin, kmax = k
        while True:
            s = rng.choice(sorted(h))
            got = interval_target(h, s, rng, kmin, kmax)
            if got:
                break
        T, t = got
        st = h.subgraph(T)
        extra = dict(band=f"{kmin}-{kmax}", dist=depth_width(h, s, T)[0],
                     is_path=st.number_of_edges() == len(T) - 1 and max(dict(st.degree()).values()) <= 2)
        solvers = SOLVERS
    depth, width = depth_width(h, s, T)
    rows = []
    for (sname, solver), rnd in itertools.product(solvers.items(), ROUNDINGS):
        f = WLScorer(h, s, T, round_to=rnd)
        res = solver(h, s, f, budget, random.Random(seed + 1))
        rows.append(dict(host=host_kind, k=len(T), alpha=alpha, seed=seed, depth=depth,
                         width=width, solver=sname, rounding=rnd or 0.0, target=target, **extra, **res))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-cell", type=int, default=6)
    ap.add_argument("--budget", type=int, default=20000)
    ap.add_argument("--out", default="results.jsonl")
    ap.add_argument("--workers", type=int, default=30)
    ap.add_argument("--target", choices=["random", "interval"], default="random")
    a = ap.parse_args()
    off = lambda hk: 0 if hk == "grid" else 500000
    if a.target == "random":
        jobs = [(hk, k, al, 1000 * i + 17 * k + int(10 * al) + off(hk), a.budget, "random")
                for hk, k, al in itertools.product(HOSTS, SIZES, ALPHAS) for i in range(a.per_cell)]
    else:
        jobs = [(hk, b, 0.0, 7000 * i + 31 * b[0] + off(hk), a.budget, "interval")
                for hk, b in itertools.product(HOSTS, SIZE_BANDS) for i in range(a.per_cell)]
    with open(a.out, "w") as fh, ProcessPoolExecutor(a.workers) as ex:
        for i, rows in enumerate(ex.map(run_one, jobs)):
            for r in rows:
                fh.write(json.dumps(r) + "\n")
            fh.flush()
            if i % 20 == 0:
                print(f"{i + 1}/{len(jobs)} instances done", flush=True)


if __name__ == "__main__":
    main()
