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
        # Update hover state
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = self.rect.collidepoint(event.pos)
            
            # If mouse is over the button, update system cursor
            if self.hovered:
                if not self.enabled:
                    try:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
                    except AttributeError: pass # older pygame
                else:
                    try:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    except AttributeError: pass
            elif was_hovered:
                # Reset to default when leaving the button area
                try:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                except AttributeError: pass

        if not self.enabled:
            return False

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
        "  enfiler source",
        "  marquer source visité",
        "  tant que file non vide :",
        "    u = défiler(file)",
        "    pour chaque voisin v de u :",
        "      si v non visité :",
        "        marquer v visité",
        "        enfiler v",
    ],
    "dfs": [
        "DFS(G, source):",
        "  empiler source",
        "  tant que pile non vide :",
        "    u = dépiler(pile)",
        "    si u non visité :",
        "      marquer u visité",
        "      pour chaque voisin v de u :",
        "        si v non visité :",
        "          empiler v",
    ],
    "dijkstra": [
        "Dijkstra(G, source):",
        "  dist[source] = 0",
        "  tant que file non vide :",
        "    u = extraire_min(file)",
        "    pour chaque voisin v de u :",
        "      si dist[u] + w < dist[v] :",
        "        dist[v] = dist[u] + w",
        "        prec[v] = u",
    ],
    "bellman_ford": [
        "BellmanFord(G, source):",
        "  dist[source] = 0",
        "  répéter |V|-1 fois :",
        "    pour chaque arête (u, v, w) :",
        "      si dist[u] + w < dist[v] :",
        "        dist[v] = dist[u] + w",
        "  pour chaque arête (u, v, w) :",
        "    si dist[u] + w < dist[v] :",
        "      erreur 'Cycle négatif'",
    ],
    "kruskal": [
        "Kruskal(G):",
        "  trier arêtes par poids",
        "  pour chaque arête (u, v, w) :",
        "    si trouve(u) != trouve(v) :",
        "      ajouter (u, v) à MST",
        "      union(u, v)",
    ],
    "prim": [
        "Prim(G, source):",
        "  visiter source",
        "  ajouter arêtes de source au tas",
        "  tant que tas non vide :",
        "    (u, v) = extraire_min(tas)",
        "    si v non visité :",
        "      ajouter (u, v) à MST",
        "      visiter v",
        "      ajouter arêtes de v au tas",
    ],
    "connected": [
        "ComposantesConnexes(G):",
        "  pour chaque nœud u de G :",
        "    si u non visité :",
        "      nouvelle composante",
        "      BFS/DFS depuis u",
        "      marquer nœuds atteints",
    ],
    "scc": [
        "Tarjan(G):",
        "  strongconnect(u):",
        "    u.index = u.lowlink = i++",
        "    pour chaque voisin v de u :",
        "      si v non visité :",
        "        strongconnect(v)",
        "        u.lowlink = min(u.lowlink, v.lowlink)",
        "      sinon si v sur pile :",
        "        u.lowlink = min(u.lowlink, v.index)",
        "    si u.lowlink == u.index : nouvelle CFC",
    ],
    "welsh_powell": [
        "WelshPowell(G):",
        "  trier nœuds par degré décroissant",
        "  pour chaque nœud u trié :",
        "    c = plus petite couleur libre",
        "    colorier u avec c",
    ],
    "eulerian": [
        "Hierholzer(G):",
        "  vérifier degrés (Th. Euler)",
        "  choisir départ u",
        "  tant que pile non vide :",
        "    si u a des voisins :",
        "      empiler u, u = voisin",
        "      supprimer arête parcourue",
        "    sinon : ajouter u au circuit",
    ],
    "bellman": [
    "BellmanDP(G, source):",
    "  initialiser dist[0][v] = ∞",
    "  dist[0][source] = 0",
    "  pour k de 1 à |V| :",
    "    pour chaque sommet v :",
    "      dist[k][v] = dist[k-1][v]",
    "    pour chaque arête (u, v, w) :",
    "      si dist[k-1][u] + w < dist[k][v] :",
    "        dist[k][v] = dist[k-1][u] + w",
    "        prec[v] = u",
    "      sinon : ne rien faire",
    "  vérifier cycle négatif",
    "  reconstruire chemins",
],
}

# Maps event types emitted by each algorithm to the pseudocode
# line index that should be highlighted when that event fires.
# Format:  algo_name -> { event_type -> line_index }
ALGO_EVENT_LINE: dict[str, dict[str, int]] = {
    "bfs": {
        "visit_node":    2,
        "process_node":  4,
        "explore_edge":  5,
        "traverse_edge": 8,
        "reject_edge":   6,
    },
    "dfs": {
        "visit_node":    5,
        "process_node":  5,
        "explore_edge":  6,
        "traverse_edge": 8,
        "reject_edge":   7,
    },
    "dijkstra": {
        "visit_node":   3,
        "explore_edge": 4,
        "relax_edge":   6,
        "reject_edge":  5,
        "final_path":   7,
    },
    "bellman_ford": {
        "visit_node":   1,
        "explore_edge": 3,
        "relax_edge":   5,
        "reject_edge":  4,
    },
    "kruskal": {
        "code_sort":     1,
        "explore_edge":  2,
        "select_edge":   4,
        "discard_edge":  3,
        "final_tree":    5,
    },
    "prim": {
        "visit_node":    1,
        "explore_edge":  2,
        "select_edge":   6,
        "reject_edge":   5,
        "final_tree":    7,
    },
    "connected": {
        "new_component":     3,
        "visit_node":        4,
        "add_to_component":  5,
    },
    "scc": {
        "visit_node":        2,
        "traverse_edge":     4,
        "new_component":     9,
        "add_to_component":  9,
    },
    "welsh_powell": {
        "visit_node":  2,
        "color_node":  4,
    },
    "eulerian": {
        "visit_node":    5,
        "traverse_edge": 5,
        "final_path":    7,
    },
    "bellman": {
    "visit_node":   2,   # dist[source] = 0
    "explore_edge": 6,   # for each edge
    "relax_edge":   8,   # update dist
    "reject_edge":  10,  # ne rien faire
    "final_path":   12,  # reconstruction
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
    _PADDING       = 30          # inner padding (px)
    _LINE_HEIGHT   = 20          # px per pseudocode row
    _HEADER_H      = 24          # height of the "Algorithm code" header
    _BORDER_RADIUS = 8

    # Colours  (light-theme, matching the vibrant app palette)
    _COL_BG        = (255, 255, 255)   # Clean white panel background
    _COL_BORDER    = (190, 210, 235)   # Soft cyan-blue border (keeps the cool-toned framing)
    _COL_HEADER    = (40,  45,  55)    # Dark slate for sharp, readable headers
    _COL_LINE      = (80,  90,  105)   # Medium-dark text for standard lines to reduce eye strain
    _COL_HIGHLIGHT = (235, 195, 65)  # Pale, vibrant blue for the active line background
    _COL_HL_TEXT   = (220,   220, 220)   # Deep, punchy blue for active line text (high contrast)
    _COL_LINENO    = (170, 180, 195)   # Muted gray-blue for the gutter so it recedes visually

    def __init__(self, rect: pygame.Rect) -> None:
        self.rect          = rect
        self._algo_name    : str | None       = None
        self._lines        : list[str]        = []
        self._active_line  : int | None       = None
        self._event_map    : dict[str, int]   = {}
        self._scroll_y     = 0

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
        Handle mouse wheel for scrolling the pseudocode.
        """
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self._scroll_y -= event.y * self._LINE_HEIGHT
                self._clamp_scroll()

    def _clamp_scroll(self) -> None:
        max_h = len(self._lines) * self._LINE_HEIGHT
        view_h = self.rect.height - self._HEADER_H - self._PADDING * 2
        max_scroll = max(0, max_h - view_h)
        self._scroll_y = max(0, min(self._scroll_y, max_scroll))

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
        self._scroll_y    = 0

    def set_active_event(self, event_type: str) -> None:
        """Highlight the line associated with *event_type* and auto-scroll if needed."""
        if event_type in self._event_map:
            self._active_line = self._event_map[event_type]
            # Auto-scroll to show the active line
            if self._active_line is not None:
                line_y = self._active_line * self._LINE_HEIGHT
                view_h = self.rect.height - self._HEADER_H - self._PADDING * 2
                if line_y < self._scroll_y:
                    self._scroll_y = line_y
                elif line_y + self._LINE_HEIGHT > self._scroll_y + view_h:
                    self._scroll_y = line_y - view_h + self._LINE_HEIGHT
                self._clamp_scroll()

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

        # --- Pseudocode lines (with clipping) ---
        code_view_rect = pygame.Rect(
            r.x + 2, y0,
            r.width - 4, r.height - self._HEADER_H - self._PADDING * 2
        )
        
        # Create a sub-surface for the code to handle clipping/scrolling easily
        code_surf = pygame.Surface(code_view_rect.size, pygame.SRCALPHA)
        
        for i, line in enumerate(self._lines):
            ly = i * self._LINE_HEIGHT - self._scroll_y
            
            # Skip lines outside the view
            if ly + self._LINE_HEIGHT < 0 or ly > code_view_rect.height:
                continue

            if i == self._active_line:
                # Highlight background
                hl_rect = pygame.Rect(
                    0, ly - 2,
                    code_view_rect.width, self._LINE_HEIGHT + 1
                )
                pygame.draw.rect(code_surf, self._COL_HIGHLIGHT, hl_rect)
                # Arrow indicator on the left
                arrow_surf = self._font_code.render("▶", True, COLOR_ACCENT)
                code_surf.blit(arrow_surf, (1, ly))
                text_col = self._COL_HL_TEXT
            else:
                text_col = self._COL_LINE

            # Line number gutter
            lineno_surf = self._font_code.render(f"{i + 1:2d}", True, self._COL_LINENO)
            code_surf.blit(lineno_surf, (8, ly))

            # Code text
            code_txt_surf = self._font_code.render(line, True, text_col)
            code_surf.blit(code_txt_surf, (30, ly))

        surface.blit(code_surf, code_view_rect.topleft)


# ============================================================
# Graph example presets panel
# ============================================================

# Each preset: (display_label, internal_key, description)
GRAPH_PRESETS = [
    ("📍 Shortest Path",    "dijkstra_shortest_path",    "Weighted graph for Dijkstra shortest path"),
    ("🌳 MST (Prim)",       "prim_mst",                  "Weighted graph for Prim's minimum spanning tree"),
    ("🔍 BFS Traversal",    "bfs_traversal",             "Tree structure for breadth-first search"),
    ("🎨 Graph Coloring",   "coloring_welsh_powell",     "Complex graph for Welsh-Powell coloring"),
    ("🔄 Eulerian Circuit", "eulerian_circuit",          "Eulerian graph with all even-degree vertices"),
    ("🧩 Connected Comps.", "connected_components_graph", "Graph with multiple connected components"),
    ("🔗 SCC (Directed)",   "scc_directed_graph",        "Directed graph for strongly connected components"),
]


class GraphExamplePanel:
    """
    A floating panel drawn on the canvas with preset graph buttons.

    Clicking a button fires the callback ``on_select(key: str)`` where
    *key* is one of the internal keys from ``GRAPH_PRESETS``.

    Parameters
    ----------
    x, y      : top-left position on screen
    on_select : callable(key) invoked when the user picks a preset
    """

    _BG         = (255, 255, 255, 230)  # Frosted white, semi-transparent
    _BORDER     = (190, 210, 235)       # Soft cyan-blue to match your other panels
    _TITLE_COL  = (40,  45,  55)        # Dark slate for sharp, readable titles
    _DESC_COL   = (110, 120, 135)       # Muted gray-blue for descriptions

    _BTN_W  = 150
    _BTN_H  = 28
    _PAD    = 10
    _GAP    = 6
    _TITLE_H = 26

    def __init__(self, x: int, y: int, on_select) -> None:
        self._on_select = on_select
        self._buttons: list[tuple[Button, str, str]] = []  # (btn, key, desc)
        self._font_title = _load_font(13, bold=True)
        self._font_desc  = _load_font(11)
        self._hovered_desc = ""

        total_h = (
            self._TITLE_H
            + self._PAD
            + len(GRAPH_PRESETS) * (self._BTN_H + self._GAP)
            + self._PAD
            + 20   # desc line
            + self._PAD
        )
        self.rect = pygame.Rect(x, y, self._BTN_W + self._PAD * 2, total_h)

        btn_x = x + self._PAD
        btn_y = y + self._TITLE_H + self._PAD
        for label, key, desc in GRAPH_PRESETS:
            btn = Button(
                rect=pygame.Rect(btn_x, btn_y, self._BTN_W, self._BTN_H),
                label=label,
                font_size=12,
                color=(30, 50, 100),
                text_color=(210, 225, 255),
                border_radius=5,
            )
            self._buttons.append((btn, key, desc))
            btn_y += self._BTN_H + self._GAP

        self._desc_y = btn_y + self._PAD

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Return the preset key that was clicked, or None."""
        self._hovered_desc = ""
        for btn, key, desc in self._buttons:
            if event.type == pygame.MOUSEMOTION and btn.rect.collidepoint(event.pos):
                self._hovered_desc = desc
            if btn.handle_event(event):
                return key
        return None

    def draw(self, surface: pygame.Surface) -> None:
        r = self.rect

        # Semi-transparent background
        bg_surf = pygame.Surface(r.size, pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, self._BG,
                         bg_surf.get_rect(), border_radius=10)
        surface.blit(bg_surf, r.topleft)
        pygame.draw.rect(surface, self._BORDER, r, 2, border_radius=10)

        # Title
        title = self._font_title.render("Example Graphs", True, self._TITLE_COL)
        surface.blit(title, (r.x + self._PAD, r.y + 6))

        # Thin separator
        pygame.draw.line(
            surface, self._BORDER,
            (r.x + self._PAD,           r.y + self._TITLE_H - 2),
            (r.x + r.width - self._PAD, r.y + self._TITLE_H - 2), 1,
        )

        # Buttons
        for btn, key, desc in self._buttons:
            btn.draw(surface)

        # Hovered description
        if self._hovered_desc:
            desc_surf = self._font_desc.render(
                self._hovered_desc, True, self._DESC_COL
            )
            surface.blit(desc_surf, (r.x + self._PAD, self._desc_y))
