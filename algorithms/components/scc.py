# ============================================================
# algorithms/components/scc.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def strongly_connected_components(graph: "Graph", source: int = None) -> List[Dict]:
    """
    Find all Strongly Connected Components (SCCs) in a directed graph.

    A strongly connected component is a maximal subgraph in which every
    node is reachable from every other node.

    Recommended algorithm: Kosaraju's (two DFS passes) or Tarjan's
    (single DFS with a stack and low-link values).

    Parameters
    ----------
    graph  : Graph       – the input graph (must be directed)
    source : int | None  – unused; accepted for API consistency

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - VISIT_NODE         : first DFS pass node discovery
        - PROCESS_NODE       : first DFS pass node finish
        - NEW_COMPONENT      : start of a new SCC
        - ADD_TO_COMPONENT   : node assigned to the current SCC
        - TRAVERSE_EDGE      : traversal along an edge

    Complexity (Tarjan / Kosaraju)
    --------------------------------
    Time  : O(V + E)
    Space : O(V)

    Raises
    ------
    NotImplementedError
        Placeholder — to be implemented by the algorithm team.
    """
    raise NotImplementedError(
        "strongly_connected_components() has not been implemented yet."
    )
