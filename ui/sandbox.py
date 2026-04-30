# ============================================================
# ui/sandbox.py — Interactive graph construction sandbox
# ============================================================

from __future__ import annotations
import pygame
from typing import Optional, Tuple, TYPE_CHECKING

from utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, SIDEBAR_WIDTH, TOPBAR_HEIGHT,
    NODE_RADIUS, COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_ACCENT,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_DANGER, COLOR_WARNING,
    ANIMATION_SPEED_DEFAULT, ANIMATION_SPEED_MIN, ANIMATION_SPEED_MAX,
)
from ui.draw import draw_graph, draw_status_bar, draw_tooltip
from ui.widgets import Button, Slider, TextInput, Label,AlgorithmCodePanel

if TYPE_CHECKING:
    from controller.app_controller import AppController


class SandboxScreen:
    """
    The main graph-editing and algorithm-visualization screen.

    Interactions
    ------------
    * Left-click on empty canvas  → create a new node
    * Left-click on a node        → select / deselect node
    * Left-click on a second node → create an edge between the two
    * Right-click on a node       → delete the node
    * Right-click on canvas       → deselect
    * Mouse drag (empty canvas)   → pan the view
    """

    def __init__(self, surface: pygame.Surface, controller: "AppController") -> None:
        self.surface  = surface
        self.ctrl     = controller

        # Selection state
        self._selected: Optional[int] = None   # first selected node for edge creation
        self._hover_node: Optional[int] = None

        # Pan offset
        self._offset: Tuple[int, int] = (0, 0)
        self._panning = False
        self._pan_start: Tuple[int, int] = (0, 0)
        self._pan_offset_start: Tuple[int, int] = (0, 0)

        # Weight input popup
        self._awaiting_weight = False
        self._edge_pending: Optional[Tuple[int, int]] = None

        # Status / hints
        self._status = "Left-click to add nodes | Select two nodes to add an edge"
        self._error_msg = ""
        self._error_timer = 0.0

        self._setup_fonts()
        self._setup_ui()

    # ------------------------------------------------------------------
    # Fonts
    # ------------------------------------------------------------------

    def _setup_fonts(self) -> None:
        try:
            self._font_ui    = pygame.font.SysFont("dejavusans", 14)
            self._font_small = pygame.font.SysFont("dejavusans", 12)
            self._font_bold  = pygame.font.SysFont("dejavusans", 15, bold=True)
        except Exception:
            self._font_ui    = pygame.font.Font(None, 16)
            self._font_small = pygame.font.Font(None, 14)
            self._font_bold  = pygame.font.Font(None, 16)

    # ------------------------------------------------------------------
    # UI panel construction
    # ------------------------------------------------------------------

    def _setup_ui(self) -> None:
        from algorithms.registry import list_algorithms
        W, H = WINDOW_WIDTH, WINDOW_HEIGHT
        sx = W - SIDEBAR_WIDTH + 10
        bw = SIDEBAR_WIDTH - 20

        # Graph info labels (updated each frame)
        self._lbl_nodes = Label((sx, 80), "Nodes: 0", 14, COLOR_TEXT_DIM)
        self._lbl_edges = Label((sx, 100), "Edges: 0", 14, COLOR_TEXT_DIM)
        self._lbl_type  = Label(
            (sx, 120),
            f"{'Directed' if self.ctrl.graph.directed else 'Undirected'} | "
            f"{'Weighted' if self.ctrl.graph.weighted else 'Unweighted'}",
            12, COLOR_TEXT_DIM,
        )

        # Algorithm buttons (one per registered algorithm)
        self._algo_buttons: list[Button] = []
        algo_names = list_algorithms()
        for i, name in enumerate(algo_names):
            btn = Button(
                rect=pygame.Rect(sx, 160 + i * 36, bw, 30),
                label=name.replace("_", " ").title(),
                font_size=13,
            )
            btn._algo_name = name          # tag for lookup on click
            self._algo_buttons.append(btn)

        ctrl_y = H - 160

        self._code_panel = AlgorithmCodePanel(
            rect=pygame.Rect(sx, 355, 240, 260) # (990, 355, 240, 260) 
        )
        
        # Animation controls
        self._btn_play  = Button(pygame.Rect(sx, ctrl_y,      bw // 2 - 4, 30), "▶ Playyy")
        self._btn_pause = Button(pygame.Rect(sx + bw // 2 + 4, ctrl_y, bw // 2 - 4, 30), "⏸ Pause")
        self._btn_step  = Button(pygame.Rect(sx, ctrl_y + 36, bw // 2 - 4, 30), "⏭ Step")
        self._btn_reset = Button(pygame.Rect(sx + bw // 2 + 4, ctrl_y + 36, bw // 2 - 4, 30), "↺ Reset")

        # Speed slider
        self._slider_speed = Slider(
            pygame.Rect(sx, ctrl_y + 82, bw - 50, 8),
            ANIMATION_SPEED_MIN, ANIMATION_SPEED_MAX, ANIMATION_SPEED_DEFAULT,
        )

        # Weight input (shown only when creating an edge on a weighted graph)
        self._weight_input = TextInput(
            pygame.Rect(W // 2 - 80, H // 2 - 20, 160, 40),
            placeholder="Weight (e.g. 3.5)",
            max_chars=8,
        )
        self._btn_confirm_weight = Button(
            pygame.Rect(W // 2 - 40, H // 2 + 30, 80, 32),
            label="Add Edge",
            font_size=13,
        )

        # Clear / export buttons
        self._btn_clear = Button(
            pygame.Rect(sx, H - 55, bw, 28),
            "Clear Graph",
            color=COLOR_DANGER,
            font_size=13,
        )

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        # Weight input popup takes priority
        if self._awaiting_weight:
            self._weight_input.handle_event(event)
            if self._btn_confirm_weight.handle_event(event):
                self._confirm_edge_with_weight()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._awaiting_weight = False
                self._edge_pending = None
                self._selected = None
            return

        # Sidebar widgets
        for btn in self._algo_buttons:
            if btn.handle_event(event):
                self._run_algorithm(btn._algo_name)

        if self._btn_play.handle_event(event):
            self.ctrl.animation_play()
        if self._btn_pause.handle_event(event):
            self.ctrl.animation_pause()
        if self._btn_step.handle_event(event):
            step = self.ctrl.animation_step()
            if step:
                self._status = f"Step: {step.get('type', '?')}"
                self._code_panel.set_active_event(step["type"])
        if self._btn_reset.handle_event(event):
            self.ctrl.animation_reset()
            self._code_panel.clear_highlight()
        if self._btn_clear.handle_event(event):
            self.ctrl.clear_graph()
            self._selected = None

        self._slider_speed.handle_event(event)
        self.ctrl.set_animation_speed(self._slider_speed.value)

        # Canvas mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._on_mouse_down(event)
        if event.type == pygame.MOUSEBUTTONUP:
            self._on_mouse_up(event)
        if event.type == pygame.MOUSEMOTION:
            self._on_mouse_move(event)

    def _on_mouse_down(self, event: pygame.event.Event) -> None:
        if not self._is_canvas_pos(event.pos):
            return
        canvas_pos = self._to_graph_coords(event.pos)

        if event.button == 1:
            hit = self._node_at(canvas_pos)
            if hit is None:
                # Create node
                node_id = self.ctrl.add_node(*canvas_pos)
                self._status = f"Added node {node_id}"
                self._selected = None
            else:
                if self._selected is None:
                    self._selected = hit
                    self._status = f"Node {hit} selected — click another node to add edge"
                elif self._selected == hit:
                    self._selected = None
                    self._status = "Deselected"
                else:
                    # Create edge
                    self._try_create_edge(self._selected, hit)

        elif event.button == 3:
            hit = self._node_at(canvas_pos)
            if hit is not None:
                self.ctrl.remove_node(hit)
                if self._selected == hit:
                    self._selected = None
                self._status = f"Removed node {hit}"
            else:
                self._selected = None

        elif event.button == 2:
            self._panning = True
            self._pan_start = event.pos
            self._pan_offset_start = self._offset

    def _on_mouse_up(self, event: pygame.event.Event) -> None:
        if event.button == 2:
            self._panning = False

    def _on_mouse_move(self, event: pygame.event.Event) -> None:
        if self._panning:
            dx = event.pos[0] - self._pan_start[0]
            dy = event.pos[1] - self._pan_start[1]
            self._offset = (
                self._pan_offset_start[0] + dx,
                self._pan_offset_start[1] + dy,
            )
        canvas_pos = self._to_graph_coords(event.pos)
        self._hover_node = self._node_at(canvas_pos)

    # ------------------------------------------------------------------
    # Edge creation helpers
    # ------------------------------------------------------------------

    def _try_create_edge(self, src: int, dest: int) -> None:
        if self.ctrl.graph.weighted:
            self._edge_pending = (src, dest)
            self._awaiting_weight = True
            self._weight_input.text = ""
            self._status = "Enter edge weight and click 'Add Edge'"
        else:
            try:
                self.ctrl.add_edge(src, dest, 1.0)
                self._status = f"Edge {src} → {dest} added"
            except ValueError as e:
                self._set_error(str(e))
            self._selected = None

    def _confirm_edge_with_weight(self) -> None:
        w = self._weight_input.get_float()
        if w is None:
            self._set_error("Invalid weight — enter a number.")
            return
        src, dest = self._edge_pending
        try:
            self.ctrl.add_edge(src, dest, w)
            self._status = f"Edge {src} → {dest} (w={w}) added"
        except ValueError as e:
            self._set_error(str(e))
        self._awaiting_weight = False
        self._edge_pending = None
        self._selected = None

    # ------------------------------------------------------------------
    # Algorithm runner
    # ------------------------------------------------------------------

    def _run_algorithm(self, name: str) -> None:
        source = self._selected
        if source is None and self.ctrl.graph.node_count() > 0:
            # Default to first node
            source = next(iter(self.ctrl.graph.nodes))
        try:
            self.ctrl.run_algorithm(name, source)
            self._status = f"Running {name} from node {source}"
            # Load pseudocode for the selected algorithm and reset highlight
            self._code_panel.set_algorithm(name)
            self._code_panel.clear_highlight()
        except NotImplementedError:
            self._set_error(f"{name} is not implemented yet.")
        except Exception as e:
            self._set_error(str(e))

    # ------------------------------------------------------------------
    # Update / Draw
    # ------------------------------------------------------------------

    def update(self, dt: float) -> None:
        self._weight_input.update(dt)
        if self._error_timer > 0:
            self._error_timer -= dt
        step = self.ctrl.animation_tick(dt)
        if step:
            self._status = f"Animating: {step.get('type', '?')}"
            self._code_panel.set_active_event(step["type"])

    def draw(self) -> None:
        self.surface.fill(COLOR_BG)
        self._draw_canvas_bg()
        self._draw_graph()
        self._draw_sidebar()
        self._draw_topbar()
        self._draw_status()
        if self._awaiting_weight:
            self._draw_weight_popup()

    def _draw_canvas_bg(self) -> None:
        """Dot-grid canvas background."""
        spacing = 32
        color = (22, 26, 42)
        W, H = WINDOW_WIDTH, WINDOW_HEIGHT
        ox, oy = self._offset
        for x in range(0, W - SIDEBAR_WIDTH, spacing):
            for y in range(TOPBAR_HEIGHT, H, spacing):
                gx = (x + ox % spacing)
                gy = (y + oy % spacing)
                pygame.draw.circle(self.surface, color, (gx, gy), 1)

    def _draw_graph(self) -> None:
        clip_rect = pygame.Rect(
            0, TOPBAR_HEIGHT,
            WINDOW_WIDTH - SIDEBAR_WIDTH,
            WINDOW_HEIGHT - TOPBAR_HEIGHT - 24,
        )
        self.surface.set_clip(clip_rect)
        draw_graph(
            self.surface,
            self.ctrl.graph,
            self.ctrl.visual_state,
            [self._selected] if self._selected is not None else [],
            offset=self._offset,
        )
        self.surface.set_clip(None)

    def _draw_sidebar(self) -> None:
        W, H = WINDOW_WIDTH, WINDOW_HEIGHT
        sb_rect = pygame.Rect(W - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, H)
        pygame.draw.rect(self.surface, COLOR_PANEL, sb_rect)
        pygame.draw.line(self.surface, COLOR_BORDER, sb_rect.topleft, sb_rect.bottomleft, 1)

        # Title
        title = self._font_bold.render("Algorithms", True, COLOR_TEXT)
        self.surface.blit(title, (sb_rect.x + 10, 14))

        # Live graph info
        self._lbl_nodes.text = f"Nodes: {self.ctrl.graph.node_count()}"
        self._lbl_edges.text = f"Edges: {self.ctrl.graph.edge_count()}"
        self._lbl_nodes.draw(self.surface)
        self._lbl_edges.draw(self.surface)
        self._lbl_type.draw(self.surface)

        # Algorithm buttons
        for btn in self._algo_buttons:
            btn.draw(self.surface)

        # Animation controls
        self._btn_play.draw(self.surface)
        self._btn_pause.draw(self.surface)
        self._btn_step.draw(self.surface)
        self._btn_reset.draw(self.surface)
        self._code_panel.draw(surface=self.surface)

        # Speed slider label
        spd_lbl = self._font_small.render("Step speed:", True, COLOR_TEXT_DIM)
        self.surface.blit(spd_lbl, (sb_rect.x + 10, WINDOW_HEIGHT - 85))
        self._slider_speed.draw(self.surface)

        self._btn_clear.draw(self.surface)

        # Progress bar
        if self.ctrl.engine:
            prog = self.ctrl.engine.progress
            bar_rect = pygame.Rect(sb_rect.x + 10, WINDOW_HEIGHT - 100, SIDEBAR_WIDTH - 20, 6)
            pygame.draw.rect(self.surface, COLOR_BORDER, bar_rect, border_radius=3)
            fill_w = int(bar_rect.width * prog)
            if fill_w > 0:
                pygame.draw.rect(
                    self.surface, COLOR_ACCENT,
                    pygame.Rect(bar_rect.x, bar_rect.y, fill_w, bar_rect.height),
                    border_radius=3,
                )
            step_lbl = self._font_small.render(
                f"{self.ctrl.engine.current_index}/{self.ctrl.engine.total_steps}",
                True, COLOR_TEXT_DIM,
            )
            self.surface.blit(step_lbl, (bar_rect.right - step_lbl.get_width(), bar_rect.y - 14))

    def _draw_topbar(self) -> None:
        top_rect = pygame.Rect(0, 0, WINDOW_WIDTH - SIDEBAR_WIDTH, TOPBAR_HEIGHT)
        pygame.draw.rect(self.surface, COLOR_PANEL, top_rect)
        pygame.draw.line(self.surface, COLOR_BORDER,
                         (0, TOPBAR_HEIGHT), (top_rect.right, TOPBAR_HEIGHT), 1)
        lbl = self._font_bold.render("Graph Algorithms Visualization Platform", True, COLOR_TEXT)
        self.surface.blit(lbl, (14, TOPBAR_HEIGHT // 2 - lbl.get_height() // 2))
        hint = self._font_small.render(
            "LClick:add node | Select + LClick:edge | RClick:delete | MMB:pan",
            True, COLOR_TEXT_DIM,
        )
        self.surface.blit(hint, (WINDOW_WIDTH - SIDEBAR_WIDTH - hint.get_width() - 12,
                                 TOPBAR_HEIGHT // 2 - hint.get_height() // 2))

    def _draw_status(self) -> None:
        H = WINDOW_HEIGHT
        bar = pygame.Rect(0, H - 24, WINDOW_WIDTH - SIDEBAR_WIDTH, 24)
        msg = self._error_msg if self._error_timer > 0 else self._status
        color = (200, 60, 60) if self._error_timer > 0 else None
        draw_status_bar(self.surface, bar, msg)
        if color:
            font = self._font_small
            lbl = font.render(msg, True, color)
            self.surface.blit(lbl, (bar.x + 12, bar.centery - lbl.get_height() // 2))

    def _draw_weight_popup(self) -> None:
        W, H = WINDOW_WIDTH, WINDOW_HEIGHT
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.surface.blit(overlay, (0, 0))
        popup = pygame.Rect(W // 2 - 120, H // 2 - 60, 240, 120)
        pygame.draw.rect(self.surface, COLOR_PANEL, popup, border_radius=8)
        pygame.draw.rect(self.surface, COLOR_BORDER, popup, 2, border_radius=8)
        lbl = self._font_ui.render("Enter edge weight:", True, COLOR_TEXT)
        self.surface.blit(lbl, lbl.get_rect(center=(W // 2, H // 2 - 38)))
        self._weight_input.draw(self.surface)
        self._btn_confirm_weight.draw(self.surface)

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------

    def _is_canvas_pos(self, screen_pos: tuple) -> bool:
        """Return True if the screen position is within the canvas area."""
        x, y = screen_pos
        return (
            x < WINDOW_WIDTH - SIDEBAR_WIDTH and
            y > TOPBAR_HEIGHT and
            y < WINDOW_HEIGHT - 24
        )

    def _to_graph_coords(self, screen_pos: tuple) -> tuple:
        ox, oy = self._offset
        return (screen_pos[0] - ox, screen_pos[1] - oy)

    def _node_at(self, canvas_pos: tuple) -> Optional[int]:
        """Return the ID of the node at (canvas) position, or None."""
        cx, cy = canvas_pos
        for node_id, (nx, ny) in self.ctrl.graph.nodes.items():
            if (nx - cx) ** 2 + (ny - cy) ** 2 <= NODE_RADIUS ** 2:
                return node_id
        return None

    # ------------------------------------------------------------------
    # Error helper
    # ------------------------------------------------------------------

    def _set_error(self, msg: str, duration: float = 3.0) -> None:
        self._error_msg   = msg
        self._error_timer = duration
