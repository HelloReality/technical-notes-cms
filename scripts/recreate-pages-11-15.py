#!/usr/bin/env python3
"""
Recreate carousel pages 11-15 (file page-11.webp .. page-15.webp) as
self-contained notebook-style HTML files.

Each output HTML uses the shared template (NOTEBOOK_CSS + ICONS + page_wrapper)
from `build_shell_scripting_template.py`, plus an extra inline `<style>` block
that adds section-card / takeaway-bar styles to match the original carousel
layout (numbered section cards in a 2-column grid with green header bars and
code blocks, plus a key-takeaway bar at the bottom).
"""

import os
import sys

# Make sure we can import the shared template
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_shell_scripting_template import (
    NOTEBOOK_CSS, ICONS, icon, page_wrapper,
)


# ============================================================
# EXTRA CSS — section cards / takeaway bar / extra icons
# ============================================================

EXTRA_CSS = r"""
  /* Section-card grid (2-column) */
  .section-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:14px;
    margin-bottom:16px;
  }
  .section-grid .full{grid-column:1 / -1;}

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
  .sec-head .ico{width:16px;height:16px;flex-shrink:0;}
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
    background:var(--gold-soft);color:var(--orange);
    padding:3px 9px;border-radius:999px;
    font-size:9.5px;font-weight:800;letter-spacing:.5px;
    text-transform:uppercase;
  }
  .side-pill.green{background:var(--green-light);color:var(--green);}
  .side-pill.blue{background:var(--blue-soft);color:var(--blue);}
  .side-pill.red{background:var(--red-soft);color:var(--red);}

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
    padding-left:18px;
    font-size:11px;line-height:1.5;color:var(--ink-2);
    margin-bottom:3px;
  }
  .check-list li::before{
    content:"";
    position:absolute;left:0;top:5px;
    width:11px;height:11px;
    background:var(--green);
    -webkit-mask:url("data:image/svg+xml;utf8,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='currentColor'%20stroke-width='3'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M20%206%20L9%2017%20L4%2012'/%3E%3C/svg%3E") center/contain no-repeat;
    mask:url("data:image/svg+xml;utf8,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='currentColor'%20stroke-width='3'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M20%206%20L9%2017%20L4%2012'/%3E%3C/svg%3E") center/contain no-repeat;
  }

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
  .takeaway-bar .item{
    padding:10px 14px;
    display:flex;align-items:center;gap:8px;
    border-right:1px solid var(--green-soft);
    font-size:11px;line-height:1.35;color:var(--ink-2);
  }
  .takeaway-bar .item:last-child{border-right:none;}
  .takeaway-bar .item .ico{
    flex-shrink:0;width:30px;height:30px;
    background:var(--green-light);border-radius:8px;
    display:flex;align-items:center;justify-content:center;
    color:var(--green);
  }
  .takeaway-bar .item .ico svg{width:18px;height:18px;}
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
    width:30px;height:30px;flex-shrink:0;
    background:var(--green);color:#fff;
    border-radius:8px;
    display:flex;align-items:center;justify-content:center;
  }
  .pillar .ico svg{width:18px;height:18px;}

  /* Page body title (section heading inside body) */
  .body-section-h{
    font-size:13px;font-weight:800;color:var(--green);
    text-transform:uppercase;letter-spacing:.5px;
    margin:14px 0 8px;
    padding-bottom:4px;
    border-bottom:2px solid var(--green);
  }
"""


# ============================================================
# EXTRA ICONS — custom SVGs we need
# ============================================================

EXTRA_ICONS = {
    "function": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.5h9l4 4v15h-13z"/><path d="M15 2.5v4h4"/><text x="8" y="17" font-family="monospace" font-size="6" fill="currentColor" stroke="none">()</text></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-3 2c1 3 3 5 6 6l2-3 5 2v4c0 1-1 2-2 2A16 16 0 0 1 3 6c0-1 1-2 2-2z"/></svg>',
    "speech-user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 4h5v5h-3v2l-3-2"/></svg>',
    "padlock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
    "refresh": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v5h-5"/></svg>',
    "recycle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17H4l3-5"/><path d="M14 17H7l3-5"/><path d="M17 17l-3-5 4-1"/><path d="M14 7l3 0 2 4"/><path d="M7 7l4-2 3 2"/><path d="M12 4l-2 3 2 2 2-2z"/></svg>',
    "shield-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z"/><path d="M8 12 L11 15 L16 9" stroke-width="2.5"/></svg>',
    "code-brackets": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="8 6 3 12 8 18"/><polyline points="16 6 21 12 16 18"/></svg>',
    "doc-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.5h9l4 4v15h-13z"/><path d="M15 2.5v4h4"/><path d="M9 14l2 2 4-4" stroke-width="2.5"/></svg>',
    "folder-plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 6.5a2 2 0 0 1 2-2h5l2 2.5h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z"/><line x1="12" y1="11" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg>',
    "copy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M4 16V6a2 2 0 0 1 2-2h10"/></svg>',
    "move": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 9l-3 3 3 3"/><path d="M2 12h14"/><path d="M14 6l3-3 3 3"/><path d="M17 3v14"/><path d="M9 17l3 3 3-3"/><path d="M12 2v14"/></svg>',
    "gauge": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18a9 9 0 1 1 18 0"/><path d="M12 18l5-7"/><circle cx="12" cy="18" r="1.5" fill="currentColor"/></svg>',
    "trash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/></svg>',
    "upload-cloud": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19a4.5 4.5 0 0 0 0-9 6 6 0 0 0-11.5 1.5A4 4 0 0 0 6 19z"/><path d="M12 13v6"/><path d="M9 16l3-3 3 3"/></svg>',
    "scissors": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>',
    "sort-arrows": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="4" x2="8" y2="20"/><polyline points="4 8 8 4 12 8"/><polyline points="4 16 8 20 12 16"/><line x1="14" y1="6" x2="20" y2="6"/><line x1="14" y1="12" x2="20" y2="12"/><line x1="14" y1="18" x2="20" y2="18"/></svg>',
    "uniq": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="14" height="16" rx="2"/><path d="M7 4v16"/><path d="M14 9l2 2 4-4"/></svg>',
    "counter": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="18" height="12" rx="2"/><text x="5.5" y="15" font-family="monospace" font-size="7" fill="currentColor" stroke="none">123</text></svg>',
    "funnel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h18l-7 8v8l-4-2v-6z"/></svg>',
    "edit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4l6 6L9 21H3v-6z"/><line x1="13" y1="5" x2="19" y2="11"/></svg>',
    "pipes": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="21"/><line x1="18" y1="3" x2="18" y2="21"/><circle cx="12" cy="12" r="3"/></svg>',
    "pie-doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.5h9l4 4v15h-13z"/><path d="M15 2.5v4h4"/><circle cx="11" cy="14" r="3"/><path d="M11 14v-3"/><path d="M11 14l2.5 1.5"/></svg>',
    "doc-search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.5h9l4 4v6"/><path d="M15 2.5v4h4"/><circle cx="11" cy="14" r="3.5"/><line x1="13.5" y1="16.5" x2="17" y2="20"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
    "keyboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><line x1="6" y1="10" x2="6" y2="10"/><line x1="10" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="14" y2="10"/><line x1="18" y1="10" x2="18" y2="10"/><line x1="6" y1="14" x2="18" y2="14"/></svg>',
    "monitor": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
    "warn-triangle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 L22 20 H2 Z"/><line x1="12" y1="9" x2="12" y2="14"/><circle cx="12" cy="17.5" r="0.5" fill="currentColor"/></svg>',
    "log-file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.5h9l4 4v15h-13z"/><path d="M15 2.5v4h4"/><line x1="9" y1="12" x2="16" y2="12"/><line x1="9" y1="16" x2="16" y2="16"/><line x1="9" y1="8" x2="13" y2="8"/></svg>',
    "success-log": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.5h9l4 4v15h-13z"/><path d="M15 2.5v4h4"/><path d="M9 14l2 2 4-4" stroke-width="2.5"/></svg>',
    "error-log": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2.5h9l4 4v15h-13z"/><path d="M15 2.5v4h4"/><line x1="9" y1="12" x2="16" y2="18"/><line x1="16" y1="12" x2="9" y2="18"/></svg>',
    "filter-process": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h18l-7 8v6l-4 2v-8z"/></svg>',
    "ribbon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 4h6v6a3 3 0 0 1-6 0z"/><path d="M9 4H4v3l5 3"/><path d="M15 4h5v3l-5 3"/><path d="M12 16v3"/><path d="M9 22l3-3 3 3"/></svg>',
    "skull": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a8 8 0 0 0-5 14v3h10v-3a8 8 0 0 0-5-14z"/><circle cx="9" cy="11" r="1.5"/><circle cx="15" cy="11" r="1.5"/><path d="M10 18v2"/><path d="M14 18v2"/></svg>',
    "clipboard-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 4V2h6v2"/><path d="M8 12l3 3 5-5" stroke-width="2.5"/></svg>',
    "circle-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M7 12l3 3 7-7" stroke-width="2.5"/></svg>',
    "process-tree": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="4" rx="1"/><rect x="3" y="14" width="6" height="4" rx="1"/><rect x="15" y="14" width="6" height="4" rx="1"/><line x1="12" y1="6" x2="6" y2="14"/><line x1="12" y1="6" x2="18" y2="14"/></svg>',
    "server-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="7" rx="1.5"/><rect x="3" y="14" width="18" height="7" rx="1.5"/><line x1="7" y1="6.5" x2="7.01" y2="6.5"/><path d="M14 17l2 2 4-4" stroke-width="2.5"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="20" x2="21" y2="20"/><rect x="5" y="12" width="3" height="8"/><rect x="11" y="6" width="3" height="14"/><rect x="17" y="14" width="3" height="6"/></svg>',
    "gear-cube": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l9 5v10l-9 5-9-5V7z"/><circle cx="12" cy="12" r="3"/></svg>',
    "list-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6l2 2 3-3"/><path d="M3 14l2 2 3-3"/><line x1="11" y1="6" x2="21" y2="6"/><line x1="11" y1="14" x2="21" y2="14"/><line x1="11" y1="18" x2="21" y2="18"/></svg>',
}


def get_icon(name: str) -> str:
    """Look up an icon from EXTRA_ICONS first, then template ICONS."""
    return EXTRA_ICONS.get(name) or ICONS.get(name, "")


# ============================================================
# HTML HELPERS
# ============================================================

def mini_term(code: str, title: str = "bash") -> str:
    """Build a small terminal window with the given code.

    `code` is rendered verbatim inside <pre> so HTML entities like
    `<` and `>` must already be escaped. We do simple span wrapping
    for prompt lines and comments.
    """
    # Escape HTML
    esc = (code.replace("&", "&amp;")
               .replace("<", "&lt;")
               .replace(">", "&gt;"))
    # Highlight comments (lines starting with #)
    lines = esc.split("\n")
    out_lines = []
    for ln in lines:
        stripped = ln.lstrip()
        if stripped.startswith("#"):
            out_lines.append(f'<span class="comment">{ln}</span>')
        elif stripped.startswith("$ "):
            inner = ln[2:]
            out_lines.append(f'<span class="prompt">$</span> <span class="cmd">{inner}</span>')
        elif stripped.startswith("→ "):
            inner = ln[2:]
            out_lines.append(f'<span class="arrow">→</span> <span class="out">{inner}</span>')
        else:
            out_lines.append(ln)
    body = "\n".join(out_lines)
    return f'''<div class="mini-term"><div class="bar"><i class="r"></i><i class="y"></i><i class="g"></i><span class="t">{title}</span></div><pre>{body}</pre></div>'''


def sec_card(num: int, title: str, icon_name: str, body_html: str, full: bool = False) -> str:
    """Build one numbered section card."""
    cls = "sec-card" + (" full" if full else "")
    return f'''<div class="{cls}">
  <div class="sec-head">
    <span class="num">{num}</span>
    <span class="title">{title}</span>
    <span class="ico">{get_icon(icon_name)}</span>
  </div>
  <div class="sec-body">{body_html}</div>
</div>'''


def takeaway_bar(items: list, four_cols: bool = False) -> str:
    """Build the bottom key-takeaway bar.

    `items` is a list of (icon_name, label, text) tuples.
    The first item is highlighted as the KEY TAKEAWAY.
    """
    cls = "takeaway-bar" + (" four" if four_cols else "")
    parts = [f'<div class="{cls}">']
    for i, (ic, lbl, txt) in enumerate(items):
        first_cls = " first" if i == 0 else ""
        parts.append(f'''<div class="item{first_cls}">
  <span class="ico">{get_icon(ic)}</span>
  <div><span class="lbl">{lbl}</span><span class="txt">{txt}</span></div>
</div>''')
    parts.append("</div>")
    return "".join(parts)


def pillars_row(items: list) -> str:
    """Build a 3-column pillars row. items = [(icon, label), ...]."""
    parts = ['<div class="pillars">']
    for ic, lbl in items:
        parts.append(f'''<div class="pillar">
  <span class="ico">{get_icon(ic)}</span>
  <span>{lbl}</span>
</div>''')
    parts.append("</div>")
    return "".join(parts)


def check_list(items: list) -> str:
    lis = "".join(f"<li>{it}</li>" for it in items)
    return f'<ul class="check-list">{lis}</ul>'


def tag_row(tags: list) -> str:
    spans = "".join(f'<span class="tag">{t}</span>' for t in tags)
    return f'<div class="tag-row">{spans}</div>'


def workflow(steps: list) -> str:
    """Build a horizontal workflow chain.
    steps = [(icon_name, label), ...]"""
    parts = ['<div class="workflow">']
    for i, (ic, lbl) in enumerate(steps):
        parts.append(f'<span class="step">{get_icon(ic)}<span>{lbl}</span></span>')
        if i < len(steps) - 1:
            parts.append('<span class="arr">→</span>')
    parts.append("</div>")
    return "".join(parts)


def side_pill(text: str, color: str = "gold") -> str:
    return f'<span class="side-pill {color}">{text}</span>'


def out_line(text: str) -> str:
    return f'<div class="out-line">{text}</div>'


def body_with_style(body_html: str) -> str:
    """Wrap body HTML with extra inline CSS via a <style> tag."""
    return f"<style>{EXTRA_CSS}</style>\n{body_html}"


# ============================================================
# PAGE BUILDERS
# ============================================================

def build_page_11() -> str:
    """PAGE 10 — 10. FUNCTIONS AND REUSABLE SCRIPTS"""
    cards = []

    # Card 1
    cards.append(sec_card(1, "CREATING FUNCTIONS", "function",
        f'<p>Define a function using a name and <code class="inline">()</code> block.</p>'
        + mini_term('greet() {\n  echo "Hello, DevOps Engineer!"\n}')
    ))

    # Card 2
    cards.append(sec_card(2, "CALLING FUNCTIONS", "phone",
        f'<p>Call the function by its name.</p>'
        + mini_term('greet')
        + out_line("→ Output: Hello, DevOps Engineer!")
    ))

    # Card 3
    cards.append(sec_card(3, "FUNCTION ARGUMENTS", "speech-user",
        f'<p>Pass values to functions.</p>'
        + mini_term('greet_user() {\n  echo "Hello, $1!"\n}\ngreet_user "Ann"')
        + out_line("→ Output: Hello, Ann!")
    ))

    # Card 4
    cards.append(sec_card(4, "LOCAL VARIABLES", "padlock",
        f'<p>Keep variables private to the function.</p>'
        + mini_term('calculate() {\n  local num=10\n  echo "Inside function: $num"\n}\ncalculate\necho "Outside: $num"')
        + out_line("Inside function: 10  Outside:")
        + side_pill("LOCAL MEANS PRIVATE", "green")
    ))

    # Card 5
    cards.append(sec_card(5, "RETURN STATUS", "refresh",
        f'<p>Functions return an exit status.</p>'
        + mini_term('check_disk() {\n  if [ $1 -gt 80 ]; then\n    return 1\n  else\n    return 0\n  fi\n}\ncheck_disk 90\necho "Status: $?"')
        + out_line("→ Output: Status: 1")
        + side_pill("0 = SUCCESS  •  1 = FAILURE", "blue")
    ))

    # Card 6 — full width
    cards.append(sec_card(6, "BREAK LARGE SCRIPTS INTO FUNCTIONS", "list-check",
        f'<p>Make scripts smaller, cleaner, and easier to read.</p>'
        + tag_row(["check_system()", "backup_files()", "deploy_app()", "send_alert()", "cleanup()", "print_summary()"])
        + workflow([("file", "MAIN SCRIPT"), ("gear", "CALL FUNCTIONS"), ("list", "DONE"), ("circle-check", "SUCCESS")]),
        full=True
    ))

    # Card 7
    cards.append(sec_card(7, "REUSABLE AUTOMATION PATTERNS", "recycle",
        check_list([
            "Health checks",
            "Log rotations",
            "Backups",
            "User management",
            "Deployments",
            "System cleanups",
        ])
    ))

    # Card 8
    cards.append(sec_card(8, "KEEP SCRIPTS MAINTAINABLE", "shield-check",
        check_list([
            "Use meaningful function names.",
            "Keep functions small and focused.",
            "Add comments to explain purpose.",
            "Test each function before using it.",
            "Reuse functions across scripts.",
        ])
        + side_pill("CLEAN CODE SAVES TIME AND HEADACHE", "green")
    ))

    body = (
        '<div class="section-grid">'
        + "".join(cards)
        + '</div>'
        + takeaway_bar([
            ("lightbulb", "KEY TAKEAWAY", "Functions make your scripts powerful, reusable, and easy to maintain."),
            ("gear", "BUILD ONCE, USE MANY TIMES", "Reusable building blocks."),
            ("code-brackets", "WRITE SMARTER, AUTOMATE BETTER", "Smart, scalable scripts."),
        ])
    )
    return page_wrapper(
        page_num=10, total=20,
        title="10. FUNCTIONS AND REUSABLE SCRIPTS",
        subtitle="WRITE ONCE. USE MANY TIMES. STAY ORGANIZED.",
        body_html=body_with_style(body),
    )


def build_page_12() -> str:
    """PAGE 11 — 11. WORKING WITH FILES AND DIRECTORIES"""
    cards = []

    cards.append(sec_card(1, "CHECKING WHETHER FILES EXIST", "doc-check",
        '<p>Use <code class="inline">-f</code> for files, <code class="inline">-d</code> for directories.</p>'
        + mini_term('if [ -f file.txt ]; then\n  echo "File exists"\nfi\nif [ -d mydir ]; then\n  echo "Directory exists"\nfi')
    ))

    cards.append(sec_card(2, "CREATING DIRECTORIES SAFELY", "folder-plus",
        '<p>Create only if it does not exist.</p>'
        + mini_term('mkdir -p /home/user/data/logs')
        + '<p class="note"><code class="inline">-p</code> creates parent directories if needed.</p>'
    ))

    cards.append(sec_card(3, "COPYING AND MOVING FILES", "copy",
        '<p>Copy files or directories.</p>'
        + mini_term('cp file.txt /backup/\ncp -r mydir /backup/')
        + '<p>Move or rename files.</p>'
        + mini_term('mv old.txt new.txt\nmv file.txt /archive/')
    ))

    cards.append(sec_card(4, "SEARCHING FOR FILES", "search",
        '<p>Find files by name.</p>'
        + mini_term('find /home/user -name "*.log"')
        + '<p>Search by type.</p>'
        + mini_term('find /var/log -type f -name "*.log"')
    ))

    cards.append(sec_card(5, "FILE PERMISSIONS", "padlock",
        '<p>View permissions.</p>'
        + mini_term('ls -l file.txt')
        + '<p>Change permissions.</p>'
        + mini_term('chmod 644 file.txt\nchmod +x script.sh')
    ))

    cards.append(sec_card(6, "DISK USAGE CHECKS", "gauge",
        '<p>Check disk usage.</p>'
        + mini_term('df -h')
        + '<p>Check folder size.</p>'
        + mini_term('du -sh /home/user/data')
    ))

    cards.append(sec_card(7, "CLEANING TEMPORARY FILES", "trash",
        '<p>Remove files older than 7 days.</p>'
        + mini_term('find /tmp -type f -mtime +7 -delete')
        + '<p>Remove all files in a directory.</p>'
        + mini_term('rm -rf /tmp/myapp/*')
    ))

    cards.append(sec_card(8, "BUILDING A SIMPLE BACKUP SCRIPT", "upload-cloud",
        '<p>Example: Backup a folder.</p>'
        + mini_term('#!/bin/bash\nSOURCE="/home/user/data"\nDEST="/backup"\nDATE=$(date +%F)\ntar -czf "$DEST/backup-$DATE.tar.gz" "$SOURCE"\necho "Backup completed: backup-$DATE.tar.gz"'),
        full=True
    ))

    body = (
        '<div class="section-grid">'
        + "".join(cards)
        + '</div>'
        + takeaway_bar([
            ("lightbulb", "KEY TAKEAWAY", "Good file management keeps your systems clean, safe, and reliable."),
            ("shield-check", "PROTECT YOUR DATA", "Guard your files."),
            ("clock", "AUTOMATE DAILY TASKS", "Save time."),
            ("folder", "STAY ORGANIZED", "Tidy systems run smoother."),
        ], four_cols=True)
    )
    return page_wrapper(
        page_num=11, total=20,
        title="11. WORKING WITH FILES AND DIRECTORIES",
        subtitle="—— ORGANIZE. PROTECT. AUTOMATE. ——",
        body_html=body_with_style(body),
    )


def build_page_13() -> str:
    """PAGE 12 — 12. TEXT PROCESSING FOR DEVOPS"""
    # Left column: 8 command cards (in 2-col grid)
    left_cards = []

    left_cards.append(sec_card(1, "grep — SEARCH TEXT PATTERNS", "search",
        '<p>Search for a pattern in files or output.</p>'
        + mini_term('grep "ERROR" app.log')
    ))
    left_cards.append(sec_card(2, "cut — EXTRACT COLUMNS", "scissors",
        '<p>Extract parts of each line.</p>'
        + mini_term("cut -d',' -f1 users.csv")
    ))
    left_cards.append(sec_card(3, "sort — SORT LINES", "sort-arrows",
        '<p>Sort lines alphabetically or numerically.</p>'
        + mini_term('sort names.txt')
    ))
    left_cards.append(sec_card(4, "uniq — REMOVE DUPLICATES", "uniq",
        '<p>Remove or count duplicate lines.</p>'
        + mini_term('sort names.txt | uniq -c')
    ))
    left_cards.append(sec_card(5, "wc — COUNT LINES, WORDS, BYTES", "counter",
        '<p>Count lines, words, and characters.</p>'
        + mini_term('wc -l file.txt')
    ))
    left_cards.append(sec_card(6, "awk — PATTERN SCANNING", "funnel",
        '<p>Extract and manipulate data.</p>'
        + mini_term("awk '{print $1, $3}' data.txt")
    ))
    left_cards.append(sec_card(7, "sed — STREAM EDITOR", "edit",
        '<p>Find and replace text.</p>'
        + mini_term("sed 's/old/new/g' file.txt")
    ))
    left_cards.append(sec_card(8, "pipes (|) — CONNECT COMMANDS", "pipes",
        '<p>Send output of one command to another.</p>'
        + mini_term('cat app.log | grep ERROR | wc -l')
    ))

    # Right column: cards 9, 10, 11
    right_cards = []

    right_cards.append(sec_card(9, "EXTRACTING USEFUL INFO FROM COMMAND OUTPUT", "pie-doc",
        '<p>Turn raw output into useful data.</p>'
        + '<p><b>List top 5 largest files</b></p>'
        + mini_term('du -h | sort -h | tail -n 5')
        + '<p><b>Count unique IP addresses</b></p>'
        + mini_term("cut -d' ' -f1 access.log | sort | uniq -c | sort -nr")
        + '<p><b>Show running processes summary</b></p>'
        + mini_term("ps aux | awk '{print $1}' | sort | uniq -c | sort -nr | head")
    ))

    right_cards.append(sec_card(10, "SEARCHING APPLICATION LOGS", "doc-search",
        '<p>Find errors, warnings, and important events fast.</p>'
        + '<p><b>Find all ERROR lines</b></p>'
        + mini_term('grep "ERROR" /var/log/app.log')
        + '<p><b>Find errors with line numbers</b></p>'
        + mini_term('grep -n "ERROR" /var/log/app.log')
        + '<p><b>Count warnings</b></p>'
        + mini_term('grep -c "WARNING" /var/log/app.log')
    ))

    # Build common combinations table
    combos = [
        ('grep "ERROR" app.log | wc -l', 'Count errors in log'),
        ('cat file.txt | sort | uniq', 'Unique sorted lines'),
        ('ps aux | grep nginx', 'Find nginx processes'),
        ("cat data.txt | awk \'{print $2}\' | sort | uniq -c", 'Count occurrences of column 2'),
        ('grep -i "failed" *.log | sort | uniq -c', 'Case-insensitive search in all logs'),
    ]
    rows = ""
    for cmd, desc in combos:
        rows += f'<tr><td><code class="inline">{cmd}</code></td><td>{desc}</td></tr>'
    table_html = f'<table class="tbl"><tr><th>Command Combination</th><th>Purpose</th></tr>{rows}</table>'

    right_cards.append(sec_card(11, "COMMON COMBINATIONS", "pipes", table_html))

    # Build layout: 2-column grid (left 8 cards in 2x4 grid + right 3 cards as sidebar)
    body = (
        '<div class="section-grid">'
        + "".join(left_cards)
        + '</div>'
        + '<div class="body-section-h">Advanced Usage</div>'
        + '<div class="section-grid">'
        + "".join(right_cards)
        + '</div>'
        # Bottom: 12. Best Practices
        + '<div class="body-section-h">12. Best Practices</div>'
        + pillars_row([
            ("target", "USE THE RIGHT TOOL FOR THE JOB"),
            ("funnel", "FILTER EARLY, FILTER OFTEN"),
            ("circle-check", "COMBINE COMMANDS WITH PIPES"),
            ("shield-check", "ALWAYS VERIFY YOUR OUTPUT"),
            ("clock", "AUTOMATE LOG ANALYSIS"),
        ]) if False else ""  # placeholder, replaced below
    )

    # Actually 5 best practices - use a 5-column grid
    best_practices_5 = (
        '<div class="body-section-h">12. Best Practices</div>'
        + f'''<div class="pillars" style="grid-template-columns:repeat(5,1fr);gap:8px;">
        <div class="pillar"><span class="ico">{get_icon("target")}</span><span>USE THE RIGHT TOOL FOR THE JOB</span></div>
        <div class="pillar"><span class="ico">{get_icon("funnel")}</span><span>FILTER EARLY, FILTER OFTEN</span></div>
        <div class="pillar"><span class="ico">{get_icon("circle-check")}</span><span>COMBINE WITH PIPES</span></div>
        <div class="pillar"><span class="ico">{get_icon("shield-check")}</span><span>VERIFY YOUR OUTPUT</span></div>
        <div class="pillar"><span class="ico">{get_icon("clock")}</span><span>AUTOMATE LOG ANALYSIS</span></div>
        </div>'''
    )

    body = (
        '<div class="section-grid">'
        + "".join(left_cards)
        + '</div>'
        + '<div class="body-section-h">Advanced Usage</div>'
        + '<div class="section-grid">'
        + "".join(right_cards)
        + '</div>'
        + best_practices_5
    )

    return page_wrapper(
        page_num=12, total=20,
        title="12. TEXT PROCESSING FOR DEVOPS",
        subtitle="—— EXTRACT. FILTER. ANALYZE. AUTOMATE. ——",
        body_html=body_with_style(body),
    )


def build_page_14() -> str:
    """PAGE 13 — 13. REDIRECTION, PIPES, AND LOGS"""
    cards = []

    cards.append(sec_card(1, "STANDARD INPUT (STDIN)", "keyboard",
        '<p>Input from keyboard or file.</p>'
        + mini_term('command < file.txt\nsort < names.txt')
    ))
    cards.append(sec_card(2, "STANDARD OUTPUT (STDOUT)", "monitor",
        '<p>Normal command output.</p>'
        + mini_term('ls -l\necho "Hello"')
    ))
    cards.append(sec_card(3, "STANDARD ERROR (STDERR)", "warn-triangle",
        '<p>Error messages and warnings.</p>'
        + mini_term('ls no_file\ncat no_file.txt')
    ))
    cards.append(sec_card(4, "OUTPUT REDIRECTION", "arrow-right",
        '<p>Overwrite output to a file.</p>'
        + mini_term('command > file.log')
        + side_pill("OVERWRITE FILE", "green")
    ))
    cards.append(sec_card(5, "APPEND REDIRECTION", "arrow-right",
        '<p>Append output to a file.</p>'
        + mini_term('command >> file.log')
        + side_pill("APPEND TO FILE", "green")
    ))
    cards.append(sec_card(6, "ERROR REDIRECTION", "warn-triangle",
        '<p>Redirect errors to a file.</p>'
        + mini_term('command 2> error.log')
        + side_pill("ERRORS ONLY", "red")
    ))
    cards.append(sec_card(7, "COMBINE STDOUT AND STDERR", "arrow-right",
        '<p>Send both output and errors to same file.</p>'
        + mini_term('command > output.log 2>&1')
        + side_pill("OUTPUT + ERRORS TOGETHER", "blue")
    ))
    cards.append(sec_card(8, "PIPES (|)", "filter-process",
        '<p>Send output of one command as input to another.</p>'
        + mini_term('ps aux | grep nginx | wc -l')
        + side_pill("FILTER AND PROCESS DATA", "green")
    ))

    # Full-width section 9
    cards.append(sec_card(9, "SEND SCRIPT OUTPUT TO LOG FILES", "log-file",
        '<p>Log everything for monitoring and audits.</p>'
        + mini_term('#!/bin/bash\necho "Starting script..." > script.log\nls -l /var/log >> script.log\ndf -h >> script.log\necho "Script completed." >> script.log'),
        full=True
    ))

    # Section 10 - capturing errors separately, also full width
    cards.append(sec_card(10, "CAPTURING ERRORS SEPARATELY", "shield-check",
        '<p>Keep success and errors in different files.</p>'
        + mini_term('#!/bin/bash\ncommand > success.log 2> error.log\necho "Done" >> success.log')
        + '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
        + side_pill("SUCCESS .LOG", "green")
        + side_pill("ERROR .LOG", "red")
        + '</div>',
        full=True
    ))

    # Section 11 - common examples table + best practices sidebar
    examples = [
        ('ls -l > files.txt', 'Save output to file (overwrite)'),
        ('ls -l >> files.txt', 'Append output to file'),
        ('command 2> error.log', 'Save errors to error.log'),
        ('command > all.log 2>&1', 'Save output and errors to all.log'),
        ('command | grep "pattern"', 'Filter output using grep'),
        ('cat access.log | grep 404 | wc -l', 'Count 404 errors in logs'),
    ]
    rows = ""
    for cmd, desc in examples:
        rows += f'<tr><td><code class="inline">{cmd}</code></td><td>→ {desc}</td></tr>'
    table_html = f'<table class="tbl"><tr><th>Command</th><th>Description</th></tr>{rows}</table>'

    bp = (
        '<div class="card">'
        f'<div class="head">{get_icon("ribbon")} BEST PRACTICES</div>'
        '<div class="body-pad">'
        + check_list([
            "Log important outputs.",
            "Separate errors from normal output.",
            "Use append (<code class=\"inline\">&gt;&gt;</code>) for long-running logs.",
            "Use pipes to analyze data.",
            "Always check your logs.",
            "Keep logs organized and rotate them.",
        ])
        + '</div></div>'
    )

    # Build section 11 + best practices in 2-column body grid
    sec11 = (
        '<div class="body-section-h">11. Common Examples</div>'
        + f'<div class="body" style="margin-bottom:14px;">'
        + f'<div class="rows"><div class="row" style="border-left-color:var(--green);background:#fff;padding:8px;">{table_html}</div></div>'
        + f'<div class="sidebar">{bp}</div>'
        + '</div>'
    )

    body = (
        '<div class="section-grid" style="grid-template-columns:repeat(3,1fr);">'
        + "".join(cards[:6])
        + '</div>'
        + '<div class="section-grid" style="grid-template-columns:repeat(2,1fr);">'
        + "".join(cards[6:8])
        + '</div>'
        + '<div class="section-grid">'
        + cards[8]
        + cards[9]
        + '</div>'
        + sec11
    )

    return page_wrapper(
        page_num=13, total=20,
        title="13. REDIRECTION, PIPES, AND LOGS",
        subtitle="— CONTROL OUTPUT. CAPTURE LOGS. DEBUG SMARTER. —",
        body_html=body_with_style(body),
    )


def build_page_15() -> str:
    """PAGE 14 — 14. PROCESSES AND SERVICES"""
    cards = []

    cards.append(sec_card(1, "ps — VIEW PROCESSES", "monitor",
        '<p>Show running processes.</p>'
        + mini_term('ps aux\nps -ef')
        + '<p class="note">Useful output columns: <b>PID</b>, <b>USER</b>, <b>%CPU</b>, <b>%MEM</b>, <b>COMMAND</b></p>'
    ))
    cards.append(sec_card(2, "pgrep — FIND PROCESSES", "search",
        '<p>Find process IDs by name.</p>'
        + mini_term('pgrep nginx\npgrep -f myapp')
        + '<p class="note">Used for scripting and automation.</p>'
    ))
    cards.append(sec_card(3, "kill — STOP PROCESSES", "skull",
        '<p>Stop processes using PID.</p>'
        + mini_term('kill 1234\nkill -9 1234')
        + '<p class="note"><b>kill</b> = graceful stop (SIGTERM)<br><b>kill -9</b> = force stop (SIGKILL)</p>'
        + f'<div class="callout warn" style="padding:6px 10px;"><span class="ico">{get_icon("warning")}</span><span>Use <code class="inline">kill -9</code> only when needed.</span></div>'
    ))
    cards.append(sec_card(4, "systemctl — MANAGE SERVICES", "gear",
        '<p>Control system services (Linux).</p>'
        + mini_term('systemctl start nginx\nsystemctl stop nginx\nsystemctl restart nginx\nsystemctl enable nginx')
        + '<p class="note">Works with systemd services.</p>'
    ))
    cards.append(sec_card(5, "CHECK IF PROCESS IS RUNNING", "clipboard-check",
        '<p>Check if a process is running.</p>'
        + mini_term('pgrep nginx >/dev/null\nif [ $? -eq 0 ]; then\n    echo "Running"\nelse\n    echo "Not running"\nfi')
        + '<p class="note">Exit code 0 = running</p>'
    ))
    cards.append(sec_card(6, "CHECK SERVICE STATUS", "circle-check",
        '<p>Check status of a service.</p>'
        + mini_term('systemctl status nginx')
        + '<p class="note">Common states: <b>active (running)</b>, <b>inactive (dead)</b>, <b>failed</b></p>'
    ))
    cards.append(sec_card(7, "RESTART FAILED SERVICES", "refresh",
        '<p>Restart a service.</p>'
        + mini_term('systemctl restart nginx')
        + '<p class="note"><b>Auto-restart on boot:</b></p>'
        + mini_term('systemctl enable nginx')
        + '<p class="note"><b>Check again:</b></p>'
        + mini_term('systemctl status nginx')
    ))
    cards.append(sec_card(8, "PROCESS INFORMATION", "process-tree",
        '<p>Get more details about a process.</p>'
        + mini_term('ps -p 1234 -o pid,user,cmd,%mem,%cpu')
        + '<p class="note"><b>Show parent process:</b></p>'
        + mini_term('ps -o pid,ppid,cmd -p 1234')
    ))

    # Section 9 — full width health check script
    cards.append(sec_card(9, "BASIC SERVICE HEALTH CHECK SCRIPT", "shield-check",
        '<p>Example: Check and restart service.</p>'
        + mini_term('#!/bin/bash\nSERVICE=nginx\npgrep $SERVICE >/dev/null\nif [ $? -eq 0 ]; then\n    echo "$SERVICE is running"\nelse\n    echo "$SERVICE is down. Restarting..."\n    systemctl restart $SERVICE\nfi'),
        full=True
    ))

    # Section 10 — common commands quick reference table + best practices sidebar
    rows_data = [
        ('ps aux', 'List all processes'),
        ('pgrep <name>', 'Find process ID'),
        ('kill <PID>', 'Stop process gracefully'),
        ('kill -9 <PID>', 'Force stop process'),
        ('systemctl status <svc>', 'Check service status'),
        ('systemctl restart <svc>', 'Restart service'),
        ('systemctl enable <svc>', 'Auto-start on boot'),
        ('journalctl -u <svc>', 'View service logs'),
    ]
    rows = ""
    for cmd, desc in rows_data:
        rows += f'<tr><td><code class="inline">{cmd}</code></td><td>→ {desc}</td></tr>'
    table_html = f'<table class="tbl"><tr><th>Command</th><th>Description</th></tr>{rows}</table>'

    bp_card = (
        '<div class="card">'
        f'<div class="head">{get_icon("shield-check")} BEST PRACTICES</div>'
        '<div class="body-pad">'
        + check_list([
            "Always check before you kill.",
            "Use meaningful process names.",
            "Monitor important services.",
            "Automate health checks.",
            "Log issues for faster troubleshooting.",
            "Restart only when necessary.",
            "Keep scripts simple and readable.",
        ])
        + '</div></div>'
    )

    sec10 = (
        '<div class="body-section-h">10. Common Commands Quick Reference</div>'
        + f'<div class="body" style="margin-bottom:14px;">'
        + f'<div class="rows"><div class="row" style="border-left-color:var(--green);background:#fff;padding:8px;">{table_html}</div></div>'
        + f'<div class="sidebar">{bp_card}</div>'
        + '</div>'
    )

    # Key takeaway footer
    takeaway = takeaway_bar([
        ("lightbulb", "KEY TAKEAWAY", "Know your processes. Control your services. Keep your systems reliable."),
        ("chart", "MONITOR PROCESSES", "Stay aware."),
        ("gear", "MANAGE SERVICES", "Stay in control."),
        ("shield-check", "KEEP SYSTEMS HEALTHY", "Stay reliable."),
    ], four_cols=True)

    body = (
        '<div class="section-grid" style="grid-template-columns:repeat(2,1fr);">'
        + "".join(cards[:8])
        + '</div>'
        + '<div class="section-grid">'
        + cards[8]
        + '</div>'
        + sec10
        + takeaway
    )

    return page_wrapper(
        page_num=14, total=20,
        title="14. PROCESSES AND SERVICES",
        subtitle="MONITOR. CONTROL. KEEP EVERYTHING RUNNING.",
        body_html=body_with_style(body),
    )


# ============================================================
# MAIN
# ============================================================

OUTPUT_DIR = "/home/z/my-project/downloads/instagram-DcaW1UljsVk"


def main():
    builders = [
        (11, build_page_11),
        (12, build_page_12),
        (13, build_page_13),
        (14, build_page_14),
        (15, build_page_15),
    ]
    for n, builder in builders:
        html = builder()
        out = os.path.join(OUTPUT_DIR, f"recreated-page-{n}.html")
        with open(out, "w") as f:
            f.write(html)
        print(f"Wrote {out} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
