# ============================================================
# utils/constants.py — Global constants for the application
# ============================================================

# --- Window ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Graph Algorithms Visualization Platform"
FPS = 60

# --- Colors (R, G, B) ---
COLOR_BG          = (15,  17,  26)
COLOR_PANEL       = (22,  26,  40)
COLOR_BORDER      = (50,  60,  90)
COLOR_TEXT        = (220, 230, 255)
COLOR_TEXT_DIM    = (120, 130, 160)
COLOR_ACCENT      = (80,  160, 255)
COLOR_SUCCESS     = (60,  210, 120)
COLOR_WARNING     = (255, 200,  60)
COLOR_DANGER      = (255,  80,  80)

# --- Node visual ---
NODE_RADIUS       = 22
NODE_COLOR_DEFAULT = (40,  55,  90)
NODE_COLOR_BORDER  = (80, 120, 200)
NODE_COLOR_VISITED = (60, 180, 255)
NODE_COLOR_PROCESSED = (40, 210, 130)
NODE_COLOR_SOURCE  = (255, 180,  50)
NODE_COLOR_PATH    = (255, 100, 180)
NODE_COLOR_COMPONENT = [
    (120,  80, 220),
    (80,  200, 120),
    (220, 120,  60),
    (60,  180, 220),
    (220,  60, 120),
]

# --- Edge visual ---
EDGE_WIDTH         = 2
EDGE_COLOR_DEFAULT = (60,  75, 110)
EDGE_COLOR_EXPLORE = (80, 160, 255)
EDGE_COLOR_RELAX   = (255, 200,  60)
EDGE_COLOR_REJECT  = (180,  50,  50)
EDGE_COLOR_SELECT  = (60,  210, 130)
EDGE_COLOR_DISCARD = (100,  60,  60)
EDGE_COLOR_FINAL   = (255, 100, 180)

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
