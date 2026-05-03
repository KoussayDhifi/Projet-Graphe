# ============================================================
# algorithms/registry.py — Central algorithm registry
# ============================================================
#
# To register an algorithm:
#
#   from algorithms.registry import ALGORITHMS
#   from algorithms.shortest_path.dijkstra import dijkstra
#   ALGORITHMS["dijkstra"] = dijkstra
#
# Or use the ``register`` decorator:
#
#   @register("my_algorithm")
#   def my_algorithm(graph, source):
#       ...
#
# ============================================================

from __future__ import annotations
from typing import Callable, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph

# ---- Registry dictionary ----
# Key   : algorithm name (str)
# Value : callable(graph, source) -> List[Dict]
ALGORITHMS: Dict[str, Callable] = {}


def register(name: str) -> Callable:
    """
    Decorator that registers an algorithm function under the given name.

    Example
    -------
    >>> from algorithms.registry import register
    >>> @register("bfs")
    ... def bfs(graph, source):
    ...     ...
    """
    def decorator(fn: Callable) -> Callable:
        ALGORITHMS[name] = fn
        return fn
    return decorator


def run_algorithm(name: str, graph: "Graph", source: int = None, destination: int = None) -> List[Dict]:
    """
    Look up and execute a registered algorithm by name.

    Parameters
    ----------
    name        : str         – the registered algorithm name
    graph       : Graph       – the graph to run on
    source      : int | None  – source node (required by most algorithms)
    destination : int | None  – destination node (optional, for path-finding algorithms)

    Returns
    -------
    List[Dict]
        Animation steps returned by the algorithm.

    Raises
    ------
    ValueError
        If ``name`` is not found in the registry.
    NotImplementedError
        If the algorithm function raises it (placeholder not yet implemented).
    """
    if name not in ALGORITHMS:
        raise ValueError(
            f"Algorithm '{name}' is not registered. "
            f"Available: {sorted(ALGORITHMS.keys())}"
        )
    
    # Try to call with destination parameter (for traversal/path-finding algorithms)
    try:
        return ALGORITHMS[name](graph, source, destination)
    except TypeError:
        # Fall back to calling without destination (for other algorithms)
        return ALGORITHMS[name](graph, source)


def list_algorithms() -> List[str]:
    """Return sorted list of all registered algorithm names."""
    return sorted(ALGORITHMS.keys())


# ============================================================
# Auto-registration block
# — Import each algorithm module; the @register decorator (or
#   explicit ALGORITHMS[...] = ...) handles the rest.
# — Modules that raise ImportError (missing deps) are skipped
#   gracefully so the rest of the app still loads.
# ============================================================

def _auto_register() -> None:
    from algorithms.shortest_path.dijkstra    import dijkstra
    from algorithms.shortest_path.bellman_ford import bellman_ford
    from algorithms.shortest_path.bellman import bellman
    from algorithms.mst.kruskal               import kruskal
    from algorithms.mst.prim                  import prim
    from algorithms.traversal.bfs             import bfs
    from algorithms.traversal.dfs             import dfs
    from algorithms.components.connected      import connected_components
    from algorithms.components.scc            import strongly_connected_components
    from algorithms.coloring.welsh_powell     import welsh_powell
    from algorithms.eulerian.eulerian         import eulerian

    ALGORITHMS.update({
        "dijkstra":          dijkstra,
        "bellman_ford":      bellman_ford,
        "kruskal":           kruskal,
        "prim":              prim,
        "bellman":           bellman,
        "connected":         connected_components,
        "scc":               strongly_connected_components,
        "welsh_powell":      welsh_powell,
        "eulerian":          eulerian,
    })


_auto_register()
