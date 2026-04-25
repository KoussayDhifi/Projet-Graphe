# ============================================================
# controller/app_controller.py — Central application controller
# ============================================================
#
# The controller owns:
#   - The Graph instance
#   - The AnimationEngine instance
#   - The Renderer and VisualState
#
# It mediates between the UI layer and the algorithm / animation layers.
# ============================================================

from __future__ import annotations
from typing import Optional, Dict, List

from core.graph import Graph
from animation.engine import AnimationEngine
from animation.renderer import Renderer, VisualState
from algorithms.registry import run_algorithm
from utils.constants import ANIMATION_SPEED_DEFAULT


class AppController:
    """
    Mediator between UI, Graph, Algorithms and Animation subsystems.

    Responsibilities
    ----------------
    * Hold and mutate the shared Graph instance.
    * Run algorithms and populate the AnimationEngine.
    * Tick the engine each frame and apply visual state updates.
    * Expose a clean API to the UI layer (no PyGame imports here).
    """

    def __init__(self, directed: bool = False, weighted: bool = False) -> None:
        self.graph   = Graph(directed=directed, weighted=weighted)
        self.engine: Optional[AnimationEngine] = None
        self._renderer   = Renderer()
        self.visual_state = VisualState()

    # ------------------------------------------------------------------
    # Graph mutation API (called by UI)
    # ------------------------------------------------------------------

    def add_node(self, x: int, y: int) -> int:
        """Add a node and return its ID."""
        node_id = self.graph.add_node(x, y)
        self.visual_state.reset()
        return node_id

    def remove_node(self, node_id: int) -> None:
        """Remove a node and all its incident edges."""
        self.graph.remove_node(node_id)
        self.visual_state.reset()

    def add_edge(self, src: int, dest: int, weight: float = 1.0) -> None:
        """Add an edge (raises ValueError for invalid input)."""
        self.graph.add_edge(src, dest, weight)

    def remove_edge(self, src: int, dest: int) -> None:
        self.graph.remove_edge(src, dest)

    def clear_graph(self) -> None:
        """Reset the graph and animation state."""
        self.graph.clear()
        self.visual_state.reset()
        self.engine = None
        self._renderer.reset()

    # ------------------------------------------------------------------
    # Algorithm execution
    # ------------------------------------------------------------------

    def run_algorithm(self, name: str, source: Optional[int] = None) -> None:
        """
        Execute a registered algorithm and prepare the animation engine.

        Parameters
        ----------
        name   : str       – registered algorithm name
        source : int|None  – source node for the algorithm

        Raises
        ------
        NotImplementedError  – if the algorithm stub hasn't been implemented
        ValueError           – if the name is unknown
        """
        steps: List[Dict] = run_algorithm(name, self.graph, source)
        self.visual_state.reset()
        self._renderer.reset()
        self.engine = AnimationEngine(steps)

    # ------------------------------------------------------------------
    # Animation control API (called by UI)
    # ------------------------------------------------------------------

    def animation_play(self) -> None:
        if self.engine:
            self.engine.play()

    def animation_pause(self) -> None:
        if self.engine:
            self.engine.pause()

    def animation_step(self) -> Optional[Dict]:
        """Manually advance one step and apply its visual effect."""
        if self.engine:
            step = self.engine.next_step()
            if step:
                self._renderer.apply(step, self.visual_state)
            return step
        return None

    def animation_reset(self) -> None:
        """Rewind and clear visual state."""
        self.visual_state.reset()
        self._renderer.reset()
        if self.engine:
            self.engine.reset()

    def set_animation_speed(self, seconds_per_step: float) -> None:
        if self.engine:
            self.engine.set_speed(seconds_per_step)

    # ------------------------------------------------------------------
    # Game-loop tick (called every frame by main.py)
    # ------------------------------------------------------------------

    def animation_tick(self, dt: float) -> Optional[Dict]:
        """
        Advance the animation engine by `dt` seconds.

        If a step was consumed, apply it to the visual state and return it.
        """
        if self.engine:
            step = self.engine.update(dt)
            if step:
                self._renderer.apply(step, self.visual_state)
            return step
        return None
