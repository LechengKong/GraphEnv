# Graph rule-induction task: a controlled probe for exploration and hypothesis testing

**Problem.** Agents do well when all the information is in front of them. They do much worse on
the loop that science and debugging depend on: guess a hypothesis, choose an experiment,
interpret the result, revise, and decide when to stop. Realistic benchmarks such as SWE-bench,
ALFWorld and Sokoban contain this loop. They don't let you vary its difficulty independently,
and they don't give you clean ground truth.

**Proposal.** The agent starts at a node s of a hidden graph and explores it one node at a time.
It must submit the **exact set of nodes** produced by a hidden structural rule anchored at s. Its
only feedback is a score that compares **shapes** and ignores node identities. That rules out
decoding the answer from the score, and finding the right shape isn't enough to pass. The agent
has to hypothesize the rule.

**What it measures.**
- **Depth:** how many hops the agent can chain.
- **Width:** how many nodes it can track at once, such as every predecessor in a layer.
- **Closure:** knowing what it hasn't checked.
- **Rule induction:** choosing which hypothesis explains the feedback.

Each of these has its own setting.

---

## 1. Task definition (v0)

### Instance
An instance is (H, s, r\*). Only s is revealed to the agent.
- **H = (V, E):** an undirected, unweighted, connected graph with n = |V| between 10³ and 10⁵.
  Node IDs are random opaque strings, so they can't be guessed.
- **s ∈ V:** the start node, given to the agent.
- **r\*:** a hidden rule. The target is T = r\*(H, s), a subset of V that always contains s.

### Rule grammar R (v0)
Every rule is anchored at s and produces a connected set.

| Rule | Output | Length |
|---|---|---|
| `Path(t)` | The shortest s–t path. The generator only picks t that have exactly one. | 1 |
| `Interval(t)` | {v : d(s,v) + d(v,t) = d(s,t)}, the shortest-path subgraph | 1 |
| `Ball(r)` | {v : d(s,v) ≤ r} | 1 |
| `Union(Interval(t₁), Interval(t₂))` | The union of the two intervals | 3 |

A rule's length counts its constructors; parameters don't count.

### Definitions
- **Shape of a set L:** the induced subgraph H[L], with s marked if s ∈ L. "Induced" means it
  keeps every edge of H between nodes in L.
- **Discovered node:** s, or any node returned by an earlier `neighbors` call.
- **Rooted isomorphism:** an isomorphism between two shapes that maps the marked s to the
  marked s.

### What the agent knows at the start
- The ID of s, and the three tools below.
- This statement: "T is a set of nodes containing s, produced by a short structural rule of the
  graph. If several sets score 1, the one produced by the shortest rule is correct."
- It is **not** told R. An easier tier (Tier 0) discloses R.

### Tools
1. **`neighbors(v)`** returns v's neighbour IDs. v must be a discovered node; otherwise the call
   returns an error.
2. **`evaluate(L)`** returns f(L), a number between 0 and 1.
   - L is a list of discovered IDs, treated as a set: order and duplicates are ignored.
   - L must have between 1 and 200 nodes.
3. **`submit(L)`** ends the episode and can be called once.

There's no limit on `neighbors` or `evaluate` calls. The episode ends at `submit` or at a turn cap
(default 1,000 turns), and cost is reported.

### Score
- **f(L) = 1** if shape(L) and shape(T) are rooted-isomorphic, checked exactly with nauty.
- **Otherwise,** f(L) is the cosine similarity of the two shapes under a Weisfeiler–Lehman (WL)
  subtree kernel, capped at 0.99.

What this gives you:
- **No membership leaks.** The score depends only on shape, never on which nodes are submitted,
  so toggling nodes reveals nothing about membership.
- **The score can't certify the answer.** Every rooted copy of T's shape scores 1.
- **Close decoys still score below 1.** Shapes that WL can't tell apart from T's, but aren't
  isomorphic to it, score 0.99.

### Conditions for accepting a generated instance
1. **Size:** T has between 10 and 60 nodes.
2. **Identifiability:** no rule of length ≤ |r\*| produces a set other than T with f = 1. This
   makes T the unique simplest answer.
3. **Multiplicity:** at least D sets other than T score f = 1, with D = 100 by default. Find them
   by sampling rooted copies of T's shape that pass through s. This guarantees the score alone
   can't locate T.
4. **Recorded settings:**
   - depth, the largest d(s,v) over v ∈ T;
   - width, the largest layer of T;
   - the rule length |r\*|;
   - the multiplicity.

### Success and metrics
- **Success:** the submitted set equals T exactly.
- **Cost:** turns, `neighbors` calls, `evaluate` calls, and tokens.
- **Trap rate:** the share of failures whose submitted set scored f = 1. The agent got the shape
  right but the wrong rule or the wrong copy.
- **Shape-found rate:** the share of episodes where the agent reached f = 1 at any point. This
  separates "never found the shape" from "found the shape but couldn't locate T".

### Access conditions

| Condition | What the agent may use | What it measures |
|---|---|---|
| C0 | Only the three tools: no shell, no files, no subagents | Attention |
| C1 | The tools plus scratch files and Python, but the tools can't be called from code | An agent with external memory |
| C2 | The tools can be called from code | An upper bound |

The gap between C0 and C1 across the depth × width grid is a result in its own right: it shows
how much an external scratchpad adds to the agent's attention.

---

## 2. Why the design looks like this

Each simpler version had an attack that made it trivial.

| Design | Attack |
|---|---|
| Graph given explicitly, find the pair | It's a coding exercise: breadth-first search plus an isomorphism check. |
| Graph written as prose | The agent extracts the edges into a file, then runs code over them. |
| Score per node, unlimited queries | Submit every node and keep the best. |
| Submit a list, get the best score among its members | Split the list in half and keep the better half: about log n queries. |
| Submit a list, scored by overlap with the true set | Toggle one node at a time: membership is revealed in about n queries (the Mastermind and coin-weighing argument). |
| Score that ignores identities, nothing else | The answer can't be identified, because every copy of the shape ties. |
| Agent knows the target is SP(s,t) | Only n valid answers exist, so enumerate them all. |

The v0 design blocks each of these:
- the score ignores identities, which stops decoding node by node;
- the multiplicity condition means matching the shape isn't enough;
- the identifiability condition makes the answer well defined;
- the rule is hidden, so the valid answers can't be listed in advance.

**The general principle.** Without an explicit budget, the task stays hard only if blind search
costs exponentially many queries while reasoning costs polynomially many. Time and tokens are then
the natural limit.

---

## 3. How it corresponds to realistic tasks

| Abstract task | Code repair | ALFWorld | Sokoban |
|---|---|---|---|
| Node | A function or module | A location, object or object state | A board state |
| Neighbour query | Open a file, follow a reference | Go to, open or examine something | Make a move or push |
| Depth | Hops from symptom to root cause | Number of subgoals | Length of the solution |
| Width | Callers or paths to account for | Candidate places the object could be | Box and position combinations in play |
| Proxy score | Visible tests passed | Subgoals completed | Boxes on goals, or heuristic distance |
| Decoy (score 1, wrong) | A patch that only passes the visible tests | The right object in the wrong state | A deadlocked state |
| Closure | No other caller is still broken | Every receptacle checked | No deadlock, or no shorter solution |

Two places where they differ, each worth making a setting:
- **Access mode.** Code allows jumping to any node. ALFWorld requires walking, and Sokoban
  requires walking with some moves that can't be undone.
- **Goal type.** Here the goal depends on structure across many nodes. Planning tasks usually
  define the goal as a property of the final state.

**The code-repair version** generates a codebase from the hidden graph. The bug sits at the root
cause and reaches the symptom along every shortest path. Visible tests cover only some of those
paths, while hidden tests cover all of them, plus some code outside the subgraph.

---

## 4. Validation plan

A claim that this "resembles realistic tasks" needs evidence. Two options:
1. **Correlation after controlling for general capability.** Raw correlation in agent rankings is
   weak evidence, because nearly all benchmarks track general capability. Test whether this task
   predicts SWE-bench, ALFWorld or Sokoban performance beyond a general capability score.
2. **Predicting specific failures.** Test whether high depth, high width or more decoys predict
   the corresponding failure types on the realistic benchmarks: stopping too early, missing a
   caller, or patching the symptom instead of the root cause.

**For training (if used for RL):**
- Reward exact match, never the score.
- Vary the surface form (abstract graph, prose, code, grid world), so the model learns behaviours
  rather than the specific algorithm.
- Use a curriculum over depth, width, multiplicity and rule length.

---

## 5. Related work to position against

- **Graph reasoning over graphs in context:**
  - OpenAI Graphwalks (2025), breadth-first search and parent-finding over an edge list;
  - NLGraph (Wang et al., 2023);
  - "Talk like a graph" (Fatemi et al., 2023).
- **Multi-hop question answering over synthetic documents:** BABILong, MuSiQue. These ask for one
  chain, not every shortest chain plus proof that no shorter one exists.
- **Rule induction:** ARC. ARC gives fixed examples; this task is an active version in which the
  agent chooses its own probes.
- **Experimental design and discovery:** BoxingGym (2025), DiscoveryWorld (2024), ScienceWorld
  (2022).
- **Proxy scores in program repair:** overfitting patches (Qi et al., 2015, the Kali study; Smith
  et al., 2015), SWE-bench audits of "resolved" patches, and SWE-smith (2025) for bug injection.
- **Black-box query complexity:** Mastermind and coin weighing, and black-box complexity in
  evolutionary computation (OneMax, Royal Road, NK landscapes).
- **Mechanisms behind the depth and width framing:**
  - the reversal curse (Berglund et al., 2023) and the two-hop curse (Balesni et al., 2024);
  - feed-forward layers as key–value memories (Geva et al., 2021);
  - in-context learning as an implicit weight update (Dherin et al., 2025).

---

## 6. Open choices

| Choice | Default | Alternative and trade-off |
|---|---|---|
| Disclose R | No | Disclose it (Tier 0). With R hidden, "shortest rule" is judged by our grammar, so an agent with a different notion of simplicity may pick a different set that also scores 1. |
| Exact-match signal | None, so the agent has to choose among sets that score 1 | f = 1 only for T. Easier, and removes the decision about when to stop. |
| Score function | WL cosine: cheap, but some shapes tie | Normalized graph edit distance: smoother, more expensive to compute. |
| Graph family | Grid-like or geometric, which gives many copies of a shape | Expanders: few copies, so the shape nearly pins T down. |
| Surface form | Abstract IDs | Nodes carry prose, and structure has to be read out of it. |
| Grammar size | 4 rules | Add intersections, k-hop layers, breadth-first trees, or several endpoints. |
