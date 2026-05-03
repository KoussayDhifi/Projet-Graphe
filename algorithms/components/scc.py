# ============================================================
# algorithms/components/scc.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph

from animation.events import NEW_COMPONENT, ADD_TO_COMPONENT, VISIT_NODE, PROCESS_NODE, TRAVERSE_EDGE

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
    """
    steps = []
    matrix = graph.to_matrix()
    nodes = sorted(graph.nodes.keys())
    
    if not nodes:
        print("Composants fortement connexes : []")
        return steps
        
    id_to_idx = {nid: i for i, nid in enumerate(nodes)}
    idx_to_id = {i: nid for i, nid in enumerate(nodes)}
    
    index = 0
    indices = {}
    lowlink = {}
    on_stack = set()
    stack = []
    components = []
    component_id = 0
    
    def strongconnect(v):
        nonlocal index, component_id
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        
        steps.append({"type": VISIT_NODE, "node": v})
        
        v_idx = id_to_idx[v]
        for w_idx, weight in enumerate(matrix[v_idx]):
            if weight != float('inf') and weight != 0.0:
                w = idx_to_id[w_idx]
                steps.append({"type": TRAVERSE_EDGE, "src": v, "dest": w})
                if w not in indices:
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif w in on_stack:
                    lowlink[v] = min(lowlink[v], indices[w])
                    
        steps.append({"type": PROCESS_NODE, "node": v})
        
        if lowlink[v] == indices[v]:
            steps.append({"type": NEW_COMPONENT, "component_id": component_id})
            current_component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                current_component.append(w)
                steps.append({"type": ADD_TO_COMPONENT, "node": w, "component_id": component_id})
                if w == v:
                    break
            components.append(current_component)
            component_id += 1

    for v in nodes:
        if v not in indices:
            strongconnect(v)
            
    print("Composants fortement connexes :")
    for i, comp in enumerate(components):
        print(f"Component {i}: {comp}")
        
    return steps, components
