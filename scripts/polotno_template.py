#!/usr/bin/env python3
"""
Polotno-based notebook page template — generates individual hole and ring
SVG elements positioned absolutely, matching the VERIQTA blank page template
from Polotno.

Unlike the old CSS background-repeat approach, this template creates each
hole and ring as a separate SVG element. The number of holes/rings is
calculated based on the page height, so they can be added/removed as needed.

Key measurements (from Polotno JSON):
- Page: 1220 × H (height varies per page)
- Paper: 1080 × paperH (positioned at x=62.97, y=24)
- Hole: 18.5×18.5, x=89.93, y_start=50.025 (relative to page), spacing=59.5
- Ring: 76×23.2, x=35.48, y_start=45.675 (relative to page), spacing=59.5
- Top edge: full paper width, h=13.69
- Bottom edge: full paper width, h=14.74
"""

import math
from pathlib import Path

# ============================================================
# SVG TEMPLATES (extracted from Polotno JSON)
# ============================================================

HOLE_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='18.5' height='18.5' viewBox='0 0 18.5 18.5'><defs><radialGradient id='h{id}' cx='0%' cy='45%' r='105%'><stop offset='0' stop-color='#000000' stop-opacity='0'/><stop offset='0.12' stop-color='#000000' stop-opacity='0'/><stop offset='0.28' stop-color='#111111' stop-opacity='0.25'/><stop offset='0.42' stop-color='#000000' stop-opacity='0.7'/><stop offset='0.55' stop-color='#000000' stop-opacity='0.95'/><stop offset='0.7' stop-color='#000000' stop-opacity='1'/><stop offset='1' stop-color='#000000' stop-opacity='1'/></radialGradient><linearGradient id='r{id}' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='#000000' stop-opacity='0'/><stop offset='0.25' stop-color='#000000' stop-opacity='0'/><stop offset='0.4' stop-color='#000000' stop-opacity='0.5'/><stop offset='0.55' stop-color='#000000' stop-opacity='0.9'/><stop offset='0.7' stop-color='#000000' stop-opacity='1'/><stop offset='1' stop-color='#000000' stop-opacity='1'/></linearGradient><clipPath id='c{id}'><circle cx='9.25' cy='9.25' r='9'/></clipPath></defs><circle cx='9.25' cy='9.25' r='9' fill='url(#h{id})'/><circle cx='9.25' cy='9.25' r='9' fill='url(#r{id})' clip-path='url(#c{id})'/><circle cx='9.25' cy='9.25' r='7' fill='#000000'/><circle cx='9.25' cy='9.25' r='9' fill='none' stroke='#000000' stroke-width='0.5' opacity='0.3'/></svg>"""

RING_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='76' height='23.2' viewBox='21.675 76 23.2'><path d='M27.2 22.95 C17 23.8 8.5 27.2 8.5 29.75 C8.5 34 16.15 36.55 27.2 37.4 C44.2 38.7 62.2 36.4 74 32.5 M27.2 30.35 C17 31.2 8.5 34.6 8.5 37.15 C8.5 41.4 16.15 43.95 27.2 44.8 C44.2 46.1 62.2 43.8 74 39.9' fill='none' stroke='#111' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/></svg>"""

PAPER_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='{paper_h}' viewBox='0 0 1080 {paper_h}' preserveAspectRatio='none'><defs><clipPath id='pc'><rect width='1080' height='{paper_h}' rx='14' ry='14'/></clipPath><pattern id='grid' width='26' height='26' patternUnits='userSpaceOnUse'><rect width='26' height='1' fill='#bcc8d6'/><rect width='1' height='26' fill='#bcc8d6'/></pattern><linearGradient id='bend' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='#000000' stop-opacity='0.45'/><stop offset='0.1667' stop-color='#000000' stop-opacity='0.30'/><stop offset='0.3889' stop-color='#000000' stop-opacity='0.18'/><stop offset='0.6667' stop-color='#000000' stop-opacity='0.08'/><stop offset='0.8889' stop-color='#000000' stop-opacity='0.03'/><stop offset='1' stop-color='#000000' stop-opacity='0'/></linearGradient></defs><g clip-path='url(#pc)'><rect width='1080' height='{paper_h}' fill='#f5f1e8'/><rect width='1080' height='{paper_h}' fill='url(#grid)' opacity='0.5'/><rect width='18' height='{paper_h}' fill='url(#bend)'/></g></svg>"""

TOP_EDGE_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='13' viewBox='0 0 1080 13' preserveAspectRatio='none'><defs><clipPath id='tc'><rect x='0' y='0' width='1080' height='28' rx='14' ry='14'/></clipPath><pattern id='tlines' width='2.4' height='2.4' patternUnits='userSpaceOnUse'><rect width='2.4' height='0.4' fill='rgba(140,120,80,0.12)'/></pattern></defs><g clip-path='url(#tc)'><rect width='1080' height='13' fill='url(#tlines)'/><rect width='1080' height='7' fill='#fbf8ef'/><rect width='1080' height='4' y='7' fill='#f7f3e8'/><rect width='1080' height='2' y='11' fill='#f5f1e8'/><rect width='1080' height='0.5' y='12.5' fill='rgba(100,80,40,0.22)'/></g></svg>"""

BOTTOM_EDGE_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='14' viewBox='0 0 1080 14' preserveAspectRatio='none'><defs><clipPath id='bc'><rect x='0' y='-15' width='1080' height='29' rx='14' ry='14'/></clipPath><pattern id='blines' width='2.4' height='2.4' patternUnits='userSpaceOnUse'><rect width='2.4' height='0.4' fill='rgba(140,120,80,0.12)'/></pattern></defs><g clip-path='url(#bc)'><rect width='1080' height='14' fill='url(#blines)'/><rect width='1080' height='7' y='7' fill='#fbf8ef'/><rect width='1080' height='4' y='10' fill='#f7f3e8'/><rect width='1080' height='2' y='13' fill='#f5f1e8'/><rect width='1080' height='0.5' y='13' fill='rgba(100,80,40,0.22)'/></g></svg>"""

# ============================================================
# POSITIONING CONSTANTS
# ============================================================

PAPER_X = 62.975306
PAPER_Y = 24
PAPER_W = 1080

HOLE_X = 89.925306
HOLE_Y_START = 50.025  # relative to page top
HOLE_SIZE = 18.5
HOLE_SPACING = 59.5

RING_X = 35.475306
RING_Y_START = 45.675  # relative to page top
RING_W = 76
RING_H = 23.2
RING_SPACING = 59.5  # same as hole spacing

TOP_EDGE_H = 13.69
BOTTOM_EDGE_H = 14.74


def calc_hole_count(paper_height: float) -> int:
    """Calculate the number of holes/rings needed for a given paper height.

    The first hole is at y=26.025 relative to paper top (50.025 - 24).
    The last hole should leave a bottom margin of ~24px.
    Spacing between holes is 59.5px.
    """
    first_hole_y = HOLE_Y_START - PAPER_Y  # 26.025 relative to paper
    # Available space = paper_height - top_margin - hole_size - bottom_margin
    available = paper_height - first_hole_y - HOLE_SIZE - PAPER_Y
    count = max(1, int(math.floor(available / HOLE_SPACING)) + 1)
    return count


def generate_holes(count: int) -> str:
    """Generate HTML for `count` hole SVG elements."""
    holes = []
    for i in range(count):
        y = HOLE_Y_START + i * HOLE_SPACING
        svg = HOLE_SVG.replace("{id}", str(i))
        holes.append(
            f'<div class="hole" style="position:absolute;left:{HOLE_X}px;top:{y}px;width:{HOLE_SIZE}px;height:{HOLE_SIZE}px;">{svg}</div>'
        )
    return "\n    ".join(holes)


def generate_rings(count: int) -> str:
    """Generate HTML for `count` ring SVG elements."""
    rings = []
    for i in range(count):
        y = RING_Y_START + i * RING_SPACING
        rings.append(
            f'<div class="ring" style="position:absolute;left:{RING_X}px;top:{y}px;width:{RING_W}px;height:{RING_H}px;">{RING_SVG}</div>'
        )
    return "\n    ".join(rings)


def page_wrapper(content_html: str, paper_height: float = 1082.16) -> str:
    """Build a complete notebook page with individual holes and rings.

    Args:
        content_html: The page content (title, body, etc.)
        paper_height: Height of the paper sheet in px. Default 1082.16.

    Returns:
        HTML string for the page-wrapper div.
    """
    page_height = paper_height + PAPER_Y * 2  # paper + top/bottom margin
    hole_count = calc_hole_count(paper_height)

    holes_html = generate_holes(hole_count)
    rings_html = generate_rings(hole_count)

    # Paper SVG with correct height
    paper_svg = PAPER_SVG.replace("{paper_h}", str(paper_height))
    top_svg = TOP_EDGE_SVG
    bottom_svg = BOTTOM_EDGE_SVG

    bottom_edge_y = PAPER_Y + paper_height - 0.5  # slightly overlap paper bottom

    return f"""<div class="page-wrapper" style="position:relative;width:1220px;height:{page_height}px;overflow:visible;">

    <!-- Paper sheet with grid + left bend -->
    <div class="paper" style="position:absolute;left:{PAPER_X}px;top:{PAPER_Y}px;width:{PAPER_W + 57.462}px;height:{paper_height}px;">
      {paper_svg}
    </div>

    <!-- Page top edge (3D stack) -->
    <div class="page-top-edge" style="position:absolute;left:{PAPER_X}px;top:{PAPER_Y}px;width:{PAPER_W + 57.462}px;height:{TOP_EDGE_H}px;">
      {top_svg}
    </div>

    <!-- Spiral binding rings -->
    <div class="spiral-rings" style="position:absolute;left:0;top:0;width:1220px;height:{page_height}px;pointer-events:none;">
    {rings_html}
    </div>

    <!-- Binding holes -->
    <div class="binding-holes" style="position:absolute;left:0;top:0;width:1220px;height:{page_height}px;pointer-events:none;">
    {holes_html}
    </div>

    <!-- Page bottom edge (3D stack) -->
    <div class="page-bottom-edge" style="position:absolute;left:{PAPER_X}px;top:{bottom_edge_y}px;width:{PAPER_W + 57.462}px;height:{BOTTOM_EDGE_H}px;">
      {bottom_svg}
    </div>

    <!-- Content -->
    <div class="content" style="position:relative;z-index:2;padding:42px 50px 26px 78px;">
      {content_html}
    </div>

  </div>"""


def multi_page_html(pages: list[str], title: str = "Notebook") -> str:
    """Build a complete multi-page HTML document.

    Args:
        pages: List of page-wrapper HTML strings.
        title: Document title.

    Returns:
        Complete HTML document.
    """
    body = "\n\n  ".join(pages)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ box-sizing:border-box;margin:0;padding:0; }}
  html, body {{ background:#cfc9bb; }}
  body {{
    font-family:"Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;
    color:#1c1c1c;
    display:flex;flex-direction:column;align-items:center;
    gap:24px;
    padding:24px 48px;
  }}
  body.multi-page {{
    flex-direction:column;
    gap:24px;
    overflow:visible;
  }}
  .page-wrapper {{
    position:relative;
    overflow:visible;
    box-shadow:0 22px 60px rgba(0,0,0,0.28);
  }}
  @media print {{
    html, body {{ background:#fff;padding:0;gap:0; }}
    .page-wrapper {{ page-break-after:always; }}
    .page-wrapper:last-child {{ page-break-after:auto; }}
  }}
</style>
</head>
<body class="multi-page">

  {body}

</body>
</html>"""


if __name__ == "__main__":
    # Test: generate a single blank page
    html = page_wrapper("<h1>Test Page</h1><p>Content goes here.</p>")
    doc = multi_page_html([html], "Test Notebook")
    out = Path("/tmp/polotno-test-page.html")
    out.write_text(doc)
    print(f"Wrote {out} ({len(doc):,} bytes)")

    # Show hole count for different page heights
    for h in [800, 1082, 1200, 1400, 1600]:
        count = calc_hole_count(h)
        print(f"  Paper height {h}px → {count} holes/rings")
