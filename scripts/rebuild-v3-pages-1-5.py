#!/usr/bin/env python3
"""
Rebuild carousel pages 1-5 of the Shell Scripting for DevOps handbook
using the Polotno notebook template (page_wrapper + multi_page_html)
and the colorful filled SVG icon library from shell_scripting_icons.py.

Output:
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/recreated-page-NN.html

Each output HTML is a standalone single-page document with:
  - Polotno notebook shell (paper, grid, 3D edges, spiral rings, holes)
  - Colorful multi-color filled SVG icons (NOT outline-only)
  - NO VERIQTA branding, NO social media footer
"""

import os
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from polotno_template import page_wrapper, multi_page_html, DEFAULT_PAPER_H  # noqa: E402
from shell_scripting_icons import ICONS, icon  # noqa: E402

OUT_DIR = Path("/home/z/my-project/downloads/instagram-DcaW1UljsVk")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Shared CSS — applied via a <style> block inside content_html
# (polotno_template.multi_page_html provides body/page-wrapper CSS,
#  but we need additional styles for cards, code blocks, etc.)
# ============================================================

SHARED_CSS = """
<style>
  /* === FIX: Polotno SVG paper must be absolute so .content overlays it === */
  /* Without this, the static SVG (1080x paper_h) pushes .content below the paper. */
  .page-wrapper > div:first-of-type > svg{position:absolute !important;top:0;left:0;}
  .page-wrapper > div:first-of-type > .content{position:absolute;top:11px;left:0;right:0;bottom:11px;overflow:hidden;}

  /* === Color tokens (Shell Scripting palette) === */
  :root{
    --green:#1B5E3F;
    --green-2:#164a32;
    --green-soft:#e8f3ec;
    --navy:#15264d;
    --navy-2:#1e3160;
    --blue:#2563eb;
    --blue-soft:#dbeafe;
    --purple:#7c3aed;
    --red:#dc2626;
    --red-soft:#fde8e8;
    --gold:#d4a017;
    --gold-soft:#fdf2cc;
    --orange:#e65100;
    --teal:#0d7377;
    --amber:#f9a825;
    --paper:#f5f1e8;
    --ink:#1c1c1c;
    --ink-2:#3a3f47;
    --grid:#bcc8d6;
    --term-bg:#0d1117;
    --term-fg:#e6edf3;
    --code-bg:#f3f4f6;
    --code-border:#d6d3c5;
  }
  .content{font-family:"Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased;}
  .content *{box-sizing:border-box;}

  /* === Page header (title row) === */
  .page-header{display:flex;align-items:flex-start;justify-content:space-between;gap:18px;margin-bottom:14px;}
  .page-title{font-size:30px;font-weight:800;color:var(--green);text-transform:uppercase;letter-spacing:.4px;line-height:1.05;}
  .page-subtitle{font-size:13px;font-weight:600;color:var(--ink-2);text-transform:uppercase;letter-spacing:.8px;margin-top:6px;}
  .page-pill{display:inline-flex;align-items:center;gap:6px;border:2px solid var(--green);color:var(--green);background:#fff;border-radius:999px;padding:5px 14px;font-size:11px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;}

  /* === Section cards === */
  .card{background:#fff;border:1px solid rgba(27,94,63,.18);border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.05);}
  .card .head{background:var(--green);color:#fff;padding:7px 12px;font-size:11px;font-weight:700;letter-spacing:.7px;text-transform:uppercase;display:flex;align-items:center;gap:8px;border-bottom:2px solid var(--green-2);}
  .card .head svg{width:16px;height:16px;flex-shrink:0;}
  .card .head.navy{background:var(--navy);border-bottom-color:var(--navy-2);}
  .card .head.blue{background:var(--blue);border-bottom-color:#1e40af;}
  .card .head.red{background:var(--red);border-bottom-color:#a01818;}
  .card .head.amber{background:var(--amber);border-bottom-color:#c87f00;color:#1c1c1c;}
  .card .head.purple{background:var(--purple);border-bottom-color:#5b22b8;}
  .card .pad{padding:10px 12px;font-size:12px;line-height:1.45;color:var(--ink);}

  /* === Grids === */
  .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
  .grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;}
  .grid-2-wide{display:grid;grid-template-columns:1.6fr 1fr;gap:12px;}
  .stack{display:flex;flex-direction:column;gap:10px;}

  /* === Lists === */
  ul.tick,ul.bullet{list-style:none;padding:0;margin:0;}
  ul.tick li,ul.bullet li{position:relative;padding-left:22px;margin:5px 0;font-size:12px;line-height:1.4;color:var(--ink);}
  ul.tick li svg{position:absolute;left:0;top:1px;width:15px;height:15px;}
  ul.bullet li::before{content:"";position:absolute;left:6px;top:7px;width:6px;height:6px;border-radius:50%;background:var(--green);}

  /* === Numbered steps === */
  .step{display:flex;align-items:flex-start;gap:8px;margin:6px 0;font-size:12px;line-height:1.4;}
  .step .n{flex-shrink:0;width:20px;height:20px;border-radius:50%;background:var(--green);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;}
  .step .body{flex:1;}
  .step .body strong{color:var(--green);text-transform:uppercase;letter-spacing:.4px;font-size:11px;}

  /* === Code (inline + block) === */
  code,.mono{font-family:"JetBrains Mono","SFMono-Regular",Menlo,Consolas,monospace;}
  code.inline{background:var(--code-bg);color:#0b3d22;border:1px solid var(--code-border);border-radius:4px;padding:1px 6px;font-size:11px;font-weight:600;}
  .codeblock{background:var(--term-bg);color:var(--term-fg);border-radius:8px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,.18);}
  .codeblock .bar{background:#1c2230;padding:5px 10px;display:flex;align-items:center;gap:6px;border-bottom:1px solid #2c3340;}
  .codeblock .dot{width:9px;height:9px;border-radius:50%;}
  .codeblock .dot.r{background:#ff5f56;} .codeblock .dot.y{background:#ffbd2e;} .codeblock .dot.g{background:#27c93f;}
  .codeblock .filename{margin-left:6px;color:#8b949e;font-size:10px;font-family:monospace;}
  .codeblock pre{margin:0;padding:10px 12px;font-family:"JetBrains Mono",Menlo,Consolas,monospace;font-size:11.5px;line-height:1.55;white-space:pre;overflow-x:auto;}
  .codeblock .c-cmt{color:#8b949e;font-style:italic;}
  .codeblock .c-kw{color:#ff7b72;}
  .codeblock .c-str{color:#a5d6ff;}
  .codeblock .c-var{color:#ffa657;}
  .codeblock .c-num{color:#79c0ff;}

  /* === Tables === */
  table.tbl{width:100%;border-collapse:collapse;font-size:11px;}
  table.tbl th{background:var(--green-soft);color:var(--green);font-weight:700;text-align:left;padding:6px 8px;border:1px solid rgba(27,94,63,.2);text-transform:uppercase;letter-spacing:.5px;font-size:10px;}
  table.tbl td{padding:5px 8px;border:1px solid rgba(27,94,63,.18);vertical-align:top;color:var(--ink);}
  table.tbl tr:nth-child(even) td{background:#faf9f3;}

  /* === Callout boxes === */
  .callout{border-radius:8px;padding:9px 12px;font-size:11.5px;line-height:1.45;display:flex;gap:9px;align-items:flex-start;}
  .callout svg{width:18px;height:18px;flex-shrink:0;}
  .callout.tip{background:#eef6ff;border:1px solid rgba(37,99,235,.35);color:#1c3a73;}
  .callout.warn{background:#fff8e1;border:1px solid var(--amber);color:#7a5b00;}
  .callout.danger{background:var(--red-soft);border:1px solid var(--red);color:#7a1212;}
  .callout.note{background:var(--green-soft);border:1px solid var(--green);color:#0d3a23;}
  .callout .lab{font-weight:800;text-transform:uppercase;letter-spacing:.6px;font-size:10px;margin-right:4px;}

  /* === Diagram arrows === */
  .flow{display:flex;align-items:center;gap:6px;flex-wrap:wrap;}
  .flow .chip{background:#fff;border:1.5px solid var(--green);color:var(--green);border-radius:8px;padding:5px 9px;font-size:11px;font-weight:700;display:flex;align-items:center;gap:5px;}
  .flow .chip svg{width:14px;height:14px;}
  .flow .arr{color:var(--green);font-weight:800;font-size:14px;}

  /* === Cover (page 1) === */
  .cover{display:flex;flex-direction:column;align-items:center;text-align:center;padding-top:6px;}
  .cover .brand{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:800;color:var(--green);letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
  .cover .brand .vq{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;background:var(--green);color:#fff;border-radius:8px;font-weight:900;font-size:18px;letter-spacing:-1px;}
  .cover .badge-row{display:flex;justify-content:center;gap:10px;margin:8px 0 14px 0;}
  .cover .badge{background:var(--green);color:#fff;border-radius:999px;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
  .cover h1{font-size:54px;font-weight:900;color:var(--green);line-height:1;margin:0;letter-spacing:-1px;text-transform:uppercase;}
  .cover h1 .for{display:block;font-size:18px;font-weight:700;color:var(--ink-2);margin:6px 0;letter-spacing:6px;}
  .cover .banner{display:inline-block;background:var(--green);color:#fff;font-size:38px;font-weight:900;letter-spacing:3px;padding:8px 28px;border-radius:6px;margin-top:8px;}
  .cover .subtitle{display:inline-block;border:2px solid var(--green);color:var(--green);background:#fff;border-radius:999px;padding:5px 18px;font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-top:14px;}
  .cover .hero-grid{display:grid;grid-template-columns:1fr 1.4fr 1fr;gap:18px;align-items:center;margin-top:18px;width:100%;}
  .cover .hero-grid .left,.cover .hero-grid .right{display:flex;flex-direction:column;align-items:center;gap:14px;}
  .cover .hero-grid .icon-circle{width:80px;height:80px;background:var(--green-soft);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(27,94,63,.15);}
  .cover .hero-grid .icon-circle svg{width:48px;height:48px;}
  .cover .hero-grid .center{display:flex;flex-direction:column;align-items:center;gap:14px;}
  .cover .hero-grid .center .term-card{background:var(--term-bg);border-radius:10px;padding:14px 16px;width:100%;box-shadow:0 8px 18px rgba(0,0,0,.25);}
  .cover .hero-grid .center .term-card .term-bar{display:flex;gap:5px;margin-bottom:8px;}
  .cover .hero-grid .center .term-card .term-bar span{width:9px;height:9px;border-radius:50%;}
  .cover .hero-grid .center .term-card pre{margin:0;color:var(--term-fg);font-family:"JetBrains Mono",monospace;font-size:13px;}
  .cover .hero-grid .center .term-card .prompt{color:#7ee787;}
  .cover .hero-grid .center .cloud-card{background:#fff;border:2px dashed var(--blue);border-radius:50px;padding:8px 22px;display:flex;align-items:center;gap:10px;}
  .cover .hero-grid .center .cloud-card svg{width:32px;height:32px;}
  .cover .value-list{display:flex;flex-direction:column;gap:7px;width:100%;}
  .cover .value-list .vi{display:flex;align-items:center;gap:8px;background:var(--green-soft);border:1.5px solid var(--green);border-radius:8px;padding:6px 10px;}
  .cover .value-list .vi svg{width:18px;height:18px;flex-shrink:0;}
  .cover .value-list .vi span{font-size:13px;font-weight:800;color:var(--green);letter-spacing:1.5px;text-transform:uppercase;}
  .cover .features{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px;width:100%;margin-top:18px;}
  .cover .feature{background:#fff;border:1.5px solid var(--green);border-radius:8px;padding:10px 8px;display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;}
  .cover .feature svg{width:26px;height:26px;}
  .cover .feature span{font-size:10px;font-weight:800;color:var(--green);letter-spacing:.5px;text-transform:uppercase;line-height:1.1;}

  /* === Command row (Section 1, page 4 style) === */
  .cmd-row{display:grid;grid-template-columns:120px 1fr;gap:8px;align-items:flex-start;padding:4px 0;border-bottom:1px dashed rgba(27,94,63,.18);}
  .cmd-row:last-child{border-bottom:none;}
  .cmd-row .cmd{font-family:"JetBrains Mono",monospace;font-size:11px;font-weight:700;color:var(--green);background:var(--green-soft);border:1px solid rgba(27,94,63,.25);border-radius:4px;padding:2px 6px;text-align:center;}
  .cmd-row .desc{font-size:11.5px;color:var(--ink-2);line-height:1.35;}
  .cmd-row .desc code.inline{display:inline-block;margin-left:4px;}

  /* === Inline mini-icons === */
  .ico-inline{display:inline-flex;vertical-align:middle;width:16px;height:16px;margin-right:4px;}

  /* === Header bar (small page identifier) === */
  .topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;}
  .topbar .brand{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:800;color:var(--green);letter-spacing:1.5px;text-transform:uppercase;}
  .topbar .brand .dot{width:10px;height:10px;background:var(--green);border-radius:2px;}

  .lead{font-size:11.5px;color:var(--ink-2);margin:4px 0 8px 0;line-height:1.45;}
  .small{font-size:10.5px;color:var(--ink-2);}
  .nowrap{white-space:nowrap;}
</style>
"""


# ============================================================
# PAGE 1 — COVER
# ============================================================

def build_page_1():
    # Icons used: terminal, lightbulb, gear, cloud, globe, check-circle
    term_icon = icon("terminal", 48)
    bulb_icon = icon("lightbulb", 48)
    gear_icon = icon("gear", 48)
    cloud_icon = icon("cloud", 32)
    globe_icon = icon("globe", 48)
    chk_icon = icon("check-circle", 18)
    chk_sm = icon("check-circle", 26)
    star_icon_big = icon("star", 26)
    pencil_big = icon("pencil", 26)
    rocket_big = icon("rocket", 26)

    content = f"""
{SHARED_CSS}
<div class="cover">
  <div class="brand"><span class="vq">$_</span><span>Shell · DevOps · Handbook</span></div>

  <div class="badge-row">
    <span class="badge">FOR COMPLETE BEGINNERS</span>
  </div>

  <h1>SHELL SCRIPTING<span class="for">— FOR —</span>DEVOPS</h1>
  <div class="banner">HANDBOOK</div>
  <div class="subtitle">Step-by-step · Practical · Beginner friendly</div>

  <div class="hero-grid">
    <div class="left">
      <div class="icon-circle">{bulb_icon}</div>
      <div class="icon-circle">{gear_icon}</div>
    </div>
    <div class="center">
      <div class="term-card">
        <div class="term-bar"><span style="background:#ff5f56"></span><span style="background:#ffbd2e"></span><span style="background:#27c93f"></span></div>
        <pre><span class="prompt">user@devops:~$</span> ./deploy.sh
<span class="prompt">&gt;</span> Building images...
<span class="prompt">&gt;</span> Pushing to registry...
<span class="prompt">&gt;</span> Deploying to cluster...
<span class="prompt">✓</span> Done. Have fun 🚀</pre>
      </div>
      <div class="cloud-card">{cloud_icon}<span style="font-family:monospace;font-weight:800;color:var(--blue);">&lt;/&gt;</span></div>
    </div>
    <div class="right">
      <div class="value-list">
        <div class="vi">{chk_icon}<span>Learn</span></div>
        <div class="vi">{chk_icon}<span>Practice</span></div>
        <div class="vi">{chk_icon}<span>Automate</span></div>
        <div class="vi">{chk_icon}<span>Deploy</span></div>
      </div>
      <div class="icon-circle">{globe_icon}</div>
    </div>
  </div>

  <div class="features">
    <div class="feature">{chk_sm}<span>Step-by-step Explanations</span></div>
    <div class="feature">{pencil_big}<span>Practical Examples</span></div>
    <div class="feature">{rocket_big}<span>DevOps Use Cases</span></div>
    <div class="feature">{star_icon_big}<span>Beginner Friendly</span></div>
  </div>
</div>
"""
    return content


# ============================================================
# PAGE 2 — WHAT IS SHELL SCRIPTING?
# ============================================================

def build_page_2():
    term_icon = icon("terminal", 16)
    shell_icon = icon("shell", 16)
    cube_icon = icon("cube", 16)
    user_icon = icon("user", 22)
    gear_icon = icon("gear", 22)
    monitor_icon = icon("monitor", 22)
    bulb_icon = icon("lightbulb", 18)
    file_icon = icon("file", 16)
    lock_icon = icon("lock", 16)
    play_icon = icon("play", 16)
    shield_icon = icon("shield", 16)
    chk = icon("check-circle", 14)

    # Numbers 1-6 for "what a shell does"
    nums = "".join(
        f'<div class="step"><span class="n">{i}</span><span class="body">{txt}</span></div>'
        for i, txt in enumerate([
            "Reads your command.",
            "Parses (understands) the command.",
            "Expands variables, wildcards, and paths.",
            "Executes the command or program.",
            "Returns the output and exit status.",
            "Waits for the next command.",
        ], 1)
    )

    why_steps = "".join(
        f'<li>{chk}{txt}</li>'
        for txt in [
            "Save time and reduce manual work.",
            "Eliminate human errors.",
            "Ensure repeatability and consistency.",
            "Scale operations easily.",
            "Automate deployments, monitoring, backups.",
            "Integrate with CI/CD pipelines.",
            "Improve reliability and speed.",
        ]
    )

    flow_diagram = f"""
    <div class="flow" style="margin:6px 0 8px 0;">
      <span class="chip">{user_icon}User</span>
      <span class="arr">→</span>
      <span class="chip">{shell_icon}Shell</span>
      <span class="arr">→</span>
      <span class="chip">{gear_icon}Kernel</span>
      <span class="arr">→</span>
      <span class="chip">{monitor_icon}Output</span>
    </div>"""

    # Running a script safely
    safe_steps = f"""
    <div class="step"><span class="n">1</span><span class="body"><strong>Create the file</strong><br><code class="inline">nano myscript.sh</code></span></div>
    <div class="step"><span class="n">2</span><span class="body"><strong>Save and exit</strong><br><code class="inline">CTRL + O, ENTER, CTRL + X</code></span></div>
    <div class="step"><span class="n">3</span><span class="body"><strong>Make it executable</strong><br><code class="inline">chmod +x myscript.sh</code></span></div>
    <div class="step"><span class="n">4</span><span class="body"><strong>Run the script</strong><br><code class="inline">./myscript.sh</code></span></div>
    """

    bp_list = "".join(
        f'<li>{chk}{txt}</li>'
        for txt in [
            "Review your script before running.",
            "Use full paths for important commands.",
            "Test in a safe environment first.",
        ]
    )

    content = f"""
{SHARED_CSS}
<div class="topbar">
  <div class="brand"><span class="dot"></span>Shell Scripting · DevOps Handbook</div>
  <span class="page-pill">Page 01</span>
</div>

<div class="page-header">
  <div>
    <div class="page-title">1. What Is Shell Scripting?</div>
    <div class="page-subtitle">Shell · Terminal · Bash · And Why DevOps Engineers Script</div>
  </div>
</div>

<div class="grid-2">
  <!-- Shell vs Terminal vs Bash -->
  <div class="card">
    <div class="head">{term_icon} Shell vs Terminal vs Bash</div>
    <div class="pad">
      <div style="margin-bottom:6px;"><strong style="color:var(--blue);">{term_icon} TERMINAL</strong> — The application you open. A text interface to interact with the computer.</div>
      <div style="margin-bottom:6px;"><strong style="color:var(--green);">{shell_icon} SHELL</strong> — The program that interprets your commands and talks to the OS.</div>
      <div><strong style="color:var(--navy);">{cube_icon} BASH</strong> — The most common shell on Linux. <em>"Bourne Again SHell"</em>. Command language + scripting interpreter.</div>
    </div>
  </div>

  <!-- What a shell does -->
  <div class="card">
    <div class="head">{shell_icon} What a Shell Actually Does</div>
    <div class="pad">
      {nums}
      {flow_diagram}
    </div>
  </div>

  <!-- Why DevOps engineers automate -->
  <div class="card">
    <div class="head">{gear_icon} Why DevOps Engineers Automate with Scripts</div>
    <div class="pad">
      <ul class="tick">{why_steps}</ul>
    </div>
  </div>

  <!-- Interactive vs Scripts table -->
  <div class="card">
    <div class="head navy">{cube_icon} Interactive Commands vs Scripts</div>
    <div class="pad" style="padding:8px;">
      <table class="tbl">
        <thead><tr><th style="width:50%;">Interactive Commands</th><th>Scripts</th></tr></thead>
        <tbody>
          <tr><td>You type and run one command at a time.</td><td>You write commands in a file and run them.</td></tr>
          <tr><td>Used for ad-hoc tasks.</td><td>Used for automation.</td></tr>
          <tr><td>Hard to repeat.</td><td>Repeatable and consistent.</td></tr>
          <tr><td>Not version controlled.</td><td>Version controlled (Git).</td></tr>
          <tr><td>Easy to forget commands.</td><td>Easy to share and reuse.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="grid-2" style="margin-top:12px;">
  <!-- Your first bash script -->
  <div class="card">
    <div class="head">{shell_icon} Your First Bash Script</div>
    <div class="pad">
      <div class="codeblock">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="filename">hello.sh</span></div>
        <pre><span class="c-cmt">#!/bin/bash</span>
<span class="c-cmt"># This is my first script</span>
<span class="c-kw">echo</span> <span class="c-str">"Hello, DevOps Engineer!"</span>
<span class="c-var">DATE</span>=$(<span class="c-kw">date</span>)
<span class="c-kw">echo</span> <span class="c-str">"Today is: $DATE"</span></pre>
      </div>
      <div class="small" style="margin-top:6px;">
        <strong>Shebang</strong> tells the system to use Bash · <strong>Comment</strong> is ignored · <strong>echo</strong> prints to screen · <strong>$(date)</strong> stores current date in a variable.
      </div>
    </div>
  </div>

  <!-- Running a script safely -->
  <div class="card">
    <div class="head">{shield_icon} Running a Script Safely</div>
    <div class="pad">
      {safe_steps}
      <div style="margin-top:6px;font-size:10.5px;font-weight:800;color:var(--green);text-transform:uppercase;letter-spacing:.5px;">Best Practices</div>
      <ul class="tick">{bp_list}</ul>
    </div>
  </div>
</div>

<div class="callout danger" style="margin-top:12px;">
  {bulb_icon}
  <div><span class="lab">Important Note</span> A script has the same power as the user who runs it. Always review scripts before executing — especially scripts downloaded from the internet.</div>
</div>
"""
    return content


# ============================================================
# PAGE 3 — CREATING AND RUNNING SHELL SCRIPTS
# ============================================================

def build_page_3():
    file_icon = icon("file", 16)
    shell_icon = icon("shell", 16)
    lock_icon = icon("lock", 16)
    play_icon = icon("play", 16)
    key_icon = icon("key", 16)
    stop_icon = icon("stop", 16)
    bulb_icon = icon("lightbulb", 18)
    wrench_icon = icon("wrench", 16)
    warn_icon = icon("warning", 16)
    question_icon = icon("question", 16)
    chk = icon("check-circle", 14)
    star = icon("star", 16)

    # Best practices list
    bp = "".join(
        f'<li>{chk}{txt}</li>'
        for txt in [
            "Always start with <code class='inline'>#!/bin/bash</code>",
            "Make your script executable.",
            "Use full paths for important commands.",
            "Add comments to explain your code.",
            "Test your script step by step.",
            "Use <code class='inline'>set -e</code> to exit on error.",
            "Keep scripts simple and readable.",
            "Great scripts start with good habits!",
        ]
    )

    content = f"""
{SHARED_CSS}
<div class="topbar">
  <div class="brand"><span class="dot"></span>Shell Scripting · DevOps Handbook</div>
  <span class="page-pill">Page 03</span>
</div>

<div class="page-header">
  <div>
    <div class="page-title">3. Creating &amp; Running Shell Scripts</div>
    <div class="page-subtitle">Turn commands into automation — .sh files · Shebang · chmod · Run · Permissions · Debugging · Best Practices</div>
  </div>
</div>

<div class="grid-3">
  <div class="card">
    <div class="head">{file_icon} 1. Create .sh Files</div>
    <div class="pad">
      Create a new file with <code class="inline">.sh</code> extension. Use any text editor: <code class="inline">nano</code>, <code class="inline">vim</code>, <code class="inline">code</code>. Write your commands inside.
      <div class="codeblock" style="margin-top:6px;">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span></div>
        <pre><span class="c-var">$</span> nano myscript.sh</pre>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="head">{shell_icon} 2. The Shebang #!/bin/bash</div>
    <div class="pad">
      The first line of your script should be the shebang. It tells the system to use Bash to run the script. <strong>Always use this at the top!</strong>
      <div class="codeblock" style="margin-top:6px;">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span></div>
        <pre><span class="c-cmt">#!/bin/bash</span></pre>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="head">{lock_icon} 3. Make It Executable</div>
    <div class="pad">
      By default, scripts are not executable. Give execute permission with <code class="inline">chmod</code>.
      <div class="codeblock" style="margin-top:6px;">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span></div>
        <pre><span class="c-var">$</span> chmod +x myscript.sh</pre>
      </div>
    </div>
  </div>
</div>

<div class="grid-3" style="margin-top:12px;">
  <div class="card">
    <div class="head">{play_icon} 4. Run Your Script</div>
    <div class="pad">
      <div style="margin-bottom:5px;"><strong style="color:var(--green);">Method 1 (Recommended)</strong></div>
      <div class="codeblock" style="margin-bottom:6px;">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span></div>
        <pre><span class="c-var">$</span> ./myscript.sh</pre>
      </div>
      <div style="margin-bottom:5px;"><strong>Method 2</strong></div>
      <div class="codeblock">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span></div>
        <pre><span class="c-var">$</span> bash myscript.sh</pre>
      </div>
      <div class="callout tip" style="margin-top:6px;padding:6px 8px;">{bulb_icon}<div><span class="lab">Tip:</span> Use <code class="inline">./</code> when running from the current directory.</div></div>
    </div>
  </div>

  <div class="card">
    <div class="head blue">{key_icon} 5. File Permissions</div>
    <div class="pad" style="padding:8px;">
      <table class="tbl">
        <thead><tr><th>Perm</th><th>Sym</th><th>Num</th><th>Meaning</th></tr></thead>
        <tbody>
          <tr><td>Read</td><td><code class="inline">r</code></td><td>4</td><td>Read the file</td></tr>
          <tr><td>Write</td><td><code class="inline">w</code></td><td>2</td><td>Modify the file</td></tr>
          <tr><td>Execute</td><td><code class="inline">x</code></td><td>1</td><td>Run the file</td></tr>
        </tbody>
      </table>
      <div class="small" style="margin-top:6px;">
        Example: <code class="inline">-rwxr-xr--</code><br>
        Owner · Group · Others<br>
        Check with: <code class="inline">ls -l myscript.sh</code>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="head red">{stop_icon} 6. Common "Permission Denied" Errors</div>
    <div class="pad">
      <ul class="bullet" style="font-size:11px;">
        <li>Script is not executable.</li>
        <li>Wrong file permissions.</li>
        <li>Trying to run without <code class="inline">./</code></li>
        <li>Script has Windows line endings (CRLF).</li>
        <li>Script saved with wrong ownership.</li>
      </ul>
      <div class="callout danger" style="margin-top:6px;padding:6px 8px;">
        {wrench_icon}
        <div><span class="lab">Fix:</span> <code class="inline">chmod +x myscript.sh</code></div>
      </div>
    </div>
  </div>
</div>

<div class="grid-2-wide" style="margin-top:12px;">
  <div class="card">
    <div class="head purple">{warn_icon} 7. Debugging a Script That Won't Execute</div>
    <div class="pad" style="padding:8px;">
      <table class="tbl">
        <thead><tr><th style="width:30%;">Problem</th><th style="width:35%;">Why It Happens</th><th>How to Fix</th></tr></thead>
        <tbody>
          <tr><td><strong>{warn_icon} Permission denied</strong></td><td>File is not executable or wrong permissions.</td><td><code class="inline">chmod +x</code><br><code class="inline">ls -l file.sh</code></td></tr>
          <tr><td><strong>{file_icon} Command not found</strong></td><td>Shebang missing/wrong, or command doesn't exist.</td><td>Check first line: <code class="inline">#!/bin/bash</code><br>Use full path to command.</td></tr>
          <tr><td><strong>{shell_icon} No such file or directory</strong></td><td>Wrong path or filename.</td><td>Check spelling: <code class="inline">ls -l</code><br><code class="inline">pwd</code></td></tr>
          <tr><td><strong>{warn_icon} ^M: bad interpreter</strong></td><td>Windows line endings (CRLF) in the script.</td><td><code class="inline">sed -i 's/\\r$//' f.sh</code></td></tr>
          <tr><td><strong>{question_icon} Runs but nothing happens</strong></td><td>No execute commands or logic errors.</td><td>Add <code class="inline">set -x</code> at top.<br><code class="inline">bash -x myscript.sh</code></td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card">
    <div class="head amber">{star} 8. Best Practices</div>
    <div class="pad">
      <ul class="tick">{bp}</ul>
      <div class="callout note" style="margin-top:6px;padding:6px 8px;">
        {star}
        <div><span class="lab">Remember:</span> Great scripts start with good habits!</div>
      </div>
    </div>
  </div>
</div>
"""
    return content


# ============================================================
# PAGE 4 — SHELL COMMANDS YOU MUST KNOW FIRST
# ============================================================

def build_page_4():
    folder_icon = icon("folder", 16)
    chk = icon("check-circle", 14)
    star_icon = icon("star", 16)
    list_icon = icon("list", 16)
    file_icon = icon("file", 16)
    eye_icon = icon("eye", 16)
    search_icon = icon("search", 16)

    nav_rows = [
        ("pwd", "Print working directory", "<code class='inline'>pwd</code> → <code class='inline'>/home/user</code>"),
        ("ls", "List files and folders", "<code class='inline'>ls</code> → <code class='inline'>file1.txt docs images</code>"),
        ("cd [dir]", "Change directory", "<code class='inline'>cd docs</code> (moves into docs)"),
        ("cd ..", "Go up one directory", "<code class='inline'>cd ..</code> (moves up one level)"),
        ("cd ~", "Go to your home directory", "<code class='inline'>cd ~</code> → <code class='inline'>/home/user</code>"),
    ]
    nav_html = "".join(
        f'<div class="cmd-row"><span class="cmd">{c}</span><span class="desc">{d} · <em>{e}</em></span></div>'
        for c, d, e in nav_rows
    )

    crud_rows = [
        ("mkdir [dir]", "Create a new directory", "<code class='inline'>mkdir new_folder</code>"),
        ("touch [file]", "Create an empty file", "<code class='inline'>touch notes.txt</code>"),
        ("cp [src] [dest]", "Copy files or folders", "<code class='inline'>cp file1.txt backup.txt</code>"),
        ("mv [src] [dest]", "Move or rename files/folders", "<code class='inline'>mv old.txt new.txt</code>"),
        ("rm [file]", "Remove (delete) files", "<code class='inline'>rm temp.txt</code>"),
    ]
    crud_html = "".join(
        f'<div class="cmd-row"><span class="cmd">{c}</span><span class="desc">{d} · <em>{e}</em></span></div>'
        for c, d, e in crud_rows
    )

    view_rows = [
        ("cat [file]", "Display entire file", "<code class='inline'>cat notes.txt</code>"),
        ("less [file]", "View file page by page", "<code class='inline'>less largefile.log</code>"),
        ("head [file]", "Show first 10 lines", "<code class='inline'>head file.log</code>"),
        ("tail [file]", "Show last 10 lines", "<code class='inline'>tail file.log</code>"),
    ]
    view_html = "".join(
        f'<div class="cmd-row"><span class="cmd">{c}</span><span class="desc">{d} · <em>{e}</em></span></div>'
        for c, d, e in view_rows
    )

    combine_rows = [
        (";", "Run commands one after another", "<code class='inline'>mkdir test ; cd test ; touch file.txt</code>"),
        ("&&", "Run next only if first succeeds", "<code class='inline'>mkdir test && cd test</code>"),
        ("||", "Run next if first fails", "<code class='inline'>mkdir test || echo \"Failed\"</code>"),
        ("|", "Send output to another command", "<code class='inline'>ls -l | less</code>"),
        (">", "Redirect output (overwrite)", "<code class='inline'>ls &gt; output.txt</code>"),
        (">>", "Redirect output (append)", "<code class='inline'>echo \"Hi\" &gt;&gt; notes.txt</code>"),
    ]
    combine_html = "".join(
        f'<div class="cmd-row"><span class="cmd">{c}</span><span class="desc">{d} · <em>{e}</em></span></div>'
        for c, d, e in combine_rows
    )

    reading_rows = [
        ("ls -l", "Lists files in long format.", list_icon),
        ("ls -l | less", "Sends output to less so you can scroll.", file_icon),
        ("cat file.txt | head -n 5", "Shows first 5 lines of a file.", eye_icon),
        ("grep \"error\" app.log", "Searches for the word \"error\".", search_icon),
    ]
    reading_html = "".join(
        f'<div class="cmd-row"><span class="cmd">{c}</span><span class="desc">{ico} {d}</span></div>'
        for c, d, ico in reading_rows
    )

    # Practice exercise 12 steps (2 rows of 6)
    steps = [
        ("pwd", "Show where you are"),
        ("ls", "List files and folders"),
        ("mkdir practice", "Create a folder"),
        ("cd practice", "Go into the folder"),
        ("touch hello.txt", "Create a file"),
        ("echo \"Hello\" > hello.txt", "Write something in the file"),
        ("cat hello.txt", "View file content"),
        ("cp hello.txt hello_copy.txt", "Copy the file"),
        ("mv hello_copy.txt renamed.txt", "Rename the file"),
        ("ls -l", "List files to see changes"),
        ("cd ..", "Go back one directory"),
        ("rm -r practice", "Remove the folder"),
    ]
    steps_html = "".join(
        f'<div class="step"><span class="n">{i}</span><span class="body"><strong>{title}</strong><br><code class="inline">{cmd}</code></span></div>'
        for i, (cmd, title) in enumerate(steps, 1)
    )

    content = f"""
{SHARED_CSS}
<div class="topbar">
  <div class="brand"><span class="dot"></span>Shell Scripting · DevOps Handbook</div>
  <span class="page-pill">Page 02</span>
</div>

<div class="page-header">
  <div>
    <div class="page-title">2. Shell Commands You Must Know First</div>
    <div class="page-subtitle">Navigate · Create · View · Paths · Combine · Read · Practice</div>
  </div>
</div>

<div class="grid-2">
  <div class="card">
    <div class="head">{list_icon} 1. Navigate Your File System</div>
    <div class="pad">{nav_html}</div>
  </div>

  <div class="card">
    <div class="head">{folder_icon} 2. Create, Copy, Move, Delete</div>
    <div class="pad">{crud_html}</div>
  </div>
</div>

<div class="grid-2" style="margin-top:12px;">
  <div class="card">
    <div class="head">{file_icon} 3. View File Content</div>
    <div class="pad">{view_html}</div>
  </div>

  <div class="card">
    <div class="head blue">{folder_icon} 4. Absolute vs Relative Paths</div>
    <div class="pad">
      <div style="margin-bottom:6px;">
        <strong style="color:var(--blue);">ABSOLUTE PATH</strong> <span class="small">(full from root)</span><br>
        <code class="inline">/home/user/docs/file.txt</code>
        <ul class="tick" style="margin-top:3px;">
          <li>{chk}Starts from the root <code class="inline">/</code></li>
          <li>{chk}Always points to the correct location</li>
        </ul>
      </div>
      <div>
        <strong style="color:var(--blue);">RELATIVE PATH</strong> <span class="small">(based on current location)</span><br>
        <span class="small">Current: <code class="inline">/home/user</code></span><br>
        <code class="inline">docs/file.txt</code>
        <ul class="tick" style="margin-top:3px;">
          <li>{chk}Does not start with <code class="inline">/</code></li>
          <li>{chk}Depends on where you are</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="grid-2" style="margin-top:12px;">
  <div class="card">
    <div class="head">{list_icon} 5. Combining Commands</div>
    <div class="pad">{combine_html}</div>
  </div>

  <div class="card">
    <div class="head blue">{eye_icon} 6. Reading Command Output</div>
    <div class="pad">{reading_html}</div>
  </div>
</div>

<div class="card" style="margin-top:12px;">
  <div class="head amber">{star_icon} 7. Beginner Practice Exercise — 12 Steps</div>
  <div class="pad">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px 24px;">
      {steps_html}
    </div>
  </div>
</div>
"""
    return content


# ============================================================
# PAGE 5 — READING USER INPUT AND SCRIPT ARGUMENTS
# ============================================================

def build_page_5():
    term_icon = icon("terminal", 16)
    user_icon = icon("user", 16)
    bulb_icon = icon("lightbulb", 18)
    rocket_icon = icon("rocket", 22)
    warn_icon = icon("warning", 16)
    chk = icon("check-circle", 14)
    gear_icon = icon("gear", 16)
    star_icon = icon("star", 16)
    clipboard_icon = icon("clipboard", 16)

    practices = "".join(
        f'<li>{chk}{txt}</li>'
        for txt in [
            "Always validate arguments.",
            "Use meaningful names.",
            "Quote <code class='inline'>\"$@\"</code> when using all args.",
            "Give helpful usage messages.",
            "Exit with code <code class='inline'>1</code> on error.",
        ]
    )

    script_does = "".join(
        f'<div class="step"><span class="n">{i}</span><span class="body">{txt}</span></div>'
        for i, txt in enumerate([
            "Checks if 3 arguments are provided.",
            "Assigns values to variables.",
            "Prints the values.",
            "Ready to add real DevOps tasks.",
        ], 1)
    )

    content = f"""
{SHARED_CSS}
<div class="topbar">
  <div class="brand"><span class="dot"></span>Shell Scripting · DevOps Handbook</div>
  <span class="page-pill">Page 05</span>
</div>

<div class="page-header">
  <div>
    <div class="page-title">5. Reading User Input &amp; Script Arguments</div>
    <div class="page-subtitle">Get input · Use arguments · Build smarter scripts</div>
  </div>
  <span class="page-pill" style="background:var(--green);color:#fff;border-color:var(--green);">{term_icon} read · $1 $2 $3 · $# · $@</span>
</div>

<div class="grid-2">
  <div class="card">
    <div class="head">{bulb_icon} 1. read: Get User Input</div>
    <div class="pad">
      Use <code class="inline">read</code> to get input from the user.
      <div class="codeblock" style="margin-top:6px;">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="filename">input.sh</span></div>
        <pre><span class="c-kw">read</span> -p <span class="c-str">"Enter your name: "</span> <span class="c-var">NAME</span>
<span class="c-kw">echo</span> <span class="c-str">"Hello, $NAME"</span></pre>
      </div>
      <div class="small" style="margin-top:6px;">{bulb_icon} <code class="inline">-p</code> shows a prompt. The value is stored in the variable.</div>
    </div>
  </div>

  <div class="card">
    <div class="head blue">{user_icon} 2. Script Arguments</div>
    <div class="pad" style="padding:8px;">
      Pass values to a script when you run it.
      <table class="tbl" style="margin-top:6px;">
        <thead><tr><th>Symbol</th><th>Meaning</th><th>Example</th></tr></thead>
        <tbody>
          <tr><td><code class="inline">$0</code></td><td>Script name</td><td><code class="inline">./deploy.sh</code></td></tr>
          <tr><td><code class="inline">$1</code></td><td>First argument</td><td><code class="inline">dev</code></td></tr>
          <tr><td><code class="inline">$2</code></td><td>Second argument</td><td><code class="inline">us-east-1</code></td></tr>
          <tr><td><code class="inline">$3</code></td><td>Third argument</td><td><code class="inline">app1</code></td></tr>
          <tr><td><code class="inline">$#</code></td><td>Number of arguments</td><td><code class="inline">3</code></td></tr>
          <tr><td><code class="inline">$@</code></td><td>All arguments</td><td><code class="inline">"$@"</code></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<div class="grid-3" style="margin-top:12px;">
  <div class="card">
    <div class="head">{rocket_icon} 3. Passing Arguments</div>
    <div class="pad">
      Run your script with values.
      <div class="codeblock" style="margin-top:6px;">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span></div>
        <pre><span class="c-var">$</span> ./deploy.sh dev us-east-1 app1</pre>
      </div>
      <div class="small" style="margin-top:6px;">
        Inside the script:<br>
        <code class="inline">$1 = dev</code><br>
        <code class="inline">$2 = us-east-1</code><br>
        <code class="inline">$3 = app1</code>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="head red">{warn_icon} 4. Validating Arguments</div>
    <div class="pad">
      Always check if arguments are provided.
      <div class="codeblock" style="margin-top:6px;">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span></div>
        <pre><span class="c-kw">if</span> [ <span class="c-var">$#</span> -lt 3 ]; <span class="c-kw">then</span>
  <span class="c-kw">echo</span> <span class="c-str">"Usage: $0 &lt;env&gt; &lt;region&gt; &lt;app&gt;"</span>
  <span class="c-kw">exit</span> 1
<span class="c-kw">fi</span></pre>
      </div>
      <div class="small" style="margin-top:6px;">{warn_icon} Prevents errors and confusion.</div>
    </div>
  </div>

  <div class="card">
    <div class="head">{chk} 5. Common Practices</div>
    <div class="pad">
      <ul class="tick">{practices}</ul>
    </div>
  </div>
</div>

<div class="grid-2-wide" style="margin-top:12px;">
  <div class="card">
    <div class="head">{term_icon} 6. Example: Simple Reusable DevOps Script</div>
    <div class="pad">
      <div class="codeblock">
        <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="filename">deploy.sh</span></div>
        <pre><span class="c-cmt">#!/bin/bash</span>
<span class="c-cmt"># Check arguments</span>
<span class="c-kw">if</span> [ <span class="c-var">$#</span> -lt 3 ]; <span class="c-kw">then</span>
  <span class="c-kw">echo</span> <span class="c-str">"Usage: $0 &lt;env&gt; &lt;region&gt; &lt;app&gt;"</span>
  <span class="c-kw">exit</span> 1
<span class="c-kw">fi</span>

<span class="c-cmt"># Assign arguments to variables</span>
<span class="c-var">ENV</span>=<span class="c-var">$1</span>
<span class="c-var">REGION</span>=<span class="c-var">$2</span>
<span class="c-var">APP</span>=<span class="c-var">$3</span>

<span class="c-cmt"># Use variables</span>
<span class="c-kw">echo</span> <span class="c-str">"Environment: $ENV"</span>
<span class="c-kw">echo</span> <span class="c-str">"Region: $REGION"</span>
<span class="c-kw">echo</span> <span class="c-str">"Application: $APP"</span>
<span class="c-kw">echo</span> <span class="c-str">"Deploying $APP to $ENV in $REGION..."</span></pre>
      </div>
    </div>
  </div>

  <div class="stack">
    <div class="card">
      <div class="head green">{term_icon} Run Example</div>
      <div class="pad">
        <div class="codeblock">
          <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span></div>
          <pre><span class="c-var">$</span> ./deploy.sh dev us-east-1 app1</pre>
        </div>
        <div class="small" style="margin-top:6px;color:var(--ink);font-family:monospace;">
          Environment: dev<br>
          Region: us-east-1<br>
          Application: app1<br>
          Deploying app1 to dev in us-east-1...
        </div>
      </div>
    </div>

    <div class="card">
      <div class="head purple">{gear_icon} What This Script Does</div>
      <div class="pad">
        {script_does}
      </div>
    </div>
  </div>
</div>

<div class="callout tip" style="margin-top:12px;">
  {star_icon}
  <div><span class="lab">Tip:</span> Good scripts take input, validate it, and do useful work. That's the foundation of automation! {clipboard_icon}</div>
</div>
"""
    return content


# ============================================================
# BUILD & WRITE
# ============================================================

PAGES = [
    (1, build_page_1(), DEFAULT_PAPER_H, "Shell Scripting for DevOps — Handbook Cover"),
    (2, build_page_2(), 1480, "Shell Scripting — Page 02 — What Is Shell Scripting"),
    (3, build_page_3(), 1500, "Shell Scripting — Page 03 — Creating & Running Scripts"),
    (4, build_page_4(), 1500, "Shell Scripting — Page 04 — Commands You Must Know First"),
    (5, build_page_5(), 1500, "Shell Scripting — Page 05 — Reading User Input & Arguments"),
]


def main():
    for n, content, paper_h, title in PAGES:
        page_html = page_wrapper(content, paper_height=paper_h, page_id=f"p{n}")
        doc = multi_page_html([page_html], title=title)
        out_path = OUT_DIR / f"recreated-page-{n:02d}.html"
        out_path.write_text(doc, encoding="utf-8")
        print(f"  Wrote {out_path} ({len(doc):,} bytes)")


if __name__ == "__main__":
    main()
