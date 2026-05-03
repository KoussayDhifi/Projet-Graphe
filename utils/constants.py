# ============================================================
# utils/constants.py — Global constants for the application
# ============================================================

# --- Window ---
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Graph Algorithms Visualization Platform"
FPS = 60

# --- Colors (R, G, B) ---
# Format: (Red, Green, Blue) → intensity from 0 to 255

COLOR_BG          = (15,  17,  26)   # very dark blue/black (low R, low G, slightly higher B)
COLOR_PANEL       = (22,  26,  40)   # dark navy blue
COLOR_BORDER      = (50,  60,  90)   # muted blue-gray
COLOR_TEXT        = (220, 230, 255)  # very light bluish white
COLOR_TEXT_DIM    = (120, 130, 160)  # soft gray with blue tint
COLOR_ACCENT      = (80,  160, 255)  # bright sky blue (strong B, medium G)
COLOR_SUCCESS     = (60,  210, 120)  # green (high G → success vibe)
COLOR_WARNING     = (255, 200,  60)  # yellow/orange (high R + G)
COLOR_DANGER      = (255,  80,  80)  # red (high R → danger)

# --- Node visual ---
NODE_RADIUS        = 22

NODE_COLOR_DEFAULT = (40,  55,  90)   # dark blue
NODE_COLOR_BORDER  = (80, 120, 200)   # medium blue
NODE_COLOR_VISITED = (60, 180, 255)   # bright cyan/blue (visited highlight)
NODE_COLOR_PROCESSED = (40, 210, 130) # green (processed/finalized)
NODE_COLOR_SOURCE  = (255, 180,  50)  # orange (source node)
NODE_COLOR_PATH    = (255, 100, 180)  # pink/magenta (final path)

NODE_COLOR_COMPONENT = [
    (120,  80, 220),  # purple
    (80,  200, 120),  # green
    (220, 120,  60),  # orange
    (60,  180, 220),  # cyan
    (220,  60, 120),  # pink/red
]

# --- Edge visual ---
EDGE_WIDTH         = 2

EDGE_COLOR_DEFAULT = (60,  75, 110)   # dark blue-gray
EDGE_COLOR_EXPLORE = (80, 160, 255)   # bright blue (exploring)
EDGE_COLOR_RELAX   = (255, 200,  60)  # yellow (relaxation step)
EDGE_COLOR_REJECT  = (180,  50,  50)  # dark red (rejected edge)
EDGE_COLOR_SELECT  = (60,  210, 130)  # green (selected edge)
EDGE_COLOR_DISCARD = (100,  60,  60)  # muted brown/red (discarded)
EDGE_COLOR_FINAL   = (255, 100, 180)  # pink (final result)

# --- Animation ---
ANIMATION_SPEED_DEFAULT = 0.5   # seconds per step
ANIMATION_SPEED_MIN     = 0.05
ANIMATION_SPEED_MAX     = 2.0

# --- UI Panel widths ---
SIDEBAR_WIDTH  = 260
TOPBAR_HEIGHT  = 60

# --- Creators ---
CREATORS = [
    "AmenAllah KALAII",
    "Youssef FNED",
    "Mohammed Adem SELMI",
    "Jalel Eddine BEN ROMDHANE",
    "Koussay DHIFI",
]
