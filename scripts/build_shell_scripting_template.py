#!/usr/bin/env python3
"""
Shared CSS + HTML template for recreating the Shell Scripting for DevOps
carousel pages as self-contained notebook-style HTML files.

Each output HTML file uses the notebook page layout (spiral binding, punched
holes, graph-paper background) from the existing instagram-carousel template,
with the carousel page's content recreated as real HTML text, CSS, and SVG.

Usage by subagents:
  from build_shell_scripting_template import NOTEBOOK_CSS, page_wrapper
  html = page_wrapper(page_num, title, subtitle, body_html)
"""

# ============================================================
# SHARED NOTEBOOK CSS
# Based on instagram-carousel-dcdsiahfbh0.html + linux-security-handbook.html
# Enhanced with content styles for the Shell Scripting handbook pages.
# ============================================================

NOTEBOOK_CSS = r"""
  /* ============================================================
     RESET & ROOT VARIABLES
     ============================================================ */
  :root{
    --paper:#f5f1e8;
    --paper-2:#efe9dd;
    --grid-line:#bcc8d6;
    --navy:#15264d;
    --navy-2:#1e3160;
    --ink:#1c1c1c;
    --ink-2:#3a3f47;
    --ink-3:#6b7280;
    --green:#1B5E3F;
    --green-2:#164a32;
    --green-light:#e8f5ee;
    --green-soft:#cdf3da;
    --blue:#2563eb;
    --blue-soft:#cfe0ff;
    --purple:#7c3aed;
    --purple-soft:#e2d4ff;
    --red:#dc2626;
    --red-soft:#ffd4d4;
    --gold:#d4a017;
    --gold-soft:#fce9b6;
    --orange:#e65100;
    --orange-soft:#fff3e0;
    --teal:#0d7377;
    --teal-soft:#d0f0f0;
    --terminal-bg:#0d1117;
    --terminal-fg:#e6edf3;
    --terminal-green:#7ee787;
    --terminal-amber:#f2cc60;
    --terminal-blue:#79c0ff;
    --terminal-dim:#8b949e;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:#cfc9bb;}
  body{
    font-family:"Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;
    color:var(--ink);
    display:flex;flex-direction:column;align-items:center;
    padding:24px 12px;
  }

  /* Wrapper holds page + binding */
  .page-wrapper{
    position:relative;
    width:1080px;
  }

  /* ============================================================
     PAGE / NOTEBOOK SHEET
     ============================================================ */
  .page{
    position:relative;
    width:1080px;
    background:var(--paper);
    border-radius:14px;
    box-shadow:0 22px 60px rgba(0,0,0,0.28), 0 2px 0 rgba(0,0,0,0.06) inset;
    overflow:hidden;
    padding:42px 50px 26px 78px;
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

  /* Page edge shadows (3D thickness) */
  .page-top-edge,.page-bottom-edge{
    position:absolute;left:0;right:0;height:6px;z-index:1;pointer-events:none;
  }
  .page-top-edge{top:0;background:linear-gradient(to bottom,rgba(0,0,0,.08),transparent);}
  .page-bottom-edge{bottom:0;background:linear-gradient(to top,rgba(0,0,0,.08),transparent);}

  /* ============================================================
     SPIRAL BINDING + HOLES
     ============================================================ */
  .spiral{
    position:absolute;z-index:7;top:0;left:-30px;width:120px;height:100%;pointer-events:none;
    background-image:url("data:image/svg+xml;utf8,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='90'%20height='70'%20viewBox='0%200%2090%2070'%20fill='none'%3E%3Cpath%20d='M32%2027%20C20%2028%2010%2032%2010%2035%20C10%2040%2019%2043%2032%2044%20C52%2045%2070%2042%2082%2038'%20stroke='%23111'%20stroke-width='3'%20stroke-linecap='round'%20stroke-linejoin='round'/%3E%3Cpath%20d='M32%2034%20C20%2035%2010%2039%2010%2042%20C10%2047%2019%2050%2032%2051%20C52%2052%2070%2049%2082%2045'%20stroke='%23111'%20stroke-width='3'%20stroke-linecap='round'%20stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat:repeat-y;
  }
  .holes{
    position:absolute;z-index:6;top:0;left:18px;width:24px;height:100%;pointer-events:none;
    background-image:radial-gradient(circle, #c9bfa8 3px, transparent 4px);
    background-size:24px 80px;
    background-position:center 40px;
    background-repeat:repeat-y;
  }

  /* ============================================================
     CONTENT WRAPPER
     ============================================================ */
  .content{position:relative;z-index:2;}

  /* Brand bar (top) */
  .brand-bar{
    display:flex;align-items:center;justify-content:space-between;
    margin-bottom:20px;
  }
  .brand-logo{
    display:flex;align-items:center;gap:8px;
    font-size:14px;font-weight:800;letter-spacing:1px;
    color:var(--green);
  }
  .brand-logo .vq-icon{width:24px;height:24px;}
  .brand-badge{
    background:var(--green);color:#fff;
    padding:6px 16px;border-radius:999px;
    font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
  }

  /* Page title */
  .page-title{
    font-size:38px;font-weight:800;color:var(--green);
    text-transform:uppercase;letter-spacing:-.5px;line-height:1.1;
    margin-bottom:6px;
  }
  .page-title .num{color:var(--green-2);}
  .page-subtitle{
    font-size:14px;font-weight:600;color:var(--ink-2);
    text-transform:uppercase;letter-spacing:1px;
    margin-bottom:20px;
    padding-bottom:14px;
    border-bottom:2px solid var(--green);
    position:relative;
  }
  .page-subtitle::after{
    content:"";position:absolute;left:50%;bottom:-6px;
    width:10px;height:10px;background:var(--green);
    border-radius:50%;transform:translateX(-50%);
  }

  /* Body grid: rows + sidebar */
  .body{
    display:grid;
    grid-template-columns:1.85fr 1fr;
    gap:20px;
    margin-bottom:20px;
  }
  .body.single{grid-template-columns:1fr;}

  /* Section rows (left column) */
  .rows{display:flex;flex-direction:column;gap:12px;}
  .row{
    display:flex;gap:12px;align-items:flex-start;
    background:rgba(255,255,255,.5);
    border-radius:10px;padding:10px 12px;
    border-left:3px solid var(--green);
  }
  .row .icon{
    flex-shrink:0;width:42px;height:42px;
    border-radius:10px;
    display:flex;align-items:center;justify-content:center;
    background:var(--green-light);
  }
  .row .icon svg{width:24px;height:24px;}
  .row .text{flex:1;min-width:0;}
  .row .text h3{
    font-size:13px;font-weight:700;color:var(--green);
    text-transform:uppercase;letter-spacing:.3px;
    margin-bottom:3px;
  }
  .row .text p{
    font-size:12px;color:var(--ink-2);line-height:1.45;
  }
  .row .text code{
    font-family:"JetBrains Mono","Fira Code",monospace;
    font-size:11px;
    background:#e8e4d4;padding:1px 5px;border-radius:3px;
    color:var(--green-2);
  }

  /* Sidebar cards (right column) */
  .sidebar{display:flex;flex-direction:column;gap:12px;}
  .card{
    background:#fff;border-radius:10px;overflow:hidden;
    box-shadow:0 2px 8px rgba(0,0,0,.06);
    border:1px solid rgba(0,0,0,.05);
  }
  .card .head{
    background:var(--green);color:#fff;
    padding:8px 14px;
    font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
    display:flex;align-items:center;gap:6px;
  }
  .card .head svg{width:14px;height:14px;}
  .card .body-pad{padding:12px 14px;}

  /* Terminal / code block */
  .terminal{
    background:var(--terminal-bg);border-radius:8px;overflow:hidden;
    box-shadow:0 4px 14px rgba(0,0,0,.2);
  }
  .terminal .term-bar{
    background:#1c2230;padding:6px 12px;
    display:flex;align-items:center;gap:6px;
  }
  .terminal .term-dot{width:10px;height:10px;border-radius:50%;}
  .terminal .dot-red{background:#ff5f56;}
  .terminal .dot-amber{background:#ffbd2e;}
  .terminal .dot-green{background:#27c93f;}
  .terminal .term-title{
    margin-left:auto;color:var(--terminal-dim);
    font-size:10px;font-family:monospace;
  }
  .terminal .term-body{
    padding:12px 14px;
    font-family:"JetBrains Mono","Fira Code",monospace;
    font-size:12px;line-height:1.6;
    color:var(--terminal-fg);
  }
  .terminal .term-body .prompt{color:var(--terminal-green);}
  .terminal .term-body .comment{color:var(--terminal-dim);}
  .terminal .term-body .cmd{color:var(--terminal-blue);}
  .terminal .term-body .str{color:var(--terminal-amber);}
  .terminal .term-body .out{color:var(--terminal-fg);}

  /* Inline code */
  code.inline{
    font-family:"JetBrains Mono","Fira Code",monospace;
    font-size:11px;
    background:#e8e4d4;padding:1px 5px;border-radius:3px;
    color:var(--green-2);
  }

  /* Tables */
  .tbl{width:100%;border-collapse:collapse;font-size:11px;}
  .tbl th{
    background:var(--green);color:#fff;
    padding:6px 10px;text-align:left;
    font-weight:700;font-size:10px;letter-spacing:.3px;text-transform:uppercase;
  }
  .tbl td{
    padding:6px 10px;
    border-bottom:1px solid #e0d8c8;
    color:var(--ink-2);
  }
  .tbl td code{
    font-family:"JetBrains Mono",monospace;font-size:10px;
    background:#e8e4d4;padding:1px 4px;border-radius:3px;
    color:var(--green-2);
  }
  .tbl tr:last-child td{border-bottom:none;}

  /* Warning / tip callout */
  .callout{
    display:flex;gap:10px;align-items:flex-start;
    border-radius:10px;padding:10px 14px;
    font-size:12px;line-height:1.45;
  }
  .callout.warn{
    background:#fff4e0;border-left:3px solid var(--orange);
    color:var(--ink-2);
  }
  .callout.tip{
    background:var(--green-light);border-left:3px solid var(--green);
    color:var(--ink-2);
  }
  .callout .ico{flex-shrink:0;width:18px;height:18px;margin-top:1px;}

  /* Numbered step list */
  .steps{display:flex;flex-direction:column;gap:8px;}
  .step{
    display:flex;gap:10px;align-items:flex-start;
    font-size:12px;color:var(--ink-2);line-height:1.45;
  }
  .step .n{
    flex-shrink:0;width:20px;height:20px;border-radius:50%;
    background:var(--green);color:#fff;
    display:flex;align-items:center;justify-content:center;
    font-size:10px;font-weight:800;font-family:monospace;
  }

  /* Two-column comparison */
  .compare{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
  .compare .col{
    border-radius:8px;padding:10px 12px;
    font-size:11px;line-height:1.5;
  }
  .compare .col h4{
    font-size:11px;font-weight:700;text-transform:uppercase;
    margin-bottom:6px;letter-spacing:.3px;
  }
  .compare .col.left{background:#fce9b6;color:var(--ink);}
  .compare .col.left h4{color:var(--orange);}
  .compare .col.right{background:var(--green-light);color:var(--ink);}
  .compare .col.right h4{color:var(--green);}
  .compare .col ul{list-style:none;padding:0;}
  .compare .col li{margin-bottom:3px;padding-left:12px;position:relative;}
  .compare .col li::before{content:"•";position:absolute;left:0;}

  /* Icon-colored backgrounds */
  .bg-green{background:var(--green-light)!important;}
  .bg-blue{background:var(--blue-soft)!important;}
  .bg-purple{background:var(--purple-soft)!important;}
  .bg-red{background:var(--red-soft)!important;}
  .bg-gold{background:var(--gold-soft)!important;}
  .bg-teal{background:var(--teal-soft)!important;}
  .bg-orange{background:var(--orange-soft)!important;}

  /* Icon colors */
  .ic-green{color:var(--green);}
  .ic-blue{color:var(--blue);}
  .ic-purple{color:var(--purple);}
  .ic-red{color:var(--red);}
  .ic-gold{color:var(--gold);}
  .ic-teal{color:var(--teal);}
  .ic-orange{color:var(--orange);}

  /* Social footer */
  .social-footer{
    display:flex;align-items:center;justify-content:space-around;
    border:2px solid var(--green);border-radius:12px;
    padding:10px 16px;margin-top:16px;
  }
  .social-footer .social{
    display:flex;flex-direction:column;align-items:center;gap:3px;
    font-size:9px;font-weight:700;letter-spacing:.5px;
    color:var(--green);text-transform:uppercase;
  }
  .social-footer .social svg{width:18px;height:18px;}

  /* Watermark pattern */
  .watermark{
    position:absolute;inset:0;z-index:0;pointer-events:none;
    opacity:.04;overflow:hidden;
  }
  .watermark span{
    position:absolute;
    font-size:60px;font-weight:800;letter-spacing:4px;
    color:var(--green);white-space:nowrap;
    transform:rotate(-30deg);
  }

  /* ============================================================
     PRINT / PDF
     ============================================================ */
  @page{size:1080px 1353px;margin:0;}
  @media print{
    html,body{background:#fff;padding:0;}
    .page-wrapper{page-break-after:always;}
    .page-wrapper:last-child{page-break-after:auto;}
    .page{box-shadow:none;border-radius:0;}
  }
"""

# ============================================================
# SVG ICON LIBRARY (green outline style matching the carousel)
# ============================================================

ICONS = {
    "terminal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="M6 9 L9 11.5 L6 14"/><line x1="11" y1="14" x2="17" y2="14"/></svg>',
    "file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.5h9l4 4v15h-13z"/><path d="M15 2.5v4h4"/></svg>',
    "folder": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 6.5a2 2 0 0 1 2-2h5l2 2.5h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z"/></svg>',
    "gear": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2 L13.5 5 L16.5 4.5 L17.5 7.5 L20.5 8.5 L19.5 11.5 L22 13 L20.5 15.5 L22 18.5 L19 19 L17.5 22 L14.5 21 L13 23.5 L10.5 22 L7.5 23 L6 20.5 L3 20 L4 17 L1.5 14.5 L3 12 L1.5 9 L4.5 8 L5.5 5 L8.5 5.5 L10.5 3 z" opacity="0.3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "lightbulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3v1h6v-1c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/></svg>',
    "cloud": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19a4.5 4.5 0 0 0 0-9 6 6 0 0 0-11.5 1.5A4 4 0 0 0 6 19z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 L9 17 L4 12"/></svg>',
    "check-square": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 12 L11 15 L16 9" stroke-width="2.5"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4" ry="10"/><line x1="2" y1="12" x2="22" y2="12"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="M10 9 L15 12 L10 15 Z" fill="currentColor"/></svg>',
    "git": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="9" r="2.5"/><path d="M6 8.5v7"/><path d="M18 11.5c0 3-4 3-6 3"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="2.5" width="19" height="19" rx="2.5"/><line x1="7" y1="10" x2="7" y2="17"/><circle cx="7" cy="6.5" r="0.5" fill="currentColor"/><path d="M11 17v-4a2.5 2.5 0 0 1 5 0v4"/><line x1="11" y1="10" x2="11" y2="17"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="4" x2="20" y2="20"/><line x1="20" y1="4" x2="4" y2="20"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.5" fill="currentColor"/></svg>',
    "telegram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 4 L3 11 L9 13 L11 20 L13.5 16 L18 20 z"/><path d="M9 13 L18 7"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h7a3 3 0 0 1 3 3v14a2 2 0 0 0-2-2H4z"/><path d="M20 4h-7a3 3 0 0 0-3 3v14a2 2 0 0 1 2-2h8z"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="8" r="2.5"/><path d="M16 20a5 5 0 0 1 5-5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z"/></svg>',
    "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="4"/><path d="M11 11 L20 20"/><path d="M17 17 L20 14"/><path d="M14 20 L11 17"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "arrow-right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="12" x2="20" y2="12"/><polyline points="14 6 20 12 14 18"/></svg>',
    "warning": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 L22 20 H2 Z"/><line x1="12" y1="9" x2="12" y2="14"/><circle cx="12" cy="17.5" r="0.5" fill="currentColor"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="11" x2="12" y2="17"/><circle cx="12" cy="7.5" r="0.5" fill="currentColor"/></svg>',
    "list": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="20" y2="12"/><line x1="8" y1="18" x2="20" y2="18"/><circle cx="4" cy="6" r="1" fill="currentColor"/><circle cx="4" cy="12" r="1" fill="currentColor"/><circle cx="4" cy="18" r="1" fill="currentColor"/></svg>',
    "database": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>',
    "server": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="7" rx="1.5"/><rect x="3" y="14" width="18" height="7" rx="1.5"/><line x1="7" y1="6.5" x2="7.01" y2="6.5"/><line x1="7" y1="17.5" x2="7.01" y2="17.5"/></svg>',
    "rocket": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.7.7-1.8 0-2.5s-1.8-.7-2.5 0z"/><path d="M12 15l-3-3a14 14 0 0 1 7-7c3 0 5 2 5 5a14 14 0 0 1-7 7z"/><path d="M9 12L4.5 16.5"/><circle cx="14.5" cy="9.5" r="1.5"/></svg>',
    "bug": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="6" width="8" height="14" rx="4"/><path d="M9 6a3 3 0 0 1 6 0"/><line x1="8" y1="10" x2="4" y2="8"/><line x1="16" y1="10" x2="20" y2="8"/><line x1="8" y1="14" x2="4" y2="14"/><line x1="16" y1="14" x2="20" y2="14"/><line x1="8" y1="18" x2="5" y2="20"/><line x1="16" y1="18" x2="19" y2="20"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.5" y2="16.5"/></svg>',
    "puzzle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3a2 2 0 0 1 4 0c0 1.5 1 2 2 2a2 2 0 0 1 0 4c-1 0-2 .5-2 2s1 2 2 2a2 2 0 0 1 0 4c-1 0-2 .5-2 2a2 2 0 0 1-4 0c0-1.5-1-2-2-2a2 2 0 0 1 0-4c1 0 2-.5 2-2s-1-2-2-2a2 2 0 0 1 0-4c1 0 2-.5 2-2z"/></svg>',
    "vq-logo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5 L9 19 L12 11 L15 19 L21 5"/><circle cx="12" cy="5" r="1.5" fill="currentColor"/></svg>',
}


def icon(name: str) -> str:
    """Return inline SVG for a named icon, or empty string if not found."""
    return ICONS.get(name, "")


def page_wrapper(page_num: int, total: int, title: str, subtitle: str,
                 body_html: str, content_path_prefix: str = "") -> str:
    """Build a complete self-contained HTML file for one carousel page.

    Args:
        page_num: 1-based page number.
        total: total number of pages (20).
        title: page title (e.g. "1. WHAT IS SHELL SCRIPTING?").
        subtitle: descriptive subtitle.
        body_html: the recreated content HTML (rows, sidebar, callouts, etc.).
        content_path_prefix: prefix for asset paths (not used in self-contained files).

    Returns:
        Complete HTML string.
    """
    # Watermark positions
    wm_spans = "".join([
        f'<span style="top:{y}%;left:{x}%;">VERIQTA</span>'
        for y in [5, 25, 50, 75] for x in [-5, 30, 65]
    ][:6])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Shell Scripting for DevOps</title>
<style>
{NOTEBOOK_CSS}
</style>
</head>
<body>

<div class="page-wrapper">
  <div class="holes" aria-hidden="true"></div>
  <div class="spiral" aria-hidden="true"></div>
  <div class="page">
    <div class="page-top-edge" aria-hidden="true"></div>
    <div class="page-bottom-edge" aria-hidden="true"></div>
    <div class="watermark" aria-hidden="true">{wm_spans}</div>
    <div class="content">

      <!-- Brand bar -->
      <div class="brand-bar">
        <div class="brand-logo">
          {icon("vq-logo")}
          <span>VERIQTA</span>
        </div>
        <div class="brand-badge">Page {page_num} of {total}</div>
      </div>

      <!-- Title -->
      <h1 class="page-title">{title}</h1>
      <div class="page-subtitle">{subtitle}</div>

      <!-- Body -->
      {body_html}

      <!-- Social footer -->
      <div class="social-footer">
        <div class="social">{icon("play")}<span>YouTube</span></div>
        <div class="social">{icon("git")}<span>GitHub</span></div>
        <div class="social">{icon("linkedin")}<span>LinkedIn</span></div>
        <div class="social">{icon("x")}<span>X</span></div>
        <div class="social">{icon("instagram")}<span>Instagram</span></div>
        <div class="social">{icon("telegram")}<span>Telegram</span></div>
      </div>

    </div>
  </div>
</div>

</body>
</html>"""


if __name__ == "__main__":
    # Test: generate a placeholder page
    html = page_wrapper(
        1, 20,
        "SHELL SCRIPTING FOR DEVOPS",
        "HANDBOOK FOR COMPLETE BEGINNERS",
        '<div class="body single"><div class="rows"><div class="row"><div class="icon bg-green ic-green">' + icon("terminal") + '</div><div class="text"><h3>Test Section</h3><p>This is a test.</p></div></div></div></div>',
    )
    with open("/tmp/test-template.html", "w") as f:
        f.write(html)
    print("Wrote /tmp/test-template.html")
