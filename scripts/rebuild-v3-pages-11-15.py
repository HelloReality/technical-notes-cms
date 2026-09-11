#!/usr/bin/env python3
"""
Rebuild Shell Scripting Handbook carousel pages 11-15 using the Polotno
notebook template (scripts/polotno_template.py).

Uses:
  - polotno_template.page_wrapper(content_html, paper_height, page_id) and
    multi_page_html(pages, title) for the page scaffold (paper, grid, holes,
    rings, 3D edges) — pixel-perfect Polotno blank-page rendering.
  - shell_scripting_icons.ICONS / icon() — colorful filled multi-color SVGs.
  - VLM analyses from /tmp/analysis-page-{11..15}.json.

Layouts (per task spec):
  Page 11 — Functions & Reusable Scripts      : 2-col grid (8 cards) + footer
  Page 12 — Working with Files & Directories : 2-col grid (8 cards) + footer
  Page 13 — Text Processing for DevOps       : 2-col split (left=cmd cards,
                                                right=examples, bottom=best practices)
  Page 14 — Redirection, Pipes, and Logs      : 3-col grid (11 cards) + best practices
  Page 15 — Processes and Services           : 3-col grid (9 cards) + 2-col
                                                (quick ref + best practices) + takeaway

NO VERIQTA branding, NO social footer.

Output: downloads/instagram-DcaW1UljsVk/recreated-page-{11..15}.html
"""

import os
import sys
from pathlib import Path

# Make sibling icon library + polotno template importable
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from polotno_template import page_wrapper, DEFAULT_PAPER_H  # noqa: E402
from shell_scripting_icons import ICONS, icon as render_icon  # noqa: E402

# ============================================================
# CONSTANTS
# ============================================================
PROJECT_ROOT = SCRIPTS_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "downloads" / "instagram-DcaW1UljsVk"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAPER_H = 1424  # matches original image height at 1080px wide


# ============================================================
# ICON HELPER
# ============================================================
def icon(name: str, size: int = 36) -> str:
    """Return inline colorful filled SVG for a named icon."""
    return render_icon(name, size)


# ============================================================
# CONTENT CSS — extends polotno_template scaffold
# (polotno_template provides body, .page-wrapper, paper sheet, holes,
#  rings, 3D edges. We add content-only styling here.)
# ============================================================
CONTENT_CSS = r"""
:root{
  --paper:#f5f1e8;
  --paper-2:#efe9dd;
  --ink:#1c1c1c;
  --ink-2:#3a3f47;
  --green:#1B5E3F;
  --green-2:#164a32;
  --green-soft:#e8f5ee;
  --navy:#15264d;
  --navy-2:#1e3160;
  --blue:#2563eb;
  --blue-soft:#cfe0ff;
  --purple:#7c3aed;
  --purple-soft:#e2d4ff;
  --red:#dc2626;
  --red-soft:#ffd4d4;
  --gold:#d4a017;
  --gold-soft:#fce9b6;
  --orange:#e65100;
  --teal:#0d7377;
  --term-bg:#0d1117;
  --term-fg:#e6edf3;
}

/* Multi-page body (polotno_template provides this too, but ensure it
   matches for individual page files) */
html, body{ background:#cfc9bb; }
body{
  font-family:"Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
  color:var(--ink);
  display:flex;flex-direction:column;align-items:center;
  gap:24px;
  padding:24px 48px;
}
body.multi-page{
  flex-direction:column;
  gap:24px;
  overflow:visible;
}

/* Content lives inside polotno_template's .content div (with padding
   42px 50px 26px 78px). Make sure stacking works. */
.content{ position:absolute !important; top:11px !important; left:0 !important; right:0 !important; bottom:11px !important; z-index:2; overflow:hidden; }

/* ============================================================
   POLOTNO PAPER SVG BACKGROUND FIX
   The polotno_template embeds the paper SVG (grid + bend) as the
   first inline child of the paper div. By default it's a static
   block that takes the full paper height, pushing the .content div
   (position:relative) below the visible area (clipped by overflow:hidden).
   Position it absolutely so it acts as the paper background and the
   content overlays it correctly.
   ============================================================ */
.page-wrapper > div:first-of-type > svg:first-of-type{
  position:absolute !important;
  top:0 !important;
  left:0 !important;
  width:100% !important;
  height:100% !important;
  pointer-events:none;
  z-index:0;
}

/* ============================================================
   BRAND BAR + PAGE BADGE
   ============================================================ */
.brand-bar{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:14px;
}
.brand-bar .crumb{
  font-size:11px;font-weight:700;letter-spacing:1.5px;
  color:var(--green);text-transform:uppercase;
  display:flex;align-items:center;gap:8px;
}
.brand-bar .crumb svg{display:block;}
.brand-bar .badge{
  background:var(--green);color:#fff;
  padding:5px 14px;border-radius:999px;
  font-size:10.5px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;
  box-shadow:0 3px 10px rgba(27,94,63,.30);
}

/* ============================================================
   PAGE TITLE + SUBTITLE
   ============================================================ */
.page-title{
  display:flex;align-items:center;justify-content:center;gap:14px;
  margin-bottom:6px;
}
.page-title .ico{flex-shrink:0;display:inline-flex;}
.page-title .ico svg{width:42px;height:42px;display:block;}
.page-title h1{
  font-size:32px;font-weight:800;color:var(--green);
  text-transform:uppercase;letter-spacing:-.5px;line-height:1.05;
  text-align:center;
}
.page-title h1 .num{color:var(--green-2);margin-right:8px;}
.page-subtitle{
  font-size:12.5px;font-weight:700;color:var(--ink-2);
  text-transform:uppercase;letter-spacing:1.4px;text-align:center;
  margin-bottom:14px;
  padding-bottom:10px;
  border-bottom:2px solid var(--green);
  position:relative;
}
.page-subtitle::after{
  content:"";position:absolute;left:50%;bottom:-6px;
  width:10px;height:10px;background:var(--green);
  border-radius:50%;transform:translateX(-50%);
}

/* ============================================================
   BODY LAYOUTS
   ============================================================ */
.body{margin-bottom:10px;}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;}
.grid-5{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;}

/* ============================================================
   CARD (header + body) — uniform dark green header (matches original)
   ============================================================ */
.card{
  background:#fff;
  border-radius:8px;
  overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
  border:1px solid rgba(0,0,0,.05);
  display:flex;flex-direction:column;
}
.card .head{
  background:var(--green);color:#fff;
  padding:6px 10px;
  font-size:11px;font-weight:800;letter-spacing:.4px;text-transform:uppercase;
  display:flex;align-items:center;gap:8px;
  line-height:1.2;
}
.card .head .num{
  background:rgba(255,255,255,.22);
  border-radius:5px;
  padding:1px 6px;font-size:9.5px;
}
.card .head .ico{flex-shrink:0;display:inline-flex;width:22px;height:22px;
  background:rgba(255,255,255,.15);border-radius:5px;
  align-items:center;justify-content:center;}
.card .head .ico svg{width:18px;height:18px;display:block;}
.card .body-pad{padding:8px 10px;flex:1;}

/* All card-header variants resolve to the same dark green so the page
   matches the original carousel's uniform header color scheme. */
.card.head-green  .head,
.card.head-blue   .head,
.card.head-purple .head,
.card.head-red    .head,
.card.head-gold   .head,
.card.head-teal   .head,
.card.head-navy   .head,
.card.head-orange .head{ background:#1B5E3F; }

/* ============================================================
   TERMINAL — LIGHT BEIGE CODE BLOCK (matches original carousel)
   Original uses light beige/cream code blocks with plain monospaced
   text, with red accents for strings and navy for keywords/commands.
   ============================================================ */
.terminal{
  background:#f0ead8;border:1px solid #d8d0b8;border-radius:6px;
  overflow:hidden;
  box-shadow:0 1px 4px rgba(0,0,0,.06);
  margin-top:4px;
}
.terminal .term-bar{
  background:#e3dcc4;padding:3px 8px;
  display:flex;align-items:center;gap:5px;
  border-bottom:1px solid #d8d0b8;
}
.terminal .term-dot{width:7px;height:7px;border-radius:50%;}
.terminal .dot-red{background:#dc2626;}
.terminal .dot-amber{background:#d4a017;}
.terminal .dot-green{background:#1B5E3F;}
.terminal .term-title{
  margin-left:auto;color:#6b7280;
  font-size:9.5px;font-family:"JetBrains Mono","Fira Code",monospace;
}
.terminal .term-body{
  padding:7px 10px;
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:10.5px;line-height:1.5;
  color:#1c1c1c;
  white-space:pre;
  overflow-x:auto;
}
.terminal .term-body .prompt{color:#1B5E3F;font-weight:700;}
.terminal .term-body .comment{color:#6b7280;font-style:italic;}
.terminal .term-body .cmd{color:#15264d;font-weight:600;}
.terminal .term-body .str{color:#dc2626;font-weight:600;}
.terminal .term-body .out{color:#3a3f47;}
.terminal .term-body .kw{color:#15264d;font-weight:700;}
.terminal .term-body .var{color:#e65100;}

/* ============================================================
   TEXT, LISTS, CODE
   ============================================================ */
.card p{font-size:11px;color:var(--ink-2);line-height:1.45;margin-bottom:3px;}
.card p:last-child{margin-bottom:0;}
.card code, code.inline{
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:10px;
  background:#efe9dd;padding:1px 4px;border-radius:3px;
  color:var(--navy);
}
.bullets{
  list-style:none;padding:0;margin:4px 0 0 0;
  font-size:10.5px;color:var(--ink-2);line-height:1.5;
}
.bullets li{
  padding-left:14px;position:relative;margin-bottom:2px;
}
.bullets li::before{
  content:"•";position:absolute;left:0;color:var(--green);font-weight:700;
}
.bullets.tick li::before{content:"✓";color:#1B5E3F;font-weight:800;}
.bullets.warn li::before{content:"!";color:#d4a017;font-weight:800;}
.bullets.cross li::before{content:"✕";color:#dc2626;font-weight:800;}

/* ============================================================
   TABLES
   ============================================================ */
.tbl{width:100%;border-collapse:collapse;font-size:10.5px;}
.tbl th{
  background:var(--green);color:#fff;
  padding:4px 7px;text-align:left;
  font-weight:700;font-size:9.5px;letter-spacing:.3px;text-transform:uppercase;
}
.tbl td{
  padding:4px 7px;
  border-bottom:1px solid #e0d8c8;
  color:var(--ink-2);
  vertical-align:top;
}
.tbl td code{
  font-family:"JetBrains Mono",monospace;font-size:9.5px;
  background:#efe9dd;padding:1px 4px;border-radius:3px;
  color:var(--navy);
}
.tbl tr:last-child td{border-bottom:none;}

/* ============================================================
   CALLOUT
   ============================================================ */
.callout{
  display:flex;gap:8px;align-items:flex-start;
  border-radius:8px;padding:7px 10px;
  font-size:10.5px;line-height:1.45;
  margin-top:5px;
}
.callout.warn{background:#fff4e0;border-left:3px solid #ef6c00;color:var(--ink);}
.callout.tip{background:#e8f5ee;border-left:3px solid #1B5E3F;color:var(--ink);}
.callout.danger{background:#ffe5e5;border-left:3px solid #dc2626;color:var(--ink);}
.callout .ico{flex-shrink:0;width:20px;height:20px;margin-top:1px;}
.callout .ico svg{width:20px;height:20px;display:block;}
.callout strong{display:block;font-size:11px;color:var(--ink);margin-bottom:1px;}

/* ============================================================
   PILL ROW (icon + heading + sub-text)
   ============================================================ */
.pill-row{
  display:grid;grid-template-columns:repeat(3,1fr);gap:8px;
}
.pill{
  background:var(--paper-2);border:1px solid rgba(0,0,0,.06);
  border-radius:6px;padding:7px 8px;
  display:flex;gap:8px;align-items:flex-start;
}
.pill .ico{flex-shrink:0;width:28px;height:28px;}
.pill .ico svg{width:28px;height:28px;display:block;}
.pill h4{font-size:10.5px;color:var(--navy);font-weight:800;text-transform:uppercase;letter-spacing:.3px;margin-bottom:2px;}
.pill p{font-size:9.5px;color:var(--ink-2);line-height:1.4;margin:0;}
.pill code{font-family:"JetBrains Mono",monospace;font-size:9.5px;background:#efe9dd;padding:1px 4px;border-radius:3px;color:var(--navy);}

/* ============================================================
   FEATURE COL (mini centered column inside card)
   ============================================================ */
.feature-col{
  background:var(--paper-2);border-radius:6px;padding:7px 6px;
  text-align:center;
}
.feature-col .ico{margin:0 auto 4px;width:28px;height:28px;}
.feature-col .ico svg{width:28px;height:28px;display:block;}
.feature-col h4{font-size:10px;color:var(--navy);font-weight:800;text-transform:uppercase;letter-spacing:.3px;margin-bottom:2px;}
.feature-col p{font-size:9.5px;color:var(--ink-2);line-height:1.4;margin:0;}

/* ============================================================
   TAKEAWAY (footer banner)
   ============================================================ */
.takeaway{
  display:flex;align-items:stretch;justify-content:space-between;
  gap:10px;
  background:var(--green);color:#fff;
  border-radius:8px;padding:8px 12px;
  margin-top:8px;
}
.takeaway .kt{
  display:flex;align-items:center;gap:8px;
  flex:1;
}
.takeaway .kt .ico{width:26px;height:26px;flex-shrink:0;}
.takeaway .kt .ico svg{width:26px;height:26px;display:block;}
.takeaway .kt .label{display:block;font-size:9px;letter-spacing:.8px;color:rgba(255,255,255,.75);font-weight:600;text-transform:uppercase;}
.takeaway .kt .text{display:block;font-size:11px;color:#fff;font-weight:800;line-height:1.25;}
.takeaway .divider{
  width:1px;background:rgba(255,255,255,.25);margin:2px 0;
}

/* ============================================================
   QUICK REFERENCE TABLE (for Section 10 page 15)
   ============================================================ */
.qref{display:grid;grid-template-columns:1fr 1fr;gap:3px 10px;}
.qref .row{
  display:flex;align-items:center;gap:6px;
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:10px;color:var(--ink);
}
.qref .row .badge{
  flex-shrink:0;width:18px;height:18px;border-radius:50%;
  background:var(--green);color:#fff;
  display:flex;align-items:center;justify-content:center;
  font-size:9px;font-weight:800;
}
.qref .row code{
  font-family:"JetBrains Mono",monospace;font-size:10px;
  background:#efe9dd;padding:1px 4px;border-radius:3px;
  color:var(--navy);
}

/* ============================================================
   NUMBER BADGE
   ============================================================ */
.nbadge{
  flex-shrink:0;width:22px;height:22px;border-radius:50%;
  display:inline-flex;align-items:center;justify-content:center;
  font-family:"JetBrains Mono",monospace;font-size:10px;font-weight:800;
  color:#fff;
}
.nbadge.green{background:#1B5E3F;}
.nbadge.red{background:#dc2626;}
.nbadge.blue{background:#2563eb;}
.nbadge.gold{background:#d4a017;}
.nbadge.purple{background:#7c3aed;}
.nbadge.navy{background:#15264d;}
.nbadge.teal{background:#0d7377;}

/* ============================================================
   NUMBERED STEP ROW (for left column of page 13 etc.)
   ============================================================ */
.cmd-row{
  display:flex;align-items:flex-start;gap:8px;
  background:#fff;
  border-radius:6px;padding:6px 8px;
  border-left:3px solid var(--green);
  box-shadow:0 1px 4px rgba(0,0,0,.04);
}
.cmd-row .num{
  flex-shrink:0;width:22px;height:22px;border-radius:50%;
  background:var(--green);color:#fff;
  display:flex;align-items:center;justify-content:center;
  font-family:"JetBrains Mono",monospace;font-size:10px;font-weight:800;
}
.cmd-row .ico{flex-shrink:0;width:22px;height:22px;}
.cmd-row .ico svg{width:22px;height:22px;display:block;}
.cmd-row .text{flex:1;min-width:0;}
.cmd-row .text h4{
  font-size:11px;font-weight:800;color:var(--green);
  text-transform:uppercase;letter-spacing:.3px;margin-bottom:2px;
}
.cmd-row .text p{
  font-size:10.5px;color:var(--ink-2);line-height:1.4;margin:0;
}
.cmd-row .text code.inline{
  font-family:"JetBrains Mono",monospace;font-size:10px;
  background:#efe9dd;padding:1px 4px;border-radius:3px;color:var(--navy);
}

/* ============================================================
   SIDEBAR CARD (for right column of 2-col split)
   ============================================================ */
.sidebar-card{
  background:#fff;
  border-radius:8px;
  overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
  border:1px solid rgba(0,0,0,.05);
  display:flex;flex-direction:column;
}
.sidebar-card .head{
  background:var(--green);color:#fff;
  padding:6px 10px;
  font-size:11px;font-weight:800;letter-spacing:.4px;text-transform:uppercase;
  display:flex;align-items:center;gap:8px;
}
.sidebar-card .head .ico{flex-shrink:0;display:inline-flex;width:22px;height:22px;
  background:rgba(255,255,255,.15);border-radius:5px;
  align-items:center;justify-content:center;}
.sidebar-card .head .ico svg{width:18px;height:18px;display:block;}
.sidebar-card .body-pad{padding:8px 10px;flex:1;}
.sidebar-card.head-green  .head,
.sidebar-card.head-blue   .head,
.sidebar-card.head-purple .head,
.sidebar-card.head-red    .head,
.sidebar-card.head-gold   .head,
.sidebar-card.head-teal   .head,
.sidebar-card.head-navy   .head,
.sidebar-card.head-orange .head{ background:#1B5E3F; }
.sidebar-card .example-row{
  padding:5px 0;
  border-bottom:1px dashed rgba(22,38,77,.10);
}
.sidebar-card .example-row:last-child{border-bottom:none;}
.sidebar-card .example-row .label{
  font-size:9.5px;color:var(--ink-2);font-weight:700;
  text-transform:uppercase;letter-spacing:.3px;margin-bottom:2px;
}
.sidebar-card .example-row .desc{
  font-size:10px;color:var(--ink-2);line-height:1.4;margin-top:3px;
}

/* ============================================================
   2-COL SPLIT (page 13)
   ============================================================ */
.split-2col{
  display:grid;
  grid-template-columns:1fr 1.1fr;
  gap:10px;
  margin-bottom:8px;
}
.split-2col .left-stack,
.split-2col .right-stack{
  display:flex;flex-direction:column;gap:7px;
}

/* ============================================================
   BOTTOM ROW (page 13 best practices full-width)
   ============================================================ */
.bottom-bar{
  background:var(--navy);color:#fff;
  border-radius:8px;padding:8px 12px;
  margin-top:4px;
}
.bottom-bar .head{
  font-size:11px;font-weight:800;letter-spacing:.5px;
  text-transform:uppercase;margin-bottom:5px;
  display:flex;align-items:center;gap:8px;
}
.bottom-bar .head svg{width:18px;height:18px;display:block;}
.bottom-bar .bp-grid{
  display:grid;grid-template-columns:repeat(5,1fr);gap:8px;
}
.bottom-bar .bp-item{
  font-size:10px;color:#e6edf3;line-height:1.4;
  padding:3px 0;
  display:flex;align-items:flex-start;gap:6px;
}
.bottom-bar .bp-item::before{
  content:"✓";color:#7ee787;font-weight:800;flex-shrink:0;
}

/* ============================================================
   FOOTER KEY TAKEAWAY (page 15) — green box, matches original
   ============================================================ */
.key-takeaway{
  display:flex;align-items:center;gap:10px;
  background:var(--green);
  color:#fff;
  border-radius:8px;padding:8px 14px;
  margin-top:6px;
}
.key-takeaway .ico{flex-shrink:0;width:30px;height:30px;
  background:rgba(255,255,255,.18);border-radius:6px;
  display:flex;align-items:center;justify-content:center;}
.key-takeaway .ico svg{width:24px;height:24px;display:block;}
.key-takeaway .label{
  font-size:9.5px;letter-spacing:.8px;color:rgba(255,255,255,.75);font-weight:700;text-transform:uppercase;
}
.key-takeaway .text{
  font-size:11.5px;color:#fff;font-weight:800;line-height:1.3;
}

/* ============================================================
   MOBILE: collapse grids
   ============================================================ */
@media (max-width: 900px){
  .grid-3,.grid-5,.pill-row,.qref,.split-2col,.bottom-bar .bp-grid{grid-template-columns:1fr;}
  .grid-2{grid-template-columns:1fr;}
  .takeaway{flex-direction:column;}
  .takeaway .divider{display:none;}
}
"""


# ============================================================
# HTML SNIPPET HELPERS
# ============================================================
def terminal(body_html: str, title: str = "bash") -> str:
    return (
        '<div class="terminal">'
        '<div class="term-bar">'
        '<span class="term-dot dot-red"></span>'
        '<span class="term-dot dot-amber"></span>'
        '<span class="term-dot dot-green"></span>'
        f'<span class="term-title">{title}</span>'
        '</div>'
        f'<div class="term-body">{body_html}</div>'
        '</div>'
    )


def card(num: str, head_icon: str, heading: str, body_html: str,
         variant: str = "green") -> str:
    """Build a .card with header (number + icon + heading) and body."""
    return (
        f'<div class="card head-{variant}">'
        '<div class="head">'
        f'<span class="num">{num}</span>'
        f'<span class="ico">{icon(head_icon, 16)}</span>'
        f'<span>{heading}</span>'
        '</div>'
        f'<div class="body-pad">{body_html}</div>'
        '</div>'
    )


def sidebar_card(head_icon: str, heading: str, body_html: str,
                 variant: str = "navy") -> str:
    """Build a sidebar card (for right column of split layouts)."""
    return (
        f'<div class="sidebar-card head-{variant}">'
        '<div class="head">'
        f'<span class="ico">{icon(head_icon, 16)}</span>'
        f'<span>{heading}</span>'
        '</div>'
        f'<div class="body-pad">{body_html}</div>'
        '</div>'
    )


def callout(kind: str, ico_name: str, title: str, text_html: str) -> str:
    return (
        f'<div class="callout {kind}">'
        f'<span class="ico">{icon(ico_name, 20)}</span>'
        f'<div><strong>{title}</strong>{text_html}</div>'
        '</div>'
    )


def brand_bar(page_num: int) -> str:
    return (
        '<div class="brand-bar">'
        f'<div class="crumb">{icon("book", 16)} Shell Scripting for DevOps</div>'
        f'<div class="badge">Page {page_num} of 20</div>'
        '</div>'
    )


def page_title(num: str, title: str, left_icon: str, right_icon: str) -> str:
    return (
        '<div class="page-title">'
        f'<span class="ico">{icon(left_icon, 42)}</span>'
        f'<h1><span class="num">{num}.</span>{title}</h1>'
        f'<span class="ico">{icon(right_icon, 42)}</span>'
        '</div>'
    )


def takeaway(items: list[tuple[str, str, str]]) -> str:
    """items: list of (icon_name, label, text)."""
    inner = []
    for ico, label, text in items:
        inner.append(
            f'<div class="kt"><span class="ico">{icon(ico, 26)}</span>'
            f'<div><span class="label">{label}</span>'
            f'<span class="text">{text}</span></div></div>'
        )
    sep = '<div class="divider"></div>'
    return f'<div class="takeaway">{sep.join(inner)}</div>'


def write_page(page_html_inner: str, page_num: int, title: str,
               page_id: str) -> Path:
    """Wrap content with polotno_template.page_wrapper and write file.

    Args:
      page_html_inner: content HTML (brand bar + title + body)
      page_num: page number (for filename)
      title: HTML <title>
      page_id: unique ID like 'p11' to avoid SVG gradient collisions
    """
    wrapped = page_wrapper(page_html_inner, paper_height=PAPER_H,
                           page_id=page_id)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{CONTENT_CSS}
</style>
</head>
<body class="multi-page">

{wrapped}

</body>
</html>
"""
    out_path = OUTPUT_DIR / f"recreated-page-{page_num:02d}.html"
    out_path.write_text(html_doc, encoding="utf-8")
    return out_path


# ============================================================
# PAGE 11 — FUNCTIONS AND REUSABLE SCRIPTS
# Layout: 2-column grid (8 cards in 4×2 rows) + 3-pillar takeaway
# ============================================================
def build_page_11() -> str:
    # Card 1: Creating Functions
    c1 = card("1", "code", "CREATING FUNCTIONS",
        '<p>Define a function using a name and <code>()</code> block.</p>'
        + terminal(
            '<span class="cmd">greet</span>() {{\n'
            '  <span class="cmd">echo</span> <span class="str">"Hello, DevOps Engineer!"</span>\n'
            '}}',
            'functions.sh'
        ),
        variant="green")

    # Card 2: Calling Functions
    c2 = card("2", "play", "CALLING FUNCTIONS",
        '<p>Call the function by its name.</p>'
        + terminal(
            '<span class="prompt">$</span> <span class="cmd">greet</span>\n'
            '<span class="out">Hello, DevOps Engineer!</span>',
            'call.sh'
        ),
        variant="blue")

    # Card 3: Function Arguments
    c3 = card("3", "user", "FUNCTION ARGUMENTS",
        '<p>Pass values to functions.</p>'
        + terminal(
            '<span class="cmd">greet_user</span>() {{\n'
            '  <span class="cmd">echo</span> <span class="str">"Hello, $1!"</span>\n'
            '}}\n'
            '<span class="cmd">greet_user</span> <span class="str">"Ann"</span>\n'
            '<span class="out">Hello, Ann!</span>',
            'args.sh'
        ),
        variant="purple")

    # Card 4: Local Variables
    c4 = card("4", "lock", "LOCAL VARIABLES",
        '<p>Keep variables private to the function.</p>'
        + terminal(
            '<span class="cmd">calculate</span>() {{\n'
            '  <span class="kw">local</span> num=10\n'
            '  <span class="cmd">echo</span> <span class="str">"Inside: $num"</span>\n'
            '}}\n'
            '<span class="cmd">calculate</span>\n'
            '<span class="cmd">echo</span> <span class="str">"Outside: $num"</span>\n'
            '<span class="out">Inside: 10\nOutside:</span>',
            'local.sh'
        ),
        variant="gold")

    # Card 5: Return Status
    c5 = card("5", "refresh", "RETURN STATUS",
        '<p>Functions return an exit status.</p>'
        + terminal(
            '<span class="cmd">check_disk</span>() {{\n'
            '  <span class="kw">if</span> [ $1 -gt 80 ]; <span class="kw">then</span>\n'
            '    <span class="kw">return</span> 1\n'
            '  <span class="kw">else</span>\n'
            '    <span class="kw">return</span> 0\n'
            '  <span class="kw">fi</span>\n'
            '}}\n'
            '<span class="cmd">check_disk</span> 90\n'
            '<span class="cmd">echo</span> <span class="str">"Status: $?"</span>\n'
            '<span class="out">Status: 1</span>',
            'return.sh'
        ),
        variant="teal")

    # Card 6: Break Large Scripts into Functions
    c6 = card("6", "scissors", "BREAK LARGE SCRIPTS",
        '<p>Make scripts smaller, cleaner, and easier to read.</p>'
        '<ul class="bullets tick">'
        '<li><code>check_system()</code></li>'
        '<li><code>backup_files()</code></li>'
        '<li><code>deploy_app()</code></li>'
        '<li><code>send_alert()</code></li>'
        '<li><code>cleanup()</code></li>'
        '<li><code>print_summary()</code></li>'
        '</ul>',
        variant="navy")

    # Card 7: Reusable Automation Patterns
    c7 = card("7", "gear", "REUSABLE AUTOMATION PATTERNS",
        '<ul class="bullets">'
        '<li>Health checks</li>'
        '<li>Log rotations</li>'
        '<li>Backups</li>'
        '<li>User management</li>'
        '<li>Deployments</li>'
        '<li>System cleanups</li>'
        '</ul>',
        variant="green")

    # Card 8: Keep Scripts Maintainable
    c8 = card("8", "check-square", "KEEP SCRIPTS MAINTAINABLE",
        '<ul class="bullets tick">'
        '<li>Use meaningful function names.</li>'
        '<li>Keep functions small and focused.</li>'
        '<li>Add comments to explain purpose.</li>'
        '<li>Test each function before using it.</li>'
        '<li>Reuse functions across scripts.</li>'
        '</ul>',
        variant="blue")

    body = (
        '<div class="body">'
        # Row 1
        f'<div class="grid-2">{c1}{c2}</div>'
        # Row 2
        f'<div class="grid-2" style="margin-top:10px;">{c3}{c4}</div>'
        # Row 3
        f'<div class="grid-2" style="margin-top:10px;">{c5}{c6}</div>'
        # Row 4
        f'<div class="grid-2" style="margin-top:10px;">{c7}{c8}</div>'
        '</div>'
        # Takeaway
        + takeaway([
            ("lightbulb", "Key Takeaway", "Functions make scripts powerful, reusable, and easy to maintain."),
            ("gear", "Build Once", "Use Many Times"),
            ("code", "Write Smarter", "Automate Better"),
        ])
    )

    content = (
        brand_bar(11)
        + page_title("10", "FUNCTIONS AND REUSABLE SCRIPTS", "terminal", "gear")
        + '<div class="page-subtitle">Write once. Use many times. Stay organized.</div>'
        + body
    )
    return content


# ============================================================
# PAGE 12 — WORKING WITH FILES AND DIRECTORIES
# Layout: 2-column grid (8 cards in 4×2 rows) + 3-pillar takeaway
# ============================================================
def build_page_12() -> str:
    # Card 1: Checking Whether Files Exist
    c1 = card("1", "check-circle", "CHECKING WHETHER FILES EXIST",
        '<p>Use <code>-f</code> for files, <code>-d</code> for directories.</p>'
        + terminal(
            '<span class="kw">if</span> [ -f file.txt ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"File exists"</span>\n'
            '<span class="kw">fi</span>\n'
            '<span class="kw">if</span> [ -d mydir ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"Directory exists"</span>\n'
            '<span class="kw">fi</span>',
            'check.sh'
        ),
        variant="green")

    # Card 2: Creating Directories Safely
    c2 = card("2", "folder", "CREATING DIRECTORIES SAFELY",
        '<p>Create only if it does not exist.</p>'
        + terminal(
            '<span class="cmd">mkdir</span> -p /home/user/data/logs\n'
            '<span class="comment"># -p creates parent dirs if needed</span>',
            'mkdir.sh'
        ),
        variant="blue")

    # Card 3: Copying and Moving Files
    c3 = card("3", "copy", "COPYING AND MOVING FILES",
        '<p>Copy files or directories.</p>'
        + terminal(
            '<span class="cmd">cp</span> file.txt /backup/\n'
            '<span class="cmd">cp</span> -r mydir /backup/',
            'cp.sh'
        )
        + '<p style="margin-top:5px;">Move or rename files.</p>'
        + terminal(
            '<span class="cmd">mv</span> old.txt new.txt\n'
            '<span class="cmd">mv</span> file.txt /archive/',
            'mv.sh'
        ),
        variant="purple")

    # Card 4: Searching for Files
    c4 = card("4", "search", "SEARCHING FOR FILES",
        '<p>Find files by name.</p>'
        + terminal(
            '<span class="cmd">find</span> /home/user -name <span class="str">"*.log"</span>',
            'find-name.sh'
        )
        + '<p style="margin-top:5px;">Search by type.</p>'
        + terminal(
            '<span class="cmd">find</span> /var/log -type f -name <span class="str">"*.log"</span>',
            'find-type.sh'
        ),
        variant="gold")

    # Card 5: File Permissions
    c5 = card("5", "lock", "FILE PERMISSIONS",
        '<p>View permissions.</p>'
        + terminal(
            '<span class="cmd">ls</span> -l file.txt',
            'ls-l.sh'
        )
        + '<p style="margin-top:5px;">Change permissions.</p>'
        + terminal(
            '<span class="cmd">chmod</span> 644 file.txt\n'
            '<span class="cmd">chmod</span> +x script.sh',
            'chmod.sh'
        ),
        variant="teal")

    # Card 6: Disk Usage Checks
    c6 = card("6", "chart", "DISK USAGE CHECKS",
        '<p>Check disk usage.</p>'
        + terminal(
            '<span class="cmd">df</span> -h',
            'df.sh'
        )
        + '<p style="margin-top:5px;">Check folder size.</p>'
        + terminal(
            '<span class="cmd">du</span> -sh /home/user/data',
            'du.sh'
        ),
        variant="navy")

    # Card 7: Cleaning Temporary Files
    c7 = card("7", "scissors", "CLEANING TEMPORARY FILES",
        '<p>Remove files older than 7 days.</p>'
        + terminal(
            '<span class="cmd">find</span> /tmp -type f -mtime +7 -delete',
            'find-mtime.sh'
        )
        + '<p style="margin-top:5px;">Remove all files in a directory.</p>'
        + terminal(
            '<span class="cmd">rm</span> -rf /tmp/myapp/*',
            'rm.sh'
        ),
        variant="red")

    # Card 8: Building a Simple Backup Script
    c8 = card("8", "cloud", "BUILDING A SIMPLE BACKUP SCRIPT",
        '<p>Example: Backup a folder.</p>'
        + terminal(
            '<span class="comment">#!/bin/bash</span>\n'
            '<span class="cmd">SOURCE</span>=<span class="str">"/home/user/data"</span>\n'
            '<span class="cmd">DEST</span>=<span class="str">"/backup"</span>\n'
            '<span class="cmd">DATE</span>=$(<span class="cmd">date</span> +%F)\n'
            '<span class="cmd">tar</span> -czf <span class="str">"$DEST/backup-$DATE.tar.gz"</span> <span class="str">"$SOURCE"</span>\n'
            '<span class="cmd">echo</span> <span class="str">"Backup completed: backup-$DATE.tar.gz"</span>',
            'backup.sh'
        ),
        variant="green")

    body = (
        '<div class="body">'
        f'<div class="grid-2">{c1}{c2}</div>'
        f'<div class="grid-2" style="margin-top:10px;">{c3}{c4}</div>'
        f'<div class="grid-2" style="margin-top:10px;">{c5}{c6}</div>'
        f'<div class="grid-2" style="margin-top:10px;">{c7}{c8}</div>'
        '</div>'
        + takeaway([
            ("lightbulb", "Key Takeaway", "Good file management keeps your systems clean, safe, and reliable."),
            ("shield", "Protect", "Your Data"),
            ("clock", "Automate", "Daily Tasks"),
        ])
    )

    content = (
        brand_bar(12)
        + page_title("11", "WORKING WITH FILES AND DIRECTORIES", "folder", "file")
        + '<div class="page-subtitle">Organize. Protect. Automate.</div>'
        + body
    )
    return content


# ============================================================
# PAGE 13 — TEXT PROCESSING FOR DEVOPS
# Layout: 2-col split (left=8 cmd cards, right=3 examples, bottom=best practices)
# ============================================================
def build_page_13() -> str:
    # LEFT: 8 command cards in 2-col sub-grid
    cmd_cards = [
        card("1", "search", "GREP – SEARCH PATTERNS",
            '<p>Search for a pattern in files or output.</p>'
            + terminal('<span class="cmd">grep</span> <span class="str">"ERROR"</span> app.log'),
            variant="green"),
        card("2", "scissors", "CUT – EXTRACT COLUMNS",
            '<p>Extract parts of each line.</p>'
            + terminal('<span class="cmd">cut</span> -d<span class="str">\',\'</span> -f1 users.csv'),
            variant="blue"),
        card("3", "list", "SORT – SORT LINES",
            '<p>Sort lines alphabetically or numerically.</p>'
            + terminal('<span class="cmd">sort</span> names.txt'),
            variant="purple"),
        card("4", "copy", "UNIQ – REMOVE DUPLICATES",
            '<p>Remove or count duplicate lines.</p>'
            + terminal('<span class="cmd">sort</span> names.txt <span class="kw">|</span> <span class="cmd">uniq</span> -c'),
            variant="gold"),
        card("5", "list", "WC – COUNT LINES/WORDS",
            '<p>Count lines, words, and characters.</p>'
            + terminal('<span class="cmd">wc</span> -l file.txt'),
            variant="teal"),
        card("6", "filter", "AWK – PATTERN SCAN",
            '<p>Extract and manipulate data.</p>'
            + terminal('<span class="cmd">awk</span> <span class="str">\'{print $1, $3}\'</span> data.txt'),
            variant="navy"),
        card("7", "pencil", "SED – STREAM EDITOR",
            '<p>Find and replace text.</p>'
            + terminal('<span class="cmd">sed</span> <span class="str">\'s/old/new/g\'</span> file.txt'),
            variant="red"),
        card("8", "branch", "PIPES (|) – CONNECT",
            '<p>Send output of one command to another.</p>'
            + terminal('<span class="cmd">cat</span> app.log <span class="kw">|</span> <span class="cmd">grep</span> ERROR <span class="kw">|</span> <span class="cmd">wc</span> -l'),
            variant="green"),
    ]
    # Lay out 8 cards in a 2-col grid (4 rows × 2 cols)
    left_inner = '<div class="grid-2">' + ''.join(cmd_cards) + '</div>'

    # RIGHT: 3 example cards (sections 9, 10, 11)
    right_ex1 = sidebar_card("chart", "9. EXTRACTING USEFUL INFO",
        '<p>Turn raw output into useful data.</p>'
        '<div class="example-row">'
        '<div class="label">List top 5 largest files</div>'
        + terminal('<span class="cmd">du</span> -h <span class="kw">|</span> <span class="cmd">sort</span> -h <span class="kw">|</span> <span class="cmd">tail</span> -n 5')
        + '</div>'
        '<div class="example-row">'
        '<div class="label">Count unique IP addresses</div>'
        + terminal('<span class="cmd">cut</span> -d<span class="str">\' \'</span> -f1 access.log <span class="kw">|</span> <span class="cmd">sort</span> <span class="kw">|</span> <span class="cmd">uniq</span> -c <span class="kw">|</span> <span class="cmd">sort</span> -nr')
        + '</div>'
        '<div class="example-row">'
        '<div class="label">Running processes summary</div>'
        + terminal('<span class="cmd">ps</span> aux <span class="kw">|</span> <span class="cmd">awk</span> <span class="str">\'{print $1}\'</span> <span class="kw">|</span> <span class="cmd">sort</span> <span class="kw">|</span> <span class="cmd">uniq</span> -c <span class="kw">|</span> <span class="cmd">sort</span> -nr <span class="kw">|</span> <span class="cmd">head</span>')
        + '</div>',
        variant="navy")

    right_ex2 = sidebar_card("search", "10. SEARCHING APP LOGS",
        '<p>Find errors, warnings, and events fast.</p>'
        '<div class="example-row">'
        '<div class="label">Find all ERROR lines</div>'
        + terminal('<span class="cmd">grep</span> <span class="str">"ERROR"</span> /var/log/app.log')
        + '</div>'
        '<div class="example-row">'
        '<div class="label">Find errors with line numbers</div>'
        + terminal('<span class="cmd">grep</span> -n <span class="str">"ERROR"</span> /var/log/app.log')
        + '</div>'
        '<div class="example-row">'
        '<div class="label">Count warnings</div>'
        + terminal('<span class="cmd">grep</span> -c <span class="str">"WARNING"</span> /var/log/app.log')
        + '</div>',
        variant="blue")

    right_ex3 = sidebar_card("check-circle", "11. COMMON COMBINATIONS",
        '<div class="example-row">'
        + terminal('<span class="cmd">grep</span> <span class="str">"ERROR"</span> app.log <span class="kw">|</span> <span class="cmd">wc</span> -l')
        + '<div class="desc">Count errors in log</div></div>'
        '<div class="example-row">'
        + terminal('<span class="cmd">cat</span> file.txt <span class="kw">|</span> <span class="cmd">sort</span> <span class="kw">|</span> <span class="cmd">uniq</span>')
        + '<div class="desc">Unique sorted lines</div></div>'
        '<div class="example-row">'
        + terminal('<span class="cmd">ps</span> aux <span class="kw">|</span> <span class="cmd">grep</span> nginx')
        + '<div class="desc">Find nginx processes</div></div>'
        '<div class="example-row">'
        + terminal('<span class="cmd">grep</span> -i <span class="str">"failed"</span> *.log <span class="kw">|</span> <span class="cmd">sort</span> <span class="kw">|</span> <span class="cmd">uniq</span> -c')
        + '<div class="desc">Case-insensitive search in all logs</div></div>',
        variant="green")

    right_inner = (
        '<div class="right-stack">'
        f'{right_ex1}{right_ex2}{right_ex3}'
        '</div>'
    )

    # BOTTOM: Best Practices (section 12) full-width
    bottom_bar = (
        '<div class="bottom-bar">'
        '<div class="head">' + icon("award", 18) + ' 12. BEST PRACTICES</div>'
        '<div class="bp-grid">'
        '<div class="bp-item">Use the right tool for the job.</div>'
        '<div class="bp-item">Filter early, filter often.</div>'
        '<div class="bp-item">Combine commands with pipes.</div>'
        '<div class="bp-item">Always verify your output.</div>'
        '<div class="bp-item">Automate log analysis tasks.</div>'
        '</div>'
        '</div>'
    )

    body = (
        '<div class="body">'
        '<div class="split-2col">'
        f'<div class="left-stack">{left_inner}</div>'
        f'{right_inner}'
        '</div>'
        f'{bottom_bar}'
        '</div>'
    )

    content = (
        brand_bar(13)
        + page_title("12", "TEXT PROCESSING FOR DEVOPS", "terminal", "filter")
        + '<div class="page-subtitle">Extract. Filter. Analyze. Automate.</div>'
        + body
    )
    return content


# ============================================================
# PAGE 14 — REDIRECTION, PIPES, AND LOGS
# Layout: 3-col grid (11 cards in 3×3 + 2 + best practices)
# ============================================================
def build_page_14() -> str:
    # Row 1: Sections 1-3 (3 cards)
    c1 = card("1", "download", "STANDARD INPUT (STDIN)",
        '<p>Input from keyboard or file.</p>'
        + terminal(
            '<span class="cmd">command</span> &lt; file.txt\n'
            '<span class="cmd">sort</span> &lt; names.txt',
            'stdin.sh'
        ),
        variant="green")
    c2 = card("2", "monitor", "STANDARD OUTPUT (STDOUT)",
        '<p>Normal command output.</p>'
        + terminal(
            '<span class="cmd">ls</span> -l\n'
            '<span class="cmd">echo</span> <span class="str">"Hello"</span>',
            'stdout.sh'
        ),
        variant="blue")
    c3 = card("3", "warning", "STANDARD ERROR (STDERR)",
        '<p>Error messages and warnings.</p>'
        + terminal(
            '<span class="cmd">ls</span> no_file\n'
            '<span class="cmd">cat</span> no_file.txt',
            'stderr.sh'
        ),
        variant="red")

    # Row 2: Sections 4-5 (2 cards in 3-col grid using col-span trick)
    # We'll lay 3 cards per row; place 4&5 in their own row of 2 wider cards
    c4 = card("4", "file", "OUTPUT REDIRECTION",
        '<p>Overwrite output to a file.</p>'
        + terminal('<span class="cmd">command</span> &gt; file.log')
        + '<div class="callout tip" style="margin-top:5px;padding:4px 8px;">'
        + '<span class="ico">' + icon("warning", 16) + '</span>'
        + '<div>OVERWRITE FILE</div></div>',
        variant="gold")
    c5 = card("5", "file", "APPEND REDIRECTION",
        '<p>Append output to a file.</p>'
        + terminal('<span class="cmd">command</span> &gt;&gt; file.log')
        + '<div class="callout tip" style="margin-top:5px;padding:4px 8px;">'
        + '<span class="ico">' + icon("refresh", 16) + '</span>'
        + '<div>APPEND TO FILE</div></div>',
        variant="teal")
    c6 = card("6", "warning", "ERROR REDIRECTION",
        '<p>Redirect errors to a file.</p>'
        + terminal('<span class="cmd">command</span> 2&gt; error.log')
        + '<div class="callout danger" style="margin-top:5px;padding:4px 8px;">'
        + '<span class="ico">' + icon("bug", 16) + '</span>'
        + '<div>ERRORS ONLY</div></div>',
        variant="red")

    # Row 3: Sections 7-8 (2 cards) — keep 3-col with c7, c8, leave gap for c9
    c7 = card("7", "copy", "COMBINE STDOUT & STDERR",
        '<p>Send both output and errors to same file.</p>'
        + terminal('<span class="cmd">command</span> &gt; output.log 2&gt;&amp;1')
        + '<div class="callout tip" style="margin-top:5px;padding:4px 8px;">'
        + '<span class="ico">' + icon("copy", 16) + '</span>'
        + '<div>OUTPUT + ERRORS TOGETHER</div></div>',
        variant="navy")
    c8 = card("8", "filter", "PIPES (|)",
        '<p>Send output of one command as input to another.</p>'
        + terminal('<span class="cmd">ps</span> aux <span class="kw">|</span> <span class="cmd">grep</span> nginx <span class="kw">|</span> <span class="cmd">wc</span> -l')
        + '<div class="callout tip" style="margin-top:5px;padding:4px 8px;">'
        + '<span class="ico">' + icon("branch", 16) + '</span>'
        + '<div>FILTER AND PROCESS DATA</div></div>',
        variant="purple")

    # Sections 9 & 10 — larger cards in 2-col
    c9 = card("9", "file", "SEND OUTPUT TO LOG FILES",
        '<p>Log everything for monitoring and audits.</p>'
        + terminal(
            '<span class="comment">#!/bin/bash</span>\n'
            '<span class="cmd">echo</span> <span class="str">"Starting script..."</span> &gt; script.log\n'
            '<span class="cmd">ls</span> -l /var/log &gt;&gt; script.log\n'
            '<span class="cmd">df</span> -h &gt;&gt; script.log\n'
            '<span class="cmd">echo</span> <span class="str">"Script completed."</span> &gt;&gt; script.log',
            'log-all.sh'
        )
        + '<div class="callout tip" style="margin-top:5px;padding:4px 8px;">'
        + '<span class="ico">' + icon("clipboard", 16) + '</span>'
        + '<div>LOG FILE</div></div>',
        variant="green")
    c10 = card("10", "file", "CAPTURING ERRORS SEPARATELY",
        '<p>Keep success and errors in different files.</p>'
        + terminal(
            '<span class="comment">#!/bin/bash</span>\n'
            '<span class="cmd">command</span> &gt; success.log 2&gt; error.log\n'
            '<span class="cmd">echo</span> <span class="str">"Done"</span> &gt;&gt; success.log',
            'split-logs.sh'
        )
        + '<div style="display:flex;gap:6px;margin-top:5px;">'
        + '<div class="callout tip" style="flex:1;padding:4px 6px;">'
        + '<span class="ico">' + icon("check-circle", 16) + '</span>'
        + '<div>SUCCESS.LOG</div></div>'
        + '<div class="callout danger" style="flex:1;padding:4px 6px;">'
        + '<span class="ico">' + icon("warning", 16) + '</span>'
        + '<div>ERROR.LOG</div></div>'
        + '</div>',
        variant="red")

    # Section 11: Common Examples — checklist style (matches original)
    c11_body = (
        '<ul class="bullets tick" style="font-size:10.5px;line-height:1.6;">'
        '<li><code>ls -l &gt; files.txt</code> — Save output to file (overwrite)</li>'
        '<li><code>ls -l &gt;&gt; files.txt</code> — Append output to file</li>'
        '<li><code>command 2&gt; error.log</code> — Save errors to error.log</li>'
        '<li><code>command &gt; all.log 2&gt;&amp;1</code> — Output + errors to all.log</li>'
        '<li><code>command | grep "pattern"</code> — Filter output using grep</li>'
        '<li><code>cat access.log | grep 404 | wc -l</code> — Count 404 errors</li>'
        '</ul>'
    )
    c11 = card("11", "list", "COMMON EXAMPLES", c11_body, variant="navy")

    # Best Practices — full-width 5-col
    bp_features = (
        '<div class="grid-5">'
        f'<div class="feature-col"><div class="ico">{icon("file", 28)}</div>'
        '<h4>Log outputs</h4><p>Capture important output for audits.</p></div>'
        f'<div class="feature-col"><div class="ico">{icon("scissors", 28)}</div>'
        '<h4>Separate errors</h4><p>Keep stderr apart from stdout.</p></div>'
        f'<div class="feature-col"><div class="ico">{icon("refresh", 28)}</div>'
        '<h4>Use append</h4><p><code>&gt;&gt;</code> for long-running logs.</p></div>'
        f'<div class="feature-col"><div class="ico">{icon("filter", 28)}</div>'
        '<h4>Use pipes</h4><p>Analyze data on the fly.</p></div>'
        f'<div class="feature-col"><div class="ico">{icon("check-circle", 28)}</div>'
        '<h4>Check logs</h4><p>Always verify and rotate them.</p></div>'
        '</div>'
    )
    bp_card = card("BP", "award", "BEST PRACTICES", bp_features, variant="green")

    body = (
        '<div class="body">'
        # Row 1: 3 cards
        f'<div class="grid-3">{c1}{c2}{c3}</div>'
        # Row 2: 3 cards
        f'<div class="grid-3" style="margin-top:10px;">{c4}{c5}{c6}</div>'
        # Row 3: 3 cards (with c7, c8, gap-to-c9 placeholder using empty div)
        f'<div class="grid-3" style="margin-top:10px;">{c7}{c8}{c9}</div>'
        # Row 4: 2 cards (c10 + c11)
        f'<div class="grid-2" style="margin-top:10px;">{c10}{c11}</div>'
        # Best practices full-width
        f'<div style="margin-top:10px;">{bp_card}</div>'
        '</div>'
    )

    content = (
        brand_bar(14)
        + page_title("13", "REDIRECTION, PIPES, AND LOGS", "terminal", "filter")
        + '<div class="page-subtitle">Control output. Capture logs. Debug smarter.</div>'
        + body
    )
    return content


# ============================================================
# PAGE 15 — PROCESSES AND SERVICES
# Layout: 3-col grid (9 cards in 3×3) + 2-col bottom (quick ref + best practices)
#         + key takeaway footer
# ============================================================
def build_page_15() -> str:
    # Card 1: ps
    c1 = card("1", "monitor", "PS – VIEW PROCESSES",
        '<p>Show running processes.</p>'
        + terminal(
            '<span class="cmd">ps</span> aux\n'
            '<span class="cmd">ps</span> -ef',
            'ps.sh'
        )
        + '<p style="margin-top:4px;">Useful columns:</p>'
        '<ul class="bullets" style="font-size:9.5px;">'
        '<li><code>PID</code> – Process ID</li>'
        '<li><code>USER</code> – Owner</li>'
        '<li><code>%CPU</code>, <code>%MEM</code> – Usage</li>'
        '<li><code>COMMAND</code> – Process name</li>'
        '</ul>',
        variant="green")

    # Card 2: pgrep
    c2 = card("2", "search", "PGREP – FIND PROCESSES",
        '<p>Find process IDs by name.</p>'
        + terminal(
            '<span class="cmd">pgrep</span> nginx\n'
            '<span class="cmd">pgrep</span> -f myapp',
            'pgrep.sh'
        )
        + '<p style="margin-top:4px;font-size:10px;">Used for scripting and automation.</p>',
        variant="blue")

    # Card 3: kill
    c3 = card("3", "stop", "KILL – STOP PROCESSES",
        '<p>Stop processes using PID.</p>'
        + terminal(
            '<span class="cmd">kill</span> 1234\n'
            '<span class="cmd">kill</span> -9 1234',
            'kill.sh'
        )
        + '<ul class="bullets" style="font-size:9.5px;margin-top:3px;">'
        '<li><code>kill</code> – graceful (SIGTERM)</li>'
        '<li><code>kill -9</code> – force (SIGKILL)</li>'
        '</ul>'
        + '<div class="callout warn" style="margin-top:4px;padding:4px 7px;">'
        + '<span class="ico">' + icon("warning", 16) + '</span>'
        + '<div>Use <code>kill -9</code> only when needed.</div></div>',
        variant="red")

    # Card 4: systemctl
    c4 = card("4", "gear", "SYSTEMCTL – MANAGE SERVICES",
        '<p>Control system services (Linux).</p>'
        + terminal(
            '<span class="cmd">systemctl</span> start nginx\n'
            '<span class="cmd">systemctl</span> stop nginx\n'
            '<span class="cmd">systemctl</span> restart nginx\n'
            '<span class="cmd">systemctl</span> enable nginx',
            'systemctl.sh'
        )
        + '<p style="margin-top:4px;font-size:10px;">Works with systemd services.</p>',
        variant="gold")

    # Card 5: check if running
    c5 = card("5", "check-circle", "CHECK IF PROCESS RUNNING",
        '<p>Check if a process is running.</p>'
        + terminal(
            '<span class="cmd">pgrep</span> nginx &gt;/dev/null\n'
            '<span class="kw">if</span> [ $? -eq 0 ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"Running"</span>\n'
            '<span class="kw">else</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"Not running"</span>\n'
            '<span class="kw">fi</span>',
            'check-proc.sh'
        )
        + '<p style="margin-top:4px;font-size:10px;">Exit code 0 = running</p>',
        variant="teal")

    # Card 6: check service status
    c6 = card("6", "clipboard", "CHECK SERVICE STATUS",
        '<p>Check status of a service.</p>'
        + terminal('<span class="cmd">systemctl</span> status nginx', 'status.sh')
        + '<p style="margin-top:4px;">Common states:</p>'
        '<ul class="bullets" style="font-size:9.5px;">'
        '<li><span class="nbadge green" style="width:14px;height:14px;font-size:8px;">●</span> active (running)</li>'
        '<li><span class="nbadge red" style="width:14px;height:14px;font-size:8px;">●</span> inactive (dead)</li>'
        '<li><span class="nbadge red" style="width:14px;height:14px;font-size:8px;">!</span> failed</li>'
        '</ul>',
        variant="purple")

    # Card 7: restart failed services
    c7 = card("7", "refresh", "RESTART FAILED SERVICES",
        '<p>Restart a service.</p>'
        + terminal(
            '<span class="cmd">systemctl</span> restart nginx\n'
            '<span class="cmd">systemctl</span> enable nginx\n'
            '<span class="cmd">systemctl</span> status nginx',
            'restart.sh'
        )
        + '<p style="margin-top:4px;font-size:10px;">Auto-restart on boot + check again.</p>',
        variant="green")

    # Card 8: process information
    c8 = card("8", "branch", "PROCESS INFORMATION",
        '<p>Get more details about a process.</p>'
        + terminal(
            '<span class="cmd">ps</span> -p 1234 -o pid,user,cmd,%mem,%cpu\n'
            '<span class="cmd">ps</span> -o pid,ppid,cmd -p 1234',
            'ps-info.sh'
        )
        + '<p style="margin-top:4px;font-size:10px;">Show parent process with <code>ppid</code>.</p>',
        variant="navy")

    # Card 9: basic service health check script
    c9 = card("9", "shield", "BASIC SERVICE HEALTH CHECK",
        '<p>Example: Check and restart service.</p>'
        + terminal(
            '<span class="comment">#!/bin/bash</span>\n'
            '<span class="cmd">SERVICE</span>=nginx\n'
            '<span class="cmd">pgrep</span> $SERVICE &gt;/dev/null\n'
            '<span class="kw">if</span> [ $? -eq 0 ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"$SERVICE is running"</span>\n'
            '<span class="kw">else</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"$SERVICE is down. Restarting..."</span>\n'
            '  <span class="cmd">systemctl</span> restart $SERVICE\n'
            '<span class="kw">fi</span>',
            'health.sh'
        ),
        variant="blue")

    # Section 10: Quick Reference (2-col bottom-left)
    c10 = card("10", "list", "QUICK REFERENCE",
        '<div class="qref">'
        '<div class="row"><span class="badge">1</span><code>ps aux</code></div>'
        '<div class="row"><span class="badge">2</span><code>pgrep &lt;name&gt;</code></div>'
        '<div class="row"><span class="badge">3</span><code>kill &lt;PID&gt;</code></div>'
        '<div class="row"><span class="badge">4</span><code>kill -9 &lt;PID&gt;</code></div>'
        '<div class="row"><span class="badge">5</span><code>systemctl status &lt;svc&gt;</code></div>'
        '<div class="row"><span class="badge">6</span><code>systemctl restart &lt;svc&gt;</code></div>'
        '<div class="row"><span class="badge">7</span><code>systemctl enable &lt;svc&gt;</code></div>'
        '<div class="row"><span class="badge">8</span><code>journalctl -u &lt;svc&gt;</code></div>'
        '</div>'
        '<ul class="bullets" style="font-size:9.5px;margin-top:5px;">'
        '<li>List, find, stop, manage, and view logs</li>'
        '</ul>',
        variant="navy")

    # Best Practices (2-col bottom-right)
    c11 = card("BP", "award", "BEST PRACTICES",
        '<ul class="bullets tick" style="font-size:10px;">'
        '<li>Always check before you kill.</li>'
        '<li>Use meaningful process names.</li>'
        '<li>Monitor important services.</li>'
        '<li>Automate health checks.</li>'
        '<li>Log issues for faster troubleshooting.</li>'
        '<li>Restart only when necessary.</li>'
        '<li>Keep scripts simple and readable.</li>'
        '</ul>',
        variant="green")

    # Key takeaway footer
    takeaway_banner = (
        '<div class="key-takeaway">'
        f'<span class="ico">{icon("lightbulb", 28)}</span>'
        '<div>'
        '<div class="label">Key Takeaway</div>'
        '<div class="text">Know your processes. Control your services. Keep your systems reliable.</div>'
        '</div>'
        '</div>'
    )

    body = (
        '<div class="body">'
        # 3×3 grid of cards 1-9
        f'<div class="grid-3">{c1}{c2}{c3}</div>'
        f'<div class="grid-3" style="margin-top:10px;">{c4}{c5}{c6}</div>'
        f'<div class="grid-3" style="margin-top:10px;">{c7}{c8}{c9}</div>'
        # 2-col bottom: quick ref + best practices
        f'<div class="grid-2" style="margin-top:10px;">{c10}{c11}</div>'
        '</div>'
        + takeaway_banner
    )

    content = (
        brand_bar(15)
        + page_title("14", "PROCESSES AND SERVICES", "monitor", "gear")
        + '<div class="page-subtitle">Monitor. Control. Keep everything running.</div>'
        + body
    )
    return content


# ============================================================
# MAIN — build all 5 pages
# ============================================================
def main() -> None:
    print(f"Polotno default paper height: {PAPER_H}")
    builders = [
        (11, "p11", "10. Functions and Reusable Scripts", build_page_11),
        (12, "p12", "11. Working with Files and Directories", build_page_12),
        (13, "p13", "12. Text Processing for DevOps", build_page_13),
        (14, "p14", "13. Redirection, Pipes, and Logs", build_page_14),
        (15, "p15", "14. Processes and Services", build_page_15),
    ]
    paths = []
    for page_num, pid, title, builder in builders:
        content_html = builder()
        path = write_page(content_html, page_num, title, pid)
        size = path.stat().st_size
        print(f"  wrote {path.name} ({size:,} bytes)")
        paths.append(path)

    print(f"\n✓ Wrote {len(paths)} pages to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
