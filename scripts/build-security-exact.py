#!/usr/bin/env python3
"""
build-security-exact.py
-----------------------
Generate /home/z/my-project/public/uploads/linux-security-handbook.html

Recreates ALL 20 pages of the Linux Security Handbook using the EXACT CSS,
inline multi-color filled SVG icon style, and 2-column grid layout (rows +
sidebar) from the reference template
VERIQTA_Linux_Security_Handbook_Page2.html.

Branding cleanup:
  - All "VERIQTA" text / logos / watermarks removed.
  - Social-media footer (YouTube, GitHub, LinkedIn, X, Instagram, Telegram)
    removed.
  - The <script> binding generator (references #binding which does not exist)
    removed — .spiral and .holes already render the binding via background SVG.

Usage:
    python3 scripts/build-security-exact.py
"""
from __future__ import annotations

import html as _html
from pathlib import Path

OUT_PATH = Path("/home/z/my-project/public/uploads/linux-security-handbook.html")

# ============================================================================
# EXACT CSS — copied verbatim from VERIQTA_Linux_Security_Handbook_Page2.html
# (every rule from :root through @media print).
# ============================================================================
CSS = """  /* ============================================================
     RESET & ROOT VARIABLES
     ============================================================ */
  :root{
    --paper:#f5f1e8;          /* warm cream paper */
    --paper-2:#efe9dd;
    --grid-line:#bcc8d6;      /* faint graph paper grid */
    --navy:#15264d;           /* primary dark navy */
    --navy-2:#1e3160;
    --ink:#1c1c1c;
    --ink-2:#3a3f47;
    --blue:#2563eb;
    --blue-soft:#cfe0ff;      /* stronger pastel blue */
    --green:#16a34a;
    --green-soft:#cdf3da;     /* stronger pastel green */
    --purple:#7c3aed;
    --purple-soft:#e2d4ff;    /* stronger pastel purple */
    --red:#dc2626;
    --red-soft:#ffd4d4;       /* stronger pastel red */
    --gold:#d4a017;
    --gold-soft:#fce9b6;      /* stronger pastel gold */
    --orange:#ef6c00;
    --term-bg:#0d1117;
    --term-fg:#e6edf3;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:#cfc9bb;}
  body{
    font-family:"Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;
    color:var(--ink);
    display:flex;justify-content:center;align-items:flex-start;
    flex-direction:column;
    gap:24px;
    padding:24px 48px;  /* 48px left/right so spiral rings (at left:-30px) are fully visible */
  }

  /* Multi-page stacking: pages stack vertically with 24px gaps */
  body.multi-page{
    flex-direction:column;
    gap:24px;
    overflow:visible;
  }

  /* Wrapper holds page + binding, allows ring to extend outside page */
  .page-wrapper{
    position:relative;
    width:1080px;
    overflow:visible;  /* Rings extend outside — must not clip */
  }

  /* ============================================================
     PAGE / NOTEBOOK SHEET
     ============================================================ */
  .page{
    position:relative;
    width:1080px;              /* fixed design width */
    background:var(--paper);
    border-radius:14px;
    box-shadow:0 22px 60px rgba(0,0,0,0.28), 0 2px 0 rgba(0,0,0,0.06) inset;
    overflow:hidden;
    padding:42px 50px 26px 78px;  /* extra left padding for spiral binding */
  }

  /* Graph paper grid */
  .page::before{
    content:"";
    position:absolute;inset:0;
    background-image:
      linear-gradient(to right, var(--grid-line) 1px, transparent 1px),
      linear-gradient(to bottom, var(--grid-line) 1px, transparent 1px);
    background-size:26px 26px;
    opacity:.5;
    pointer-events:none;
    z-index:0;
  }

  /* ============================================================
     LEFT-EDGE BINDING (perfected layout)
     Ring extends OUTSIDE the page's left edge.
     ============================================================ */

  /* Page bend shadow at the very left edge */
  .page-bend{
    position:absolute;
    z-index:1;
    top:0;left:0;
    width:18px;height:100%;
    pointer-events:none;
    background:linear-gradient(
      90deg,
      rgba(0,0,0,0.45) 0%,
      rgba(0,0,0,0.30) 3px,
      rgba(0,0,0,0.18) 7px,
      rgba(0,0,0,0.08) 12px,
      rgba(0,0,0,0.03) 16px,
      transparent 18px
    );
    border-radius:14px 0 0 14px;
  }

  /* SVG ring (spiral wire) — extends OUTSIDE the page's left edge */
  .spiral{
    position:absolute;
    z-index:7;
    top:0;
    left:-30px;
    width:120px;
    height:100%;
    pointer-events:none;
    background-image: url("data:image/svg+xml;utf8,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='90'%20height='70'%20viewBox='0%200%2090%2070'%20fill='none'%3E%3Cpath%20d='M32%2027%20C20%2028%2010%2032%2010%2035%20C10%2040%2019%2043%2032%2044%20C52%2045%2070%2042%2082%2038'%20stroke='%23111'%20stroke-width='3'%20stroke-linecap='round'%20stroke-linejoin='round'/%3E%3Cpath%20d='M32%2034%20C20%2035%2010%2039%2010%2042%20C10%2047%2019%2050%2032%2051%20C52%2052%2070%2049%2082%2045'%20stroke='%23111'%20stroke-width='3'%20stroke-linecap='round'%20stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat: repeat-y;
    background-position: 2.5px 0;
    background-size: 76.5px 59.5px;
  }

  /* SVG hole — aligned with wire right extension end */
  .holes{
    position:absolute;
    z-index:4;
    top:0; left:-30px;
    width:120px;
    height:100%;
    pointer-events:none;
    background-image: url("data:image/svg+xml;utf8,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='76.5'%20height='59.5'%20viewBox='0%200%2076.5%2059.5'%3E%3Cdefs%3E%3CradialGradient%20id='h'%20cx='0%25'%20cy='45%25'%20r='105%25'%3E%3Cstop%20offset='0%25'%20stop-color='%23000'%20stop-opacity='0'/%3E%3Cstop%20offset='12%25'%20stop-color='%23000'%20stop-opacity='0'/%3E%3Cstop%20offset='28%25'%20stop-color='%23111'%20stop-opacity='.25'/%3E%3Cstop%20offset='42%25'%20stop-color='%23000'%20stop-opacity='.7'/%3E%3Cstop%20offset='55%25'%20stop-color='%23000'%20stop-opacity='.95'/%3E%3Cstop%20offset='70%25'%20stop-color='%23000'%20stop-opacity='1'/%3E%3Cstop%20offset='100%25'%20stop-color='%23000'%20stop-opacity='1'/%3E%3C/radialGradient%3E%3ClinearGradient%20id='r'%20x1='0'%20y1='0'%20x2='1'%20y2='0'%3E%3Cstop%20offset='0%25'%20stop-color='%23000'%20stop-opacity='0'/%3E%3Cstop%20offset='25%25'%20stop-color='%23000'%20stop-opacity='0'/%3E%3Cstop%20offset='40%25'%20stop-color='%23000'%20stop-opacity='.5'/%3E%3Cstop%20offset='55%25'%20stop-color='%23000'%20stop-opacity='.9'/%3E%3Cstop%20offset='70%25'%20stop-color='%23000'%20stop-opacity='1'/%3E%3Cstop%20offset='100%25'%20stop-color='%23000'%20stop-opacity='1'/%3E%3C/linearGradient%3E%3CclipPath%20id='c1'%3E%3Ccircle%20cx='66.7'%20cy='35.275'%20r='9'/%3E%3C/clipPath%3E%3C/defs%3E%3Ccircle%20cx='66.7'%20cy='35.275'%20r='9'%20fill='url(%23h)'/%3E%3Ccircle%20cx='66.7'%20cy='35.275'%20r='9'%20fill='url(%23r)'%20clip-path='url(%23c1)'/%3E%3Ccircle%20cx='66.7'%20cy='35.275'%20r='7'%20fill='%23000'/%3E%3Ccircle%20cx='66.7'%20cy='35.275'%20r='9'%20fill='none'%20stroke='%23000'%20stroke-width='0.5'%20opacity='.3'/%3E%3C/svg%3E");
    background-size:76.5px 59.5px;
    background-repeat:repeat-y;
    background-position:-0.5px 0;
  }

  /* (6) Page TOP edge — thin band showing page-stack thickness (3D block).
         Lighter cream at the very top (edge of paper stack), with subtle
         horizontal sheet lines, transitioning to the page color. A thin
         shadow line at the bottom of the band creates the 3D fold. */
  .page-top-edge{
    position:absolute;
    z-index:8;
    top:0; left:0; right:0;
    height:11px;
    pointer-events:none;
    background:
      /* Subtle horizontal sheet lines (stacked pages) */
      repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 2px,
        rgba(140,120,80,0.12) 2px,
        rgba(140,120,80,0.12) 2.4px
      ),
      /* Base gradient: lighter at top (edge), transitioning to page color */
      linear-gradient(
        to bottom,
        #fbf8ef 0%,
        #f7f3e8 55%,
        var(--paper) 100%
      );
    border-bottom:1px solid rgba(100,80,40,0.22);
    box-shadow:0 1px 2px rgba(0,0,0,0.10);
  }

  /* (7) Page BOTTOM edge — mirror of top edge. */
  .page-bottom-edge{
    position:absolute;
    z-index:8;
    bottom:0; left:0; right:0;
    height:11px;
    pointer-events:none;
    background:
      repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 2px,
        rgba(140,120,80,0.12) 2px,
        rgba(140,120,80,0.12) 2.4px
      ),
      linear-gradient(
        to top,
        #fbf8ef 0%,
        #f7f3e8 55%,
        var(--paper) 100%
      );
    border-top:1px solid rgba(100,80,40,0.22);
    box-shadow:0 -1px 2px rgba(0,0,0,0.10);
  }

  /* Content wrapper sits above grid */
  .content{position:relative;z-index:2;}

  /* ============================================================
     TOP STRIP — badges
     ============================================================ */
  .top-strip{
    display:flex;justify-content:flex-end;align-items:center;
    margin-bottom:6px;
  }

  .badges{display:flex;gap:10px;}
  .badge{
    background:var(--navy);
    color:#fff;
    font-size:11.5px;
    font-weight:700;
    letter-spacing:1.6px;
    padding:8px 16px;
    border-radius:999px;
    text-transform:uppercase;
    box-shadow:0 2px 4px rgba(21,38,77,0.25);
  }

  /* ============================================================
     TITLE BLOCK
     ============================================================ */
  .title-block{
    margin:22px 0 6px 0;
  }
  .title{
    font-size:46px;
    line-height:1.04;
    font-weight:800;
    color:var(--navy);
    letter-spacing:-0.6px;
    text-transform:uppercase;
  }
  .title .num{color:var(--navy);}
  .divider{
    display:flex;align-items:center;
    margin:14px 0 22px 0;
  }
  .divider .line{
    flex:1;height:2px;background:var(--navy);
  }
  .divider .dot{
    width:9px;height:9px;border-radius:50%;
    background:var(--navy);margin:0 10px;
  }

  /* ============================================================
     BODY — 2 column layout
     ============================================================ */
  .body{
    display:grid;
    grid-template-columns:1.85fr 1fr;
    gap:24px;
  }

  /* LEFT — list of rows */
  .rows{display:flex;flex-direction:column;gap:13px;}
  .row{
    display:grid;
    grid-template-columns:58px 1fr;
    gap:14px;
    align-items:flex-start;
    padding:10px 12px 10px 4px;
    border-bottom:1px dashed rgba(22,38,77,0.18);
  }
  .row:last-child{border-bottom:none;}
  .row .icon{
    width:58px;height:58px;
    display:flex;align-items:center;justify-content:center;
    border-radius:13px;
    background:#fff;
    border:1px solid rgba(22,38,77,0.10);
    box-shadow:0 2px 5px rgba(0,0,0,0.07);
  }
  .row .icon svg{width:36px;height:36px;display:block;}
  .row .text{padding-top:2px;}
  .row h3{
    font-size:13.5px;
    font-weight:800;
    letter-spacing:0.7px;
    color:var(--navy);
    text-transform:uppercase;
    margin-bottom:4px;
  }
  .row p{
    font-size:12.5px;
    line-height:1.5;
    color:var(--ink-2);
    font-weight:400;
  }

  /* Color tints per row icon background */
  .bg-blue{background:var(--blue-soft)!important;}
  .bg-green{background:var(--green-soft)!important;}
  .bg-purple{background:var(--purple-soft)!important;}
  .bg-red{background:var(--red-soft)!important;}
  .bg-gold{background:var(--gold-soft)!important;}

  /* RIGHT — sidebar boxes */
  .sidebar{display:flex;flex-direction:column;gap:14px;}
  .card{
    background:#fff;
    border-radius:14px;
    border:1px solid rgba(22,38,77,0.10);
    box-shadow:0 2px 6px rgba(0,0,0,0.05);
    overflow:hidden;
  }
  .card .head{
    background:var(--navy);
    color:#fff;
    font-size:12px;font-weight:700;letter-spacing:1.4px;
    text-transform:uppercase;
    padding:9px 14px;
  }
  .card .body-pad{padding:12px 14px 14px 14px;}

  /* file list rows in card 1 */
  .file-row{
    display:grid;grid-template-columns:30px 1fr;
    gap:10px;align-items:center;
    padding:6px 0;
  }
  .file-row + .file-row{border-top:1px solid rgba(22,38,77,0.07);}
  .file-row .ficon{width:28px;height:28px;display:flex;align-items:center;justify-content:center;}
  .file-row .ficon svg{width:24px;height:24px;}
  .file-row .ftext{line-height:1.25;}
  .file-row .fpath{font-size:12px;font-weight:700;color:var(--ink);font-family:"JetBrains Mono","Consolas",monospace;}
  .file-row .fdesc{font-size:10.5px;color:var(--ink-2);}

  .card .dashed{
    border-top:1.5px dashed rgba(22,38,77,0.30);
    margin:8px 0 8px 0;
  }
  .warn{
    display:grid;grid-template-columns:26px 1fr;gap:8px;align-items:center;
    padding:6px 4px 0 4px;
  }
  .warn svg{width:22px;height:22px;}
  .warn p{font-size:11px;color:var(--ink);font-weight:600;line-height:1.35;}

  /* card 2 — commands */
  .cmd-head-row{
    display:flex;align-items:center;gap:8px;
    padding:8px 14px;background:#f4f1ea;border-bottom:1px solid rgba(22,38,77,0.08);
  }
  .term-pill{
    display:inline-flex;align-items:center;
    background:var(--term-bg);color:var(--term-fg);
    font-family:"JetBrains Mono","Consolas",monospace;
    font-size:11px;font-weight:700;
    padding:3px 7px;border-radius:4px;
  }
  .term-pill .arrow{color:#7ee787;}
  .cmd-head-row span.lbl{font-size:11px;color:var(--ink-2);font-weight:600;letter-spacing:.4px;}
  .cmd-list{padding:6px 14px 12px 14px;display:flex;flex-direction:column;gap:6px;}
  .cmd-row{display:flex;flex-direction:column;gap:2px;padding:5px 0;border-bottom:1px dashed rgba(22,38,77,0.10);}
  .cmd-row:last-child{border-bottom:none;}
  .cmd-row code{
    font-family:"JetBrains Mono","Consolas",monospace;
    font-size:12.5px;font-weight:700;
    color:var(--navy);
    background:#eef1f8;
    border-radius:4px;padding:2px 6px;
    display:inline-block;
    white-space:pre;           /* Full command on one line, no wrapping */
    align-self:flex-start;    /* Don't stretch to full width */
    line-height:1.4;
    margin-bottom:0;
  }
  .cmd-row span{
    display:block;             /* Description on its own line below */
    font-size:11.5px;color:var(--ink-2);line-height:1.4;
    margin-top:1px;            /* Tight spacing below command */
  }

  /* ============================================================
     COVER PAGE — special layout
     ============================================================ */
  .cover{display:flex;flex-direction:column;height:100%;min-height:1100px;}
  .cover-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;}
  .cover-title{
    font-size:84px;line-height:0.96;font-weight:900;color:var(--navy);
    letter-spacing:-2px;text-transform:uppercase;margin-top:60px;
  }
  .cover-title .stack{display:block;}
  .cover-subtitle{
    font-size:18px;font-weight:600;color:var(--ink-2);letter-spacing:0.4px;
    margin-top:22px;line-height:1.4;max-width:680px;text-transform:uppercase;
  }
  .cover-divider{
    display:flex;align-items:center;margin:28px 0 30px 0;
  }
  .cover-divider .line{flex:1;height:3px;background:var(--navy);}
  .cover-divider .dot{width:13px;height:13px;border-radius:50%;background:var(--navy);margin:0 14px;}

  .topic-grid{
    display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:14px;
  }
  .topic-card{
    background:#fff;border-radius:14px;
    border:1px solid rgba(22,38,77,0.10);
    box-shadow:0 3px 10px rgba(0,0,0,0.06);
    padding:18px 16px;display:flex;flex-direction:column;gap:10px;align-items:flex-start;
  }
  .topic-card .tic{
    width:46px;height:46px;border-radius:11px;display:flex;align-items:center;justify-content:center;
  }
  .topic-card .tic svg{width:30px;height:30px;display:block;}
  .topic-card .tlabel{font-size:12px;font-weight:800;letter-spacing:1px;color:var(--navy);text-transform:uppercase;line-height:1.25;}

  .cover-tagline{
    margin-top:auto;padding-top:30px;
    text-align:center;
  }
  .cover-tagline .big{
    font-size:30px;font-weight:900;color:var(--navy);letter-spacing:1px;text-transform:uppercase;line-height:1.15;
  }
  .cover-tagline .row-pills{
    display:flex;justify-content:center;gap:18px;margin-top:18px;flex-wrap:wrap;
  }
  .cover-tagline .pill{
    display:inline-flex;align-items:center;gap:8px;
    background:var(--navy);color:#fff;
    padding:9px 18px;border-radius:999px;
    font-size:11.5px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;
    box-shadow:0 2px 5px rgba(21,38,77,0.25);
  }
  .cover-tagline .pill .psvg{width:14px;height:14px;display:inline-block;}
  .cover-tagline .sub{font-size:13px;color:var(--ink-2);margin-top:14px;letter-spacing:0.5px;}

  /* ============================================================
     STEPS grid (used by page 20 — incident investigation)
     ============================================================ */
  .steps-grid{
    display:grid;grid-template-columns:1fr 1fr;gap:10px;
  }
  .step{
    background:#fff;border-radius:11px;
    border:1px solid rgba(22,38,77,0.10);
    box-shadow:0 1px 4px rgba(0,0,0,0.05);
    padding:11px 13px;display:flex;flex-direction:column;gap:6px;
  }
  .step .shead{display:flex;align-items:center;gap:8px;}
  .step .snum{
    width:24px;height:24px;border-radius:50%;background:var(--navy);color:#fff;
    font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0;
  }
  .step .stitle{font-size:11.5px;font-weight:800;letter-spacing:0.7px;color:var(--navy);text-transform:uppercase;line-height:1.2;}
  .step .scode{
    font-family:"JetBrains Mono","Consolas",monospace;
    background:var(--term-bg);color:var(--term-fg);
    font-size:10.5px;font-weight:600;
    padding:6px 8px;border-radius:5px;line-height:1.4;word-break:break-word;
  }
  .step.full{grid-column:1 / -1;}
  .steps-grid .step:nth-last-child(1):nth-child(odd){grid-column:1 / -1;}

  /* generic tip box (sidebar) */
  .tip-list{display:flex;flex-direction:column;gap:6px;padding:10px 14px 12px 14px;}
  .tip-item{
    display:grid;grid-template-columns:18px 1fr;gap:8px;align-items:flex-start;
    padding:4px 0;border-bottom:1px dashed rgba(22,38,77,0.10);
  }
  .tip-item:last-child{border-bottom:none;}
  .tip-item .dot-b{
    width:8px;height:8px;border-radius:50%;background:var(--navy);margin-top:5px;
  }
  .tip-item p{font-size:11.5px;color:var(--ink);line-height:1.4;font-weight:500;}

  /* config table (for sshd_config & similar) */
  .cfg-block{
    background:var(--term-bg);color:var(--term-fg);
    font-family:"JetBrains Mono","Consolas",monospace;
    font-size:11.5px;line-height:1.6;
    padding:11px 14px;border-radius:8px;
    margin:10px 14px 12px 14px;
  }
  .cfg-block .k{color:#79c0ff;}
  .cfg-block .v{color:#7ee787;}
  .cfg-block .c{color:#8b949e;font-style:italic;}

  /* generic numbered list inside cards */
  .num-list{padding:10px 14px 12px 14px;display:flex;flex-direction:column;gap:7px;}
  .num-item{display:grid;grid-template-columns:22px 1fr;gap:8px;align-items:flex-start;padding:3px 0;border-bottom:1px dashed rgba(22,38,77,0.10);}
  .num-item:last-child{border-bottom:none;}
  .num-item .ni-n{font-size:11px;font-weight:800;color:var(--navy);}
  .num-item p{font-size:11.5px;color:var(--ink);line-height:1.4;}

  /* ============================================================
     PRINT / PDF
     ============================================================ */
  @page{
    size:1080px 1353px;   /* matches design aspect ratio */
    margin:0;
  }
  @media print{
    html,body{background:#fff;padding:0;gap:0;}
    .page{
      box-shadow:none;
      border-radius:0;
      width:1080px;
      page-break-after:always;
    }
    .page:last-child{page-break-after:auto;}
  }
"""

# ============================================================================
# ICON LIBRARY — multi-color filled inline SVGs (matching reference style)
# Each icon is a function returning the SVG markup (no wrapper).
# Colors use the same HEX values as the reference.
# ============================================================================

NAVY = "#15264d"
BLUE = "#2563eb"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
RED = "#dc2626"
GOLD = "#e0a517"
GOLD_DK = "#a9780d"
ORANGE = "#ef6c00"
TEAL = "#0d9488"
PINK = "#db2777"
SLATE = "#475569"

SVG_OPEN = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
SVG_CLOSE = "</svg>"


def _svg(inner: str) -> str:
    return SVG_OPEN + inner + SVG_CLOSE


# ---- People / Users (blue + green, two figures) ----
def icon_users() -> str:
    return _svg(
        '<circle cx="9" cy="8" r="3.4" fill="#2563eb"/>'
        '<circle cx="15.5" cy="9" r="2.7" fill="#16a34a"/>'
        '<path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M13.5 20c0-2.5 1.8-4.5 4-4.5s4 2 4 4.5" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round"/>'
    )


# ---- File document (color-parametric, with text lines) ----
def icon_file(color: str = BLUE) -> str:
    return _svg(
        f'<path d="M6 2.5h9l4 4v15h-13z" fill="#ffffff" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<path d="M15 2.5v4h4" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<line x1="8.5" y1="10" x2="16" y2="10" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<line x1="8.5" y1="12.8" x2="16" y2="12.8" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<line x1="8.5" y1="15.6" x2="13" y2="15.6" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<rect x="6" y="18" width="13" height="3.5" rx="1" fill="{color}"/>'
    )


# ---- File document with colored content rects (green variant) ----
def icon_file_rects(color: str = GREEN) -> str:
    return _svg(
        f'<path d="M6 2.5h9l4 4v15h-13z" fill="#ffffff" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<path d="M15 2.5v4h4" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<rect x="8.5" y="9.4" width="7.5" height="2" rx="1" fill="{color}"/>'
        f'<rect x="8.5" y="12.4" width="7.5" height="2" rx="1" fill="{color}"/>'
        f'<rect x="8.5" y="15.4" width="4.5" height="2" rx="1" fill="{color}"/>'
        f'<rect x="6" y="18" width="13" height="3.5" rx="1" fill="{color}"/>'
    )


# ---- Shield with person inside (solid fill + white inner symbol) ----
def icon_shield_person(color: str = BLUE, dark: str = "#1e40af") -> str:
    return _svg(
        f'<path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" '
        f'fill="{color}" stroke="{dark}" stroke-width="1.2" stroke-linejoin="round"/>'
        '<circle cx="12" cy="10.5" r="2.4" fill="#ffffff"/>'
        '<path d="M8 17 c0-2.6 1.8-4.2 4-4.2 s4 1.6 4 4.2 z" fill="#ffffff"/>'
    )


# ---- Shield with checkmark (used for hardening / validation) ----
def icon_shield_check(color: str = GREEN, dark: str = "#15803d") -> str:
    return _svg(
        f'<path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" '
        f'fill="{color}" stroke="{dark}" stroke-width="1.2" stroke-linejoin="round"/>'
        '<path d="M8.5 11.5 L11 14 L16 9" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
    )


# ---- Magnifying glass (gold stroke) ----
def icon_magnifier(color: str = GOLD) -> str:
    return _svg(
        f'<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="{color}" stroke-width="2.4"/>'
        f'<line x1="15.5" y1="15.5" x2="20" y2="20" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/>'
        f'<circle cx="10.5" cy="10.5" r="3.2" fill="none" stroke="{color}" stroke-width="1.3"/>'
    )


# ---- Magnifying glass with exclamation (audit / investigation) ----
def icon_magnifier_alert(color: str = RED) -> str:
    return _svg(
        f'<circle cx="10" cy="10" r="7" fill="none" stroke="{color}" stroke-width="2.2"/>'
        f'<line x1="15" y1="15" x2="20" y2="20" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/>'
        f'<line x1="10" y1="6.5" x2="10" y2="11" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="10" cy="13.5" r="1.1" fill="{color}"/>'
    )


# ---- Padlock (red fill + white keyhole) ----
def icon_padlock(color: str = RED) -> str:
    return _svg(
        f'<path d="M7 10 V8 a5 5 0 0 1 10 0 V10" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>'
        f'<rect x="5" y="10" width="14" height="10" rx="2.4" fill="{color}"/>'
        '<circle cx="12" cy="14.5" r="1.5" fill="#ffffff"/>'
        '<rect x="11.2" y="14.5" width="1.6" height="3" fill="#ffffff" rx="0.5"/>'
    )


# ---- Crown (gold fill + dark details) ----
def icon_crown(color: str = GOLD, dark: str = GOLD_DK) -> str:
    return _svg(
        f'<path d="M3 8 L7 13 L12 6 L17 13 L21 8 L19 18 H5 Z" '
        f'fill="{color}" stroke="{dark}" stroke-width="1.1" stroke-linejoin="round"/>'
        f'<circle cx="3" cy="8" r="1.3" fill="{dark}"/>'
        f'<circle cx="12" cy="6" r="1.3" fill="{dark}"/>'
        f'<circle cx="21" cy="8" r="1.3" fill="{dark}"/>'
        f'<rect x="5" y="18.5" width="14" height="2" rx="0.5" fill="{dark}"/>'
    )


# ---- Terminal (dark bg + green text + colored dots) ----
def icon_terminal() -> str:
    return _svg(
        '<rect x="2.5" y="4" width="19" height="16" rx="2.2" fill="#0d1117"/>'
        '<rect x="2.5" y="4" width="19" height="3" rx="2.2" fill="#1c2230"/>'
        '<circle cx="5" cy="5.5" r="0.6" fill="#ff5f56"/>'
        '<circle cx="6.8" cy="5.5" r="0.6" fill="#ffbd2e"/>'
        '<circle cx="8.6" cy="5.5" r="0.6" fill="#27c93f"/>'
        '<path d="M6 11 L9 13.5 L6 16" fill="none" stroke="#7ee787" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<line x1="11" y1="16" x2="17" y2="16" stroke="#e6edf3" stroke-width="1.6" stroke-linecap="round"/>'
    )


# ---- Layers / stack (defense in depth) ----
def icon_layers(color: str = PURPLE) -> str:
    return _svg(
        f'<path d="M12 2 L21 7 L12 12 L3 7 Z" fill="{color}" opacity="0.9"/>'
        f'<path d="M3 12 L12 17 L21 12" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<path d="M3 17 L12 22 L21 17" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
    )


# ---- Network globe (network exposure) ----
def icon_globe(color: str = BLUE) -> str:
    return _svg(
        f'<circle cx="12" cy="12" r="9" fill="none" stroke="{color}" stroke-width="1.8"/>'
        f'<ellipse cx="12" cy="12" rx="4" ry="9" fill="none" stroke="{color}" stroke-width="1.5"/>'
        f'<line x1="3" y1="12" x2="21" y2="12" stroke="{color}" stroke-width="1.5"/>'
        f'<line x1="5" y1="6.5" x2="19" y2="6.5" stroke="{color}" stroke-width="1.2" opacity="0.7"/>'
        f'<line x1="5" y1="17.5" x2="19" y2="17.5" stroke="{color}" stroke-width="1.2" opacity="0.7"/>'
    )


# ---- Brick wall / firewall ----
def icon_wall(color: str = ORANGE) -> str:
    return _svg(
        f'<rect x="2.5" y="4" width="19" height="16" rx="1.5" fill="none" stroke="{color}" stroke-width="1.8"/>'
        f'<line x1="2.5" y1="9.3" x2="21.5" y2="9.3" stroke="{color}" stroke-width="1.6"/>'
        f'<line x1="2.5" y1="14.7" x2="21.5" y2="14.7" stroke="{color}" stroke-width="1.6"/>'
        f'<line x1="9" y1="4" x2="9" y2="9.3" stroke="{color}" stroke-width="1.6"/>'
        f'<line x1="15" y1="4" x2="15" y2="9.3" stroke="{color}" stroke-width="1.6"/>'
        f'<line x1="6" y1="9.3" x2="6" y2="14.7" stroke="{color}" stroke-width="1.6"/>'
        f'<line x1="12" y1="9.3" x2="12" y2="14.7" stroke="{color}" stroke-width="1.6"/>'
        f'<line x1="18" y1="9.3" x2="18" y2="14.7" stroke="{color}" stroke-width="1.6"/>'
        f'<line x1="9" y1="14.7" x2="9" y2="20" stroke="{color}" stroke-width="1.6"/>'
        f'<line x1="15" y1="14.7" x2="15" y2="20" stroke="{color}" stroke-width="1.6"/>'
    )


# ---- Gear / cog (processes, runtime) ----
def icon_gear(color: str = SLATE) -> str:
    return _svg(
        f'<path d="M12 8.5 L12 4 L13.5 4 L13.5 8.5 Z" fill="{color}"/>'
        f'<path d="M12 15.5 L12 20 L10.5 20 L10.5 15.5 Z" fill="{color}"/>'
        f'<path d="M8.5 12 L4 12 L4 10.5 L8.5 10.5 Z" fill="{color}"/>'
        f'<path d="M15.5 12 L20 12 L20 13.5 L15.5 13.5 Z" fill="{color}"/>'
        f'<circle cx="12" cy="12" r="5.5" fill="none" stroke="{color}" stroke-width="2"/>'
        f'<circle cx="12" cy="12" r="2.2" fill="{color}"/>'
    )


# ---- Log document with lines (logging) ----
def icon_log(color: str = TEAL) -> str:
    return _svg(
        f'<rect x="3.5" y="3" width="17" height="18" rx="1.6" fill="none" stroke="{color}" stroke-width="1.8"/>'
        f'<line x1="6.5" y1="7.5" x2="17.5" y2="7.5" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<line x1="6.5" y1="10.5" x2="17.5" y2="10.5" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<line x1="6.5" y1="13.5" x2="14" y2="13.5" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<rect x="6.5" y="15.5" width="11" height="3" rx="0.8" fill="{color}" opacity="0.6"/>'
    )


# ---- Eye (auditing / monitoring) ----
def icon_eye(color: str = PURPLE) -> str:
    return _svg(
        f'<path d="M2 12 C5 7 9 5 12 5 C15 5 19 7 22 12 C19 17 15 19 12 19 C9 19 5 17 2 12 Z" '
        f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<circle cx="12" cy="12" r="3.5" fill="{color}"/>'
        '<circle cx="12" cy="12" r="1.5" fill="#ffffff"/>'
    )


# ---- Key (secrets / credentials) ----
def icon_key(color: str = GOLD) -> str:
    return _svg(
        f'<circle cx="8" cy="8" r="4" fill="none" stroke="{color}" stroke-width="2"/>'
        f'<circle cx="8" cy="8" r="1.4" fill="{color}"/>'
        f'<line x1="11" y1="11" x2="20" y2="20" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>'
        f'<line x1="16" y1="16" x2="19" y2="13" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>'
        f'<line x1="18" y1="18" x2="20" y2="16" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>'
    )


# ---- Database cylinder (secrets storage) ----
def icon_database(color: str = BLUE) -> str:
    return _svg(
        f'<ellipse cx="12" cy="5.5" rx="7.5" ry="2.5" fill="none" stroke="{color}" stroke-width="1.8"/>'
        f'<path d="M4.5 5.5 V18 a7.5 2.5 0 0 0 15 0 V5.5" fill="none" stroke="{color}" stroke-width="1.8"/>'
        f'<path d="M4.5 9.5 a7.5 2.5 0 0 0 15 0" fill="none" stroke="{color}" stroke-width="1.4" opacity="0.7"/>'
        f'<path d="M4.5 13.5 a7.5 2.5 0 0 0 15 0" fill="none" stroke="{color}" stroke-width="1.4" opacity="0.7"/>'
    )


# ---- Package / box (package security) ----
def icon_package(color: str = ORANGE) -> str:
    return _svg(
        f'<path d="M12 2 L21 6.5 V17.5 L12 22 L3 17.5 V6.5 Z" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<path d="M3 6.5 L12 11 L21 6.5" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<line x1="12" y1="11" x2="12" y2="22" stroke="{color}" stroke-width="1.6"/>'
        f'<path d="M7.5 4.2 L16.5 9" stroke="{color}" stroke-width="1.4" opacity="0.7" stroke-linecap="round"/>'
    )


# ---- Server box (services / systemd) ----
def icon_server(color: str = GREEN) -> str:
    return _svg(
        f'<rect x="3" y="3.5" width="18" height="7" rx="1.5" fill="none" stroke="{color}" stroke-width="1.7"/>'
        f'<rect x="3" y="13.5" width="18" height="7" rx="1.5" fill="none" stroke="{color}" stroke-width="1.7"/>'
        f'<circle cx="6.5" cy="7" r="1" fill="{color}"/>'
        f'<circle cx="6.5" cy="17" r="1" fill="{color}"/>'
        f'<line x1="10" y1="7" x2="18" y2="7" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<line x1="10" y1="17" x2="18" y2="17" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
    )


# ---- Bell / alert (auditing alerts) ----
def icon_bell(color: str = RED) -> str:
    return _svg(
        f'<path d="M6 16 C6 11 8 6 12 6 C16 6 18 11 18 16 L20 18 H4 Z" fill="{color}"/>'
        f'<path d="M10 18 a2 2 0 0 0 4 0" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<line x1="12" y1="3" x2="12" y2="5" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
    )


# ---- Clock (session timeout) ----
def icon_clock(color: str = PURPLE) -> str:
    return _svg(
        f'<circle cx="12" cy="12" r="9" fill="none" stroke="{color}" stroke-width="1.9"/>'
        f'<path d="M12 6.5 V12 L16 14.2" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    )


# ---- Folder (directories) ----
def icon_folder(color: str = GOLD) -> str:
    return _svg(
        f'<path d="M2.5 6.5 L9 6.5 L11 8.5 L21.5 8.5 V19 H2.5 Z" fill="{color}" opacity="0.9" stroke="{GOLD_DK}" stroke-width="1.2" stroke-linejoin="round"/>'
        f'<path d="M2.5 10.5 H21.5" stroke="#ffffff" stroke-width="1" opacity="0.4"/>'
    )


# ---- Hash / fingerprint (file integrity) ----
def icon_hash(color: str = TEAL) -> str:
    return _svg(
        f'<line x1="6" y1="5" x2="6" y2="19" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
        f'<line x1="18" y1="5" x2="18" y2="19" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
        f'<line x1="3" y1="9" x2="21" y2="9" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
        f'<line x1="3" y1="15" x2="21" y2="15" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
        f'<line x1="9" y1="5" x2="9" y2="19" stroke="{color}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>'
        f'<line x1="15" y1="5" x2="15" y2="19" stroke="{color}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>'
    )


# ---- Checklist (hardening baseline) ----
def icon_checklist(color: str = GREEN) -> str:
    return _svg(
        f'<rect x="3.5" y="2.5" width="17" height="19" rx="1.8" fill="none" stroke="{color}" stroke-width="1.7"/>'
        f'<rect x="6" y="6" width="3.5" height="3.5" rx="0.6" fill="none" stroke="{color}" stroke-width="1.5"/>'
        f'<path d="M6.6 7.7 L7.6 8.7 L9 6.8" fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<rect x="6" y="11.5" width="3.5" height="3.5" rx="0.6" fill="none" stroke="{color}" stroke-width="1.5"/>'
        f'<path d="M6.6 12.7 L7.6 13.7 L9 11.8" fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<rect x="6" y="17" width="3.5" height="3.5" rx="0.6" fill="none" stroke="{color}" stroke-width="1.5"/>'
        f'<line x1="11" y1="7.7" x2="18" y2="7.7" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<line x1="11" y1="13.2" x2="18" y2="13.2" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<line x1="11" y1="18.7" x2="18" y2="18.7" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
    )


# ---- Network nodes (sockets / ports) ----
def icon_nodes(color: str = BLUE) -> str:
    return _svg(
        f'<circle cx="6" cy="6" r="2.2" fill="{color}"/>'
        f'<circle cx="18" cy="6" r="2.2" fill="{color}"/>'
        f'<circle cx="6" cy="18" r="2.2" fill="{color}"/>'
        f'<circle cx="18" cy="18" r="2.2" fill="{color}"/>'
        f'<circle cx="12" cy="12" r="2.5" fill="{color}"/>'
        f'<line x1="8" y1="6" x2="16" y2="6" stroke="{color}" stroke-width="1.5"/>'
        f'<line x1="8" y1="18" x2="16" y2="18" stroke="{color}" stroke-width="1.5"/>'
        f'<line x1="6" y1="8" x2="6" y2="16" stroke="{color}" stroke-width="1.5"/>'
        f'<line x1="18" y1="8" x2="18" y2="16" stroke="{color}" stroke-width="1.5"/>'
        f'<line x1="8" y1="8" x2="10.5" y2="10.5" stroke="{color}" stroke-width="1.4"/>'
        f'<line x1="16" y1="8" x2="13.5" y2="10.5" stroke="{color}" stroke-width="1.4"/>'
        f'<line x1="8" y1="16" x2="10.5" y2="13.5" stroke="{color}" stroke-width="1.4"/>'
        f'<line x1="16" y1="16" x2="13.5" y2="13.5" stroke="{color}" stroke-width="1.4"/>'
    )


# ---- Bug (threat / vulnerability) ----
def icon_bug(color: str = RED) -> str:
    return _svg(
        f'<ellipse cx="12" cy="13" rx="4.5" ry="6" fill="{color}"/>'
        f'<line x1="12" y1="9" x2="12" y2="19" stroke="#ffffff" stroke-width="1.4"/>'
        f'<line x1="6" y1="9" x2="9" y2="11" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="18" y1="9" x2="15" y2="11" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="6" y1="14" x2="8.5" y2="14" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="18" y1="14" x2="15.5" y2="14" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="6" y1="18" x2="9" y2="17" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="18" y1="18" x2="15" y2="17" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<circle cx="10" cy="6" r="1.3" fill="{color}"/>'
        f'<circle cx="14" cy="6" r="1.3" fill="{color}"/>'
    )


# ---- Wrench / settings (configuration) ----
def icon_wrench(color: str = SLATE) -> str:
    return _svg(
        f'<path d="M14 4 a4 4 0 0 0 -5 5 L4 14 V20 H10 L15 15 a4 4 0 0 0 5 -5 L17 13 L13 9 Z" '
        f'fill="{color}" stroke="{color}" stroke-width="0.8" stroke-linejoin="round"/>'
    )


# ---- Lightning (privilege escalation / risk) ----
def icon_lightning(color: str = GOLD) -> str:
    return _svg(
        f'<path d="M13 2 L4 13 H11 L9 22 L20 9 H13 Z" fill="{color}" stroke="{GOLD_DK}" stroke-width="1" stroke-linejoin="round"/>'
    )


# ---- Document with magnifier (audit log) ----
def icon_doc_search(color: str = PURPLE) -> str:
    return _svg(
        f'<path d="M6 2.5h9l4 4v15h-13z" fill="#ffffff" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<path d="M15 2.5v4h4" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<line x1="8.5" y1="10" x2="14" y2="10" stroke="{color}" stroke-width="1.3" stroke-linecap="round"/>'
        f'<line x1="8.5" y1="12.6" x2="13" y2="12.6" stroke="{color}" stroke-width="1.3" stroke-linecap="round"/>'
        f'<circle cx="15.5" cy="16.5" r="3" fill="none" stroke="{GOLD}" stroke-width="1.6"/>'
        f'<line x1="17.5" y1="18.5" x2="20" y2="21" stroke="{GOLD}" stroke-width="1.9" stroke-linecap="round"/>'
    )


# ---- Star (privilege / privileged) ----
def icon_star(color: str = GOLD) -> str:
    return _svg(
        f'<path d="M12 2 L14.5 9 L22 9 L16 13.5 L18.5 21 L12 16.5 L5.5 21 L8 13.5 L2 9 L9.5 9 Z" '
        f'fill="{color}" stroke="{GOLD_DK}" stroke-width="1" stroke-linejoin="round"/>'
    )


# ---- Shield with lock (SELinux / AppArmor) ----
def icon_shield_lock(color: str = PURPLE, dark: str = "#5b21b6") -> str:
    return _svg(
        f'<path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" '
        f'fill="{color}" stroke="{dark}" stroke-width="1.2" stroke-linejoin="round"/>'
        '<rect x="8.5" y="11.5" width="7" height="6" rx="1.2" fill="#ffffff"/>'
        '<path d="M9.8 11.5 V9.5 a2.2 2.2 0 0 1 4.4 0 V11.5" fill="none" stroke="#ffffff" stroke-width="1.4"/>'
        f'<circle cx="12" cy="14.5" r="0.9" fill="{color}"/>'
    )


# ---- Image/photo (forensic capture) ----
def icon_camera(color: str = SLATE) -> str:
    return _svg(
        f'<rect x="2.5" y="6" width="19" height="13" rx="2" fill="none" stroke="{color}" stroke-width="1.7"/>'
        f'<path d="M8 6 L9 3.5 H15 L16 6" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<circle cx="12" cy="12.5" r="3.2" fill="none" stroke="{color}" stroke-width="1.6"/>'
        f'<circle cx="12" cy="12.5" r="1.4" fill="{color}"/>'
    )


# ---- Fingerprint (file integrity) ----
def icon_fingerprint(color: str = TEAL) -> str:
    return _svg(
        f'<path d="M8 5 C5 7 4 10 4 13" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<path d="M16 5 C19 7 20 10 20 13" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<path d="M6 11 C6 9 7 7 9 6" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<path d="M18 11 C18 9 17 7 15 6" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<path d="M9 13 C9 10 10 8 12 8 C14 8 15 10 15 13 V16" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round"/>'
        f'<path d="M12 13 V17" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round"/>'
        f'<path d="M8 14 V17" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<path d="M16 14 V17" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
    )


# ---- Settings sliders (systemd / config) ----
def icon_sliders(color: str = BLUE) -> str:
    return _svg(
        f'<line x1="4" y1="6" x2="20" y2="6" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="4" y1="12" x2="20" y2="12" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="4" y1="18" x2="20" y2="18" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<circle cx="9" cy="6" r="2" fill="#ffffff" stroke="{color}" stroke-width="1.6"/>'
        f'<circle cx="15" cy="12" r="2" fill="#ffffff" stroke="{color}" stroke-width="1.6"/>'
        f'<circle cx="8" cy="18" r="2" fill="#ffffff" stroke="{color}" stroke-width="1.6"/>'
    )


# ---- Refresh / restart (restart policies) ----
def icon_refresh(color: str = GREEN) -> str:
    return _svg(
        f'<path d="M19 8 A8 8 0 1 0 20 14" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M20 4 V9 H15" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    )


# ---- Lock-open (login restrictions / disabled) ----
def icon_lock_open(color: str = ORANGE) -> str:
    return _svg(
        f'<path d="M7 10 V8 a5 5 0 0 1 9 -2" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>'
        f'<rect x="5" y="10" width="14" height="10" rx="2.4" fill="{color}"/>'
        '<circle cx="12" cy="14.5" r="1.5" fill="#ffffff"/>'
        '<rect x="11.2" y="14.5" width="1.6" height="3" fill="#ffffff" rx="0.5"/>'
    )


# ---- Sandbox / box isolation (service isolation) ----
def icon_sandbox(color: str = PURPLE) -> str:
    return _svg(
        f'<rect x="3" y="3" width="18" height="18" rx="2" fill="none" stroke="{color}" stroke-width="1.6"/>'
        f'<rect x="7" y="7" width="10" height="10" rx="1.5" fill="{color}" opacity="0.7"/>'
        f'<line x1="3" y1="3" x2="7" y2="7" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<line x1="21" y1="3" x2="17" y2="7" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<line x1="3" y1="21" x2="7" y2="17" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<line x1="21" y1="21" x2="17" y2="17" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/>'
    )


# ---- Tag / label (signature) ----
def icon_tag(color: str = BLUE) -> str:
    return _svg(
        f'<path d="M3 3 H11 L21 13 L13 21 L3 11 Z" fill="none" stroke="{color}" stroke-width="1.7" stroke-linejoin="round"/>'
        f'<circle cx="7.5" cy="7.5" r="1.6" fill="{color}"/>'
    )


# ---- Download / patch (security updates) ----
def icon_download(color: str = GREEN) -> str:
    return _svg(
        f'<path d="M12 3 V14" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>'
        f'<path d="M7 10 L12 15 L17 10" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M4 18 H20 V21 H4 Z" fill="{color}"/>'
    )


# ---- Brain /wrench (hardening) ----
def icon_shield_grid(color: str = NAVY) -> str:
    return _svg(
        f'<path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" '
        f'fill="{color}" stroke="{NAVY}" stroke-width="1.2" stroke-linejoin="round"/>'
        '<rect x="8" y="8" width="3" height="3" fill="#ffffff"/>'
        '<rect x="13" y="8" width="3" height="3" fill="#ffffff"/>'
        '<rect x="8" y="13" width="3" height="3" fill="#ffffff"/>'
        '<rect x="13" y="13" width="3" height="3" fill="#ffffff"/>'
    )


# ---- Cylinder /etc/shadow (encrypted secrets) ----
def icon_vault(color: str = GOLD) -> str:
    return _svg(
        f'<rect x="4" y="4" width="16" height="16" rx="2" fill="none" stroke="{color}" stroke-width="1.8"/>'
        f'<circle cx="12" cy="12" r="3.5" fill="none" stroke="{color}" stroke-width="1.8"/>'
        f'<circle cx="12" cy="12" r="1.2" fill="{color}"/>'
        f'<line x1="12" y1="4" x2="12" y2="6" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="12" y1="18" x2="12" y2="20" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="4" y1="12" x2="6" y2="12" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<line x1="18" y1="12" x2="20" y2="12" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>'
    )


# ---- Bookmark / pin (persistence) ----
def icon_bookmark(color: str = RED) -> str:
    return _svg(
        f'<path d="M6 3 H18 V21 L12 16 L6 21 Z" fill="{color}" stroke="{color}" stroke-width="1.2" stroke-linejoin="round"/>'
    )


# ---- Topic-grid icons for the cover (smaller, used inside .topic-card) ----
def topic_icon_access() -> str:  # Access control — keyhole in shield
    return _svg(
        f'<path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" fill="{BLUE}"/>'
        '<circle cx="12" cy="11" r="1.7" fill="#ffffff"/>'
        '<rect x="11.3" y="11" width="1.4" height="3" fill="#ffffff" rx="0.4"/>'
    )


def topic_icon_auth() -> str:  # Authentication — fingerprint
    return icon_fingerprint(PURPLE)


def topic_icon_firewall() -> str:  # Firewall — brick wall
    return icon_wall(ORANGE)


def topic_icon_hardening() -> str:  # System hardening — shield check
    return icon_shield_check(GREEN)


def topic_icon_perms() -> str:  # File permissions — file with bars
    return _svg(
        f'<path d="M6 2.5h9l4 4v15h-13z" fill="#ffffff" stroke="{GOLD}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<path d="M15 2.5v4h4" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<rect x="8.5" y="9.5" width="7.5" height="1.7" rx="0.8" fill="{GOLD}"/>'
        f'<rect x="8.5" y="12.2" width="7.5" height="1.7" rx="0.8" fill="{GOLD}"/>'
        f'<rect x="8.5" y="14.9" width="4.5" height="1.7" rx="0.8" fill="{GOLD}"/>'
    )


def topic_icon_compliance() -> str:  # Compliance — checklist
    return icon_checklist(BLUE)


def topic_icon_audit() -> str:  # Auditing & logging — eye
    return icon_eye(PURPLE)


def topic_icon_monitoring() -> str:  # Monitoring — bell
    return icon_bell(RED)


# ============================================================================
# PAGE-ELEMENT BUILDERS
# ============================================================================


def esc(s: str) -> str:
    return _html.escape(s, quote=False)


def page_wrapper(inner_html: str) -> str:
    """Wrap inner content in the standard page-wrapper structure."""
    return (
        '<div class="page-wrapper">\n'
        '  <div class="holes" aria-hidden="true"></div>\n'
        '  <div class="spiral" aria-hidden="true"></div>\n'
        '  <div class="page-bend" aria-hidden="true"></div>\n'
        '  <div class="page">\n'
        '    <div class="page-top-edge" aria-hidden="true"></div>\n'
        '    <div class="page-bottom-edge" aria-hidden="true"></div>\n'
        f'    <div class="content">\n{inner_html}\n    </div>\n'
        '  </div>\n'
        '</div>'
    )


def top_strip(page_label: str | None) -> str:
    """Top strip with two badges. If page_label is None, only the handbook badge is shown."""
    if page_label:
        badges = (
            '<span class="badge">LINUX SECURITY HANDBOOK</span>\n'
            f'        <span class="badge">{esc(page_label)}</span>'
        )
    else:
        badges = '<span class="badge">LINUX SECURITY HANDBOOK</span>'
    return (
        '<div class="top-strip">\n'
        f'      <div class="badges">\n        {badges}\n      </div>\n'
        '    </div>'
    )


def title_block(title_html: str) -> str:
    """Title block with the title and divider. title_html may contain <br>."""
    return (
        '<div class="title-block">\n'
        f'      <h1 class="title">{title_html}</h1>\n'
        '    </div>\n'
        '    <div class="divider">\n'
        '      <span class="line"></span><span class="dot"></span><span class="line"></span>\n'
        '    </div>'
    )


def row(icon_html: str, h3: str, p: str, bg_class: str = "") -> str:
    """A single row: icon (58x58 box with SVG) + h3 + p."""
    cls = f'icon {bg_class}'.strip()
    return (
        '<div class="row">\n'
        f'          <div class="{cls}">\n            {icon_html}\n          </div>\n'
        '          <div class="text">\n'
        f'            <h3>{esc(h3)}</h3>\n'
        f'            <p>{esc(p)}</p>\n'
        '          </div>\n'
        '        </div>'
    )


def rows(items: list[dict]) -> str:
    """Render a list of row dicts. Each item: {icon, h3, p, bg}."""
    out = ['<div class="rows">']
    for it in items:
        out.append(row(it["icon"], it["h3"], it["p"], it.get("bg", "")))
    out.append('</div>')
    return "\n".join(out)


def sidebar(cards: list[str]) -> str:
    """Wrap a list of card HTML strings into the sidebar."""
    inner = "\n\n".join(cards)
    return f'<div class="sidebar">\n\n{inner}\n\n      </div>'


def card_file_list(head: str, files: list[dict], warn_text: str | None = None) -> str:
    """Card with a list of file rows. Each file: {icon, path, desc}."""
    file_rows = []
    for f in files:
        file_rows.append(
            '<div class="file-row">\n'
            f'              <div class="ficon">\n                {f["icon"]}\n              </div>\n'
            '              <div class="ftext">\n'
            f'                <div class="fpath">{esc(f["path"])}</div>\n'
            f'                <div class="fdesc">{esc(f["desc"])}</div>\n'
            '              </div>\n'
            '            </div>'
        )
    body = "\n\n            ".join(file_rows)
    if warn_text:
        warn_block = (
            '\n\n            <div class="dashed"></div>\n\n'
            '            <div class="warn">\n'
            '              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">\n'
            f'                <path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" fill="{BLUE}"/>\n'
            '                <rect x="8.5" y="11.5" width="7" height="6" rx="1.5" fill="#ffffff"/>\n'
            '                <path d="M9.8 11.5 V9.5 a2.2 2.2 0 0 1 4.4 0 V11.5" fill="none" stroke="#ffffff" stroke-width="1.4"/>\n'
            f'                <circle cx="12" cy="14.5" r="0.9" fill="{BLUE}"/>\n'
            '              </svg>\n'
            f'              <p>{esc(warn_text)}</p>\n'
            '            </div>'
        )
    else:
        warn_block = ""
    return (
        '<div class="card">\n'
        f'          <div class="head">{esc(head)}</div>\n'
        '          <div class="body-pad">\n\n'
        f'            {body}{warn_block}\n\n'
        '          </div>\n'
        '        </div>'
    ).replace("{BLUE}", BLUE)


def card_commands(head: str, label: str, commands: list[dict]) -> str:
    """Card with a terminal pill header and a list of cmd rows. Each cmd: {cmd, desc}."""
    cmd_rows = []
    for c in commands:
        cmd_rows.append(
            '<div class="cmd-row">\n'
            f'              <code>{esc(c["cmd"])}</code>\n'
            f'              <span>{esc(c["desc"])}</span>\n'
            '            </div>'
        )
    body = "\n\n            ".join(cmd_rows)
    return (
        '<div class="card">\n'
        f'          <div class="head">{esc(head)}</div>\n'
        '          <div class="cmd-head-row">\n'
        '            <span class="term-pill"><span class="arrow">&gt;_</span></span>\n'
        f'            <span class="lbl">{esc(label)}</span>\n'
        '          </div>\n'
        '          <div class="cmd-list">\n\n'
        f'            {body}\n\n'
        '          </div>\n'
        '        </div>'
    )


def card_tips(head: str, tips: list[str]) -> str:
    """Card with a list of tip bullets."""
    tip_items = []
    for t in tips:
        tip_items.append(
            '<div class="tip-item">\n'
            '              <div class="dot-b"></div>\n'
            f'              <p>{esc(t)}</p>\n'
            '            </div>'
        )
    body = "\n            ".join(tip_items)
    return (
        '<div class="card">\n'
        f'          <div class="head">{esc(head)}</div>\n'
        f'          <div class="tip-list">\n            {body}\n          </div>\n'
        '        </div>'
    )


def card_numbered(head: str, items: list[str]) -> str:
    """Card with a numbered list."""
    ni = []
    for i, t in enumerate(items, 1):
        ni.append(
            '<div class="num-item">\n'
            f'              <div class="ni-n">{i:02d}</div>\n'
            f'              <p>{esc(t)}</p>\n'
            '            </div>'
        )
    body = "\n            ".join(ni)
    return (
        '<div class="card">\n'
        f'          <div class="head">{esc(head)}</div>\n'
        f'          <div class="num-list">\n            {body}\n          </div>\n'
        '        </div>'
    )


def card_cfg(head: str, label: str, cfg_lines: list[tuple[str, str, str]]) -> str:
    """Card with a config-block (sshd_config style). cfg_lines: (key, value, comment)."""
    lines = []
    for k, v, c in cfg_lines:
        parts = []
        if k:
            parts.append(f'<span class="k">{esc(k)}</span>')
        if v:
            parts.append(f' <span class="v">{esc(v)}</span>')
        if c:
            parts.append(f' <span class="c">{esc(c)}</span>')
        lines.append("".join(parts))
    cfg_body = "\n".join(lines)
    return (
        '<div class="card">\n'
        f'          <div class="head">{esc(head)}</div>\n'
        '          <div class="cmd-head-row">\n'
        '            <span class="term-pill"><span class="arrow">&gt;_</span></span>\n'
        f'            <span class="lbl">{esc(label)}</span>\n'
        '          </div>\n'
        f'          <div class="cfg-block">{cfg_body}</div>\n'
        '        </div>'
    )


# ============================================================================
# PAGE 1 — COVER
# ============================================================================


def build_cover() -> str:
    """Cover page — big title, subtitle, topic icons, tagline."""
    topics = [
        (topic_icon_access(), "ACCESS CONTROL"),
        (topic_icon_auth(), "AUTHENTICATION"),
        (topic_icon_firewall(), "FIREWALL"),
        (topic_icon_hardening(), "SYSTEM HARDENING"),
        (topic_icon_perms(), "FILE PERMISSIONS"),
        (topic_icon_compliance(), "COMPLIANCE"),
        (topic_icon_audit(), "AUDITING & LOGGING"),
        (topic_icon_monitoring(), "MONITORING"),
        (icon_terminal(), "TERMINAL OPS"),
    ]
    topic_cards = []
    tints = ["bg-blue", "bg-purple", "bg-gold", "bg-green", "bg-gold", "bg-blue", "bg-purple", "bg-red", ""]
    for (icon, label), tint in zip(topics, tints):
        cls = f"tic {tint}".strip()
        topic_cards.append(
            '<div class="topic-card">\n'
            f'            <div class="{cls}">{icon}</div>\n'
            f'            <div class="tlabel">{esc(label)}</div>\n'
            '          </div>'
        )
    topic_grid = "\n        ".join(topic_cards)

    inner = (
        f'{top_strip(None)}\n\n'
        '    <div class="cover">\n'
        '      <h1 class="cover-title">\n'
        '        <span class="stack">LINUX</span>\n'
        '        <span class="stack">SECURITY</span>\n'
        '        <span class="stack" style="color:#7c3aed">HANDBOOK</span>\n'
        '      </h1>\n'
        '      <p class="cover-subtitle">FROM LINUX HARDENING<br>TO PRODUCTION SECURITY</p>\n'
        '      <div class="cover-divider">\n'
        '        <span class="line"></span><span class="dot"></span><span class="line"></span>\n'
        '      </div>\n'
        f'      <div class="topic-grid">\n        {topic_grid}\n      </div>\n'
        '      <div class="cover-tagline">\n'
        '        <div class="big">SECURE TODAY. PROTECT TOMORROW.</div>\n'
        '        <div class="row-pills">\n'
        '          <span class="pill">HARDEN</span>\n'
        '          <span class="pill">DETECT</span>\n'
        '          <span class="pill">PROTECT</span>\n'
        '          <span class="pill">RECOVER FAST</span>\n'
        '        </div>\n'
        '        <p class="sub">Secure systems · Find threats · Stop attacks · Recover fast</p>\n'
        '      </div>\n'
        '    </div>'
    )
    return page_wrapper(inner)


# ============================================================================
# PAGE 3 — REFERENCE PAGE (copy VERIQTA_Linux_Security_Handbook_Page2.html EXACTLY)
# ============================================================================


def build_reference_page_3() -> str:
    """Reproduce the reference page (page 2 of 20) EXACTLY — Users, Groups, Identity."""
    inner = (
        f'{top_strip("PAGE 2 OF 20")}\n\n'
        '    <!-- TITLE -->\n'
        '    <div class="title-block">\n'
        '      <h1 class="title">2. USERS, GROUPS,<br>AND IDENTITY SECURITY</h1>\n'
        '    </div>\n'
        '    <div class="divider">\n'
        '      <span class="line"></span><span class="dot"></span><span class="line"></span>\n'
        '    </div>\n\n'
        '    <!-- BODY -->\n'
        '    <div class="body">\n\n'
        '      <!-- LEFT COLUMN -->\n'
        '      <div class="rows">\n\n'
        '        <!-- Row 1 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon bg-blue">\n'
        f'            {icon_users()}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>LOCAL USERS AND SYSTEM ACCOUNTS</h3>\n'
        f'            <p>Linux uses local users and system accounts to manage access and ownership. System accounts usually have low UIDs and no login shell.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '        <!-- Row 2 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon bg-blue">\n'
        f'            {icon_file(BLUE)}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>/ETC/PASSWD</h3>\n'
        f'            <p>Stores user account information including username, UID, GID, home directory, and default shell.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '        <!-- Row 3 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon bg-green">\n'
        f'            {icon_file_rects(GREEN)}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>/ETC/SHADOW</h3>\n'
        f'            <p>Stores encrypted passwords and password aging information. Access is restricted to the root user.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '        <!-- Row 4 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon bg-purple">\n'
        f'            {icon_file(PURPLE)}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>/ETC/GROUP</h3>\n'
        f'            <p>Stores group information including GID and member list.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '        <!-- Row 5 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon bg-blue">\n'
        f'            {icon_shield_person(BLUE)}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>UID AND GID SECURITY</h3>\n'
        f'            <p>Every user and group has a unique UID and GID. Protect UID 0 (root) and other privileged IDs.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '        <!-- Row 6 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon bg-gold">\n'
        f'            {icon_magnifier(GOLD)}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>DETECTING UNEXPECTED ACCOUNTS</h3>\n'
        f'            <p>Regularly check for unknown or suspicious user accounts and groups.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '        <!-- Row 7 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon bg-red">\n'
        f'            {icon_padlock(RED)}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>LOCKING AND DISABLING ACCOUNTS</h3>\n'
        f'            <p>Lock or disable unused or compromised accounts to prevent unauthorized access.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '        <!-- Row 8 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon bg-gold">\n'
        f'            {icon_crown(GOLD)}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>REVIEWING PRIVILEGED USERS</h3>\n'
        f'            <p>Review users with UID 0 and sudo access. Limit privileged access to only what is necessary.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '        <!-- Row 9 -->\n'
        f'        <div class="row">\n'
        f'          <div class="icon">\n'
        f'            {icon_terminal()}\n'
        f'          </div>\n'
        f'          <div class="text">\n'
        f'            <h3>KEY MANAGEMENT COMMANDS</h3>\n'
        f'            <p>Use Linux commands to inspect and manage users, groups, and account settings.</p>\n'
        f'          </div>\n'
        f'        </div>\n\n'
        '      </div>\n\n'
        '      <!-- RIGHT COLUMN — SIDEBAR -->\n'
        '      <div class="sidebar">\n\n'
        '        <!-- Card 1 — Key Account Files -->\n'
        '        <div class="card">\n'
        '          <div class="head">KEY ACCOUNT FILES</div>\n'
        '          <div class="body-pad">\n\n'
        '            <div class="file-row">\n'
        '              <div class="ficon">\n'
        f'                {icon_file(BLUE)}\n'
        '              </div>\n'
        '              <div class="ftext">\n'
        '                <div class="fpath">/etc/passwd</div>\n'
        '                <div class="fdesc">User account information</div>\n'
        '              </div>\n'
        '            </div>\n\n'
        '            <div class="file-row">\n'
        '              <div class="ficon">\n'
        f'                {icon_file_rects(GREEN)}\n'
        '              </div>\n'
        '              <div class="ftext">\n'
        '                <div class="fpath">/etc/shadow</div>\n'
        '                <div class="fdesc">Encrypted passwords and aging info</div>\n'
        '              </div>\n'
        '            </div>\n\n'
        '            <div class="file-row">\n'
        '              <div class="ficon">\n'
        f'                {icon_file(PURPLE)}\n'
        '              </div>\n'
        '              <div class="ftext">\n'
        '                <div class="fpath">/etc/group</div>\n'
        '                <div class="fdesc">Group information and members</div>\n'
        '              </div>\n'
        '            </div>\n\n'
        '            <div class="dashed"></div>\n\n'
        '            <div class="warn">\n'
        '              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">\n'
        f'                <path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" fill="{BLUE}"/>\n'
        '                <rect x="8.5" y="11.5" width="7" height="6" rx="1.5" fill="#ffffff"/>\n'
        '                <path d="M9.8 11.5 V9.5 a2.2 2.2 0 0 1 4.4 0 V11.5" fill="none" stroke="#ffffff" stroke-width="1.4"/>\n'
        f'                <circle cx="12" cy="14.5" r="0.9" fill="{BLUE}"/>\n'
        '              </svg>\n'
        '              <p>These files are critical for identity security. Protect them carefully.</p>\n'
        '            </div>\n\n'
        '          </div>\n'
        '        </div>\n\n'
        '        <!-- Card 2 — Key Commands -->\n'
        '        <div class="card">\n'
        '          <div class="head">KEY COMMANDS</div>\n'
        '          <div class="cmd-head-row">\n'
        '            <span class="term-pill"><span class="arrow">&gt;_</span></span>\n'
        '            <span class="lbl">user · group · identity</span>\n'
        '          </div>\n'
        '          <div class="cmd-list">\n'
        '            <div class="cmd-row">\n'
        '              <code>id</code>\n'
        '              <span>Show user and group identity information</span>\n'
        '            </div>\n'
        '            <div class="cmd-row">\n'
        '              <code>getent</code>\n'
        '              <span>Query user and group database</span>\n'
        '            </div>\n'
        '            <div class="cmd-row">\n'
        '              <code>passwd</code>\n'
        '              <span>Manage user passwords</span>\n'
        '            </div>\n'
        '            <div class="cmd-row">\n'
        '              <code>usermod</code>\n'
        '              <span>Modify user account properties</span>\n'
        '            </div>\n'
        '            <div class="cmd-row">\n'
        '              <code>chage</code>\n'
        '              <span>Manage password aging and expiry</span>\n'
        '            </div>\n'
        '          </div>\n'
        '        </div>\n\n'
        '      </div>\n'
        '    </div>'
    )
    return page_wrapper(inner)


# ============================================================================
# Generic content-page builder
# ============================================================================


def build_content_page(
    page_label: str,
    title_html: str,
    rows_items: list[dict],
    sidebar_cards: list[str],
) -> str:
    """Standard content page: top-strip + title + divider + body(rows + sidebar)."""
    inner = (
        f'{top_strip(page_label)}\n\n'
        f'    {title_block(title_html)}\n\n'
        '    <div class="body">\n\n'
        f'      {rows(rows_items)}\n\n'
        f'      {sidebar(sidebar_cards)}\n'
        '    </div>'
    )
    return page_wrapper(inner)


# ============================================================================
# PAGE CONTENT DATA — parsed from /tmp/all_pages_ocr.json (cleaned of noise)
# ============================================================================

# ----- PAGE 2 — "1. LINUX SECURITY FOUNDATIONS" (badge: PAGE 1 OF 20) -----
PAGE2_ROWS = [
    {"icon": icon_layers(PURPLE), "bg": "bg-purple",
     "h3": "LINUX SECURITY LAYERS",
     "p": "Linux security is built in multiple layers including the kernel, system services, filesystem, users, and network. Every component interacts — securing each layer reduces risk across the entire system."},
    {"icon": icon_users(), "bg": "bg-blue",
     "h3": "AUTHENTICATION VS AUTHORIZATION",
     "p": "Authentication verifies who you are. Authorization determines what you are allowed to do. Both must be configured correctly for the system to remain secure."},
    {"icon": icon_shield_person(BLUE), "bg": "bg-blue",
     "h3": "LEAST PRIVILEGE",
     "p": "Users, services, and processes should have only the minimum permissions required to perform their tasks. Limit access to reduce risk."},
    {"icon": icon_globe(RED), "bg": "bg-red",
     "h3": "ATTACK SURFACE",
     "p": "Any point that can be used to attack your system. Reduce exposed services, open ports, and unnecessary access to shrink the attack surface."},
    {"icon": icon_shield_grid(NAVY), "bg": "bg-blue",
     "h3": "DEFENSE IN DEPTH",
     "p": "No single control is perfect. Use multiple layers of security so that if one layer fails, other layers continue to protect the system."},
    {"icon": icon_checklist(GREEN), "bg": "bg-green",
     "h3": "SECURITY BASELINE VS ONGOING MONITORING",
     "p": "A strong baseline sets the foundation. Continuous monitoring detects changes, threats, and abnormal behavior early."},
]
PAGE2_SIDEBAR = [
    card_tips("KEY PRINCIPLES", [
        "Kernel, services, filesystem, users, and network are all security layers.",
        "Authentication answers who you are; authorization answers what you can do.",
        "Grant only the minimum permissions required for each task.",
        "Reduce exposed services and open ports to shrink the attack surface.",
        "Combine multiple controls so a failure in one layer does not compromise the system.",
        "Set a strong baseline, then monitor continuously for change.",
    ]),
    card_commands("FOUNDATION COMMANDS", "system · identity · audit", [
        {"cmd": "uname -a", "desc": "Show kernel and system information"},
        {"cmd": "hostnamectl", "desc": "Show host identity and OS facts"},
        {"cmd": "whoami", "desc": "Show the current effective user"},
        {"cmd": "id", "desc": "Show UID, GID, and group memberships"},
        {"cmd": "uptime", "desc": "Show system uptime and load"},
        {"cmd": "lsmod", "desc": "List loaded kernel modules"},
    ]),
]


# ----- PAGE 4 — "3. PASSWORD AND ACCOUNT SECURITY" (badge: PAGE 3 OF 20) -----
PAGE4_ROWS = [
    {"icon": icon_clock(PURPLE), "bg": "bg-purple",
     "h3": "PASSWORD AGING",
     "p": "Defines the minimum number of days before a password can be changed again. Prevents frequent and weak password changes."},
    {"icon": icon_refresh(GREEN), "bg": "bg-green",
     "h3": "PASSWORD EXPIRATION",
     "p": "Forces users to change passwords after a specified number of days. Reduces risk from compromised passwords."},
    {"icon": icon_lock_open(ORANGE), "bg": "bg-gold",
     "h3": "ACCOUNT EXPIRATION",
     "p": "Sets an expiration date for user accounts. Prevents unused or unnecessary accounts from remaining active."},
    {"icon": icon_shield_lock(PURPLE), "bg": "bg-purple",
     "h3": "PAM PASSWORD POLICIES",
     "p": "Pluggable Authentication Modules (PAM) enforce password strength, complexity, and reuse rules. Configured in /etc/pam.d/ and /etc/security/."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "FAILED AUTHENTICATION ATTEMPTS",
     "p": "Limit and monitor failed login attempts. Helps prevent brute-force and password guessing attacks."},
    {"icon": icon_lock_open(ORANGE), "bg": "bg-gold",
     "h3": "DORMANT ACCOUNTS",
     "p": "Accounts that have not been used for a long time increase risk. Identify and disable or remove dormant accounts."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "LOGIN RESTRICTIONS",
     "p": "Restrict login access by time, source IP, or TTY. Enhances security for privileged and system accounts."},
    {"icon": icon_magnifier(GOLD), "bg": "bg-gold",
     "h3": "REVIEWING PASSWORD STATUS",
     "p": "Regularly review password aging, expiration, and account status. Use tools to ensure policies are enforced."},
    {"icon": icon_key(GOLD), "bg": "bg-gold",
     "h3": "SECURE SERVICE-ACCOUNT PRACTICES",
     "p": "Use strong, long passwords or keys for service accounts. Restrict permissions and avoid interactive logins."},
]
PAGE4_SIDEBAR = [
    card_commands("ACCOUNT & PASSWORD COMMANDS", "chage · passwd · usermod", [
        {"cmd": "chage -l <user>", "desc": "Display password aging information"},
        {"cmd": "chage -M 90 <user>", "desc": "Set password expiration (days)"},
        {"cmd": "chage -E 2025-12-31 <user>", "desc": "Set account expiration date"},
        {"cmd": "passwd -S <user>", "desc": "Show password status"},
        {"cmd": "usermod -L <user>", "desc": "Lock user account"},
        {"cmd": "usermod -e 1 <user>", "desc": "Expire user account immediately"},
        {"cmd": "lastlog", "desc": "Check last login time for all users"},
        {"cmd": "grep 'Failed password' /var/log/auth.log", "desc": "View failed login attempts"},
    ]),
    card_tips("PAM & POLICY NOTES", [
        "PAM policy files live in /etc/pam.d/ — never edit with a broken syntax.",
        "Password quality modules: pam_pwquality, pam_cracklib.",
        "Set pam_tally2 or pam_faillock to lock accounts after N failures.",
        "Service accounts: use long random keys, no interactive shell.",
    ]),
]


# ----- PAGE 5 — "4. FILE AND DIRECTORY PERMISSIONS" (badge: PAGE 4 OF 20) -----
PAGE5_ROWS = [
    {"icon": icon_users(), "bg": "bg-blue",
     "h3": "OWNER, GROUP, AND OTHER PERMISSIONS",
     "p": "Every file and directory has three types of access: Owner (user), Group, and Other (everyone else). Permissions control what each can do."},
    {"icon": icon_file(BLUE), "bg": "bg-blue",
     "h3": "READ, WRITE, AND EXECUTE",
     "p": "R (read): view file contents or list directory. W (write): modify file or create/delete in directory. X (execute): run file or access directory."},
    {"icon": icon_sliders(PURPLE), "bg": "bg-purple",
     "h3": "NUMERIC AND SYMBOLIC PERMISSIONS",
     "p": "Numeric: use numbers (0-7) to represent permissions. Symbolic: use letters (r, w, x) to set permissions. Example: 755 = rwxr-xr-x."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "CHMOD, CHOWN, CHGRP",
     "p": "chmod: change file or directory permissions. chown: change file or directory owner. chgrp: change file or directory group."},
    {"icon": icon_folder(GOLD), "bg": "bg-gold",
     "h3": "DIRECTORY PERMISSION BEHAVIOR",
     "p": "Read (r): list files in the directory. Write (w): create, delete, or rename files. Execute (x): enter and access the directory. Without x, you cannot access files inside."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "UMASK",
     "p": "The umask sets default permissions for new files and directories. It determines what permissions are removed by default. Check with: umask."},
    {"icon": icon_magnifier_alert(RED), "bg": "bg-red",
     "h3": "FINDING DANGEROUS PERMISSIONS",
     "p": "Look for world-writable files and directories. Use tools to find risky permissions. Example: chmod 777 or writable system files."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "PRODUCTION PERMISSION MISTAKES",
     "p": "Using 777 permissions; making sensitive files world-readable; incorrect ownership of application files; writable system directories; ignoring umask settings."},
]
PAGE5_SIDEBAR = [
    card_file_list("PERMISSION REFERENCE", [
        {"icon": icon_file(BLUE), "path": "FILE: script.sh", "desc": "-rw-r--r-- (644)"},
        {"icon": icon_file_rects(GREEN), "path": "FILE: application.log", "desc": "-rw-rw---- (660)"},
        {"icon": icon_folder(GOLD), "path": "DIR: /var/www", "desc": "drwxr-xr-x (755)"},
        {"icon": icon_folder(GOLD), "path": "DIR: /data", "desc": "drwx------ (700)"},
    ], warn_text="Wrong permissions on config files lead to credential leaks. Always audit before deploy."),
    card_commands("QUICK CHECK COMMANDS", "ls · stat · find", [
        {"cmd": "ls -l", "desc": "List files with permissions"},
        {"cmd": "namei -l /path/to/file", "desc": "Show full path permissions"},
        {"cmd": "stat file.txt", "desc": "Detailed file information"},
        {"cmd": "find / -type f -perm -o+w", "desc": "Find world-writable files"},
        {"cmd": "find / -type d -perm -002", "desc": "Find world-writable directories"},
    ]),
]


# ----- PAGE 6 — "5. SUID, SGID, STICKY BIT, AND ACLs" (badge: PAGE 5 OF 20) -----
PAGE6_ROWS = [
    {"icon": icon_star(GOLD), "bg": "bg-gold",
     "h3": "SUID EXECUTABLES",
     "p": "When a file has the SUID bit set, it runs with the permissions of the file owner (usually root). Risk: can be abused to gain elevated privileges. Check SUID files regularly."},
    {"icon": icon_users(), "bg": "bg-blue",
     "h3": "SGID FILES AND DIRECTORIES",
     "p": "SGID on files: runs with the group owner's privileges. SGID on directories: new files inherit the directory's group ownership. Helps in controlled group collaboration."},
    {"icon": icon_bookmark(RED), "bg": "bg-red",
     "h3": "STICKY BIT",
     "p": "On directories, only the file owner, directory owner, or root can delete or rename files. Common on /tmp to prevent users from deleting each other's files."},
    {"icon": icon_sliders(PURPLE), "bg": "bg-purple",
     "h3": "ACCESS CONTROL LISTS (ACLs)",
     "p": "Provide fine-grained permissions beyond the traditional user/group/other model. Useful for granting access to specific users without changing ownership."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "GETFACL AND SETFACL",
     "p": "getfacl: view ACLs on files and directories. setfacl: modify ACLs for fine-grained access. ACLs override standard permissions."},
    {"icon": icon_magnifier(GOLD), "bg": "bg-gold",
     "h3": "SEARCHING FOR SUID AND SGID BINARIES",
     "p": "Regularly search for SUID/SGID files to detect unexpected privilege escalation paths. New or unknown files can be a security risk."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "UNEXPECTED PRIVILEGE PATHS",
     "p": "Attackers exploit misconfigured SUID/SGID files or writable paths to escalate privileges. Always verify owner, permissions, and purpose."},
    {"icon": icon_checklist(GREEN), "bg": "bg-green",
     "h3": "AUDITING SPECIAL PERMISSIONS",
     "p": "Maintain an inventory of all special permission files. Review regularly and document approved exceptions. Remove unnecessary permissions immediately."},
]
PAGE6_SIDEBAR = [
    card_tips("SPECIAL PERMISSION TYPES", [
        "SUID (4xxx) — run as file owner.",
        "SGID (2xxx) — run as group owner.",
        "STICKY (1xxx) — restricted deletion in directories.",
        "ACLs — extended permissions for specific users/groups.",
    ]),
    card_commands("FIND & ACL COMMANDS", "find · getfacl · setfacl", [
        {"cmd": "find / -type f -perm -4000 -exec ls -l {} \\;", "desc": "Find all SUID files"},
        {"cmd": "find / -type f -perm -2000 -exec ls -l {} \\;", "desc": "Find all SGID files"},
        {"cmd": "find /bin /sbin /usr/bin /usr/sbin -perm -4000 -o -perm -2000 -ls", "desc": "Find SUID/SGID in common paths"},
        {"cmd": "getfacl /path/to/file", "desc": "View ACLs"},
        {"cmd": "setfacl -m u:user:rw /path/to/file", "desc": "Add ACL entry"},
        {"cmd": "setfacl -x u:user /path/to/file", "desc": "Remove ACL entry"},
        {"cmd": "setfacl -b /path/to/file", "desc": "Remove all ACLs"},
    ]),
    card_tips("AUDIT CHECKLIST", [
        "Review all SUID, SGID, and Sticky files.",
        "Verify file purpose and ownership.",
        "Ensure directories with SGID are required.",
        "Check ACLs for unnecessary access.",
        "Document approved exceptions.",
        "Remove or fix unnecessary entries.",
    ]),
]


# ----- PAGE 7 — "6. SUDO AND PRIVILEGE ESCALATION SECURITY" (badge: PAGE 6 OF 20) -----
PAGE7_ROWS = [
    {"icon": icon_lightning(RED), "bg": "bg-red",
     "h3": "ROOT ACCESS RISKS",
     "p": "Root has unlimited power on the system. A single mistake or compromise can lead to full system takeover. Limit and monitor root access carefully."},
    {"icon": icon_file(BLUE), "bg": "bg-blue",
     "h3": "/ETC/SUDOERS",
     "p": "Main sudo configuration file. Controls which users or groups can run which commands as root or another user. Always edit with visudo, never a text editor."},
    {"icon": icon_folder(GOLD), "bg": "bg-gold",
     "h3": "/ETC/SUDOERS.D/",
     "p": "Directory for additional sudo configuration files. Used to add custom rules without modifying the main sudoers file. Each file is included automatically."},
    {"icon": icon_wrench(SLATE), "bg": "",
     "h3": "VISUDO",
     "p": "Safe way to edit sudoers files. Syntax is checked before saving. Prevents locking yourself out of sudo access. Always use: visudo or visudo -f <file>."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "COMMAND-SPECIFIC SUDO ACCESS",
     "p": "Grant users access to only the commands they need. Example: allow restart of specific services without full root access. Reduces the attack surface."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "DANGEROUS SUDO CONFIGURATIONS",
     "p": "Avoid broad permissions and wildcard commands. Dangerous: ALL=(ALL) ALL, ALL=(ALL) NOPASSWD: ALL, command wildcards like /bin/*. These can lead to full privilege escalation."},
    {"icon": icon_lock_open(ORANGE), "bg": "bg-gold",
     "h3": "NOPASSWD RISKS",
     "p": "NOPASSWD allows running commands without entering a password. If misconfigured, attackers can escalate privileges without any authentication. Use only when absolutely necessary."},
    {"icon": icon_magnifier(GOLD), "bg": "bg-gold",
     "h3": "REVIEWING SUDO PRIVILEGES",
     "p": "Regularly review who has sudo access and what they can run. Remove unused or excessive privileges. Use audit logs to monitor sudo activity."},
    {"icon": icon_shield_person(BLUE), "bg": "bg-blue",
     "h3": "LEAST-PRIVILEGE ADMINISTRATION",
     "p": "Grant only the minimum access required. Remove elevated access when not needed. Use groups, command restrictions, and logging to enforce least-privilege principles."},
]
PAGE7_SIDEBAR = [
    card_commands("SUDO COMMAND EXAMPLES", "sudo · visudo", [
        {"cmd": "sudo -l", "desc": "List allowed sudo commands for current user"},
        {"cmd": "sudo -ll", "desc": "List all privileges in detail"},
        {"cmd": "sudo -u <user> <command>", "desc": "Run command as another user"},
        {"cmd": "visudo", "desc": "Edit /etc/sudoers safely"},
        {"cmd": "visudo -f /etc/sudoers.d/<file>", "desc": "Edit a file in sudoers.d directory"},
        {"cmd": "sudo -k", "desc": "Invalidate password timestamp"},
        {"cmd": "sudo -v", "desc": "Refresh the sudo timestamp"},
    ]),
    card_tips("SUDO SECURITY CHECKLIST", [
        "Limit users with sudo access.",
        "Use command-specific permissions.",
        "Avoid NOPASSWD unless required.",
        "Do not use wildcards carelessly.",
        "Review /etc/sudoers regularly.",
        "Audit sudo usage in logs.",
        "Remove unnecessary privileges.",
        "Use least-privilege principles.",
        "Test configurations before deployment.",
    ]),
]


# ----- PAGE 8 — "7. SSH SERVER HARDENING" (badge: PAGE 7 OF 20) -----
PAGE8_ROWS = [
    {"icon": icon_globe(RED), "bg": "bg-red",
     "h3": "SSH ATTACK SURFACE",
     "p": "SSH is a common target for attackers. Reduce exposure by limiting access, strengthening authentication, and monitoring activity."},
    {"icon": icon_key(GOLD), "bg": "bg-gold",
     "h3": "KEY-BASED AUTHENTICATION",
     "p": "Use SSH keys instead of passwords. Stronger, more secure, and resistant to brute-force attacks."},
    {"icon": icon_lock_open(ORANGE), "bg": "bg-gold",
     "h3": "DISABLING ROOT SSH LOGIN",
     "p": "Do not allow root to login via SSH. Use a regular user and sudo for administrative tasks."},
    {"icon": icon_padlock(RED), "bg": "bg-red",
     "h3": "DISABLING PASSWORD AUTHENTICATION",
     "p": "Disable password-based login. Prevents brute-force and credential stuffing attacks."},
    {"icon": icon_file(BLUE), "bg": "bg-blue",
     "h3": "SSHD_CONFIG",
     "p": "Main SSH server configuration file. Harden settings in /etc/ssh/sshd_config and reload SSH service safely."},
    {"icon": icon_users(), "bg": "bg-blue",
     "h3": "RESTRICTING USERS AND GROUPS",
     "p": "Allow only specific users or groups to access SSH. Deny all others."},
    {"icon": icon_sliders(PURPLE), "bg": "bg-purple",
     "h3": "SSH KEY PERMISSIONS",
     "p": "Private key (id_rsa): 600. Public key (id_rsa.pub): 644. ~/.ssh directory: 700. authorized_keys file: 600. Wrong permissions = login failure."},
    {"icon": icon_clock(PURPLE), "bg": "bg-purple",
     "h3": "IDLE-SESSION CONTROLS",
     "p": "Set timeouts for idle sessions. Disconnect inactive sessions automatically to reduce risk."},
    {"icon": icon_checklist(GREEN), "bg": "bg-green",
     "h3": "TESTING CONFIGURATION BEFORE RESTART",
     "p": "Always validate SSH configuration before restarting to avoid lockout. Use test mode: sshd -t."},
    {"icon": icon_log(TEAL), "bg": "",
     "h3": "REVIEWING SSH AUTHENTICATION LOGS",
     "p": "Monitor SSH login attempts, failed logins, and suspicious activity regularly. Logs help detect brute-force attacks early."},
]
PAGE8_SIDEBAR = [
    card_cfg("SSHD_CONFIG — HARDENED BASELINE", "/etc/ssh/sshd_config", [
        ("Port", "22", "# keep default or change"),
        ("Protocol", "2", ""),
        ("PermitRootLogin", "no", ""),
        ("PasswordAuthentication", "no", ""),
        ("ChallengeResponseAuthentication", "no", ""),
        ("UsePAM", "yes", ""),
        ("AllowUsers", "user1 user2", ""),
        ("AllowGroups", "sshusers", ""),
        ("X11Forwarding", "no", ""),
        ("MaxAuthTries", "3", ""),
        ("LoginGraceTime", "30s", ""),
        ("ClientAliveInterval", "300", ""),
        ("ClientAliveCountMax", "2", ""),
    ]),
    card_commands("SSH KEY & VALIDATION", "ssh-keygen · sshd · systemctl", [
        {"cmd": "ssh-keygen -t ed25519 -C \"you@domain.com\" -f ~/.ssh/id_ed25519", "desc": "Generate ED25519 key pair"},
        {"cmd": "cat ~/.ssh/id_ed25519.pub | ssh user@srv \"mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys\"", "desc": "Copy public key to server"},
        {"cmd": "sshd -t", "desc": "Validate configuration (silent = OK)"},
        {"cmd": "sudo systemctl reload sshd", "desc": "Reload SSH service"},
        {"cmd": "sudo systemctl restart sshd", "desc": "Restart SSH service"},
        {"cmd": "sudo journalctl -u ssh --since \"1 hour ago\"", "desc": "Review SSH journal logs"},
        {"cmd": "sudo grep \"Failed password\" /var/log/auth.log", "desc": "Find failed SSH logins"},
    ]),
]


# ----- PAGE 9 — "8. LINUX SERVICES AND SYSTEMD SECURITY" (badge: PAGE 8 OF 20) -----
PAGE9_ROWS = [
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "IDENTIFYING UNNECESSARY SERVICES",
     "p": "Many services start automatically by default. Remove or disable services you do not need. Every unnecessary service increases your attack surface."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "SYSTEMCTL",
     "p": "The primary tool for managing systemd services. Used to start, stop, enable, disable, and inspect services."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "ENABLED VERSUS RUNNING SERVICES",
     "p": "Enabled: starts automatically at boot. Running: currently active in memory. A service can be enabled, running, both, or neither."},
    {"icon": icon_lock_open(ORANGE), "bg": "bg-gold",
     "h3": "DISABLING UNUSED SERVICES",
     "p": "Disable services to prevent them from starting at boot. Stop services that are not needed now. Example: systemctl disable --now <service>."},
    {"icon": icon_users(), "bg": "bg-blue",
     "h3": "SERVICE USERS",
     "p": "Services should run as an unprivileged user. Avoid running services as root. Check the User= and Group= settings in unit files."},
    {"icon": icon_file(PURPLE), "bg": "bg-purple",
     "h3": "SYSTEMD UNIT PERMISSIONS",
     "p": "Unit files control how services run. Protect unit files from unauthorized changes. Typical path: /etc/systemd/system/. Use proper file permissions."},
    {"icon": icon_sandbox(PURPLE), "bg": "bg-purple",
     "h3": "SERVICE ISOLATION",
     "p": "Use systemd sandboxing to limit damage. Options: ProtectSystem, ProtectHome, PrivateTmp, NoNewPrivileges, RestrictAddressFamilies, and more. Stronger isolation = better security."},
    {"icon": icon_refresh(GREEN), "bg": "bg-green",
     "h3": "RESTART POLICIES",
     "p": "Configure how services behave when they fail. Common policies: no, on-failure, on-abnormal, on-watchdog, always. Use RestartSec= to set delay between restarts."},
    {"icon": icon_magnifier_alert(RED), "bg": "bg-red",
     "h3": "INSPECTING FAILED OR SUSPICIOUS SERVICES",
     "p": "Check failed services and view recent logs. Look for crash loops, repeated failures, or unexpected behavior. Use systemctl status <service> and journalctl -u <service>."},
    {"icon": icon_shield_check(GREEN), "bg": "bg-green",
     "h3": "REDUCING SERVICE ATTACK SURFACE",
     "p": "Run only what you need. Disable, mask, or remove unneeded services. Keep services updated and properly configured. Minimize privileges and isolate workloads."},
]
PAGE9_SIDEBAR = [
    card_commands("COMMON SYSTEMCTL COMMANDS", "systemctl · journalctl", [
        {"cmd": "systemctl list-units --type=service", "desc": "List all services"},
        {"cmd": "systemctl list-unit-files --type=service", "desc": "Show enabled/disabled services"},
        {"cmd": "systemctl status <service>", "desc": "Show service status and logs"},
        {"cmd": "systemctl start <service>", "desc": "Start a service"},
        {"cmd": "systemctl stop <service>", "desc": "Stop a service"},
        {"cmd": "systemctl restart <service>", "desc": "Restart a service"},
        {"cmd": "systemctl enable <service>", "desc": "Enable at boot"},
        {"cmd": "systemctl disable <service>", "desc": "Disable from boot"},
        {"cmd": "systemctl mask <service>", "desc": "Prevent service from starting"},
        {"cmd": "systemctl unmask <service>", "desc": "Unmask a service"},
        {"cmd": "systemctl cat <service>", "desc": "Show full unit file"},
        {"cmd": "systemctl show <service>", "desc": "Show all properties"},
    ]),
    card_tips("BEST PRACTICES", [
        "Disable services you do not use.",
        "Run services as non-root users.",
        "Harden services with isolation options.",
        "Limit network and filesystem access.",
        "Monitor service logs and failures.",
        "Keep services updated.",
        "Review services regularly.",
        "Follow least-privilege principles.",
    ]),
    card_commands("ENABLED VS RUNNING", "list-unit-files · list-units", [
        {"cmd": "systemctl list-unit-files --type=service --state=enabled", "desc": "List enabled services"},
        {"cmd": "systemctl list-units --type=service --state=running", "desc": "List running services"},
    ]),
]


# ----- PAGE 10 — "9. NETWORK EXPOSURE AND OPEN PORTS" (badge: PAGE 9 OF 20) -----
PAGE10_ROWS = [
    {"icon": icon_nodes(BLUE), "bg": "bg-blue",
     "h3": "LISTENING SOCKETS",
     "p": "Listening sockets are endpoints that accept incoming connections or packets on the system."},
    {"icon": icon_globe(RED), "bg": "bg-red",
     "h3": "TCP AND UDP EXPOSURE",
     "p": "Open TCP ports establish connections. Open UDP ports receive datagrams. Both increase the attack surface."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "SS",
     "p": "ss is the modern tool to view socket statistics, listening ports, and network connections. Use it to identify what is listening on the system."},
    {"icon": icon_doc_search(PURPLE), "bg": "bg-purple",
     "h3": "LSOF",
     "p": "lsof lists open files and the processes that opened them, including network sockets. Useful for identifying listening ports and connections."},
    {"icon": icon_magnifier(GOLD), "bg": "bg-gold",
     "h3": "IDENTIFYING PROCESSES BEHIND PORTS",
     "p": "Find which process is listening on a specific port. Understand the service, user, and risk associated with that process."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "LOOPBACK VERSUS PUBLIC INTERFACES",
     "p": "Services bound to 127.0.0.1 are only accessible locally. Services bound to 0.0.0.0 or public IPs are accessible from the network or internet."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "UNEXPECTED LISTENING SERVICES",
     "p": "Unexpected or unnecessary services listening on ports may indicate misconfiguration or potential compromise. Always review and minimize exposed services."},
    {"icon": icon_doc_search(PURPLE), "bg": "bg-purple",
     "h3": "NETWORK EXPOSURE INVESTIGATION",
     "p": "Investigate open ports, services, and connections. Correlate with logs and configurations to assess the security impact."},
]
PAGE10_SIDEBAR = [
    card_tips("PRODUCTION PORT AUDITING", [
        "Regularly audit open ports and listening services.",
        "Validate that only required services are exposed.",
        "Document, monitor, and review continuously.",
        "Compare enabled vs running services.",
        "Investigate any unexpected listener immediately.",
    ]),
    card_commands("LISTENING-PORT COMMANDS", "ss · lsof · netstat", [
        {"cmd": "ss -tulpen", "desc": "List all TCP/UDP listening sockets with process"},
        {"cmd": "ss -antp", "desc": "List all TCP connections with process"},
        {"cmd": "lsof -i -P -n", "desc": "List network sockets and owning processes"},
        {"cmd": "netstat -tulpen", "desc": "Legacy: list listening sockets"},
        {"cmd": "ss -s", "desc": "Show socket statistics summary"},
        {"cmd": "lsof -i :22", "desc": "Find process listening on port 22"},
    ]),
]


# ----- PAGE 11 — "10. LINUX FIREWALL SECURITY" (badge: PAGE 10 OF 20) -----
PAGE11_ROWS = [
    {"icon": icon_wall(ORANGE), "bg": "bg-gold",
     "h3": "HOST-BASED FIREWALL PURPOSE",
     "p": "A host-based firewall controls network traffic to and from your Linux system. It blocks unauthorized access, reduces attack surface, and enforces security policies at the host level."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "NFTABLES",
     "p": "nftables is the modern Linux packet filtering framework. It is powerful, fast, and replaces legacy iptables. It supports complex rules, sets, maps, and stateful filtering."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "IPTABLES CONCEPTS",
     "p": "iptables is the legacy firewall tool based on tables, chains, and rules. Key tables: filter, nat, mangle, raw. Key chains: INPUT, OUTPUT, FORWARD."},
    {"icon": icon_shield_check(GREEN), "bg": "bg-green",
     "h3": "UFW AND FIREWALLD",
     "p": "UFW is a simple frontend for iptables/nftables. firewalld provides a dynamic firewall with zones, services, and runtime management."},
    {"icon": icon_shield_person(BLUE), "bg": "bg-blue",
     "h3": "DEFAULT-DENY STRATEGY",
     "p": "Start with default deny for incoming connections. Allow only what is required. This minimizes risk by blocking everything except explicitly allowed traffic."},
    {"icon": icon_nodes(BLUE), "bg": "bg-blue",
     "h3": "INBOUND VERSUS OUTBOUND RULES",
     "p": "Inbound rules control traffic coming into the system. Outbound rules control traffic leaving the system. Both should be defined intentionally."},
    {"icon": icon_padlock(RED), "bg": "bg-red",
     "h3": "RESTRICTING ADMINISTRATIVE PORTS",
     "p": "Limit access to administrative ports (SSH, RDP, etc.) to trusted IPs or networks only. Never expose admin ports to the public internet."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "RULE ORDERING",
     "p": "Firewall rules are processed in order from top to bottom. Place specific allow rules before general deny rules. Incorrect ordering can create security gaps."},
    {"icon": icon_refresh(GREEN), "bg": "bg-green",
     "h3": "PERSISTENT FIREWALL CONFIGURATION",
     "p": "Firewall rules must survive reboots. Use appropriate tools to save rules: nft list ruleset > file, iptables-save, ufw enable, firewalld --permanent."},
    {"icon": icon_magnifier_alert(RED), "bg": "bg-red",
     "h3": "TESTING RULES WITHOUT LOCKING YOURSELF OUT",
     "p": "Always test firewall changes carefully. Use a second SSH session or console access. Apply changes gradually and verify before closing your session."},
]
PAGE11_SIDEBAR = [
    card_commands("FIREWALL COMMANDS", "nft · iptables · ufw · firewall-cmd", [
        {"cmd": "nft list ruleset", "desc": "Show current nftables ruleset"},
        {"cmd": "nft add rule inet filter input tcp dport 22 accept", "desc": "Allow SSH in nftables"},
        {"cmd": "iptables -L -n -v", "desc": "List iptables rules with counters"},
        {"cmd": "iptables -A INPUT -p tcp --dport 22 -j ACCEPT", "desc": "Allow SSH in iptables"},
        {"cmd": "iptables-save > /etc/iptables/rules.v4", "desc": "Save iptables rules"},
        {"cmd": "ufw enable", "desc": "Enable UFW"},
        {"cmd": "ufw allow 22/tcp", "desc": "Allow SSH in UFW"},
        {"cmd": "ufw status verbose", "desc": "Show UFW status"},
        {"cmd": "firewall-cmd --permanent --add-service=ssh", "desc": "Add SSH service in firewalld"},
        {"cmd": "firewall-cmd --reload", "desc": "Reload firewalld rules"},
    ]),
    card_tips("FIREWALL BEST PRACTICES", [
        "Default-deny inbound; explicitly allow what is required.",
        "Restrict admin ports to trusted IPs only.",
        "Order specific allows before general denies.",
        "Persist rules across reboots (iptables-save / ufw enable).",
        "Test from a second session before disconnecting.",
    ]),
]


# ----- PAGE 12 — "11. PROCESS AND RUNTIME SECURITY" (badge: PAGE 11 OF 20) -----
PAGE12_ROWS = [
    {"icon": icon_users(), "bg": "bg-blue",
     "h3": "PROCESS OWNERSHIP",
     "p": "Every process runs as a specific user and group. Review process ownership to ensure least privilege and detect suspicious activity."},
    {"icon": icon_gear(SLATE), "bg": "",
     "h3": "PARENT AND CHILD PROCESSES",
     "p": "Processes are created by other processes. Understanding parent-child relationships helps trace the origin of a process."},
    {"icon": icon_lightning(RED), "bg": "bg-red",
     "h3": "PRIVILEGED PROCESSES",
     "p": "Processes running as root or with elevated capabilities pose higher risk. Review and restrict privileged processes."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "PS, TOP, PSTREE",
     "p": "Use ps to view processes, top for live monitoring, and pstree to visualize process trees. Essential tools for runtime visibility."},
    {"icon": icon_folder(GOLD), "bg": "bg-gold",
     "h3": "/PROC",
     "p": "The /proc filesystem provides real-time information about processes, memory, mounts, network, and more. Powerful for investigation."},
    {"icon": icon_magnifier_alert(RED), "bg": "bg-red",
     "h3": "SUSPICIOUS COMMAND LINES",
     "p": "Review process command lines. Look for obfuscated, encoded, or unusual commands that may indicate malicious activity."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "UNEXPECTED BINARIES",
     "p": "Processes running from unusual locations (e.g., /tmp, /dev/shm) or unknown binaries may indicate compromise."},
    {"icon": icon_clock(PURPLE), "bg": "bg-purple",
     "h3": "LONG-RUNNING PROCESSES",
     "p": "Processes running longer than expected can indicate stuck services or persistence mechanisms. Review and validate regularly."},
    {"icon": icon_nodes(BLUE), "bg": "bg-blue",
     "h3": "PROCESSES LISTENING ON THE NETWORK",
     "p": "Identify processes that have open sockets. Ensure only required services are listening on expected ports and interfaces."},
    {"icon": icon_doc_search(PURPLE), "bg": "bg-purple",
     "h3": "INVESTIGATING ABNORMAL RUNTIME ACTIVITY",
     "p": "Correlate process behavior, network activity, and logs to detect anomalies. Investigate immediately and contain threats."},
]
PAGE12_SIDEBAR = [
    card_commands("RUNTIME INSPECTION", "ps · top · pstree · /proc", [
        {"cmd": "ps aux", "desc": "List all processes with user and command"},
        {"cmd": "ps -ef --forest", "desc": "Show process tree"},
        {"cmd": "top", "desc": "Live process monitor (CPU, memory)"},
        {"cmd": "pstree -p", "desc": "Tree view with PIDs"},
        {"cmd": "cat /proc/<pid>/cmdline", "desc": "Inspect process command line"},
        {"cmd": "cat /proc/<pid>/environ", "desc": "Inspect process environment"},
        {"cmd": "ls -l /proc/<pid>/exe", "desc": "Resolve binary path for a process"},
        {"cmd": "ss -tulpen", "desc": "Find processes listening on ports"},
    ]),
    card_tips("RUNTIME RED FLAGS", [
        "Processes from /tmp, /dev/shm, or /var/tmp.",
        "Obfuscated / base64-encoded command lines.",
        "Long-running unknown binaries.",
        "Process running as root that should not be.",
        "Unexpected outbound network connections.",
        "Deleted-but-running binaries (ls -l /proc/*/exe).",
    ]),
]


# ----- PAGE 13 — "12. LOGGING AND SECURITY INVESTIGATION" (badge: PAGE 12 OF 20) -----
PAGE13_ROWS = [
    {"icon": icon_log(TEAL), "bg": "",
     "h3": "LINUX AUTHENTICATION LOGS",
     "p": "Authentication logs record user logins, logouts, and security-relevant events. Key sources: /var/log/auth.log, /var/log/secure."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "JOURNALCTL",
     "p": "journalctl is the systemd log manager. View system, service, kernel, and boot logs. Powerful filtering with time, unit, priority, and more."},
    {"icon": icon_folder(GOLD), "bg": "bg-gold",
     "h3": "/VAR/LOG",
     "p": "Traditional log files stored in /var/log. Contains authentication, system, application, and service logs."},
    {"icon": icon_key(GOLD), "bg": "bg-gold",
     "h3": "SSH LOGIN EVENTS",
     "p": "Track successful and failed SSH logins. Logs show IP address, user, time, and authentication method. Helps detect brute-force and suspicious access."},
    {"icon": icon_lightning(RED), "bg": "bg-red",
     "h3": "SUDO ACTIVITY",
     "p": "Monitor sudo command usage and privilege escalation. Logs show who ran what command and when. Essential for auditing privileged access."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "FAILED AUTHENTICATION",
     "p": "Failed login attempts indicate attacks or misconfiguration. Track repeated failures from the same IP or user. Helps identify brute-force and password attacks."},
    {"icon": icon_refresh(GREEN), "bg": "bg-green",
     "h3": "SERVICE FAILURES",
     "p": "Service errors can impact availability and security. Logs show crashes, dependency issues, and start failures. Helps detect misconfigurations and potential attacks."},
    {"icon": icon_gear(SLATE), "bg": "",
     "h3": "KERNEL MESSAGES",
     "p": "Kernel logs report hardware, driver, and system events. Important for detecting panics, OOM kills, and security issues. Access via dmesg or journalctl -k."},
    {"icon": icon_magnifier(GOLD), "bg": "bg-gold",
     "h3": "SEARCHING AND FILTERING LOGS",
     "p": "Use tools like grep, awk, sed, and journalctl filters. Filter by time, user, IP, service, priority, or keywords. Effective searching speeds up investigation."},
    {"icon": icon_checklist(GREEN), "bg": "bg-green",
     "h3": "BUILDING AN INCIDENT TIMELINE",
     "p": "Correlate events from multiple logs to understand what happened. Establish sequence: initial access, actions, and impact. A clear timeline is critical for response and reporting."},
]
PAGE13_SIDEBAR = [
    card_commands("LOG INSPECTION COMMANDS", "journalctl · grep · last", [
        {"cmd": "journalctl -u ssh --since \"1 hour ago\"", "desc": "SSH logs from last hour"},
        {"cmd": "journalctl -p err -b", "desc": "Errors since boot"},
        {"cmd": "journalctl -k", "desc": "Kernel messages"},
        {"cmd": "grep \"sshd\" /var/log/auth.log", "desc": "SSH events in auth log"},
        {"cmd": "grep \"Failed password\" /var/log/auth.log", "desc": "Failed SSH logins"},
        {"cmd": "grep \"sudo\" /var/log/auth.log", "desc": "Sudo activity"},
        {"cmd": "last -a", "desc": "Recent login sessions with IPs"},
        {"cmd": "lastlog", "desc": "Last login time per user"},
        {"cmd": "dmesg -T", "desc": "Kernel ring buffer with timestamps"},
    ]),
    card_tips("INVESTIGATION CHECKLIST", [
        "Identify time window and time zone of incident.",
        "Pull auth.log + journalctl for that window.",
        "Track failed logins and successful logins.",
        "Trace sudo / su privilege escalation.",
        "Correlate with service + kernel logs.",
        "Build a timeline: initial access, actions, impact.",
    ]),
]


# ----- PAGE 14 — "13. LINUX AUDITING WITH AUDITD" (badge: PAGE 13 OF 20) -----
PAGE14_ROWS = [
    {"icon": icon_eye(PURPLE), "bg": "bg-purple",
     "h3": "LINUX AUDIT FRAMEWORK",
     "p": "The Linux Audit Framework provides a comprehensive system for monitoring, recording, and reviewing security-relevant events. It operates at the kernel level for high integrity and reliability."},
    {"icon": icon_server(GREEN), "bg": "bg-green",
     "h3": "AUDITD",
     "p": "auditd is the user-space service that collects audit events from the kernel and writes them to the audit log. It is highly configurable and essential for security monitoring."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "AUDIT RULES",
     "p": "Audit rules define what events to monitor. Rules can be file watches, syscalls, users, commands, or system calls. Use auditctl to load and manage rules."},
    {"icon": icon_file(BLUE), "bg": "bg-blue",
     "h3": "WATCHING SENSITIVE FILES",
     "p": "Monitor critical files and directories for reads, writes, attribute changes, and deletions. Example: /etc/passwd, /etc/shadow, /etc/sudoers."},
    {"icon": icon_lightning(RED), "bg": "bg-red",
     "h3": "MONITORING PRIVILEGED COMMANDS",
     "p": "Track the use of privileged commands such as sudo, su, useradd, chmod, chown, setuid, and more. Helps detect privilege escalation and misuse."},
    {"icon": icon_magnifier(GOLD), "bg": "bg-gold",
     "h3": "AUSEARCH",
     "p": "ausearch is used to search the audit log. Filter by time, user, event type, file, PID, or command. Essential for incident investigations."},
    {"icon": icon_log(TEAL), "bg": "",
     "h3": "AUREPORT",
     "p": "aureport generates summarized reports from audit logs. Use it for quick insights on logins, commands, files, and SELinux events."},
    {"icon": icon_doc_search(PURPLE), "bg": "bg-purple",
     "h3": "TRACKING CONFIGURATION CHANGES",
     "p": "Monitor changes to critical configuration files. Detect unauthorized modifications to system settings, services, and security policies."},
    {"icon": icon_padlock(RED), "bg": "bg-red",
     "h3": "AUDIT-LOG PROTECTION",
     "p": "Protect audit logs from tampering. Set proper permissions, enable log rotation, and forward logs to a secure, centralized location."},
]
PAGE14_SIDEBAR = [
    card_commands("AUDITD COMMANDS", "auditctl · ausearch · aureport", [
        {"cmd": "auditctl -w /etc/passwd -p wa -k identity", "desc": "Watch /etc/passwd for writes/attr changes"},
        {"cmd": "auditctl -w /etc/shadow -p wa -k identity", "desc": "Watch /etc/shadow"},
        {"cmd": "auditctl -w /etc/sudoers -p wa -k sudoers", "desc": "Watch /etc/sudoers"},
        {"cmd": "auditctl -a always,exit -F path=/usr/bin/sudo -F perm=x -k priv_cmd", "desc": "Audit sudo executions"},
        {"cmd": "auditctl -l", "desc": "List current audit rules"},
        {"cmd": "auditctl -D", "desc": "Delete all audit rules"},
        {"cmd": "ausearch -k identity", "desc": "Search by key"},
        {"cmd": "ausearch -m USER_CMD -ts today", "desc": "Today's user commands"},
        {"cmd": "aureport --summary", "desc": "Summarized audit report"},
        {"cmd": "aureport -x", "desc": "Executable report"},
    ]),
    card_tips("PRACTICAL INVESTIGATION EXAMPLES", [
        "Detect unauthorized access to /etc/shadow.",
        "Track changes to /etc/sudoers.",
        "Identify privilege escalation via sudo/su.",
        "Watch for unexpected file deletions.",
        "Investigate suspicious activity step-by-step.",
    ]),
]


# ----- PAGE 15 — "14. SELINUX AND APPARMOR" (badge: PAGE 14 OF 20) -----
PAGE15_ROWS = [
    {"icon": icon_shield_lock(PURPLE), "bg": "bg-purple",
     "h3": "MANDATORY ACCESS CONTROL",
     "p": "SELinux and AppArmor are Mandatory Access Control (MAC) systems that restrict what processes can do, even if they are compromised or running as root."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "SELINUX MODES",
     "p": "SELinux operates in three main modes that determine how policies are enforced: Enforcing, Permissive, and Disabled."},
    {"icon": icon_checklist(GREEN), "bg": "bg-green",
     "h3": "ENFORCING, PERMISSIVE, AND DISABLED",
     "p": "Enforcing: policies are active and violations are blocked. Permissive: policies are active but violations are only logged. Disabled: SELinux is turned off (not recommended)."},
    {"icon": icon_tag(BLUE), "bg": "bg-blue",
     "h3": "SELINUX CONTEXTS",
     "p": "SELinux uses security contexts (labels) to define what users, roles, types, and levels a process or file has. Contexts control access decisions."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "POLICY VIOLATIONS",
     "p": "When a process is blocked by SELinux, an AVC (Access Vector Cache) denial is logged. These logs show what was blocked and why."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "GETENFORCE",
     "p": "getenforce shows the current SELinux mode. Command: getenforce. Example output: Enforcing | Permissive | Disabled."},
    {"icon": icon_log(TEAL), "bg": "",
     "h3": "SESTATUS",
     "p": "sestatus displays SELinux status, mode, policy type, and other important details. Command: sestatus."},
    {"icon": icon_file(PURPLE), "bg": "bg-purple",
     "h3": "APPARMOR PROFILES",
     "p": "AppArmor uses profiles to restrict programs. Each profile defines what the program can access. Profiles are stored in /etc/apparmor.d/."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "ENFORCE VERSUS COMPLAIN MODE",
     "p": "Enforce: violations are blocked. Complain: violations are logged but not blocked. Use complain mode to test profiles before enforcing."},
    {"icon": icon_wrench(SLATE), "bg": "",
     "h3": "TROUBLESHOOTING BLOCKED APPLICATIONS SAFELY",
     "p": "Review AVC logs (ausearch -m avc -ts recent). Identify the blocked action and target. Adjust the policy or profile. Use permissive or complain mode during troubleshooting, then return to Enforcing."},
]
PAGE15_SIDEBAR = [
    card_commands("SELINUX & APPARMOR COMMANDS", "getenforce · sestatus · aa-*", [
        {"cmd": "getenforce", "desc": "Show current SELinux mode"},
        {"cmd": "sestatus", "desc": "Detailed SELinux status"},
        {"cmd": "setenforce 0", "desc": "Set SELinux to Permissive (temp)"},
        {"cmd": "setenforce 1", "desc": "Set SELinux to Enforcing (temp)"},
        {"cmd": "ausearch -m avc -ts recent", "desc": "Review recent AVC denials"},
        {"cmd": "semanage fcontext -a -t httpd_sys_content_t '/web(/.*)?'", "desc": "Set SELinux context for a path"},
        {"cmd": "restorecon -Rv /web", "desc": "Apply SELinux contexts recursively"},
        {"cmd": "apparmor_status", "desc": "AppArmor status & profiles"},
        {"cmd": "aa-enforce /etc/apparmor.d/usr.sbin.nginx", "desc": "Set AppArmor profile to enforce"},
        {"cmd": "aa-complain /etc/apparmor.d/usr.sbin.nginx", "desc": "Set AppArmor profile to complain"},
    ]),
    card_tips("TROUBLESHOOTING BLOCKED APPS", [
        "Review AVC logs: ausearch -m avc -ts recent.",
        "Identify the blocked action and target.",
        "Adjust the policy or profile.",
        "Use permissive or complain mode during testing.",
        "Return to Enforcing/Enforce mode after validation.",
    ]),
]


# ----- PAGE 16 — "15. PACKAGE, REPOSITORY, AND PATCH SECURITY" (badge: PAGE 15 OF 20) -----
PAGE16_ROWS = [
    {"icon": icon_package(ORANGE), "bg": "bg-gold",
     "h3": "TRUSTED PACKAGE REPOSITORIES",
     "p": "Use official and trusted repositories from your distribution. Avoid third-party repositories unless absolutely necessary. Untrusted repositories can introduce malicious packages."},
    {"icon": icon_tag(BLUE), "bg": "bg-blue",
     "h3": "PACKAGE SIGNATURES",
     "p": "Packages are cryptographically signed by the repository. The system verifies signatures before installing packages. Ensures integrity and authenticity of packages."},
    {"icon": icon_refresh(GREEN), "bg": "bg-green",
     "h3": "SECURITY UPDATES",
     "p": "Security updates fix vulnerabilities and reduce risk. Apply updates promptly to protect against known threats. Subscribe to security advisories for your distribution."},
    {"icon": icon_checklist(GREEN), "bg": "bg-green",
     "h3": "PATCH MANAGEMENT",
     "p": "Establish a process for testing and applying patches. Use staging environments before production rollout. Document changes and maintain rollback plans."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "VULNERABILITY EXPOSURE",
     "p": "Outdated packages are a common attack vector. Vulnerabilities can lead to privilege escalation or system compromise. Regular patching reduces your attack surface."},
    {"icon": icon_magnifier(GOLD), "bg": "bg-gold",
     "h3": "DETECTING OUTDATED PACKAGES",
     "p": "Use tools to list outdated or vulnerable packages. Examples: dnf check-update, apt list --upgradable. Regularly review and prioritize critical updates."},
    {"icon": icon_refresh(GREEN), "bg": "bg-green",
     "h3": "AUTOMATIC SECURITY UPDATES",
     "p": "Enable automatic updates for critical security patches. Tools: unattended-upgrades, dnf-automatic, yum-cron. Balance automation with change control policies."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "REPOSITORY CONFIGURATION",
     "p": "Configure repositories securely and verify URLs. Disable unnecessary or unused repositories. Ensure GPG keys are imported and trusted."},
    {"icon": icon_package(ORANGE), "bg": "bg-gold",
     "h3": "REMOVING UNNECESSARY PACKAGES",
     "p": "Remove unused packages and dependencies. Reduce system bloat and minimize attack surface. Tools: dnf remove, apt autoremove."},
    {"icon": icon_shield_check(GREEN), "bg": "bg-green",
     "h3": "PRODUCTION PATCHING STRATEGY",
     "p": "Define patch windows and maintenance schedules. Prioritize critical and high-risk vulnerabilities. Test, deploy, verify, and monitor after patching. Maintain documentation and audit patch compliance."},
]
PAGE16_SIDEBAR = [
    card_commands("PACKAGE & PATCH COMMANDS", "apt · dnf · unattended-upgrades", [
        {"cmd": "apt update", "desc": "Refresh package index"},
        {"cmd": "apt list --upgradable", "desc": "List upgradable packages"},
        {"cmd": "apt upgrade", "desc": "Install all upgrades"},
        {"cmd": "apt autoremove", "desc": "Remove unused dependencies"},
        {"cmd": "apt install unattended-upgrades", "desc": "Install automatic upgrades tool"},
        {"cmd": "dpkg-reconfigure -plow unattended-upgrades", "desc": "Enable automatic security updates"},
        {"cmd": "dnf check-update", "desc": "Check for updates (RHEL/Fedora)"},
        {"cmd": "dnf upgrade --security", "desc": "Apply only security updates"},
        {"cmd": "dnf-automatic", "desc": "Run dnf-automatic for auto-patching"},
        {"cmd": "rpm -qa --last", "desc": "List packages by install time"},
    ]),
    card_tips("PATCH MANAGEMENT BEST PRACTICES", [
        "Use only trusted, signed repositories.",
        "Subscribe to distro security advisories.",
        "Test patches in staging before production.",
        "Maintain rollback plans and backups.",
        "Automate critical security patches.",
        "Audit patch compliance regularly.",
    ]),
]


# ----- PAGE 17 — "16. FILE INTEGRITY AND PERSISTENCE DETECTION" (badge: PAGE 16 OF 20) -----
PAGE17_ROWS = [
    {"icon": icon_hash(TEAL), "bg": "",
     "h3": "FILE HASHES WITH SHA256SUM",
     "p": "Generate SHA256 hashes for files and verify them against known good values. Used to detect tampering and unauthorized modifications."},
    {"icon": icon_fingerprint(TEAL), "bg": "",
     "h3": "FILE INTEGRITY MONITORING",
     "p": "Regularly hash critical files. Store hashes securely. Compare hashes to detect changes. Use tools like AIDE, Tripwire, or OSSEC."},
    {"icon": icon_bookmark(RED), "bg": "bg-red",
     "h3": "CRON PERSISTENCE",
     "p": "Attackers plant malicious jobs in crontab, /etc/cron.*, or /var/spool/cron/. Check crontab -l and ls -la /etc/cron.* regularly."},
    {"icon": icon_server(GREEN), "bg": "bg-green",
     "h3": "SYSTEMD PERSISTENCE",
     "p": "Malicious or unknown systemd services can survive reboots. Inspect systemctl list-unit-files and /etc/systemd/system/ for suspicious units."},
    {"icon": icon_file(BLUE), "bg": "bg-blue",
     "h3": "SHELL STARTUP FILES",
     "p": "Detect unauthorized changes in ~/.bashrc, ~/.bash_profile, and /etc/profile.d/. Attackers inject commands here to persist across sessions."},
    {"icon": icon_bug(RED), "bg": "bg-red",
     "h3": "SUSPICIOUS BINARIES",
     "p": "Unknown binaries in /tmp, /dev/shm, or user home directories may indicate compromise. Hash, identify, and investigate them."},
    {"icon": icon_magnifier_alert(RED), "bg": "bg-red",
     "h3": "DETECTING UNAUTHORIZED CHANGES",
     "p": "Monitor critical files and directories. Track new or modified binaries. Review file ownership and permissions. Alert on unexpected changes."},
    {"icon": icon_checklist(GREEN), "bg": "bg-green",
     "h3": "PROTECT. MONITOR. VERIFY.",
     "p": "Integrity today, security forever. Combine hashing, monitoring tools, and configuration baselines to detect persistence and tampering."},
]
PAGE17_SIDEBAR = [
    card_file_list("CRITICAL SYSTEM FILES", [
        {"icon": icon_file(BLUE), "path": "/etc/passwd", "desc": "User account information"},
        {"icon": icon_file_rects(GREEN), "path": "/etc/shadow", "desc": "Encrypted passwords"},
        {"icon": icon_file(PURPLE), "path": "/etc/sudoers", "desc": "Sudo configuration"},
        {"icon": icon_file(BLUE), "path": "/etc/ssh/sshd_config", "desc": "SSH server configuration"},
        {"icon": icon_folder(GOLD), "path": "/bin, /sbin, /usr/bin, /usr/sbin", "desc": "System binaries"},
        {"icon": icon_folder(GOLD), "path": "/etc/systemd/system/", "desc": "Custom systemd units"},
        {"icon": icon_folder(GOLD), "path": "/boot/", "desc": "Kernel & bootloader"},
        {"icon": icon_folder(GOLD), "path": "/var/spool/cron/", "desc": "User cron jobs"},
        {"icon": icon_folder(GOLD), "path": "/root/.bashrc, /root/.ssh/", "desc": "Root shell & SSH"},
    ], warn_text="Hash these files regularly. Any change = investigate immediately."),
    card_commands("INTEGRITY & PERSISTENCE COMMANDS", "sha256sum · crontab · systemctl", [
        {"cmd": "sha256sum /etc/passwd", "desc": "Hash a file"},
        {"cmd": "sha256sum -r /etc > etc.sha256", "desc": "Hash /etc recursively"},
        {"cmd": "sha256sum -c etc.sha256", "desc": "Verify against known good list"},
        {"cmd": "crontab -l", "desc": "List user cron jobs"},
        {"cmd": "ls -la /etc/cron.* /var/spool/cron/", "desc": "Inspect cron directories"},
        {"cmd": "systemctl list-unit-files --type=service", "desc": "List all systemd services"},
        {"cmd": "ls -la /etc/systemd/system/", "desc": "Inspect custom units"},
        {"cmd": "cat ~/.bashrc", "desc": "Check shell startup file"},
        {"cmd": "aide --check", "desc": "Run AIDE integrity check"},
    ]),
]


# ----- PAGE 18 — "17. SECRETS, CREDENTIALS, AND SENSITIVE DATA" (badge: PAGE 17 OF 20) -----
PAGE18_ROWS = [
    {"icon": icon_file(BLUE), "bg": "bg-blue",
     "h3": "1. CONFIGURATION FILES",
     "p": "Avoid storing passwords, API keys, or tokens in plain-text config files. Common files: /etc/*.conf, ~/.config/*, /var/www/html/*.php, .env, settings.json."},
    {"icon": icon_sliders(BLUE), "bg": "bg-blue",
     "h3": "2. ENVIRONMENT VARIABLES",
     "p": "Environment variables may contain secrets. Check: env, printenv, cat /proc/*/environ. Never pass secrets via env on shared systems."},
    {"icon": icon_key(GOLD), "bg": "bg-gold",
     "h3": "3. SSH PRIVATE KEYS",
     "p": "Protect private keys at all times. Default location: ~/.ssh/. Check: ~/.ssh/id_rsa. Store securely. Key permissions 600. Avoid hardcoding. Rotate regularly. Never share private keys."},
    {"icon": icon_database(BLUE), "bg": "bg-blue",
     "h3": "4. DATABASE CREDENTIALS",
     "p": "Credentials should never be stored in plain text. Check config files, scripts, and environment variables. Use vaults or secret managers."},
    {"icon": icon_padlock(RED), "bg": "bg-red",
     "h3": "5. FILE PERMISSION MISTAKES",
     "p": "Incorrect permissions can expose secrets. Sensitive files should be readable by owner only. Check: ls -l <file>. Fix with: chmod 600 <file>."},
    {"icon": icon_log(TEAL), "bg": "",
     "h3": "6. SHELL HISTORY EXPOSURE",
     "p": "Commands containing secrets may be saved in history. Check ~/.bash_history. Clear history when needed: history -c && history -w."},
    {"icon": icon_terminal(), "bg": "",
     "h3": "7. PROCESS ARGUMENT EXPOSURE",
     "p": "Secrets passed as arguments can be visible to other users. Check running processes: ps aux. Avoid passing secrets as command-line arguments."},
    {"icon": icon_refresh(GREEN), "bg": "bg-green",
     "h3": "8. PROCESS ENVIRONMENT EXPOSURE",
     "p": "Process environ may contain secrets. Check /proc/<pid>/environ. Run secrets-bearing services as isolated users."},
    {"icon": icon_key(GOLD), "bg": "bg-gold",
     "h3": "9. SECRET ROTATION",
     "p": "Rotate credentials regularly. Revoke old keys and tokens. Automate rotation where possible. Document rotation procedures. Monitor for unused credentials."},
    {"icon": icon_magnifier(GOLD), "bg": "bg-gold",
     "h3": "10. SEARCHING SYSTEMS FOR EXPOSED CREDENTIALS",
     "p": "Search for common patterns: grep -rni \"password|passwd|api_key|secret|token\" /. Use tools: ripgrep (rg), trufflehog, git-secrets, gitleaks."},
]
PAGE18_SIDEBAR = [
    card_commands("SECRET-SCANNING COMMANDS", "grep · rg · trufflehog", [
        {"cmd": "grep -rni \"password\" /", "desc": "Search for 'password'"},
        {"cmd": "grep -rni \"passwd\" /", "desc": "Search for 'passwd'"},
        {"cmd": "grep -rni \"api_key\" /", "desc": "Search for 'api_key'"},
        {"cmd": "grep -rni \"secret\" /", "desc": "Search for 'secret'"},
        {"cmd": "grep -rni \"token\" /", "desc": "Search for 'token'"},
        {"cmd": "rg -i \"password|secret|token\" /etc", "desc": "ripgrep across /etc"},
        {"cmd": "trufflehog filesystem --path=/", "desc": "Scan filesystem with trufflehog"},
        {"cmd": "git-secrets --scan -r /repo", "desc": "Scan a repo with git-secrets"},
        {"cmd": "gitleaks detect --source=/repo", "desc": "Scan a repo with gitleaks"},
    ]),
    card_tips("SECRET HYGIENE", [
        "Use a vault or secret manager (no plain text).",
        "Private keys: 600, never commit to git.",
        "Rotate credentials regularly; revoke old ones.",
        "Never pass secrets as command-line arguments.",
        "Clear shell history after using secrets.",
        "Scan repositories before every push.",
    ]),
]


# ----- PAGE 19 — "18. LINUX SECURITY HARDENING BASELINE" (badge: PAGE 18 OF 20) -----
PAGE19_ROWS = [
    {"icon": icon_checklist(GREEN), "bg": "bg-green",
     "h3": "SECURE INSTALLATION BASELINE",
     "p": "Install a minimal OS. Use trusted repositories only. Configure hostname, timezone, and NTP."},
    {"icon": icon_package(ORANGE), "bg": "bg-gold",
     "h3": "REMOVE UNNECESSARY SOFTWARE",
     "p": "Remove unused packages. Avoid installing unnecessary tools. Reduce attack surface."},
    {"icon": icon_lock_open(ORANGE), "bg": "bg-gold",
     "h3": "DISABLE UNUSED SERVICES",
     "p": "Identify unnecessary services. Disable and stop them. Prevent unwanted exposure."},
    {"icon": icon_wall(ORANGE), "bg": "bg-gold",
     "h3": "CONFIGURE FIREWALL RULES",
     "p": "Apply default deny policy. Allow only required services. Restrict admin ports. Review rules regularly."},
    {"icon": icon_eye(PURPLE), "bg": "bg-purple",
     "h3": "ENABLE AUDITING",
     "p": "Install and configure auditd. Monitor privileged commands. Watch critical files and directories. Review audit logs regularly."},
    {"icon": icon_shield_person(BLUE), "bg": "bg-blue",
     "h3": "RESTRICT PRIVILEGED ACCESS",
     "p": "Limit root access. Use sudo with least privilege. Review and tighten sudoers rules."},
    {"icon": icon_refresh(GREEN), "bg": "bg-green",
     "h3": "APPLY SECURITY UPDATES",
     "p": "Keep system and packages updated. Enable automatic security updates where possible. Regularly check for vulnerabilities."},
    {"icon": icon_key(GOLD), "bg": "bg-gold",
     "h3": "HARDEN SSH",
     "p": "Disable root login. Disable password authentication. Use key-based authentication. Restrict users and groups."},
    {"icon": icon_checklist(BLUE), "bg": "bg-blue",
     "h3": "CIS BENCHMARK CONCEPTS",
     "p": "Follow CIS Benchmark guidelines. Apply secure configurations. Validate settings against CIS controls. Continuously improve security posture."},
    {"icon": icon_folder(GOLD), "bg": "bg-gold",
     "h3": "SECURE FILESYSTEM PERMISSIONS",
     "p": "Set correct ownership and permissions. Use least-privilege file access. Audit critical directories and files."},
    {"icon": icon_doc_search(PURPLE), "bg": "bg-purple",
     "h3": "DOCUMENTING APPROVED EXCEPTIONS",
     "p": "Document any security exceptions. Include business justification. Review and revalidate regularly."},
]
PAGE19_SIDEBAR = [
    card_tips("HARDENING BASELINE — A STRONG START", [
        "Minimal install + trusted repositories.",
        "Remove unused packages & services.",
        "Default-deny firewall + restricted admin ports.",
        "auditd enabled, watching privileged commands.",
        "Root access limited; sudo least-privilege.",
        "Auto security updates enabled.",
        "SSH: keys only, no root, restricted users.",
        "CIS Benchmark compliance validated.",
        "Filesystem permissions audited.",
        "Exceptions documented with business justification.",
    ]),
    card_commands("HARDENING COMMANDS", "systemctl · ufw · apt · visudo", [
        {"cmd": "systemctl disable --now <service>", "desc": "Disable a service"},
        {"cmd": "ufw default deny incoming", "desc": "Default-deny inbound"},
        {"cmd": "ufw allow 22/tcp", "desc": "Allow SSH"},
        {"cmd": "apt install auditd", "desc": "Install auditd"},
        {"cmd": "visudo", "desc": "Safely edit sudoers"},
        {"cmd": "apt install unattended-upgrades", "desc": "Auto security updates"},
        {"cmd": "sed -i 's/#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config", "desc": "Disable SSH root login"},
        {"cmd": "sshd -t", "desc": "Validate SSH config"},
    ]),
]


# ----- PAGE 20 — "19. PRODUCTION SECURITY INCIDENT INVESTIGATION" (badge: PAGE 19 OF 20) -----
# This page uses a special layout: rows (text) + steps-grid (sidebar replacement).
PAGE20_STEPS = [
    {"n": "01", "title": "IDENTIFY ACTIVE USERS", "code": "who; whoami; w"},
    {"n": "02", "title": "REVIEW RECENT LOGINS", "code": "last; last -a; lastlog"},
    {"n": "03", "title": "SEARCH AUTHENTICATION LOGS", "code": "grep -E 'sshd|login|su|sudo' /var/log/auth.log"},
    {"n": "04", "title": "CHECK FAILED SSH ATTEMPTS", "code": "grep \"Failed password\" /var/log/auth.log"},
    {"n": "05", "title": "INSPECT SUDO ACTIVITY", "code": "sudo journalctl -u sudo; ausearch -m USER_CMD"},
    {"n": "06", "title": "CHECK CRON JOBS & SYSTEMD UNITS", "code": "crontab -l; ls -la /etc/cron.*; systemctl list-unit-files --type=service"},
    {"n": "07", "title": "FIND RECENTLY MODIFIED FILES", "code": "find / -type f -mtime -1 -ls"},
    {"n": "08", "title": "LOOK FOR SUID BINARIES", "code": "find / -type f -perm -4000 -ls 2>/dev/null"},
    {"n": "09", "title": "CHECK NEW OR MODIFIED USER ACCOUNTS", "code": "cut -d: -f1 /etc/passwd; getent passwd"},
    {"n": "10", "title": "REVIEW RUNNING PROCESSES", "code": "ps aux; top; pstree -p"},
    {"n": "11", "title": "IDENTIFY OPEN PORTS", "code": "ss -tulpen; netstat -tulpen"},
    {"n": "12", "title": "INSPECT NETWORK CONNECTIONS", "code": "ss -antp; lsof -i -P -n"},
    {"n": "13", "title": "PRESERVE EVIDENCE", "code": "journalctl -u ssh > /root/evidence_auth_$(date +%F).log; dmesg > /root/evidence_dmesg_$(date +%F).log"},
]


def build_page_20() -> str:
    """Page 20: incident investigation — scenario + 13 steps grid."""
    steps_html = []
    for s in PAGE20_STEPS:
        steps_html.append(
            '<div class="step">\n'
            f'            <div class="shead"><div class="snum">{s["n"]}</div><div class="stitle">{esc(s["title"])}</div></div>\n'
            f'            <div class="scode">{esc(s["code"])}</div>\n'
            '          </div>'
        )
    steps_grid = "\n        ".join(steps_html)
    scenario_card = (
        '<div class="card">\n'
        '          <div class="head">SCENARIO</div>\n'
        '          <div class="body-pad">\n'
        '            <p style="font-size:13px;color:var(--ink);font-weight:600;line-height:1.5;">A Linux server shows suspicious activity. Follow these investigation steps to identify, contain, and document the incident.</p>\n'
        '            <div class="dashed"></div>\n'
        '            <div class="warn">\n'
        '              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">\n'
        f'                <path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" fill="{RED}"/>\n'
        '                <rect x="11" y="7" width="2" height="6" rx="1" fill="#ffffff"/>\n'
        '                <circle cx="12" cy="16" r="1.1" fill="#ffffff"/>\n'
        '              </svg>\n'
        '              <p>Always preserve evidence before taking corrective action. Document everything.</p>\n'
        '            </div>\n'
        '          </div>\n'
        '        </div>'
    )
    inner = (
        f'{top_strip("PAGE 19 OF 20")}\n\n'
        '    <!-- TITLE -->\n'
        '    <div class="title-block">\n'
        '      <h1 class="title">19. PRODUCTION SECURITY<br>INCIDENT INVESTIGATION</h1>\n'
        '    </div>\n'
        '    <div class="divider">\n'
        '      <span class="line"></span><span class="dot"></span><span class="line"></span>\n'
        '    </div>\n\n'
        '    <!-- BODY -->\n'
        '    <div class="body">\n\n'
        f'      <div class="rows">\n        {scenario_card}\n      </div>\n\n'
        '      <div class="sidebar">\n'
        f'        <div class="card">\n'
        '          <div class="head">INVESTIGATION STEPS</div>\n'
        '          <div class="cmd-head-row">\n'
        '            <span class="term-pill"><span class="arrow">&gt;_</span></span>\n'
        '            <span class="lbl">13 steps · live forensics</span>\n'
        '          </div>\n'
        f'          <div style="padding:12px 14px;">\n            <div class="steps-grid">\n        {steps_grid}\n            </div>\n          </div>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>'
    )
    return page_wrapper(inner)


# ============================================================================
# MAIN — assemble all 20 pages and write to disk
# ============================================================================


def build_all_pages() -> list[str]:
    pages: list[str] = []

    # PAGE 1 — COVER
    pages.append(build_cover())

    # PAGE 2 — 1. LINUX SECURITY FOUNDATIONS (badge: PAGE 1 OF 20)
    pages.append(build_content_page(
        "PAGE 1 OF 20",
        "1. LINUX SECURITY<br>FOUNDATIONS",
        PAGE2_ROWS,
        PAGE2_SIDEBAR,
    ))

    # PAGE 3 — 2. USERS, GROUPS, AND IDENTITY SECURITY (EXACT reference copy)
    pages.append(build_reference_page_3())

    # PAGE 4 — 3. PASSWORD AND ACCOUNT SECURITY
    pages.append(build_content_page(
        "PAGE 3 OF 20",
        "3. PASSWORD AND<br>ACCOUNT SECURITY",
        PAGE4_ROWS,
        PAGE4_SIDEBAR,
    ))

    # PAGE 5 — 4. FILE AND DIRECTORY PERMISSIONS
    pages.append(build_content_page(
        "PAGE 4 OF 20",
        "4. FILE AND DIRECTORY<br>PERMISSIONS",
        PAGE5_ROWS,
        PAGE5_SIDEBAR,
    ))

    # PAGE 6 — 5. SUID, SGID, STICKY BIT, AND ACLs
    pages.append(build_content_page(
        "PAGE 5 OF 20",
        "5. SUID, SGID, STICKY<br>BIT, AND ACLs",
        PAGE6_ROWS,
        PAGE6_SIDEBAR,
    ))

    # PAGE 7 — 6. SUDO AND PRIVILEGE ESCALATION SECURITY
    pages.append(build_content_page(
        "PAGE 6 OF 20",
        "6. SUDO AND PRIVILEGE<br>ESCALATION SECURITY",
        PAGE7_ROWS,
        PAGE7_SIDEBAR,
    ))

    # PAGE 8 — 7. SSH SERVER HARDENING
    pages.append(build_content_page(
        "PAGE 7 OF 20",
        "7. SSH SERVER<br>HARDENING",
        PAGE8_ROWS,
        PAGE8_SIDEBAR,
    ))

    # PAGE 9 — 8. LINUX SERVICES AND SYSTEMD SECURITY
    pages.append(build_content_page(
        "PAGE 8 OF 20",
        "8. LINUX SERVICES AND<br>SYSTEMD SECURITY",
        PAGE9_ROWS,
        PAGE9_SIDEBAR,
    ))

    # PAGE 10 — 9. NETWORK EXPOSURE AND OPEN PORTS
    pages.append(build_content_page(
        "PAGE 9 OF 20",
        "9. NETWORK EXPOSURE<br>AND OPEN PORTS",
        PAGE10_ROWS,
        PAGE10_SIDEBAR,
    ))

    # PAGE 11 — 10. LINUX FIREWALL SECURITY
    pages.append(build_content_page(
        "PAGE 10 OF 20",
        "10. LINUX FIREWALL<br>SECURITY",
        PAGE11_ROWS,
        PAGE11_SIDEBAR,
    ))

    # PAGE 12 — 11. PROCESS AND RUNTIME SECURITY
    pages.append(build_content_page(
        "PAGE 11 OF 20",
        "11. PROCESS AND<br>RUNTIME SECURITY",
        PAGE12_ROWS,
        PAGE12_SIDEBAR,
    ))

    # PAGE 13 — 12. LOGGING AND SECURITY INVESTIGATION
    pages.append(build_content_page(
        "PAGE 12 OF 20",
        "12. LOGGING AND<br>SECURITY INVESTIGATION",
        PAGE13_ROWS,
        PAGE13_SIDEBAR,
    ))

    # PAGE 14 — 13. LINUX AUDITING WITH AUDITD
    pages.append(build_content_page(
        "PAGE 13 OF 20",
        "13. LINUX AUDITING<br>WITH AUDITD",
        PAGE14_ROWS,
        PAGE14_SIDEBAR,
    ))

    # PAGE 15 — 14. SELINUX AND APPARMOR
    pages.append(build_content_page(
        "PAGE 14 OF 20",
        "14. SELINUX<br>AND APPARMOR",
        PAGE15_ROWS,
        PAGE15_SIDEBAR,
    ))

    # PAGE 16 — 15. PACKAGE, REPOSITORY, AND PATCH SECURITY
    pages.append(build_content_page(
        "PAGE 15 OF 20",
        "15. PACKAGE, REPOSITORY,<br>AND PATCH SECURITY",
        PAGE16_ROWS,
        PAGE16_SIDEBAR,
    ))

    # PAGE 17 — 16. FILE INTEGRITY AND PERSISTENCE DETECTION
    pages.append(build_content_page(
        "PAGE 16 OF 20",
        "16. FILE INTEGRITY AND<br>PERSISTENCE DETECTION",
        PAGE17_ROWS,
        PAGE17_SIDEBAR,
    ))

    # PAGE 18 — 17. SECRETS, CREDENTIALS, AND SENSITIVE DATA
    pages.append(build_content_page(
        "PAGE 17 OF 20",
        "17. SECRETS, CREDENTIALS,<br>AND SENSITIVE DATA",
        PAGE18_ROWS,
        PAGE18_SIDEBAR,
    ))

    # PAGE 19 — 18. LINUX SECURITY HARDENING BASELINE
    pages.append(build_content_page(
        "PAGE 18 OF 20",
        "18. LINUX SECURITY<br>HARDENING BASELINE",
        PAGE19_ROWS,
        PAGE19_SIDEBAR,
    ))

    # PAGE 20 — 19. PRODUCTION SECURITY INCIDENT INVESTIGATION
    pages.append(build_page_20())

    return pages


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Linux Security Handbook — 20 Pages</title>
<style>
{css}
</style>
</head>
<body class="multi-page">

{pages}

</body>
</html>
<!-- All inline SVG icons are original vector illustrations created for this
     document. Spiral binding rendered via CSS background-image SVG. -->
"""


def main() -> None:
    pages = build_all_pages()
    full_html = HTML_TEMPLATE.format(css=CSS, pages="\n\n".join(pages))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(full_html, encoding="utf-8")

    # Quick stats
    page_count = full_html.count('<div class="page-wrapper">')
    svg_count = full_html.count("<svg")
    veriqta_count = sum(
        s.lower().count("veriqta") for s in full_html.lower().split("veriqta")
    ) - 1  # subtract the split
    veriqta_count = full_html.lower().count("veriqta")
    social_count = (
        full_html.lower().count("@veriqta")
        + full_html.lower().count("youtube")
        + full_html.lower().count("github")
        + full_html.lower().count("linkedin")
        + full_html.lower().count("instagram")
        + full_html.lower().count("telegram")
    )

    print(f"Wrote: {OUT_PATH}")
    print(f"  Size:        {len(full_html):,} bytes")
    print(f"  Pages:       {page_count}")
    print(f"  SVG icons:   {svg_count}")
    print(f"  VERIQTA:     {veriqta_count} (must be 0)")
    print(f"  Social refs: {social_count} (must be 0)")


if __name__ == "__main__":
    main()
