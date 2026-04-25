# ============================================================
# algorithms/coloring/welsh_powell.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


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

    Raises
    ------
    NotImplementedError
        Placeholder — to be implemented by the algorithm team.
    """
    raise NotImplementedError("welsh_powell() has not been implemented yet.")
