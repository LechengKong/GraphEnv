"""Grade the submission recorded by the oracle.

Correct  <=>  the submitted set, as an induced subgraph with the start node marked, is
isomorphic to the hidden target (rooted isomorphism): the same criterion under which the
service's `evaluate` returns 1.0. In this instance the target is the only set of items with
that property, so this is equivalent to submitting exactly the target. Order and duplicates
in the submission are irrelevant (the service records it as a sorted set).
"""
import argparse
import json
import os

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher


def rooted(g, s, nodes):
    sub = g.subgraph(nodes).copy()
    for v in sub:
        sub.nodes[v]["root"] = v == s
    return sub


def grade(state, inst):
    sub_path = os.path.join(state, "submission.json")
    if not os.path.exists(sub_path):
        return 0.0, {"reason": "no submission"}
    nodes = json.load(open(sub_path))["nodes"]
    g = nx.Graph()
    g.add_nodes_from(inst["nodes"])
    g.add_edges_from(inst["edges"])
    if not set(nodes) <= set(g):
        return 0.0, {"reason": "submission contains unknown IDs"}
    evals, expanded = 0, set()
    log_path = os.path.join(state, "log.jsonl")
    if os.path.exists(log_path):
        for line in open(log_path):
            e = json.loads(line)
            if e.get("op") == "evaluate":
                evals += 1
            elif e.get("op") == "neighbors":
                expanded.add(e.get("node"))
    if evals > inst["eval_budget"]:
        return 0.0, {"reason": "evaluate budget exceeded", "evaluate_used": evals}
    nb_budget = inst.get("neighbors_budget")
    if nb_budget is not None and len(expanded) > nb_budget:
        return 0.0, {"reason": "neighbors budget exceeded", "neighbors_used": len(expanded)}
    s = inst["start"]
    a, b = rooted(g, s, nodes), rooted(g, s, inst["target"])
    ok = (len(a) == len(b) and a.number_of_edges() == b.number_of_edges()
          and GraphMatcher(a, b, node_match=lambda x, y: x["root"] == y["root"]).is_isomorphic())
    info = {"submitted_size": len(nodes), "target_size": len(b), "evaluate_used": evals,
            "neighbors_used": len(expanded),
            "exact_target_set": sorted(nodes) == sorted(inst["target"]),
            "reason": "pattern match" if ok else "pattern mismatch"}
    return (1.0 if ok else 0.0), info


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", default="/state")
    ap.add_argument("--instance", default="/tests/instance.json")
    ap.add_argument("--out", default="/logs/verifier")
    a = ap.parse_args()
    reward, info = grade(a.state, json.load(open(a.instance)))
    os.makedirs(a.out, exist_ok=True)
    open(os.path.join(a.out, "reward.txt"), "w").write(f"{reward}\n")
    json.dump(info, open(os.path.join(a.out, "details.json"), "w"), indent=1)
    print(json.dumps({"reward": reward, **info}))
