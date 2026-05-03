# ============================================================
# algorithms/shortest_path/dijkstra.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


from animation.events import make_step, VISIT_NODE, RELAX_EDGE, EXPLORE_EDGE, REJECT_EDGE, FINAL_PATH
import heapq

def dijkstra(graph: "Graph", source: int) -> List[Dict]:
    steps: List[Dict] = []
    if source not in graph.nodes:
        return steps

    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    predecessors = {node: None for node in graph.nodes}
    pq = [(0, source)]
    
    visited_final = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited_final:
            continue
        visited_final.add(u)
        steps.append(make_step(VISIT_NODE, node=u))

        for v, weight in graph.neighbors(u):
            steps.append(make_step(EXPLORE_EDGE, src=u, dest=v))
            new_dist = d + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(pq, (new_dist, v))
                steps.append(make_step(RELAX_EDGE, src=u, dest=v, weight=weight))
            else:
                steps.append(make_step(REJECT_EDGE, src=u, dest=v))

    # Emit final paths
    for node in graph.nodes:
        if distances[node] != float('inf'):
            path = []
            curr = node
            while curr is not None:
                path.append(curr)
                curr = predecessors[curr]
            path.reverse()
            if path:
                steps.append(make_step(FINAL_PATH, path=path))

    return steps
