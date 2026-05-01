# ============================================================
# algorithms/coloring/welsh_powell.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph

from animation.events import make_step, VISIT_NODE, COLOR_NODE


def welsh_powell(graph: "Graph", source: int = None) -> List[Dict]:
    """
    Colour the graph's nodes using the Welsh-Powell greedy algorithm.

    Welsh-Powell is a greedy graph colouring heuristic that produces good
    (though not necessarily optimal) colourings.  Nodes are sorted in
    decreasing order of degree, then colours are assigned greedily: for
    each node, assign the smallest colour index not already used by any
    of its neighbours.

    Parameters
    ----------
    graph  : Graph       – the input graph (undirected)
    source : int | None  – unused; accepted for API consistency

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - VISIT_NODE   : when a node is about to be coloured
        - COLOR_NODE   : when a colour is assigned (payload includes ``color`` index)

    Notes
    -----
    The number of colours used is the chromatic number estimate for this
    ordering.  The actual chromatic number (NP-hard in general) may be lower.

    Complexity
    ----------
    Time  : O(V² + E)  (dominated by the sorting + neighbour checks)
    Space : O(V)
    """
    steps: List[Dict] = []

    if not graph.nodes:
        return steps

    # Build a SYMMETRIC adjacency set regardless of graph.directed.
    # Colouring is inherently an undirected concept: if u and v share an edge
    # they must receive different colours no matter which direction the edge
    # was stored in.  Without always adding BOTH directions, a neighbour that
    # was coloured before the current node may be invisible in neighbour_colors,
    # letting the same colour be reused on adjacent nodes.
    adj: Dict[int, set] = {nid: set() for nid in graph.nodes} # {1:{} , 2:{} ... }
    for src, dest, _ in graph.edges:
        adj[src].add(dest)
        adj[dest].add(src)   # always symmetric — this is the critical fix

    # Sort nodes by degree descending (Welsh-Powell ordering)
    sorted_nodes = sorted(graph.nodes.keys(), key=lambda n: len(adj[n]), reverse=True)

    # color_map: node_id -> assigned color index
    color_map: Dict[int, int] = {}

    for node in sorted_nodes:
        # Emit VISIT_NODE before attempting to colour
        steps.append(make_step(VISIT_NODE, node=node))

        # Collect colors already used by neighbours
        neighbour_colors = {color_map[nb] for nb in adj[node] if nb in color_map}

        # Find the smallest non-negative integer not in neighbour_colors
        color = 0
        while color in neighbour_colors:
            color += 1

        color_map[node] = color

        # Emit COLOR_NODE with the assigned color index
        steps.append(make_step(COLOR_NODE, node=node, color=color))

    return steps