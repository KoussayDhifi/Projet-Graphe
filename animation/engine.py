# ============================================================
# animation/engine.py — Step-by-step animation playback engine
# ============================================================

from __future__ import annotations
from typing import List, Dict, Optional


class AnimationEngine:
    """
    Controls playback of a sequence of algorithm animation steps.

    The engine is intentionally algorithm-agnostic: it simply stores a
    list of step dicts and provides navigation primitives.  Visual
    rendering is delegated to ``animation/renderer.py``.

    Parameters
    ----------
    steps : List[Dict]
        The ordered list of animation steps returned by an algorithm.
    """

    def __init__(self, steps: List[Dict]) -> None:
        self.steps: List[Dict] = steps
        self.index: int = 0
        self._playing: bool = False
        self._speed: float = 0.5        # seconds between auto-advance steps
        self._elapsed: float = 0.0     # accumulated time since last step

    # ------------------------------------------------------------------
    # Core navigation
    # ------------------------------------------------------------------

    def next_step(self) -> Optional[Dict]:
        """
        Return the current step and advance the index.

        Returns
        -------
        dict | None
            The next step dict, or ``None`` when all steps are exhausted.
        """
        if self.index < len(self.steps):
            step = self.steps[self.index]
            self.index += 1
            return step
        return None

    def prev_step(self) -> Optional[Dict]:
        """
        Move one step backwards and return that step.

        Returns ``None`` if already at the beginning.
        """
        if self.index > 0:
            self.index -= 1
            if self.index > 0:
                return self.steps[self.index - 1]
        return None

    def peek(self) -> Optional[Dict]:
        """Return the next step without consuming it."""
        if self.index < len(self.steps):
            return self.steps[self.index]
        return None

    def reset(self) -> None:
        """Rewind to the beginning."""
        self.index = 0
        self._elapsed = 0.0
        self._playing = False

    def seek(self, index: int) -> None:
        """Jump to an absolute step index (clamped to valid range)."""
        self.index = max(0, min(index, len(self.steps)))

    # ------------------------------------------------------------------
    # Playback control
    # ------------------------------------------------------------------

    def play(self) -> None:
        """Begin or resume automatic playback."""
        self._playing = True
        self._elapsed = 0.0

    def pause(self) -> None:
        """Pause automatic playback."""
        self._playing = False

    def toggle_play(self) -> None:
        """Toggle between playing and paused."""
        if self._playing:
            self.pause()
        else:
            self.play()

    def set_speed(self, seconds_per_step: float) -> None:
        """
        Set how long (in seconds) the engine waits before auto-advancing.

        Parameters
        ----------
        seconds_per_step : float
            Must be > 0. Smaller = faster playback.
        """
        if seconds_per_step <= 0:
            raise ValueError("Speed must be positive.")
        self._speed = seconds_per_step

    # ------------------------------------------------------------------
    # Game-loop integration
    # ------------------------------------------------------------------

    def update(self, dt: float) -> Optional[Dict]:
        """
        Advance the engine by ``dt`` seconds.

        Call this once per frame from your game loop.  When in auto-play
        mode and the accumulated time exceeds ``_speed``, the engine
        consumes the next step and returns it.

        Parameters
        ----------
        dt : float
            Elapsed time since the last frame (seconds).

        Returns
        -------
        dict | None
            The step that was consumed this frame, or ``None``.
        """
        if not self._playing:
            return None
        self._elapsed += dt
        if self._elapsed >= self._speed:
            self._elapsed -= self._speed
            step = self.next_step()
            if step is None:
                self._playing = False
            return step
        return None

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    @property
    def is_playing(self) -> bool:
        return self._playing

    @property
    def is_finished(self) -> bool:
        return self.index >= len(self.steps)

    @property
    def progress(self) -> float:
        """Current progress as a fraction in [0, 1]."""
        if not self.steps:
            return 1.0
        return self.index / len(self.steps)

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    @property
    def current_index(self) -> int:
        return self.index

    def __repr__(self) -> str:
        return (
            f"AnimationEngine(index={self.index}/{self.total_steps}, "
            f"playing={self._playing}, speed={self._speed}s)"
        )
