# GraphEnv

A generator and calibration pipeline for **hidden-pattern probe** tasks: agentic evaluation tasks
that isolate the hypothesis-testing loop. The agent explores a hidden graph, gets feedback from an
identity-blind structural similarity score, and has to infer both what the score measures and
which rule produced the target.

The submitted task instances live in [SPInference](https://github.com/LechengKong/SPInference).
This repo holds everything used to design, generate, calibrate and validate them.

- [`docs/design.md`](docs/design.md): why the tasks look the way they do. The shortcut each
  simpler design allows, the choice of score and rule, uniqueness, the infrastructure, the
  calibration levers.
- [`docs/results.md`](docs/results.md): every measurement. Blind-search baselines, the reference
  solver, Harbor QC, agent pass rates and failure modes.
- [`docs/harbor-notes.md`](docs/harbor-notes.md): Harbor features used, running agents on
  Bedrock, and the gotchas we hit.
- [`docs/env-design-v0.md`](docs/env-design-v0.md): the original proposal.

## Layout

```
prototype/   calibration experiments: host graphs, targets, the WL scorer, blind solvers
             (core.py, solvers.py, run_experiment.py, analyze*.py, multiplicity.py, results)
tools/       instance pipeline and evaluation tooling
  make_instance.py     generate host graph, start, hidden end node(s) and target;
                       writes the instance to a task's oracle and verifier dirs
  check_unique.py      exhaustive check that the target is the only rooted copy of its shape
  offline_solve.py     run the reference solver offline against an instance
  sweep_reference.py   reference solver across many generated instances
  negatives/           shortcut and wrong attempts (hill climb, ball, single path, tampering)
  run_harbor.sh, run_agent.sh, make_variant.sh, aws_env.py   Harbor and Bedrock runners
  collect_results.py   jobs/ -> results/trials.csv and trajectory summaries
  summarize_traj.py    print an agent's text and commands from a trajectory
tasks/       Harbor task packages built during development
  hidden-pattern-probe         single interval, unlimited exploration
  hidden-pattern-probe-budget  single interval, 350-item exploration budget (submitted)
  hidden-pattern-probe-union   union of two intervals (not submitted)
results/     trials.csv (every Harbor trial) and per-trial trajectory summaries
```

## Pipeline

```bash
uv sync --project prototype                     # networkx, numpy, matplotlib

# 1. generate an instance (rule: interval | union2) into a task package
uv run --project prototype python tools/make_instance.py --task tasks/<slug> --seed 777
#    union:   --rule union2 --dmin 7 --dmax 11 --kmin 30 --kmax 60 --wmin 5

# 2. require uniqueness: the target must be the only rooted copy of its shape
uv run --project prototype python tools/check_unique.py tasks/<slug>/tests/instance.json

# 3. confirm the reference solves it well inside the budget
uv run --project prototype python tools/offline_solve.py tasks/<slug>/tests/instance.json

# 4. Harbor QC (canonical, no-op, wrong attempts), then agent trials
TASK=tasks/<slug> tools/run_harbor.sh <job> -a oracle
TASK=tasks/<slug> tools/run_agent.sh <job> us.anthropic.claude-opus-5-5 5
python3 tools/collect_results.py
```

## Headline results

| Task | Opus 5.5 | Haiku 5.5 | Reference solver |
|---|---|---|---|
| Single interval, unlimited exploration | 5/10 | 0/5 | 4 `evaluate` calls |
| Single interval, 350-item exploration budget | 0/5 | 0/5 | 4 calls, 350 lookups |
| Union of two intervals | 0/4 | – | 5 calls |

Blind search on the same targets: 0 to 8% solved even with 20,000 `evaluate` calls.
