# ============================================================
# algorithms/traversal/dfs.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


from animation.events import make_step, VISIT_NODE, PROCESS_NODE, TRAVERSE_EDGE, REJECT_EDGE

def dfs(graph: "Graph", source: int) -> List[Dict]:
    steps: List[Dict] = []
    if source not in graph.nodes:
        return steps

    visited = set()
    stack = [source]

    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            steps.append(make_step(VISIT_NODE, node=u))
            steps.append(make_step(PROCESS_NODE, node=u))

            # Reverse neighbors to maintain order typical for DFS stack
            neighbors = list(graph.neighbors(u))
            neighbors.reverse()
            for v, weight in neighbors:
                steps.append(make_step(EXPLORE_EDGE, src=u, dest=v))
                if v not in visited:
                    steps.append(make_step(TRAVERSE_EDGE, src=u, dest=v))
                    stack.append(v)
                else:
                    steps.append(make_step(REJECT_EDGE, src=u, dest=v))

    return steps
