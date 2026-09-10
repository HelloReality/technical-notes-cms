#!/usr/bin/env python3
"""
Polotno-based notebook page template — generates individual hole and ring
SVG elements positioned absolutely, matching EXACTLY the VERIQTA blank page
template from Polotno.

The SVG content for each element is extracted verbatim from the Polotno JSON
to ensure pixel-perfect rendering.

Key measurements (from Polotno JSON):
- Page: 1220 × H (height = paper_height + 2 * PAPER_Y)
- Paper: 1080 × paperH (positioned at x=62.975306, y=24)
- Hole: 18.5×18.5, x=89.925306, y_start=50.025, spacing=59.5
- Ring: 76×23.2, x=35.475306, y_start=45.675, spacing=59.5
- Top edge: 1137.462023 × 13.691672
- Bottom edge: 1137.462023 × 14.744878
"""

import math
from pathlib import Path

# ============================================================
# SVG CONTENT — extracted verbatim from Polotno JSON
# Each {ID} placeholder is replaced with a unique index to avoid
# SVG ID collisions when multiple elements appear on the same page.
# ============================================================

# Hole SVG — 18.5×18.5px with 3D radial+linear gradients
HOLE_SVG_TEMPLATE = """<svg xmlns='http://www.w3.org/2000/svg' width='18.5' height='18.5' viewBox='0 0 18.5 18.5'><defs><radialGradient id='h{id}' cx='0%' cy='45%' r='105%'><stop offset='0' stop-color='#000000' stop-opacity='0'/><stop offset='0.12' stop-color='#000000' stop-opacity='0'/><stop offset='0.28' stop-color='#111111' stop-opacity='0.25'/><stop offset='0.42' stop-color='#000000' stop-opacity='0.7'/><stop offset='0.55' stop-color='#000000' stop-opacity='0.95'/><stop offset='0.7' stop-color='#000000' stop-opacity='1'/><stop offset='1' stop-color='#000000' stop-opacity='1'/></radialGradient><linearGradient id='r{id}' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='#000000' stop-opacity='0'/><stop offset='0.25' stop-color='#000000' stop-opacity='0'/><stop offset='0.4' stop-color='#000000' stop-opacity='0.5'/><stop offset='0.55' stop-color='#000000' stop-opacity='0.9'/><stop offset='0.7' stop-color='#000000' stop-opacity='1'/><stop offset='1' stop-color='#000000' stop-opacity='1'/></linearGradient><clipPath id='c{id}'><circle cx='9.25' cy='9.25' r='9'/></clipPath></defs><circle cx='9.25' cy='9.25' r='9' fill='url(#h{id})'/><circle cx='9.25' cy='9.25' r='9' fill='url(#r{id})' clip-path='url(#c{id})'/><circle cx='9.25' cy='9.25' r='7' fill='#000000'/><circle cx='9.25' cy='9.25' r='9' fill='none' stroke='#000000' stroke-width='0.5' opacity='0.3'/></svg>"""

# Ring SVG — 76×23.2px with 2 separate path elements (exact from Polotno)
RING_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='76' height='23.2' viewBox='0 21.675 76 23.2'><path d='M27.2 22.95 C17 23.8 8.5 27.2 8.5 29.75 C8.5 34 16.15 36.55 27.2 37.4 C44.2 38.25 59.5 35.7 69.7 32.3' fill='none' stroke='#111111' stroke-width='2.55' stroke-linecap='round' stroke-linejoin='round'/><path d='M27.2 28.9 C17 29.75 8.5 33.15 8.5 35.7 C8.5 39.95 16.15 42.5 27.2 43.35 C44.2 44.2 59.5 41.65 69.7 38.25' fill='none' stroke='#111111' stroke-width='2.55' stroke-linecap='round' stroke-linejoin='round'/></svg>"""

# Paper SVG — grid pattern + left bend shadow
PAPER_SVG_TEMPLATE = """<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='{paper_h}' viewBox='0 0 1080 {paper_h}' preserveAspectRatio='none'><defs><clipPath id='pc'><rect width='1080' height='{paper_h}' rx='14' ry='14'/></clipPath><pattern id='grid' width='26' height='26' patternUnits='userSpaceOnUse'><rect width='26' height='1' fill='#bcc8d6'/><rect width='1' height='26' fill='#bcc8d6'/></pattern><linearGradient id='bend' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='#000000' stop-opacity='0.45'/><stop offset='0.1667' stop-color='#000000' stop-opacity='0.30'/><stop offset='0.3889' stop-color='#000000' stop-opacity='0.18'/><stop offset='0.6667' stop-color='#000000' stop-opacity='0.08'/><stop offset='0.8889' stop-color='#000000' stop-opacity='0.03'/><stop offset='1' stop-color='#000000' stop-opacity='0'/></linearGradient></defs><g clip-path='url(#pc)'><rect width='1080' height='{paper_h}' fill='#f5f1e8'/><rect width='1080' height='{paper_h}' fill='url(#grid)' opacity='0.5'/><rect width='18' height='{paper_h}' fill='url(#bend)'/></g></svg>"""

# Top edge SVG — 3D page-stack thickness
TOP_EDGE_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='13' viewBox='0 0 1080 13' preserveAspectRatio='none'><defs><clipPath id='tc'><rect x='0' y='0' width='1080' height='28' rx='14' ry='14'/></clipPath><pattern id='tlines' width='2.4' height='2.4' patternUnits='userSpaceOnUse'><rect width='2.4' height='0.4' fill='rgba(140,120,80,0.12)'/></pattern></defs><g clip-path='url(#tc)'><rect width='1080' height='13' fill='url(#tlines)'/><rect width='1080' height='7' fill='#fbf8ef'/><rect width='1080' height='4' y='7' fill='#f7f3e8'/><rect width='1080' height='2' y='11' fill='#f5f1e8'/><rect width='1080' height='0.5' y='12.5' fill='rgba(100,80,40,0.22)'/></g></svg>"""

# Bottom edge SVG — 3D page-stack thickness
BOTTOM_EDGE_SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='14' viewBox='0 0 1080 14' preserveAspectRatio='none'><defs><clipPath id='bc'><rect x='0' y='-15' width='1080' height='29' rx='14' ry='14'/></clipPath><pattern id='blines' width='2.4' height='2.4' patternUnits='userSpaceOnUse'><rect width='2.4' height='0.4' fill='rgba(140,120,80,0.12)'/></pattern></defs><g clip-path='url(#bc)'><rect width='1080' height='14' fill='url(#blines)'/><rect width='1080' height='7' y='7' fill='#fbf8ef'/><rect width='1080' height='4' y='10' fill='#f7f3e8'/><rect width='1080' height='2' y='13' fill='#f5f1e8'/><rect width='1080' height='0.5' y='13' fill='rgba(100,80,40,0.22)'/></g></svg>"""

# ============================================================
# POSITIONING CONSTANTS (exact from Polotno JSON)
# ============================================================

PAGE_WIDTH = 1220

PAPER_X = 62.975306
PAPER_Y = 24
PAPER_W = 1137.462023  # full width including binding overflow
PAPER_DESIGN_W = 1080  # the design width (paper content)

HOLE_X = 89.925306
HOLE_Y_START = 50.025  # relative to page top
HOLE_SIZE = 18.5
HOLE_SPACING = 59.5

RING_X = 35.475306
RING_Y_START = 45.675  # relative to page top
RING_W = 76
RING_H = 23.2
RING_SPACING = 59.5  # same as hole spacing

TOP_EDGE_H = 13.691672
BOTTOM_EDGE_H = 14.744878

# Default paper height (matches Polotno original exactly)
DEFAULT_PAPER_H = 1139.736947


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


def generate_holes(count: int, id_prefix: str = "") -> str:
    """Generate HTML for `count` hole SVG elements with unique gradient IDs."""
    holes = []
    for i in range(count):
        y = HOLE_Y_START + i * HOLE_SPACING
        svg = HOLE_SVG_TEMPLATE.replace("{id}", f"{id_prefix}{i}")
        holes.append(
            f'<div style="position:absolute;left:{HOLE_X}px;top:{y}px;width:{HOLE_SIZE}px;height:{HOLE_SIZE}px;">{svg}</div>'
        )
    return "\n    ".join(holes)


def generate_rings(count: int) -> str:
    """Generate HTML for `count` ring SVG elements."""
    rings = []
    for i in range(count):
        y = RING_Y_START + i * RING_SPACING
        rings.append(
            f'<div style="position:absolute;left:{RING_X}px;top:{y}px;width:{RING_W}px;height:{RING_H}px;">{RING_SVG}</div>'
        )
    return "\n    ".join(rings)


def page_wrapper(content_html: str, paper_height: float = DEFAULT_PAPER_H, page_id: str = "") -> str:
    """Build a complete notebook page with individual holes and rings.

    Args:
        content_html: The page content (title, body, etc.)
        paper_height: Height of the paper sheet in px. Default 1082.16.
        page_id: Unique ID for this page (avoids SVG gradient ID collisions
                 when multiple pages appear in the same document).

    Returns:
        HTML string for the page-wrapper div.
    """
    page_height = paper_height + PAPER_Y + PAPER_Y * 0.268  # paper + top margin + bottom margin (matches Polotno: 1139.736947 + 24 + 6.423 = 1170.16)
    hole_count = calc_hole_count(paper_height)

    # Generate holes with unique IDs
    holes_html = generate_holes(hole_count, id_prefix=page_id)
    rings_html = generate_rings(hole_count)

    # Paper SVG with correct height
    paper_svg = PAPER_SVG_TEMPLATE.replace("{paper_h}", str(paper_height))
    top_svg = TOP_EDGE_SVG
    bottom_svg = BOTTOM_EDGE_SVG

    bottom_edge_y = PAPER_Y + paper_height - BOTTOM_EDGE_H  # edge bottom = paper bottom

    return f"""<div class="page-wrapper" style="position:relative;width:{PAGE_WIDTH}px;height:{page_height}px;overflow:visible;box-shadow:0 22px 60px rgba(0,0,0,0.28);">

    <!-- Paper sheet with grid + left bend -->
    <div style="position:absolute;left:{PAPER_X}px;top:{PAPER_Y}px;width:{PAPER_W}px;height:{paper_height}px;">
      {paper_svg}
    </div>

    <!-- Page top edge (3D stack) -->
    <div style="position:absolute;left:{PAPER_X}px;top:{PAPER_Y}px;width:{PAPER_W}px;height:{TOP_EDGE_H}px;">
      {top_svg}
    </div>

    <!-- Spiral binding rings -->
    <div style="position:absolute;left:0;top:0;width:{PAGE_WIDTH}px;height:{page_height}px;pointer-events:none;">
    {rings_html}
    </div>

    <!-- Binding holes -->
    <div style="position:absolute;left:0;top:0;width:{PAGE_WIDTH}px;height:{page_height}px;pointer-events:none;">
    {holes_html}
    </div>

    <!-- Page bottom edge (3D stack) -->
    <div style="position:absolute;left:{PAPER_X}px;top:{bottom_edge_y}px;width:{PAPER_W}px;height:{BOTTOM_EDGE_H}px;">
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
    # Test: generate a single blank page matching the Polotno reference
    html = page_wrapper(
        '<div style="padding:60px 0 0 0;"><h1 style="font-size:38px;color:#1B5E3F;font-weight:800;text-transform:uppercase;">Page Title</h1><p style="margin-top:12px;font-size:14px;color:#3a3f47;">Content goes here.</p></div>',
        paper_height=DEFAULT_PAPER_H,
        page_id="p1"
    )
    doc = multi_page_html([html], "Polotno Template Test")
    out = Path("/tmp/polotno-test-exact.html")
    out.write_text(doc)
    print(f"Wrote {out} ({len(doc):,} bytes)")

    # Show hole count for different page heights
    for h in [800, 1082, 1200, 1400, 1600]:
        count = calc_hole_count(h)
        print(f"  Paper height {h}px → {count} holes/rings")
