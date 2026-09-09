#!/usr/bin/env python3
"""
Rebuild carousel pages 6-10 as self-contained HTML files.

This is the v2 rebuild — uses:
  - The colorful filled SVG icons from scripts/shell_scripting_icons.py
  - The canonical notebook-template.css
    (public/uploads/notebook-template/notebook-template.css)
  - The correct layout per page based on VLM analysis:
      Page 6: 3-column layout  (Variables)
      Page 7: 3-column layout  (Exit Codes)
      Page 8: 3-column layout  (Conditional Statements)
      Page 9: single column centered (Logical Operators)
      Page 10: 2-column grid   (Loops for Automation)

Output structure: <body class="multi-page"> > .page-wrapper > .page > .content

NO VERIQTA branding, NO social footer.

Writes:
  downloads/instagram-DcaW1UljsVk/recreated-page-06.html
  downloads/instagram-DcaW1UljsVk/recreated-page-07.html
  downloads/instagram-DcaW1UljsVk/recreated-page-08.html
  downloads/instagram-DcaW1UljsVk/recreated-page-09.html
  downloads/instagram-DcaW1UljsVk/recreated-page-10.html
"""

import os
import sys

# Make sibling icon library importable
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

# Colorful multi-color filled SVG icons (53 icons)
from shell_scripting_icons import icon as color_icon  # noqa: E402

# Canonical notebook template CSS
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPTS_DIR, ".."))
CANONICAL_CSS_PATH = os.path.join(
    PROJECT_ROOT, "public", "uploads", "notebook-template", "notebook-template.css"
)
with open(CANONICAL_CSS_PATH, "r", encoding="utf-8") as f:
    CANONICAL_CSS = f.read()

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT, "downloads", "instagram-DcaW1UljsVk"
)


# ============================================================
# CONTENT CSS — extends the canonical notebook template
# ============================================================

CONTENT_CSS = r"""
/* ============================================================
   CONTENT STYLES for Shell Scripting carousel pages
   (extends canonical notebook-template.css)
   ============================================================ */

/* ---- Brand bar ---- */
.brand-bar{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:18px;
}
.brand-bar .badge{
  background:var(--navy);color:#fff;
  padding:6px 16px;border-radius:999px;
  font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
}
.brand-bar .crumb{
  font-size:11px;font-weight:700;letter-spacing:1.5px;
  color:var(--navy);text-transform:uppercase;
  display:flex;align-items:center;gap:8px;
}

/* ---- Page title ---- */
.page-title{
  display:flex;align-items:center;justify-content:center;gap:14px;
  margin-bottom:6px;
}
.page-title .ico{flex-shrink:0;}
.page-title .ico svg{width:46px;height:46px;display:block;}
.page-title h1{
  font-size:34px;font-weight:800;color:var(--navy);
  text-transform:uppercase;letter-spacing:-.5px;line-height:1.05;
  text-align:center;
}
.page-subtitle{
  font-size:13px;font-weight:700;color:var(--ink-2);
  text-transform:uppercase;letter-spacing:1.4px;text-align:center;
  margin-bottom:18px;
  padding-bottom:12px;
  border-bottom:2px solid var(--navy);
  position:relative;
}
.page-subtitle::after{
  content:"";position:absolute;left:50%;bottom:-6px;
  width:10px;height:10px;background:var(--navy);
  border-radius:50%;transform:translateX(-50%);
}

/* ---- Body layout primitives ---- */
.body{margin-bottom:14px;}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;}
.grid-5{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;}
.single{max-width:920px;margin:0 auto;}

/* ---- Card ---- */
.card{
  background:#fff;
  border-radius:10px;
  overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
  border:1px solid rgba(0,0,0,.05);
  display:flex;flex-direction:column;
}
.card .head{
  background:var(--navy);color:#fff;
  padding:8px 12px;
  font-size:11.5px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
  display:flex;align-items:center;gap:8px;
  line-height:1.2;
}
.card .head .num{
  background:rgba(255,255,255,.18);
  border-radius:6px;
  padding:1px 6px;font-size:10px;
}
.card .head .ico{flex-shrink:0;display:inline-flex;}
.card .head .ico svg{width:18px;height:18px;display:block;}
.card .body-pad{padding:10px 12px;flex:1;}

/* ---- Card heading variants (color-coded) ---- */
.card.head-green .head{background:#1B5E3F;}
.card.head-blue .head{background:#2563eb;}
.card.head-purple .head{background:#7c3aed;}
.card.head-red .head{background:#dc2626;}
.card.head-gold .head{background:#d4a017;}
.card.head-teal .head{background:#0d7377;}
.card.head-navy .head{background:#15264d;}

/* ---- Terminal ---- */
.terminal{
  background:#0d1117;border-radius:8px;overflow:hidden;
  box-shadow:0 4px 14px rgba(0,0,0,.2);
}
.terminal .term-bar{
  background:#1c2230;padding:6px 12px;
  display:flex;align-items:center;gap:6px;
}
.terminal .term-dot{width:9px;height:9px;border-radius:50%;}
.terminal .dot-red{background:#ff5f56;}
.terminal .dot-amber{background:#ffbd2e;}
.terminal .dot-green{background:#27c93f;}
.terminal .term-title{
  margin-left:auto;color:#8b949e;
  font-size:10px;font-family:"JetBrains Mono","Fira Code",monospace;
}
.terminal .term-body{
  padding:10px 12px;
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:11.5px;line-height:1.55;
  color:#e6edf3;
  white-space:pre;
  overflow-x:auto;
}
.terminal .term-body .prompt{color:#7ee787;}
.terminal .term-body .comment{color:#8b949e;}
.terminal .term-body .cmd{color:#79c0ff;}
.terminal .term-body .str{color:#f2cc60;}
.terminal .term-body .out{color:#e6edf3;}
.terminal .term-body .kw{color:#ff7b72;}

/* ---- Inline code & text ---- */
.card p{font-size:11.5px;color:var(--ink-2);line-height:1.5;margin-bottom:4px;}
.card p:last-child{margin-bottom:0;}
.card code, code.inline{
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:10.5px;
  background:#efe9dd;padding:1px 5px;border-radius:3px;
  color:var(--navy);
}
.bullets{
  list-style:none;padding:0;margin:0;
  font-size:11px;color:var(--ink-2);line-height:1.5;
}
.bullets li{
  padding-left:14px;position:relative;margin-bottom:2px;
}
.bullets li::before{
  content:"•";position:absolute;left:0;color:var(--navy);font-weight:700;
}
.bullets.tick li::before{content:"✓";color:#1B5E3F;font-weight:800;}
.bullets.warn li::before{content:"!";color:#d4a017;font-weight:800;}

/* ---- Tables ---- */
.tbl{width:100%;border-collapse:collapse;font-size:11px;}
.tbl th{
  background:var(--navy);color:#fff;
  padding:6px 9px;text-align:left;
  font-weight:700;font-size:10px;letter-spacing:.3px;text-transform:uppercase;
}
.tbl td{
  padding:5px 9px;
  border-bottom:1px solid #e0d8c8;
  color:var(--ink-2);
  vertical-align:top;
}
.tbl td code{
  font-family:"JetBrains Mono",monospace;font-size:10px;
  background:#efe9dd;padding:1px 4px;border-radius:3px;
  color:var(--navy);
}
.tbl tr:last-child td{border-bottom:none;}

/* ---- Callout ---- */
.callout{
  display:flex;gap:10px;align-items:flex-start;
  border-radius:10px;padding:10px 12px;
  font-size:11.5px;line-height:1.5;
}
.callout.warn{background:#fff4e0;border-left:3px solid #ef6c00;color:var(--ink);}
.callout.tip{background:#e8f5ee;border-left:3px solid #1B5E3F;color:var(--ink);}
.callout.danger{background:#ffe5e5;border-left:3px solid #dc2626;color:var(--ink);}
.callout .ico{flex-shrink:0;width:22px;height:22px;margin-top:1px;}
.callout .ico svg{width:22px;height:22px;display:block;}
.callout strong{display:block;font-size:12px;color:var(--ink);margin-bottom:2px;}

/* ---- Pill (small icon row inside full-width card) ---- */
.pill-row{
  display:grid;grid-template-columns:repeat(3,1fr);gap:12px;
}
.pill{
  background:#f7f3e8;border:1px solid rgba(0,0,0,.06);
  border-radius:8px;padding:10px;
  display:flex;gap:10px;align-items:flex-start;
}
.pill .ico{flex-shrink:0;width:36px;height:36px;}
.pill .ico svg{width:36px;height:36px;display:block;}
.pill h4{font-size:12px;color:var(--navy);font-weight:800;text-transform:uppercase;letter-spacing:.3px;margin-bottom:3px;}
.pill p{font-size:11px;color:var(--ink-2);line-height:1.45;margin:0 0 5px 0;}
.pill code{font-family:"JetBrains Mono",monospace;font-size:10px;background:#efe9dd;padding:1px 5px;border-radius:3px;color:var(--navy);}

/* ---- Mini feature column inside full-width card ---- */
.feature-col{
  background:#f7f3e8;border-radius:8px;padding:10px 12px;
  text-align:center;
}
.feature-col .ico{margin:0 auto 6px;width:36px;height:36px;}
.feature-col .ico svg{width:36px;height:36px;display:block;}
.feature-col h4{font-size:11px;color:var(--navy);font-weight:800;text-transform:uppercase;letter-spacing:.3px;margin-bottom:3px;}
.feature-col p{font-size:10.5px;color:var(--ink-2);line-height:1.45;margin:0;}

/* ---- Bottom takeaway banner ---- */
.takeaway{
  display:flex;align-items:center;justify-content:space-around;
  gap:18px;
  background:#15264d;color:#fff;
  border-radius:10px;padding:12px 18px;
  margin-top:14px;
}
.takeaway .item{
  display:flex;align-items:center;gap:10px;
  font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
}
.takeaway .item .ico{width:28px;height:28px;}
.takeaway .item .ico svg{width:28px;height:28px;display:block;}
.takeaway .item .label{display:block;font-size:9.5px;letter-spacing:.8px;color:#bcc8d6;font-weight:600;}
.takeaway .item .text{display:block;font-size:13px;color:#fff;font-weight:800;}

/* ---- Quick reference keywords ---- */
.qref{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;}
.qref .row{
  display:flex;align-items:center;gap:8px;
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:11px;color:var(--ink);
}
.qref .badge{
  flex-shrink:0;width:28px;height:28px;border-radius:50%;
  background:#1B5E3F;color:#fff;
  display:flex;align-items:center;justify-content:center;
  font-size:10px;font-weight:800;
}
.qref .badge.check{
  background:#1B5E3F;
}
.qref .badge.check svg{width:14px;height:14px;display:block;}

/* ---- Number badge ---- */
.nbadge{
  flex-shrink:0;width:30px;height:30px;border-radius:50%;
  display:inline-flex;align-items:center;justify-content:center;
  font-family:"JetBrains Mono",monospace;font-size:11px;font-weight:800;
  color:#fff;
}
.nbadge.green{background:#1B5E3F;}
.nbadge.red{background:#dc2626;}
.nbadge.blue{background:#2563eb;}
.nbadge.gold{background:#d4a017;}
.nbadge.purple{background:#7c3aed;}
.nbadge.navy{background:#15264d;}
.nbadge.teal{background:#0d7377;}

/* ---- Mobile: collapse grids to single column ---- */
@media (max-width: 900px){
  .grid-3,.grid-5,.pill-row,.qref{grid-template-columns:1fr;}
  .grid-2{grid-template-columns:1fr;}
  .takeaway{flex-direction:column;}
}
"""


# ============================================================
# HTML helper builders
# ============================================================

def icon(name: str, size: int = 48) -> str:
    """Return a colorful filled SVG icon by name (from shell_scripting_icons)."""
    return color_icon(name, size)


def terminal(title: str, body_html: str) -> str:
    """Build a terminal block with macOS-style title bar."""
    return (
        f'<div class="terminal">'
        f'<div class="term-bar">'
        f'<span class="term-dot dot-red"></span>'
        f'<span class="term-dot dot-amber"></span>'
        f'<span class="term-dot dot-green"></span>'
        f'<span class="term-title">{title}</span>'
        f'</div>'
        f'<div class="term-body">{body_html}</div>'
        f'</div>'
    )


def card(num: str, head_icon: str, heading: str, body_html: str,
         variant: str = "navy") -> str:
    """Build a .card with header (number + icon + heading) and body."""
    return (
        f'<div class="card head-{variant}">'
        f'<div class="head">'
        f'<span class="num">{num}</span>'
        f'<span class="ico">{icon(head_icon, 18)}</span>'
        f'<span>{heading}</span>'
        f'</div>'
        f'<div class="body-pad">{body_html}</div>'
        f'</div>'
    )


def callout(kind: str, ico: str, title: str, text_html: str) -> str:
    """Build a callout box (warn/tip/danger)."""
    return (
        f'<div class="callout {kind}">'
        f'<span class="ico">{icon(ico, 22)}</span>'
        f'<div><strong>{title}</strong>{text_html}</div>'
        f'</div>'
    )


def page_wrapper(page_num: int, total: int, title: str, subtitle: str,
                 left_icon: str, right_icon: str, body_html: str) -> str:
    """Build a complete self-contained HTML page using the canonical CSS.

    No VERIQTA branding, no social footer. Body has class="multi-page".
    Structure: .page-wrapper > .page > .content
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{CANONICAL_CSS}

{CONTENT_CSS}
</style>
</head>
<body class="multi-page">

<div class="page-wrapper">
  <div class="holes" aria-hidden="true"></div>
  <div class="spiral" aria-hidden="true"></div>
  <div class="page-bend" aria-hidden="true"></div>
  <div class="page">
    <div class="page-top-edge" aria-hidden="true"></div>
    <div class="page-bottom-edge" aria-hidden="true"></div>
    <div class="content">

      <!-- Brand bar -->
      <div class="brand-bar">
        <div class="crumb">{icon('book', 18)} Shell Scripting for DevOps</div>
        <div class="badge">Page {page_num} of {total}</div>
      </div>

      <!-- Title -->
      <div class="page-title">
        <span class="ico">{icon(left_icon, 46)}</span>
        <h1>{title}</h1>
        <span class="ico">{icon(right_icon, 46)}</span>
      </div>
      <div class="page-subtitle">{subtitle}</div>

      <!-- Body -->
      {body_html}

    </div>
  </div>
</div>

</body>
</html>"""


# ============================================================
# PAGE 6 — VARIABLES AND ENVIRONMENT VARIABLES
# Layout: 3-column (top 6 cards in 3x2 grid, full-width env card,
#         then 2-col bottom: script + best practices)
# ============================================================
def body_page_06() -> str:
    # Card 1: Creating Variables
    c1 = card("1", "tag", "Creating Variables",
        '<p>No spaces around <code>=</code> sign.</p>'
        '<div style="margin-top:6px;">' +
        terminal("variables.sh",
            '<span class="cmd">NAME</span>=<span class="str">DevOps</span>\n'
            '<span class="cmd">COUNT</span>=<span class="str">5</span>'
        ) + '</div>',
        variant="green")

    # Card 2: Reading Variables
    c2 = card("2", "play", "Reading Variables",
        '<p>Use <code>$</code> to read a variable.</p>'
        '<div style="margin-top:6px;">' +
        terminal("read.sh",
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$NAME</span>\n'
            '<span class="out">DevOps</span>'
        ) + '</div>',
        variant="blue")

    # Card 3: Quoting Variables
    c3 = card("3", "book", "Quoting Variables",
        '<ul class="bullets">'
        '<li>Use quotes to handle spaces.</li>'
        '<li>Prevents word splitting.</li>'
        '<li>Prevents filename expansion.</li>'
        '</ul>'
        '<div style="margin-top:6px;">' +
        terminal("quote.sh",
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">"$NAME"</span>\n'
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">\'$NAME\'</span>'
        ) + '</div>',
        variant="purple")

    # Card 4: Command Substitution
    c4 = card("4", "cube", "Command Substitution",
        '<p>Store the output of a command.</p>'
        '<div style="margin-top:6px;">' +
        terminal("sub.sh",
            '<span class="prompt">$</span> <span class="cmd">DATE</span>=$(<span class="cmd">date</span> +%Y-%m-%d)\n'
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$DATE</span>\n'
            '<span class="out">2025-05-18</span>'
        ) + '</div>',
        variant="gold")

    # Card 5: Export Variables
    c5 = card("5", "rocket", "Export Variables",
        '<ul class="bullets">'
        '<li>Makes a variable available to child processes.</li>'
        '<li>Use <code>export</code>.</li>'
        '</ul>'
        '<div style="margin-top:6px;">' +
        terminal("export.sh",
            '<span class="prompt">$</span> <span class="cmd">export</span> PROJECT=<span class="str">MyApp</span>\n'
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$PROJECT</span>\n'
            '<span class="out">MyApp</span>'
        ) + '</div>',
        variant="teal")

    # Card 6: Environment Variables
    c6 = card("6", "server", "Environment Variables",
        '<p>Set by the system. Available in every shell.</p>'
        '<div style="margin-top:6px;">' +
        terminal("env.sh",
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$HOME</span>\n'
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$USER</span>\n'
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$SHELL</span>\n'
            '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$LANG</span>'
        ) + '</div>',
        variant="navy")

    # Card 7 (full-width): Common Environment Variables
    env_pills = (
        '<div class="pill-row">'
        '<div class="pill">'
        f'<div class="ico">{icon("folder", 36)}</div>'
        '<div><h4>$HOME</h4><p>Your home directory path.</p>'
        '<code>/home/user</code></div>'
        '</div>'
        '<div class="pill">'
        f'<div class="ico">{icon("user", 36)}</div>'
        '<div><h4>$USER</h4><p>Currently logged-in user.</p>'
        '<code>user</code></div>'
        '</div>'
        '<div class="pill">'
        f'<div class="ico">{icon("terminal", 36)}</div>'
        '<div><h4>$PATH</h4><p>Command search directories.</p>'
        '<code>/usr/bin:/bin</code></div>'
        '</div>'
        '</div>'
    )
    c7 = card("7", "clipboard", "Common Environment Variables", env_pills, variant="navy")

    # Card 8: Using Variables in Scripts
    c8 = card("8", "terminal", "Using Variables in Scripts",
        terminal("app.sh",
            '<span class="comment">#!/bin/bash</span>\n'
            '<span class="cmd">APP_NAME</span>=<span class="str">"MyApp"</span>\n'
            '<span class="cmd">LOG_DIR</span>=<span class="str">"$HOME/logs"</span>\n'
            '<span class="cmd">mkdir</span> -p <span class="str">"$LOG_DIR"</span>\n'
            '<span class="cmd">echo</span> <span class="str">"Starting $APP_NAME..."</span>\n'
            '<span class="cmd">echo</span> <span class="str">"Logs in $LOG_DIR"</span>'
        ),
        variant="green")

    # Card 9: Best Practices (checklist callout)
    c9_body = (
        '<ul class="bullets tick">'
        '<li>Always use quotes when in doubt.</li>'
        '<li>Use meaningful variable names.</li>'
        '<li>Export only what child processes need.</li>'
        '<li>Keep constants uppercase.</li>'
        '<li>Use <code>$( )</code> for command substitution.</li>'
        '<li>Test scripts with different values.</li>'
        '</ul>'
    )
    c9 = card("9", "check-square", "Best Practices", c9_body, variant="green")

    body = (
        '<div class="body">'
        # Row 1: 3 cards (Creating, Reading, Quoting)
        f'<div class="grid-3">{c1}{c2}{c3}</div>'
        # Row 2: 3 cards (Substitution, Export, Environment)
        f'<div class="grid-3" style="margin-top:14px;">{c4}{c5}{c6}</div>'
        # Full-width card 7
        f'<div style="margin-top:14px;">{c7}</div>'
        # Row 3: 2 cards (Script + Best Practices)
        f'<div class="grid-2" style="margin-top:14px;">{c8}{c9}</div>'
        '</div>'
    )
    return body


# ============================================================
# PAGE 7 — EXIT CODES AND COMMAND SUCCESS
# Layout: 3-column (top 6 cards in 3x2 grid, full-width
#         5-column "Preventing Failures" card)
# ============================================================
def body_page_07() -> str:
    # Card 1: What Exit Codes Mean
    c1 = card("1", "question", "What Exit Codes Mean",
        '<p>After any command runs, the system returns a number called an <strong>exit code</strong>. '
        'It tells you if the command succeeded or failed.</p>'
        '<p style="margin-top:6px;"><code>echo $?</code> &mdash; shows the exit code of the last command.</p>',
        variant="blue")

    # Card 2: Basic Exit Code Rules (table)
    c2_body = (
        '<table class="tbl">'
        '<thead><tr><th>Code</th><th>Type</th><th>Meaning</th></tr></thead>'
        '<tbody>'
        '<tr><td><span class="nbadge green">0</span></td><td>Success</td><td>Command completed successfully.</td></tr>'
        '<tr><td><span class="nbadge red">1+</span></td><td>Non-zero</td><td>Failure — check the error.</td></tr>'
        '</tbody>'
        '</table>'
    )
    c2 = card("2", "clipboard", "Basic Exit Code Rules", c2_body, variant="green")

    # Card 3: Examples
    c3 = card("3", "terminal", "Examples",
        '<p style="margin-bottom:6px;">See exit codes in action.</p>'
        + terminal("examples.sh",
            '<span class="prompt">$</span> <span class="cmd">ls</span> /home; <span class="cmd">echo</span> <span class="str">$?</span>\n'
            '<span class="out">0</span>\n\n'
            '<span class="prompt">$</span> <span class="cmd">ls</span> /nope; <span class="cmd">echo</span> <span class="str">$?</span>\n'
            '<span class="out">2</span>\n\n'
            '<span class="prompt">$</span> <span class="cmd">cat</span> file.txt; <span class="cmd">echo</span> <span class="str">$?</span>\n'
            '<span class="out">0 or 1+</span>'
        ),
        variant="purple")

    # Card 4: The exit Command
    c4 = card("4", "lock", "The exit Command",
        '<p>End a script and return a code.</p>'
        '<div style="margin-top:6px;">'
        + terminal("exit-cmd.sh",
            '<span class="kw">if</span> [ ! -f file.txt ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"File not found!"</span>\n'
            '  <span class="cmd">exit</span> 1\n'
            '<span class="kw">fi</span>\n\n'
            '<span class="comment"># exit 0 = success</span>\n'
            '<span class="comment"># exit 1 = failure</span>'
        ) + '</div>',
        variant="gold")

    # Card 5: Testing Command Success
    c5 = card("5", "check-circle", "Testing Command Success",
        '<p>Use exit codes in conditions.</p>'
        '<div style="margin-top:6px;">'
        + terminal("test.sh",
            '<span class="cmd">ls</span> /home\n'
            '<span class="kw">if</span> [ <span class="str">$?</span> -eq 0 ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"Success"</span>\n'
            '<span class="kw">else</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"Failed"</span>\n'
            '<span class="kw">fi</span>'
        ) + '</div>',
        variant="teal")

    # Card 6: Why CI/CD Pipelines Depend on Exit Codes
    c6 = card("6", "rocket", "Why CI/CD Pipelines Depend on Exit Codes",
        '<ul class="bullets tick">'
        '<li>Each step returns an exit code.</li>'
        '<li>CI/CD tools stop the pipeline on failure.</li>'
        '<li>Exit 0 = pipeline continues.</li>'
        '<li>Exit 1+ = pipeline fails.</li>'
        '<li>Ensures reliable, consistent deployments.</li>'
        '</ul>',
        variant="navy")

    # Card 7 (full-width): Preventing Silent Automation Failures (5 columns)
    features = (
        '<div class="grid-5">'
        f'<div class="feature-col"><div class="ico">{icon("shield", 36)}</div>'
        '<h4>Validate</h4><p>Check files & inputs before running.</p></div>'
        f'<div class="feature-col"><div class="ico">{icon("monitor", 36)}</div>'
        '<h4>Log</h4><p>Capture stdout & stderr for diagnosis.</p></div>'
        f'<div class="feature-col"><div class="ico">{icon("folder", 36)}</div>'
        '<h4>Document</h4><p>Track each step in a script log file.</p></div>'
        f'<div class="feature-col"><div class="ico">{icon("warning", 36)}</div>'
        '<h4>Alert</h4><p>Surface non-zero exit codes immediately.</p></div>'
        f'<div class="feature-col"><div class="ico">{icon("gear", 36)}</div>'
        '<h4>Tune</h4><p>Set <code>set -e</code> for fail-fast behavior.</p></div>'
        '</div>'
    )
    c7 = card("7", "shield", "Preventing Silent Automation Failures",
              features, variant="navy")

    # Bottom takeaway banner
    takeaway = (
        '<div class="takeaway">'
        f'<div class="item"><span class="ico">{icon("star", 28)}</span>'
        '<div><span class="label">Tip</span><span class="text">Always check $? after risky commands</span></div></div>'
        f'<div class="item"><span class="ico">{icon("terminal", 28)}</span>'
        '<div><span class="label">Pattern</span><span class="text">set -e + set -o pipefail</span></div></div>'
        '</div>'
    )

    body = (
        '<div class="body">'
        # Row 1: 3 cards
        f'<div class="grid-3">{c1}{c2}{c3}</div>'
        # Row 2: 3 cards
        f'<div class="grid-3" style="margin-top:14px;">{c4}{c5}{c6}</div>'
        # Full-width card 7 (5-column inner)
        f'<div style="margin-top:14px;">{c7}</div>'
        # Takeaway banner
        f'{takeaway}'
        '</div>'
    )
    return body


# ============================================================
# PAGE 8 — CONDITIONAL STATEMENTS
# Layout: 3-column (top 6 cards in 3x2 grid + tip banner)
# ============================================================
def body_page_08() -> str:
    # Card 1: Basic Syntax
    c1 = card("1", "book", "Basic Syntax",
        '<p>The <code>if</code> statement runs code based on a condition.</p>'
        '<div style="margin-top:6px;">'
        + terminal("if.sh",
            '<span class="kw">if</span> [ condition ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"yes"</span>\n'
            '<span class="kw">elif</span> [ other ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"maybe"</span>\n'
            '<span class="kw">else</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"no"</span>\n'
            '<span class="kw">fi</span>'
        ) + '</div>',
        variant="navy")

    # Card 2: Numeric Comparisons (table)
    c2_body = (
        '<table class="tbl">'
        '<thead><tr><th>Op</th><th>Meaning</th><th>Example</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>-eq</code></td><td>Equal</td><td>[ $a -eq 5 ]</td></tr>'
        '<tr><td><code>-ne</code></td><td>Not equal</td><td>[ $a -ne 5 ]</td></tr>'
        '<tr><td><code>-lt</code></td><td>Less than</td><td>[ $a -lt 5 ]</td></tr>'
        '<tr><td><code>-le</code></td><td>Less or equal</td><td>[ $a -le 5 ]</td></tr>'
        '<tr><td><code>-gt</code></td><td>Greater than</td><td>[ $a -gt 5 ]</td></tr>'
        '<tr><td><code>-ge</code></td><td>Greater or equal</td><td>[ $a -ge 5 ]</td></tr>'
        '</tbody>'
        '</table>'
    )
    c2 = card("2", "clipboard", "Numeric Comparisons", c2_body, variant="green")

    # Card 3: String Comparisons
    c3_body = (
        '<table class="tbl" style="margin-bottom:6px;">'
        '<thead><tr><th>Op</th><th>Meaning</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>=</code></td><td>Equal strings</td></tr>'
        '<tr><td><code>!=</code></td><td>Not equal</td></tr>'
        '<tr><td><code>-z</code></td><td>Empty string</td></tr>'
        '<tr><td><code>-n</code></td><td>Non-empty</td></tr>'
        '</tbody>'
        '</table>'
        + '<div class="callout tip" style="padding:6px 8px;margin-top:6px;">'
        f'<span class="ico">{icon("lightbulb", 18)}</span>'
        '<div>Always quote variables: <code>[ "$s" = "y" ]</code></div></div>'
    )
    c3 = card("3", "lightbulb", "String Comparisons", c3_body, variant="purple")

    # Card 4: File Tests
    c4_body = (
        '<table class="tbl">'
        '<thead><tr><th>Flag</th><th>True if</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>-f</code></td><td>File exists & is regular</td></tr>'
        '<tr><td><code>-d</code></td><td>Directory exists</td></tr>'
        '<tr><td><code>-e</code></td><td>Path exists</td></tr>'
        '<tr><td><code>-r</code></td><td>Readable</td></tr>'
        '<tr><td><code>-w</code></td><td>Writable</td></tr>'
        '<tr><td><code>-x</code></td><td>Executable</td></tr>'
        '</tbody>'
        '</table>'
    )
    c4 = card("4", "folder", "File Tests", c4_body, variant="teal")

    # Card 5: Practical Example
    c5 = card("5", "terminal", "Practical Example",
        '<p style="margin-bottom:6px;">Check if a service is running.</p>'
        + terminal("check.sh",
            '<span class="kw">if</span> <span class="cmd">systemctl</span> is-active --quiet nginx; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"nginx up"</span>\n'
            '<span class="kw">else</span>\n'
            '  <span class="cmd">sudo</span> systemctl start nginx\n'
            '<span class="kw">fi</span>'
        ),
        variant="blue")

    # Card 6: Quick Reference
    c6_body = (
        '<div class="qref">'
        '<div class="row"><span class="badge">if</span> starts a block</div>'
        '<div class="row"><span class="badge check">' + icon("check-square", 14) + '</span> use [ ] or [[ ]]</div>'
        '<div class="row"><span class="badge">then</span> body runs if true</div>'
        '<div class="row"><span class="badge check">' + icon("check-square", 14) + '</span> quote variables</div>'
        '<div class="row"><span class="badge">elif</span> else-if chain</div>'
        '<div class="row"><span class="badge check">' + icon("check-square", 14) + '</span> close with fi</div>'
        '<div class="row"><span class="badge">else</span> fallback</div>'
        '<div class="row"><span class="badge check">' + icon("check-square", 14) + '</span> use &amp;&amp; / ||</div>'
        '<div class="row"><span class="badge">fi</span> ends block</div>'
        '<div class="row"><span class="badge check">' + icon("check-square", 14) + '</span> test with -e first</div>'
        '</div>'
    )
    c6 = card("6", "check-square", "Quick Reference", c6_body, variant="green")

    # Bottom takeaway banner
    takeaway = (
        '<div class="takeaway">'
        f'<div class="item"><span class="ico">{icon("star", 28)}</span>'
        '<div><span class="label">Tip</span><span class="text">Prefer [[ ]] for safer tests</span></div></div>'
        f'<div class="item"><span class="ico">{icon("terminal", 28)}</span>'
        '<div><span class="label">Pattern</span><span class="text">[ -f x ] &amp;&amp; echo ok</span></div></div>'
        '</div>'
    )

    body = (
        '<div class="body">'
        # Row 1: 3 cards
        f'<div class="grid-3">{c1}{c2}{c3}</div>'
        # Row 2: 3 cards
        f'<div class="grid-3" style="margin-top:14px;">{c4}{c5}{c6}</div>'
        # Takeaway banner
        f'{takeaway}'
        '</div>'
    )
    return body


# ============================================================
# PAGE 9 — LOGICAL OPERATORS
# Layout: single column centered (max-width 920px)
# Internal sections:
#   - Logical Operators table
#   - Short-Circuit Execution list
#   - AND / OR / NOT condition code blocks (stacked)
#   - Combining Multiple Tests (3 examples stacked)
#   - Building Safer Checks code + checklist
# ============================================================
def body_page_09() -> str:
    # Section 1: Logical Operators table
    s1 = card("1", "clipboard", "Logical Operators",
        '<table class="tbl">'
        '<thead><tr><th>Operator</th><th>Meaning</th><th>Example</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>&amp;&amp;</code></td><td>AND — run next if previous succeeds</td><td>cmd1 &amp;&amp; cmd2</td></tr>'
        '<tr><td><code>||</code></td><td>OR — run next if previous fails</td><td>cmd1 || cmd2</td></tr>'
        '<tr><td><code>!</code></td><td>NOT — invert exit status</td><td>! cmd</td></tr>'
        '</tbody>'
        '</table>',
        variant="navy")

    # Section 2: Short-Circuit Execution (icon list)
    s2 = card("2", "cube", "Short-Circuit Execution",
        '<div class="grid-2" style="gap:8px;">'
        '<div class="row" style="display:flex;gap:8px;align-items:flex-start;">'
        f'<span class="nbadge green" style="background:#1B5E3F;width:26px;height:26px;font-size:11px;">&amp;&amp;</span>'
        '<div style="font-size:11px;color:var(--ink-2);line-height:1.45;">'
        '<strong style="color:var(--ink);">AND</strong> — runs the second command only if the first succeeds (exit 0).</div></div>'
        '<div class="row" style="display:flex;gap:8px;align-items:flex-start;">'
        f'<span class="nbadge blue" style="background:#2563eb;width:26px;height:26px;font-size:11px;">||</span>'
        '<div style="font-size:11px;color:var(--ink-2);line-height:1.45;">'
        '<strong style="color:var(--ink);">OR</strong> — runs the second command only if the first fails (non-zero).</div></div>'
        '<div class="row" style="display:flex;gap:8px;align-items:flex-start;">'
        f'<span class="nbadge red" style="background:#dc2626;width:26px;height:26px;font-size:11px;">!</span>'
        '<div style="font-size:11px;color:var(--ink-2);line-height:1.45;">'
        '<strong style="color:var(--ink);">NOT</strong> — inverts the exit status of a command.</div></div>'
        '<div class="row" style="display:flex;gap:8px;align-items:flex-start;">'
        f'<span class="ico" style="flex-shrink:0;">{icon("lightbulb", 26)}</span>'
        '<div style="font-size:11px;color:var(--ink-2);line-height:1.45;">'
        '<strong style="color:var(--ink);">Efficiency</strong> — shell skips commands that cannot change the result.</div></div>'
        '</div>',
        variant="blue")

    # Sections 3-5: AND, OR, NOT conditions (single column stack)
    s3 = card("3", "check-circle", "AND Conditions",
        '<p>Run a chain only if every step succeeds.</p>'
        '<div style="margin-top:6px;">'
        + terminal("and.sh",
            '<span class="cmd">mkdir</span> build <span class="kw">&amp;&amp;</span> <span class="cmd">cd</span> build <span class="kw">&amp;&amp;</span> <span class="cmd">make</span>\n'
            '<span class="comment"># only proceeds if each step returns 0</span>'
        ) + '</div>'
        '<div style="margin-top:6px;">' + callout("tip", "check-circle", "OK",
            '<span style="font-size:11px;">All three commands ran successfully.</span>') + '</div>',
        variant="green")

    s4 = card("4", "check-circle", "OR Conditions",
        '<p>Provide a fallback when the first command fails.</p>'
        '<div style="margin-top:6px;">'
        + terminal("or.sh",
            '<span class="cmd">cat</span> config.cfg <span class="kw">||</span> <span class="cmd">echo</span> <span class="str">"missing config"</span>\n'
            '<span class="comment"># prints fallback if cat fails</span>'
        ) + '</div>'
        '<div style="margin-top:6px;">' + callout("tip", "check-circle", "OK",
            '<span style="font-size:11px;">Reads file or reports missing.</span>') + '</div>',
        variant="blue")

    s5 = card("5", "check-circle", "NOT Condition",
        '<p>Invert a test result (useful in <code>if</code> blocks).</p>'
        '<div style="margin-top:6px;">'
        + terminal("not.sh",
            '<span class="kw">if</span> [ ! -f /tmp/lock ]; <span class="kw">then</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"lock absent — proceed"</span>\n'
            '<span class="kw">fi</span>'
        ) + '</div>'
        '<div style="margin-top:6px;">' + callout("tip", "check-circle", "OK",
            '<span style="font-size:11px;">Proceeds only when lock is absent.</span>') + '</div>',
        variant="purple")

    # Section 6: Combining Multiple Tests
    s6_intro = card("6", "book", "Combining Multiple Tests",
        '<p>Stack operators for richer logic. Examples 1, 2, and 3 below.</p>',
        variant="gold")

    s6_examples = (
        '<div class="grid-2" style="margin-top:0;">'
        + card("", "check-circle", "Example 1 — File exists & readable",
            terminal("ex1.sh",
                '<span class="kw">if</span> [ -f app.conf ] &amp;&amp; [ -r app.conf ]; <span class="kw">then</span>\n'
                '  <span class="cmd">echo</span> <span class="str">"config OK"</span>\n'
                '<span class="kw">fi</span>'
            ), variant="green")
        + card("", "check-circle", "Example 2 — Ping or fallback",
            terminal("ex2.sh",
                '<span class="cmd">ping</span> -c1 host <span class="kw">||</span> <span class="cmd">echo</span> <span class="str">"down"</span>'
            ), variant="blue")
        + '</div>'
        '<div class="grid-2" style="margin-top:14px;">'
        + card("", "check-circle", "Example 3 — Both required",
            terminal("ex3.sh",
                '<span class="cmd">[ -d logs ]</span> <span class="kw">&amp;&amp;</span> <span class="cmd">[ -w logs ]</span> <span class="kw">||</span> <span class="cmd">exit</span> 1'
            ), variant="purple")
        + card("", "shield", "Safe Deployment",
            '<ul class="bullets tick">'
            '<li>Verify preconditions.</li>'
            '<li>Capture every failure.</li>'
            '<li>Provide meaningful fallbacks.</li>'
            '<li>Use <code>set -e</code> for safety.</li>'
            '</ul>'
            + '<div style="margin-top:8px;">' + callout("danger", "shield", "Safe Deployment",
                '<span style="font-size:11px;">Always validate inputs and exit codes before acting on results.</span>') + '</div>',
            variant="navy")
        + '</div>'
    )

    # Section 7: Building Safer Checks
    s7 = card("7", "shield", "Building Safer Checks",
        '<p style="margin-bottom:6px;">Combine operators with explicit tests for robust scripts.</p>'
        + terminal("safe.sh",
            '<span class="comment">#!/bin/bash</span>\n'
            '<span class="cmd">set</span> -e\n'
            '<span class="cmd">[ -f /etc/app.conf ]</span> <span class="kw">&amp;&amp;</span> <span class="cmd">source</span> /etc/app.conf <span class="kw">||</span> <span class="cmd">exit</span> 1\n'
            '<span class="cmd">[ -n <span class="str">"$APP_KEY"</span> ]</span> <span class="kw">||</span> { <span class="cmd">echo</span> <span class="str">"missing APP_KEY"</span>; <span class="cmd">exit</span> 2; }\n'
            '<span class="cmd">deploy</span> <span class="str">"$APP_KEY"</span>'
        ),
        variant="navy")

    # Bottom takeaway banner
    takeaway = (
        '<div class="takeaway">'
        f'<div class="item"><span class="ico">{icon("star", 28)}</span>'
        '<div><span class="label">Tip</span><span class="text">Short-circuit keeps scripts lean</span></div></div>'
        f'<div class="item"><span class="ico">{icon("terminal", 28)}</span>'
        '<div><span class="label">Pattern</span><span class="text">cmd &amp;&amp; ok || fail</span></div></div>'
        f'<div class="item"><span class="ico">{icon("shield", 28)}</span>'
        '<div><span class="label">Safety</span><span class="text">Validate then act</span></div></div>'
        '</div>'
    )

    body = (
        '<div class="body">'
        '<div class="single">'
        # Sections 1 & 2 side-by-side
        f'<div class="grid-2">{s1}{s2}</div>'
        # Sections 3, 4, 5 stacked (single column)
        f'<div style="margin-top:14px;">{s3}</div>'
        f'<div style="margin-top:14px;">{s4}</div>'
        f'<div style="margin-top:14px;">{s5}</div>'
        # Section 6 intro + examples
        f'<div style="margin-top:14px;">{s6_intro}</div>'
        f'<div style="margin-top:14px;">{s6_examples}</div>'
        # Section 7
        f'<div style="margin-top:14px;">{s7}</div>'
        # Takeaway
        f'{takeaway}'
        '</div>'
        '</div>'
    )
    return body


# ============================================================
# PAGE 10 — LOOPS FOR AUTOMATION
# Layout: 2-column grid (8 cards in 4 rows × 2 cols + takeaway banner)
# ============================================================
def body_page_10() -> str:
    # Card 1: For Loops
    c1 = card("1", "play", "For Loops",
        '<p>Iterate over a list or range.</p>'
        '<div style="margin-top:6px;">'
        + terminal("for.sh",
            '<span class="kw">for</span> i <span class="kw">in</span> 1 2 3; <span class="kw">do</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"Item $i"</span>\n'
            '<span class="kw">done</span>'
        ) + '</div>',
        variant="green")

    # Card 2: While Loops
    c2 = card("2", "cube", "While Loops",
        '<p>Repeat while a condition is true.</p>'
        '<div style="margin-top:6px;">'
        + terminal("while.sh",
            '<span class="cmd">n=0</span>\n'
            '<span class="kw">while</span> [ $n -lt 3 ]; <span class="kw">do</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"n=$n"</span>\n'
            '  <span class="cmd">n=$((n+1))</span>\n'
            '<span class="kw">done</span>'
        ) + '</div>',
        variant="blue")

    # Card 3: Looping Through Files
    c3 = card("3", "folder", "Looping Through Files",
        '<p>Process every file in a directory.</p>'
        '<div style="margin-top:6px;">'
        + terminal("files.sh",
            '<span class="kw">for</span> f <span class="kw">in</span> /etc/*.conf; <span class="kw">do</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"$f"</span>\n'
            '<span class="kw">done</span>'
        ) + '</div>',
        variant="teal")

    # Card 4: Looping Through Servers
    c4 = card("4", "server", "Looping Through Servers",
        '<p>Run a command on each host.</p>'
        '<div style="margin-top:6px;">'
        + terminal("hosts.sh",
            '<span class="kw">for</span> h <span class="kw">in</span> web1 web2 web3; <span class="kw">do</span>\n'
            '  <span class="cmd">ssh</span> $h <span class="str">"uptime"</span>\n'
            '<span class="kw">done</span>'
        ) + '</div>',
        variant="purple")

    # Card 5: Break
    c5 = card("5", "stop", "Break",
        '<p>Exit the loop early when a condition is met.</p>'
        '<div style="margin-top:6px;">'
        + terminal("break.sh",
            '<span class="kw">for</span> i <span class="kw">in</span> 1 2 3 4 5; <span class="kw">do</span>\n'
            '  <span class="kw">if</span> [ $i -eq 3 ]; <span class="kw">then</span> <span class="cmd">break</span>; <span class="kw">fi</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"$i"</span>\n'
            '<span class="kw">done</span>\n'
            '<span class="out">1\n2</span>'
        ) + '</div>',
        variant="red")

    # Card 6: Continue
    c6 = card("6", "rocket", "Continue",
        '<p>Skip the current iteration and continue with the next.</p>'
        '<div style="margin-top:6px;">'
        + terminal("continue.sh",
            '<span class="kw">for</span> i <span class="kw">in</span> 1 2 3 4 5; <span class="kw">do</span>\n'
            '  <span class="kw">if</span> [ $((i%2)) -eq 0 ]; <span class="kw">then</span> <span class="cmd">continue</span>; <span class="kw">fi</span>\n'
            '  <span class="cmd">echo</span> <span class="str">"$i"</span>\n'
            '<span class="kw">done</span>\n'
            '<span class="out">1\n3\n5</span>'
        ) + '</div>',
        variant="gold")

    # Card 7: Avoiding Infinite Loops
    c7 = card("7", "warning", "Avoiding Infinite Loops",
        '<ul class="bullets warn">'
        '<li>Always increment or decrement the counter.</li>'
        '<li>Use <code>break</code> for an explicit exit.</li>'
        '<li>Set a maximum iteration cap.</li>'
        '<li>Use <code>set -e</code> to abort on errors.</li>'
        '</ul>'
        '<div style="margin-top:6px;">'
        + callout("danger", "warning", "Risk",
            '<span style="font-size:11px;">A forgotten counter hangs the script forever.</span>')
        + '</div>',
        variant="red")

    # Card 8: Automating Repetitive Tasks
    c8 = card("8", "check-square", "Automating Repetitive Tasks",
        '<ul class="bullets tick">'
        '<li>Back up logs nightly.</li>'
        '<li>Rotate files older than 7 days.</li>'
        '<li>Poll a service until ready.</li>'
        '<li>Run health checks across hosts.</li>'
        '<li>Process CSV rows one by one.</li>'
        '<li>Apply config to multiple nodes.</li>'
        '</ul>',
        variant="green")

    # Bottom takeaway banner
    takeaway = (
        '<div class="takeaway">'
        f'<div class="item"><span class="ico">{icon("lightbulb", 28)}</span>'
        '<div><span class="label">Key Takeaway</span><span class="text">Automate, do not repeat</span></div></div>'
        f'<div class="item"><span class="ico">{icon("branch", 28)}</span>'
        '<div><span class="label">Repeat</span><span class="text">Smarter every day</span></div></div>'
        f'<div class="item"><span class="ico">{icon("clock", 28)}</span>'
        '<div><span class="label">Save Time</span><span class="text">Every single day</span></div></div>'
        '</div>'
    )

    body = (
        '<div class="body">'
        # 4 rows × 2 cols
        f'<div class="grid-2">{c1}{c2}</div>'
        f'<div class="grid-2" style="margin-top:14px;">{c3}{c4}</div>'
        f'<div class="grid-2" style="margin-top:14px;">{c5}{c6}</div>'
        f'<div class="grid-2" style="margin-top:14px;">{c7}{c8}</div>'
        # Takeaway
        f'{takeaway}'
        '</div>'
    )
    return body


# ============================================================
# MAIN — write all 5 pages
# ============================================================

def main():
    pages = [
        # (page_num, total, title, subtitle, left_icon, right_icon, body_fn)
        (6, 20,
         "4. VARIABLES & ENVIRONMENT VARIABLES",
         "STORE DATA. REUSE. AUTOMATE.",
         "terminal", "dollar", body_page_06),
        (7, 20,
         "6. EXIT CODES & COMMAND SUCCESS",
         "EVERY COMMAND RETURNS A STATUS.",
         "terminal", "check-circle", body_page_07),
        (8, 20,
         "7. CONDITIONAL STATEMENTS",
         "IF. THEN. ELSE. ELIF.",
         "terminal", "shield", body_page_08),
        (9, 20,
         "8. LOGICAL OPERATORS",
         "COMBINE COMMANDS. CONTROL FLOW.",
         "terminal", "network", body_page_09),
        (10, 20,
         "9. LOOPS FOR AUTOMATION",
         "REPEAT TASKS. SAVE TIME. ELIMINATE MANUAL WORK.",
         "rocket", "gear", body_page_10),
    ]

    written = []
    for page_num, total, title, subtitle, licon, ricon, body_fn in pages:
        body_html = body_fn()
        html = page_wrapper(page_num, total, title, subtitle, licon, ricon, body_html)
        out_path = os.path.join(OUTPUT_DIR, f"recreated-page-{page_num:02d}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        written.append((out_path, len(html)))
        print(f"  wrote {out_path} ({len(html)} bytes)")

    print()
    print(f"Wrote {len(written)} pages.")
    print("Pages:")
    for path, size in written:
        print(f"  {path}  ({size} bytes)")


if __name__ == "__main__":
    main()
