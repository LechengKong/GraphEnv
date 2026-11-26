"""Collect every Harbor trial under jobs/ into results/trials.csv plus short per-trial
trajectory summaries (agent text only) under results/trajectories/."""
import csv, json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
JOBS, OUT = ROOT / "jobs", ROOT / "results"
(OUT / "trajectories").mkdir(parents=True, exist_ok=True)
rows = []
for res in sorted(JOBS.glob("**/result.json")):
    trial = res.parent
    if not (trial / "trial.log").exists() or not (trial / "config.json").exists():
        continue                                    # job-level result.json
    r = json.load(open(res)); cfg = json.load(open(trial / "config.json"))
    agent = (cfg.get("agent") or {}); task = (cfg.get("task") or {})
    log = trial / "artifacts/state/log.jsonl"
    L = [json.loads(l) for l in open(log)] if log.exists() else []
    ev = [e["score"] for e in L if e.get("op") == "evaluate"]
    det = json.load(open(trial / "verifier/details.json")) if (trial / "verifier/details.json").exists() else {}
    row = dict(job=trial.parent.name, trial=trial.name,
               task=Path(str(task.get("path", ""))).name,
               agent=agent.get("name"), model=agent.get("model_name"),
               reward=((r.get("verifier_result") or {}).get("rewards") or {}).get("reward"),
               exception=(r.get("exception_info") or {}).get("exception_type"),
               evaluate_calls=len(ev), best_score=max(ev) if ev else None,
               neighbors_distinct=len({e["node"] for e in L if e.get("op") == "neighbors"}),
               submitted_size=det.get("submitted_size"), verdict=det.get("reason"),
               started=r.get("started_at"), finished=r.get("finished_at"))
    rows.append(row)
    tj = trial / "agent/trajectory.json"
    if tj.exists():
        t = json.load(open(tj))
        with open(OUT / "trajectories" / f"{row['job']}__{trial.name}.md", "w") as fh:
            fh.write(f"# {row['job']} / {trial.name}\n\nmodel={row['model']} reward={row['reward']} "
                     f"exception={row['exception']} evaluate={row['evaluate_calls']} best={row['best_score']}\n\n")
            for st in t.get("steps", []):
                if st.get("source") != "agent":
                    continue
                if st.get("message"):
                    fh.write(f"**agent:** {st['message'].strip()}\n\n")
                for tc in st.get("tool_calls") or []:
                    cmd = str((tc.get("arguments") or {}).get("command", ""))[:600]
                    if cmd:
                        fh.write("```bash\n" + cmd + "\n```\n\n")
with open(OUT / "trials.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "trials ->", OUT / "trials.csv")
