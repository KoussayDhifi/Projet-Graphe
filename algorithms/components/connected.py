# ============================================================
# algorithms/components/connected.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def connected_components(graph: "Graph", source: int = None) -> List[Dict]:
    """
    Find all connected components in an undirected graph.

    Uses repeated BFS or DFS from unvisited nodes to discover and label
    each component.  Each component is identified by a zero-based integer ID.

    Parameters
    ----------
    graph  : Graph       – the input graph (should be undirected)
    source : int | None  – unused; accepted for API consistency

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - NEW_COMPONENT      : signals the start of a new component
        - ADD_TO_COMPONENT   : adds a node to the current component
        - VISIT_NODE         : optional — when a node is first reached
        - TRAVERSE_EDGE      : optional — when moving to a neighbour

    Complexity
    ----------
    Time  : O(V + E)
    Space : O(V)

    Raises
    ------
    NotImplementedError
        Placeholder — to be implemented by the algorithm team.
    """
    raise NotImplementedError(
        "connected_components() has not been implemented yet."
    )
