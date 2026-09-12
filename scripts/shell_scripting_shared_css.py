#!/usr/bin/env python3
"""
Unified CSS for all Shell Scripting handbook pages.

This file consolidates ALL CSS from the 4 batch build scripts into a single
shared stylesheet. Each build script imports SHARED_CSS from this file and
includes it in the page's <style> block. This eliminates CSS conflicts when
pages from different batches are combined into a single HTML file.

Usage in build scripts:
  import sys; sys.path.insert(0, "scripts")
  from shell_scripting_shared_css import SHARED_CSS
  # Then include SHARED_CSS in the page's <style> block
"""

SHARED_CSS = """
/* ============================================================
   UNIFIED CSS — shared by all Shell Scripting handbook pages
   ============================================================ */

/* --- Root variables --- */
:root{
  --paper:#f5f1e8;--paper-2:#efe9dd;--grid-line:#bcc8d6;
  --navy:#15264d;--navy-2:#1e3160;--ink:#1c1c1c;--ink-2:#3a3f47;
  --green:#1B5E3F;--green-2:#164a32;--green-soft:#cdf3da;--green-light:#e8f5ee;
  --blue:#2563eb;--blue-soft:#cfe0ff;
  --purple:#7c3aed;--purple-soft:#e2d4ff;
  --red:#dc2626;--red-soft:#ffd4d4;
  --gold:#d4a017;--gold-soft:#fce9b6;--amber:#f9a825;
  --orange:#e65100;--teal:#0d7377;
  --term-bg:#0d1117;--term-fg:#e6edf3;--term-green:#7ee787;
  --card-bg:#fff;--card-border:rgba(0,0,0,.05);
}

/* --- Content positioning (between 3D edges) --- */
.page-wrapper > div:first-of-type > .content{
  position:absolute !important;top:11px !important;left:0 !important;
  right:0 !important;bottom:11px !important;z-index:2;overflow:auto;
}
.page-wrapper > div:first-of-type > div:first-of-type > svg{
  position:absolute !important;top:0;left:0;width:100% !important;
  height:100% !important;z-index:0;pointer-events:none;
}

/* --- Brand bar --- */
.brand-bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;}
.crumb{font-size:11px;font-weight:700;letter-spacing:1.5px;color:var(--green);text-transform:uppercase;display:flex;align-items:center;gap:6px;}
.badge{background:var(--green);color:#fff;padding:5px 14px;border-radius:999px;font-size:10.5px;font-weight:800;letter-spacing:1px;}

/* --- Page title --- */
.page-title{display:flex;align-items:center;gap:14px;margin-bottom:6px;}
.page-title h1{font-size:30px;font-weight:800;color:var(--green);text-transform:uppercase;letter-spacing:-.4px;line-height:1.1;margin:0;}
.page-title .num{color:var(--green-2);}
.page-title .ico{flex-shrink:0;display:inline-flex;width:42px;height:42px;}
.page-subtitle{font-size:12.5px;font-weight:700;color:var(--ink-2);text-transform:uppercase;letter-spacing:1.4px;text-align:center;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid var(--green);position:relative;}
.page-subtitle::after{content:"";position:absolute;left:50%;bottom:-5px;width:9px;height:9px;background:var(--green);border-radius:50%;transform:translateX(-50%);}

/* --- Body layout --- */
.body{display:grid;grid-template-columns:1.85fr 1fr;gap:16px;margin-bottom:14px;}
.body.single{grid-template-columns:1fr;}
.split-2col{display:grid;grid-template-columns:1fr 1.1fr;gap:10px;margin-bottom:8px;}
.right-stack{display:flex;flex-direction:column;gap:7px;}
.left-stack{display:flex;flex-direction:column;gap:11px;}

/* --- Grid layouts --- */
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;}
.grid-5{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;}
.single{grid-template-columns:1fr;}

/* --- Cards --- */
.card{background:#fff;border-radius:9px;overflow:auto;box-shadow:0 2px 8px rgba(0,0,0,.06);border:1px solid var(--card-border);}
.card .head{background:var(--green);color:#fff;padding:7px 12px;font-size:10.5px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;display:flex;align-items:center;gap:8px;}
.card .head svg{width:16px;height:16px;flex-shrink:0;}
.card .head .num{flex-shrink:0;width:22px;height:22px;border-radius:50%;background:rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;}
.card .body-pad{padding:9px 12px;}
.card .pad{padding:10px 12px;font-size:12px;line-height:1.45;color:var(--ink);}

/* --- Sidebar cards --- */
.sidebar-card{background:#fff;border-radius:8px;overflow:auto;box-shadow:0 2px 8px rgba(0,0,0,.06);border:1px solid var(--card-border);}
.sidebar-card .head{background:var(--navy);color:#fff;padding:7px 12px;font-size:10.5px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;display:flex;align-items:center;gap:8px;}
.sidebar-card .head svg{width:16px;height:16px;flex-shrink:0;}
.sidebar-card .body-pad{padding:9px 12px;}

/* --- Terminal / code blocks --- */
.terminal{background:var(--term-bg);border-radius:7px;overflow:auto;box-shadow:0 3px 12px rgba(0,0,0,.18);margin-top:4px;}
.terminal .term-bar{background:#1c2230;padding:5px 10px;display:flex;align-items:center;gap:6px;border-bottom:1px solid #2c3340;}
.terminal .term-dot{width:8px;height:8px;border-radius:50%;}
.terminal .dot-red{background:#ff5f56;}
.terminal .dot-amber{background:#ffbd2e;}
.terminal .dot-green{background:#27c93f;}
.terminal .term-title{margin-left:auto;color:#8b949e;font-size:9.5px;font-family:"JetBrains Mono",monospace;}
.terminal .term-body{padding:8px 12px;font-family:"JetBrains Mono","Fira Code",monospace;font-size:10.5px;line-height:1.5;color:var(--term-fg);}
.terminal .term-body .cmd{color:#79c0ff;}
.terminal .term-body .str{color:#f2cc60;}
.terminal .term-body .kw{color:#ff7b72;font-weight:600;}
.terminal .term-body .prompt{color:var(--term-green);}
.terminal .term-body .comment{color:#8b949e;font-style:italic;}
.terminal .term-body .out{color:var(--term-fg);}

/* --- Code light blocks (beige code boxes) --- */
.code-light{background:#f4f1e7;border:1px solid #d8d3c0;border-radius:6px;padding:6px 9px;font-family:"JetBrains Mono",monospace;font-size:10.5px;color:var(--ink);line-height:1.4;margin:4px 0;}

/* --- Inline code --- */
.inline{font-family:"JetBrains Mono","Fira Code",monospace;font-size:10px;background:#efe9dd;padding:1px 4px;border-radius:3px;color:var(--green);font-weight:600;}

/* --- Tables --- */
.tbl{width:100%;border-collapse:collapse;font-size:10.5px;margin-top:4px;}
.tbl th{background:var(--green);color:#fff;padding:6px 9px;text-align:left;font-weight:700;font-size:10px;letter-spacing:.3px;text-transform:uppercase;}
.tbl td{padding:5px 9px;border-bottom:1px solid #e0d8c8;color:var(--ink-2);vertical-align:top;}
.tbl td code{font-family:"JetBrains Mono",monospace;font-size:10px;background:#e8e4d4;padding:1px 4px;border-radius:3px;color:var(--green);display:inline-block;vertical-align:top;}
.tbl tr:last-child td{border-bottom:none;}

/* --- Callouts --- */
.callout{display:flex;gap:9px;align-items:flex-start;border-radius:8px;padding:8px 12px;font-size:11px;line-height:1.45;margin:4px 0;}
.callout.warn{background:#fff4e0;border-left:3px solid var(--orange);color:var(--ink-2);}
.callout.tip{background:var(--green-light);border-left:3px solid var(--green);color:var(--ink-2);}
.callout.danger{background:var(--red-soft);border-left:3px solid var(--red);color:var(--ink-2);}
.callout.note{background:var(--green-soft);border-left:3px solid var(--green);color:var(--ink-2);}
.callout .ico{flex-shrink:0;width:18px;height:18px;margin-top:1px;}

/* --- Example rows --- */
.example-row{padding:5px 0;border-bottom:1px dashed rgba(22,38,77,.10);}
.example-row:last-child{border-bottom:none;}
.example-row .label{font-size:9.5px;color:var(--ink-2);font-weight:700;text-transform:uppercase;letter-spacing:.3px;margin-bottom:3px;}
.example-row .desc{font-size:10px;color:var(--ink-2);line-height:1.4;margin-top:3px;}

/* --- Numbered steps --- */
.steps{display:flex;flex-direction:column;gap:5px;}
.step{display:flex;gap:9px;align-items:flex-start;font-size:11px;color:var(--ink-2);line-height:1.4;}
.step .n{flex-shrink:0;width:20px;height:20px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;font-family:monospace;}

/* --- Compare grids --- */
.compare{display:grid;grid-template-columns:1fr 1fr;gap:7px;}
.compare .col{border-radius:7px;padding:7px 9px;font-size:10px;line-height:1.4;background:#fff;border:1px solid #e0d8c8;}
.compare .col h4{font-size:10px;font-weight:700;text-transform:uppercase;margin-bottom:5px;}
.compare .col.left{background:#fce9b6;}
.compare .col.left h4{color:var(--orange);}
.compare .col.right{background:var(--green-light);}
.compare .col.right h4{color:var(--green);}

/* --- Bottom bar (key takeaway / best practices) --- */
.bottom-bar{background:var(--navy);color:#fff;border-radius:8px;padding:8px 12px;margin-top:4px;}
.bottom-bar .head{font-size:11px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;display:flex;align-items:center;gap:8px;margin-bottom:6px;}
.bottom-bar .head svg{width:18px;height:18px;}
.bp-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;}
.bp-item{font-size:10px;color:#e6edf3;line-height:1.4;padding:3px 0;display:flex;align-items:flex-start;gap:6px;}

/* --- Key takeaway --- */
.key-takeaway{display:flex;align-items:center;gap:10px;background:var(--green);color:#fff;border-radius:8px;padding:10px 14px;margin-top:6px;}
.key-takeaway .kt-ico{flex-shrink:0;width:30px;height:30px;display:inline-flex;align-items:center;justify-content:center;}
.key-takeaway .kt-text{flex:1;font-size:12px;line-height:1.5;}

/* --- Rows (icon + heading + text) --- */
.rows{display:flex;flex-direction:column;gap:8px;}
.row{display:flex;gap:11px;align-items:flex-start;background:rgba(255,255,255,.55);border-radius:9px;padding:8px 11px;border-left:3px solid var(--green);}
.row .ico{flex-shrink:0;width:42px;height:42px;border-radius:9px;display:flex;align-items:center;justify-content:center;background:var(--green-light);}
.row .ico svg{width:24px;height:24px;}
.row .text{flex:1;min-width:0;}
.row .text h3{font-size:13px;font-weight:800;color:var(--green);text-transform:uppercase;letter-spacing:.3px;margin-bottom:3px;}
.row .text p{font-size:12px;color:var(--ink-2);line-height:1.45;}

/* --- Workflow strip --- */
.workflow{display:flex;align-items:center;justify-content:space-between;gap:8px;background:#fff;border:2px solid var(--green-light);border-radius:10px;padding:10px 14px;margin-top:8px;}
.wf-step{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:10px;font-weight:800;color:var(--green);text-transform:uppercase;}
.wf-arrow{color:var(--green);font-weight:800;font-size:15px;}
.wf-check{width:30px;height:30px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;}

/* --- Head color variants --- */
.head-green .head{background:var(--green);}
.head-blue .head{background:var(--blue);}
.head-purple .head{background:var(--purple);}
.head-red .head{background:var(--red);}
.head-gold .head{background:var(--gold);}
.head-teal .head{background:var(--teal);}
.head-navy .head{background:var(--navy);}
.head-orange .head{background:var(--orange);}

/* --- Misc --- */
.mono{font-family:"JetBrains Mono","Fira Code","Consolas",monospace;font-size:10px;color:var(--navy);background:#eef0f5;padding:1px 4px;border-radius:3px;}
.muted{color:var(--ink-2);}
.small{font-size:10.5px;color:var(--ink-2);}
.lead{font-size:11.5px;color:var(--ink-2);margin:4px 0 8px 0;line-height:1.45;}
.pill{display:inline-flex;align-items:center;gap:5px;padding:3px 8px;border-radius:999px;font-size:10px;font-weight:800;background:var(--green-soft);color:var(--green);}
.star{flex-shrink:0;width:25px;height:25px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;}
"""
