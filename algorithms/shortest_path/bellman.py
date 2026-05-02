from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph

from animation.events import (
    make_step,
    VISIT_NODE, RELAX_EDGE, REJECT_EDGE, FINAL_PATH,
)

def bellman(graph: "Graph", source: int) -> List[Dict]:
    """
    Compute single-source shortest paths using Bellman's original Dynamic Programming formulation.

    Unlike Bellman-Ford, which optimises space by updating a 1D array in-place,
    pure Bellman's algorithm explicitly computes paths based on hop-counts. It maintains
    a 2D table `dist[k][v]` representing the shortest path to node `v` using at most `k` edges.

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
        If a negative-weight cycle reachable from *source* is detected.

    Complexity
    ----------
    Time  : O(V × E)
    Space : O(V²) - specifically to maintain the explicit 2D Dynamic Programming table.
            (Can be optimized to O(V) by only keeping the k and k-1 arrays, but kept
            as O(V²) here to explicitly model the Bellman Equation state).
    """
    steps: List[Dict] = []

    if source not in graph.nodes:
        raise KeyError(f"Source node {source} does not exist in the graph.")

    INF = float("inf")
    node_ids = list(graph.nodes.keys())
    V = len(node_ids)

    all_edges: List[tuple] = []
    for src, dest, weight in graph.edges:
        all_edges.append((src, dest, weight))
        if not graph.directed:
            all_edges.append((dest, src, weight))

    # dist[k][v] : best distance from source to v using at most k edges
    dist: Dict[int, Dict[int, float]] = {k: {nid: INF for nid in node_ids} for k in range(V)}
    dist[0][source] = 0.0

    # prev[v] : overarching predecessor of v for path reconstruction
    prev: Dict[int, int | None] = {nid: None for nid in node_ids}

    # Emit VISIT_NODE for the source immediately
    steps.append(make_step(VISIT_NODE, node=source))

    # ----------------------------------------------------------------
    # Main DP loop: Compute paths using strictly 1 to V-1 hops
    # ----------------------------------------------------------------
    for k in range(1, V):
        relaxed_any = False

        # 1. Carry over the best distances from the previous hop count
        for nid in node_ids:
            dist[k][nid] = dist[k - 1][nid]

        # 2. Relax edges reading strictly from the (k-1) state
        for src, dest, weight in all_edges:
            if dist[k - 1][src] == INF:
                # Source unreachable in k-1 hops — cannot form a k-hop path through it
                steps.append(make_step(REJECT_EDGE, src=src, dest=dest))
                continue

            new_dist = dist[k - 1][src] + weight

            if new_dist < dist[k][dest]:
                # Relaxation succeeded using exactly k hops
                first_visit = dist[k - 1][dest] == INF and dist[k][dest] == INF
                
                dist[k][dest] = new_dist
                prev[dest] = src
                relaxed_any = True

                steps.append(make_step(RELAX_EDGE, src=src, dest=dest, weight=weight))

                if first_visit:
                    steps.append(make_step(VISIT_NODE, node=dest))
            else:
                # Relaxation failed — no improvement over the k-1 state or previous edge this pass
                steps.append(make_step(REJECT_EDGE, src=src, dest=dest))

        if not relaxed_any:
            # Early exit: If no shorter path exists using k edges, propagate current state to end
            for j in range(k + 1, V):
                for nid in node_ids:
                    dist[j][nid] = dist[k][nid]
            break

    # ----------------------------------------------------------------
    # Negative-cycle detection
    # ----------------------------------------------------------------
    # If a V-th edge relaxation improves the state of dist[V-1], a cycle exists.
    for src, dest, weight in all_edges:
        if dist[V - 1][src] != INF and dist[V - 1][src] + weight < dist[V - 1][dest]:
            raise ValueError(
                f"Negative-weight cycle detected reachable from source {source}."
            )

    # ----------------------------------------------------------------
    # Emit FINAL_PATH for every reachable node
    # ----------------------------------------------------------------
    final_dist = dist[V - 1]

    for target in node_ids:
        if target == source:
            steps.append(make_step(FINAL_PATH, path=[source]))
            continue

        if final_dist[target] == INF:
            continue

        # Reconstruct path by walking prev[] pointers
        path: List[int] = []
        current: int | None = target
        visited_check: set = set()

        while current is not None:
            if current in visited_check:
                break
            visited_check.add(current)
            path.append(current)
            current = prev[current]

        path.reverse()

        if path and path[0] == source:
            steps.append(make_step(FINAL_PATH, path=path))

    return steps