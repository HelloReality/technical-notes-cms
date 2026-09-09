#!/usr/bin/env python3
"""
Rebuild carousel pages 11-15 (file page-11.webp .. page-15.webp) as
self-contained notebook-style HTML files.

Requirements (per task shell-scripting-rebuild-v2-batch3):
1. Use COLORFUL FILLED icons from `scripts/shell_scripting_icons.py`
   (NOT the old outline-only icons from build_shell_scripting_template).
2. Use canonical notebook CSS at:
   public/uploads/notebook-template/notebook-template.css
3. Body must have class="multi-page".
4. NO VERIQTA branding, NO social footer.
5. Each page uses .page-wrapper > .page > .content structure.

Page layouts (per task spec):
- Page 11 (10. FUNCTIONS AND REUSABLE SCRIPTS)      : 2-column grid (8 cards)
- Page 12 (11. WORKING WITH FILES AND DIRECTORIES)   : 2-column grid (8 cards)
- Page 13 (12. TEXT PROCESSING FOR DEVOPS)           : 2-col (left commands 1-8, right sections 9-11)
- Page 14 (13. REDIRECTION, PIPES, AND LOGS)         : 3-column grid
- Page 15 (14. PROCESSES AND SERVICES)               : 3-column grid
"""

import os
import sys

# Make sure we can import the colorful icon library
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from shell_scripting_icons import ICONS  # 53 multi-color filled SVGs

# ============================================================
# PATHS
# ============================================================

CANONICAL_CSS_PATH = "/home/z/my-project/public/uploads/notebook-template/notebook-template.css"
OUT_DIR = "/home/z/my-project/downloads/instagram-DcaW1UljsVk"


def read_canonical_css() -> str:
    with open(CANONICAL_CSS_PATH, "r", encoding="utf-8") as f:
        return f.read()


# ============================================================
# ICON HELPER — colorful filled icons
# ============================================================

def ic(name: str, size: int = 40) -> str:
    """Return inline colorful SVG for a named icon at given pixel size."""
    svg = ICONS.get(name, ICONS.get("terminal", ""))
    return svg.replace(
        'viewBox="0 0 48 48"',
        f'viewBox="0 0 48 48" width="{size}" height="{size}"',
    )


# ============================================================
# EXTRA PAGE-SPECIFIC CSS (added on top of canonical)
# ============================================================

EXTRA_CSS = r"""
/* ============================================================
   PAGE-SPECIFIC STYLES — content area, cards, terminals, etc.
   These layer on top of the canonical notebook-template.css
   ============================================================ */

/* Content wrapper — sits above the graph-paper grid */
.content{position:relative;z-index:2;}

/* Color tokens used by page-specific styles */
:root{
  --green:#1B5E3F;
  --green-2:#164a32;
  --green-light:#e8f5ee;
  --green-soft:#cdf3da;
  --ink:#1c1c1c;
  --ink-2:#3a3f47;
  --ink-3:#6b7280;
  --terminal-bg:#0d1117;
  --terminal-fg:#e6edf3;
  --terminal-green:#7ee787;
  --terminal-amber:#f2cc60;
  --terminal-blue:#79c0ff;
  --terminal-dim:#8b949e;
}

/* Page header (title + subtitle + icons) */
.page-header{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:14px;gap:18px;
}
.page-header .h-ico{flex-shrink:0;width:54px;height:54px;display:flex;align-items:center;justify-content:center;}
.page-header .h-ico svg{width:54px;height:54px;}
.page-header .h-title-wrap{flex:1;text-align:center;}
.page-title{
  font-size:32px;font-weight:800;color:var(--green);
  text-transform:uppercase;letter-spacing:-.4px;line-height:1.1;
  margin-bottom:4px;
}
.page-title .num{color:var(--green-2);}
.page-subtitle{
  font-size:13px;font-weight:700;color:var(--ink-2);
  text-transform:uppercase;letter-spacing:1.2px;
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
   SECTION-CARD GRID (2-column or 3-column)
   ============================================================ */
.section-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:12px;
  margin-bottom:14px;
}
.section-grid.three{grid-template-columns:1fr 1fr 1fr;}
.section-grid .full{grid-column:1 / -1;}
.section-grid .span-2{grid-column:span 2;}

/* Section card */
.sec-card{
  background:#fff;
  border-radius:10px;
  overflow:hidden;
  border:1px solid rgba(0,0,0,.06);
  box-shadow:0 2px 8px rgba(0,0,0,.05);
  display:flex;flex-direction:column;
}
.sec-head{
  background:var(--green);
  color:#fff;
  padding:7px 12px;
  display:flex;align-items:center;gap:8px;
}
.sec-head .num{
  width:22px;height:22px;border-radius:50%;
  background:#fff;color:var(--green);
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:800;font-family:monospace;
  flex-shrink:0;
}
.sec-head .title{
  flex:1;
  font-size:11px;font-weight:700;letter-spacing:.4px;
  text-transform:uppercase;
}
.sec-head .ico{
  width:22px;height:22px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
}
.sec-head .ico svg{width:22px;height:22px;}
.sec-body{
  padding:10px 12px;
  font-size:11.5px;color:var(--ink-2);line-height:1.5;
  display:flex;flex-direction:column;gap:6px;
  flex:1;
}
.sec-body p{margin:0;}
.sec-body .note{
  font-size:10.5px;color:var(--ink-3);
  font-style:italic;
}
.sec-body .body-row{
  display:flex;align-items:center;gap:10px;
}
.sec-body .body-row .text{flex:1;min-width:0;}
.sec-body .body-row .icon{
  flex-shrink:0;width:40px;height:40px;
  border-radius:8px;
  background:var(--green-light);
  display:flex;align-items:center;justify-content:center;
}
.sec-body .body-row .icon svg{width:32px;height:32px;}

/* Inline code */
code.inline{
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:11px;
  background:#e8e4d4;padding:1px 5px;border-radius:3px;
  color:var(--green-2);
}

/* Mini terminal used inside cards */
.mini-term{
  background:var(--terminal-bg);border-radius:6px;overflow:hidden;
  box-shadow:0 2px 6px rgba(0,0,0,.18);
}
.mini-term .bar{
  background:#1c2230;padding:4px 8px;
  display:flex;align-items:center;gap:5px;
}
.mini-term .bar i{
  width:7px;height:7px;border-radius:50%;display:inline-block;
}
.mini-term .bar i.r{background:#ff5f56;}
.mini-term .bar i.y{background:#ffbd2e;}
.mini-term .bar i.g{background:#27c93f;}
.mini-term .bar .t{
  margin-left:auto;color:var(--terminal-dim);
  font-size:9px;font-family:monospace;
}
.mini-term pre{
  margin:0;
  padding:8px 10px;
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:10.5px;line-height:1.55;
  color:var(--terminal-fg);
  white-space:pre;overflow-x:auto;
}
.mini-term pre .prompt{color:var(--terminal-green);}
.mini-term pre .comment{color:var(--terminal-dim);}
.mini-term pre .cmd{color:var(--terminal-blue);}
.mini-term pre .str{color:var(--terminal-amber);}
.mini-term pre .out{color:var(--terminal-fg);}
.mini-term pre .err{color:#ff7b72;}
.mini-term pre .arrow{color:var(--terminal-green);font-weight:700;}
.mini-term pre .kw{color:#ff7b72;}

/* Output line under code blocks */
.out-line{
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:10.5px;color:var(--green-2);
  background:var(--green-light);
  padding:4px 8px;border-radius:5px;
  border-left:3px solid var(--green);
}

/* Side label / pill */
.side-pill{
  align-self:flex-start;
  background:#fce9b6;color:#e65100;
  padding:3px 9px;border-radius:999px;
  font-size:9.5px;font-weight:800;letter-spacing:.5px;
  text-transform:uppercase;
}
.side-pill.green{background:var(--green-light);color:var(--green);}
.side-pill.blue{background:#cfe0ff;color:#2563eb;}
.side-pill.red{background:#ffd4d4;color:#dc2626;}

/* Function tag pills */
.tag-row{
  display:flex;flex-wrap:wrap;gap:5px;
}
.tag-row .tag{
  background:var(--green-light);color:var(--green-2);
  font-family:"JetBrains Mono",monospace;
  font-size:10px;font-weight:600;
  padding:3px 8px;border-radius:5px;
  border:1px solid var(--green-soft);
}

/* Workflow chain */
.workflow{
  display:flex;align-items:center;gap:6px;flex-wrap:wrap;
  font-size:9.5px;font-weight:700;color:var(--ink-2);
  text-transform:uppercase;letter-spacing:.3px;
}
.workflow .step{
  display:flex;align-items:center;gap:4px;
  background:var(--green-light);
  padding:4px 8px;border-radius:6px;
  color:var(--green);
}
.workflow .step svg{width:14px;height:14px;}
.workflow .arr{color:var(--green);font-weight:800;}

/* Checklist list */
.check-list{list-style:none;padding:0;margin:0;}
.check-list li{
  position:relative;
  padding-left:20px;
  font-size:11px;line-height:1.55;color:var(--ink-2);
  margin-bottom:4px;
}
.check-list li .ci{
  position:absolute;left:0;top:1px;
  width:14px;height:14px;
}
.check-list li .ci svg{width:14px;height:14px;display:block;}

/* Key takeaway bar at bottom */
.takeaway-bar{
  display:grid;
  grid-template-columns:1.4fr 1fr 1fr;
  gap:0;
  border:2px solid var(--green);
  border-radius:12px;
  overflow:hidden;
  margin-top:8px;margin-bottom:14px;
  background:#fff;
}
.takeaway-bar.four{grid-template-columns:1.4fr 1fr 1fr 1fr;}
.takeaway-bar.five{grid-template-columns:1.4fr 1fr 1fr 1fr 1fr;}
.takeaway-bar .item{
  padding:10px 14px;
  display:flex;align-items:center;gap:8px;
  border-right:1px solid var(--green-soft);
  font-size:11px;line-height:1.35;color:var(--ink-2);
}
.takeaway-bar .item:last-child{border-right:none;}
.takeaway-bar .item .ico{
  flex-shrink:0;width:34px;height:34px;
  background:var(--green-light);border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  color:var(--green);
}
.takeaway-bar .item .ico svg{width:24px;height:24px;}
.takeaway-bar .item .lbl{
  font-size:10px;font-weight:800;color:var(--green);
  text-transform:uppercase;letter-spacing:.5px;
  margin-bottom:2px;display:block;
}
.takeaway-bar .item .txt{
  font-size:11px;color:var(--ink-2);line-height:1.4;
}
.takeaway-bar .item.first{
  background:var(--green-light);
}
.takeaway-bar .item.first .lbl{color:var(--green-2);}
.takeaway-bar .item.first .txt{color:var(--ink);}

/* Pillars row (3 columns) */
.pillars{
  display:grid;grid-template-columns:1fr 1fr 1fr;
  gap:10px;margin-bottom:14px;
}
.pillar{
  background:#fff;
  border:2px solid var(--green);
  border-radius:10px;
  padding:10px 12px;
  display:flex;align-items:center;gap:8px;
  font-size:11px;font-weight:700;
  color:var(--green);
  text-transform:uppercase;letter-spacing:.4px;
}
.pillar .ico{
  width:34px;height:34px;flex-shrink:0;
  background:var(--green);color:#fff;
  border-radius:8px;
  display:flex;align-items:center;justify-content:center;
}
.pillar .ico svg{width:22px;height:22px;}

/* Page body title (section heading inside body) */
.body-section-h{
  font-size:13px;font-weight:800;color:var(--green);
  text-transform:uppercase;letter-spacing:.5px;
  margin:14px 0 8px;
  padding-bottom:4px;
  border-bottom:2px solid var(--green);
}

/* Two-column body (left commands, right sections) */
.two-col-body{
  display:grid;
  grid-template-columns:1.15fr 1fr;
  gap:14px;
  margin-bottom:14px;
}
.two-col-body .col{
  display:flex;flex-direction:column;gap:10px;
}

/* Compact command row card */
.cmd-card{
  background:#fff;
  border-radius:10px;
  overflow:hidden;
  border:1px solid rgba(0,0,0,.06);
  box-shadow:0 2px 6px rgba(0,0,0,.04);
  display:flex;flex-direction:column;
}
.cmd-card .cmd-head{
  background:var(--green);
  color:#fff;
  padding:6px 10px;
  display:flex;align-items:center;gap:8px;
}
.cmd-card .cmd-head .n{
  width:20px;height:20px;border-radius:50%;
  background:#fff;color:var(--green);
  display:flex;align-items:center;justify-content:center;
  font-size:10px;font-weight:800;font-family:monospace;
  flex-shrink:0;
}
.cmd-card .cmd-head .name{
  flex:1;font-family:"JetBrains Mono",monospace;
  font-size:12px;font-weight:700;letter-spacing:.3px;
}
.cmd-card .cmd-head .ico{
  flex-shrink:0;width:22px;height:22px;
  display:flex;align-items:center;justify-content:center;
}
.cmd-card .cmd-head .ico svg{width:22px;height:22px;}
.cmd-card .cmd-body{
  padding:8px 10px;
  font-size:11px;color:var(--ink-2);line-height:1.5;
  display:flex;flex-direction:column;gap:5px;
}
.cmd-card .cmd-body p{margin:0;}

/* Bottom split row: wide left + narrow right */
.bottom-split{
  display:grid;
  grid-template-columns:2fr 1fr;
  gap:12px;
  margin-bottom:14px;
}

/* Quick-ref command list (2-col internal) */
.cmd-quickref{
  background:#fff;
  border-radius:10px;
  border:1px solid rgba(0,0,0,.06);
  overflow:hidden;
  box-shadow:0 2px 6px rgba(0,0,0,.04);
}
.cmd-quickref .head{
  background:var(--green);color:#fff;
  padding:7px 12px;
  display:flex;align-items:center;gap:8px;
}
.cmd-quickref .head .num{
  width:22px;height:22px;border-radius:50%;
  background:#fff;color:var(--green);
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:800;font-family:monospace;
  flex-shrink:0;
}
.cmd-quickref .head .title{
  flex:1;
  font-size:11px;font-weight:700;letter-spacing:.4px;
  text-transform:uppercase;
}
.cmd-quickref .head .ico{flex-shrink:0;width:30px;height:30px;display:flex;align-items:center;justify-content:center;}
.cmd-quickref .head .ico svg{width:28px;height:28px;}
.cmd-quickref .body{
  padding:10px 14px;
  display:grid;grid-template-columns:1fr 1fr;
  gap:6px 14px;
}
.cmd-quickref .body .row{
  display:flex;align-items:flex-start;gap:8px;
  font-size:11px;line-height:1.4;
  padding:3px 0;
  border-bottom:1px dashed rgba(22,38,77,.08);
}
.cmd-quickref .body .row:last-child{border-bottom:none;}
.cmd-quickref .body .row .ci{
  flex-shrink:0;width:14px;height:14px;margin-top:1px;
}
.cmd-quickref .body .row .ci svg{width:14px;height:14px;display:block;}
.cmd-quickref .body .row code{
  font-family:"JetBrains Mono",monospace;font-size:11px;
  background:#e8e4d4;padding:1px 5px;border-radius:3px;
  color:var(--green-2);font-weight:600;flex-shrink:0;
}
.cmd-quickref .body .row .desc{
  flex:1;color:var(--ink-2);
}

/* Best-practices sidebar */
.best-practices{
  background:#fff;
  border-radius:10px;
  border:2px solid var(--green);
  overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
  display:flex;flex-direction:column;
}
.best-practices .head{
  background:var(--green);color:#fff;
  padding:8px 12px;
  display:flex;align-items:center;gap:8px;
}
.best-practices .head .ico{flex-shrink:0;width:24px;height:24px;display:flex;align-items:center;justify-content:center;}
.best-practices .head .ico svg{width:22px;height:22px;}
.best-practices .head .title{
  flex:1;
  font-size:11px;font-weight:800;letter-spacing:.5px;
  text-transform:uppercase;
}
.best-practices .body{
  padding:10px 12px;
  display:flex;flex-direction:column;gap:5px;
}
.best-practices .body .row{
  display:flex;align-items:flex-start;gap:8px;
  font-size:11px;line-height:1.45;color:var(--ink-2);
}
.best-practices .body .row .ci{flex-shrink:0;width:14px;height:14px;margin-top:1px;}
.best-practices .body .row .ci svg{width:14px;height:14px;display:block;}
.best-practices .body .row .txt{flex:1;}

/* Hero header (page 14 — pipe flow diagram) */
.pipe-flow{
  display:flex;align-items:center;justify-content:center;
  gap:8px;flex-wrap:wrap;
  background:#fff;
  border-radius:10px;
  border:1px solid rgba(0,0,0,.06);
  padding:10px 14px;
  margin-bottom:14px;
  box-shadow:0 2px 6px rgba(0,0,0,.04);
}
.pipe-flow .node{
  display:flex;flex-direction:column;align-items:center;gap:4px;
  padding:6px 10px;border-radius:8px;
  background:var(--green-light);
  min-width:80px;
}
.pipe-flow .node .ico{width:28px;height:28px;}
.pipe-flow .node .ico svg{width:28px;height:28px;}
.pipe-flow .node .lbl{
  font-size:9.5px;font-weight:700;color:var(--green);
  text-transform:uppercase;letter-spacing:.3px;
}
.pipe-flow .arrow{
  width:30px;height:24px;
  display:flex;align-items:center;justify-content:center;
}
.pipe-flow .arrow svg{width:30px;height:24px;}

/* Process flow row inside card (icon arrow icon arrow icon) */
.flow-row{
  display:flex;align-items:center;gap:6px;
  padding:6px 0;
  flex-wrap:wrap;
}
.flow-row .node{
  display:flex;align-items:center;gap:6px;
  background:var(--green-light);border-radius:6px;
  padding:4px 8px;
}
.flow-row .node .ico{width:22px;height:22px;display:flex;align-items:center;justify-content:center;}
.flow-row .node .ico svg{width:22px;height:22px;}
.flow-row .node .lbl{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.3px;}
.flow-row .arr{width:24px;height:14px;}
.flow-row .arr svg{width:24px;height:14px;}
"""


# ============================================================
# HTML HELPERS
# ============================================================

def esc(s: str) -> str:
    """Escape HTML special chars in code samples."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mini_term(code: str, title: str = "bash") -> str:
    """Build a small terminal window.

    `code` is the raw shell text. We escape it and add simple syntax
    highlight spans for comments / prompts / output arrows.
    """
    e = esc(code)
    lines = e.split("\n")
    out = []
    for ln in lines:
        stripped = ln.lstrip()
        if stripped.startswith("#"):
            out.append(f'<span class="comment">{ln}</span>')
        elif stripped.startswith("$ "):
            inner = ln[2:]
            out.append(f'<span class="prompt">$</span> <span class="cmd">{inner}</span>')
        elif stripped.startswith("→ "):
            inner = ln[2:]
            out.append(f'<span class="arrow">→</span> <span class="out">{inner}</span>')
        elif stripped.startswith("OUTPUT:"):
            out.append(f'<span class="arrow">→</span> <span class="out">{ln}</span>')
        else:
            out.append(ln)
    body = "\n".join(out)
    return (
        f'<div class="mini-term">'
        f'<div class="bar"><i class="r"></i><i class="y"></i><i class="g"></i>'
        f'<span class="t">{esc(title)}</span></div>'
        f'<pre>{body}</pre></div>'
    )


def sec_card(num, title, icon_name, body_html, full=False, span2=False):
    cls = "sec-card"
    if full:
        cls += " full"
    if span2:
        cls += " span-2"
    return f'''<div class="{cls}">
  <div class="sec-head">
    <span class="num">{num}</span>
    <span class="title">{title}</span>
    <span class="ico">{ic(icon_name, 22)}</span>
  </div>
  <div class="sec-body">{body_html}</div>
</div>'''


def cmd_card(num, name, icon_name, body_html):
    """Compact card used in left column of page 13."""
    return f'''<div class="cmd-card">
  <div class="cmd-head">
    <span class="n">{num}</span>
    <span class="name">{esc(name)}</span>
    <span class="ico">{ic(icon_name, 22)}</span>
  </div>
  <div class="cmd-body">{body_html}</div>
</div>'''


def takeaway_bar(items, cols=None):
    cls = "takeaway-bar"
    if cols == 4:
        cls += " four"
    elif cols == 5:
        cls += " five"
    parts = [f'<div class="{cls}">']
    for i, (icon_name, lbl, txt) in enumerate(items):
        first_cls = " first" if i == 0 else ""
        parts.append(
            f'<div class="item{first_cls}">'
            f'<span class="ico">{ic(icon_name, 24)}</span>'
            f'<div><span class="lbl">{lbl}</span>'
            f'<span class="txt">{txt}</span></div>'
            f'</div>'
        )
    parts.append("</div>")
    return "".join(parts)


def check_list(items):
    """Build a checklist with colorful check-circle icons."""
    lis = []
    for it in items:
        lis.append(
            f'<li><span class="ci">{ic("check-circle", 14)}</span>{it}</li>'
        )
    return f'<ul class="check-list">{"".join(lis)}</ul>'


def tag_row(tags):
    spans = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)
    return f'<div class="tag-row">{spans}</div>'


# ============================================================
# PAGE-WRAPPER — canonical structure (no branding, no footer)
# ============================================================

def page_html(title_main, num, subtitle, body_html,
              left_header_icon="terminal", right_header_icon="cube") -> str:
    """Build a complete standalone HTML file.

    Uses canonical notebook CSS + extra page-specific CSS.
    Body has class="multi-page". No branding, no social footer.
    """
    canonical_css = read_canonical_css()
    full_title = f"{num}. {title_main}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{full_title} — Shell Scripting for DevOps</title>
<style>
{canonical_css}

{EXTRA_CSS}
</style>
</head>
<body class="multi-page">

<div class="page-wrapper">
  <div class="page">
    <div class="page-bend" aria-hidden="true"></div>
    <div class="page-top-edge" aria-hidden="true"></div>
    <div class="page-bottom-edge" aria-hidden="true"></div>
    <div class="spiral" aria-hidden="true"></div>
    <div class="holes" aria-hidden="true"></div>

    <div class="content">

      <!-- Page header (no brand bar, no page badge) -->
      <div class="page-header">
        <div class="h-ico">{ic(left_header_icon, 54)}</div>
        <div class="h-title-wrap">
          <h1 class="page-title"><span class="num">{num}.</span> {title_main}</h1>
          <div class="page-subtitle">{subtitle}</div>
        </div>
        <div class="h-ico">{ic(right_header_icon, 54)}</div>
      </div>

      <!-- Body -->
      {body_html}

    </div>
  </div>
</div>

</body>
</html>
'''


# ============================================================
# PAGE 11 — 10. FUNCTIONS AND REUSABLE SCRIPTS
# Layout: 2-column grid, 8 cards (2 x 4)
# Source image: page-11.webp (analysis-page-11.json)
# ============================================================

def build_page_11() -> str:
    cards = [
        sec_card(1, "CREATING FUNCTIONS", "file", (
            '<p>Define a reusable block of code.</p>'
            + mini_term(
                '# Define a function\ngreet() {\n  echo "Hello, $1"\n}',
                "func.sh"
            )
        )),
        sec_card(2, "CALLING FUNCTIONS", "bell", (
            '<p>Invoke the function by name.</p>'
            + mini_term(
                'greet "World"\n# → Hello, World',
                "call.sh"
            )
        )),
        sec_card(3, "FUNCTION ARGUMENTS", "users", (
            '<p>Pass arguments by position.</p>'
            + mini_term(
                'greet() {\n  echo "Hi, $1 from $2"\n}\ngreet "DevOps" "Texas"',
                "args.sh"
            )
        )),
        sec_card(4, "LOCAL VARIABLES", "lock", (
            '<p>Keep variables scoped to the function.</p>'
            + mini_term(
                'counter() {\n  local count=0\n  count=$((count + 1))\n  echo $count\n}',
                "local.sh"
            )
        )),
        sec_card(5, "RETURN STATUS", "refresh", (
            '<p>Use <code class="inline">return</code> for exit codes.</p>'
            + mini_term(
                'is_file() {\n  [ -f "$1" ] && return 0\n  return 1\n}',
                "return.sh"
            )
        )),
        sec_card(6, "BREAK LARGE SCRIPTS", "clipboard", (
            '<p>Split a long script into many small functions.</p>'
            + '<div class="workflow">'
            + f'<span class="step">{ic("file", 14)}<span>MAIN.SH</span></span>'
            + '<span class="arr">→</span>'
            + f'<span class="step">{ic("gear", 14)}<span>CALL FNS</span></span>'
            + '<span class="arr">→</span>'
            + f'<span class="step">{ic("check-square", 14)}<span>DONE</span></span>'
            + '<span class="arr">→</span>'
            + f'<span class="step">{ic("check-circle", 14)}<span>SUCCESS</span></span>'
            + '</div>'
        )),
        sec_card(7, "REUSABLE PATTERNS", "refresh", (
            '<p>Group common tasks into a library of functions.</p>'
            + check_list([
                "Log messages",
                "Send alerts",
                "Validate input",
                "Check disk space",
            ])
        )),
        sec_card(8, "MAINTAINABILITY", "shield", (
            '<p>Functions make scripts easier to read, test, and maintain.</p>'
            + check_list([
                "Smaller, focused blocks",
                "Clear, descriptive names",
                "Easier debugging",
                "Reusable across projects",
            ])
        )),
    ]
    grid = f'<div class="section-grid">{"".join(cards)}</div>'
    takeaway = takeaway_bar([
        ("lightbulb", "KEY TAKEAWAY",
         "Functions let you build once, use many times, and stay organized."),
        ("gear", "BUILD ONCE",
         "Reuse everywhere."),
        ("code", "WRITE SMARTER",
         "Maintain with ease."),
    ], cols=3)

    body = grid + takeaway
    return page_html(
        "FUNCTIONS AND REUSABLE SCRIPTS",
        10,
        "WRITE ONCE. USE MANY TIMES. STAY ORGANIZED.",
        body,
        left_header_icon="terminal",
        right_header_icon="cube",
    )


# ============================================================
# PAGE 12 — 11. WORKING WITH FILES AND DIRECTORIES
# Layout: 2-column grid, 8 cards (2 x 4)
# Source image: page-12.webp (analysis-page-12.json)
# ============================================================

def build_page_12() -> str:
    cards = [
        sec_card(1, "CHECKING WHETHER FILES EXIST", "check-circle", (
            '<p>Use <code class="inline">-f</code> for files, '
            '<code class="inline">-d</code> for directories.</p>'
            + mini_term(
                'if [ -f file.txt ]; then\n  echo "File exists"\nfi\n'
                'if [ -d mydir ]; then\n  echo "Directory exists"\nfi',
                "check.sh"
            )
        )),
        sec_card(2, "CREATING DIRECTORIES SAFELY", "folder", (
            '<p>Create only if it does not exist.</p>'
            + mini_term(
                'mkdir -p /home/user/data/logs',
                "mkdir.sh"
            )
            + '<p class="note"><code class="inline">-p</code> creates parent '
            'directories if needed.</p>'
        )),
        sec_card(3, "COPYING AND MOVING FILES", "copy", (
            '<p>Copy files or directories.</p>'
            + mini_term(
                'cp file.txt /backup/\ncp -r mydir /backup/',
                "copy.sh"
            )
            + '<p>Move or rename files.</p>'
            + mini_term(
                'mv old.txt new.txt\nmv file.txt /archive/',
                "move.sh"
            )
        )),
        sec_card(4, "SEARCHING FOR FILES", "search", (
            '<p>Find files by name.</p>'
            + mini_term(
                'find /home/user -name "*.log"',
                "find.sh"
            )
            + '<p>Search by type.</p>'
            + mini_term(
                'find /var/log -type f -name "*.log"',
                "find2.sh"
            )
        )),
        sec_card(5, "FILE PERMISSIONS", "lock", (
            '<p>View permissions.</p>'
            + mini_term(
                'ls -l file.txt',
                "perm.sh"
            )
            + '<p>Change permissions.</p>'
            + mini_term(
                'chmod 644 file.txt\nchmod +x script.sh',
                "chmod.sh"
            )
        )),
        sec_card(6, "DISK USAGE CHECKS", "chart", (
            '<p>Check disk usage.</p>'
            + mini_term(
                'df -h',
                "disk.sh"
            )
            + '<p>Check folder size.</p>'
            + mini_term(
                'du -sh /home/user/data',
                "size.sh"
            )
        )),
        sec_card(7, "CLEANING TEMPORARY FILES", "scissors", (
            '<p>Remove files older than 7 days.</p>'
            + mini_term(
                'find /tmp -type f -mtime +7 -delete',
                "clean.sh"
            )
            + '<p>Remove all files in a directory.</p>'
            + mini_term(
                'rm -rf /tmp/myapp/*',
                "rm.sh"
            )
        )),
        sec_card(8, "BUILDING A SIMPLE BACKUP SCRIPT", "cloud", (
            '<p>Example: backup a folder.</p>'
            + mini_term(
                '#!/bin/bash\nSOURCE="/home/user/data"\nDEST="/backup"\n'
                'DATE=$(date +%F)\ntar -czf "$DEST/backup-$DATE.tar.gz" "$SOURCE"\n'
                'echo "Backup completed: backup-$DATE.tar.gz"',
                "backup.sh"
            )
        )),
    ]
    grid = f'<div class="section-grid">{"".join(cards)}</div>'
    takeaway = takeaway_bar([
        ("lightbulb", "KEY TAKEAWAY",
         "Good file management keeps your systems clean, safe, and reliable."),
        ("shield", "PROTECT YOUR DATA",
         "Guard your files."),
        ("clock", "AUTOMATE DAILY TASKS",
         "Save time."),
        ("folder", "STAY ORGANIZED",
         "Tidy systems run smoother."),
    ], cols=4)

    body = grid + takeaway
    return page_html(
        "WORKING WITH FILES AND DIRECTORIES",
        11,
        "ORGANIZE. PROTECT. AUTOMATE.",
        body,
        left_header_icon="folder",
        right_header_icon="file",
    )


# ============================================================
# PAGE 13 — 12. TEXT PROCESSING FOR DEVOPS
# Layout: 2-column (left = commands 1-8 stack, right = sections 9-11)
# Source image: page-13.webp (analysis-page-13.json)
# ============================================================

def build_page_13() -> str:
    # Left column: 8 command cards stacked
    left_cards = [
        cmd_card(1, "grep", "search", (
            '<p>Search text using patterns.</p>'
            + mini_term('grep "ERROR" /var/log/app.log', "grep.sh")
        )),
        cmd_card(2, "cut", "scissors", (
            '<p>Extract columns from text.</p>'
            + mini_term('cut -d: -f1 /etc/passwd', "cut.sh")
        )),
        cmd_card(3, "sort", "list", (
            '<p>Sort lines of text.</p>'
            + mini_term('sort names.txt\nsort -n -k2 scores.txt', "sort.sh")
        )),
        cmd_card(4, "uniq", "copy", (
            '<p>Remove duplicate adjacent lines.</p>'
            + mini_term('sort file.txt | uniq -c', "uniq.sh")
        )),
        cmd_card(5, "wc", "list", (
            '<p>Count lines, words, bytes.</p>'
            + mini_term('wc -l access.log\nwc -w notes.txt', "wc.sh")
        )),
        cmd_card(6, "awk", "filter", (
            '<p>Pattern-action processing.</p>'
            + mini_term('awk \'{print $2}\' file.txt', "awk.sh")
        )),
        cmd_card(7, "sed", "pencil", (
            '<p>Stream editor for text transforms.</p>'
            + mini_term('sed \'s/old/new/g\' file.txt', "sed.sh")
        )),
        cmd_card(8, "pipes |", "network", (
            '<p>Chain commands together.</p>'
            + mini_term('cat log | grep ERR | wc -l', "pipe.sh")
        )),
    ]
    left_col = f'<div class="col">{"".join(left_cards)}</div>'

    # Right column: 3 section blocks (9, 10, 11)
    right_cards = [
        sec_card(9, "EXTRACTING USEFUL INFORMATION FROM LOGS", "chart", (
            '<p>Pull out the data you need from massive logs.</p>'
            + mini_term(
                'grep "ERROR" app.log | cut -d" " -f3 | sort | uniq -c | sort -nr',
                "extract.sh"
            )
            + '<p class="note">Counts each unique error and ranks them.</p>'
        )),
        sec_card(10, "SEARCHING APPLICATION LOGS", "search", (
            '<p>Find specific events by keyword or timestamp.</p>'
            + mini_term(
                'grep "2025-01-15" app.log\ngrep -i "warning" *.log',
                "search.sh"
            )
            + '<p class="note"><code class="inline">-i</code> = case-insensitive.</p>'
        )),
        sec_card(11, "COMMON COMBINATIONS", "code", (
            '<p>Combine tools for powerful one-liners.</p>'
            + check_list([
                '<code class="inline">cat log | grep ERR | wc -l</code> &mdash; count errors',
                '<code class="inline">ps aux | sort -rk4 | head -10</code> &mdash; top 10 memory hogs',
                '<code class="inline">df -h | awk \'{print $5}\'</code> &mdash; list disk usage %',
                '<code class="inline">cut -d: -f1 /etc/passwd | sort</code> &mdash; sorted users',
                '<code class="inline">grep -v "#" config | sed \'/^$/d\'</code> &mdash; strip comments &amp; blanks',
                '<code class="inline">du -sh * | sort -rh</code> &mdash; biggest folders first',
            ])
        )),
    ]
    right_col = f'<div class="col">{"".join(right_cards)}</div>'

    body_grid = f'<div class="two-col-body">{left_col}{right_col}</div>'

    # Bottom: best-practices bar (5 items)
    takeaway = takeaway_bar([
        ("lightbulb", "KEY TAKEAWAY",
         "Text tools turn raw logs into actionable insight."),
        ("target", "BE SPECIFIC",
         "Filter early."),
        ("filter", "PIPELINE",
         "Combine small tools."),
        ("shield", "VALIDATE",
         "Check output sanity."),
        ("clock", "AUTOMATE",
         "Schedule reports."),
    ], cols=5)

    body = body_grid + takeaway
    return page_html(
        "TEXT PROCESSING FOR DEVOPS",
        12,
        "EXTRACT. FILTER. TRANSFORM. AUTOMATE.",
        body,
        left_header_icon="terminal",
        right_header_icon="file",
    )


# ============================================================
# PAGE 14 — 13. REDIRECTION, PIPES, AND LOGS
# Layout: 3-column grid (mix of 3-col and 2-col rows)
# Source image: page-14.webp (analysis-page-14.json)
# ============================================================

def build_page_14() -> str:
    # Row 1 — three standard streams (3 columns)
    row1 = [
        sec_card(1, "STANDARD INPUT (STDIN)", "terminal", (
            '<p>Read input from keyboard or another command.</p>'
            + '<div class="flow-row">'
            + f'<span class="node">{ic("key", 22)}<span class="lbl">KEY</span></span>'
            + f'<span class="arr">{ic("arrow", 24)}</span>'
            + f'<span class="node">{ic("terminal", 22)}<span class="lbl">CMD</span></span>'
            + '</div>'
        )),
        sec_card(2, "STANDARD OUTPUT (STDOUT)", "monitor", (
            '<p>Default output goes to the screen.</p>'
            + '<div class="flow-row">'
            + f'<span class="node">{ic("terminal", 22)}<span class="lbl">CMD</span></span>'
            + f'<span class="arr">{ic("arrow", 24)}</span>'
            + f'<span class="node">{ic("monitor", 22)}<span class="lbl">SCREEN</span></span>'
            + '</div>'
        )),
        sec_card(3, "STANDARD ERROR (STDERR)", "warning", (
            '<p>Error messages go to a separate stream.</p>'
            + '<div class="flow-row">'
            + f'<span class="node">{ic("terminal", 22)}<span class="lbl">CMD</span></span>'
            + f'<span class="arr">{ic("arrow", 24)}</span>'
            + f'<span class="node">{ic("warning", 22)}<span class="lbl">ERROR</span></span>'
            + '</div>'
        )),
    ]
    row1_html = f'<div class="section-grid three">{"".join(row1)}</div>'

    # Row 2 — basic redirection (2 columns)
    row2 = [
        sec_card(4, "OUTPUT REDIRECTION (>)", "file", (
            '<p>Overwrite a file with command output.</p>'
            + mini_term('echo "Hello" > file.txt\nls > listing.txt', "redir.sh")
            + '<p class="note">Creates or overwrites the file.</p>'
        ), span2=False),
        sec_card(5, "APPEND REDIRECTION (>>)", "file", (
            '<p>Append output to an existing file.</p>'
            + mini_term('echo "Line 2" >> file.txt\ndate >> log.txt', "append.sh")
            + '<p class="note">Adds without overwriting.</p>'
        ), span2=False),
    ]
    row2_html = f'<div class="section-grid">{"".join(row2)}</div>'

    # Row 3 — advanced redirection & pipes (3 columns)
    row3 = [
        sec_card(6, "ERROR REDIRECTION (2>)", "warning", (
            '<p>Send errors to a separate file.</p>'
            + mini_term('ls /missing 2> errors.log', "err-redir.sh")
        )),
        sec_card(7, "COMBINE STDOUT &amp; STDERR (2&gt;&amp;1)", "file", (
            '<p>Send both output and errors to one file.</p>'
            + mini_term('cmd > all.log 2>&1', "combine.sh")
        )),
        sec_card(8, "PIPES (|)", "filter", (
            '<p>Send one command\'s output to another.</p>'
            + mini_term('cat log | grep ERR | wc -l', "pipe.sh")
        )),
    ]
    row3_html = f'<div class="section-grid three">{"".join(row3)}</div>'

    # Row 4 — scripting & logging (2 columns)
    row4 = [
        sec_card(9, "SEND SCRIPT OUTPUT TO LOG FILES", "file", (
            '<p>Inside a script, redirect everything.</p>'
            + mini_term(
                '#!/bin/bash\nLOG="/var/log/myscript.log"\n'
                'echo "Starting..." > "$LOG"\napt update >> "$LOG" 2>&1\n'
                'echo "Done." >> "$LOG"',
                "script-log.sh"
            )
        ), span2=False),
        sec_card(10, "CAPTURING ERRORS SEPARATELY", "warning", (
            '<p>Split success and error streams.</p>'
            + mini_term(
                'cmd > success.log 2> error.log',
                "split-log.sh"
            )
            + '<div class="body-row" style="margin-top:4px;">'
            + '<span class="icon" style="background:#e8f5ee;">'
            + ic("file", 32) + '</span>'
            + '<div class="text"><strong>success.log</strong><br>'
            + '<span class="note">STDOUT only</span></div></div>'
            + '<div class="body-row">'
            + '<span class="icon" style="background:#ffd4d4;">'
            + ic("warning", 32) + '</span>'
            + '<div class="text"><strong>error.log</strong><br>'
            + '<span class="note">STDERR only</span></div></div>'
        ), span2=False),
    ]
    row4_html = f'<div class="section-grid">{"".join(row4)}</div>'

    # Row 5 — bottom split: common examples + best practices
    examples_card = (
        '<div class="cmd-quickref">'
        '<div class="head">'
        f'<span class="num">11</span>'
        '<span class="title">COMMON EXAMPLES</span>'
        f'<span class="ico">{ic("code", 28)}</span>'
        '</div>'
        '<div class="body">'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>cmd &gt; file</code>'
        + '<span class="desc">Overwrite file</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>cmd &gt;&gt; file</code>'
        + '<span class="desc">Append to file</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>cmd 2&gt; file</code>'
        + '<span class="desc">Errors to file</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>cmd &gt; file 2&gt;&amp;1</code>'
        + '<span class="desc">Both to file</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>cmd | less</code>'
        + '<span class="desc">Page output</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>cmd | tee file</code>'
        + '<span class="desc">Show &amp; save</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>cmd &lt; file</code>'
        + '<span class="desc">Read from file</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>cmd1 | cmd2</code>'
        + '<span class="desc">Pipe output</span></div>'
        + '</div>'
        '</div>'
    )

    best_practices = (
        '<div class="best-practices">'
        '<div class="head">'
        f'<span class="ico">{ic("award", 22)}</span>'
        '<span class="title">BEST PRACTICES</span>'
        '</div>'
        '<div class="body">'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Always log script output to a file.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Separate STDOUT and STDERR when debugging.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Use <code class="inline">&gt;&gt;</code> to append, not overwrite.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Use <code class="inline">tee</code> to see and save output.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Rotate logs to avoid disk bloat.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Validate exit codes with <code class="inline">$?</code>.</span></div>'
        + '</div>'
        '</div>'
    )

    row5_html = (
        f'<div class="bottom-split">{examples_card}{best_practices}</div>'
    )

    body = row1_html + row2_html + row3_html + row4_html + row5_html
    return page_html(
        "REDIRECTION, PIPES, AND LOGS",
        13,
        "CONTROL OUTPUT. CAPTURE LOGS. DEBUG SMARTER.",
        body,
        left_header_icon="terminal",
        right_header_icon="file",
    )


# ============================================================
# PAGE 15 — 14. PROCESSES AND SERVICES
# Layout: 3-column grid (9 cards in 3x3, plus bottom split row)
# Source image: page-15.webp (analysis-page-15.json)
# ============================================================

def build_page_15() -> str:
    # Row 1 — ps, pgrep, kill
    row1 = [
        sec_card(1, "PS &mdash; VIEW PROCESSES", "monitor", (
            '<p>List currently running processes.</p>'
            + mini_term('ps aux\nps -ef | grep nginx', "ps.sh")
        )),
        sec_card(2, "PGREP &mdash; FIND PROCESSES", "search", (
            '<p>Find a process by name.</p>'
            + mini_term('pgrep -f nginx\npgrep -u root sshd', "pgrep.sh")
        )),
        sec_card(3, "KILL &mdash; STOP PROCESSES", "stop", (
            '<p>Send signals to processes.</p>'
            + mini_term('kill 1234\nkill -9 1234  # force\npkill nginx', "kill.sh")
            + '<p class="note"><code class="inline">-9</code> = SIGKILL (last resort).</p>'
        )),
    ]
    row1_html = f'<div class="section-grid three">{"".join(row1)}</div>'

    # Row 2 — systemctl + checks
    row2 = [
        sec_card(4, "SYSTEMCTL &mdash; MANAGE SERVICES", "gear", (
            '<p>Control systemd services.</p>'
            + mini_term(
                'systemctl start nginx\nsystemctl stop nginx\n'
                'systemctl restart nginx\nsystemctl enable nginx',
                "systemctl.sh"
            )
        )),
        sec_card(5, "CHECK IF PROCESS IS RUNNING", "clipboard", (
            '<p>Verify a process is up.</p>'
            + mini_term(
                'if pgrep -x nginx > /dev/null; then\n  echo "Running"\nelse\n  echo "Stopped"\nfi',
                "check.sh"
            )
        )),
        sec_card(6, "CHECK SERVICE STATUS", "check-circle", (
            '<p>See if a service is active.</p>'
            + mini_term(
                'systemctl status nginx\nsystemctl is-active nginx',
                "status.sh"
            )
        )),
    ]
    row2_html = f'<div class="section-grid three">{"".join(row2)}</div>'

    # Row 3 — restart, info, script
    row3 = [
        sec_card(7, "RESTART FAILED SERVICES", "refresh", (
            '<p>Auto-restart crashed services.</p>'
            + mini_term(
                'systemctl reset-failed nginx\nsystemctl restart nginx',
                "restart.sh"
            )
        )),
        sec_card(8, "PROCESS INFORMATION", "network", (
            '<p>See process tree &amp; hierarchy.</p>'
            + mini_term(
                'pstree -p\nhtop\ntop',
                "info.sh"
            )
        )),
        sec_card(9, "BASIC SERVICE HEALTH CHECK SCRIPT", "terminal", (
            '<p>Auto-check &amp; restart a service.</p>'
            + mini_term(
                '#!/bin/bash\nSERVICE="nginx"\nif ! systemctl is-active --quiet $SERVICE; then\n  systemctl restart $SERVICE\n  echo "$SERVICE restarted" >> /var/log/health.log\nfi',
                "health.sh"
            )
        )),
    ]
    row3_html = f'<div class="section-grid three">{"".join(row3)}</div>'

    # Bottom split: quick reference + best practices
    quickref = (
        '<div class="cmd-quickref">'
        '<div class="head">'
        f'<span class="num">10</span>'
        '<span class="title">COMMON COMMANDS QUICK REFERENCE</span>'
        f'<span class="ico">{ic("server", 28)}</span>'
        '</div>'
        '<div class="body">'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>ps aux</code>'
        + '<span class="desc">All processes</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>top</code>'
        + '<span class="desc">Live process view</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>kill -9 PID</code>'
        + '<span class="desc">Force-kill process</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>pkill name</code>'
        + '<span class="desc">Kill by name</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>systemctl status svc</code>'
        + '<span class="desc">Service status</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>systemctl restart svc</code>'
        + '<span class="desc">Restart service</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>journalctl -u svc</code>'
        + '<span class="desc">Service logs</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<code>pgrep -f name</code>'
        + '<span class="desc">Find PID by name</span></div>'
        + '</div>'
        '</div>'
    )

    best_practices = (
        '<div class="best-practices">'
        '<div class="head">'
        f'<span class="ico">{ic("shield", 22)}</span>'
        '<span class="title">BEST PRACTICES</span>'
        '</div>'
        '<div class="body">'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Avoid <code class="inline">kill -9</code> unless needed.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Use <code class="inline">systemctl</code> for services.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Log all restarts for audits.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Monitor with <code class="inline">htop</code> or <code class="inline">top</code>.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Enable services to start on boot.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Check <code class="inline">journalctl</code> for service logs.</span></div>'
        + '<div class="row">'
        + f'<span class="ci">{ic("check-circle", 14)}</span>'
        + '<span class="txt">Automate health checks.</span></div>'
        + '</div>'
        '</div>'
    )

    bottom_html = (
        f'<div class="bottom-split">{quickref}{best_practices}</div>'
    )

    # Key takeaway bar at very bottom (4 items)
    takeaway = takeaway_bar([
        ("lightbulb", "KEY TAKEAWAY",
         "Mastering processes and services keeps systems healthy."),
        ("chart", "MONITOR PROCESSES",
         "Watch what runs."),
        ("gear", "MANAGE SERVICES",
         "Start, stop, restart."),
        ("shield", "KEEP SYSTEMS HEALTHY",
         "Auto-recover on failure."),
    ], cols=4)

    body = row1_html + row2_html + row3_html + bottom_html + takeaway
    return page_html(
        "PROCESSES AND SERVICES",
        14,
        "MONITOR. CONTROL. KEEP EVERYTHING RUNNING.",
        body,
        left_header_icon="terminal",
        right_header_icon="gear",
    )


# ============================================================
# MAIN
# ============================================================

def main():
    builders = [
        (11, build_page_11),
        (12, build_page_12),
        (13, build_page_13),
        (14, build_page_14),
        (15, build_page_15),
    ]
    for n, fn in builders:
        html = fn()
        out_path = os.path.join(OUT_DIR, f"recreated-page-{n:02d}.html")
        # Also write to the non-padded filename the task expects
        alt_path = os.path.join(OUT_DIR, f"recreated-page-{n}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        with open(alt_path, "w", encoding="utf-8") as f:
            f.write(html)
        size_kb = len(html) / 1024
        print(f"  wrote {out_path}  ({size_kb:.1f} KB)")
        print(f"  wrote {alt_path}  ({size_kb:.1f} KB)")
    print("\nDone. All 5 pages rebuilt with colorful icons + canonical CSS.")


if __name__ == "__main__":
    main()
