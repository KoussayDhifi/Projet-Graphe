# ============================================================
# algorithms/components/connected.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph

from collections import deque
from animation.events import NEW_COMPONENT, ADD_TO_COMPONENT, VISIT_NODE, TRAVERSE_EDGE

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
    """
    steps = []
    matrix = graph.to_matrix()
    nodes = sorted(graph.nodes.keys())
    
    if not nodes:
        print("Composants connexes : []")
        return steps
        
    id_to_idx = {nid: i for i, nid in enumerate(nodes)}
    idx_to_id = {i: nid for i, nid in enumerate(nodes)}
    
    visited = set()
    components = []
    component_id = 0
    
    for node_id in nodes:
        if node_id not in visited:
            steps.append({"type": NEW_COMPONENT, "component_id": component_id})
            current_component = []
            
            queue = deque([node_id])
            visited.add(node_id)
            steps.append({"type": VISIT_NODE, "node": node_id})
            
            while queue:
                curr = queue.popleft()
                steps.append({"type": ADD_TO_COMPONENT, "node": curr, "component_id": component_id})
                current_component.append(curr)
                
                curr_idx = id_to_idx[curr]
                for nxt_idx, weight in enumerate(matrix[curr_idx]):
                    if weight != float('inf') and weight != 0.0:
                        nxt = idx_to_id[nxt_idx]
                        if nxt not in visited:
                            steps.append({"type": TRAVERSE_EDGE, "src": curr, "dest": nxt})
                            visited.add(nxt)
                            steps.append({"type": VISIT_NODE, "node": nxt})
                            queue.append(nxt)
            
            components.append(current_component)
            component_id += 1
            
    print("Composants connexes :")
    for i, comp in enumerate(components):
        print(f"Component {i}: {comp}")
        
    return steps, components
