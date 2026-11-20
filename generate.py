#!/usr/bin/env python3
"""Builds fetch.svg, a fastfetch-style card for the GitHub profile README.

Edit LOGO or INFO below, then run:  python3 generate.py
"""
from html import escape

# Dracula+ palette (matches the Ghostty theme)
BG = "#1f1c1b"  # warm near-black
BAR = "#2b2624"
FG = "#f6efe6"
DIM = "#8a7d74"
PINK = "#ff79c6"
PURPLE = "#bd93f9"
CYAN = "#8be9fd"
GREEN = "#50fa7b"
YELLOW = "#f1fa8c"
ORANGE = "#ffb86c"
RED = "#ff5555"

LOGO = [
    "███╗   ███╗███████╗██╗     ",
    "████╗ ████║██╔════╝██║     ",
    "██╔████╔██║█████╗  ██║     ",
    "██║╚██╔╝██║██╔══╝  ██║     ",
    "██║ ╚═╝ ██║███████╗███████╗",
    "╚═╝     ╚═╝╚══════╝╚══════╝",
]


def gradient(stops, n):
    """n colors fading evenly through the given hex stops."""
    rgb = [[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in stops]
    out = []
    for t in range(n):
        p = t / (n - 1) * (len(stops) - 1)
        i = min(int(p), len(stops) - 2)
        f = p - i
        out.append("#%02x%02x%02x" % tuple(round(a + (b - a) * f) for a, b in zip(rgb[i], rgb[i + 1])))
    return out


# yellow at the top fading to red at the bottom
LOGO_COLORS = gradient([YELLOW, ORANGE, RED], len(LOGO))
TITLE_COLOR = YELLOW  # mel@muunkk
KEY_COLOR = ORANGE  # Location, Packages, ...

# (key, value). key=None means a raw line (title / separator / blank).
INFO = [
    (None, "title"),
    (None, "sep"),
    ("Location", "New York City, Bangkok, Shanghai"),
    ("Packages", "tutornet, vector, munk, subtrakt, workingset"),
    ("Theme", "Dracula+"),
    ("Font", "MesloLGS NF 16pt"),
    ("Contact", "x.com/melboonchan · melboonchan.com"),
    (None, "blank"),
    (None, "colors"),
]

USER, HOST = "mel", "muunkk"

# Layout
FONT = 15
LINE = 21
CHAR_W = FONT * 0.6  # monospace advance width
PAD_X = 28
LOGO_FONT = 18
LOGO_LINE = 21  # tight so block glyphs touch
TOP = 64  # below the title bar

logo_w = max(len(l) for l in LOGO) * LOGO_FONT * 0.6
info_x = PAD_X + logo_w + 36
longest = max(len(k) + 2 + len(v) for k, v in INFO if k)
width = int(info_x + longest * CHAR_W + PAD_X + 8)
height = TOP + (len(INFO) + 1) * LINE + 30

out = []
w = out.append
w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
  f'viewBox="0 0 {width} {height}" role="img" aria-label="mel@muunkk: a fastfetch-style bio">')
w("""<style>
  text { font-family: ui-monospace, 'SFMono-Regular', 'MesloLGS NF', Menlo, Consolas, 'Liberation Mono', monospace; font-size: %dpx; white-space: pre; }
  .cursor { animation: blink 1.1s steps(1) infinite; }
  @keyframes blink { 50%% { opacity: 0; } }
  @media (prefers-reduced-motion: reduce) { .cursor { animation: none; } }
</style>""" % FONT)

# Window
w(f'<rect width="{width}" height="{height}" rx="12" fill="{BG}"/>')
w(f'<path d="M12 0h{width-24}a12 12 0 0 1 12 12v24H0V12A12 12 0 0 1 12 0z" fill="{BAR}"/>')
for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
    w(f'<circle cx="{22 + i*20}" cy="18" r="6" fill="{c}"/>')
w(f'<text x="{width/2}" y="23" fill="{DIM}" text-anchor="middle" style="font-size:12px">mel — fastfetch — 120×30</text>')

# Prompt line
w(f'<text x="{PAD_X}" y="{TOP - 8}"><tspan fill="{RED}">➜</tspan>  <tspan fill="{YELLOW}">~</tspan> <tspan fill="{FG}">fastfetch</tspan></text>')

# Logo, vertically centered against the info block
body_top = TOP + 18
logo_top = body_top + (len(INFO) * LINE - len(LOGO) * LOGO_LINE) / 2 - LINE / 2
for i, (line, color) in enumerate(zip(LOGO, LOGO_COLORS)):
    y = logo_top + i * LOGO_LINE
    w(f'<text x="{PAD_X}" y="{y:.1f}" fill="{color}" style="font-size:{LOGO_FONT}px">{escape(line)}</text>')

# Info
title = f"{USER}@{HOST}"
for i, (key, val) in enumerate(INFO):
    y = body_top + i * LINE
    if key is None:
        if val == "title":
            w(f'<text x="{info_x:.1f}" y="{y}"><tspan fill="{TITLE_COLOR}" font-weight="bold">{USER}</tspan><tspan fill="{FG}">@</tspan><tspan fill="{TITLE_COLOR}" font-weight="bold">{HOST}</tspan></text>')
        elif val == "sep":
            w(f'<text x="{info_x:.1f}" y="{y}" fill="{DIM}">{"-" * len(title)}</text>')
        elif val == "colors":
            sw = CHAR_W * 3
            for j, c in enumerate(["#44475a", RED, GREEN, YELLOW, PURPLE, PINK, CYAN, FG]):
                w(f'<rect x="{info_x + j*sw:.1f}" y="{y - FONT + 2}" width="{sw:.1f}" height="{LINE - 2}" fill="{c}"/>')
        continue
    w(f'<text x="{info_x:.1f}" y="{y}"><tspan fill="{KEY_COLOR}" font-weight="bold">{escape(key)}</tspan>'
      f'<tspan fill="{DIM}">: </tspan><tspan fill="{FG}">{escape(val)}</tspan></text>')

# fresh prompt with a blinking cursor
py = body_top + (len(INFO) + 0.6) * LINE
w(f'<text x="{PAD_X}" y="{py:.1f}"><tspan fill="{RED}">➜</tspan>  <tspan fill="{YELLOW}">~</tspan> </text>')
w(f'<rect class="cursor" x="{PAD_X + 5*CHAR_W:.1f}" y="{py - FONT + 2:.1f}" width="{CHAR_W:.1f}" height="{FONT + 3}" fill="{ORANGE}"/>')

w("</svg>")

with open("fetch.svg", "w") as f:
    f.write("\n".join(out) + "\n")
print(f"wrote fetch.svg ({width}x{height})")
