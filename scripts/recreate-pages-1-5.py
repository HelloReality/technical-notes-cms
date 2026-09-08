#!/usr/bin/env python3
"""
Recreate carousel pages 1-5 of the Shell Scripting for DevOps handbook
as individual self-contained HTML files.

Uses the shared notebook template (NOTEBOOK_CSS, ICONS, page_wrapper)
from build_shell_scripting_template.py.

Each output HTML file is fully self-contained (inline CSS + inline SVG).
"""

import os
import sys

# Ensure we can import the template module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from build_shell_scripting_template import (
    NOTEBOOK_CSS, ICONS, icon, page_wrapper
)

OUT_DIR = "/home/z/my-project/downloads/instagram-DcaW1UljsVk"

# ============================================================
# Helper builders
# ============================================================

def terminal(title, lines):
    """Build a terminal block. `lines` is a list of (cls, text) tuples.
    cls ∈ {'prompt','comment','cmd','str','out',''} (empty = plain fg).
    """
    dots = ('<span class="term-dot dot-red"></span>'
            '<span class="term-dot dot-amber"></span>'
            '<span class="term-dot dot-green"></span>')
    body = "\n".join(
        f'<div class="{cls}">{txt}</div>' if cls else f'<div>{txt}</div>'
        for cls, txt in lines
    )
    return f"""<div class="terminal">
  <div class="term-bar">{dots}<span class="term-title">{title}</span></div>
  <div class="term-body">{body}</div>
</div>"""


def table(headers, rows, header_classes=None):
    """Build a .tbl table. `rows` is a list of lists/tuples of strings."""
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = []
    for r in rows:
        tds = "".join(f"<td>{c}</td>" for c in r)
        trs.append(f"<tr>{tds}</tr>")
    return f"""<table class="tbl"><thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table>"""


def row(icon_name, heading, text_html, icon_bg="bg-green", icon_cls="ic-green"):
    """Build a single .row item."""
    return f"""<div class="row">
  <div class="icon {icon_bg} {icon_cls}">{icon(icon_name)}</div>
  <div class="text"><h3>{heading}</h3><p>{text_html}</p></div>
</div>"""


def card(head_text, head_icon, body_html):
    """Build a sidebar card."""
    return f"""<div class="card">
  <div class="head">{icon(head_icon) if head_icon else ''}<span>{head_text}</span></div>
  <div class="body-pad">{body_html}</div>
</div>"""


def callout(kind, ico_name, text_html):
    """Build a callout (warn or tip)."""
    return f"""<div class="callout {kind}">
  <span class="ico ic-{ 'orange' if kind=='warn' else 'green'}">{icon(ico_name)}</span>
  <div>{text_html}</div>
</div>"""


# ============================================================
# PAGE 1 — COVER
# ============================================================

# Custom cover CSS injected via <style> in the body
COVER_CSS = """
<style>
  /* Cover-specific overrides */
  .cover-page .page-title,
  .cover-page .page-subtitle{ display:none; }
  .cover-wrap{ display:flex; flex-direction:column; align-items:center; gap:14px; padding:8px 0 6px; }
  .cover-tagline{
    display:inline-block; border:2px solid var(--green); color:var(--green);
    background:#fff; padding:6px 22px; border-radius:999px;
    font-size:14px; font-weight:700; letter-spacing:2px; text-transform:uppercase;
  }
  .cover-title{
    font-size:84px; font-weight:900; color:var(--green); line-height:0.95;
    text-align:center; letter-spacing:-2px; text-transform:uppercase;
    position:relative;
  }
  .cover-title .small{ font-size:54px; }
  .cover-title .for-line{
    display:flex; align-items:center; justify-content:center; gap:18px;
    font-size:48px; font-weight:900; color:var(--green); margin:6px 0;
  }
  .cover-title .for-line .ln{ flex:0 0 100px; height:3px; background:var(--green); border-radius:2px;}
  .ribbon{
    position:relative; display:inline-block; background:var(--green); color:#fff;
    font-size:34px; font-weight:900; padding:6px 36px; letter-spacing:4px;
    text-transform:uppercase; margin-top:-4px;
  }
  .ribbon::before, .ribbon::after{
    content:""; position:absolute; top:0; width:0; height:0;
    border-top:26px solid var(--green); border-bottom:26px solid var(--green);
  }
  .ribbon::before{ left:-22px; border-left:22px solid transparent; }
  .ribbon::after{ right:-22px; border-right:22px solid transparent; }

  .cover-mid{
    display:flex; align-items:center; justify-content:center; gap:32px; margin:8px 0;
  }
  .cover-mid .iconbox{
    width:84px; height:84px; border-radius:18px; background:var(--green-light);
    display:flex; align-items:center; justify-content:center; color:var(--green);
  }
  .cover-mid .iconbox svg{ width:48px; height:48px; }
  .cover-mid .terminal-card{
    width:300px; background:var(--terminal-bg); border-radius:14px; overflow:hidden;
    box-shadow:0 10px 30px rgba(0,0,0,.25);
  }
  .cover-mid .terminal-card .tbar{
    background:#1c2230; padding:10px 14px; display:flex; gap:6px;
  }
  .cover-mid .terminal-card .tbar i{
    width:11px; height:11px; border-radius:50%; display:inline-block;
  }
  .cover-mid .terminal-card .tbody{
    padding:30px 18px; font-family:"JetBrains Mono",monospace;
    color:var(--terminal-green); font-size:38px; font-weight:700; text-align:center;
  }
  .cover-checklist{
    display:flex; flex-direction:column; gap:8px; align-items:flex-start;
  }
  .cover-checklist .ci{
    display:flex; align-items:center; gap:10px;
    font-size:20px; font-weight:800; color:var(--green);
    letter-spacing:1.5px; text-transform:uppercase;
  }
  .cover-checklist .ci .ck{
    width:30px; height:30px; border-radius:50%; background:var(--green);
    color:#fff; display:flex; align-items:center; justify-content:center;
  }
  .cover-checklist .ci .ck svg{ width:18px; height:18px; }

  .feature-bar{
    display:grid; grid-template-columns:repeat(4,1fr); gap:0;
    background:#fff; border:2px solid var(--green); border-radius:12px;
    overflow:hidden; margin-top:4px;
  }
  .feature-bar .fcell{
    padding:14px 12px; text-align:center; border-right:1px solid var(--green-light);
    display:flex; flex-direction:column; align-items:center; gap:6px;
  }
  .feature-bar .fcell:last-child{ border-right:none; }
  .feature-bar .fcell .fi{
    width:36px; height:36px; border-radius:9px; background:var(--green-light);
    color:var(--green); display:flex; align-items:center; justify-content:center;
  }
  .feature-bar .fcell .fi svg{ width:22px; height:22px; }
  .feature-bar .fcell .ft{
    font-size:11px; font-weight:800; color:var(--green); letter-spacing:.5px;
    text-transform:uppercase; line-height:1.2;
  }
</style>
"""

def page1_body():
    body = COVER_CSS + """
<div class="cover-wrap">
  <div class="cover-title">
    SHELL<br>
    SCRIPTING<br>
    <span class="for-line"><span class="ln"></span>FOR<span class="ln"></span></span>
    DEVOPS<br>
    <span class="ribbon">HANDBOOK</span>
  </div>

  <div class="cover-tagline">FOR COMPLETE BEGINNERS</div>

  <div class="cover-mid">
    <div class="iconbox">""" + icon("lightbulb") + """</div>
    <div class="iconbox">""" + icon("gear") + """</div>
    <div class="terminal-card">
      <div class="tbar"><i style="background:#ff5f56;"></i><i style="background:#ffbd2e;"></i><i style="background:#27c93f;"></i></div>
      <div class="tbody">&gt;_</div>
    </div>
    <div class="cover-checklist">
      <div class="ci"><span class="ck">""" + icon("check") + """</span>LEARN</div>
      <div class="ci"><span class="ck">""" + icon("check") + """</span>PRACTICE</div>
      <div class="ci"><span class="ck">""" + icon("check") + """</span>AUTOMATE</div>
      <div class="ci"><span class="ck">""" + icon("check") + """</span>DEPLOY</div>
    </div>
    <div class="iconbox">""" + icon("globe") + """</div>
  </div>

  <div class="feature-bar">
    <div class="fcell"><div class="fi">""" + icon("book") + """</div><div class="ft">Step-by-step<br>Explanations</div></div>
    <div class="fcell"><div class="fi">""" + icon("play") + """</div><div class="ft">Practical<br>Examples</div></div>
    <div class="fcell"><div class="fi">""" + icon("rocket") + """</div><div class="ft">DevOps<br>Use Cases</div></div>
    <div class="fcell"><div class="fi">""" + icon("users") + """</div><div class="ft">Beginner<br>Friendly</div></div>
  </div>
</div>
"""
    # page_wrapper wraps the body inside .content but we want the cover styling
    # We add the .cover-page class to the page-wrapper via a small wrapper div
    # Use empty title — the cover-title replaces it
    return body


# ============================================================
# PAGE 2 — "1. WHAT IS SHELL SCRIPTING?"
# ============================================================

def page2_body():
    p2_css = """
<style>
  .p2-flow{display:flex; align-items:center; gap:6px; margin-top:6px; flex-wrap:wrap; justify-content:center;}
  .p2-flow .node{
    background:var(--green-light); border:2px solid var(--green); color:var(--green);
    padding:5px 10px; border-radius:6px; font-size:10px; font-weight:800; letter-spacing:.3px;
    text-transform:uppercase; display:flex; align-items:center; gap:4px;
  }
  .p2-flow .node svg{width:14px;height:14px;}
  .p2-flow .arr{color:var(--green); font-weight:800; font-size:14px;}
  .p2-script{
    background:var(--terminal-bg); border-radius:8px; overflow:hidden;
    box-shadow:0 4px 14px rgba(0,0,0,.2);
  }
  .p2-script .sb{padding:8px 10px; font-family:"JetBrains Mono","Fira Code",monospace; font-size:11px; line-height:1.7;}
  .p2-script .ln-row{display:flex; gap:8px; align-items:flex-start;}
  .p2-script .ln-num{
    flex-shrink:0; width:18px; height:18px; border-radius:50%; background:var(--green);
    color:#fff; font-size:9px; font-weight:800; display:flex; align-items:center; justify-content:center;
    font-family:monospace;
  }
  .p2-script .ln-code{color:var(--terminal-fg); flex:1; word-break:break-all;}
  .p2-script .ln-code .comment{color:var(--terminal-dim);}
  .p2-script .ln-code .cmd{color:var(--terminal-blue);}
  .p2-script .ln-code .str{color:var(--terminal-amber);}
  .p2-script .ln-code .arr{color:var(--terminal-amber); margin:0 4px;}
  .p2-script .ln-code .ex{color:var(--terminal-fg); opacity:.85; font-size:10.5px;}
  .p2-safe{display:flex; flex-direction:column; gap:6px;}
  .p2-safe .ss{display:flex; gap:8px; align-items:flex-start; padding:4px 0; border-bottom:1px solid #ece6d3;}
  .p2-safe .ss:last-child{border-bottom:none;}
  .p2-safe .ss .si{width:28px; height:28px; flex-shrink:0; border-radius:7px; background:var(--green-light); color:var(--green); display:flex; align-items:center; justify-content:center;}
  .p2-safe .ss .si svg{width:16px; height:16px;}
  .p2-safe .ss .st{flex:1; font-size:11px; color:var(--ink-2); line-height:1.4;}
  .p2-safe .ss .st b{color:var(--green); text-transform:uppercase; font-size:10.5px; letter-spacing:.3px;}
  .p2-checks li::before{content:"✓"; color:var(--green); font-weight:800;}
</style>
"""
    # Left column rows
    rows_left = []
    rows_left.append(
        """<div class="row">
  <div class="icon bg-green ic-green">""" + icon("terminal") + """</div>
  <div class="text">
    <h3>SHELL VS TERMINAL VS BASH</h3>
    <p><b>TERMINAL:</b> The application you open — a text interface to interact with the computer.<br>
    <b>SHELL:</b> The program that interprets your commands and talks to the OS.<br>
    <b>BASH:</b> "Bourne Again SHell" — the most common Linux shell; a command language and scripting interpreter.</p>
  </div>
</div>"""
    )
    rows_left.append(
        """<div class="row">
  <div class="icon bg-blue ic-blue">""" + icon("gear") + """</div>
  <div class="text">
    <h3>WHAT A SHELL ACTUALLY DOES</h3>
    <p>1. Reads your command.<br>
    2. Parses (understands) the command.<br>
    3. Expands variables, wildcards, paths.<br>
    4. Executes the command or program.<br>
    5. Returns the output and exit status.<br>
    6. Waits for the next command.</p>
    <div class="p2-flow">
      <span class="node">""" + icon("users") + """User</span>
      <span class="arr">→</span>
      <span class="node">""" + icon("terminal") + """Shell</span>
      <span class="arr">→</span>
      <span class="node">""" + icon("server") + """Kernel</span>
      <span class="arr">→</span>
      <span class="node">""" + icon("play") + """Output</span>
    </div>
  </div>
</div>"""
    )
    rows_left.append(
        """<div class="row">
  <div class="icon bg-purple ic-purple">""" + icon("arrow-right") + """</div>
  <div class="text">
    <h3>COMMAND EXECUTION FLOW</h3>
    <div class="p2-flow">
      <span class="node">You type a command</span>
      <span class="arr">→</span>
      <span class="node">Shell interprets it</span>
      <span class="arr">→</span>
      <span class="node">Kernel executes it</span>
      <span class="arr">→</span>
      <span class="node">Output + Exit status</span>
    </div>
  </div>
</div>"""
    )
    rows_left.append(
        """<div class="row">
  <div class="icon bg-gold ic-gold">""" + icon("rocket") + """</div>
  <div class="text">
    <h3>WHY DEVOPS ENGINEERS AUTOMATE WITH SCRIPTS</h3>
    <ul class="p2-checks" style="list-style:none; padding:0; margin:0;">
      <li style="padding-left:14px; position:relative;">Save time and reduce manual work.</li>
      <li style="padding-left:14px; position:relative;">Eliminate human errors.</li>
      <li style="padding-left:14px; position:relative;">Ensure repeatability and consistency.</li>
      <li style="padding-left:14px; position:relative;">Scale operations easily.</li>
      <li style="padding-left:14px; position:relative;">Automate deployments, monitoring, backups, and more.</li>
      <li style="padding-left:14px; position:relative;">Integrate with CI/CD pipelines.</li>
      <li style="padding-left:14px; position:relative;">Improve reliability and speed.</li>
    </ul>
  </div>
</div>"""
    )

    # "YOUR FIRST BASH SCRIPT" — numbered line-by-line annotated layout
    first_script = """
<div class="row" style="align-items:flex-start; display:block;">
  <div style="display:flex; gap:12px; align-items:center; margin-bottom:6px;">
    <div class="icon bg-teal ic-teal" style="width:42px; height:42px;">""" + icon("file") + """</div>
    <h3 style="font-size:13px; font-weight:700; color:var(--green); text-transform:uppercase; letter-spacing:.3px; margin:0;">YOUR FIRST BASH SCRIPT</h3>
  </div>
  <div class="p2-script">
    <div class="sb">
      <div class="ln-row">
        <span class="ln-num">1</span>
        <span class="ln-code"><span class="comment">#!/bin/bash</span> <span class="arr">→</span> <span class="ex">Shebang: tells the system to use Bash</span></span>
      </div>
      <div class="ln-row">
        <span class="ln-num">2</span>
        <span class="ln-code"><span class="comment"># This is my first script</span> <span class="arr">→</span> <span class="ex">Comment: ignored by the shell</span></span>
      </div>
      <div class="ln-row">
        <span class="ln-num">3</span>
        <span class="ln-code"><span class="cmd">echo</span> <span class="str">"Hello, DevOps Engineer!"</span> <span class="arr">→</span> <span class="ex">Prints a message to the screen</span></span>
      </div>
      <div class="ln-row">
        <span class="ln-num">4</span>
        <span class="ln-code"><span class="cmd">DATE=$(date)</span> <span class="arr">→</span> <span class="ex">Stores the current date in a variable</span></span>
      </div>
      <div class="ln-row">
        <span class="ln-num">5</span>
        <span class="ln-code"><span class="cmd">echo</span> <span class="str">"Today is: $DATE"</span> <span class="arr">→</span> <span class="ex">Prints the date</span></span>
      </div>
    </div>
  </div>
</div>
"""

    # Interactive vs Scripts comparison
    compare_html = """
<div class="compare">
  <div class="col left">
    <h4>Interactive Commands</h4>
    <ul>
      <li>You type and run one command at a time.</li>
      <li>Used for ad-hoc tasks.</li>
      <li>Hard to repeat.</li>
      <li>Not version controlled.</li>
      <li>Easy to forget commands.</li>
    </ul>
  </div>
  <div class="col right">
    <h4>Scripts</h4>
    <ul>
      <li>You write commands in a file and run them.</li>
      <li>Used for automation.</li>
      <li>Repeatable and consistent.</li>
      <li>Version controlled (Git).</li>
      <li>Easy to share and reuse.</li>
    </ul>
  </div>
</div>
"""

    # Running a script safely — with specific icons per step
    safe_steps = """
<div class="p2-safe">
  <div class="ss">
    <span class="si">""" + icon("file") + """</span>
    <div class="st"><b>1. CREATE THE FILE</b><br><code class="inline">nano myscript.sh</code></div>
  </div>
  <div class="ss">
    <span class="si">""" + icon("check") + """</span>
    <div class="st"><b>2. SAVE AND EXIT</b><br><code class="inline">CTRL + O, ENTER, CTRL + X</code></div>
  </div>
  <div class="ss">
    <span class="si">""" + icon("key") + """</span>
    <div class="st"><b>3. MAKE IT EXECUTABLE</b><br><code class="inline">chmod +x myscript.sh</code></div>
  </div>
  <div class="ss">
    <span class="si">""" + icon("play") + """</span>
    <div class="st"><b>4. RUN THE SCRIPT</b><br><code class="inline">./myscript.sh</code></div>
  </div>
  <div class="ss">
    <span class="si">""" + icon("shield") + """</span>
    <div class="st"><b>5. BEST PRACTICES</b> — Review your script before running · Use full paths for important commands · Test in a safe environment first.</div>
  </div>
</div>
"""

    important_note = callout(
        "tip", "lightbulb",
        "<b>IMPORTANT NOTE:</b> A script has the same power as the user who runs it. "
        "Always review scripts before executing, especially scripts from the internet."
    )

    body_html = p2_css + f"""
<div class="body">
  <div class="rows">
    {"".join(rows_left)}
    {first_script}
  </div>
  <div class="sidebar">
    {card("Interactive Commands vs Scripts", "list", compare_html)}
    {card("Running a Script Safely", "play", safe_steps)}
    {important_note}
  </div>
</div>
"""
    return body_html


# ============================================================
# PAGE 3 — "3. CREATING AND RUNNING SHELL SCRIPTS"
# ============================================================

def page3_body():
    # Three-column grid layout. Use a custom grid CSS via inline style.
    grid_css = """
<style>
  .p3-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:14px;}
  .p3-grid .col-card{
    background:#fff; border-radius:10px; overflow:hidden;
    box-shadow:0 2px 8px rgba(0,0,0,.06); border:1px solid rgba(0,0,0,.05);
    display:flex; flex-direction:column;
  }
  .p3-grid .col-card .h{
    background:var(--green); color:#fff; padding:7px 12px;
    font-size:11px; font-weight:700; letter-spacing:.4px; text-transform:uppercase;
    display:flex; align-items:center; gap:6px;
  }
  .p3-grid .col-card .h svg{width:14px;height:14px;}
  .p3-grid .col-card .b{padding:10px 12px; font-size:11px; color:var(--ink-2); line-height:1.5;}
  .p3-grid .col-card .b ul{list-style:none; padding:0; margin:0 0 6px;}
  .p3-grid .col-card .b li{padding-left:14px; position:relative; margin-bottom:3px;}
  .p3-grid .col-card .b li::before{content:"•"; position:absolute; left:0; color:var(--green); font-weight:800;}
  .p3-grid .col-card .ex{font-size:10px; color:var(--ink-3); text-transform:uppercase; letter-spacing:.3px; margin:4px 0 2px;}
  .p3-grid .col-card .code{
    background:var(--terminal-bg); color:var(--terminal-fg);
    border-radius:6px; padding:6px 9px; font-family:"JetBrains Mono",monospace;
    font-size:11px; margin-bottom:6px;
  }
  .p3-grid .col-card .note{
    background:var(--green-light); border-left:3px solid var(--green);
    padding:5px 9px; font-size:11px; border-radius:5px; margin-top:4px;
  }
  .p3-tip{background:var(--green-light); border-left:3px solid var(--green); padding:5px 9px; border-radius:5px; font-size:10.5px;}
  .p3-method{font-size:10.5px; font-weight:700; color:var(--green); text-transform:uppercase; letter-spacing:.3px; margin:4px 0 2px;}
  .p3-perm-diag{
    display:flex; gap:6px; justify-content:space-around; margin:6px 0;
    font-size:10px; font-weight:700; color:var(--green);
  }
  .p3-perm-diag .seg{
    flex:1; text-align:center; background:var(--green-light); border-radius:5px; padding:4px;
  }
  .p3-perm-diag .seg .l{font-size:9px; color:var(--ink-3); display:block; font-weight:600;}
  .p3-fix{
    background:#fff4e0; border-left:3px solid var(--orange); border-radius:6px;
    padding:6px 9px; margin-top:6px; font-size:11px;
    display:flex; gap:8px; align-items:flex-start;
  }
  .p3-fix .fxi{width:20px; height:20px; flex-shrink:0; color:var(--orange); display:flex; align-items:center; justify-content:center;}
  .p3-fix .fxi svg{width:14px; height:14px;}
  .p3-fix .fx-c{flex:1;}
  .p3-fix b{color:var(--orange); text-transform:uppercase; font-size:10px;}
  .p3-remember{
    background:var(--blue-soft); border-left:3px solid var(--blue); border-radius:6px;
    padding:6px 10px; margin-top:10px; font-size:11.5px; color:var(--ink-2);
    display:flex; gap:8px; align-items:center;
  }
  .p3-remember .ri{width:24px; height:24px; flex-shrink:0; background:var(--blue); color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center;}
  .p3-remember .ri svg{width:14px; height:14px;}
  .p3-remember b{color:var(--blue);}
  .p3-bottom{display:grid; grid-template-columns:2fr 1fr; gap:12px; margin-top:12px;}
  .p3-best{
    background:#fff; border:1px solid rgba(0,0,0,.05); border-radius:10px; overflow:hidden;
    box-shadow:0 2px 8px rgba(0,0,0,.06);
  }
  .p3-best .h{background:var(--green); color:#fff; padding:7px 12px; font-size:11px; font-weight:700; letter-spacing:.4px; text-transform:uppercase; display:flex; align-items:center; gap:6px;}
  .p3-best .h svg{width:14px;height:14px;}
  .p3-best .b{padding:10px 12px;}
  .p3-best .b ul{list-style:none; padding:0; margin:0;}
  .p3-best .b li{padding-left:22px; position:relative; margin-bottom:5px; font-size:11.5px; color:var(--ink-2);}
  .p3-best .b li::before{
    content:""; position:absolute; left:0; top:1px;
    width:14px; height:14px; background:var(--green); border-radius:50%;
  }
  .p3-best .b li::after{
    content:"✓"; position:absolute; left:3px; top:0; color:#fff; font-size:10px; font-weight:800;
  }
</style>
"""

    body_html = grid_css + f"""
<div class="p3-grid">
  <!-- 1. CREATING .SH FILES -->
  <div class="col-card">
    <div class="h">{icon('file')}1. Creating .sh Files</div>
    <div class="b">
      <ul>
        <li>Create a new file with <code class="inline">.sh</code> extension.</li>
        <li>Use any text editor: nano, vim, code, etc.</li>
        <li>Write your commands inside.</li>
      </ul>
      <div class="ex">Example:</div>
      <div class="code">nano myscript.sh</div>
    </div>
  </div>

  <!-- 2. THE SHEBANG -->
  <div class="col-card">
    <div class="h">{icon('terminal')}2. The Shebang #!/bin/bash</div>
    <div class="b">
      <ul>
        <li>The first line of your script should be the shebang.</li>
        <li>It tells the system to use Bash to run the script.</li>
      </ul>
      <div class="ex">Example:</div>
      <div class="code">#!/bin/bash</div>
      <div class="note">Always use this at the top!</div>
    </div>
  </div>

  <!-- 3. MAKE IT EXECUTABLE -->
  <div class="col-card">
    <div class="h">{icon('key')}3. Make It Executable chmod +x</div>
    <div class="b">
      <ul>
        <li>By default, scripts are not executable.</li>
        <li>Give execute permission.</li>
      </ul>
      <div class="ex">Example:</div>
      <div class="code">chmod +x myscript.sh</div>
    </div>
  </div>

  <!-- 4. RUN YOUR SCRIPT -->
  <div class="col-card">
    <div class="h">{icon('play')}4. Run Your Script</div>
    <div class="b">
      <div class="p3-method">Method 1 (Recommended)</div>
      <div class="code">./myscript.sh</div>
      <div class="p3-method">Method 2</div>
      <div class="code">bash myscript.sh</div>
      <div class="p3-tip"><b>Tip:</b> Use <code class="inline">./</code> when running from the current directory.</div>
    </div>
  </div>

  <!-- 5. FILE PERMISSIONS -->
  <div class="col-card">
    <div class="h">{icon('shield')}5. File Permissions</div>
    <div class="b">
      {table(["Permission","Symbol","Number","Meaning"],[
        ["Read","r","4","Read the file"],
        ["Write","w","2","Modify the file"],
        ["Execute","x","1","Run the file"],
      ])}
      <div style="margin-top:6px; font-size:11px;">Example Permission: <code class="inline">-rwxr-xr--</code></div>
      <div class="p3-perm-diag">
        <div class="seg"><span class="l">Owner</span>rwx</div>
        <div class="seg"><span class="l">Group</span>r-x</div>
        <div class="seg"><span class="l">Others</span>r--</div>
      </div>
      <div style="font-size:11px;">Check permissions with: <code class="inline">ls -l myscript.sh</code></div>
    </div>
  </div>

  <!-- 6. COMMON "PERMISSION DENIED" ERRORS -->
  <div class="col-card">
    <div class="h">{icon('warning')}6. Common "Permission Denied" Errors</div>
    <div class="b">
      <ul>
        <li>Script is not executable.</li>
        <li>Wrong file permissions.</li>
        <li>Trying to run without <code class="inline">./</code></li>
        <li>Script has Windows line endings (CRLF).</li>
        <li>Script saved with wrong ownership.</li>
      </ul>
      <div class="p3-fix">
        <span class="fxi">""" + icon("gear") + """</span>
        <div class="fx-c"><b>Fix:</b><br><code class="inline">chmod +x myscript.sh</code></div>
      </div>
    </div>
  </div>
</div>

<!-- 7 + 8 SIDE BY SIDE -->
<div class="p3-bottom">
  <!-- 7. DEBUGGING TABLE -->
  {card('7. Debugging a Script That Will Not Execute', 'bug',
    table(["Problem","Why It Happens","How to Fix"],[
      ["Permission denied","File is not executable or wrong permissions.","<code class='inline'>chmod +x myscript.sh</code><br><code class='inline'>ls -l myscript.sh</code>"],
      ["Command not found","Shebang missing or wrong, or command doesn't exist.","Check first line: <code class='inline'>#!/bin/bash</code><br>Use full path to command if needed."],
      ["No such file or directory","Wrong path or filename.","Check spelling and path:<br><code class='inline'>ls -l</code> <code class='inline'>pwd</code>"],
      ["^M: bad interpreter","Windows line endings (CRLF) in the script.","Fix line endings:<br><code class='inline'>sed -i 's/\\r$//' myscript.sh</code>"],
      ["Script runs but nothing happens","No execute commands or logic errors.","Add set -x at top for debug.<br><code class='inline'>bash -x myscript.sh</code>"],
    ])
  )}

  <!-- 8. BEST PRACTICES -->
  <div class="p3-best">
    <div class="h">{icon('check-square')}8. Best Practices</div>
    <div class="b">
      <ul>
        <li>Always start with <code class="inline">#!/bin/bash</code></li>
        <li>Make your script executable.</li>
        <li>Use full paths for important commands.</li>
        <li>Add comments to explain your code.</li>
        <li>Test your script step by step.</li>
        <li>Use <code class="inline">set -e</code> to exit on error.</li>
        <li>Keep scripts simple and readable.</li>
      </ul>
    </div>
  </div>
</div>

<div class="p3-remember">
  <span class="ri">""" + icon("info") + """</span>
  <div><b>Remember:</b> Great scripts start with good habits!</div>
</div>
"""
    return body_html


# ============================================================
# PAGE 4 — "2. SHELL COMMANDS YOU MUST KNOW FIRST"
# ============================================================

def page4_body():
    css = """
<style>
  .p4-grid{display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;}
  .p4-card{background:#fff; border:1px solid rgba(0,0,0,.05); border-radius:10px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,.06);}
  .p4-card .h{background:var(--green); color:#fff; padding:7px 12px; font-size:11px; font-weight:700; letter-spacing:.4px; text-transform:uppercase; display:flex; align-items:center; gap:6px;}
  .p4-card.navy .h{background:var(--navy);}
  .p4-card .h svg{width:14px;height:14px;}
  .p4-card .b{padding:8px 12px; font-size:11px;}
  .p4-cmd{display:flex; gap:8px; padding:5px 0; border-bottom:1px solid #ece6d3; align-items:flex-start;}
  .p4-cmd:last-child{border-bottom:none;}
  .p4-cmd .cmd-name{font-family:"JetBrains Mono",monospace; font-weight:700; color:var(--green-2); font-size:11px; min-width:110px;}
  .p4-cmd .cmd-desc{flex:1; color:var(--ink-2); font-size:11px; line-height:1.4;}
  .p4-cmd .cmd-ex{font-family:"JetBrains Mono",monospace; font-size:10px; background:#e8e4d4; padding:1px 5px; border-radius:3px; color:var(--green-2); display:inline-block; margin-top:2px;}
  .p4-compare{display:grid; grid-template-columns:1fr 1fr; gap:6px;}
  .p4-compare .col{padding:8px 10px; border-radius:6px; font-size:11px;}
  .p4-compare .col.abs{background:#e8f5ee;}
  .p4-compare .col.rel{background:#fce9b6;}
  .p4-compare .col h4{font-size:11px; font-weight:700; text-transform:uppercase; margin-bottom:4px; letter-spacing:.3px;}
  .p4-compare .col.abs h4{color:var(--green);}
  .p4-compare .col.rel h4{color:var(--orange);}
  .p4-compare .col ul{list-style:none; padding:0; margin:4px 0 0;}
  .p4-compare .col li{padding-left:14px; position:relative; margin-bottom:3px; font-size:10.5px;}
  .p4-compare .col li::before{content:"✓"; position:absolute; left:0; color:var(--green); font-weight:800;}
  .p4-path-tree{font-family:"JetBrains Mono",monospace; font-size:10px; background:#f5f1e8; padding:5px 8px; border-radius:4px; margin-bottom:4px;}
  .p4-op{display:flex; gap:8px; padding:5px 0; border-bottom:1px solid #ece6d3;}
  .p4-op:last-child{border-bottom:none;}
  .p4-op .op-desc{flex:1; font-size:10.5px; color:var(--ink-2);}
  .p4-op .op-code{font-family:"JetBrains Mono",monospace; font-size:10px; background:var(--terminal-bg); color:var(--terminal-green); padding:2px 6px; border-radius:3px;}
  .p4-out{display:flex; gap:8px; padding:5px 0; align-items:flex-start; border-bottom:1px solid #ece6d3;}
  .p4-out:last-child{border-bottom:none;}
  .p4-out .oi{width:22px; height:22px; flex-shrink:0; background:var(--green-light); color:var(--green); border-radius:5px; display:flex; align-items:center; justify-content:center;}
  .p4-out .oi svg{width:14px;height:14px;}
  .p4-out .ot{flex:1; font-size:10.5px;}
  .p4-out .ot b{font-family:"JetBrains Mono",monospace; color:var(--green-2);}
  .p4-exercise{background:#fff; border:1px solid rgba(0,0,0,.05); border-radius:10px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,.06);}
  .p4-exercise .h{background:var(--navy); color:#fff; padding:7px 12px; font-size:11px; font-weight:700; letter-spacing:.4px; text-transform:uppercase; display:flex; align-items:center; gap:6px;}
  .p4-exercise .h svg{width:14px;height:14px;}
  .p4-exercise .b{padding:8px 12px;}
  .p4-steps{display:grid; grid-template-columns:repeat(6,1fr); gap:6px 8px;}
  .p4-step{display:flex; flex-direction:column; gap:2px; position:relative;}
  .p4-step:not(:nth-child(6n))::after{
    content:"→"; position:absolute; right:-9px; top:8px;
    color:var(--green); font-size:14px; font-weight:800;
  }
  .p4-step:nth-child(n+7){ margin-top:8px; }
  .p4-step .n{width:20px; height:20px; border-radius:50%; background:var(--green); color:#fff; font-size:10px; font-weight:800; display:flex; align-items:center; justify-content:center; font-family:monospace;}
  .p4-step .t{font-size:9.5px; font-weight:700; color:var(--ink); text-transform:uppercase; letter-spacing:.3px; line-height:1.15; margin-top:2px;}
  .p4-step .c{font-family:"JetBrains Mono",monospace; font-size:10px; background:var(--terminal-bg); color:var(--terminal-green); padding:2px 5px; border-radius:3px;}
</style>
"""

    body_html = css + f"""
<div class="p4-grid">
  <!-- 1. NAVIGATE YOUR FILE SYSTEM -->
  <div class="p4-card">
    <div class="h">{icon('folder')}1. Navigate Your File System</div>
    <div class="b">
      <div class="p4-cmd"><span class="cmd-name">pwd</span><span class="cmd-desc">Print working directory.<br><span class="cmd-ex">pwd → /home/user</span></span></div>
      <div class="p4-cmd"><span class="cmd-name">ls</span><span class="cmd-desc">List files and folders.<br><span class="cmd-ex">ls → file1.txt docs images</span></span></div>
      <div class="p4-cmd"><span class="cmd-name">cd [dir]</span><span class="cmd-desc">Change directory.<br><span class="cmd-ex">cd docs</span> (moves into docs)</span></div>
      <div class="p4-cmd"><span class="cmd-name">cd ..</span><span class="cmd-desc">Go up one directory.<br><span class="cmd-ex">cd ..</span> (moves up one level)</span></div>
      <div class="p4-cmd"><span class="cmd-name">cd ~</span><span class="cmd-desc">Go to your home directory.<br><span class="cmd-ex">cd ~ → /home/user</span></span></div>
    </div>
  </div>

  <!-- 2. CREATE, COPY, MOVE, DELETE -->
  <div class="p4-card">
    <div class="h">{icon('file')}2. Create, Copy, Move, Delete</div>
    <div class="b">
      <div class="p4-cmd"><span class="cmd-name">mkdir [dir]</span><span class="cmd-desc">Create a new directory.<br><span class="cmd-ex">mkdir new_folder</span> (creates new_folder)</span></div>
      <div class="p4-cmd"><span class="cmd-name">touch [file]</span><span class="cmd-desc">Create an empty file.<br><span class="cmd-ex">touch notes.txt</span> (creates notes.txt)</span></div>
      <div class="p4-cmd"><span class="cmd-name">cp [src] [dest]</span><span class="cmd-desc">Copy files or folders.<br><span class="cmd-ex">cp file1.txt backup.txt</span></span></div>
      <div class="p4-cmd"><span class="cmd-name">mv [src] [dest]</span><span class="cmd-desc">Move or rename files/folders.<br><span class="cmd-ex">mv old.txt new.txt</span></span></div>
      <div class="p4-cmd"><span class="cmd-name">rm [file]</span><span class="cmd-desc">Remove (delete) files.<br><span class="cmd-ex">rm temp.txt</span></span></div>
    </div>
  </div>

  <!-- 3. VIEW FILE CONTENT -->
  <div class="p4-card">
    <div class="h">{icon('list')}3. View File Content</div>
    <div class="b">
      <div class="p4-cmd"><span class="cmd-name">cat [file]</span><span class="cmd-desc">Display entire file.<br><span class="cmd-ex">cat notes.txt</span> (shows full content)</span></div>
      <div class="p4-cmd"><span class="cmd-name">less [file]</span><span class="cmd-desc">View file page by page.<br><span class="cmd-ex">less largefile.log</span> (scroll with arrows / q to quit)</span></div>
      <div class="p4-cmd"><span class="cmd-name">head [file]</span><span class="cmd-desc">Show first 10 lines.<br><span class="cmd-ex">head file.log</span> (first 10 lines)</span></div>
      <div class="p4-cmd"><span class="cmd-name">tail [file]</span><span class="cmd-desc">Show last 10 lines.<br><span class="cmd-ex">tail file.log</span> (last 10 lines)</span></div>
    </div>
  </div>

  <!-- 4. ABSOLUTE VS RELATIVE PATHS -->
  <div class="p4-card navy">
    <div class="h">{icon('globe')}4. Absolute vs Relative Paths</div>
    <div class="b">
      <div class="p4-compare">
        <div class="col abs">
          <h4>Absolute Path</h4>
          <div style="font-size:10px; color:var(--ink-3); margin-bottom:2px;">Full path from root</div>
          <div class="p4-path-tree">/ → home → user → docs</div>
          <div style="font-family:monospace; font-size:10px; color:var(--green-2);">/home/user/docs/file.txt</div>
          <ul>
            <li>Starts from the root /</li>
            <li>Always points to the correct location</li>
          </ul>
        </div>
        <div class="col rel">
          <h4>Relative Path</h4>
          <div style="font-size:10px; color:var(--ink-3); margin-bottom:2px;">Based on current location</div>
          <div class="p4-path-tree">📍 /home/user</div>
          <div style="font-family:monospace; font-size:10px; color:var(--green-2);">docs/file.txt</div>
          <ul>
            <li>Does not start with /</li>
            <li>Depends on where you are</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- 5. COMBINING COMMANDS -->
  <div class="p4-card">
    <div class="h">{icon('puzzle')}5. Combining Commands</div>
    <div class="b">
      <div class="p4-op"><span class="op-desc">Use <b>;</b> to run commands one after another</span><span class="op-code">mkdir test ; cd test ; touch file.txt</span></div>
      <div class="p4-op"><span class="op-desc">Use <b>&amp;&amp;</b> to run next command only if the first succeeds</span><span class="op-code">mkdir test &amp;&amp; cd test</span></div>
      <div class="p4-op"><span class="op-desc">Use <b>||</b> to run next command if the first fails</span><span class="op-code">mkdir test || echo "Failed to create"</span></div>
      <div class="p4-op"><span class="op-desc">Use <b>|</b> to send output of one command to another</span><span class="op-code">ls -l | less</span></div>
      <div class="p4-op"><span class="op-desc">Use <b>&gt;</b> to redirect output to a file (overwrite)</span><span class="op-code">ls &gt; output.txt</span></div>
      <div class="p4-op"><span class="op-desc">Use <b>&gt;&gt;</b> to redirect output to a file (append)</span><span class="op-code">echo "Hello" &gt;&gt; notes.txt</span></div>
    </div>
  </div>

  <!-- 6. READING COMMAND OUTPUT -->
  <div class="p4-card navy">
    <div class="h">{icon('search')}6. Reading Command Output</div>
    <div class="b">
      <div class="p4-out"><span class="oi">{icon('list')}</span><span class="ot"><b>ls -l</b> — Lists files in long format.</span></div>
      <div class="p4-out"><span class="oi">{icon('file')}</span><span class="ot"><b>ls -l | less</b> — Sends output to less so you can scroll.</span></div>
      <div class="p4-out"><span class="oi">{icon('list')}</span><span class="ot"><b>cat file.txt | head -n 5</b> — Shows first 5 lines of a file.</span></div>
      <div class="p4-out"><span class="oi">{icon('search')}</span><span class="ot"><b>grep "error" app.log</b> — Searches for the word "error" in the file.</span></div>
    </div>
  </div>
</div>

<!-- 7. BEGINNER PRACTICE EXERCISE -->
<div class="p4-exercise">
  <div class="h">{icon('play')}7. Beginner Practice Exercise</div>
  <div class="b">
    <div class="p4-steps">
      <div class="p4-step"><span class="n">1</span><div class="t">Show Where You Are</div><div class="c">pwd</div></div>
      <div class="p4-step"><span class="n">2</span><div class="t">List Files and Folders</div><div class="c">ls</div></div>
      <div class="p4-step"><span class="n">3</span><div class="t">Create a Folder</div><div class="c">mkdir practice</div></div>
      <div class="p4-step"><span class="n">4</span><div class="t">Go Into the Folder</div><div class="c">cd practice</div></div>
      <div class="p4-step"><span class="n">5</span><div class="t">Create a File</div><div class="c">touch hello.txt</div></div>
      <div class="p4-step"><span class="n">6</span><div class="t">Write Something in the File</div><div class="c">echo "Hello" &gt; hello.txt</div></div>
      <div class="p4-step"><span class="n">7</span><div class="t">View File Content</div><div class="c">cat hello.txt</div></div>
      <div class="p4-step"><span class="n">8</span><div class="t">Copy the File</div><div class="c">cp hello.txt hello_copy.txt</div></div>
      <div class="p4-step"><span class="n">9</span><div class="t">Rename the File</div><div class="c">mv hello_copy.txt renamed.txt</div></div>
      <div class="p4-step"><span class="n">10</span><div class="t">List Files to See Changes</div><div class="c">ls -l</div></div>
      <div class="p4-step"><span class="n">11</span><div class="t">Go Back One Directory</div><div class="c">cd ..</div></div>
      <div class="p4-step"><span class="n">12</span><div class="t">Remove the Folder</div><div class="c">rm -r practice</div></div>
    </div>
  </div>
</div>
"""
    return body_html


# ============================================================
# PAGE 5 — "5. READING USER INPUT AND SCRIPT ARGUMENTS"
# ============================================================

def page5_body():
    css = """
<style>
  .p5-top{display:grid; grid-template-columns:1fr 1.2fr; gap:12px; margin-bottom:12px;}
  .p5-mid{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:12px;}
  .p5-bot{display:grid; grid-template-columns:1.5fr 1fr; gap:12px;}
  .p5-card{background:#fff; border:1px solid rgba(0,0,0,.05); border-radius:10px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,.06);}
  .p5-card .h{background:var(--green); color:#fff; padding:7px 12px; font-size:11px; font-weight:700; letter-spacing:.4px; text-transform:uppercase; display:flex; align-items:center; gap:6px;}
  .p5-card .h svg{width:14px;height:14px;}
  .p5-card .b{padding:10px 12px; font-size:11.5px; color:var(--ink-2); line-height:1.5;}
  .p5-card .b ul{list-style:none; padding:0; margin:0;}
  .p5-card .b li{padding-left:14px; position:relative; margin-bottom:4px;}
  .p5-card .b li::before{content:"•"; position:absolute; left:0; color:var(--green); font-weight:800;}
  .p5-best li::before{content:"✓"; color:var(--green); font-weight:800;}
  .p5-arg-list{margin-top:6px;}
  .p5-arg-list li{padding-left:18px; position:relative;}
  .p5-arg-list li::before{content:"✓"; position:absolute; left:0; color:var(--green); font-weight:800;}
  .p5-bot .p5-card.right-col{display:flex; flex-direction:column;}
  .p5-bot .p5-card.right-col .stack{display:flex; flex-direction:column; gap:10px; padding:10px 12px;}
  .p5-run-box{background:var(--terminal-bg); border-radius:8px; overflow:hidden;}
  .p5-run-box .rb-h{background:#1c2230; padding:5px 10px; display:flex; align-items:center; gap:6px;}
  .p5-run-box .rb-h i{width:8px; height:8px; border-radius:50%; display:inline-block;}
  .p5-run-box .rb-h .rt{margin-left:auto; color:var(--terminal-dim); font-size:9px; font-family:monospace;}
  .p5-run-box .rb-b{padding:8px 10px; font-family:"JetBrains Mono",monospace; font-size:11px; color:var(--terminal-fg); line-height:1.6;}
  .p5-run-box .rb-b .p{color:var(--terminal-green);}
  .p5-run-box .rb-b .o{color:var(--terminal-fg);}
  .p5-does-box{background:var(--green-light); border-radius:8px; padding:8px 10px;}
  .p5-does-box h4{font-size:11px; font-weight:700; color:var(--green); text-transform:uppercase; margin-bottom:4px; letter-spacing:.3px;}
  .p5-does-box ul{list-style:none; padding:0; margin:0;}
  .p5-does-box li{padding-left:14px; position:relative; margin-bottom:3px; font-size:10.5px; color:var(--ink-2);}
  .p5-does-box li::before{content:"✓"; position:absolute; left:0; color:var(--green); font-weight:800;}
  .p5-tip{
    background:var(--green-light); border:2px solid var(--green); border-radius:10px;
    padding:10px 14px; margin-top:12px; display:flex; gap:10px; align-items:center;
    font-size:12px; color:var(--ink-2);
  }
  .p5-tip .ti{width:30px; height:30px; border-radius:50%; background:var(--green); color:#fff; flex-shrink:0; display:flex; align-items:center; justify-content:center;}
  .p5-tip .ti svg{width:18px; height:18px;}
  .p5-tip b{color:var(--green);}
</style>
"""

    body_html = css + f"""
<div class="p5-top">
  <!-- 1. READ: GET USER INPUT -->
  <div class="p5-card">
    <div class="h">{icon('lightbulb')}1. Read: Get User Input</div>
    <div class="b">
      <ul>
        <li>Use <code class="inline">read</code> to get input from the user.</li>
        <li><code class="inline">-p</code> shows a prompt.</li>
        <li>The value is stored in the variable.</li>
      </ul>
      {terminal("terminal",[
        ("cmd",'read -p "Enter your name: " NAME'),
        ("cmd",'echo "Hello, $NAME"'),
      ])}
    </div>
  </div>

  <!-- 2. SCRIPT ARGUMENTS -->
  <div class="p5-card">
    <div class="h">{icon('list')}2. Script Arguments</div>
    <div class="b">
      <div style="margin-bottom:6px;">Pass values to a script when you run it.</div>
      {table(["Symbol","Meaning","Example"],[
        ["$0","Script name","./deploy.sh"],
        ["$1","First argument","dev"],
        ["$2","Second argument","us-east-1"],
        ["$3","Third argument","app1"],
        ["$#","Number of arguments","3"],
        ["$@","All arguments",'"$@"'],
      ])}
    </div>
  </div>
</div>

<div class="p5-mid">
  <!-- 3. PASSING ARGUMENTS -->
  <div class="p5-card">
    <div class="h">{icon('rocket')}3. Passing Arguments</div>
    <div class="b">
      <div>Run your script with values:</div>
      {terminal("terminal",[("cmd","./deploy.sh dev us-east-1 app1")])}
      <div style="margin-top:6px;">Inside the script:</div>
      {terminal("terminal",[
        ("cmd","$1 = dev"),
        ("cmd","$2 = us-east-1"),
        ("cmd","$3 = app1"),
      ])}
    </div>
  </div>

  <!-- 4. VALIDATING ARGUMENTS -->
  <div class="p5-card">
    <div class="h">{icon('warning')}4. Validating Arguments</div>
    <div class="b">
      <ul>
        <li>Always check if arguments are provided.</li>
        <li>Prevents errors and confusion.</li>
      </ul>
      {terminal("terminal",[
        ("cmd","if [ $# -lt 3 ]; then"),
        ("cmd",'  echo "Usage: $0 <env> <region> <app>"'),
        ("cmd","  exit 1"),
        ("cmd","fi"),
      ])}
    </div>
  </div>

  <!-- 5. COMMON PRACTICES -->
  <div class="p5-card">
    <div class="h">{icon('check-square')}5. Common Practices</div>
    <div class="b">
      <ul class="p5-arg-list p5-best">
        <li>Always validate arguments.</li>
        <li>Use meaningful names.</li>
        <li>Quote <code class="inline">"$@"</code> when using all args.</li>
        <li>Give helpful usage messages.</li>
        <li>Exit with code 1 on error.</li>
      </ul>
    </div>
  </div>
</div>

<div class="p5-bot">
  <!-- 6. EXAMPLE: SIMPLE REUSABLE DEVOPS SCRIPT -->
  <div class="p5-card">
    <div class="h">{icon('terminal')}6. Example: Simple Reusable DevOps Script</div>
    <div class="b">
      {terminal("deploy.sh",[
        ("comment","#!/bin/bash"),
        ("comment","# Check arguments"),
        ("cmd","if [ $# -lt 3 ]; then"),
        ("cmd",'  echo "Usage: $0 <env> <region> <app>"'),
        ("cmd","  exit 1"),
        ("cmd","fi"),
        ("",""),
        ("comment","# Assign arguments to variables"),
        ("cmd","ENV=$1"),
        ("cmd","REGION=$2"),
        ("cmd","APP=$3"),
        ("",""),
        ("comment","# Use variables"),
        ('cmd','echo "Environment: $ENV"'),
        ('cmd','echo "Region: $REGION"'),
        ('cmd','echo "Application: $APP"'),
        ('cmd','echo "Deploying $APP to $ENV in $REGION..."'),
      ])}
    </div>
  </div>

  <!-- RIGHT STACK: RUN EXAMPLE + WHAT THIS SCRIPT DOES -->
  <div class="p5-card right-col">
    <div class="h">{icon('play')}Run Example</div>
    <div class="stack">
      <div class="p5-run-box">
        <div class="rb-h"><i style="background:#ff5f56;"></i><i style="background:#ffbd2e;"></i><i style="background:#27c93f;"></i><span class="rt">bash</span></div>
        <div class="rb-b">
          <div><span class="p">$</span> ./deploy.sh dev us-east-1 app1</div>
          <div class="o">Environment: dev</div>
          <div class="o">Region: us-east-1</div>
          <div class="o">Application: app1</div>
          <div class="o">Deploying app1 to dev in us-east-1...</div>
        </div>
      </div>
      <div class="p5-does-box">
        <h4>What This Script Does</h4>
        <ul>
          <li>Checks if 3 arguments are provided.</li>
          <li>Assigns values to variables.</li>
          <li>Prints the values.</li>
          <li>Ready to add real DevOps tasks.</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="p5-tip">
  <span class="ti">{icon('lightbulb')}</span>
  <div><b>TIP:</b> Good scripts take input, validate it, and do useful work. That's the foundation of automation!</div>
</div>
"""
    return body_html


# ============================================================
# Main: build & write all 5 files
# ============================================================

PAGES = [
    {
        "num": 1,
        "title": "SHELL SCRIPTING FOR DEVOPS HANDBOOK",
        "subtitle": "FOR COMPLETE BEGINNERS",
        "body": page1_body(),
        "filename": "recreated-page-01.html",
        "cover": True,
    },
    {
        "num": 2,
        "title": "1. WHAT IS SHELL SCRIPTING?",
        "subtitle": "",
        "body": page2_body(),
        "filename": "recreated-page-02.html",
    },
    {
        "num": 3,
        "title": "3. CREATING AND RUNNING SHELL SCRIPTS",
        "subtitle": "TURN COMMANDS INTO AUTOMATION",
        "body": page3_body(),
        "filename": "recreated-page-03.html",
    },
    {
        "num": 4,
        "title": "2. SHELL COMMANDS YOU MUST KNOW FIRST",
        "subtitle": "",
        "body": page4_body(),
        "filename": "recreated-page-04.html",
    },
    {
        "num": 5,
        "title": "5. READING USER INPUT AND SCRIPT ARGUMENTS",
        "subtitle": "GET INPUT. USE ARGUMENTS. BUILD SMARTER SCRIPTS.",
        "body": page5_body(),
        "filename": "recreated-page-05.html",
    },
]


def build_page(p):
    """Build a complete HTML file for a page.
    For the cover, we want to hide the regular page-title and use the
    custom cover layout, so we pass empty title/subtitle and add a
    wrapper class to the page-wrapper.
    """
    if p.get("cover"):
        # Build with empty title/subtitle, then post-process to add cover-page class
        html = page_wrapper(
            p["num"], 20, "", "",
            p["body"],
        )
        # Add .cover-page class to .page-wrapper so cover CSS hides default title
        html = html.replace(
            '<div class="page-wrapper">',
            '<div class="page-wrapper cover-page">',
            1,
        )
        return html
    else:
        # If no subtitle, hide it via injected CSS
        body = p["body"]
        if not p.get("subtitle"):
            body = "<style>.page-subtitle{display:none;}</style>" + body
        return page_wrapper(
            p["num"], 20,
            p["title"], p.get("subtitle", ""),
            body,
        )


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for p in PAGES:
        html = build_page(p)
        out_path = os.path.join(OUT_DIR, p["filename"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Wrote {out_path} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
