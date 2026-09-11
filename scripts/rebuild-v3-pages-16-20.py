#!/usr/bin/env python3
"""
Rebuild Shell Scripting Handbook carousel pages 16-20 (v3) as individual
self-contained HTML files.

Uses:
- `polotno_template.page_wrapper(content_html, paper_height, page_id)` for
  the notebook page chrome (spiral binding, holes, 3D edges, graph paper).
- `shell_scripting_icons.ICONS` (53 multi-color filled SVGs) for icons.

Per VLM verification of source webp images:
  page-16.webp → 16. ERROR HANDLING AND SAFER SCRIPTS  (3-col grid)
  page-17.webp → 15. NETWORKING WITH SHELL SCRIPTS     (2-col rows+sidebar)
  page-18.webp → 18. SCHEDULING SCRIPTS WITH CRON       (2-col rows+sidebar)
  page-19.webp → 17. DEBUGGING SHELL SCRIPTS            (2-col rows+sidebar)
  page-20.webp → 19. SHELL SCRIPTING IN DEVOPS WORKFLOWS (2-col rows+sidebar)

Output: downloads/instagram-DcaW1UljsVk/recreated-page-NN.html
"""
from __future__ import annotations
import sys
from pathlib import Path

# Make sibling scripts importable
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from polotno_template import page_wrapper, DEFAULT_PAPER_H
from shell_scripting_icons import ICONS, icon as render_icon


# ============================================================
# PATHS
# ============================================================
PROJECT_ROOT = SCRIPTS_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "downloads" / "instagram-DcaW1UljsVk"

# Default Polotno paper height (matches reference exactly)
DEFAULT_HEIGHT = 1424  # matches original image height

# Per-page paper heights — measured to fit each page's content
# (content height + ~60-80px buffer for breathing room at the bottom).
# The polotno_template.calc_hole_count() auto-adjusts hole/ring count.
PAGE_HEIGHTS = {
    16: 1424,
    17: 1424,
    18: 1424,
    19: 1424,
    20: 1424,
}


# ============================================================
# ICON HELPER
# ============================================================
def icon(name: str, size: int = 36) -> str:
    """Return inline colorful filled SVG for a named icon."""
    return render_icon(name, size)


# ============================================================
# SUPPLEMENTAL CSS — color tokens + page-specific styles
# ============================================================
SUPPLEMENTAL_CSS = """
/* ============================================================
   COLOR TOKENS
   ============================================================ */
:root{
  --paper:#f5f1e8;
  --paper-2:#efe9dd;
  --grid-line:#bcc8d6;
  --green:#1B5E3F;
  --green-2:#164a32;
  --green-light:#e8f5ee;
  --green-soft:#cdf3da;
  --navy:#15264d;
  --navy-2:#1e3160;
  --ink:#1c1c1c;
  --ink-2:#3a3f47;
  --ink-3:#6b7280;
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
  --terminal-green:#7ee787;
  --terminal-dim:#8b949e;
}

*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#cfc9bb;}
body{
  font-family:"Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
  color:var(--ink);
  display:flex;flex-direction:column;align-items:center;
  gap:24px;
  padding:24px 48px;
}
body.multi-page{flex-direction:column;gap:24px;overflow:visible;}
.page-wrapper{position:relative;overflow:visible;}
@media print{
  html,body{background:#fff;padding:0;gap:0;}
  .page-wrapper{page-break-after:always;}
  .page-wrapper:last-child{page-break-after:auto;}
}

/* content sits above graph-paper grid.
   IMPORTANT FIX: polotno_template's paper <svg> is a regular block element
   (no position:absolute), which means it occupies vertical flow space
   equal to paper_height and pushes .content down BELOW the paper (where it
   gets clipped by overflow:hidden). We force the SVG to be position:absolute
   so it overlays the paper as a background, letting .content flow naturally
   from the top of the paper (with the inline padding). */
.content{position:absolute !important;top:11px !important;left:0 !important;right:0 !important;bottom:11px !important;z-index:2;overflow:hidden;}
.page-wrapper > div:first-child > div:first-child > svg{
  position:absolute !important;
  top:0; left:0;
  width:100% !important;
  height:100% !important;
  z-index:0;
  pointer-events:none;
}

/* ============================================================
   PAGE HEADER (title + subtitle)
   ============================================================ */
.page-title{
  font-size:32px;font-weight:800;color:var(--green);
  text-transform:uppercase;letter-spacing:-.4px;line-height:1.1;
  margin-bottom:4px;
  display:flex;align-items:center;gap:12px;
}
.page-title .num{color:var(--green-2);}
.page-title .title-ico{display:inline-flex;width:42px;height:42px;flex-shrink:0;}
.page-title .title-ico svg{display:block;}
.page-subtitle{
  font-size:12.5px;font-weight:700;color:var(--ink-2);
  text-transform:uppercase;letter-spacing:1.4px;
  padding-bottom:10px;margin-bottom:14px;
  border-bottom:2px solid var(--green);
  position:relative;
}
.page-subtitle::after{
  content:"";position:absolute;left:50%;bottom:-6px;
  width:10px;height:10px;background:var(--green);
  border-radius:50%;transform:translateX(-50%);
}

/* Page badge (top-right) */
.page-badge{
  position:absolute;top:18px;right:24px;z-index:9;
  background:var(--green);color:#fff;
  padding:5px 14px;border-radius:999px;
  font-size:10.5px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;
  box-shadow:0 4px 12px rgba(27,94,63,.35);
}

/* ============================================================
   BODY LAYOUTS
   ============================================================ */
.body{
  display:grid;
  grid-template-columns:1.85fr 1fr;
  gap:16px;
  margin-bottom:14px;
}
.body.single{grid-template-columns:1fr;}
.body.three-col{grid-template-columns:1fr 1fr 1fr;}

/* ============================================================
   ROWS (left column sections)
   ============================================================ */
.rows{display:flex;flex-direction:column;gap:8px;}
.row{
  display:flex;gap:11px;align-items:flex-start;
  background:rgba(255,255,255,.55);
  border-radius:9px;padding:8px 11px;
  border-left:3px solid var(--green);
}
.row .ico{
  flex-shrink:0;width:42px;height:42px;
  border-radius:9px;
  display:flex;align-items:center;justify-content:center;
  background:var(--paper-2);
}
.row .ico svg{display:block;}
.row .text{flex:1;min-width:0;}
.row .text h3{
  font-size:12.5px;font-weight:800;color:var(--green);
  text-transform:uppercase;letter-spacing:.3px;
  margin-bottom:3px;
}
.row .text p{
  font-size:11.5px;color:var(--ink-2);line-height:1.45;
  margin-bottom:4px;
}
.row .text ul{
  list-style:none;padding:0;margin:4px 0 0 0;
  font-size:11px;color:var(--ink-2);line-height:1.5;
}
.row .text ul li{
  padding-left:16px;position:relative;margin-bottom:3px;
}
.row .text ul li::before{
  content:"";position:absolute;left:2px;top:6px;
  width:7px;height:7px;border-radius:50%;
  background:var(--green);
}
.row .text code.inline,
code.inline{
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:10.5px;
  background:#e8e4d4;padding:1px 5px;border-radius:3px;
  color:var(--navy);
}

/* ============================================================
   TERMINAL / CODE BLOCK
   ============================================================ */
.terminal{
  background:var(--term-bg);border-radius:7px;overflow:hidden;
  box-shadow:0 3px 12px rgba(0,0,0,.18);
  margin-top:6px;
}
.terminal .term-bar{
  background:#1c2230;padding:5px 11px;
  display:flex;align-items:center;gap:6px;
}
.terminal .term-dot{width:9px;height:9px;border-radius:50%;}
.terminal .dot-red{background:#ff5f56;}
.terminal .dot-amber{background:#ffbd2e;}
.terminal .dot-green{background:#27c93f;}
.terminal .term-title{
  margin-left:auto;color:#8b949e;
  font-size:9.5px;font-family:monospace;
}
.terminal .term-body{
  padding:8px 12px;
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:10.5px;line-height:1.5;
  color:var(--term-fg);
  white-space:pre-wrap;
}
.terminal .term-body .prompt{color:var(--terminal-green);}
.terminal .term-body .comment{color:var(--terminal-dim);font-style:italic;}
.terminal .term-body .cmd{color:#79c0ff;}
.terminal .term-body .str{color:#f2cc60;}
.terminal .term-body .out{color:var(--term-fg);}
.terminal .term-body .kw{color:#ff7b72;font-weight:600;}

/* ============================================================
   SIDEBAR CARDS (right column)
   ============================================================ */
.sidebar{display:flex;flex-direction:column;gap:8px;}
.card{
  background:#fff;border-radius:9px;overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
  border:1px solid rgba(0,0,0,.05);
}
.card .head{
  background:var(--green);color:#fff;
  padding:7px 12px;
  font-size:10.5px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;
  display:flex;align-items:center;gap:8px;
}
.card .head .head-ico{
  width:18px;height:18px;display:inline-flex;align-items:center;justify-content:center;
}
.card .head .head-ico svg{display:block;}
.card .body-pad{padding:10px 12px;}
.card .body-pad p{
  font-size:11px;color:var(--ink-2);line-height:1.45;
  margin-bottom:5px;
}
.card .body-pad ul{
  list-style:none;padding:0;margin:0;
  font-size:11px;color:var(--ink-2);line-height:1.5;
}
.card .body-pad ul li{
  padding-left:18px;position:relative;margin-bottom:4px;
}
.card .body-pad ul li::before{
  content:"";position:absolute;left:2px;top:6px;
  width:7px;height:7px;border-radius:50%;background:var(--green);
}

/* ============================================================
   TABLES
   ============================================================ */
.tbl{width:100%;border-collapse:collapse;font-size:10.5px;margin-top:4px;}
.tbl th{
  background:var(--green);color:#fff;
  padding:5px 8px;text-align:left;
  font-weight:700;font-size:9.5px;letter-spacing:.3px;text-transform:uppercase;
}
.tbl td{
  padding:5px 8px;
  border-bottom:1px solid #e0d8c8;
  color:var(--ink-2);
}
.tbl td code,
.tbl td .mono{
  font-family:"JetBrains Mono",monospace;font-size:9.5px;
  background:#e8e4d4;padding:1px 4px;border-radius:3px;
  color:var(--navy);
  display:inline-block;vertical-align:top;
}
.tbl tr:last-child td{border-bottom:none;}

/* ============================================================
   CALLOUTS (warn / tip / danger)
   ============================================================ */
.callout{
  display:flex;gap:9px;align-items:flex-start;
  border-radius:7px;padding:7px 11px;
  font-size:11px;line-height:1.45;
  margin-top:5px;
}
.callout.warn{
  background:#fff4e0;border-left:3px solid var(--orange);
  color:var(--ink-2);
}
.callout.tip{
  background:#e8f5ee;border-left:3px solid var(--green);
  color:var(--ink-2);
}
.callout.danger{
  background:#ffe5e5;border-left:3px solid var(--red);
  color:var(--ink-2);
}
.callout .ico{flex-shrink:0;width:18px;height:18px;margin-top:1px;display:inline-flex;}
.callout .ico svg{display:block;}

/* ============================================================
   3-COLUMN GRID CARDS (page 16 — error handling)
   ============================================================ */
.card-grid-3{
  display:grid;
  grid-template-columns:1fr 1fr 1fr;
  gap:9px;
  margin-bottom:11px;
}
.grid-card{
  background:#fff;border-radius:9px;overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
  border:1px solid rgba(0,0,0,.05);
  display:flex;flex-direction:column;
}
.grid-card .gc-head{
  padding:7px 11px;
  font-size:10.5px;font-weight:800;letter-spacing:.3px;text-transform:uppercase;
  display:flex;align-items:center;gap:7px;
  color:#fff;
}
.grid-card .gc-head .gc-ico{
  width:20px;height:20px;display:inline-flex;align-items:center;justify-content:center;
  flex-shrink:0;
}
.grid-card .gc-head .gc-ico svg{display:block;}
.grid-card .gc-body{
  padding:8px 11px;
  flex:1;display:flex;flex-direction:column;gap:5px;
}
.grid-card .gc-body p{
  font-size:10.5px;color:var(--ink-2);line-height:1.4;
}
.grid-card .gc-body ul{
  list-style:none;padding:0;margin:0;
  font-size:10px;color:var(--ink-2);line-height:1.5;
}
.grid-card .gc-body ul li{
  padding-left:14px;position:relative;margin-bottom:3px;
}
.grid-card .gc-body ul li::before{
  content:"";position:absolute;left:0;top:6px;
  width:6px;height:6px;border-radius:50%;background:var(--green);
}
.grid-card .gc-body .terminal{margin-top:4px;}
.grid-card .gc-body .terminal .term-body{font-size:10px;padding:6px 10px;}

/* color variants */
.gc-green{background:var(--green);}
.gc-blue{background:var(--blue);}
.gc-purple{background:var(--purple);}
.gc-red{background:var(--red);}
.gc-gold{background:var(--gold);}
.gc-teal{background:var(--teal);}
.gc-navy{background:var(--navy);}
.gc-orange{background:var(--orange);}

/* ============================================================
   KEY TAKEAWAY BOX
   ============================================================ */
.key-takeaway{
  display:flex;align-items:center;gap:13px;
  background:var(--green);color:#fff;
  border-radius:9px;padding:11px 18px;
  margin-top:11px;
}
.key-takeaway .kt-ico{
  flex-shrink:0;width:34px;height:34px;
  display:inline-flex;align-items:center;justify-content:center;
}
.key-takeaway .kt-ico svg{display:block;}
.key-takeaway .kt-text{
  flex:1;font-size:12px;line-height:1.5;
}
.key-takeaway .kt-text strong{
  display:block;font-size:12.5px;letter-spacing:1.4px;
  margin-bottom:2px;text-transform:uppercase;
}

/* ============================================================
   STEPS (numbered)
   ============================================================ */
.steps{display:flex;flex-direction:column;gap:5px;}
.step{
  display:flex;gap:9px;align-items:flex-start;
  font-size:11.5px;color:var(--ink-2);line-height:1.4;
}
.step .n{
  flex-shrink:0;width:20px;height:20px;border-radius:50%;
  background:var(--green);color:#fff;
  display:flex;align-items:center;justify-content:center;
  font-size:10.5px;font-weight:800;font-family:monospace;
}
.step .step-ico{
  flex-shrink:0;width:20px;height:20px;
  display:inline-flex;align-items:center;justify-content:center;
}
.step .step-ico svg{display:block;}

/* ============================================================
   COMPARE (debugging page - 2-col comparison)
   ============================================================ */
.compare{display:grid;grid-template-columns:1fr 1fr;gap:7px;}
.compare .col{
  border-radius:7px;padding:7px 9px;
  font-size:10px;line-height:1.4;
  background:#fff;
  border:1px solid #e0d8c8;
}
.compare .col h4{
  font-size:10px;font-weight:800;text-transform:uppercase;
  margin-bottom:3px;letter-spacing:.3px;
  display:flex;align-items:center;gap:6px;
}
.compare .col h4 .h-ico{width:15px;height:15px;display:inline-flex;}
.compare .col h4 .h-ico svg{display:block;}
.compare .col p{margin-bottom:3px;color:var(--ink-2);}
.compare .col .fix{
  font-size:9.5px;color:var(--green);font-weight:700;
}
.compare .col .mini-code{
  font-family:"JetBrains Mono",monospace;font-size:9px;
  background:var(--term-bg);color:var(--term-fg);
  padding:4px 6px;border-radius:4px;margin-top:4px;
  white-space:pre-wrap;
}
.compare-grid-3{
  display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-top:6px;
}
.compare-grid-3 .compare{grid-template-columns:1fr;}

/* ============================================================
   WORKFLOW STRIP (page 20)
   ============================================================ */
.workflow{
  display:flex;align-items:center;justify-content:space-between;gap:8px;
  background:#fff;border:2px solid var(--green);border-radius:11px;
  padding:11px 15px;margin-top:11px;
}
.workflow .wf-step{
  display:flex;flex-direction:column;align-items:center;gap:4px;
  font-size:10px;font-weight:800;color:var(--green);text-transform:uppercase;
  flex:1;
}
.workflow .wf-step .wf-ico{width:30px;height:30px;display:inline-flex;}
.workflow .wf-step .wf-ico svg{display:block;}
.workflow .wf-arrow{color:var(--green);font-weight:800;font-size:15px;}
.workflow .wf-final{
  display:flex;align-items:center;gap:8px;padding-left:12px;
  border-left:2px solid #cde4d4;
}
.workflow .wf-final .wf-check{
  width:30px;height:30px;border-radius:50%;
  background:var(--green);color:#fff;
  display:flex;align-items:center;justify-content:center;
}
.workflow .wf-final .wf-check svg{display:block;}
.workflow .wf-final .wf-text{
  font-size:10.5px;font-weight:800;color:var(--green);
  text-transform:uppercase;line-height:1.3;
}

/* ============================================================
   STATUS BADGES (HTTP codes)
   ============================================================ */
.status-badges{
  display:flex;flex-direction:column;gap:4px;align-items:flex-start;
}
.status-badge{
  display:inline-flex;align-items:center;gap:6px;
  padding:3px 9px;border-radius:5px;
  font-size:10.5px;font-weight:800;color:#fff;
  font-family:monospace;
}
.status-2xx{background:var(--green);}
.status-3xx{background:var(--orange);}
.status-4xx{background:var(--red);}
.status-5xx{background:#7c2d12;}

/* ============================================================
   SAFE-SCRIPT TEMPLATE (page 16 full-width section)
   ============================================================ */
.template-section{
  background:#fff;border:1px solid #e0d8c8;border-radius:9px;
  padding:11px 14px;margin-bottom:11px;
  box-shadow:0 2px 8px rgba(0,0,0,.05);
}
.template-section h3{
  font-size:13px;font-weight:800;color:var(--green);
  text-transform:uppercase;letter-spacing:.5px;
  margin-bottom:8px;
  display:flex;align-items:center;gap:8px;
}
.template-section h3 .h-ico{width:22px;height:22px;display:inline-flex;}
.template-section h3 .h-ico svg{display:block;}
.template-section .ts-grid{
  display:grid;grid-template-columns:1.4fr 1fr;gap:12px;
}
.template-section .ts-explain{
  display:flex;flex-direction:column;gap:5px;
}
.template-section .ts-explain .ex-row{
  display:flex;gap:8px;align-items:flex-start;
  font-size:11px;color:var(--ink-2);line-height:1.4;
}
.template-section .ts-explain .ex-row .ex-ico{
  flex-shrink:0;width:18px;height:18px;display:inline-flex;
}
.template-section .ts-explain .ex-row .ex-ico svg{display:block;}
.template-section .ts-explain .ex-row .ex-text strong{
  color:var(--green);font-weight:800;
}
"""


# ============================================================
# HTML SNIPPET HELPERS
# ============================================================
def terminal(code: str, title: str = "bash") -> str:
    """Build a terminal block. `code` should be pre-formatted HTML."""
    return (
        f'<div class="terminal"><div class="term-bar">'
        f'<span class="term-dot dot-red"></span>'
        f'<span class="term-dot dot-amber"></span>'
        f'<span class="term-dot dot-green"></span>'
        f'<span class="term-title">{title}</span>'
        f'</div><div class="term-body">{code}</div></div>'
    )


def callout(text: str, style: str = "tip", ico_name: str | None = None) -> str:
    ico_html = f'<span class="ico">{icon(ico_name, 18)}</span>' if ico_name else ""
    return f'<div class="callout {style}">{ico_html}<div>{text}</div></div>'


def row(icon_name: str, num: str, heading: str, desc: str = "",
        inner_html: str = "") -> str:
    desc_html = f"<p>{desc}</p>" if desc else ""
    return (
        f'<div class="row"><div class="ico">{icon(icon_name, 34)}</div>'
        f'<div class="text"><h3>{num}{heading}</h3>{desc_html}{inner_html}</div></div>'
    )


def sidebar_card(icon_name: str, heading: str, body_html: str) -> str:
    return (
        f'<div class="card"><div class="head">'
        f'<span class="head-ico">{icon(icon_name, 16)}</span>'
        f'<span>{heading}</span></div>'
        f'<div class="body-pad">{body_html}</div></div>'
    )


def grid_card(icon_name: str, heading: str, color: str, body_html: str) -> str:
    return (
        f'<div class="grid-card"><div class="gc-head gc-{color}">'
        f'<span class="gc-ico">{icon(icon_name, 18)}</span>'
        f'<span>{heading}</span></div>'
        f'<div class="gc-body">{body_html}</div></div>'
    )


def key_takeaway(text: str, ico_name: str = "lightbulb",
                 heading: str = "KEY TAKEAWAY") -> str:
    return (
        f'<div class="key-takeaway"><span class="kt-ico">{icon(ico_name, 30)}</span>'
        f'<div class="kt-text"><strong>{heading}</strong>{text}</div></div>'
    )


# ============================================================
# PAGE-HEADER (title + subtitle)
# ============================================================
def page_header(title_num: str, title: str, subtitle: str,
                page_num: int, header_icon: str = "shell") -> str:
    return (
        f'<h1 class="page-title">'
        f'<span class="title-ico">{icon(header_icon, 40)}</span>'
        f'<span class="num">{title_num}.</span> {title}</h1>'
        f'<div class="page-subtitle">{subtitle}</div>'
        f'<div class="page-badge">Page {page_num} of 20</div>'
    )


# ============================================================
# FULL HTML DOC WRAPPER
# ============================================================
def make_html_doc(page_html: str, title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{SUPPLEMENTAL_CSS}
</style>
</head>
<body class="multi-page">

  {page_html}

</body>
</html>"""


# ============================================================
# PAGE 16 — 16. ERROR HANDLING AND SAFER SCRIPTS (3-col grid)
# (matches page-16.webp)
# ============================================================
def build_page_16() -> str:
    cards_html = f"""
      <div class="card-grid-3">
        {grid_card("warning", "1. WHY SCRIPTS FAIL SILENTLY", "red", """
          <p>By default, bash ignores errors and keeps going — hiding real issues.</p>
          {terminal('<span class="cmd">rm</span> file.txt\\n<span class="cmd">echo</span> <span class="str">"Deleted"</span>\\n<span class="cmd">echo</span> <span class="str">"Script finished"</span>', 'bad.sh')}
          {callout('<strong>Problem:</strong> If <code class="inline">rm</code> fails, the script keeps running and hides the error.', 'danger', 'bug')}
        """)}

        {grid_card("shield", "2. SET -E: EXIT ON ERROR", "green", """
          <p>Exit immediately if any command fails.</p>
          {terminal('<span class="cmd">set</span> -e\\n<span class="cmd">rm</span> file.txt\\n<span class="comment"># runs only if rm succeeds</span>', 'set -e')}
          {callout('<strong>Benefit:</strong> Stops the script when a command fails.', 'tip', 'check-circle')}
        """)}

        {grid_card("user", "3. SET -U: UNSET VARS", "navy", """
          <p>Exit if you use a variable that is not set.</p>
          {terminal('<span class="cmd">set</span> -u\\n<span class="cmd">echo</span> <span class="str">"$UNSET_VAR"</span>\\n<span class="comment"># fails fast</span>', 'set -u')}
          {callout('<strong>Benefit:</strong> Catches typos and missing variables early.', 'tip', 'check-circle')}
        """)}
      </div>

      <div class="card-grid-3">
        {grid_card("code", "4. SET -O PIPEFAIL", "blue", """
          <p>Detect failures inside pipelines.</p>
          {terminal('<span class="cmd">set</span> -o pipefail\\n<span class="cmd">cat</span> file <span class="kw">|</span> <span class="cmd">grep</span> <span class="str">"ERR"</span> <span class="kw">|</span> <span class="cmd">wc</span> -l', 'pipefail')}
          {callout('<strong>Benefit:</strong> Without pipefail, only the last command\\'s status is checked.', 'tip', 'check-circle')}
        """)}

        {grid_card("shield", "5. SET -EUO PIPEFAIL", "green", """
          <p>Best practice for safer scripts.</p>
          {terminal('<span class="cmd">set</span> -euo pipefail', 'safe-mode')}
          <ul>
            <li>Exit on any command error</li>
            <li>Error on unset variables</li>
            <li>Catch pipeline failures</li>
          </ul>
          <p style="margin-top:4px;font-size:10px;font-weight:800;color:var(--green);text-align:center;letter-spacing:.5px;">WRITE SAFER. SLEEP BETTER.</p>
        """)}

        {grid_card("clipboard", "6. VALIDATING INPUTS", "purple", """
          <p>Always verify inputs before using them.</p>
          {terminal('<span class="kw">if</span> [ -z <span class="str">"$1"</span> ]; <span class="kw">then</span>\\n  <span class="cmd">echo</span> <span class="str">"Usage: $0 &lt;url&gt;"</span>\\n  <span class="cmd">exit</span> 1\\n<span class="kw">fi</span>', 'validate')}
          {callout('<strong>Benefit:</strong> Prevents errors; makes scripts user-friendly.', 'tip', 'check-circle')}
        """)}
      </div>

      <div class="card-grid-3">
        {grid_card("gear", "7. CHECK DEPENDENCIES", "gold", """
          <p>Ensure required commands exist before running.</p>
          {terminal('<span class="kw">if</span> ! <span class="cmd">command</span> -v curl <span class="kw">&gt;/dev/null</span> 2&gt;&amp;1; <span class="kw">then</span>\\n  <span class="cmd">echo</span> <span class="str">"curl not found!"</span>\\n  <span class="cmd">exit</span> 1\\n<span class="kw">fi</span>', 'dep-check')}
          {callout('<strong>Benefit:</strong> Avoids failures due to missing tools.', 'tip', 'check-circle')}
        """)}

        {grid_card("bug", "8. HANDLING FAILURES", "red", """
          <p>Check command results and handle failures.</p>
          {terminal('<span class="kw">if</span> ! <span class="cmd">rm</span> file.txt; <span class="kw">then</span>\\n  <span class="cmd">echo</span> <span class="str">"Failed to remove file.txt"</span>\\n  <span class="cmd">exit</span> 1\\n<span class="kw">fi</span>', 'handle')}
          {callout('<strong>Benefit:</strong> React to failures; prevent bad outcomes.', 'tip', 'check-circle')}
        """)}

        {grid_card("refresh", "9. CLEAN UP ON FAIL", "teal", """
          <p>Use traps to clean up on exit or error.</p>
          {terminal('<span class="cmd">cleanup</span>() {{\\n  <span class="cmd">echo</span> <span class="str">"Cleaning up..."</span>\\n  <span class="cmd">rm</span> -f temp.log\\n}}\\n<span class="cmd">trap</span> cleanup EXIT', 'trap')}
          {callout('<strong>Benefit:</strong> Keeps systems clean even when scripts fail.', 'tip', 'check-circle')}
        """)}
      </div>

      <div class="card-grid-3">
        {grid_card("target", "10. PREDICTABLE AUTOMATION", "navy", """
          <p>Follow these rules for reliable scripts:</p>
          <ul>
            <li>Fail fast</li>
            <li>Validate inputs</li>
            <li>Check dependencies</li>
            <li>Handle errors</li>
            <li>Clean up properly</li>
            <li>Log what happens</li>
            <li>Exit with the right status code</li>
          </ul>
          <p style="margin-top:5px;font-size:10px;color:var(--green);font-weight:800;"><strong>Result:</strong> Reliable and predictable automation every time.</p>
        """)}

        {grid_card("check-circle", "11. SAFETY CHECKLIST", "green", """
          <p>The 7 rules of safer scripts:</p>
          <ul>
            <li>Use <code class="inline">set -euo pipefail</code></li>
            <li>Validate all user inputs</li>
            <li>Check command dependencies</li>
            <li>Handle command failures</li>
            <li>Trap cleanup on EXIT</li>
            <li>Log every action</li>
            <li>Exit 0 / non-zero explicitly</li>
          </ul>
        """)}

        {grid_card("lightbulb", "12. WHY IT MATTERS", "gold", """
          <p>Safe scripts = Less downtime, fewer bugs, happier users.</p>
          <p style="margin-top:5px;font-size:10px;">Always handle errors. Always clean up. Always be predictable.</p>
        """)}
      </div>

      <div class="template-section">
        <h3><span class="h-ico">{icon('code', 22)}</span>EXAMPLE: SAFE SCRIPT TEMPLATE</h3>
        <div class="ts-grid">
          {terminal('<span class="comment">#!/bin/bash</span>\\n<span class="cmd">set</span> -euo pipefail\\n\\n<span class="comment"># Check input</span>\\n<span class="kw">if</span> [ -z <span class="str">"$1"</span> ]; <span class="kw">then</span>\\n  <span class="cmd">echo</span> <span class="str">"Usage: $0 &lt;url&gt;"</span>; <span class="cmd">exit</span> 1\\n<span class="kw">fi</span>\\n\\n<span class="comment"># Check dependency</span>\\n<span class="cmd">command</span> -v curl <span class="kw">&gt;/dev/null</span> 2&gt;&amp;1 <span class="kw">||</span> {{ <span class="cmd">echo</span> <span class="str">"curl not found"</span>; <span class="cmd">exit</span> 1; }}\\n\\n<span class="comment"># Cleanup trap</span>\\n<span class="cmd">cleanup</span>() {{ <span class="cmd">echo</span> <span class="str">"Cleaning up..."</span>; <span class="cmd">rm</span> -f temp.log; }}\\n<span class="cmd">trap</span> cleanup EXIT\\n\\n<span class="comment"># Main logic</span>\\n<span class="cmd">URL</span>=<span class="str">"$1"</span>\\n<span class="cmd">HTTP_CODE</span>=$(<span class="cmd">curl</span> -s -o /dev/null -w <span class="str">"%{{http_code}}"</span> <span class="str">"$URL"</span>)\\n<span class="kw">if</span> [ <span class="str">"$HTTP_CODE"</span> -ge 200 ] <span class="kw">&amp;&amp;</span> [ <span class="str">"$HTTP_CODE"</span> -lt 400 ]; <span class="kw">then</span>\\n  <span class="cmd">echo</span> <span class="str">"[$URL] is UP (HTTP $HTTP_CODE)"</span>\\n<span class="kw">else</span>\\n  <span class="cmd">echo</span> <span class="str">"[$URL] is DOWN (HTTP $HTTP_CODE)"</span>; <span class="cmd">exit</span> 1\\n<span class="kw">fi</span>', 'safe-template.sh')}
          <div class="ts-explain">
            <div class="ex-row"><span class="ex-ico">{icon("shield", 18)}</span><div class="ex-text"><strong>Safe Mode</strong> — <code class="inline">set -euo pipefail</code> makes the script strict and safe.</div></div>
            <div class="ex-row"><span class="ex-ico">{icon("clipboard", 18)}</span><div class="ex-text"><strong>Validate Input</strong> — Ensure the user provides the required input.</div></div>
            <div class="ex-row"><span class="ex-ico">{icon("gear", 18)}</span><div class="ex-text"><strong>Check Dependency</strong> — Stop early if a required tool is missing.</div></div>
            <div class="ex-row"><span class="ex-ico">{icon("refresh", 18)}</span><div class="ex-text"><strong>Cleanup on Exit</strong> — Cleanup runs automatically on success or failure.</div></div>
            <div class="ex-row"><span class="ex-ico">{icon("code", 18)}</span><div class="ex-text"><strong>Main Logic</strong> — Do the work and check results.</div></div>
            <div class="ex-row"><span class="ex-ico">{icon("check-circle", 18)}</span><div class="ex-text"><strong>Exit Status</strong> — Exit 0 for success, non-zero for failure.</div></div>
          </div>
        </div>
      </div>
    """

    body_html = f"""
      {cards_html}

      {key_takeaway("Safe scripts = less downtime, fewer bugs, and happier users. Always handle errors. Always clean up. Always be predictable.", "lightbulb")}
    """

    content = page_header(
        title_num="16",
        title="ERROR HANDLING &amp; SAFER SCRIPTS",
        subtitle="WRITE PREDICTABLE. RELIABLE. SAFE AUTOMATION.",
        page_num=16,
        header_icon="shield",
    ) + body_html

    page_html = page_wrapper(content, paper_height=PAGE_HEIGHTS[16], page_id="p16")
    return make_html_doc(page_html, "16. ERROR HANDLING & SAFER SCRIPTS — Shell Scripting for DevOps")


# ============================================================
# PAGE 17 — 15. NETWORKING WITH SHELL SCRIPTS (2-col)
# (matches page-17.webp)
# ============================================================
def build_page_17() -> str:
    rows_html = f"""
      {row("globe", "1. ", "CURL — SEND HTTP REQUESTS",
          "Send HTTP requests to endpoints.",
          terminal('<span class="prompt">$</span> <span class="cmd">curl</span> <span class="str">https://example.com</span>\\n<span class="prompt">$</span> <span class="cmd">curl</span> -I <span class="str">https://example.com</span>\\n<span class="prompt">$</span> <span class="cmd">curl</span> -s -o /dev/null -w <span class="str">"%{{http_code}}"</span> URL', 'curl') +
          callout('<strong>Flags:</strong> <code class="inline">-I</code> headers only · <code class="inline">-s</code> silent · <code class="inline">-o /dev/null</code> discard body', 'tip', 'lightbulb'))}

      {row("monitor", "2. ", "PING — TEST CONNECTIVITY",
          "Test whether a host is reachable.",
          terminal('<span class="prompt">$</span> <span class="cmd">ping</span> -c 4 google.com\\n<span class="prompt">$</span> <span class="cmd">ping</span> -c 4 8.8.8.8', 'ping'))}

      {row("network", "3. ", "SS — CHECK CONNECTIONS",
          "Show network sockets and connections.",
          terminal('<span class="prompt">$</span> <span class="cmd">ss</span> -tlnp   <span class="comment"># listening ports</span>\\n<span class="prompt">$</span> <span class="cmd">ss</span> -tnp    <span class="comment"># all connections</span>\\n<span class="prompt">$</span> <span class="cmd">ss</span> -ltnp   <span class="comment"># listening with PID</span>', 'ss'))}

      {row("server", "4. ", "HOSTNAME — SYSTEM NAME",
          "Get or set the system hostname.",
          terminal('<span class="prompt">$</span> <span class="cmd">hostname</span>      <span class="comment"># name</span>\\n<span class="prompt">$</span> <span class="cmd">hostname</span> -I    <span class="comment"># IPs</span>\\n<span class="prompt">$</span> <span class="cmd">hostnamectl</span>   <span class="comment"># details</span>', 'hostname'))}

      {row("globe", "5. ", "DNS CHECKS — RESOLVE NAMES",
          "Check DNS resolution.",
          terminal('<span class="prompt">$</span> <span class="cmd">nslookup</span> example.com\\n<span class="prompt">$</span> <span class="cmd">dig</span> example.com\\n<span class="prompt">$</span> <span class="cmd">host</span> example.com', 'dns'))}

      {row("warning", "6. ", "HTTP STATUS CODES",
          "Check HTTP response codes — always check status codes, not just ping!",
          '<div class="status-badges">'
          '<span class="status-badge status-2xx">200 OK — Success</span>'
          '<span class="status-badge status-3xx">301/302 Redirect</span>'
          '<span class="status-badge status-4xx">404 Not Found</span>'
          '<span class="status-badge status-5xx">500 Server Error</span>'
          '</div>')}

      {row("check-circle", "7. ", "TEST ENDPOINT UP",
          "Quickly test if an endpoint is up.",
          terminal('<span class="prompt">$</span> <span class="cmd">curl</span> -s -o /dev/null -w <span class="str">"%{{http_code}}"</span> URL\\n<span class="comment"># 200-399 = Available</span>\\n<span class="comment"># 400-599 = Not Available</span>\\n<span class="comment"># 000 = No Response</span>', 'test'))}

      {row("bell", "8. ", "APP HEALTH CHECK",
          "Check if application health endpoint is OK.",
          terminal('<span class="prompt">$</span> <span class="cmd">curl</span> -s <span class="str">https://app/health</span>\\n<span class="prompt">$</span> <span class="cmd">curl</span> -sf URL <span class="kw">&amp;&amp;</span> <span class="cmd">echo</span> Healthy <span class="kw">||</span> <span class="cmd">echo</span> Unhealthy', 'health') +
          callout('<strong>Best practice:</strong> Expose a <code class="inline">/health</code> endpoint in apps.', 'tip', 'lightbulb'))}

      {row("shield", "9. ", "WEBSITE AVAILABILITY SCRIPT",
          "Example: Check website availability.",
          terminal('<span class="comment">#!/bin/bash</span>\\n<span class="cmd">URL</span>=<span class="str">"https://example.com"</span>\\n<span class="cmd">STATUS</span>=$(<span class="cmd">curl</span> -so /dev/null -w "%{{http_code}}" "$URL")\\n<span class="kw">if</span> [ "$STATUS" = "200" ]; <span class="kw">then</span>\\n  <span class="cmd">echo</span> <span class="str">"[OK] $URL is UP (200)"</span>\\n<span class="kw">else</span>\\n  <span class="cmd">echo</span> <span class="str">"[DOWN] $URL is DOWN (Code: $STATUS)"</span>\\n<span class="kw">fi</span>', 'avail.sh'))}
    """

    sidebar_html = f"""
      {sidebar_card("list", "NETWORKING QUICK REF", """
        <table class="tbl">
          <thead><tr><th>Command</th><th>Use</th></tr></thead>
          <tbody>
            <tr><td><code>curl URL</code></td><td>HTTP request</td></tr>
            <tr><td><code>ping HOST</code></td><td>Connectivity</td></tr>
            <tr><td><code>ss -tuln</code></td><td>Listening ports</td></tr>
            <tr><td><code>hostname</code></td><td>System name</td></tr>
            <tr><td><code>nslookup DOM</code></td><td>DNS lookup (basic)</td></tr>
            <tr><td><code>dig DOM</code></td><td>DNS lookup (advanced)</td></tr>
            <tr><td><code>host DOM</code></td><td>DNS lookup (simple)</td></tr>
            <tr><td><code>curl -I URL</code></td><td>Fetch headers</td></tr>
            <tr><td><code>curl -w "%{http_code}"</code></td><td>HTTP status code</td></tr>
          </tbody>
        </table>
      """)}

      {sidebar_card("check-circle", "BEST PRACTICES", """
        <ul>
          <li>Always check HTTP status codes.</li>
          <li>Use timeouts to avoid hanging scripts.</li>
          <li>Check both connectivity and application health.</li>
          <li>Log results for monitoring and alerting.</li>
          <li>Use meaningful alerts when a service is down.</li>
          <li>Test from the same network as users.</li>
          <li>Keep scripts simple, clear, and maintainable.</li>
        </ul>
      """)}

      {sidebar_card("globe", "WORKFLOW", """
        <div class="steps">
          <div class="step"><span class="step-ico">{icon('terminal', 18)}</span><div><strong>1. CHECK URL</strong> — Target the endpoint.</div></div>
          <div class="step"><span class="step-ico">{icon('clipboard', 18)}</span><div><strong>2. GET STATUS</strong> — Capture HTTP code.</div></div>
          <div class="step"><span class="step-ico">{icon('shield', 18)}</span><div><strong>3. REPORT RESULT</strong> — UP / DOWN message.</div></div>
        </div>
      """)}
    """

    body_html = f"""
      <div class="body">
        <div class="rows">
          {rows_html}
        </div>
        <div class="sidebar">
          {sidebar_html}
        </div>
      </div>

      {key_takeaway("Automate your network checks. Detect issues early. Keep your systems and services reliable.", "lightbulb")}
    """

    content = page_header(
        title_num="15",
        title="NETWORKING WITH SHELL SCRIPTS",
        subtitle="TEST. MONITOR. ENSURE AVAILABILITY.",
        page_num=17,
        header_icon="globe",
    ) + body_html

    page_html = page_wrapper(content, paper_height=PAGE_HEIGHTS[17], page_id="p17")
    return make_html_doc(page_html, "15. NETWORKING WITH SHELL SCRIPTS — Shell Scripting for DevOps")


# ============================================================
# PAGE 18 — 18. SCHEDULING SCRIPTS WITH CRON (2-col)
# (matches page-18.webp)
# ============================================================
def build_page_18() -> str:
    rows_html = f"""
      {row("gear", "1. ", "WHAT CRON DOES",
          "Cron runs commands or scripts automatically at scheduled times. Perfect for backups, cleanup, monitoring, reports, and more.")}

      {row("pencil", "2. ", "UNDERSTANDING CRONTAB",
          "Crontab is your personal cron schedule.",
          terminal('<span class="cmd">crontab</span> -e    <span class="comment"># Edit</span>\\n<span class="cmd">crontab</span> -l    <span class="comment"># List jobs</span>\\n<span class="cmd">crontab</span> -r    <span class="comment"># Remove all jobs</span>', 'crontab'))}

      {row("list", "3. ", "CRON TIMING SYNTAX",
          "Five fields: <code class='inline'>MIN HOUR DAY MONTH DOW</code>",
          '<table class="tbl"><thead><tr><th>Field</th><th>Range</th></tr></thead><tbody>'
          '<tr><td>MIN</td><td>0–59</td></tr>'
          '<tr><td>HOUR</td><td>0–23</td></tr>'
          '<tr><td>DAY</td><td>1–31</td></tr>'
          '<tr><td>MONTH</td><td>1–12</td></tr>'
          '<tr><td>DOW</td><td>0–6 (0=Sun)</td></tr>'
          '</tbody></table>'
          '<p style="font-size:10.5px;margin-top:6px;font-weight:800;color:var(--green);">EXAMPLES</p>'
          '<table class="tbl"><thead><tr><th>Pattern</th><th>Meaning</th></tr></thead><tbody>'
          '<tr><td><code>* * * * *</code></td><td>Every minute</td></tr>'
          '<tr><td><code>0 * * * *</code></td><td>Every hour at :00</td></tr>'
          '<tr><td><code>0 2 * * *</code></td><td>Daily at 2 AM</td></tr>'
          '<tr><td><code>30 1 * * 1</code></td><td>Mon at 1:30 AM</td></tr>'
          '<tr><td><code>0 3 1 * *</code></td><td>1st of month at 3 AM</td></tr>'
          '</tbody></table>')}

      {row("play", "4. ", "RUNNING SCRIPTS AUTOMATICALLY",
          "Add your cron job with <code class='inline'>crontab -e</code>. Cron runs jobs in the background — no need to keep your terminal open. Great for hands-off automation.")}

      {row("monitor", "5. ", "ENVIRONMENT DIFFERENCES",
          "Cron runs with a minimal environment. Your PATH, variables, and shell may be different. Use full paths in scripts and set needed variables inside the script.",
          terminal('<span class="cmd">PATH</span>=/usr/local/bin:/usr/bin:/bin\\n<span class="cmd">export</span> PATH', 'env'))}

      {row("file", "6. ", "LOGGING CRON OUTPUT",
          "Always log output for debugging. Redirect output and errors.",
          terminal('<span class="comment">*/5 * * * * /path/to/script.sh \\</span>\\n  <span class="kw">&gt;&gt;</span> /var/log/mycron.log 2&gt;&amp;1', 'logging'))}

      {row("warning", "7. ", "COMMON CRON FAILURES",
          "Watch for these pitfalls:",
          '<ul>'
          '<li>Wrong timing syntax</li>'
          '<li>Script path incorrect</li>'
          '<li>Script not executable</li>'
          '<li>Missing environment variables</li>'
          '<li>No permissions to run script</li>'
          '<li>Output not logged</li>'
          '<li>Mail not configured</li>'
          '<li>Cron service not running</li>'
          '</ul>')}

      {row("refresh", "8. ", "BACKUP &amp; CLEANUP JOBS",
          "Two practical scheduled-job examples:",
          terminal('<span class="comment"># BACKUP JOB — daily at 2 AM</span>\\n0 2 * * * /backup.sh \\<span class="kw">&gt;&gt;</span> /var/log/backup.log 2&gt;&amp;1\\n\\n<span class="comment"># CLEANUP JOB — weekly Sun at 3:30 AM</span>\\n30 3 * * 0 /cleanup.sh \\<span class="kw">&gt;&gt;</span> /var/log/cleanup.log 2&gt;&amp;1', 'jobs'))}
    """

    sidebar_html = f"""
      {sidebar_card("list", "CRON SYNTAX QUICK REF", """
        <table class="tbl">
          <thead><tr><th>Symbol</th><th>Meaning</th></tr></thead>
          <tbody>
            <tr><td><code>*</code></td><td>Any value</td></tr>
            <tr><td><code>,</code></td><td>Values list (1,2,3)</td></tr>
            <tr><td><code>-</code></td><td>Range (1-5)</td></tr>
            <tr><td><code>/</code></td><td>Step values (*/10)</td></tr>
            <tr><td><code>0-59</code></td><td>Minute</td></tr>
            <tr><td><code>0-23</code></td><td>Hour</td></tr>
            <tr><td><code>1-31</code></td><td>Day of month</td></tr>
            <tr><td><code>1-12</code></td><td>Month</td></tr>
            <tr><td><code>0-6</code></td><td>Day of week (0=Sun)</td></tr>
            <tr><td><code>@daily</code></td><td>Same as 0 0 * * *</td></tr>
            <tr><td><code>@weekly</code></td><td>Same as 0 0 * * 0</td></tr>
            <tr><td><code>@reboot</code></td><td>Run once at startup</td></tr>
          </tbody>
        </table>
      """)}

      {sidebar_card("check-circle", "BEST PRACTICES", """
        <ul>
          <li>Use full paths for commands and scripts.</li>
          <li>Log all cron outputs.</li>
          <li>Test scripts manually before scheduling.</li>
          <li>Keep cron jobs simple and reliable.</li>
          <li>Review your crontab regularly.</li>
          <li>Set PATH and needed variables inside scripts.</li>
          <li>Make scripts executable (<code>chmod +x</code>).</li>
        </ul>
      """)}

      {sidebar_card("calendar", "SCHEDULE EXAMPLES", """
        <p>Common schedule patterns:</p>
        <table class="tbl">
          <thead><tr><th>Pattern</th><th>When</th></tr></thead>
          <tbody>
            <tr><td><code>*/5 * * * *</code></td><td>Every 5 min</td></tr>
            <tr><td><code>0 * * * *</code></td><td>Hourly</td></tr>
            <tr><td><code>0 0 * * *</code></td><td>Midnight daily</td></tr>
            <tr><td><code>0 2 * * *</code></td><td>2 AM daily</td></tr>
            <tr><td><code>0 0 * * 0</code></td><td>Weekly Sun</td></tr>
            <tr><td><code>0 0 1 * *</code></td><td>Monthly 1st</td></tr>
          </tbody>
        </table>
      """)}
    """

    body_html = f"""
      <div class="body">
        <div class="rows">
          {rows_html}
        </div>
        <div class="sidebar">
          {sidebar_html}
        </div>
      </div>

      {key_takeaway("Cron automates the boring stuff: backups, cleanups, monitoring, reports. Use full paths, log output, and test before scheduling.", "lightbulb")}
    """

    content = page_header(
        title_num="18",
        title="SCHEDULING SCRIPTS WITH CRON",
        subtitle="AUTOMATE TASKS. SAVE TIME. STAY RELIABLE.",
        page_num=18,
        header_icon="calendar",
    ) + body_html

    page_html = page_wrapper(content, paper_height=PAGE_HEIGHTS[18], page_id="p18")
    return make_html_doc(page_html, "18. SCHEDULING SCRIPTS WITH CRON — Shell Scripting for DevOps")


# ============================================================
# PAGE 19 — 17. DEBUGGING SHELL SCRIPTS (2-col)
# (matches page-19.webp)
# ============================================================
def build_page_19() -> str:
    compare_cards = """
      <div class="compare-grid-3">
        <div class="compare">
          <div class="col">
            <h4><span class="h-ico">__BUG_A__</span>A. SYNTAX ERRORS</h4>
            <p>Missing symbols or wrong structure.</p>
            <div class="mini-code">if [ "${VAR}" = "x" ]
echo "missing fi"</div>
            <p class="fix">Fix: check brackets, then/fi, do/done.</p>
          </div>
          <div class="col">
            <h4><span class="h-ico">__BUG_B__</span>B. QUOTING PROBLEMS</h4>
            <p>Wrong quotes break the script.</p>
            <div class="mini-code">echo "Hi $USER"    # ok
echo 'Hi $USER'    # literal
echo "He said "hi""  # bad</div>
            <p class="fix">Fix: use double quotes; escape inner.</p>
          </div>
        </div>
        <div class="compare">
          <div class="col">
            <h4><span class="h-ico">__BUG_C__</span>C. MISSING VARIABLES</h4>
            <p>Using variables that are not set.</p>
            <div class="mini-code">echo $NAME
./script.sh: line 5: NAME:
  unbound variable</div>
            <p class="fix">Fix: define or use ${NAME:-default}.</p>
          </div>
          <div class="col">
            <h4><span class="h-ico">__BUG_D__</span>D. PERMISSION ERRORS</h4>
            <p>Script or files not executable.</p>
            <div class="mini-code">./script.sh: line 3:
  ./other.sh: Permission denied</div>
            <p class="fix">Fix: chmod +x script.sh.</p>
          </div>
        </div>
        <div class="compare">
          <div class="col">
            <h4><span class="h-ico">__BUG_E__</span>E. PATH PROBLEMS</h4>
            <p>Command not found.</p>
            <div class="mini-code">mycmd: command not found</div>
            <p class="fix">Fix: check PATH or use full path.</p>
          </div>
          <div class="col">
            <h4><span class="h-ico">__BUG_F__</span>F. FILE MISSING</h4>
            <p>File or directory does not exist.</p>
            <div class="mini-code">cat: file.txt:
  No such file or directory</div>
            <p class="fix">Fix: verify path; use absolute path.</p>
          </div>
        </div>
      </div>
    """
    for letter in ["A", "B", "C", "D", "E", "F"]:
        compare_cards = compare_cards.replace(f"__BUG_{letter}__", icon("bug", 16))

    rows_html = f"""
      {row("eye", "1. ", "READING SHELL ERRORS",
          "Errors tell you what went wrong. Read them carefully — the message always gives a clue.",
          terminal('./script.sh: <span class="comment">line 10: mycmd: command not found</span>\\n./script.sh: <span class="comment">line 15: [ : : integer expression expected</span>\\n<span class="comment">Permission denied</span>\\n<span class="comment">No such file or directory</span>') +
          callout('<strong>Tip:</strong> The error message always gives a clue. Look at the line number and message.', 'tip', 'lightbulb'))}

      {row("terminal", "2. ", "DEBUG MODE WITH BASH -X",
          "Run your script with <code class='inline'>bash -x</code> to see each command as it executes.",
          terminal('<span class="prompt">$</span> <span class="cmd">bash</span> -x script.sh\\n<span class="comment"># Example output:</span>\\n+ <span class="cmd">echo</span> <span class="str">"Starting"</span>\\nStarting\\n+ VAR=hello\\n+ <span class="cmd">echo</span> $VAR\\nhello\\n+ <span class="cmd">ls</span> /not/exist\\nls: cannot access <span class="str">\'/not/exist\'</span>: No such file or directory'))}

      {row("code", "3. ", "DEBUG MODE INSIDE SCRIPT",
          "Use <code class='inline'>set -x</code> to enable debug inside the script.",
          terminal('<span class="cmd">set</span> -x\\n<span class="comment"># Your commands here</span>\\n<span class="cmd">set</span> +x   <span class="comment"># Turn off debug</span>') +
          callout('<strong>Benefit:</strong> Shows each command as it runs. Very helpful to trace issues.', 'tip', 'check-circle'))}

      {row("bug", "4. ", "COMMON PROBLEMS &amp; FIXES",
          "Six common failure categories:",
          compare_cards)}

      {row("list", "5. ", "DEBUGGING STEP BY STEP",
          "A repeatable workflow for fixing any script:",
          '<div class="steps">' +
          '<div class="step"><span class="step-ico">' + icon("book", 18) + '</span><div><strong>1. Read the error</strong> — Understand what the error says. Note the line number and message.</div></div>' +
          '<div class="step"><span class="step-ico">' + icon("search", 18) + '</span><div><strong>2. Reproduce the issue</strong> — Run the script and confirm the error happens again.</div></div>' +
          '<div class="step"><span class="step-ico">' + icon("terminal", 18) + '</span><div><strong>3. Run with bash -x</strong> — Use <code class="inline">bash -x script.sh</code> to see each command and where it fails.</div></div>' +
          '<div class="step"><span class="step-ico">' + icon("clipboard", 18) + '</span><div><strong>4. Check variables and quotes</strong> — Make sure variables are set and quoted correctly.</div></div>' +
          '<div class="step"><span class="step-ico">' + icon("wrench", 18) + '</span><div><strong>5. Fix and test again</strong> — Make the change and run again. Repeat until the error is gone.</div></div>' +
          '<div class="step"><span class="step-ico">' + icon("check-circle", 18) + '</span><div><strong>6. Remove debug</strong> — Remove <code class="inline">set -x</code> or stop using <code class="inline">bash -x</code> after fixing.</div></div>' +
          '</div>')}
    """

    sidebar_html = f"""
      {sidebar_card("bug", "COMMON ERROR MESSAGES", """
        <p>What each message usually means:</p>
        <ul>
          <li><strong>command not found</strong> — PATH issue or typo.</li>
          <li><strong>Permission denied</strong> — missing +x or wrong owner.</li>
          <li><strong>No such file</strong> — path typo or missing file.</li>
          <li><strong>unbound variable</strong> — used with <code>set -u</code>.</li>
          <li><strong>integer expression expected</strong> — non-numeric in <code>[ ]</code>.</li>
          <li><strong>unexpected token</strong> — missing <code>fi</code>, <code>done</code>, or quote.</li>
        </ul>
      """)}

      {sidebar_card("terminal", "DEBUG TOOLBOX", """
        <p>Tools to debug shell scripts:</p>
        <table class="tbl">
          <thead><tr><th>Tool</th><th>Use</th></tr></thead>
          <tbody>
            <tr><td><code>bash -x</code></td><td>Trace each command</td></tr>
            <tr><td><code>set -x</code> / <code>set +x</code></td><td>Toggle trace</td></tr>
            <tr><td><code>bash -v</code></td><td>Verbose (read lines)</td></tr>
            <tr><td><code>bash -n</code></td><td>Syntax check only</td></tr>
            <tr><td><code>shellcheck</code></td><td>Static linter</td></tr>
            <tr><td><code>echo $VAR</code></td><td>Inspect value</td></tr>
            <tr><td><code>trap</code></td><td>Catch signals/errors</td></tr>
          </tbody>
        </table>
      """)}

      {sidebar_card("check-circle", "DEBUG CHECKLIST", """
        <ul>
          <li>Read the error message.</li>
          <li>Reproduce consistently.</li>
          <li>Trace with <code>bash -x</code>.</li>
          <li>Verify all variables.</li>
          <li>Check all quotes.</li>
          <li>Confirm file paths exist.</li>
          <li>Validate permissions.</li>
          <li>Test fix; remove debug.</li>
        </ul>
      """)}
    """

    body_html = f"""
      <div class="body">
        <div class="rows">
          {rows_html}
        </div>
        <div class="sidebar">
          {sidebar_html}
        </div>
      </div>

      {key_takeaway("Read errors carefully, reproduce the issue, and trace with bash -x. Most bugs are syntax, quoting, or path issues. Debug methodically — don't guess.", "lightbulb")}
    """

    content = page_header(
        title_num="17",
        title="DEBUGGING SHELL SCRIPTS",
        subtitle="FIND ISSUES. UNDERSTAND CAUSES. FIX FAST.",
        page_num=19,
        header_icon="search",
    ) + body_html

    page_html = page_wrapper(content, paper_height=PAGE_HEIGHTS[19], page_id="p19")
    return make_html_doc(page_html, "17. DEBUGGING SHELL SCRIPTS — Shell Scripting for DevOps")


# ============================================================
# PAGE 20 — 19. SHELL SCRIPTING IN DEVOPS WORKFLOWS (2-col)
# (matches page-20.webp)
# ============================================================
def build_page_20() -> str:
    rows_html = f"""
      {row("refresh", "1. ", "SHELL SCRIPTS IN CI/CD",
          "Automate build, test, and deploy across every stage.",
          '<ul>'
          '<li>Run commands at every stage</li>'
          '<li>Make pipelines reliable and repeatable</li>'
          '<li>Handle setup, checks, and notifications</li>'
          '</ul>')}

      {row("branch", "2. ", "GITHUB ACTIONS",
          "Use shell scripts in workflow steps.",
          '<ul>'
          '<li>Run custom commands easily</li>'
          '<li>Prepare environments</li>'
          '<li>Build, test, and deploy apps</li>'
          '</ul>' +
          terminal('- <span class="cmd">name</span>: Run script\\n  <span class="cmd">run</span>: ./deploy.sh', 'github-actions'))}

      {row("server", "3. ", "JENKINS",
          "Execute shell scripts in build steps.",
          '<ul>'
          '<li>Automate jobs and deployments</li>'
          '<li>Manage environments</li>'
          '<li>Integrate with other tools</li>'
          '</ul>' +
          terminal('<span class="comment">#!/bin/bash</span>\\n./build.sh <span class="kw">&amp;&amp;</span> ./deploy.sh', 'jenkins'))}

      {row("container", "4. ", "DOCKER",
          "Build and push images with shell scripts.",
          '<ul>'
          '<li>Build and push images</li>'
          '<li>Prepare container environments</li>'
          '<li>Clean up unused resources</li>'
          '<li>Manage volumes and networks</li>'
          '</ul>' +
          terminal('<span class="comment">#!/bin/bash</span>\\n<span class="cmd">docker</span> build -t myapp .\\n<span class="cmd">docker</span> push myapp:latest', 'docker'))}

      {row("network", "5. ", "KUBERNETES",
          "Automate kubectl commands.",
          '<ul>'
          '<li>Deploy and update applications</li>'
          '<li>Manage configs and secrets</li>'
          '<li>Check pod and service status</li>'
          '</ul>' +
          terminal('<span class="cmd">kubectl</span> apply -f app.yaml\\n<span class="cmd">kubectl</span> rollout status deploy/app', 'kubectl'))}

      {row("cloud", "6. ", "CLOUD VM INITIALIZATION",
          "Run scripts on first boot via cloud-init.",
          '<ul>'
          '<li>Install packages and tools</li>'
          '<li>Configure users and services</li>'
          '<li>Set up security and updates</li>'
          '</ul>' +
          terminal('<span class="comment">#!/bin/bash</span>\\n<span class="cmd">apt</span> update <span class="kw">&amp;&amp;</span> <span class="cmd">apt</span> install -y nginx\\n<span class="cmd">systemctl</span> enable nginx', 'cloud-init'))}

      {row("rocket", "7. ", "DEPLOYMENT SCRIPTS",
          "Automate deployments with rollback safety.",
          '<ul>'
          '<li>Automate deployments</li>'
          '<li>Backup before updates</li>'
          '<li>Rollback on failure</li>'
          '<li>Zero- or low-downtime</li>'
          '</ul>' +
          terminal('./deploy.sh --env prod\\n./rollback.sh', 'deploy'))}

      {row("bell", "8. ", "HEALTH CHECKS",
          "Verify apps and services stay up.",
          '<ul>'
          '<li>Check app and services</li>'
          '<li>Validate endpoints</li>'
          '<li>Alert on failure</li>'
          '<li>Keep systems reliable</li>'
          '</ul>' +
          terminal('<span class="comment">#!/bin/bash</span>\\n<span class="cmd">curl</span> -f http://localhost/ <span class="kw">||</span> <span class="cmd">exit</span> 1', 'health.sh'))}

      {row("clipboard", "9. ", "ENVIRONMENT VALIDATION",
          "Fail fast if the environment is wrong.",
          '<ul>'
          '<li>Verify required tools</li>'
          '<li>Check variables and configs</li>'
          '<li>Validate dependencies</li>'
          '<li>Fail fast if something is wrong</li>'
          '</ul>' +
          terminal('<span class="cmd">command</span> -v docker <span class="kw">&gt;/dev/null</span> <span class="kw">||</span> {{ <span class="cmd">echo</span> <span class="str">"Docker not found"</span>; <span class="cmd">exit</span> 1; }}', 'validate'))}

      {row("cube", "10. ", "WHERE SHELL SCRIPTING FITS",
          "The glue between every DevOps tool.",
          '<ul>'
          '<li>Glue between tools</li>'
          '<li>Automate small and big tasks</li>'
          '<li>Provide flexibility</li>'
          '<li>Save time and reduce errors</li>'
          '<li>Core skill for every DevOps engineer</li>'
          '</ul>')}
    """

    sidebar_html = f"""
      {sidebar_card("rocket", "DEVOPS WORKFLOW", """
        <p>Where shell scripts fit:</p>
        <div class="steps" style="gap:6px;">
          <div class="step"><span class="step-ico">{icon('code', 18)}</span><div><strong>Code</strong> — write &amp; commit</div></div>
          <div class="step"><span class="step-ico">{icon('gear', 18)}</span><div><strong>Build</strong> — compile &amp; package</div></div>
          <div class="step"><span class="step-ico">{icon('clipboard', 18)}</span><div><strong>Test</strong> — run test suite</div></div>
          <div class="step"><span class="step-ico">{icon('rocket', 18)}</span><div><strong>Deploy</strong> — push to prod</div></div>
          <div class="step"><span class="step-ico">{icon('server', 18)}</span><div><strong>Monitor</strong> — health &amp; alerts</div></div>
        </div>
      """)}

      {sidebar_card("container", "TOOLS YOU'LL TOUCH", """
        <p>Popular DevOps tools driven by shell scripts:</p>
        <ul>
          <li><strong>CI/CD:</strong> GitHub Actions, Jenkins, GitLab CI</li>
          <li><strong>Containers:</strong> Docker, Podman</li>
          <li><strong>Orchestration:</strong> Kubernetes, Helm</li>
          <li><strong>Cloud:</strong> AWS, GCP, Azure (CLIs)</li>
          <li><strong>IaC:</strong> Terraform, Ansible</li>
          <li><strong>Monitoring:</strong> Prometheus, Grafana</li>
        </ul>
      """)}

      {sidebar_card("check-circle", "DEVOPS BEST PRACTICES", """
        <ul>
          <li>Make scripts idempotent (safe to re-run).</li>
          <li>Always log what happens.</li>
          <li>Use <code>set -euo pipefail</code>.</li>
          <li>Validate environment before running.</li>
          <li>Backup before deploying.</li>
          <li>Rollback on failure.</li>
          <li>Monitor after every deploy.</li>
        </ul>
      """)}
    """

    workflow_html = f"""
      <div class="workflow">
        <div class="wf-step"><span class="wf-ico">{icon('code', 28)}</span><span>Code</span></div>
        <span class="wf-arrow">→</span>
        <div class="wf-step"><span class="wf-ico">{icon('gear', 28)}</span><span>Build</span></div>
        <span class="wf-arrow">→</span>
        <div class="wf-step"><span class="wf-ico">{icon('clipboard', 28)}</span><span>Test</span></div>
        <span class="wf-arrow">→</span>
        <div class="wf-step"><span class="wf-ico">{icon('rocket', 28)}</span><span>Deploy</span></div>
        <span class="wf-arrow">→</span>
        <div class="wf-step"><span class="wf-ico">{icon('server', 28)}</span><span>Monitor</span></div>
        <div class="wf-final">
          <span class="wf-check">{icon('check-circle', 22)}</span>
          <span class="wf-text">One simple script can<br>automate hours of work.</span>
        </div>
      </div>
    """

    body_html = f"""
      <div class="body">
        <div class="rows">
          {rows_html}
        </div>
        <div class="sidebar">
          {sidebar_html}
        </div>
      </div>

      {workflow_html}

      {key_takeaway("Shell scripting is the glue of DevOps — automate everything, integrate everywhere, deploy with confidence.", "lightbulb")}
    """

    content = page_header(
        title_num="19",
        title="SHELL SCRIPTING IN DEVOPS WORKFLOWS",
        subtitle="AUTOMATE. INTEGRATE. DEPLOY.",
        page_num=20,
        header_icon="rocket",
    ) + body_html

    page_html = page_wrapper(content, paper_height=PAGE_HEIGHTS[20], page_id="p20")
    return make_html_doc(page_html, "19. SHELL SCRIPTING IN DEVOPS WORKFLOWS — Shell Scripting for DevOps")


# ============================================================
# MAIN
# ============================================================
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pages = [
        (16, build_page_16()),
        (17, build_page_17()),
        (18, build_page_18()),
        (19, build_page_19()),
        (20, build_page_20()),
    ]

    import re as _re
    print("--- Building pages 16-20 (v3, polotno_template) ---")
    for page_num, html in pages:
        out_path = OUTPUT_DIR / f"recreated-page-{page_num:02d}.html"
        out_path.write_text(html, encoding="utf-8")
        # Quick verification
        content = out_path.read_text(encoding="utf-8")
        content_no_css = _re.sub(r'/\*.*?\*/', '', content, flags=_re.DOTALL)
        icon_count = content.count('viewBox="0 0 48 48"')
        has_polotno = 'class="page-wrapper"' in content and 'HOLE_SVG_TEMPLATE' not in content
        has_multi = 'class="multi-page"' in content
        no_veriqta = "VERIQTA" not in content_no_css.upper()
        no_social = "social-footer" not in content
        # Each polotno page has 18+ holes with unique gradient IDs (h0..h17 etc.)
        hole_count = content.count("stop-color='#000000' stop-opacity='0'")
        print(f"  Page {page_num}: {len(html):,} bytes, {icon_count} icons, "
              f"{hole_count} hole stops, polotno_wrapper={has_polotno}, "
              f"multi-page={has_multi}, no-veriqta-visible={no_veriqta}, no-social={no_social}")


if __name__ == "__main__":
    main()
