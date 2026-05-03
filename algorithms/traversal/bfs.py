# ============================================================
# algorithms/traversal/bfs.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


from animation.events import make_step, VISIT_NODE, PROCESS_NODE, TRAVERSE_EDGE, REJECT_EDGE
from collections import deque

def bfs(graph: "Graph", source: int) -> List[Dict]:
    steps: List[Dict] = []
    if source not in graph.nodes:
        return steps

    visited = {source}
    queue = deque([source])
    
    steps.append(make_step(VISIT_NODE, node=source))

    while queue:
        u = queue.popleft()
        steps.append(make_step(PROCESS_NODE, node=u))

        for v, weight in graph.neighbors(u):
            steps.append(make_step(EXPLORE_EDGE, src=u, dest=v))
            if v not in visited:
                visited.add(v)
                steps.append(make_step(TRAVERSE_EDGE, src=u, dest=v))
                steps.append(make_step(VISIT_NODE, node=v))
                queue.append(v)
            else:
                steps.append(make_step(REJECT_EDGE, src=u, dest=v))

    return steps
