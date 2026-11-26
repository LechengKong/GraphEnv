# Design: why the tasks look the way they do

This records the reasoning behind the hidden-pattern probe tasks, in the order the decisions were
made. The original v0 proposal is in [`env-design-v0.md`](env-design-v0.md). The measurements
behind each decision are in [`results.md`](results.md).

## 1. The capability being targeted

Agents do well when all the information is in front of them. They are much weaker at the loop
science and debugging depend on: propose a hypothesis, choose an experiment, interpret the
result, revise, and decide when to stop. Realistic benchmarks contain that loop, but they don't
let you vary its difficulty independently, and they don't give clean ground truth.

The task isolates the loop. The agent explores a hidden structure and gets feedback from a score
it doesn't understand. It must infer both what the score measures and what rule produced the
target.

## 2. Each simpler design has a shortcut

| Design | Shortcut |
|---|---|
| Show the graph and ask for the target | A coding exercise: breadth-first search plus an isomorphism check |
| Write the graph as prose | Extract the edges into a file, then run code |
| Score each node, unlimited queries | Submit every node and keep the best |
| Score a list by its best member | Split in half and keep the better half: about log n queries |
| Score a list by overlap with the target | Toggle one node at a time: membership is revealed in about n queries (the Mastermind and coin-weighing argument) |
| A score that ignores identities, and nothing else | The answer is not identifiable: every copy of the shape ties |
| Tell the agent the target is a shortest-path set | Enumerate about n candidates: a coding exercise again |

What survives:
- **The score ignores identities.** It compares the *shape* of the induced subgraph, rooted at
  the start node, with the target's. Toggling nodes reveals nothing about which nodes are in the
  target, so membership can't be decoded.
- **The target comes from a hidden rule.** The agent is told only that the target is "defined by
  a simple rule relative to the start item and the way items are linked".
- **The answer is unique.** No other set in the graph has the target's rooted shape, so a score
  of 1.0 is reached only by the target (see §6).
- **The `evaluate` calls are budgeted.**

## 3. The score: rooted Weisfeiler-Lehman cosine

The score is WL subtree features (3 rounds, with the start node labelled differently) compared by
cosine similarity, capped at 0.99 for anything that is not an exact rooted isomorphism. An exact
check returns 1.0.

- **It's cheap and smooth.** It gives partial credit, so experiments are informative.
- **It's identity-blind by construction.**
- **It's learnable.** Small probes (single items, pairs, stars) produce clean, interpretable values.
  That turned out to be decisive: every successful agent run reverse-engineered the kernel from
  such probes.
- **It's misleading at the top.** A 174-node ball scores 0.94 against a 29-node target, so
  "close" scores mislead hill-climbing and naive agents.

## 4. Why a rule, and why shortest-path sets

**Random targets don't work.** Prototyping with random connected targets showed that blind search
fails at sizes of 20 or more (0% at 20k calls), but there is also nothing to *reason* about. The
score is flat near the top, and no strategy beats search. That fails the fairness bar:
difficulty would come from missing information, not from investigation.

**So the target needs structure that reasoning can exploit.** We use
Interval(s, t) = {v : d(s,v) + d(v,t) = d(s,t)}, every node on some shortest path from the start
s to a hidden end node t.
- It's natural and short, so it is fair to call it "a simple rule".
- It isn't the first thing an agent tries. Balls, layers and neighbourhoods come first.
- Once hypothesized, it is very cheap to confirm.

**The calibration on 72 targets shows a gap.** Blind search solves 0 to 8%. A solver that knows
the rule family and enumerates end nodes solves 100%, with a median of 265 calls.

**A score-aware reference closes most of the gap.** The best-first solver with angular pruning
uses the bound

    angle(c, T) >= |angle(e, T) - angle(c, e)|

and needs a median of 3 calls (at most 5 over 40 instances). The cosine score is extremely
informative once the hypothesis class is known. That is why a budget of 150 is generous for
reasoning and hopeless for search.

## 5. Variants

- **`hidden-pattern-probe`:** one interval, unlimited `neighbors`, 150 `evaluate` calls. Opus 5.5
  solves 5/10, Haiku 5.5 0/5. This is the calibrated task.
- **`hidden-pattern-probe-budget`:** a fresh instance, with `neighbors` capped at 350 distinct
  items (about 22% of the graph; expanding everything within the target's depth needs 257).
  It tests deciding where to explore before knowing what you're looking for. Opus 0/5: every run
  under-explored, and one tested the correct rule only on its explored region and rejected it.
- **`hidden-pattern-probe-union`** (not submitted): the target is
  Interval(s, t1) ∪ Interval(s, t2). The reference still needs about 5 calls (20/20). Opus 0/4,
  with one run reaching the single-interval hypothesis and stalling there. A real step beyond the
  single-interval task, but currently too hard to be informative.

## 6. Grading and uniqueness

Two grading choices were considered:
- **(A) Accept any set rooted-isomorphic to T.** This is fair, and it is what the verifier checks.
- **(B) Require exactly T.** This needs a tie-break when copies exist. Under a hidden rule, that
  tie-break grades the agent on our grammar, not on its reasoning.

The resolution: generate until **T is the only induced rooted copy of its shape in the whole
graph**. Any rooted copy lies within the target's depth of s, so searching that ball is
exhaustive (`tools/check_unique.py`). Then (A) and (B) coincide, a score of 1.0 certifies the
answer, and "accept materially different valid solutions" holds trivially.

Measurement: only 28/72 random interval instances are unique even among intervals. Uniqueness is
a filter, and a cheap one for a single fixed instance.

## 7. Infrastructure: keeping the hidden information hidden

- **The `oracle` is a Compose sidecar** that holds the instance and serves `/neighbors`,
  `/evaluate`, `/submit` and `/status`. It enforces the budgets and the seen-items rule, and logs
  to its own `/state`.
- **The agent's container (`main`) has only the `probe` client.** It never holds hidden data.
- **The verifier runs in a separate container** built from `tests/`. Harbor collects `/state` from
  the oracle service as an artifact and re-materializes it in the verifier. The agent can't read
  the instance and can't forge the record. Tampering QC confirms this: forged state and a planted
  reward file are ignored.

## 8. Calibration levers, and what we learned about each

| Lever | Effect |
|---|---|
| `evaluate` budget | Successful Opus runs used 80 to 109 calls; the reference uses about 4. Lowering it to about 75 would cut the Opus pass rate. |
| Score precision | Rounding to 0.05 made blind search much worse in the prototype. It would also slow the reverse-engineering of the kernel that every success relied on. Re-verify the reference first. |
| Rule family | The union of two intervals is much harder (0/4). Other families: k-hop layers, intersections, cores of a ball. |
| Exploration budget | Effective, and it tests a different skill. Combined with a 30-minute timeout it was too hard for Opus (0/5). |
| Timeout | It binds for strong agents that commit to brute-force fitting. 3 of 5 Opus failures on task 1 were timeouts. |
| Prose surface | Not built. It only adds difficulty if relations are implicit. Otherwise a regex extracts the edges. It must be checked by parsing the text back into the original edge set. |
| Realistic framing | Considered: hospital incident response, where the score is a pseudonymized footprint match. It makes the shortest-path rule guessable and requires exact grading. Shelved in favour of the abstract probe. |

## 9. Real-world analogues

The task is a controlled probe of a loop that real tasks contain, not a realistic task itself.
The identity-blind score is engineered.

| Domain | Structure | Target | Signal |
|---|---|---|---|
| Code impact analysis | Call graph | Functions on call paths from an entry point to a change | Coverage or tests |
| Security attack paths | Active Directory or network graph | Hosts on shortest paths from a foothold to assets (BloodHound) | Anonymized telemetry |
| Chemistry | Molecules | A substructure | Morgan/ECFP fingerprint similarity, which is a WL kernel |
| Math and science | Computable examples | A hidden law | A similarity measure you must reverse-engineer |
