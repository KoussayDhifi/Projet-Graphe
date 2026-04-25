# ============================================================
# core/exporters.py — Serialise / deserialise Graph objects
# ============================================================

from __future__ import annotations
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def graph_to_dict(graph: "Graph") -> dict:
    """
    Convert a Graph to a plain Python dict suitable for JSON serialisation.

    Schema
    ------
    {
        "directed": bool,
        "weighted": bool,
        "nodes": [[id, x, y], ...],
        "edges": [[src, dest, weight], ...]
    }
    """
    return {
        "directed": graph.directed,
        "weighted": graph.weighted,
        "nodes": [[nid, x, y] for nid, (x, y) in graph.nodes.items()],
        "edges": [[s, d, w] for s, d, w in graph.edges],
    }


def graph_from_dict(data: dict) -> "Graph":
    """
    Reconstruct a Graph from the dict produced by ``graph_to_dict``.
    """
    from core.graph import Graph
    g = Graph(directed=data["directed"], weighted=data["weighted"])
    for nid, x, y in data["nodes"]:
        g.nodes[nid] = (int(x), int(y))
        if nid >= g._next_id:
            g._next_id = nid + 1
    for s, d, w in data["edges"]:
        g.edges.append((int(s), int(d), float(w)))
    return g


def export_json(graph: "Graph", path: str) -> None:
    """Write graph to a JSON file."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(graph_to_dict(graph), fh, indent=2)


def import_json(path: str) -> "Graph":
    """Read a graph from a JSON file produced by ``export_json``."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return graph_from_dict(data)


def export_edge_list(graph: "Graph", path: str) -> None:
    """
    Export graph as a simple edge list text file.

    Format per line: ``src dest weight``
    First line: ``# nodes=N directed=True/False weighted=True/False``
    """
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"# nodes={graph.node_count()} "
                 f"directed={graph.directed} weighted={graph.weighted}\n")
        for src, dest, weight in graph.edges:
            fh.write(f"{src} {dest} {weight}\n")
