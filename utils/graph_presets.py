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

def gen_complete_k5(graph: "Graph", cx: int, cy: int) -> None:
    """Complete graph K₅ — 5 nodes, every pair connected."""
    positions = _ring(5, cx, cy, 110)
    ids = [graph.add_node(x, y) for x, y in positions]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            graph.add_edge(ids[i], ids[j])


def gen_petersen(graph: "Graph", cx: int, cy: int) -> None:
    """Petersen graph — 10 nodes, classic non-planar graph."""
    outer = _ring(5, cx, cy, 130)
    inner = _ring(5, cx, cy, 65)
    # rotate inner ring by 36° for standard Petersen look
    inner = _ring_rotated(5, cx, cy, 65, offset_angle=math.pi / 5)

    out_ids = [graph.add_node(x, y) for x, y in outer]
    inn_ids = [graph.add_node(x, y) for x, y in inner]

    # Outer pentagon
    for i in range(5):
        graph.add_edge(out_ids[i], out_ids[(i + 1) % 5])
    # Spokes
    for i in range(5):
        graph.add_edge(out_ids[i], inn_ids[i])
    # Inner pentagram (skip-1 connections)
    for i in range(5):
        graph.add_edge(inn_ids[i], inn_ids[(i + 2) % 5])


def _ring_rotated(n, cx, cy, r, offset_angle=0.0):
    positions = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2 + offset_angle
        positions.append((int(cx + r * math.cos(angle)),
                          int(cy + r * math.sin(angle))))
    return positions


def gen_star_s7(graph: "Graph", cx: int, cy: int) -> None:
    """Star graph S₇ — central hub connected to 7 leaves."""
    hub = graph.add_node(cx, cy)
    leaves = _ring(7, cx, cy, 120)
    for x, y in leaves:
        leaf_id = graph.add_node(x, y)
        graph.add_edge(hub, leaf_id)


def gen_cycle_c8(graph: "Graph", cx: int, cy: int) -> None:
    """Cycle C₈ — 8-node ring."""
    positions = _ring(8, cx, cy, 120)
    ids = [graph.add_node(x, y) for x, y in positions]
    for i in range(len(ids)):
        graph.add_edge(ids[i], ids[(i + 1) % len(ids)])


def gen_grid_3x3(graph: "Graph", cx: int, cy: int) -> None:
    """3×3 grid / lattice graph — 9 nodes."""
    spacing = 90
    rows, cols = 3, 3
    grid: dict[tuple[int, int], int] = {}
    ox = cx - (cols - 1) * spacing // 2
    oy = cy - (rows - 1) * spacing // 2
    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing
            y = oy + r * spacing
            grid[(r, c)] = graph.add_node(x, y)
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                graph.add_edge(grid[(r, c)], grid[(r, c + 1)])
            if r + 1 < rows:
                graph.add_edge(grid[(r, c)], grid[(r + 1, c)])


def gen_bin_tree(graph: "Graph", cx: int, cy: int) -> None:
    """Complete binary tree with 4 levels (15 nodes)."""
    levels = 4
    v_gap  = 70
    top_y  = cy - (levels - 1) * v_gap // 2
    nodes: dict[int, int] = {}   # tree_index → graph_id

    def add(idx: int, x: int, y: int) -> None:
        nodes[idx] = graph.add_node(x, y)

    # Level 0: root
    add(1, cx, top_y)

    for lvl in range(1, levels):
        count    = 2 ** lvl
        h_span   = min(count * 60, 500)
        step     = h_span // count if count > 1 else 0
        start_x  = cx - h_span // 2 + step // 2
        y        = top_y + lvl * v_gap
        for pos in range(count):
            idx = 2 ** lvl + pos
            x   = start_x + pos * step
            add(idx, x, y)
            parent_idx = idx // 2
            graph.add_edge(nodes[parent_idx], nodes[idx])


def gen_bipartite(graph: "Graph", cx: int, cy: int) -> None:
    """Complete bipartite K₃,₄ — two groups, all cross-edges."""
    left_n, right_n = 3, 4
    v_gap   = 70
    h_gap   = 160

    left_ids  = []
    right_ids = []

    left_top  = cy - (left_n  - 1) * v_gap // 2
    right_top = cy - (right_n - 1) * v_gap // 2

    for i in range(left_n):
        left_ids.append(graph.add_node(cx - h_gap, left_top  + i * v_gap))
    for i in range(right_n):
        right_ids.append(graph.add_node(cx + h_gap, right_top + i * v_gap))

    for l in left_ids:
        for r in right_ids:
            graph.add_edge(l, r)


def gen_path_p8(graph: "Graph", cx: int, cy: int) -> None:
    """Path graph P₈ — 8 nodes in a straight chain."""
    n      = 8
    h_gap  = 80
    start_x = cx - (n - 1) * h_gap // 2
    ids = [graph.add_node(start_x + i * h_gap, cy) for i in range(n)]
    for i in range(len(ids) - 1):
        graph.add_edge(ids[i], ids[i + 1])


# ------------------------------------------------------------------
# Dispatcher
# ------------------------------------------------------------------

_GENERATORS = {
    "complete_k5": gen_complete_k5,
    "petersen":    gen_petersen,
    "star_s7":     gen_star_s7,
    "cycle_c8":    gen_cycle_c8,
    "grid_3x3":    gen_grid_3x3,
    "bin_tree":    gen_bin_tree,
    "bipartite":   gen_bipartite,
    "path_p8":     gen_path_p8,
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
