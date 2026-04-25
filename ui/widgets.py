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
