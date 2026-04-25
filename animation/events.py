# ============================================================
# animation/events.py — Animation event type definitions
# ============================================================
#
# Every step emitted by an algorithm must be a dict with at least:
#
#   {
#       "type": <EVENT_TYPE>,   # one of the constants below
#       ... additional payload fields (see per-event docs)
#   }
#
# ============================================================

# -----------------------------------------------------------
# Node events
# -----------------------------------------------------------

VISIT_NODE = "visit_node"
"""
Emitted when a node is first reached / discovered.

Payload:
    node (int): the node ID that was just visited.
"""

PROCESS_NODE = "process_node"
"""
Emitted when a node is fully processed / popped from the queue.

Payload:
    node (int): the node ID that was processed.
"""

COLOR_NODE = "color_node"
"""
Assign a color index to a node (used by graph colouring algorithms).

Payload:
    node  (int): the node being coloured.
    color (int): zero-based colour index.
"""

# -----------------------------------------------------------
# Edge events
# -----------------------------------------------------------

EXPLORE_EDGE = "explore_edge"
"""
Emitted when an edge is first examined.

Payload:
    src  (int): source node.
    dest (int): destination node.
"""

RELAX_EDGE = "relax_edge"
"""
Emitted when an edge is relaxed (better path found).

Payload:
    src    (int)  : source node.
    dest   (int)  : destination node.
    weight (float): edge weight.
"""

REJECT_EDGE = "reject_edge"
"""
Emitted when an edge is examined but not useful.

Payload:
    src  (int): source node.
    dest (int): destination node.
"""

SELECT_EDGE = "select_edge"
"""
Emitted when an edge is selected for inclusion (e.g. MST).

Payload:
    src  (int): source node.
    dest (int): destination node.
"""

DISCARD_EDGE = "discard_edge"
"""
Emitted when an edge is explicitly discarded (e.g. would form a cycle).

Payload:
    src  (int): source node.
    dest (int): destination node.
"""

TRAVERSE_EDGE = "traverse_edge"
"""
Emitted during traversal algorithms when moving along an edge.

Payload:
    src  (int): source node.
    dest (int): destination node.
"""

# -----------------------------------------------------------
# Result events
# -----------------------------------------------------------

FINAL_PATH = "final_path"
"""
Marks the final shortest / optimal path.

Payload:
    path (List[int]): ordered list of node IDs forming the path.
"""

FINAL_TREE = "final_tree"
"""
Marks the final spanning tree edges.

Payload:
    edges (List[Tuple[int, int]]): list of (src, dest) pairs in the tree.
"""

# -----------------------------------------------------------
# Component events
# -----------------------------------------------------------

NEW_COMPONENT = "new_component"
"""
Signals the start of a new connected component.

Payload:
    component_id (int): zero-based component index.
"""

ADD_TO_COMPONENT = "add_to_component"
"""
Adds a node to the current component.

Payload:
    node         (int): the node being added.
    component_id (int): which component it belongs to.
"""

# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------

ALL_EVENTS = {
    VISIT_NODE, PROCESS_NODE, COLOR_NODE,
    EXPLORE_EDGE, RELAX_EDGE, REJECT_EDGE,
    SELECT_EDGE, DISCARD_EDGE, TRAVERSE_EDGE,
    FINAL_PATH, FINAL_TREE,
    NEW_COMPONENT, ADD_TO_COMPONENT,
}


def make_step(event_type: str, **kwargs) -> dict:
    """
    Convenience factory for building a well-formed animation step dict.

    Example
    -------
    >>> make_step(VISIT_NODE, node=3)
    {'type': 'visit_node', 'node': 3}
    """
    if event_type not in ALL_EVENTS:
        raise ValueError(f"Unknown event type: {event_type!r}")
    return {"type": event_type, **kwargs}
