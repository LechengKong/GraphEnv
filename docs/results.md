# Results

All numbers below come from this repo. Raw per-trial data is in
[`../results/trials.csv`](../results/trials.csv), and agent trajectories (agent text and commands)
are in [`../results/trajectories/`](../results/trajectories/).

## Prototype: blind search on random connected targets

144 instances on two host families (a perturbed 45×45 grid and a random geometric graph of 2k
nodes), with a 20k `evaluate` budget. The solvers see the whole graph, so this is an upper bound
on what blind search can do. Source: `prototype/run_experiment.py`, `analyze.py`.

| Target size | Hill climb, exact | Hill climb, rounded to 0.05 | Tabu, exact | Tabu, rounded to 0.05 |
|---|---|---|---|---|
| 10 | 72% | 58% | 33% | 14% |
| 20 | 25% | 0% | 3% | 0% |
| 30 | 3% | 0% | 8% | 0% |
| 45 | 0% | 0% | 0% | 0% |

Failed runs plateau at 0.96 to 0.98. See `prototype/solve_vs_budget.png`.

## Prototype: interval targets

72 instances in size bands 10–19, 20–34 and 35–60, with a 20k budget.

| Solver | Solved | Calls, median / 90th percentile |
|---|---|---|
| Hill climb (blind) | 8% | about 10k / 17k |
| Tabu (blind) | 1% | – |
| Enumerate end nodes, one call per distinct shape | **100%** | **265 / 727** |

Instance properties: 3% are pure paths, the median d(s,t) is 18, and the median width is 3. Only
28/72 targets are unique among intervals (`prototype/multiplicity.py`).

## Reference solver with angular pruning

Source: `tasks/*/solution/solve.py`, `tools/sweep_reference.py`.

| Rule | Instances | Solved | `evaluate` calls, median / max |
|---|---|---|---|
| Single interval | 40 | 40 | 3 / 5 |
| Union of two intervals | 20 | 20 | 5 / 6 |

## Harbor QC (submitted packages, in the SPInference repo)

| Check | `hidden-pattern-probe` | `hidden-pattern-probe-budget` |
|---|---|---|
| Canonical solution | 1.0 | 1.0 |
| No-op | 0.0 | 0.0 |
| Hill climb | 0.0 | 0.0 |
| Ball guess | 0.0 | 0.0 |
| Single path | 0.0 | 0.0 |
| Tampering | 0.0 | 0.0 |
| Grader unit tests | 7/7 | 9/9 |

## Agent trials (Claude Code on Bedrock)

| Task | Model | Valid trials | Solved | Notes |
|---|---|---|---|---|
| `hidden-pattern-probe` | Opus 5.5 | 10 | **5** | 3 timeouts, 2 wrong submissions; 1 API error excluded. Timeout 60 min (first 3 trials), then 30 min. |
| `hidden-pattern-probe` | Haiku 5.5 | 5 | 0 | Gave up after 10 to 14 minutes; 4/5 never submitted |
| `hidden-pattern-probe-budget` | Opus 5.5 | 5 | 0 | All timed out (30 min); used 95 to 210 of 350 lookups |
| `hidden-pattern-probe-budget` | Haiku 5.5 | 5 | 0 | – |
| `hidden-pattern-probe-union` | Opus 5.5 | 4 | 0 | 3 timeouts (60 min); one reached the single-interval hypothesis |

### How successful runs solved it (Opus, task 1)
1. Crawl the whole graph with free `neighbors` calls.
2. Probe the score with single items, pairs and stars, and find it is not overlap.
3. Fit a WL kernel model (3 rounds, root-labelled, global cosine) that reproduces every observed
   score.
4. Infer target facts from the model: |T| = 29, and the start has 2 neighbours inside T.
5. Test rule families offline against all observations. The shortest-path set to `7718202434`
   fits, and is confirmed with one `evaluate` call.

The successful runs used 80 to 109 `evaluate` calls.

### Failure modes
- **Never modelling the score.** The agent submits the best-scoring ball (0.95 to 0.97). This was
  2 of the Opus failures on task 1.
- **Committing to brute-force reconstruction.** The agent anneals over node sets against noisy
  observations: 80 parallel processes on 2 CPUs, then waits until the timeout. This was 3 of the
  Opus failures on task 1.
- **Giving up early with budget left.** All Haiku runs.
- **Under-exploring under a budget,** then rejecting the correct rule because it was tested on an
  incomplete region. The budget task.
- **Stopping one inference short.** On the union task, the agent finds the single-interval family
  but never considers two end nodes.
