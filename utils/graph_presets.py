# ============================================================
# utils/graph_presets.py — Popular graph topology generators
# ============================================================
#
# Each generator receives a Graph instance (already cleared) and
# a (cx, cy) canvas centre point, then populates it with nodes
# and edges arranged in a visually clean layout.
#
# All positions are in graph-space (no pan offset applied here;
# the caller centres around the visible canvas midpoint).
# ============================================================

from __future__ import annotations
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def _ring(n: int, cx: int, cy: int, r: int) -> list[tuple[int, int]]:
    """Return n evenly-spaced points around a circle."""
    positions = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2   # start at top
        positions.append((int(cx + r * math.cos(angle)),
                          int(cy + r * math.sin(angle))))
    return positions


# ------------------------------------------------------------------
# Presets
# ------------------------------------------------------------------

def gen_dijkstra_shortest_path(graph: "Graph", cx: int, cy: int) -> None:
    """Weighted graph for testing Dijkstra's algorithm (shortest path)."""
    positions = _ring(6, cx, cy, 120)
    ids = [graph.add_node(x, y) for x, y in positions]
    # Create edges with weights
    edges = [
        (ids[0], ids[1], 4),
        (ids[0], ids[2], 2),
        (ids[1], ids[2], 1),
        (ids[1], ids[3], 5),
        (ids[2], ids[3], 8),
        (ids[2], ids[4], 10),
        (ids[3], ids[4], 2),
        (ids[3], ids[5], 6),
        (ids[4], ids[5], 3),
    ]
    for src, dest, w in edges:
        graph.add_edge(src, dest, w)


def gen_prim_mst(graph: "Graph", cx: int, cy: int) -> None:
    """Weighted graph for testing Prim's MST algorithm."""
    positions = _ring(6, cx, cy, 120)
    ids = [graph.add_node(x, y) for x, y in positions]
    edges = [
        (ids[0], ids[1], 7),
        (ids[0], ids[2], 5),
        (ids[1], ids[2], 8),
        (ids[1], ids[3], 7),
        (ids[2], ids[3], 15),
        (ids[2], ids[4], 6),
        (ids[3], ids[4], 5),
        (ids[3], ids[5], 1),
        (ids[4], ids[5], 2),
    ]
    for src, dest, w in edges:
        graph.add_edge(src, dest, w)


def gen_bfs_traversal(graph: "Graph", cx: int, cy: int) -> None:
    """Connected graph for testing BFS traversal."""
    # Create a simple tree structure
    positions = [
        (cx, cy - 100),        # 0 (root)
        (cx - 80, cy - 20),    # 1 (left child)
        (cx + 80, cy - 20),    # 2 (right child)
        (cx - 120, cy + 60),   # 3
        (cx - 40, cy + 60),    # 4
        (cx + 40, cy + 60),    # 5
        (cx + 120, cy + 60),   # 6
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    edges = [
        (ids[0], ids[1]),
        (ids[0], ids[2]),
        (ids[1], ids[3]),
        (ids[1], ids[4]),
        (ids[2], ids[5]),
        (ids[2], ids[6]),
    ]
    for src, dest in edges:
        graph.add_edge(src, dest)


def gen_coloring_welsh_powell(graph: "Graph", cx: int, cy: int) -> None:
    """Graph for testing graph coloring (Welsh-Powell algorithm)."""
    # Create an undirected graph with varying degrees
    positions = [
        (cx - 100, cy - 80),   # 0
        (cx - 50, cy - 80),    # 1
        (cx + 50, cy - 80),    # 2
        (cx + 100, cy - 80),   # 3
        (cx - 75, cy + 60),    # 4
        (cx + 75, cy + 60),    # 5
        (cx, cy + 120),        # 6
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    edges = [
        (ids[0], ids[1]),
        (ids[0], ids[4]),
        (ids[1], ids[2]),
        (ids[1], ids[4]),
        (ids[2], ids[3]),
        (ids[2], ids[5]),
        (ids[3], ids[5]),
        (ids[4], ids[6]),
        (ids[5], ids[6]),
        (ids[0], ids[2]),
    ]
    for src, dest in edges:
        graph.add_edge(src, dest)


def gen_eulerian_circuit(graph: "Graph", cx: int, cy: int) -> None:
    """Eulerian graph for testing Eulerian circuit/path algorithm."""
    # Create a simple graph where ALL vertices have even degree (Eulerian circuit exists)
    positions = [
        (cx - 100, cy - 60),   # 0
        (cx + 100, cy - 60),   # 1
        (cx + 100, cy + 60),   # 2
        (cx - 100, cy + 60),   # 3
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    # Create edges so each vertex has degree 2 (Eulerian circuit)
    edges = [
        (ids[0], ids[1]),
        (ids[1], ids[2]),
        (ids[2], ids[3]),
        (ids[3], ids[0]),
    ]
    for src, dest in edges:
        graph.add_edge(src, dest)


def gen_connected_components_graph(graph: "Graph", cx: int, cy: int) -> None:
    """Graph with multiple connected components."""
    # Component 1 (left)
    comp1_pos = [(cx - 150, cy - 80), (cx - 100, cy), (cx - 150, cy + 80)]
    comp1_ids = [graph.add_node(x, y) for x, y in comp1_pos]
    graph.add_edge(comp1_ids[0], comp1_ids[1])
    graph.add_edge(comp1_ids[1], comp1_ids[2])
    
    # Component 2 (middle)
    comp2_pos = [(cx, cy - 80), (cx + 50, cy), (cx, cy + 80), (cx + 100, cy)]
    comp2_ids = [graph.add_node(x, y) for x, y in comp2_pos]
    graph.add_edge(comp2_ids[0], comp2_ids[1])
    graph.add_edge(comp2_ids[1], comp2_ids[2])
    graph.add_edge(comp2_ids[2], comp2_ids[3])
    graph.add_edge(comp2_ids[3], comp2_ids[0])
    
    # Component 3 (right - single isolated node)
    graph.add_node(cx + 180, cy)


def gen_scc_directed_graph(graph: "Graph", cx: int, cy: int) -> None:
    """Directed graph for testing strongly connected components."""
    positions = [
        (cx - 120, cy - 60),   # 0
        (cx, cy - 60),         # 1
        (cx + 120, cy - 60),   # 2
        (cx - 120, cy + 60),   # 3
        (cx, cy + 60),         # 4
        (cx + 120, cy + 60),   # 5
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    # Create strongly connected components
    edges = [
        (ids[0], ids[1]),
        (ids[1], ids[0]),  # SCC: {0, 1}
        (ids[1], ids[2]),
        (ids[2], ids[1]),  # SCC: {1, 2}
        (ids[3], ids[4]),
        (ids[4], ids[5]),
        (ids[5], ids[3]),  # SCC: {3, 4, 5}
        (ids[2], ids[5]),  # Edge from one SCC to another
    ]
    for src, dest in edges:
        graph.add_edge(src, dest)


def _ring_rotated(n, cx, cy, r, offset_angle=0.0):
    positions = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2 + offset_angle
        positions.append((int(cx + r * math.cos(angle)),
                          int(cy + r * math.sin(angle))))
    return positions


# ------------------------------------------------------------------
# Dispatcher
# ------------------------------------------------------------------

_GENERATORS = {
    "dijkstra_shortest_path":    gen_dijkstra_shortest_path,
    "prim_mst":                  gen_prim_mst,
    "bfs_traversal":             gen_bfs_traversal,
    "coloring_welsh_powell":     gen_coloring_welsh_powell,
    "eulerian_circuit":          gen_eulerian_circuit,
    "connected_components_graph": gen_connected_components_graph,
    "scc_directed_graph":        gen_scc_directed_graph,
}


def generate_preset(key: str, graph: "Graph", cx: int, cy: int) -> None:
    """
    Populate *graph* with the named preset, centred at (cx, cy).

    Parameters
    ----------
    key   : one of the keys in GRAPH_PRESETS (from widgets.py)
    graph : a freshly-cleared Graph instance
    cx,cy : canvas centre in graph-space
    """
    fn = _GENERATORS.get(key)
    if fn is None:
        raise ValueError(f"Unknown graph preset: {key!r}")
    fn(graph, cx, cy)
