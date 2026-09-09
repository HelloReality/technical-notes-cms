#!/usr/bin/env python3
"""
Rebuild carousel pages 1-5 of the Shell Scripting for DevOps handbook.

Uses:
  - Colorful filled multi-color SVG icons from shell_scripting_icons.py
  - Canonical notebook template CSS (public/uploads/notebook-template/notebook-template.css)
  - VLM analysis (text, layout, icon inventory) per page

Output: /home/z/my-project/downloads/instagram-DcaW1UljsVk/recreated-page-NN.html

Each output HTML is fully self-contained (inline CSS + inline colorful SVG icons).
NO VERIQTA branding, NO social media footer.
Each page uses the canonical scaffold:
    <body class="multi-page">
      <div class="page-wrapper">
        <div class="page">
          <div class="spiral"></div>
          <div class="holes"></div>
          <div class="page-bend"></div>
          <div class="page-top-edge"></div>
          <div class="page-bottom-edge"></div>
          <div class="content"> ... </div>
        </div>
      </div>
    </body>
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Import the colorful multi-color filled SVG icon library
from shell_scripting_icons import ICONS, icon  # noqa: F401

PROJECT_ROOT = "/home/z/my-project"
CSS_PATH = os.path.join(
    PROJECT_ROOT, "public", "uploads", "notebook-template", "notebook-template.css"
)
OUT_DIR = os.path.join(
    PROJECT_ROOT, "downloads", "instagram-DcaW1UljsVk"
)

# Read the canonical notebook CSS once — inlined into every page
with open(CSS_PATH, "r", encoding="utf-8") as fh:
    CANONICAL_CSS = fh.read()

# ============================================================
# Common page scaffold helpers
# ============================================================

# Extra CSS shared by every page (page-specific styles are appended per page)
SHARED_EXTRA_CSS = """
/* ====== PAGE-LEVEL LAYOUT (extends canonical notebook CSS) ====== */
.content{position:relative;z-index:2;}

/* Generic content card */
.card{
  background:#fff;
  border-radius:10px;
  overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,.06);
  border:1px solid rgba(0,0,0,.06);
}
.card .head{
  background:var(--green);
  color:#fff;
  padding:8px 14px;
  font-size:12px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;
  display:flex;align-items:center;gap:8px;
  border-bottom:2px solid var(--green-2);
}
.card .head.navy{background:var(--navy);border-bottom-color:var(--navy-2);}
.card .head.red{background:var(--red);border-bottom-color:#a01818;}
.card .head svg{width:18px;height:18px;flex-shrink:0;}
.card .pad{padding:12px 14px;}

/* Generic two-column body */
.body-2col{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.body-3col{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;}
.col-stack{display:flex;flex-direction:column;gap:14px;}

/* Terminal / code block (dark) */
.terminal{
  background:var(--term-bg);
  border-radius:8px;
  overflow:hidden;
  box-shadow:0 4px 14px rgba(0,0,0,.22);
}
.terminal .bar{
  background:#1c2230;
  padding:6px 12px;
  display:flex;align-items:center;gap:6px;
}
.terminal .dot{width:10px;height:10px;border-radius:50%;}
.terminal .dot-r{background:#ff5f56;}
.terminal .dot-y{background:#ffbd2e;}
.terminal .dot-g{background:#27c93f;}
.terminal .ttl{margin-left:auto;color:#8b949e;font-size:10px;font-family:monospace;}
.terminal .body{
  padding:12px 14px;
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:12px;line-height:1.65;
  color:var(--term-fg);
  white-space:pre;
}
.terminal .body .p{color:#7ee787;}
.terminal .body .c{color:#8b949e;}
.terminal .body .k{color:#79c0ff;}
.terminal .body .s{color:#f2cc60;}
.terminal .body .o{color:#e6edf3;}

/* Inline code */
code.inl{
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:11px;
  background:#e8e4d4;padding:1px 5px;border-radius:3px;
  color:var(--green-2);
}

/* Tables */
.tbl{width:100%;border-collapse:collapse;font-size:11.5px;}
.tbl th{
  background:var(--green);color:#fff;
  padding:7px 10px;text-align:left;
  font-weight:700;font-size:10.5px;letter-spacing:.3px;text-transform:uppercase;
}
.tbl td{padding:6px 10px;border-bottom:1px solid #e0d8c8;color:var(--ink-2);vertical-align:top;}
.tbl td code{
  font-family:"JetBrains Mono",monospace;font-size:10.5px;
  background:#e8e4d4;padding:1px 4px;border-radius:3px;color:var(--green-2);
}
.tbl tr:last-child td{border-bottom:none;}

/* Numbered steps */
.steps{display:flex;flex-direction:column;gap:7px;}
.step{display:flex;gap:10px;align-items:flex-start;font-size:11.5px;color:var(--ink-2);line-height:1.45;}
.step .n{
  flex-shrink:0;width:22px;height:22px;border-radius:50%;
  background:var(--green);color:#fff;
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:800;font-family:monospace;
}
.step .ico{flex-shrink:0;width:24px;height:24px;}
.step .txt{flex:1;min-width:0;}
.step .txt b{color:var(--green-2);}

/* Checkmark bullets */
.checks{display:flex;flex-direction:column;gap:6px;}
.check{display:flex;gap:8px;align-items:flex-start;font-size:11.5px;color:var(--ink-2);line-height:1.45;}
.check svg{flex-shrink:0;width:18px;height:18px;}

/* Callouts */
.callout{display:flex;gap:10px;align-items:flex-start;border-radius:10px;padding:10px 14px;font-size:11.5px;line-height:1.45;}
.callout.warn{background:#fff4e0;border-left:3px solid var(--orange);color:var(--ink-2);}
.callout.tip{background:var(--green-light);border-left:3px solid var(--green);color:var(--ink-2);}
.callout.err{background:var(--red-soft);border-left:3px solid var(--red);color:var(--ink-2);}
.callout .ico{flex-shrink:0;width:24px;height:24px;margin-top:1px;}
.callout .ico svg{width:24px;height:24px;}

/* Mini flow boxes (for diagrams) */
.flow{display:flex;align-items:stretch;gap:8px;flex-wrap:wrap;}
.flow .box{
  flex:1;min-width:0;
  background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:8px;
  padding:10px 8px;display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;
}
.flow .box .ico{width:34px;height:34px;}
.flow .box .lbl{font-size:10px;font-weight:700;color:var(--green-2);text-transform:uppercase;letter-spacing:.3px;}
.flow .box .sub{font-size:9.5px;color:var(--ink-3);}
.flow .arr{display:flex;align-items:center;color:var(--ink-3);}

/* Page header */
.page-head{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:14px;
}
.page-head .badge{
  background:var(--green);color:#fff;
  padding:5px 14px;border-radius:999px;
  font-size:10.5px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
}
.page-head .brand{
  font-size:13px;font-weight:800;letter-spacing:1.5px;color:var(--green-2);
  display:flex;align-items:center;gap:8px;
}
.page-head .brand .vq{
  width:26px;height:26px;border-radius:6px;background:var(--green);
  color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;
}

.page-title{
  font-size:30px;font-weight:900;color:var(--green);
  text-transform:uppercase;letter-spacing:-.5px;line-height:1.05;
  margin-bottom:4px;
}
.page-title .num{color:var(--gold);}
.page-subtitle{
  font-size:13px;font-weight:700;color:var(--ink-2);
  text-transform:uppercase;letter-spacing:1.5px;
  margin-bottom:18px;padding-bottom:12px;
  border-bottom:2px solid var(--green);position:relative;
}
.page-subtitle::after{
  content:"";position:absolute;left:50%;bottom:-6px;
  width:10px;height:10px;background:var(--green);
  border-radius:50%;transform:translateX(-50%);
}
"""


def html_scaffold(title: str, page_css: str, content: str) -> str:
    """Wrap page content in a full HTML document with canonical + shared + page CSS."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
/* ====== CANONICAL NOTEBOOK TEMPLATE CSS ====== */
{CANONICAL_CSS}

/* ====== SHARED PAGE EXTENSIONS ====== */
{SHARED_EXTRA_CSS}

/* ====== PAGE-SPECIFIC STYLES ====== */
{page_css}
</style>
</head>
<body class="multi-page">
<div class="page-wrapper">
  <div class="page">
    <div class="spiral"></div>
    <div class="holes"></div>
    <div class="page-bend"></div>
    <div class="page-top-edge"></div>
    <div class="page-bottom-edge"></div>
    <div class="content">
{content}
    </div>
  </div>
</div>
</body>
</html>"""


def head(brand_text: str, page_label: str, title_html: str, subtitle_html: str = "") -> str:
    """Page header (brand + badge + title + subtitle)."""
    sub = ""
    if subtitle_html:
        sub = f'<div class="page-subtitle">{subtitle_html}</div>'
    else:
        sub = '<div class="page-subtitle">&nbsp;</div>'
    return f"""
<div class="page-head">
  <div class="brand"><span class="vq">S</span>{brand_text}</div>
  <div class="badge">{page_label}</div>
</div>
<h1 class="page-title">{title_html}</h1>
{sub}
"""


def card(head_html: str, body_html: str, extra_cls: str = "") -> str:
    """A standard .card with header + pad body."""
    return f'<div class="card {extra_cls}"><div class="head">{head_html}</div><div class="pad">{body_html}</div></div>'


def terminal_block(title: str, body_lines: list, extra_cls: str = "") -> str:
    """Dark terminal block. body_lines is a list of (cls, text)."""
    dots = (
        '<span class="dot dot-r"></span>'
        '<span class="dot dot-y"></span>'
        '<span class="dot dot-g"></span>'
    )
    body_html = "\n".join(
        f'<div class="{cls}">{txt}</div>' if cls else f'<div>{txt}</div>'
        for cls, txt in body_lines
    )
    return f"""<div class="terminal {extra_cls}">
  <div class="bar">{dots}<span class="ttl">{title}</span></div>
  <div class="body">{body_html}</div>
</div>"""


# ============================================================
# PAGE 1 — Cover (single column centered)
# ============================================================

def build_page_1() -> str:
    page_css = """
.cover{
  display:flex;flex-direction:column;align-items:center;
  text-align:center;padding:8px 0 0;
}
.cover .pre{
  font-size:12px;font-weight:700;letter-spacing:3px;color:var(--ink-3);
  text-transform:uppercase;margin-bottom:14px;
}
.cover .title-1{
  font-size:78px;font-weight:900;color:var(--green);
  letter-spacing:-2px;line-height:1;text-transform:uppercase;
}
.cover .title-for{
  display:flex;align-items:center;justify-content:center;gap:18px;
  margin:6px 0;
}
.cover .title-for .ln{flex:0 0 80px;height:3px;background:var(--green);border-radius:2px;}
.cover .title-for .t{font-size:34px;font-weight:800;color:var(--green-2);letter-spacing:6px;text-transform:uppercase;}
.cover .title-2{
  font-size:78px;font-weight:900;color:var(--green);
  letter-spacing:-2px;line-height:1;text-transform:uppercase;
}
.cover .ribbon{
  margin-top:6px;
  background:var(--green);
  color:#fff;
  font-size:32px;font-weight:900;letter-spacing:4px;
  padding:6px 60px;text-transform:uppercase;
  position:relative;
  box-shadow:0 4px 12px rgba(0,0,0,.18);
}
.cover .ribbon::before,.cover .ribbon::after{
  content:"";position:absolute;top:0;bottom:0;width:0;
  border:18px solid transparent;
}
.cover .ribbon::before{left:-36px;border-right:18px solid var(--green);}
.cover .ribbon::after{right:-36px;border-left:18px solid var(--green);}

.cover .pill{
  margin-top:18px;
  display:inline-block;padding:7px 24px;
  border:2.5px solid var(--green);
  color:var(--green);font-size:13px;font-weight:800;
  letter-spacing:2px;text-transform:uppercase;border-radius:999px;
}

.cover .stage{
  margin-top:24px;
  display:grid;
  grid-template-columns:1fr 1.4fr 1fr;
  gap:18px;align-items:center;
  width:100%;
}
.cover .side-icons{display:flex;flex-direction:column;align-items:center;gap:14px;}
.cover .side-icons .ic{width:62px;height:62px;}
.cover .side-icons.left{align-items:flex-start;}
.cover .side-icons.right{align-items:flex-end;gap:10px;}

.cover .terminal-hero{
  background:var(--term-bg);
  border-radius:14px;
  overflow:hidden;
  box-shadow:0 14px 40px rgba(0,0,0,.3);
  border:3px solid var(--navy);
}
.cover .terminal-hero .bar{
  background:#1c2230;padding:8px 12px;
  display:flex;align-items:center;gap:6px;
}
.cover .terminal-hero .dot{width:11px;height:11px;border-radius:50%;}
.cover .terminal-hero .dot-r{background:#ff5f56;}
.cover .terminal-hero .dot-y{background:#ffbd2e;}
.cover .terminal-hero .dot-g{background:#27c93f;}
.cover .terminal-hero .ttl{margin-left:auto;color:#8b949e;font-size:11px;font-family:monospace;}
.cover .terminal-hero .body{
  padding:18px 18px 24px;
  font-family:"JetBrains Mono","Fira Code",monospace;
  font-size:15px;line-height:1.9;color:var(--term-fg);
  text-align:left;
}
.cover .terminal-hero .body .p{color:#7ee787;}
.cover .terminal-hero .body .c{color:#8b949e;}
.cover .terminal-hero .body .k{color:#79c0ff;}
.cover .terminal-hero .body .s{color:#f2cc60;}
.cover .terminal-hero .body .o{color:#e6edf3;}

.cover .checklist{
  display:flex;flex-direction:column;align-items:flex-end;gap:6px;
}
.cover .checklist .it{
  display:flex;align-items:center;gap:6px;
  font-size:13px;font-weight:800;color:var(--green-2);
  letter-spacing:1.5px;text-transform:uppercase;
}
.cover .checklist .it svg{width:22px;height:22px;}
.cover .checklist .it.under{
  border-bottom:2px solid var(--green);padding-bottom:2px;width:auto;
}

.cover .features{
  margin-top:26px;
  display:grid;grid-template-columns:repeat(4,1fr);gap:0;
  border-top:2px solid var(--green);border-bottom:2px solid var(--green);
  padding:14px 0;
}
.cover .features .feat{
  display:flex;flex-direction:column;align-items:center;gap:6px;
  padding:0 14px;border-right:1px dashed rgba(27,94,63,.35);
}
.cover .features .feat:last-child{border-right:none;}
.cover .features .feat svg{width:32px;height:32px;}
.cover .features .feat .lbl{
  font-size:11px;font-weight:800;color:var(--green-2);
  text-transform:uppercase;letter-spacing:.8px;text-align:center;line-height:1.3;
}
"""

    body = f"""
<div class="cover">
  <div class="pre">The DevOps Engineer's Pocket Guide · Vol. 01</div>

  <div class="title-1">Shell Scripting</div>
  <div class="title-for"><span class="ln"></span><span class="t">For</span><span class="ln"></span></div>
  <div class="title-2">DevOps</div>
  <div class="ribbon">Handbook</div>

  <div class="pill">For Complete Beginners</div>

  <div class="stage">
    <div class="side-icons left">
      <div class="ic">{icon("lightbulb", 62)}</div>
      <div class="ic">{icon("gear", 50)}</div>
    </div>

    <div class="terminal-hero">
      <div class="bar">
        <span class="dot dot-r"></span>
        <span class="dot dot-y"></span>
        <span class="dot dot-g"></span>
        <span class="ttl">bash — devops@handbook</span>
      </div>
      <div class="body"><span class="c">#!/bin/bash</span>
<span class="p">$</span> <span class="k">echo</span> <span class="s">"Hello, DevOps!"</span>
<span class="o">Hello, DevOps!</span>
<span class="p">$</span> <span class="k">./deploy.sh</span> <span class="s">--env=prod</span>
<span class="o">  → building</span>
<span class="o">  → testing</span>
<span class="o">  → shipping</span>
<span class="c"># automate everything.</span></div>
    </div>

    <div class="side-icons right">
      <div class="ic">{icon("cloud", 62)}</div>
      <div class="checklist">
        <div class="it">{icon("check-circle", 22)} Learn</div>
        <div class="it">{icon("check-circle", 22)} Practice</div>
        <div class="it">{icon("check-circle", 22)} Automate</div>
        <div class="it under">{icon("check-circle", 22)} Deploy</div>
      </div>
      <div class="ic">{icon("globe", 50)}</div>
    </div>
  </div>

  <div class="features">
    <div class="feat">{icon("check-circle", 32)}<div class="lbl">Step-by-Step<br>Explanations</div></div>
    <div class="feat">{icon("lightbulb", 32)}<div class="lbl">Practical<br>Examples</div></div>
    <div class="feat">{icon("rocket", 32)}<div class="lbl">DevOps<br>Use Cases</div></div>
    <div class="feat">{icon("book", 32)}<div class="lbl">Beginner<br>Friendly</div></div>
  </div>
</div>
"""
    return html_scaffold(
        "Shell Scripting for DevOps — Handbook Cover",
        page_css,
        body,
    )


# ============================================================
# PAGE 2 — 2-column layout (left + right)
# ============================================================

def build_page_2() -> str:
    page_css = """
.p2-body{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.p2-body .col{display:flex;flex-direction:column;gap:14px;}

.compare-row{
  display:grid;grid-template-columns:48px 1fr;gap:10px;align-items:center;
  padding:8px 4px;border-bottom:1px dashed rgba(22,38,77,.10);
}
.compare-row:last-child{border-bottom:none;}
.compare-row .ico-box{
  width:48px;height:48px;border-radius:10px;
  background:var(--green-light);
  display:flex;align-items:center;justify-content:center;
}
.compare-row .ico-box svg{width:34px;height:34px;}
.compare-row .ico-box.navy{background:var(--blue-soft);}
.compare-row .txt h4{
  font-size:13px;font-weight:800;color:var(--green-2);
  text-transform:uppercase;letter-spacing:.5px;margin-bottom:1px;
}
.compare-row .txt p{font-size:11.5px;color:var(--ink-2);line-height:1.4;}

.flow-2 .box .ico svg{width:34px;height:34px;}
.compare-2col{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.compare-2col .col{
  border-radius:8px;padding:8px 10px;font-size:11px;line-height:1.45;
}
.compare-2col .col.blue{background:var(--blue-soft);border-left:3px solid var(--blue);}
.compare-2col .col.green{background:var(--green-light);border-left:3px solid var(--green);}
.compare-2col .col h4{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.4px;margin-bottom:4px;}
.compare-2col .col.blue h4{color:var(--blue);}
.compare-2col .col.green h4{color:var(--green);}
.compare-2col .col p{color:var(--ink-2);}
"""

    title = head(
        "Shell&nbsp;Scripting Handbook",
        "Page 2 of 20",
        "<span class='num'>1.</span> What is Shell Scripting?",
        "The Command-Line Foundations Every DevOps Engineer Needs",
    )

    # Left column
    left_col = f"""
{card(f"{icon('terminal', 18)} Shell vs Terminal vs Bash", """
  <div class="compare-row">
    <div class="ico-box navy">{icon('terminal', 34)}</div>
    <div class="txt"><h4>Terminal</h4><p>The application window that lets you type commands and see output. It's the UI, not the brain.</p></div>
  </div>
  <div class="compare-row">
    <div class="ico-box">{icon('shell', 34)}</div>
    <div class="txt"><h4>Shell</h4><p>The interpreter that parses your commands and asks the kernel to run them (bash, zsh, sh, fish…).</p></div>
  </div>
  <div class="compare-row">
    <div class="ico-box navy">{icon('cube', 34)}</div>
    <div class="txt"><h4>Bash</h4><p>One specific shell (Bourne-Again SHell). Default on most Linux distros &amp; the one this handbook uses.</p></div>
  </div>
""")}

{card(f"{icon('check-circle', 18)} Why DevOps Engineers Automate with Scripts", """
  <div class="checks">
    <div class="check">{icon('check-circle', 18)}<div>Eliminate repetitive toil — run one command, not fifty.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Make deployments repeatable, auditable &amp; reversible.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Codify institutional knowledge instead of sticky-notes.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Reduce human error in fragile production changes.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Enable CI/CD pipelines to run unattended at 3&nbsp;AM.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Ship a self-contained script instead of a 12-step runbook.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Version control your operations the same way you version code.</div></div>
  </div>
""")}

{card(f"{icon('file', 18)} Your First Bash Script", """
  """ + terminal_block("hello.sh", [
      ("c", "#!/bin/bash"),
      ("", '<span class="p">$</span> <span class="k">echo</span> <span class="s">"Hello, DevOps!"</span>'),
      ("o", "Hello, DevOps!"),
      ("c", "# Shebang tells the system which shell to use"),
      ("c", "# Comments start with # and are ignored at runtime"),
      ("", '<span class="p">$</span> <span class="k">name</span><span class="o">=</span><span class="s">"Alice"</span>'),
      ("", '<span class="p">$</span> <span class="k">echo</span> <span class="s">"Hi, $name"</span>'),
      ("o", "Hi, Alice"),
  ]) + """
""")}

{card(f"{icon('lightbulb', 18)} Important Note", """
  <div class="callout warn">
    <div class="ico">""" + icon("lightbulb", 24) + """</div>
    <div><b>Scripts are plain text files.</b> Save with a <code class="inl">.sh</code> extension (convention only),
    mark them executable with <code class="inl">chmod +x</code>, then run them with
    <code class="inl">./script.sh</code> or <code class="inl">bash script.sh</code>. No compilation needed.</div>
  </div>
""")}
"""

    # Right column
    right_col = f"""
{card(f"{icon('gear', 18)} What a Shell Actually Does", """
  <div class="steps">
    <div class="step"><div class="n">1</div><div class="txt"><b>Reads</b> your command from stdin (the keyboard).</div></div>
    <div class="step"><div class="n">2</div><div class="txt"><b>Parses</b> it into tokens: command + flags + arguments.</div></div>
    <div class="step"><div class="n">3</div><div class="txt"><b>Expands</b> variables, globs, and command substitutions.</div></div>
    <div class="step"><div class="n">4</div><div class="txt"><b>Resolves</b> the command path via <code class="inl">$PATH</code>.</div></div>
    <div class="step"><div class="n">5</div><div class="txt"><b>Asks the kernel</b> to spawn the process.</div></div>
    <div class="step"><div class="n">6</div><div class="txt"><b>Streams</b> stdout/stderr back to your terminal.</div></div>
  </div>
  <div style="margin-top:10px;" class="flow flow-2">
    <div class="box"><div class="ico">""" + icon("user", 34) + """</div><div class="lbl">You</div></div>
    <div class="arr">→</div>
    <div class="box"><div class="ico">""" + icon("shell", 34) + """</div><div class="lbl">Shell</div></div>
    <div class="arr">→</div>
    <div class="box"><div class="ico">""" + icon("gear", 34) + """</div><div class="lbl">Kernel</div></div>
    <div class="arr">→</div>
    <div class="box"><div class="ico">""" + icon("monitor", 34) + """</div><div class="lbl">Output</div></div>
  </div>
""")}

{card(f"{icon('arrow', 18)} Command Execution Flow", """
  <div class="flow flow-2">
    <div class="box"><div class="ico">""" + icon("pencil", 34) + """</div><div class="lbl">You Type</div><div class="sub">a command</div></div>
    <div class="arr">→</div>
    <div class="box"><div class="ico">""" + icon("terminal", 34) + """</div><div class="lbl">Shell</div><div class="sub">interprets</div></div>
    <div class="arr">→</div>
    <div class="box"><div class="ico">""" + icon("gear", 34) + """</div><div class="lbl">Kernel</div><div class="sub">executes</div></div>
    <div class="arr">→</div>
    <div class="box"><div class="ico">""" + icon("monitor", 34) + """</div><div class="lbl">Output</div><div class="sub">+ exit code</div></div>
  </div>
""")}

{card(f"{icon('list', 18)} Interactive Commands vs Scripts", """
  <div class="compare-2col">
    <div class="col blue">
      <h4>Interactive</h4>
      <p>One command at a time. Great for exploration &amp; quick fixes. Lost when the terminal closes.</p>
    </div>
    <div class="col green">
      <h4>Scripted</h4>
      <p>Many commands saved to a file. Repeatable, version-controlled, and runnable unattended in CI.</p>
    </div>
  </div>
""")}

{card(f"{icon('play', 18)} Running a Script Safely", """
  <div class="steps">
    <div class="step"><div class="n">1</div><div class="ico">""" + icon("file", 24) + """</div><div class="txt"><b>Create the file</b><br><code class="inl">nano myscript.sh</code></div></div>
    <div class="step"><div class="n">2</div><div class="ico">""" + icon("download", 24) + """</div><div class="txt"><b>Save &amp; exit</b><br><code class="inl">Ctrl+O</code>, <code class="inl">Enter</code>, <code class="inl">Ctrl+X</code></div></div>
    <div class="step"><div class="n">3</div><div class="ico">""" + icon("lock", 24) + """</div><div class="txt"><b>Make it executable</b><br><code class="inl">chmod +x myscript.sh</code></div></div>
    <div class="step"><div class="n">4</div><div class="ico">""" + icon("play", 24) + """</div><div class="txt"><b>Run the script</b><br><code class="inl">./myscript.sh</code></div></div>
    <div class="step"><div class="n">5</div><div class="ico">""" + icon("shield", 24) + """</div><div class="txt"><b>Best practices</b><br>Always read scripts before running them — especially with <code class="inl">sudo</code>.</div></div>
  </div>
""")}
"""

    content = f"""
{title}
<div class="p2-body">
  <div class="col">{left_col}</div>
  <div class="col">{right_col}</div>
</div>
"""
    return html_scaffold(
        "1. What is Shell Scripting? — Shell Scripting Handbook",
        page_css,
        content,
    )


# ============================================================
# PAGE 3 — 3-column grid (6 cards) + 2-col bottom
# ============================================================

def build_page_3() -> str:
    page_css = """
.p3-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px;}
.p3-bottom{display:grid;grid-template-columns:1.9fr 1fr;gap:14px;}
.perm-chips{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;}
.perm-chips .chip{
  font-family:"JetBrains Mono",monospace;font-size:11px;
  background:#e8e4d4;color:var(--green-2);
  padding:2px 6px;border-radius:3px;font-weight:700;
}
.perm-vis{
  display:grid;grid-template-columns:auto 1fr;gap:4px 10px;
  font-family:monospace;font-size:11px;margin-top:6px;
  background:#0d1117;color:#e6edf3;border-radius:6px;padding:8px 10px;
}
.perm-vis .s{color:#7ee787;font-weight:700;}
.perm-vis .d{color:#8b949e;}
.err-list{display:flex;flex-direction:column;gap:5px;font-size:11px;line-height:1.4;}
.err-list .it{display:flex;gap:6px;align-items:flex-start;}
.err-list .it .tag{
  flex-shrink:0;font-family:monospace;font-size:10px;
  background:#ffd4d4;color:#a01818;padding:1px 5px;border-radius:3px;font-weight:700;
}
.dbg-tbl td{font-size:11px;}
.dbg-tbl .pcol{width:30%;}
.dbg-tbl .wcol{width:35%;}
.dbg-tbl .fcol{width:35%;}
.tip-bar{
  display:flex;align-items:center;gap:10px;
  background:var(--blue-soft);border-left:3px solid var(--blue);
  border-radius:8px;padding:8px 12px;font-size:11px;
  margin-top:8px;
}
.tip-bar svg{flex-shrink:0;width:20px;height:20px;}
.tip-bar b{color:var(--blue);}
"""

    title = head(
        "Shell&nbsp;Scripting Handbook",
        "Page 3 of 20",
        "<span class='num'>3.</span> Creating &amp; Running Shell Scripts",
        "Turn Commands Into Automation",
    )

    card1 = card(
        f"{icon('file', 18)} Creating .sh Files",
        f"""
  <p style="font-size:11.5px;color:var(--ink-2);margin-bottom:8px;">Use your editor to create a script file with a descriptive name and the <code class="inl">.sh</code> extension.</p>
  {terminal_block("create script", [
      ("", '<span class="p">$</span> <span class="k">nano</span> deploy.sh'),
      ("", '<span class="p">$</span> <span class="k">touch</span> backup.sh'),
      ("", '<span class="p">$</span> <span class="k">chmod</span> +x backup.sh'),
  ])}
""",
    )

    card2 = card(
        f"{icon('code', 18)} The Shebang",
        f"""
  <p style="font-size:11.5px;color:var(--ink-2);margin-bottom:8px;">Line <b>1</b> of every script must declare the interpreter so the kernel knows what to run.</p>
  {terminal_block("shebang", [
      ("c", "#!/bin/bash"),
      ("c", "#!/usr/bin/env bash  ← portable"),
      ("c", "#!/bin/sh            ← minimal POSIX"),
      ("o", "# Without it: system may use the wrong shell"),
  ])}
""",
    )

    card3 = card(
        f"{icon('lock', 18)} Make It Executable",
        f"""
  <p style="font-size:11.5px;color:var(--ink-2);margin-bottom:8px;">By default new files are not runnable. Grant execute permission, then run directly.</p>
  {terminal_block("chmod +x", [
      ("", '<span class="p">$</span> <span class="k">chmod</span> +x deploy.sh'),
      ("", '<span class="p">$</span> <span class="k">./deploy.sh</span>'),
      ("o", "→ Building..."),
      ("o", "→ Deploying to prod"),
  ])}
""",
    )

    card4 = card(
        f"{icon('play', 18)} Run Your Script",
        f"""
  <p style="font-size:11.5px;color:var(--ink-2);margin-bottom:8px;">Two equivalent ways to invoke a script:</p>
  {terminal_block("run script", [
      ("c", "# Method 1: direct (needs +x & shebang)"),
      ("", '<span class="p">$</span> <span class="k">./deploy.sh</span>'),
      ("c", "# Method 2: pass to bash explicitly"),
      ("", '<span class="p">$</span> <span class="k">bash</span> deploy.sh'),
  ])}
  <div class="tip-bar">{icon('lightbulb', 20)}<div><b>Tip:</b> Method&nbsp;2 works even without <code class="inl">+x</code> — handy for one-off scripts.</div></div>
""",
    )

    card5 = card(
        f"{icon('key', 18)} File Permissions",
        f"""
  <table class="tbl">
    <tr><th>Perm</th><th>Symbol</th><th>Number</th><th>Meaning</th></tr>
    <tr><td>Read</td><td><code>r</code></td><td>4</td><td>View file</td></tr>
    <tr><td>Write</td><td><code>w</code></td><td>2</td><td>Modify</td></tr>
    <tr><td>Execute</td><td><code>x</code></td><td>1</td><td>Run / enter</td></tr>
  </table>
  <div class="perm-vis">
    <div class="s">-</div><div class="d">file type</div>
    <div class="s">rwx</div><div class="d">owner&nbsp;=&nbsp;7</div>
    <div class="s">r-x</div><div class="d">group&nbsp;=&nbsp;5</div>
    <div class="s">r--</div><div class="d">other&nbsp;=&nbsp;4</div>
  </div>
  <div class="perm-chips">
    <span class="chip">chmod 754 script.sh</span>
    <span class="chip">chmod +x</span>
    <span class="chip">chmod u+x</span>
  </div>
""",
    )

    card6 = card(
        f"{icon('stop', 18)} Common Errors",
        f"""<div class="head red">{icon('stop', 18)} Common Errors</div>""",
        extra_cls="",
    )
    # Rebuild card6 with red header
    card6 = f"""<div class="card"><div class="head red">{icon('stop', 18)} Common Errors</div><div class="pad">
  <div class="err-list">
    <div class="it"><span class="tag">E1</span><div><b>Permission denied</b> — forgot <code class="inl">chmod +x</code>.</div></div>
    <div class="it"><span class="tag">E2</span><div><b>Command not found</b> — typo or missing <code class="inl">$PATH</code>.</div></div>
    <div class="it"><span class="tag">E3</span><div><b>bad interpreter</b> — wrong shebang path.</div></div>
    <div class="it"><span class="tag">E4</span><div><b>Syntax error near token</b> — unmatched quote or missing <code class="inl">fi</code>/<code class="inl">done</code>.</div></div>
  </div>
  <div class="callout err" style="margin-top:8px;">
    <div class="ico">{icon('wrench', 24)}</div>
    <div><b>Fix:</b> Always run <code class="inl">bash -n script.sh</code> to syntax-check before executing.</div>
  </div>
</div></div>"""

    # Bottom row
    card7 = f"""<div class="card"><div class="head">{icon('bug', 18)} Debugging Like a Pro</div><div class="pad">
  <table class="tbl dbg-tbl">
    <tr><th class="pcol">Problem</th><th class="wcol">Why</th><th class="fcol">How to Fix</th></tr>
    <tr>
      <td><div style="display:flex;gap:6px;align-items:center;">{icon('warning', 18)} Permission denied</div></td>
      <td>File lacks execute bit.</td>
      <td><code>chmod +x script.sh</code></td>
    </tr>
    <tr>
      <td><div style="display:flex;gap:6px;align-items:center;">{icon('file', 18)} Script not found</div></td>
      <td>Wrong path or <code>./</code> omitted.</td>
      <td><code>./script.sh</code> (note the dot-slash)</td>
    </tr>
    <tr>
      <td><div style="display:flex;gap:6px;align-items:center;">{icon('terminal', 18)} bad interpreter</div></td>
      <td>Bad shebang or hidden CRLF line endings.</td>
      <td><code>dos2unix script.sh</code> then re-check shebang</td>
    </tr>
    <tr>
      <td><div style="display:flex;gap:6px;align-items:center;">{icon('code', 18)} Syntax error</div></td>
      <td>Unmatched quote / missing keyword.</td>
      <td><code>bash -n script.sh</code> to find the line</td>
    </tr>
    <tr>
      <td><div style="display:flex;gap:6px;align-items:center;">{icon('question', 18)} Logic wrong, no error</div></td>
      <td>Variables expanding unexpectedly.</td>
      <td><code>bash -x script.sh</code> to trace each step</td>
    </tr>
  </table>
</div></div>"""

    card8 = f"""<div class="card"><div class="head">{icon('check-square', 18)} Best Practices</div><div class="pad">
  <div class="checks">
    <div class="check">{icon('check-circle', 18)}<div>Always start with <code class="inl">#!/bin/bash</code></div></div>
    <div class="check">{icon('check-circle', 18)}<div>Use <code class="inl">set -euo pipefail</code> to fail loudly.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Quote every variable: <code class="inl">"$VAR"</code></div></div>
    <div class="check">{icon('check-circle', 18)}<div>Comment the <b>why</b>, not the <b>what</b>.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Test with <code class="inl">bash -n</code> before running.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Keep scripts under 200 lines; refactor more.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Use <code class="inl">shellcheck</code> as your linter.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Exit with explicit codes: <code class="inl">exit 1</code></div></div>
  </div>
  <div class="tip-bar" style="background:var(--green-light);border-left-color:var(--green);">
    {icon('star', 20)}
    <div><b style="color:var(--green-2);">Remember:</b> A script that fails silently is worse than no script at all. Make noise!</div>
  </div>
</div></div>"""

    content = f"""
{title}
<div class="p3-grid">{card1}{card2}{card3}{card4}{card5}{card6}</div>
<div class="p3-bottom">{card7}{card8}</div>
"""
    return html_scaffold(
        "3. Creating & Running Shell Scripts — Shell Scripting Handbook",
        page_css,
        content,
    )


# ============================================================
# PAGE 4 — Structured 2-col grid + full-width bottom
# ============================================================

def build_page_4() -> str:
    page_css = """
.p4-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;}
.p4-full{display:grid;grid-template-columns:1fr;}
.tree{font-family:monospace;font-size:11px;line-height:1.7;color:var(--ink-2);}
.tree .l{display:flex;align-items:center;gap:6px;}
.tree .l svg{width:14px;height:14px;flex-shrink:0;}
.tree .ind{padding-left:18px;}
.tree .ind2{padding-left:36px;}
.tree .ind3{padding-left:54px;}
.path-box{
  background:#0d1117;color:#e6edf3;border-radius:6px;padding:8px 12px;
  font-family:monospace;font-size:11.5px;margin:6px 0;
}
.path-box .p{color:#7ee787;}
.path-box .s{color:#f2cc60;}
.op-grid{display:grid;grid-template-columns:auto 1fr;gap:6px 10px;font-size:11px;line-height:1.5;}
.op-grid code{
  font-family:"JetBrains Mono",monospace;font-size:11px;
  background:#e8e4d4;color:var(--green-2);padding:1px 6px;border-radius:3px;font-weight:700;
}
.op-grid .desc{color:var(--ink-2);}
.cmd-list .row4{
  display:grid;grid-template-columns:32px auto 1fr;gap:8px;align-items:center;
  padding:6px 4px;border-bottom:1px dashed rgba(22,38,77,.10);
}
.cmd-list .row4:last-child{border-bottom:none;}
.cmd-list .row4 .ic{width:24px;height:24px;}
.cmd-list .row4 .cmd code{
  font-family:"JetBrains Mono",monospace;font-size:10.5px;
  background:#e8e4d4;color:var(--green-2);padding:1px 5px;border-radius:3px;font-weight:700;
}
.cmd-list .row4 .desc{font-size:11px;color:var(--ink-2);}
.exercise{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;}
.exercise .st{
  background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:8px;
  padding:8px 6px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px;
  position:relative;
}
.exercise .st .n{
  width:24px;height:24px;border-radius:50%;background:var(--green);color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;font-family:monospace;
}
.exercise .st .t{font-size:10px;font-weight:700;color:var(--green-2);text-transform:uppercase;letter-spacing:.3px;line-height:1.2;}
.exercise .st .c{font-size:9.5px;color:var(--ink-3);font-family:monospace;}
.exercise .st::after{
  content:"→";position:absolute;right:-9px;top:50%;transform:translateY(-50%);
  color:var(--green);font-size:14px;font-weight:900;
}
.exercise .st:last-child::after{content:"";}
.exercise .st:nth-child(6)::after{content:"↓";right:auto;left:50%;top:auto;bottom:-12px;transform:translateX(-50%);}
"""

    title = head(
        "Shell&nbsp;Scripting Handbook",
        "Page 4 of 20",
        "<span class='num'>2.</span> Shell Commands",
        "You Must Know First",
    )

    card1 = card(
        f"{icon('folder', 18)} Navigate Your File System",
        """
  <table class="tbl">
    <tr><th>Cmd</th><th>What it does</th></tr>
    <tr><td><code>pwd</code></td><td>Print working directory</td></tr>
    <tr><td><code>ls</code></td><td>List files in current dir</td></tr>
    <tr><td><code>ls -la</code></td><td>List all (incl. hidden) in long form</td></tr>
    <tr><td><code>cd /tmp</code></td><td>Change directory to /tmp</td></tr>
    <tr><td><code>cd ~</code></td><td>Go to your home directory</td></tr>
    <tr><td><code>cd ..</code></td><td>Go up one level</td></tr>
    <tr><td><code>cd -</code></td><td>Toggle to previous directory</td></tr>
  </table>
""",
    )

    card2 = card(
        f"{icon('pencil', 18)} Create, Copy, Move, Delete",
        """
  <table class="tbl">
    <tr><th>Cmd</th><th>What it does</th></tr>
    <tr><td><code>mkdir logs</code></td><td>Make a new directory</td></tr>
    <tr><td><code>touch app.sh</code></td><td>Create empty file (or update mtime)</td></tr>
    <tr><td><code>cp a.sh b.sh</code></td><td>Copy file a → b</td></tr>
    <tr><td><code>cp -r src/ dst/</code></td><td>Copy directory recursively</td></tr>
    <tr><td><code>mv old.sh new.sh</code></td><td>Move or rename</td></tr>
    <tr><td><code>rm file.tmp</code></td><td>Delete a file</td></tr>
    <tr><td><code>rm -rf build/</code></td><td>Force-remove a directory tree</td></tr>
  </table>
""",
    )

    card3 = card(
        f"{icon('eye', 18)} View File Content",
        """
  <table class="tbl">
    <tr><th>Cmd</th><th>What it does</th></tr>
    <tr><td><code>cat file</code></td><td>Print whole file to stdout</td></tr>
    <tr><td><code>less file</code></td><td>Pager (q to quit, / to search)</td></tr>
    <tr><td><code>head -n 20 file</code></td><td>First 20 lines</td></tr>
    <tr><td><code>tail -n 20 file</code></td><td>Last 20 lines</td></tr>
    <tr><td><code>tail -f log</code></td><td>Follow a growing log live</td></tr>
    <tr><td><code>wc -l file</code></td><td>Count lines</td></tr>
  </table>
""",
    )

    card4 = f"""<div class="card"><div class="head navy">{icon('folder', 18)} Absolute vs Relative Paths</div><div class="pad">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
    <div>
      <div style="font-size:11px;font-weight:800;color:var(--navy);text-transform:uppercase;margin-bottom:4px;">Absolute</div>
      <div class="path-box"><span class="p">/</span>home<span class="p">/</span>user<span class="p">/</span><span class="s">scripts</span></div>
      <div class="tree">
        <div class="l">{icon('folder', 14)} /</div>
        <div class="l ind">{icon('folder', 14)} home</div>
        <div class="l ind2">{icon('folder', 14)} user</div>
        <div class="l ind3">{icon('folder', 14)} scripts ←</div>
      </div>
    </div>
    <div>
      <div style="font-size:11px;font-weight:800;color:var(--navy);text-transform:uppercase;margin-bottom:4px;">Relative</div>
      <div class="path-box"><span class="s">scripts</span><span class="p">/</span>deploy.sh</div>
      <div class="checks" style="margin-top:4px;">
        <div class="check">{icon('check-circle', 18)}<div>Relative to <b>cwd</b>.</div></div>
        <div class="check">{icon('check-circle', 18)}<div><code class="inl">.</code> = here</div></div>
        <div class="check">{icon('check-circle', 18)}<div><code class="inl">..</code> = parent</div></div>
        <div class="check">{icon('check-circle', 18)}<div><code class="inl">~/</code> = home</div></div>
      </div>
    </div>
  </div>
</div></div>"""

    card5 = card(
        f"{icon('branch', 18)} Combining Commands",
        """
  <div class="op-grid">
    <code>;</code><div class="desc">Run sequentially: <code class="inl">a ; b</code></div>
    <code>&amp;&amp;</code><div class="desc">Run b only if a succeeds: <code class="inl">build &amp;&amp; deploy</code></div>
    <code>||</code><div class="desc">Run b only if a fails: <code class="inl">ping host || alert</code></div>
    <code>|</code><div class="desc">Pipe a's output into b's input: <code class="inl">cat log | grep err</code></div>
    <code>&gt;</code><div class="desc">Overwrite file with output: <code class="inl">echo hi &gt; f.txt</code></div>
    <code>&gt;&gt;</code><div class="desc">Append output to file: <code class="inl">echo hi &gt;&gt; f.txt</code></div>
  </div>
""",
    )

    card6 = f"""<div class="card"><div class="head navy">{icon('list', 18)} Reading Command Output</div><div class="pad">
  <div class="cmd-list">
    <div class="row4"><div class="ic">{icon('list', 24)}</div><div class="cmd"><code>ls -l</code></div><div class="desc">Long listing of files &amp; perms</div></div>
    <div class="row4"><div class="ic">{icon('file', 24)}</div><div class="cmd"><code>ls -l | less</code></div><div class="desc">Page through a long listing</div></div>
    <div class="row4"><div class="ic">{icon('code', 24)}</div><div class="cmd"><code>cat file.txt | head</code></div><div class="desc">First 10 lines of a file</div></div>
    <div class="row4"><div class="ic">{icon('search', 24)}</div><div class="cmd"><code>grep "error" log</code></div><div class="desc">Filter matching lines</div></div>
  </div>
</div></div>"""

    card7 = f"""<div class="card"><div class="head navy">{icon('rocket', 18)} Beginner Practice Exercise</div><div class="pad">
  <p style="font-size:11.5px;color:var(--ink-2);margin-bottom:10px;">Follow the 12 steps in order. Each builds on the previous one.</p>
  <div class="exercise">
    <div class="st"><div class="n">1</div><div class="t">Open Term</div><div class="c">Ctrl+Alt+T</div></div>
    <div class="st"><div class="n">2</div><div class="t">Where am I</div><div class="c">pwd</div></div>
    <div class="st"><div class="n">3</div><div class="t">List files</div><div class="c">ls -la</div></div>
    <div class="st"><div class="n">4</div><div class="t">Make dir</div><div class="c">mkdir devops</div></div>
    <div class="st"><div class="n">5</div><div class="t">Enter dir</div><div class="c">cd devops</div></div>
    <div class="st"><div class="n">6</div><div class="t">Create file</div><div class="c">touch notes.sh</div></div>
    <div class="st"><div class="n">7</div><div class="t">Edit file</div><div class="c">nano notes.sh</div></div>
    <div class="st"><div class="n">8</div><div class="t">Add shebang</div><div class="c">#!/bin/bash</div></div>
    <div class="st"><div class="n">9</div><div class="t">Save &amp; exit</div><div class="c">Ctrl+O, X</div></div>
    <div class="st"><div class="n">10</div><div class="t">Make exec</div><div class="c">chmod +x</div></div>
    <div class="st"><div class="n">11</div><div class="t">Run it</div><div class="c">./notes.sh</div></div>
    <div class="st"><div class="n">12</div><div class="t">Go home</div><div class="c">cd ~</div></div>
  </div>
</div></div>"""

    content = f"""
{title}
<div class="p4-grid">{card1}{card2}</div>
<div class="p4-grid">{card3}{card4}</div>
<div class="p4-grid">{card5}{card6}</div>
<div class="p4-full">{card7}</div>
"""
    return html_scaffold(
        "2. Shell Commands — Shell Scripting Handbook",
        page_css,
        content,
    )


# ============================================================
# PAGE 5 — 2-column + 3-column split layout
# ============================================================

def build_page_5() -> str:
    page_css = """
.p5-row1{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px;}
.p5-row2{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px;}
.p5-row3{display:grid;grid-template-columns:1.5fr 1fr;gap:14px;margin-bottom:14px;}
.p5-right-stack{display:flex;flex-direction:column;gap:14px;}
.tip-banner{
  display:flex;align-items:center;gap:12px;
  background:var(--green-light);border-left:4px solid var(--green);
  border-radius:10px;padding:10px 16px;font-size:12px;color:var(--ink-2);
}
.tip-banner svg{flex-shrink:0;width:28px;height:28px;}
.tip-banner .end-ico{margin-left:auto;}
.tip-banner b{color:var(--green-2);}
.arg-tbl{font-size:11px;}
.arg-tbl td{padding:5px 8px;}
"""

    title = head(
        "Shell&nbsp;Scripting Handbook",
        "Page 5 of 20",
        "<span class='num'>5.</span> Reading User Input &amp; Arguments",
        "Get Input · Use Arguments · Build Smarter Scripts",
    )

    card1 = card(
        f"{icon('terminal', 18)} Read: Get User Input",
        f"""
  {terminal_block("read.sh", [
      ("c", "#!/bin/bash"),
      ("c", "# Prompt the user and store their answer"),
      ("", '<span class="p">$</span> <span class="k">read</span> -p <span class="s">"Enter your name: "</span> name'),
      ("", '<span class="p">$</span> <span class="k">echo</span> <span class="s">"Hi, $name!"</span>'),
      ("o", "Enter your name: Alice"),
      ("o", "Hi, Alice!"),
  ])}
  <div class="callout tip" style="margin-top:8px;">
    <div class="ico">{icon('lightbulb', 24)}</div>
    <div><b>read</b> pauses the script until the user presses Enter. Use <code class="inl">-s</code> for passwords (silent) and <code class="inl">-t 10</code> to time out after 10s.</div>
  </div>
""",
    )

    card2 = card(
        f"{icon('list', 18)} Script Arguments",
        """
  <table class="tbl arg-tbl">
    <tr><th>Symbol</th><th>Meaning</th><th>Example</th></tr>
    <tr><td><code>$0</code></td><td>Script name</td><td>./deploy.sh</td></tr>
    <tr><td><code>$1 … $9</code></td><td>1st–9th argument</td><td>$1 = prod</td></tr>
    <tr><td><code>$#</code></td><td>Argument count</td><td>3</td></tr>
    <tr><td><code>$@</code></td><td>All args (array)</td><td>prod us-east-1 v1</td></tr>
    <tr><td><code>$?</code></td><td>Last exit code</td><td>0 = success</td></tr>
    <tr><td><code>$$</code></td><td>PID of script</td><td>4287</td></tr>
  </table>
""",
    )

    card3 = card(
        f"{icon('rocket', 18)} Passing Arguments",
        f"""
  {terminal_block("args.sh", [
      ("c", "#!/bin/bash"),
      ("", '<span class="p">$</span> <span class="k">echo</span> <span class="s">"Script: $0"</span>'),
      ("", '<span class="p">$</span> <span class="k">echo</span> <span class="s">"Env:   $1"</span>'),
      ("", '<span class="p">$</span> <span class="k">echo</span> <span class="s">"Ver:   $2"</span>'),
      ("", '<span class="p">$</span> <span class="k">./args.sh prod v1.2</span>'),
      ("o", "Script: ./args.sh"),
      ("o", "Env:   prod"),
      ("o", "Ver:   v1.2"),
  ])}
  <div style="display:flex;justify-content:flex-end;margin-top:6px;">{icon('rocket', 36)}</div>
""",
    )

    card4 = card(
        f"{icon('warning', 18)} Validating Arguments",
        f"""
  {terminal_block("validate.sh", [
      ("c", "#!/bin/bash"),
      ("c", "# Stop if the user forgot the env arg"),
      ("", '<span class="p">$</span> <span class="k">if</span> [ -z <span class="s">"$1"</span> ]; <span class="k">then</span>'),
      ("", '<span class="p">$</span>   <span class="k">echo</span> <span class="s">"Usage: $0 &lt;env&gt;"</span>'),
      ("", '<span class="p">$</span>   <span class="k">exit</span> 1'),
      ("", '<span class="p">$</span> <span class="k">fi</span>'),
  ])}
  <div class="callout warn" style="margin-top:8px;">
    <div class="ico">{icon('warning', 24)}</div>
    <div><b>Validate early.</b> Fail fast with <code class="inl">exit 1</code> before any work begins.</div>
  </div>
""",
    )

    card5 = card(
        f"{icon('check-circle', 18)} Common Practices",
        """
  <div class="checks">
    <div class="check">{icon('check-circle', 18)}<div>Always quote: <code class="inl">"$1"</code></div></div>
    <div class="check">{icon('check-circle', 18)}<div>Check <code class="inl">$#</code> before using args.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Use <code class="inl">$@</code> (not <code class="inl">$*</code>) in loops.</div></div>
    <div class="check">{icon('check-circle', 18)}<div>Default with <code class="inl">${1:-default}</code></div></div>
    <div class="check">{icon('check-circle', 18)}<div>Print usage on bad input.</div></div>
  </div>
""",
    )

    card6 = card(
        f"{icon('code', 18)} Example: Simple Reusable DevOps Script",
        f"""
  {terminal_block("deploy.sh", [
      ("c", "#!/bin/bash"),
      ("c", "# A reusable deploy script"),
      ("", '<span class="p">$</span> <span class="k">set</span> -euo pipefail'),
      ("", '<span class="p">$</span> ENV<span class="o">=</span><span class="s">"${1:-staging}"</span>'),
      ("", '<span class="p">$</span> <span class="k">echo</span> <span class="s">"Deploying to $ENV…"</span>'),
      ("", '<span class="p">$</span> <span class="k">./build</span> && <span class="k">./test</span> && <span class="k">./ship</span> <span class="s">"$ENV"</span>'),
      ("", '<span class="p">$</span> <span class="k">echo</span> <span class="s">"Done. ($?)"</span>'),
  ])}
""",
    )

    sub_a = card(
        f"{icon('terminal', 18)} Run Example",
        f"""
  {terminal_block("console", [
      ("", '<span class="p">$</span> <span class="k">./deploy.sh</span> prod'),
      ("o", "Deploying to prod…"),
      ("o", "  → build OK"),
      ("o", "  → test  OK"),
      ("o", "  → ship  OK"),
      ("o", "Done. (0)"),
  ])}
""",
    )

    sub_b = card(
        f"{icon('gear', 18)} What This Script Does",
        f"""
  <div class="steps">
    <div class="step"><div class="n">1</div><div class="txt"><b>set -euo pipefail</b> — fail on any error.</div></div>
    <div class="step"><div class="n">2</div><div class="txt"><b>ENV=${{1:-staging}}</b> — use arg or default.</div></div>
    <div class="step"><div class="n">3</div><div class="txt"><b>&amp;&amp;</b> chains build → test → ship.</div></div>
    <div class="step"><div class="n">4</div><div class="txt"><b>$?</b> prints the final exit code.</div></div>
  </div>
  <div style="display:flex;justify-content:flex-end;margin-top:6px;">{icon('gear', 40)}</div>
""",
    )

    tip_banner = f"""
<div class="tip-banner">
  {icon('star', 28)}
  <div><b>Tip:</b> Combine <code class="inl">read</code> for interactive prompts with positional args for automation. Same script, two modes.</div>
  <div class="end-ico">{icon('clipboard', 28)}</div>
</div>
"""

    content = f"""
{title}
<div class="p5-row1">{card1}{card2}</div>
<div class="p5-row2">{card3}{card4}{card5}</div>
<div class="p5-row3">
  {card6}
  <div class="p5-right-stack">{sub_a}{sub_b}</div>
</div>
{tip_banner}
"""
    return html_scaffold(
        "5. Reading User Input & Arguments — Shell Scripting Handbook",
        page_css,
        content,
    )


# ============================================================
# Main
# ============================================================

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    pages = [
        (1, build_page_1),
        (2, build_page_2),
        (3, build_page_3),
        (4, build_page_4),
        (5, build_page_5),
    ]
    for n, fn in pages:
        html = fn()
        out = os.path.join(OUT_DIR, f"recreated-page-{n:02d}.html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        size_kb = len(html) / 1024
        print(f"  ✓ page {n:02d} → {out}  ({size_kb:.1f} KB)")
    print(f"\nDone. {len(pages)} pages written to {OUT_DIR}")


if __name__ == "__main__":
    main()
