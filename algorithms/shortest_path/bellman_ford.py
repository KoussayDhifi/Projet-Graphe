# ============================================================
# algorithms/shortest_path/bellman_ford.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph

from animation.events import (
    make_step,
    VISIT_NODE, RELAX_EDGE, REJECT_EDGE, FINAL_PATH,
)


def bellman_ford(graph: "Graph", source: int) -> List[Dict]:
    """
    Compute single-source shortest paths using the Bellman-Ford algorithm.

    Unlike Dijkstra, Bellman-Ford handles graphs with negative edge weights
    and can detect negative-weight cycles.  It relaxes all edges V-1 times,
    then performs one additional pass to check for negative cycles.

    Parameters
    ----------
    graph  : Graph  – the input graph (directed or undirected)
    source : int    – the source node ID

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - VISIT_NODE   : when a node's distance is first reduced to a finite value
        - RELAX_EDGE   : each time an edge relaxation succeeds (distance improved)
        - REJECT_EDGE  : each time an edge relaxation fails (no improvement)
        - FINAL_PATH   : emitted once per reachable node with the shortest path
                         from source to that node

    Raises
    ------
    ValueError
        If a negative-weight cycle reachable from *source* is detected on the
        (V)-th relaxation pass.

    Complexity
    ----------
    Time  : O(V × E)
    Space : O(V)
    """
    steps: List[Dict] = []

    if source not in graph.nodes:
        raise KeyError(f"Source node {source} does not exist in the graph.")

    INF = float("inf")
    node_ids = list(graph.nodes.keys())
    V = len(node_ids)

    # For undirected graphs each edge must be relaxed in both directions
    # so we expand the edge list here rather than branching inside the loop.
    all_edges: List[tuple] = []
    for src, dest, weight in graph.edges:
        all_edges.append((src, dest, weight))
        if not graph.directed:
            all_edges.append((dest, src, weight))

    # dist[v]  : best known distance from source to v
    # prev[v]  : predecessor of v on the shortest path (for path reconstruction)
    dist: Dict[int, float] = {nid: INF for nid in node_ids}
    prev: Dict[int, int | None] = {nid: None for nid in node_ids}
    dist[source] = 0.0

    # Emit VISIT_NODE for the source immediately
    steps.append(make_step(VISIT_NODE, node=source))

    # ----------------------------------------------------------------
    # Main loop: relax all edges V-1 times
    # ----------------------------------------------------------------
    for iteration in range(V - 1):
        relaxed_any = False  # early-exit optimisation

        for src, dest, weight in all_edges:
            if dist[src] == INF:
                # Source not yet reachable — cannot improve dest through it
                steps.append(make_step(REJECT_EDGE, src=src, dest=dest))
                continue

            new_dist = dist[src] + weight

            if new_dist < dist[dest]:
                # Relaxation succeeded
                first_visit = dist[dest] == INF
                dist[dest] = new_dist
                prev[dest] = src
                relaxed_any = True

                steps.append(make_step(RELAX_EDGE, src=src, dest=dest, weight=weight))

                if first_visit:
                    # Node reached for the first time
                    steps.append(make_step(VISIT_NODE, node=dest))
            else:
                # Relaxation failed — no improvement
                steps.append(make_step(REJECT_EDGE, src=src, dest=dest))

        if not relaxed_any:
            # No edge was relaxed in this full pass → already optimal
            break

    # ----------------------------------------------------------------
    # Negative-cycle detection: one extra pass
    # ----------------------------------------------------------------
    for src, dest, weight in all_edges:
        if dist[src] != INF and dist[src] + weight < dist[dest]:
            raise ValueError(
                f"Negative-weight cycle detected reachable from source {source}."
            )

    # ----------------------------------------------------------------
    # Emit FINAL_PATH for every reachable node
    # ----------------------------------------------------------------
    for target in node_ids:
        if target == source:
            steps.append(make_step(FINAL_PATH, path=[source]))
            continue

        if dist[target] == INF:
            # Unreachable — no path event emitted
            continue

        # Reconstruct path by walking prev[] pointers
        path: List[int] = []
        current: int | None = target
        visited_check: set = set()  # guard against malformed prev chains

        while current is not None:
            if current in visited_check:
                break  # cycle guard (shouldn't happen without negative cycles)
            visited_check.add(current)
            path.append(current)
            current = prev[current]

        path.reverse()

        if path and path[0] == source:
            steps.append(make_step(FINAL_PATH, path=path))

    return steps