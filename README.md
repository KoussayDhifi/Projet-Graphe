# Graph Algorithms Visualization Platform

A modular PyGame application for constructing graphs and visualizing classic graph algorithms step by step.

## Team

| Name | Role |
|------|------|
| AmenAllah KALAII | Algorithm Team |
| Youssef FNED | Algorithm Team |
| Mohammed Adem SELMI | Algorithm Team |
| Jalel Eddine BEN ROMDHANE | Algorithm Team |
| Koussay DHIFI | Algorithm Team |

---

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Project Structure

```
graph_app/
├── main.py                         # Entry point
├── core/
│   ├── graph.py                    # Graph data structure
│   └── exporters.py                # JSON / edge-list I/O
├── algorithms/
│   ├── registry.py                 # Algorithm registry + dispatcher
│   ├── shortest_path/
│   │   ├── dijkstra.py             # ← TO IMPLEMENT
│   │   └── bellman_ford.py         # ← TO IMPLEMENT
│   ├── mst/
│   │   ├── kruskal.py              # ← TO IMPLEMENT
│   │   └── prim.py                 # ← TO IMPLEMENT
│   ├── traversal/
│   │   ├── bfs.py                  # ← TO IMPLEMENT
│   │   └── dfs.py                  # ← TO IMPLEMENT
│   ├── components/
│   │   ├── connected.py            # ← TO IMPLEMENT
│   │   └── scc.py                  # ← TO IMPLEMENT
│   └── coloring/
│       └── welsh_powell.py         # ← TO IMPLEMENT
├── animation/
│   ├── events.py                   # Event type constants + make_step()
│   ├── engine.py                   # Playback engine (step/play/pause)
│   └── renderer.py                 # Maps events → visual state
├── ui/
│   ├── menu.py                     # Configuration / start screen
│   ├── sandbox.py                  # Interactive graph editor
│   ├── draw.py                     # Low-level drawing routines
│   └── widgets.py                  # Button, Toggle, Slider, TextInput
├── controller/
│   └── app_controller.py           # Mediator (graph + engine + renderer)
├── tests/
│   └── test_graphs.py              # Unit tests + sample graph fixtures
└── utils/
    └── constants.py                # Colors, sizes, speed defaults
```

---

## Implementing an Algorithm

Each algorithm file (e.g. `algorithms/shortest_path/dijkstra.py`) contains a stub function.  
Replace the `raise NotImplementedError(...)` with your implementation.

Your function **must** return `List[Dict]` — a list of animation step dicts.  
Use the helpers from `animation/events.py`:

```python
from animation.events import make_step, VISIT_NODE, RELAX_EDGE, FINAL_PATH

def dijkstra(graph, source):
    steps = []
    # ... your algorithm ...
    steps.append(make_step(VISIT_NODE, node=current))
    steps.append(make_step(RELAX_EDGE, src=u, dest=v, weight=w))
    steps.append(make_step(FINAL_PATH, path=[0, 2, 4]))
    return steps
```

**Rules:**
- Algorithm files must **not** import `pygame`
- Return `List[Dict]` — never modify the graph or visual state directly
- Use only event types defined in `animation/events.py`

---

## Event Protocol Reference

| Event | Required Payload | Used by |
|-------|-----------------|---------|
| `visit_node` | `node` | BFS, DFS, Dijkstra, Prim |
| `process_node` | `node` | BFS, DFS |
| `explore_edge` | `src`, `dest` | All traversal / path algorithms |
| `relax_edge` | `src`, `dest`, `weight` | Dijkstra, Bellman-Ford |
| `reject_edge` | `src`, `dest` | All algorithms |
| `select_edge` | `src`, `dest` | Kruskal, Prim |
| `discard_edge` | `src`, `dest` | Kruskal |
| `traverse_edge` | `src`, `dest` | BFS, DFS |
| `final_path` | `path` (List[int]) | Dijkstra, Bellman-Ford |
| `final_tree` | `edges` (List[Tuple]) | Kruskal, Prim |
| `new_component` | `component_id` | Connected, SCC |
| `add_to_component` | `node`, `component_id` | Connected, SCC |
| `color_node` | `node`, `color` (int) | Welsh-Powell |

---

## Running Tests

```bash
cd graph_app
pytest tests/ -v
```

Tests verify the `Graph` core API and that each algorithm stub correctly raises `NotImplementedError`.
