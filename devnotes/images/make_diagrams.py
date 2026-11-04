"""Draws the diagrams for the devnotes as SVG files.

A line is an ordered list of cells. Each dot has four cells (NW, NE, SE, SW)
at its corners. The curve is a closed quadratic B-spline: cell centres are
control points, and the curve passes through the midpoints between
consecutive cell centres. A "pointy" cell is passed through exactly, which
gives a sharp corner.

Run: python3 make_diagrams.py   (writes the .svg files next to this script)
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).parent
U = 120          # pixels between neighbouring dots
CELL = 0.25      # cell centre offset from its dot, in dot spacings

INK = "#1f1b16"
GOLD = "#d08f1c"
TEAL = "#1e8c85"
RED = "#b5452f"
FAINT = "#c9c2b6"
OFFS = {"NW": (-1, -1), "NE": (1, -1), "SE": (1, 1), "SW": (-1, 1)}


def cell(dot: tuple[float, float], corner: str) -> tuple[float, float]:
    dx, dy = OFFS[corner]
    return dot[0] + dx * CELL, dot[1] + dy * CELL


def path_d(cells: list[tuple[float, float]], pointy: frozenset[int] | None = None,
           ox: float = 0.0, oy: float = 0.0) -> str:
    """SVG path for a closed line through cells (closed quadratic B-spline)."""
    pointy = pointy or frozenset()
    p = [((x + ox) * U, (y + oy) * U) for x, y in cells]
    n = len(p)
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    f = lambda q: f"{q[0]:.1f},{q[1]:.1f}"
    start = mid(p[-1], p[0])
    d = [f"M{f(start)}"]
    for i in range(n):
        end = mid(p[i], p[(i + 1) % n])
        if i in pointy:
            d.append(f"L{f(p[i])} L{f(end)}")
        else:
            d.append(f"Q{f(p[i])} {f(end)}")
    return " ".join(d) + " Z"


def svg(width, height, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="system-ui, sans-serif">'
        f'<rect width="100%" height="100%" fill="#fbf8f2"/>{body}</svg>\n'
    )


def dot(x, y, ox=0.0, oy=0.0, hidden=False) -> str:
    cx, cy = (x + ox) * U, (y + oy) * U
    if hidden:
        return (f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{INK}" '
                f'stroke-width="1.5" stroke-dasharray="3 3"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="6" fill="{INK}"/>'


def line(cells: list[tuple[float, float]], color: str = GOLD, pointy: frozenset[int] | None = None,
         ox: float = 0.0, oy: float = 0.0, width: int = 6) -> str:
    return (f'<path d="{path_d(cells, pointy, ox, oy)}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linejoin="round"/>')


def label(x, y, text, size=15, color=INK, anchor="middle") -> str:
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}">{text}</text>')


def cell_grid(dots, ox, oy) -> str:
    """Faint squares showing each dot's four cells."""
    out = []
    s = 2 * CELL * U
    for x, y in dots:
        for corner in OFFS:
            cx, cy = cell((x, y), corner)
            out.append(f'<rect x="{(cx + ox) * U - s / 2}" y="{(cy + oy) * U - s / 2}" '
                       f'width="{s}" height="{s}" fill="none" stroke="{FAINT}" stroke-width="1"/>')
    return "".join(out)


A, B = (0.0, 0.0), (1.0, 0.0)
# Figure-eight around two dots: once around A, cross over, once around B.
EIGHT = [cell(A, "NE"), cell(A, "NW"), cell(A, "SW"), cell(A, "SE"),
         cell(B, "NW"), cell(B, "NE"), cell(B, "SE"), cell(B, "SW")]


def four_vertices() -> str:
    """A dot split into four cells; cells joined into a line; the smoothed result."""
    body = []
    # Panel 1: one dot, four labelled cells
    ox, oy = 1.1, 1.2
    body.append(cell_grid([A], ox, oy))
    body.append(dot(*A, ox, oy))
    for corner in OFFS:
        cx, cy = cell(A, corner)
        body.append(f'<circle cx="{(cx + ox) * U}" cy="{(cy + oy) * U}" r="4" fill="{GOLD}"/>')
        body.append(label((cx + ox) * U, (cy + oy) * U + (-12 if "N" in corner else 22),
                          corner, 13, GOLD))
    body.append(label(ox * U, 2.35 * U, "1. A point has 4 cells (vertices)"))
    # Panel 2: two dots, cells joined in order (straight edges)
    ox2 = 2.6
    body.append(cell_grid([A, B], ox2, oy))
    pts = " ".join(f"{(x + ox2) * U:.1f},{(y + oy) * U:.1f}" for x, y in EIGHT)
    body.append(f'<polygon points="{pts}" fill="none" stroke="{TEAL}" stroke-width="4" '
                f'stroke-linejoin="round"/>')
    body += [dot(*A, ox2, oy), dot(*B, ox2, oy)]
    body.append(label((ox2 + 0.5) * U, 2.35 * U, "2. Connect cells into a line"))
    # Panel 3: the same cells, smoothed
    ox3 = 5.0
    body.append(line(EIGHT, GOLD, ox=ox3, oy=oy))
    body += [dot(*A, ox3, oy), dot(*B, ox3, oy)]
    body.append(label((ox3 + 0.5) * U, 2.35 * U, "3. Smooth it into a sona"))
    return svg(int(6.6 * U), int(2.6 * U), "".join(body))


def plaited(cols: int, rows: int) -> list[list[tuple[float, float]]]:
    """The lines of a plain plaited sona on a cols x rows dot grid.

    Billiard construction: the line runs diagonally through the points halfway
    between neighbouring dots and bounces off the border. Coordinates are in
    half dot spacings while tracing (dots at odd positions), then converted.
    A grid gives gcd(cols, rows) separate lines.
    """
    W, H = 2 * cols, 2 * rows
    used: set[frozenset] = set()
    lines = []
    starts = [(x, y, dx, dy) for y in range(H + 1) for x in range(W + 1) if (x + y) % 2
              for dx in (1, -1) for dy in (1, -1)]
    for x0, y0, dx0, dy0 in starts:
        nx, ny = x0 + dx0, y0 + dy0
        if not (0 <= nx <= W and 0 <= ny <= H) or frozenset({(x0, y0), (nx, ny)}) in used:
            continue
        pts, (x, y, dx, dy) = [], (x0, y0, dx0, dy0)
        while True:
            pts.append((x, y))
            if not 0 <= x + dx <= W:
                dx = -dx
            if not 0 <= y + dy <= H:
                dy = -dy
            edge = frozenset({(x, y), (x + dx, y + dy)})
            if edge in used:  # back where the line started
                break
            used.add(edge)
            x, y = x + dx, y + dy
        pts.pop()  # the start point, appended again on the way back
        lines.append([((px - 1) / 2, (py - 1) / 2) for px, py in pts])
    return lines


def layers() -> str:
    """Multilinear: one pattern made of several lines on the same dots, one layer per line."""
    ox, oy = 0.9, 0.75
    body = [line(pts, color, ox=ox, oy=oy)
            for pts, color in zip(plaited(3, 3), (GOLD, TEAL, RED))]
    body += [dot(x, y, ox, oy) for y in range(3) for x in range(3)]
    for i, (color, name) in enumerate(((GOLD, "Layer 1"), (TEAL, "Layer 2"), (RED, "Layer 3"))):
        body.append(label(3.6 * U, (1.0 + 0.5 * i) * U, name, 16, color, "start"))
    body.append(label(2.3 * U, 3.55 * U, "One sona, three lines on the same dots: one layer per line"))
    return svg(int(4.6 * U), int(3.85 * U), "".join(body))


def pointy() -> str:
    """The same line, smooth vs. one cell marked pointy."""
    oy = 1.0
    nw = EIGHT.index(cell(A, "NW"))
    body = [line(EIGHT, GOLD, ox=0.9, oy=oy), dot(*A, 0.9, oy), dot(*B, 0.9, oy),
            line(EIGHT, GOLD, pointy=frozenset({nw}), ox=3.4, oy=oy),
            dot(*A, 3.4, oy), dot(*B, 3.4, oy)]
    px, py = cell(A, "NW")
    body.append(f'<circle cx="{(px + 3.4) * U}" cy="{(py + oy) * U}" r="14" fill="none" '
                f'stroke="{TEAL}" stroke-width="2"/>')
    body.append(label(1.4 * U, 1.9 * U, "Smooth"))
    body.append(label(3.9 * U, 1.9 * U, "NW cell set to pointy"))
    return svg(int(5.3 * U), int(2.2 * U), "".join(body))


def invisible_points() -> str:
    """An invisible point lets the line make a loop where there is no dot."""
    I = (0.0, -1.0)
    # Cross between A and B, then cross again between A and I to make a lobe.
    ear = [cell(A, "SW"), cell(A, "SE"), cell(B, "NW"), cell(B, "NE"),
           cell(B, "SE"), cell(B, "SW"), cell(A, "NE"),
           cell(I, "SW"), cell(I, "NW"), cell(I, "NE"), cell(I, "SE"),
           cell(A, "NW")]
    oy = 2.0
    body = [line(EIGHT, GOLD, ox=0.9, oy=oy), dot(*A, 0.9, oy), dot(*B, 0.9, oy),
            label(1.4 * U, 2.9 * U, "Dots only")]
    body += [line(ear, GOLD, ox=3.3, oy=oy), dot(*A, 3.3, oy), dot(*B, 3.3, oy),
             dot(*I, 3.3, oy, hidden=True),
             label(3.8 * U, 2.9 * U, "Editor: invisible point (dashed)")]
    body += [line(ear, GOLD, ox=5.7, oy=oy), dot(*A, 5.7, oy), dot(*B, 5.7, oy),
             label(6.2 * U, 2.9 * U, "Final drawing")]
    return svg(int(7.2 * U), int(3.2 * U), "".join(body))


if __name__ == "__main__":
    for name, make in {"four_vertices": four_vertices, "layers": layers,
                       "pointy": pointy, "invisible_points": invisible_points}.items():
        (OUT / f"{name}.svg").write_text(make())
        print("wrote", name + ".svg")
