# ============================================================
# ui/widgets.py — Reusable PyGame UI widget primitives
# ============================================================

from __future__ import annotations
import pygame
from utils.constants import (
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_ACCENT, COLOR_PANEL,
    COLOR_BORDER, COLOR_BG, COLOR_SUCCESS, COLOR_DANGER,
)


def _load_font(size: int, bold: bool = False) -> pygame.font.Font:
    try:
        return pygame.font.SysFont("dejavusans", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)


class Button:
    """A simple clickable button widget."""

    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        color=COLOR_ACCENT,
        text_color=COLOR_TEXT,
        font_size: int = 16,
        border_radius: int = 6,
    ) -> None:
        self.rect = rect
        self.label = label
        self.color = color
        self.text_color = text_color
        self.border_radius = border_radius
        self._font = _load_font(font_size, bold=True)
        self.hovered = False
        self.active = False    # toggled/selected state
        self.enabled = True

    def draw(self, surface: pygame.Surface) -> None:
        if not self.enabled:
            bg = tuple(max(0, c - 40) for c in self.color)
            alpha_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            pygame.draw.rect(alpha_surf, bg + (120,), alpha_surf.get_rect(),
                             border_radius=self.border_radius)
            surface.blit(alpha_surf, self.rect.topleft)
        else:
            bg = tuple(min(255, c + 30) for c in self.color) if self.hovered else self.color
            if self.active:
                bg = COLOR_SUCCESS
            pygame.draw.rect(surface, bg, self.rect, border_radius=self.border_radius)

        text_surf = self._font.render(self.label, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Return True if the button was clicked."""
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Toggle(Button):
    """A button that toggles between two states."""

    def __init__(self, rect, label_off: str, label_on: str, **kwargs) -> None:
        super().__init__(rect, label_off, **kwargs)
        self.label_off = label_off
        self.label_on = label_on
        self._state = False

    @property
    def state(self) -> bool:
        return self._state

    def handle_event(self, event: pygame.event.Event) -> bool:
        clicked = super().handle_event(event)
        if clicked:
            self._state = not self._state
            self.label = self.label_on if self._state else self.label_off
            self.active = self._state
        return clicked


class Label:
    """Non-interactive text label."""

    def __init__(
        self,
        pos: tuple,
        text: str,
        font_size: int = 16,
        color=COLOR_TEXT,
        bold: bool = False,
        anchor: str = "topleft",
    ) -> None:
        self.pos = pos
        self.text = text
        self.color = color
        self.anchor = anchor
        self._font = _load_font(font_size, bold=bold)

    def draw(self, surface: pygame.Surface) -> None:
        surf = self._font.render(self.text, True, self.color)
        rect = surf.get_rect(**{self.anchor: self.pos})
        surface.blit(surf, rect)


class Slider:
    """Horizontal slider widget for float values."""

    def __init__(
        self,
        rect: pygame.Rect,
        min_val: float,
        max_val: float,
        value: float,
    ) -> None:
        self.rect = rect
        self.min_val = min_val
        self.max_val = max_val
        self._value = value
        self._dragging = False
        self._font = _load_font(13)

    @property
    def value(self) -> float:
        return self._value

    def _frac(self) -> float:
        span = self.max_val - self.min_val
        return (self._value - self.min_val) / span if span else 0.0

    def draw(self, surface: pygame.Surface) -> None:
        # Track
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, border_radius=4)
        # Fill
        fill_w = int(self.rect.width * self._frac())
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.height)
        pygame.draw.rect(surface, COLOR_ACCENT, fill_rect, border_radius=4)
        # Thumb
        thumb_x = self.rect.x + fill_w
        thumb_rect = pygame.Rect(thumb_x - 6, self.rect.y - 4, 12, self.rect.height + 8)
        pygame.draw.rect(surface, COLOR_TEXT, thumb_rect, border_radius=3)
        # Value label
        lbl = self._font.render(f"{self._value:.2f}s", True, COLOR_TEXT_DIM)
        surface.blit(lbl, (self.rect.right + 8, self.rect.centery - lbl.get_height() // 2))

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            expand = pygame.Rect(
                self.rect.x, self.rect.y - 8,
                self.rect.width, self.rect.height + 16,
            )
            if expand.collidepoint(event.pos):
                self._dragging = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False
        if event.type == pygame.MOUSEMOTION and self._dragging:
            frac = (event.pos[0] - self.rect.x) / self.rect.width
            frac = max(0.0, min(1.0, frac))
            self._value = self.min_val + frac * (self.max_val - self.min_val)
            return True
        return False


class TextInput:
    """Single-line text input field."""

    def __init__(self, rect: pygame.Rect, placeholder: str = "", max_chars: int = 8) -> None:
        self.rect = rect
        self.placeholder = placeholder
        self.max_chars = max_chars
        self.text = ""
        self.active = False
        self._font = _load_font(16)
        self._cursor_visible = True
        self._cursor_timer = 0.0

    def draw(self, surface: pygame.Surface) -> None:
        border_col = COLOR_ACCENT if self.active else COLOR_BORDER
        pygame.draw.rect(surface, COLOR_PANEL, self.rect, border_radius=4)
        pygame.draw.rect(surface, border_col, self.rect, 2, border_radius=4)
        display = self.text
        if not display:
            surf = self._font.render(self.placeholder, True, COLOR_TEXT_DIM)
        else:
            cursor_str = display + ("|" if self.active and self._cursor_visible else "")
            surf = self._font.render(cursor_str, True, COLOR_TEXT)
        surface.blit(surf, (self.rect.x + 8, self.rect.centery - surf.get_height() // 2))

    def update(self, dt: float) -> None:
        self._cursor_timer += dt
        if self._cursor_timer >= 0.5:
            self._cursor_visible = not self._cursor_visible
            self._cursor_timer = 0.0

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return True
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.active = False
                return True
            if len(self.text) < self.max_chars and event.unicode.isprintable():
                self.text += event.unicode
                return True
        return False

    def get_float(self) -> float | None:
        try:
            return float(self.text)
        except ValueError:
            return None


# ============================================================
# Algorithm pseudocode registry
# Maps algorithm name (lowercase, as used in the registry) →
# list of pseudocode lines shown in the panel.
# ============================================================

ALGO_PSEUDOCODE: dict[str, list[str]] = {
    "bfs": [
        "BFS(G, source):",
        "  enqueue source",
        "  mark source as visited",
        "  while queue not empty:",
        "    u = dequeue()",
        "    for each neighbour v of u:",
        "      if v not visited:",
        "        mark v as visited",
        "        enqueue v",
    ],
    "dfs": [
        "DFS(G, source):",
        "  push source onto stack",
        "  while stack not empty:",
        "    u = pop()",
        "    if u not visited:",
        "      mark u as visited",
        "      for each neighbour v of u:",
        "        push v onto stack",
    ],
    "dijkstra": [
        "Dijkstra(G, source):",
        "  dist[source] = 0",
        "  for all other nodes: dist = ∞",
        "  add all nodes to priority queue",
        "  while queue not empty:",
        "    u = extract_min(queue)",
        "    for each neighbour v of u:",
        "      alt = dist[u] + weight(u, v)",
        "      if alt < dist[v]:",
        "        dist[v] = alt",
        "        prev[v] = u",
    ],
    "bellman_ford": [
        "BellmanFord(G, source):",
        "  dist[source] = 0",
        "  for all other nodes: dist = ∞",
        "  repeat |V| - 1 times:",
        "    for each edge (u, v, w):",
        "      if dist[u] + w < dist[v]:",
        "        dist[v] = dist[u] + w",
        "  for each edge (u, v, w):",
        "    if dist[u] + w < dist[v]:",
        "      report negative cycle",
    ],
    "kruskal": [
        "Kruskal(G):",
        "  A := empty set",
        "  for each vertex v of G:",
        "    creerEnsemble(v)",
        "  sort edges by weight ascending",
        "  for each edge (u, v) by weight:",
        "    if find(u) != find(v):",
        "      add edge (u, v) to A",
        "      union(u, v)",
    ],
    "prim": [
        "Prim(G, source):",
        "  key[source] = 0",
        "  for all other nodes: key = ∞",
        "  add all nodes to priority queue",
        "  while queue not empty:",
        "    u = extract_min(queue)",
        "    for each neighbour v of u:",
        "      if v in queue and w(u,v) < key[v]:",
        "        parent[v] = u",
        "        key[v] = w(u, v)",
    ],
    "connected": [
        "Connected(G):",
        "  component_id = 0",
        "  for each unvisited node u:",
        "    start BFS/DFS from u",
        "    label all reached nodes",
        "    with component_id",
        "    component_id += 1",
    ],
    "scc": [
        "SCC / Kosaraju(G):",
        "  run DFS on G, record finish order",
        "  build reversed graph G_r",
        "  run DFS on G_r in reverse",
        "    finish order",
        "  each DFS tree = one SCC",
    ],
    "welsh_powell": [
        "WelshPowell(G):",
        "  sort nodes by degree descending",
        "  color_map = {}",
        "  for each node u (sorted):",
        "    nbr_colors = colors of neighbours",
        "    color = smallest int not in",
        "      nbr_colors",
        "    color_map[u] = color",
    ],
    "eulerian": [
        "Eulerian(G, source):",
        "  check Euler conditions:",
        "    if all degrees even:",
        "      → Eulerian circuit",
        "    if exactly 2 odd degrees:",
        "      → Eulerian path",
        "    else: no Eulerian path",
        "  Hierholzer:",
        "  stack = [start_node]",
        "  path = []",
        "  while stack not empty:",
        "    u = peek(stack)",
        "    if u has unused edges:",
        "      v = next neighbour of u",
        "      remove edge (u, v)",
        "      push v onto stack",
        "    else:",
        "      path.prepend(pop(stack))",
        "  return path",
    ],
}

# Maps event types emitted by each algorithm to the pseudocode
# line index that should be highlighted when that event fires.
# Format:  algo_name -> { event_type -> line_index }
ALGO_EVENT_LINE: dict[str, dict[str, int]] = {
    "bfs": {
        "visit_node":    1,
        "traverse_edge": 6,
        "process_node":  4,
        "explore_edge":  5,
        "reject_edge":   5,
    },
    "dfs": {
        "visit_node":    5,
        "traverse_edge": 6,
        "process_node":  4,
        "explore_edge":  6,
        "reject_edge":   6,
    },
    "dijkstra": {
        "visit_node":   5,
        "explore_edge": 6,
        "relax_edge":   7,
        "reject_edge":  7,
        "final_path":   10,
    },
    "bellman_ford": {
        "visit_node":   3,
        "explore_edge": 4,
        "relax_edge":   5,
        "reject_edge":  5,
        "final_path":   9,
    },
    "kruskal": {
        "visit_node":    2,
        "explore_edge":  5,
        "select_edge":   7,
        "discard_edge":  5,
        "final_tree":    8,
    },
    "prim": {
        "visit_node":   4,
        "explore_edge": 6,
        "relax_edge":   7,
        "select_edge":  7,
        "reject_edge":  6,
        "final_tree":   8,
    },
    "connected": {
        "visit_node":        3,
        "new_component":     2,
        "add_to_component":  4,
        "explore_edge":      3,
    },
    "scc": {
        "visit_node":        1,
        "new_component":     5,
        "add_to_component":  5,
        "explore_edge":      1,
    },
    "welsh_powell": {
        "visit_node":  3,
        "color_node":  6,
    },
}


class AlgorithmCodePanel:
    """
    Displays a pseudocode panel for the currently selected algorithm,
    highlighting the line that corresponds to the most recently emitted
    animation event.

    Usage
    -----
    Create once and store on the sandbox / controller:

        self.code_panel = AlgorithmCodePanel(
            rect=pygame.Rect(x, y, width, height)
        )

    When the user selects an algorithm:

        self.code_panel.set_algorithm("kruskal")

    Each time the animation engine emits a step dict:

        self.code_panel.set_active_event(step["type"])

    Call in the draw loop:

        self.code_panel.draw(surface)
    """

    # Visual constants
    _PADDING       = 10          # inner padding (px)
    _LINE_HEIGHT   = 18          # px per pseudocode row
    _HEADER_H      = 24          # height of the "Algorithm code" header
    _BORDER_RADIUS = 8

    # Colours  (dark-theme, matching the app palette)
    _COL_BG        = (12,  18,  35)    # panel background
    _COL_BORDER    = (50,  90, 160)    # border — cyan-blue
    _COL_HEADER    = (180, 200, 230)   # header text
    _COL_LINE      = (160, 180, 210)   # normal line text
    _COL_HIGHLIGHT = (30,  60, 110)    # active-line background
    _COL_HL_TEXT   = (255, 255, 255)   # active-line text
    _COL_LINENO    = (70,  90, 130)    # line-number gutter

    def __init__(self, rect: pygame.Rect) -> None:
        self.rect          = rect
        self._algo_name    : str | None       = None
        self._lines        : list[str]        = []
        self._active_line  : int | None       = None
        self._event_map    : dict[str, int]   = {}

        # --- Dragging State ---
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        self._font_header = _load_font(13, bold=True)
        self._font_code   = _load_font(12)          # monospace fallback via dejavusans
        try:
            self._font_code = pygame.font.SysFont("dejavusansmono", 12)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Processes mouse events for dragging the panel.
        Call this in your main event loop: self.code_panel.handle_event(event)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    # Calculate where inside the panel we clicked
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y
                    
                    # Change cursor to 'hand' or 'move'
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                # Update position based on mouse + original offset
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

    def set_algorithm(self, name: str) -> None:
        """
        Load the pseudocode for *name* (case-insensitive, spaces/hyphens
        normalised to underscores).
        """
        key = name.lower().replace(" ", "_").replace("-", "_")
        self._algo_name   = key
        self._lines       = ALGO_PSEUDOCODE.get(key, [f"# {name}", "  (no pseudocode)"])
        self._event_map   = ALGO_EVENT_LINE.get(key, {})
        self._active_line = None

    def set_active_event(self, event_type: str) -> None:
        """Highlight the line associated with *event_type*."""
        if event_type in self._event_map:
            self._active_line = self._event_map[event_type]

    def clear_highlight(self) -> None:
        self._active_line = None

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        r = self.rect

        # --- Panel background + border ---
        panel_surf = pygame.Surface(r.size, pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, self._COL_BG + (230,),
                         panel_surf.get_rect(), border_radius=self._BORDER_RADIUS)
        surface.blit(panel_surf, r.topleft)
        pygame.draw.rect(surface, self._COL_BORDER, r, 2,
                         border_radius=self._BORDER_RADIUS)

        x0   = r.x + self._PADDING
        y0   = r.y + self._PADDING

        # --- Header ---
        algo_label = self._algo_name.replace("_", " ").title() if self._algo_name else "—"
        header_surf = self._font_header.render(
            f"Algorithm code  ·  {algo_label}", True, self._COL_HEADER
        )
        surface.blit(header_surf, (x0, y0))
        y0 += self._HEADER_H

        # Thin separator line
        pygame.draw.line(
            surface, self._COL_BORDER,
            (r.x + self._PADDING,       y0 - 4),
            (r.x + r.width - self._PADDING, y0 - 4), 1
        )

        # --- Pseudocode lines ---
        max_lines = (r.height - self._HEADER_H - self._PADDING * 2) // self._LINE_HEIGHT

        for i, line in enumerate(self._lines[:max_lines]):
            ly = y0 + i * self._LINE_HEIGHT

            if i == self._active_line:
                # Highlight background
                hl_rect = pygame.Rect(
                    r.x + 2, ly - 2,
                    r.width - 4, self._LINE_HEIGHT + 1
                )
                pygame.draw.rect(surface, self._COL_HIGHLIGHT, hl_rect)
                # Arrow indicator on the left
                arrow_surf = self._font_code.render("▶", True, COLOR_ACCENT)
                surface.blit(arrow_surf, (r.x + 3, ly))
                text_col = self._COL_HL_TEXT
            else:
                text_col = self._COL_LINE

            # Line number gutter
            lineno_surf = self._font_code.render(f"{i + 1:2d}", True, self._COL_LINENO)
            surface.blit(lineno_surf, (x0, ly))

            # Code text
            code_surf = self._font_code.render(line, True, text_col)
            surface.blit(code_surf, (x0 + 22, ly))
