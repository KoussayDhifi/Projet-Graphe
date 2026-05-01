# ============================================================
# algorithms/mst/prim.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING, Tuple
import heapq

if TYPE_CHECKING:
    from core.graph import Graph


def prim(graph: "Graph", source: int = 0) -> List[Dict]:
    """
    Compute a Minimum Spanning Tree using Prim's algorithm.

    Prim's algorithm grows the MST from a starting node by repeatedly
    selecting the minimum-weight edge that connects a node inside the
    current tree to a node outside it.  A priority queue (min-heap) is
    used to track candidate edges efficiently.

    Parameters
    ----------
    graph  : Graph  – the input graph (undirected, weighted)
    source : int    – the node from which to grow the MST (default 0)

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - VISIT_NODE    : when a node is added to the growing MST
        - EXPLORE_EDGE  : when a neighbour edge is considered
        - SELECT_EDGE   : when the minimum edge is chosen
        - REJECT_EDGE   : when an edge leads to an already-visited node
        - FINAL_TREE    : at the end, containing all MST edges

    Complexity
    ----------
    Time  : O((V + E) log V) with a binary heap
    Space : O(V)

    Raises
    ------
    NotImplementedError
        Placeholder — to be implemented by the algorithm team.
    """
    steps: List[Dict] = []

    if graph.node_count() == 0:
        return [{"type": "final_tree", "edges": []}]

    if source not in graph.nodes:
        source = next(iter(graph.nodes))

    visited = set([source])
    mst_edges: List[Tuple[int, int]] = []

    steps.append({"type": "visit_node", "node": source})

    heap: List[Tuple[float, int, int]] = []
    for neighbor, weight in graph.neighbors(source):
        steps.append({"type": "explore_edge", "src": source, "dest": neighbor})
        heapq.heappush(heap, (weight, source, neighbor))

    while heap:
        weight, src, dest = heapq.heappop(heap)
        if dest in visited:
            steps.append({"type": "reject_edge", "src": src, "dest": dest})
            continue

        visited.add(dest)
        mst_edges.append((src, dest))
        steps.append({"type": "select_edge", "src": src, "dest": dest})
        steps.append({"type": "visit_node", "node": dest})

        for neighbor, w in graph.neighbors(dest):
            steps.append({"type": "explore_edge", "src": dest, "dest": neighbor})
            if neighbor not in visited:
                heapq.heappush(heap, (w, dest, neighbor))
            else:
                steps.append({"type": "reject_edge", "src": dest, "dest": neighbor})

    steps.append({"type": "final_tree", "edges": mst_edges})
    return steps
