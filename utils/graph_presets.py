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
    """Complex weighted graph for testing Dijkstra's algorithm (shortest path)."""
    positions = [
        (cx - 120, cy - 100),  # 0
        (cx - 50, cy - 100),   # 1
        (cx + 50, cy - 100),   # 2
        (cx + 120, cy - 100),  # 3
        (cx - 100, cy),        # 4
        (cx, cy),              # 5
        (cx + 100, cy),        # 6
        (cx - 70, cy + 100),   # 7
        (cx + 70, cy + 100),   # 8
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    edges = [
        (ids[0], ids[1], 7),
        (ids[0], ids[4], 3),
        (ids[1], ids[2], 5),
        (ids[1], ids[5], 6),
        (ids[2], ids[3], 4),
        (ids[2], ids[6], 8),
        (ids[3], ids[6], 2),
        (ids[4], ids[5], 4),
        (ids[4], ids[7], 9),
        (ids[5], ids[6], 3),
        (ids[5], ids[8], 7),
        (ids[6], ids[8], 5),
        (ids[7], ids[8], 6),
        (ids[1], ids[4], 2),
        (ids[2], ids[5], 3),
    ]
    for src, dest, w in edges:
        graph.add_edge(src, dest, w)


def gen_prim_mst(graph: "Graph", cx: int, cy: int) -> None:
    """Complex weighted graph for testing Prim's MST algorithm."""
    positions = [
        (cx - 120, cy - 80),   # 0
        (cx - 40, cy - 100),   # 1
        (cx + 50, cy - 80),    # 2
        (cx + 120, cy - 60),   # 3
        (cx - 100, cy + 20),   # 4
        (cx, cy + 40),         # 5
        (cx + 100, cy + 20),   # 6
        (cx - 60, cy + 120),   # 7
        (cx + 60, cy + 120),   # 8
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    edges = [
        (ids[0], ids[1], 9),
        (ids[0], ids[4], 7),
        (ids[1], ids[2], 8),
        (ids[1], ids[5], 10),
        (ids[2], ids[3], 6),
        (ids[2], ids[6], 7),
        (ids[3], ids[6], 5),
        (ids[4], ids[5], 3),
        (ids[4], ids[7], 8),
        (ids[5], ids[6], 4),
        (ids[5], ids[8], 9),
        (ids[6], ids[8], 5),
        (ids[7], ids[8], 7),
        (ids[0], ids[2], 11),
        (ids[3], ids[8], 12),
    ]
    for src, dest, w in edges:
        graph.add_edge(src, dest, w)


def gen_bfs_traversal(graph: "Graph", cx: int, cy: int) -> None:
    """Complex connected graph for testing BFS traversal (not used - kept for reference)."""
    # This will be replaced - keeping structure
    pass


def gen_coloring_welsh_powell(graph: "Graph", cx: int, cy: int) -> None:
    """Complex graph for testing graph coloring (Welsh-Powell algorithm)."""
    # Create a more intricate undirected graph with varying degrees
    positions = [
        (cx - 120, cy - 80),   # 0
        (cx - 60, cy - 100),   # 1
        (cx, cy - 120),        # 2
        (cx + 60, cy - 100),   # 3
        (cx + 120, cy - 80),   # 4
        (cx - 100, cy),        # 5
        (cx - 30, cy - 20),    # 6
        (cx + 30, cy - 20),    # 7
        (cx + 100, cy),        # 8
        (cx - 80, cy + 100),   # 9
        (cx, cy + 120),        # 10
        (cx + 80, cy + 100),   # 11
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    edges = [
        (ids[0], ids[1]),
        (ids[0], ids[5]),
        (ids[1], ids[2]),
        (ids[1], ids[6]),
        (ids[2], ids[3]),
        (ids[2], ids[7]),
        (ids[3], ids[4]),
        (ids[3], ids[8]),
        (ids[4], ids[8]),
        (ids[5], ids[6]),
        (ids[5], ids[9]),
        (ids[6], ids[7]),
        (ids[6], ids[10]),
        (ids[7], ids[8]),
        (ids[7], ids[11]),
        (ids[8], ids[11]),
        (ids[9], ids[10]),
        (ids[10], ids[11]),
        (ids[0], ids[4]),
        (ids[1], ids[3]),
        (ids[5], ids[8]),
        (ids[9], ids[11]),
    ]
    for src, dest in edges:
        graph.add_edge(src, dest)


def gen_eulerian_circuit(graph: "Graph", cx: int, cy: int) -> None:
    """Simpler Eulerian graph for testing Eulerian circuit/path algorithm."""
    # Create a simple graph where ALL vertices have even degree (degree 4)
    # This ensures an Eulerian circuit exists
    positions = [
        (cx - 100, cy - 80),   # 0
        (cx + 100, cy - 80),   # 1
        (cx + 100, cy + 80),   # 2
        (cx - 100, cy + 80),   # 3
        (cx, cy),              # 4 (center)
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    # Create edges so each vertex has even degree (Eulerian circuit exists)
    edges = [
        # Outer square
        (ids[0], ids[1]),
        (ids[1], ids[2]),
        (ids[2], ids[3]),
        (ids[3], ids[0]),
        # Center hub connections (each vertex connects to center)
        (ids[0], ids[4]),
        (ids[1], ids[4]),
        (ids[2], ids[4]),
        (ids[3], ids[4]),
    ]
    for src, dest in edges:
        graph.add_edge(src, dest)


def gen_connected_components_graph(graph: "Graph", cx: int, cy: int) -> None:
    """Complex graph with multiple connected components."""
    # Component 1 (left side - complex structure)
    comp1_pos = [
        (cx - 180, cy - 100),
        (cx - 120, cy - 100),
        (cx - 150, cy),
        (cx - 180, cy + 80),
        (cx - 120, cy + 80),
    ]
    comp1_ids = [graph.add_node(x, y) for x, y in comp1_pos]
    comp1_edges = [
        (comp1_ids[0], comp1_ids[1]),
        (comp1_ids[0], comp1_ids[2]),
        (comp1_ids[1], comp1_ids[2]),
        (comp1_ids[2], comp1_ids[3]),
        (comp1_ids[3], comp1_ids[4]),
        (comp1_ids[4], comp1_ids[1]),
    ]
    for src, dest in comp1_edges:
        graph.add_edge(src, dest)
    
    # Component 2 (middle - more complex)
    comp2_pos = [
        (cx - 40, cy - 120),
        (cx + 40, cy - 120),
        (cx, cy - 40),
        (cx - 60, cy + 40),
        (cx + 60, cy + 40),
        (cx, cy + 120),
    ]
    comp2_ids = [graph.add_node(x, y) for x, y in comp2_pos]
    comp2_edges = [
        (comp2_ids[0], comp2_ids[1]),
        (comp2_ids[0], comp2_ids[2]),
        (comp2_ids[1], comp2_ids[2]),
        (comp2_ids[2], comp2_ids[3]),
        (comp2_ids[2], comp2_ids[4]),
        (comp2_ids[3], comp2_ids[5]),
        (comp2_ids[4], comp2_ids[5]),
    ]
    for src, dest in comp2_edges:
        graph.add_edge(src, dest)
    
    # Component 3 (right - medium complexity)
    comp3_pos = [
        (cx + 140, cy - 80),
        (cx + 180, cy),
        (cx + 140, cy + 80),
    ]
    comp3_ids = [graph.add_node(x, y) for x, y in comp3_pos]
    comp3_edges = [
        (comp3_ids[0], comp3_ids[1]),
        (comp3_ids[1], comp3_ids[2]),
        (comp3_ids[2], comp3_ids[0]),
    ]
    for src, dest in comp3_edges:
        graph.add_edge(src, dest)


def gen_scc_directed_graph(graph: "Graph", cx: int, cy: int) -> None:
    """Complex directed graph for testing strongly connected components."""
    positions = [
        (cx - 140, cy - 80),   # 0
        (cx - 60, cy - 100),   # 1
        (cx + 60, cy - 100),   # 2
        (cx + 140, cy - 80),   # 3
        (cx - 100, cy + 20),   # 4
        (cx, cy),              # 5
        (cx + 100, cy + 20),   # 6
        (cx - 60, cy + 100),   # 7
        (cx + 60, cy + 100),   # 8
    ]
    ids = [graph.add_node(x, y) for x, y in positions]
    # Create multiple strongly connected components with some bridges
    edges = [
        # SCC 1: {0, 1, 2}
        (ids[0], ids[1]),
        (ids[1], ids[2]),
        (ids[2], ids[0]),
        # SCC 2: {3, 4, 5}
        (ids[3], ids[4]),
        (ids[4], ids[5]),
        (ids[5], ids[3]),
        # SCC 3: {6, 7, 8}
        (ids[6], ids[7]),
        (ids[7], ids[8]),
        (ids[8], ids[6]),
        # Bridges between SCCs
        (ids[2], ids[3]),
        (ids[5], ids[6]),
        # Additional internal edges for complexity
        (ids[0], ids[4]),
        (ids[1], ids[5]),
        (ids[4], ids[7]),
        (ids[8], ids[3]),
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
    "dijkstra_shortest_path":     gen_dijkstra_shortest_path,
    "prim_mst":                   gen_prim_mst,
    "coloring_welsh_powell":      gen_coloring_welsh_powell,
    "eulerian_circuit":           gen_eulerian_circuit,
    "connected_components_graph": gen_connected_components_graph,
    "scc_directed_graph":         gen_scc_directed_graph,
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
