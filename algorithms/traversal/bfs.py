# ============================================================
# algorithms/traversal/bfs.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    from core.graph import Graph


from animation.events import make_step, VISIT_NODE, PROCESS_NODE, TRAVERSE_EDGE, REJECT_EDGE
from collections import deque

def bfs(graph: "Graph", source: int) -> List[Dict]:
    """
    Breadth-First Search with animation steps.
    """

    steps: List[Dict] = []

    # Use adjacency list for efficiency
    adj = graph.to_adj_list()

    visited = set()
    queue = deque()

    # Initialize
    visited.add(source)
    queue.append(source)

    steps.append({"type": "visit_node", "node": source})

    while queue:
        current = queue.popleft()
        steps.append({"type": "process_node", "node": current})

        for neighbor, _ in adj[current]:
            steps.append({
                "type": "explore_edge",
                "src": current,
                "dest": neighbor
            })

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

                steps.append({
                    "type": "traverse_edge",
                    "src": current,
                    "dest": neighbor
                })

                steps.append({
                    "type": "visit_node",
                    "node": neighbor
                })
            else:
                steps.append({
                    "type": "reject_edge",
                    "src": current,
                    "dest": neighbor
                })

    return steps
