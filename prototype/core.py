"""Core pieces for the shape-inference prototype: host graphs, targets, and the WL scorer."""
from __future__ import annotations

import random
from collections import Counter, deque

import networkx as nx
import numpy as np
from networkx.algorithms.isomorphism import GraphMatcher


# --------------------------------------------------------------------------- host graphs

def perturbed_grid(side: int, p_delete: float, p_diag: float, rng: random.Random) -> nx.Graph:
    """2D grid with random edge deletions and random diagonals; largest component kept."""
    g = nx.grid_2d_graph(side, side)
    for e in list(g.edges()):
        if rng.random() < p_delete:
            g.remove_edge(*e)
    for x in range(side - 1):
        for y in range(side - 1):
            if rng.random() < p_diag:
                g.add_edge((x, y), (x + 1, y + 1))
            if rng.random() < p_diag:
                g.add_edge((x + 1, y), (x, y + 1))
    g = g.subgraph(max(nx.connected_components(g), key=len)).copy()
    return nx.convert_node_labels_to_integers(g)


def geometric(n: int, avg_deg: float, rng: random.Random) -> nx.Graph:
    radius = (avg_deg / (np.pi * n)) ** 0.5
    g = nx.random_geometric_graph(n, radius, seed=rng.randrange(2**31))
    g = g.subgraph(max(nx.connected_components(g), key=len)).copy()
    return nx.convert_node_labels_to_integers(g)


def make_host(kind: str, rng: random.Random) -> nx.Graph:
    if kind == "grid":
        return perturbed_grid(45, p_delete=0.15, p_diag=0.10, rng=rng)
    if kind == "geo":
        return geometric(2000, avg_deg=6.0, rng=rng)
    raise ValueError(kind)


# --------------------------------------------------------------------------- targets

def grow_target(h: nx.Graph, s: int, k: int, alpha: float, rng: random.Random) -> set[int]:
    """Random connected set of size k containing s.

    Frontier nodes are chosen with weight (1 + d(s, v))**alpha: alpha > 0 favours deep,
    thin targets; alpha < 0 favours shallow, wide ones.
    """
    dist = nx.single_source_shortest_path_length(h, s, cutoff=k)
    chosen = {s}
    frontier = set(h[s])
    while len(chosen) < k and frontier:
        fl = sorted(frontier)
        w = [(1 + dist[v]) ** alpha for v in fl]
        v = rng.choices(fl, weights=w)[0]
        chosen.add(v)
        frontier.discard(v)
        frontier.update(u for u in h[v] if u not in chosen)
    return chosen


def interval(h: nx.Graph, s: int, t: int, ds: dict | None = None) -> set[int]:
    """Shortest-path subgraph: {v : d(s,v) + d(v,t) = d(s,t)}."""
    ds = ds if ds is not None else nx.single_source_shortest_path_length(h, s)
    dt = nx.single_source_shortest_path_length(h, t, cutoff=ds[t])
    return {v for v, d in dt.items() if v in ds and ds[v] + d == ds[t]}


def interval_target(h: nx.Graph, s: int, rng: random.Random, kmin: int = 10, kmax: int = 60,
                    tries: int = 500) -> tuple[set[int], int] | None:
    """Pick a hidden t with kmin <= |Interval(s,t)| <= kmax. Returns (T, t) or None."""
    ds = nx.single_source_shortest_path_length(h, s)
    cands = [v for v, d in ds.items() if d >= 3]
    for _ in range(tries):
        t = rng.choice(cands)
        T = interval(h, s, t, ds)
        if kmin <= len(T) <= kmax:
            return T, t
    return None


def depth_width(h: nx.Graph, s: int, nodes: set[int]) -> tuple[int, int]:
    """Depth and width measured inside the induced shape (distance from s within H[T])."""
    d = nx.single_source_shortest_path_length(h.subgraph(nodes), s)
    layers = Counter(d.values())
    return max(d.values()), max(layers.values())


# --------------------------------------------------------------------------- scorer

class WLScorer:
    """Rooted WL-subtree cosine similarity against a fixed target, with an exact iso check.

    Labels are compressed through a dictionary shared across all calls, so feature
    indices are comparable between the target and any query.
    """

    def __init__(self, h: nx.Graph, s: int, target: set[int], iters: int = 3,
                 round_to: float | None = None):
        self.h, self.s, self.iters, self.round_to = h, s, iters, round_to
        self._labels: dict = {}
        self.calls = 0
        self.target_nodes = frozenset(target)
        self.t_graph = self._shape(target)
        self.t_feat = self._features(self.t_graph)
        self.t_norm = np.sqrt(sum(v * v for v in self.t_feat.values()))

    def _shape(self, nodes) -> nx.Graph:
        g = self.h.subgraph(nodes).copy()
        for v in g:
            g.nodes[v]["root"] = v == self.s
        return g

    def _compress(self, key) -> int:
        lab = self._labels.get(key)
        if lab is None:
            lab = self._labels[key] = len(self._labels)
        return lab

    def _features(self, g: nx.Graph) -> Counter:
        lab = {v: self._compress(("r", g.nodes[v]["root"])) for v in g}
        feat = Counter(lab.values())
        for _ in range(self.iters):
            lab = {v: self._compress((lab[v], tuple(sorted(lab[u] for u in g[v])))) for v in g}
            feat.update(lab.values())
        return feat

    def raw(self, nodes) -> float:
        """Uncounted, unrounded score (used for diagnostics only)."""
        g = self._shape(nodes)
        f = self._features(g)
        dot = sum(c * self.t_feat.get(k, 0) for k, c in f.items())
        norm = np.sqrt(sum(c * c for c in f.values()))
        cos = dot / (norm * self.t_norm)
        if cos > 1 - 1e-12 and g.number_of_nodes() == self.t_graph.number_of_nodes():
            gm = GraphMatcher(g, self.t_graph, node_match=lambda a, b: a["root"] == b["root"])
            return 1.0 if gm.is_isomorphic() else 0.99
        return min(cos, 0.99)

    def __call__(self, nodes) -> float:
        self.calls += 1
        v = self.raw(nodes)
        if self.round_to and v < 1.0:
            v = min(np.floor(v / self.round_to) * self.round_to, 0.99)
        return float(v)
