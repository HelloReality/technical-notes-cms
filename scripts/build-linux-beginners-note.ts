// ============================================================================
// build-linux-beginners-note.ts
// ----------------------------------------------------------------------------
// Generate a single self-contained HTML file recreating the
// "Linux for Complete Beginners" Instagram carousel (20 pages) as a notebook
// in the same aesthetic as VERIQTA_Linux_Security_Handbook_Page2.html
// (cream paper, spiral binding, graph grid, navy badges, card sections,
// terminal blocks, navy-header tables, footer with practice tips).
//
// All VERIQTA branding is removed; no original images are embedded.
//
// Run:  bun run scripts/build-linux-beginners-note.ts
// Output: public/uploads/linux-for-beginners.html
// ============================================================================

import { writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// ---------------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------------
type Tint = "blue" | "green" | "purple" | "red" | "gold" | "neutral";

interface Cmd {
  cmd: string;
  desc?: string;
  out?: string;
}

interface Concept {
  num?: string;
  title: string;
  body?: string;
  bullets?: string[];
  cmds?: Cmd[];
  tint?: Tint;
  icon?: string; // inline SVG string
}

interface TableRow {
  cells: string[];
}

interface Callout {
  type: "tip" | "warning" | "note" | "success" | "goal";
  title?: string;
  text: string;
  icon?: string;
}

interface Step {
  n: string;
  title: string;
  cmd?: string;
  out?: string;
}

// ---------------------------------------------------------------------------
// HTML escape
// ---------------------------------------------------------------------------
function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// ---------------------------------------------------------------------------
// CSS — based on VERIQTA reference template, extended for new content types
// ---------------------------------------------------------------------------
const CSS = `
/* ============================================================
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
  --linux-green:#1B4D3E;   /* dark green from cover */
  --linux-green-2:#0f6b3f;
  --blue:#2563eb;
  --blue-soft:#cfe0ff;
  --green:#16a34a;
  --green-soft:#cdf3da;
  --purple:#7c3aed;
  --purple-soft:#e2d4ff;
  --red:#dc2626;
  --red-soft:#ffd4d4;
  --gold:#d4a017;
  --gold-soft:#fce9b6;
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
  display:flex;flex-direction:column;align-items:center;gap:34px;
  padding:28px 12px;
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
  padding:42px 50px 28px 78px;  /* extra left padding for spiral binding */
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

/* SVG punch holes */
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

/* Page top/bottom edges (3D block effect) */
.page-top-edge,.page-bottom-edge{
  position:absolute;z-index:8;left:0;right:0;height:11px;pointer-events:none;
  background:
    repeating-linear-gradient(to bottom, transparent 0px, transparent 2px, rgba(140,120,80,0.12) 2px, rgba(140,120,80,0.12) 2.4px),
    linear-gradient(to bottom, #fbf8ef 0%, #f7f3e8 55%, var(--paper) 100%);
}
.page-top-edge{top:0;border-bottom:1px solid rgba(100,80,40,0.22);box-shadow:0 1px 2px rgba(0,0,0,0.10);}
.page-bottom-edge{
  bottom:0;
  background:
    repeating-linear-gradient(to bottom, transparent 0px, transparent 2px, rgba(140,120,80,0.12) 2px, rgba(140,120,80,0.12) 2.4px),
    linear-gradient(to top, #fbf8ef 0%, #f7f3e8 55%, var(--paper) 100%);
  border-top:1px solid rgba(100,80,40,0.22);
  box-shadow:0 -1px 2px rgba(0,0,0,0.10);
}

.content{position:relative;z-index:2;}

/* ============================================================
   TOP STRIP — badges
   ============================================================ */
.top-strip{
  display:flex;justify-content:flex-end;align-items:center;
  margin-bottom:6px;
}
.badges{display:flex;gap:10px;flex-wrap:wrap;}
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
.badge.green{background:var(--linux-green);}
.badge.alt{background:var(--navy-2);}

/* ============================================================
   TITLE BLOCK
   ============================================================ */
.title-block{margin:18px 0 6px 0;}
.title{
  font-size:42px;
  line-height:1.04;
  font-weight:800;
  color:var(--linux-green);
  letter-spacing:-0.6px;
  text-transform:uppercase;
}
.title.navy{color:var(--navy);}
.title .small{display:block;font-size:22px;color:var(--ink);font-weight:700;letter-spacing:-0.2px;margin-top:4px;}
.subtitle{
  margin-top:8px;
  font-size:13px;
  font-weight:700;
  letter-spacing:1.3px;
  color:var(--ink-2);
  text-transform:uppercase;
}
.divider{
  display:flex;align-items:center;
  margin:12px 0 18px 0;
}
.divider .line{flex:1;height:2px;background:var(--linux-green);}
.divider .dot{width:9px;height:9px;border-radius:50%;background:var(--linux-green);margin:0 10px;}

/* ============================================================
   COVER PAGE
   ============================================================ */
.cover{
  display:flex;flex-direction:column;align-items:center;
  padding:12px 4px 0 4px;
  text-align:center;
}
.cover .super{
  display:inline-block;
  background:var(--linux-green);
  color:#fff;
  font-size:11px;letter-spacing:3px;font-weight:700;
  padding:6px 14px;border-radius:999px;
  margin-bottom:14px;
}
.cover .title-big{
  font-size:148px;line-height:0.92;
  font-weight:900;
  color:var(--linux-green);
  letter-spacing:-4px;
  text-transform:uppercase;
  text-shadow:0 6px 0 rgba(0,0,0,0.06);
}
.cover .title-sub-wrap{
  display:flex;align-items:center;justify-content:center;gap:14px;
  margin-top:8px;
}
.cover .title-sub-wrap .hline{
  height:3px;width:90px;background:var(--linux-green);border-radius:2px;
}
.cover .title-sub{
  font-size:42px;font-weight:900;color:var(--ink);
  letter-spacing:-0.4px;
  text-transform:uppercase;line-height:1;
}
.cover .title-sub .green{color:var(--linux-green);}
.cover .sub-box{
  margin-top:22px;
  display:inline-flex;align-items:center;gap:16px;
  background:#fff;
  border:2px solid var(--linux-green);
  border-radius:14px;
  padding:14px 22px;
  box-shadow:0 4px 12px rgba(27,77,62,0.18);
  max-width:760px;
}
.cover .sub-box .tux{flex-shrink:0;width:56px;}
.cover .sub-box .sub-text{
  text-align:left;
  font-size:13px;letter-spacing:1.6px;color:var(--linux-green);
  font-weight:700;line-height:1.45;text-transform:uppercase;
}
.cover .icon-row{
  display:flex;justify-content:center;gap:28px;
  margin-top:28px;flex-wrap:wrap;
}
.cover .icon-pill{
  display:flex;flex-direction:column;align-items:center;gap:8px;
  width:110px;
}
.cover .icon-pill .icn{
  width:70px;height:70px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  background:#fff;
  border:2.5px solid var(--linux-green);
  box-shadow:0 3px 8px rgba(0,0,0,0.06);
}
.cover .icon-pill .icn svg{width:40px;height:40px;}
.cover .icon-pill .lbl{
  font-size:11px;font-weight:700;color:var(--ink);
  text-transform:uppercase;letter-spacing:0.6px;text-align:center;
}
.cover .features{
  margin-top:28px;
  width:100%;max-width:880px;
  background:#fff;
  border:1.5px solid rgba(27,77,62,0.22);
  border-radius:16px;
  padding:22px 28px;
  box-shadow:0 4px 12px rgba(0,0,0,0.08);
  position:relative;
  display:grid;grid-template-columns:1fr 200px;gap:18px;
  align-items:center;
}
.cover .features h4{
  font-size:14px;font-weight:800;color:var(--linux-green);
  text-transform:uppercase;letter-spacing:1.4px;margin-bottom:14px;
}
.cover .features ul{list-style:none;display:flex;flex-direction:column;gap:9px;}
.cover .features li{
  display:flex;align-items:center;gap:11px;
  font-size:14px;color:var(--ink);font-weight:600;
}
.cover .features li .check{
  width:22px;height:22px;border-radius:50%;
  background:var(--linux-green);
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.cover .features li .check svg{width:14px;height:14px;}
.cover .features .laptop-illu{
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:8px;
}
.cover .features .laptop-illu svg{width:160px;height:auto;}
.cover .features .laptop-illu .caption{
  font-size:10px;letter-spacing:1.4px;color:var(--linux-green);font-weight:700;text-transform:uppercase;
}
.cover .footer-tag{
  margin-top:26px;
  display:inline-flex;align-items:center;gap:14px;
  background:var(--linux-green);
  color:#fff;
  border-radius:999px;
  padding:11px 26px;
  font-size:13px;font-weight:700;letter-spacing:2px;
  box-shadow:0 4px 10px rgba(27,77,62,0.30);
}
.cover .footer-tag svg{width:22px;height:22px;}

/* ============================================================
   BODY — column layouts
   ============================================================ */
.body{display:grid;gap:20px;}
.body.cols-2{grid-template-columns:1fr 1fr;}
.body.cols-3{grid-template-columns:1fr 1fr 1fr;}
.body.cols-2-uneven{grid-template-columns:1.6fr 1fr;}
.body.cols-3-uneven{grid-template-columns:1fr 1fr 1.2fr;}

/* ============================================================
   CONCEPT GRID — numbered concept boxes
   ============================================================ */
.concept-grid{
  display:grid;gap:14px;
  grid-template-columns:repeat(2, 1fr);
}
.concept-grid.cols-3{grid-template-columns:repeat(3, 1fr);}
.concept-grid.cols-4{grid-template-columns:repeat(4, 1fr);}
.concept-card{
  background:#fff;
  border:1px solid rgba(21,38,77,0.10);
  border-radius:12px;
  padding:12px 14px;
  box-shadow:0 2px 6px rgba(0,0,0,0.05);
  display:flex;flex-direction:column;gap:6px;
}
.concept-card .ch{
  display:flex;align-items:center;gap:10px;
}
.concept-card .num{
  width:26px;height:26px;border-radius:50%;
  background:var(--linux-green);color:#fff;
  font-size:12px;font-weight:800;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.concept-card .icn-mini{
  width:34px;height:34px;border-radius:9px;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;
}
.concept-card .icn-mini svg{width:22px;height:22px;}
.concept-card h3{
  font-size:12.5px;font-weight:800;letter-spacing:0.5px;
  color:var(--linux-green);text-transform:uppercase;
  line-height:1.2;
  flex:1;
}
.concept-card .body-text{
  font-size:11.5px;color:var(--ink-2);line-height:1.5;
}
.concept-card ul{list-style:none;display:flex;flex-direction:column;gap:3px;}
.concept-card ul li{
  font-size:11.5px;color:var(--ink-2);line-height:1.45;
  padding-left:12px;position:relative;
}
.concept-card ul li::before{
  content:"";position:absolute;left:0;top:7px;
  width:5px;height:5px;border-radius:50%;background:var(--linux-green);
}
.concept-card .sub-label{
  font-size:10.5px;color:var(--ink);font-weight:700;letter-spacing:0.4px;
  margin-top:4px;text-transform:uppercase;
}
.concept-card .mini-term{
  background:var(--term-bg);color:var(--term-fg);
  font-family:"JetBrains Mono","Consolas",monospace;
  font-size:10.5px;line-height:1.4;
  padding:6px 8px;border-radius:5px;
  margin-top:4px;overflow-x:auto;
  white-space:pre;
}
.concept-card .distro-row{
  display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;
}
.concept-card .distro-row .distro{
  display:inline-flex;align-items:center;gap:5px;
  background:#f1efe6;border:1px solid rgba(0,0,0,0.06);
  border-radius:6px;padding:3px 7px;
  font-size:10px;font-weight:700;color:var(--ink);
}
.concept-card .distro-row .distro svg{width:13px;height:13px;}

/* tint classes */
.bg-blue{background:var(--blue-soft)!important;}
.bg-green{background:var(--green-soft)!important;}
.bg-purple{background:var(--purple-soft)!important;}
.bg-red{background:var(--red-soft)!important;}
.bg-gold{background:var(--gold-soft)!important;}
.bg-neutral{background:#eef1f5!important;}

/* ============================================================
   COMMAND CARDS — large, with terminal example
   ============================================================ */
.cmd-grid{display:grid;gap:14px;grid-template-columns:repeat(2, 1fr);}
.cmd-grid.cols-3{grid-template-columns:repeat(3, 1fr);}
.cmd-card{
  background:#fff;
  border:1px solid rgba(21,38,77,0.10);
  border-radius:12px;
  padding:12px 14px;
  box-shadow:0 2px 6px rgba(0,0,0,0.05);
  display:flex;gap:12px;align-items:flex-start;
}
.cmd-card .ic{
  width:42px;height:42px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
  background:#f1efe6;
}
.cmd-card .ic svg{width:26px;height:26px;}
.cmd-card .body-text{flex:1;}
.cmd-card h4{
  font-size:14px;font-weight:800;letter-spacing:0.4px;
  color:var(--linux-green);text-transform:lowercase;
}
.cmd-card .desc{
  font-size:11.5px;color:var(--ink-2);line-height:1.45;margin-top:2px;
}
.cmd-card .term{
  background:var(--term-bg);color:var(--term-fg);
  font-family:"JetBrains Mono","Consolas",monospace;
  font-size:11px;line-height:1.5;
  padding:7px 9px;border-radius:6px;
  margin-top:6px;overflow-x:auto;
  white-space:pre;
}
.cmd-card .term .pmt{color:#7ee787;}
.cmd-card .term .cmt{color:#8b949e;}
.cmd-card .term .err{color:#ff7b72;}
.cmd-card .term .out{color:#79c0ff;}

/* ============================================================
   TERMINAL BLOCKS — dark, multi-line
   ============================================================ */
.term-block{
  background:var(--term-bg);
  color:var(--term-fg);
  border-radius:10px;
  overflow:hidden;
  box-shadow:0 4px 14px rgba(0,0,0,0.18);
  font-family:"JetBrains Mono","Consolas",monospace;
}
.term-block .term-head{
  background:#1c2230;
  padding:6px 12px;
  display:flex;align-items:center;gap:8px;
  border-bottom:1px solid rgba(255,255,255,0.06);
}
.term-block .term-head .dot{width:10px;height:10px;border-radius:50%;}
.term-block .term-head .dot.r{background:#ff5f56;}
.term-block .term-head .dot.y{background:#ffbd2e;}
.term-block .term-head .dot.g{background:#27c93f;}
.term-block .term-head .ttl{
  margin-left:8px;font-size:11px;color:#8b949e;letter-spacing:0.6px;
}
.term-block .term-body{
  padding:10px 14px;font-size:11.5px;line-height:1.55;
  overflow-x:auto;white-space:pre;
}
.term-block .term-body .pmt{color:#7ee787;}
.term-block .term-body .cmt{color:#8b949e;}
.term-block .term-body .err{color:#ff7b72;}
.term-block .term-body .out{color:#79c0ff;}
.term-block .term-body .warn{color:#d29922;}

/* ============================================================
   DATA TABLES — navy header
   ============================================================ */
.data-table{
  width:100%;border-collapse:collapse;
  background:#fff;
  border-radius:12px;overflow:hidden;
  box-shadow:0 3px 10px rgba(0,0,0,0.06);
  font-size:11.5px;
  border:1px solid rgba(21,38,77,0.10);
}
.data-table thead th{
  background:var(--linux-green);
  color:#fff;
  font-weight:700;letter-spacing:0.6px;
  text-transform:uppercase;font-size:10.5px;
  padding:9px 10px;text-align:left;
  border-right:1px solid rgba(255,255,255,0.10);
}
.data-table thead th:last-child{border-right:none;}
.data-table tbody td{
  padding:8px 10px;
  border-bottom:1px solid rgba(21,38,77,0.07);
  border-right:1px solid rgba(21,38,77,0.05);
  color:var(--ink);line-height:1.4;
  vertical-align:top;
}
.data-table tbody td:last-child{border-right:none;}
.data-table tbody tr:nth-child(even) td{background:#f8f5ec;}
.data-table tbody tr:last-child td{border-bottom:none;}
.data-table code,.data-table .mono{
  font-family:"JetBrains Mono","Consolas",monospace;
  font-size:11px;font-weight:600;
  color:var(--linux-green);
  background:#eef5ef;border-radius:3px;padding:1px 5px;
  display:inline-block;vertical-align:top;
}
.data-table .center{text-align:center;}

/* table caption */
.table-caption{
  background:var(--linux-green);color:#fff;
  font-size:11px;font-weight:700;letter-spacing:1.2px;
  text-transform:uppercase;
  padding:8px 14px;
  border-radius:10px 10px 0 0;
}
.table-wrap{
  border-radius:10px;overflow:hidden;
  box-shadow:0 3px 10px rgba(0,0,0,0.06);
  border:1px solid rgba(21,38,77,0.10);
  background:#fff;
}

/* ============================================================
   CALLOUT BOXES
   ============================================================ */
.callout{
  display:flex;gap:12px;align-items:flex-start;
  padding:12px 14px;border-radius:11px;
  border:1px solid rgba(21,38,77,0.10);
  box-shadow:0 2px 6px rgba(0,0,0,0.05);
}
.callout .icn{
  width:34px;height:34px;border-radius:9px;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.callout .icn svg{width:20px;height:20px;}
.callout .ct{flex:1;}
.callout .ct h5{
  font-size:11px;font-weight:800;letter-spacing:1px;
  text-transform:uppercase;margin-bottom:3px;
}
.callout .ct p{font-size:12px;color:var(--ink);line-height:1.5;}
.callout .ct ul{list-style:none;margin-top:4px;display:flex;flex-direction:column;gap:2px;}
.callout .ct ul li{
  font-size:12px;color:var(--ink);line-height:1.5;
  padding-left:14px;position:relative;
}
.callout .ct ul li::before{
  content:"";position:absolute;left:0;top:7px;
  width:5px;height:5px;border-radius:50%;background:currentColor;
}
.callout.tip{background:var(--green-soft);}
.callout.tip .icn{background:rgba(22,163,74,0.25);}
.callout.tip .ct h5{color:#0f6b3f;}
.callout.warning{background:var(--gold-soft);}
.callout.warning .icn{background:rgba(212,160,23,0.30);}
.callout.warning .ct h5{color:#8a6500;}
.callout.note{background:var(--blue-soft);}
.callout.note .icn{background:rgba(37,99,235,0.20);}
.callout.note .ct h5{color:#1e40af;}
.callout.success{background:#d8f5e3;}
.callout.success .icn{background:rgba(16,107,63,0.25);}
.callout.success .ct h5{color:var(--linux-green);}
.callout.goal{background:#e7def8;}
.callout.goal .icn{background:rgba(124,58,237,0.20);}
.callout.goal .ct h5{color:#5b21b6;}

.callout-grid{display:grid;gap:12px;grid-template-columns:repeat(2, 1fr);}
.callout-grid.cols-3{grid-template-columns:repeat(3, 1fr);}

/* ============================================================
   STEPS WORKFLOW — numbered practical
   ============================================================ */
.steps-flow{
  display:flex;flex-direction:column;gap:8px;
}
.step{
  display:grid;grid-template-columns:34px 1fr;gap:12px;align-items:flex-start;
  padding:9px 12px;
  background:#fff;border:1px solid rgba(21,38,77,0.08);
  border-radius:10px;
  box-shadow:0 1px 4px rgba(0,0,0,0.04);
}
.step .n{
  width:28px;height:28px;border-radius:50%;
  background:var(--linux-green);color:#fff;
  font-size:12px;font-weight:800;
  display:flex;align-items:center;justify-content:center;
}
.step .bd{display:flex;flex-direction:column;gap:3px;}
.step .bd .t{font-size:12.5px;font-weight:700;color:var(--linux-green);text-transform:uppercase;letter-spacing:0.4px;}
.step .bd .term{
  background:var(--term-bg);color:var(--term-fg);
  font-family:"JetBrains Mono","Consolas",monospace;
  font-size:10.5px;line-height:1.5;
  padding:6px 9px;border-radius:5px;
  margin-top:3px;overflow-x:auto;white-space:pre;
}
.step .bd .term .pmt{color:#7ee787;}
.step .bd .term .out{color:#79c0ff;}

/* ============================================================
   SECTION HEADER (in body)
   ============================================================ */
.section-h{
  display:flex;align-items:center;gap:10px;
  margin:8px 0 8px 0;
}
.section-h .bar{
  width:4px;height:18px;background:var(--linux-green);border-radius:2px;
}
.section-h h4{
  font-size:14px;font-weight:800;color:var(--linux-green);
  text-transform:uppercase;letter-spacing:0.6px;
}
.section-h .pill{
  margin-left:auto;
  background:#eef5ef;color:var(--linux-green);
  font-size:10px;font-weight:700;letter-spacing:0.6px;
  padding:3px 9px;border-radius:999px;
  text-transform:uppercase;
}

/* two-column file/term rows */
.kv-row{
  display:grid;grid-template-columns:140px 1fr;gap:10px;align-items:baseline;
  padding:6px 0;border-bottom:1px dashed rgba(21,38,77,0.10);
}
.kv-row:last-child{border-bottom:none;}
.kv-row .k{
  font-family:"JetBrains Mono","Consolas",monospace;
  font-size:11.5px;font-weight:700;color:var(--linux-green);
}
.kv-row .v{font-size:11.5px;color:var(--ink-2);line-height:1.45;}

/* ============================================================
   PAGE FOOTER
   ============================================================ */
.page-footer{
  margin-top:20px;
  border-top:2px dashed rgba(21,38,77,0.18);
  padding-top:12px;
  display:flex;justify-content:space-between;align-items:center;
  font-size:11px;color:var(--ink-2);
  gap:16px;flex-wrap:wrap;
}
.page-footer .src{
  background:var(--green-soft);color:var(--linux-green);
  padding:5px 12px;border-radius:999px;font-weight:700;letter-spacing:0.4px;
}
.page-footer .tip{
  background:var(--gold-soft);color:#8a6500;
  padding:5px 12px;border-radius:999px;font-weight:700;letter-spacing:0.3px;
  flex:1;text-align:center;
}
.page-footer .pg{
  background:var(--linux-green);color:#fff;
  padding:5px 12px;border-radius:999px;font-weight:700;letter-spacing:0.6px;
}

/* ============================================================
   PRINT / PDF
   ============================================================ */
@page{size:1080px 1420px;margin:0;}
@media print{
  html,body{background:#fff;padding:0;gap:0;}
  .page-wrapper{margin:0;}
  .page{box-shadow:none;border-radius:0;width:1080px;page-break-after:always;}
}
`;

// ---------------------------------------------------------------------------
// Inline SVG icon library (simple, original illustrations)
// ---------------------------------------------------------------------------
const ICON = {
  tux: `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M32 6c-7 0-12 6-12 14 0 4 1 7 3 9-3 4-7 11-9 18-1 4-2 9 0 11 1 1 2 1 3 0 1 3 3 4 5 4h20c2 0 4-1 5-4 1 1 2 1 3 0 2-2 1-7 0-11-2-7-6-14-9-18 2-2 3-5 3-9 0-8-5-14-12-14z" fill="#1a1a1a"/><path d="M32 8c-4 0-7 4-7 9 0 3 1 5 2 7 1-1 3-1 5-1s4 0 5 1c1-2 2-4 2-7 0-5-3-9-7-9z" fill="#fff"/><circle cx="27" cy="20" r="2.4" fill="#1a1a1a"/><circle cx="37" cy="20" r="2.4" fill="#1a1a1a"/><circle cx="27.6" cy="20" r="0.8" fill="#fff"/><circle cx="37.6" cy="20" r="0.8" fill="#fff"/><path d="M28 25c2 2 6 2 8 0-1 3-3 4-4 4s-3-1-4-4z" fill="#f5a623"/><path d="M22 33c-2 4-5 10-6 16 4-2 8-2 12-2-3-4-5-9-6-14z" fill="#fff" opacity=".92"/><path d="M42 33c2 4 5 10 6 16-4-2-8-2-12-2 3-4 5-9 6-14z" fill="#fff" opacity=".92"/><path d="M26 54c2 1 4 1 6 1s4 0 6-1c-2 2-4 3-6 3s-4-1-6-3z" fill="#f5a623"/><path d="M29 50c1 0 2 1 3 1s2-1 3-1c0 2-1 3-3 3s-3-1-3-3z" fill="#f5a623"/></svg>`,
  terminal: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><rect x="2.5" y="4" width="19" height="16" rx="2.2" fill="#0d1117"/><rect x="2.5" y="4" width="19" height="3" rx="2.2" fill="#1c2230"/><circle cx="5" cy="5.5" r="0.6" fill="#ff5f56"/><circle cx="6.8" cy="5.5" r="0.6" fill="#ffbd2e"/><circle cx="8.6" cy="5.5" r="0.6" fill="#27c93f"/><path d="M6 11 L9 13.5 L6 16" fill="none" stroke="#7ee787" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><line x1="11" y1="16" x2="17" y2="16" stroke="#e6edf3" stroke-width="1.6" stroke-linecap="round"/></svg>`,
  folder: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M3 6.5h5.5l1.7 2H21v10.5a1.5 1.5 0 0 1-1.5 1.5H4.5A1.5 1.5 0 0 1 3 19z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M3 9.5h18" stroke="currentColor" stroke-width="1.5"/></svg>`,
  users: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="9" cy="8" r="3.4" fill="currentColor"/><circle cx="15.5" cy="9" r="2.7" fill="currentColor" opacity=".75"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M13.5 20c0-2.5 1.8-4.5 4-4.5s4 2 4 4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity=".75"/></svg>`,
  gear: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zm-2 3.5a2 2 0 1 1 4 0 2 2 0 0 1-4 0z" fill="currentColor"/><path d="M19.4 12.9a7.5 7.5 0 0 0 .06-1.8l1.5-1.1-1.5-2.6-1.8.6a7.6 7.6 0 0 0-1.55-.9l-.4-1.85h-3l-.4 1.85a7.6 7.6 0 0 0-1.55.9l-1.8-.6L7.04 9.99l1.5 1.1a7.5 7.5 0 0 0 0 1.8l-1.5 1.1 1.5 2.6 1.8-.6a7.6 7.6 0 0 0 1.55.9l.4 1.85h3l.4-1.85a7.6 7.6 0 0 0 1.55-.9l1.8.6 1.5-2.6z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
  cloud: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M7.5 18a4.5 4.5 0 0 1 0-9 5.5 5.5 0 0 1 10.5-1.5A4 4 0 0 1 18 18z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>`,
  target: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="8" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="11" cy="11" r="4.5" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="11" cy="11" r="1.8" fill="currentColor"/><path d="M16 11l6-6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="M19 5l3 0 0 3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>`,
  laptop: `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><rect x="11" y="14" width="42" height="28" rx="2.5" fill="#0d1117"/><rect x="13.5" y="16.5" width="37" height="23" rx="1" fill="#1c2230"/><text x="32" y="32" font-family="monospace" font-size="9" fill="#7ee787" text-anchor="middle">&gt;_</text><path d="M5 44h54l-3 5a3 3 0 0 1-2.6 1.5H10.6A3 3 0 0 1 8 49z" fill="#cfe9dd"/><rect x="26" y="46" width="12" height="1.5" fill="#7c9d92"/></svg>`,
  check: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M5 13l4 4L19 7" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  lightbulb: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9 18h6m-5 2h4M12 3a6 6 0 0 0-4 10.5c.7.7 1.2 1.5 1.4 2.5h5.2c.2-1 .7-1.8 1.4-2.5A6 6 0 0 0 12 3z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"/></svg>`,
  warning: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5l10.5 18.5H1.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><line x1="12" y1="10" x2="12" y2="14.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="17.5" r="1.2" fill="currentColor"/></svg>`,
  book: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M4 4h7v15H4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M13 4h7v15h-7z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><line x1="6" y1="8" x2="9" y2="8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><line x1="6" y1="11" x2="9" y2="11" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><line x1="15" y1="8" x2="18" y2="8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><line x1="15" y1="11" x2="18" y2="11" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>`,
  shield: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M8.5 12l2.5 2.5L16 9.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  lock: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10 V8 a5 5 0 0 1 10 0 V10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="5" y="10" width="14" height="10" rx="2.4" fill="currentColor"/><circle cx="12" cy="14.5" r="1.5" fill="#fff"/><rect x="11.2" y="14.5" width="1.6" height="3" fill="#fff" rx="0.5"/></svg>`,
  magnifier: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><line x1="15.5" y1="15.5" x2="20" y2="20" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>`,
  server: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="4" width="18" height="6" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/><rect x="3" y="14" width="18" height="6" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="6" cy="7" r="0.8" fill="currentColor"/><circle cx="6" cy="17" r="0.8" fill="currentColor"/><line x1="9" y1="7" x2="18" y2="7" stroke="currentColor" stroke-width="1.2"/><line x1="9" y1="17" x2="18" y2="17" stroke="currentColor" stroke-width="1.2"/></svg>`,
  key: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="8" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 12h9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M17 12v3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M20 12v2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>`,
  database: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><ellipse cx="12" cy="6" rx="7" ry="2.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M5 6v6c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5V6" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M5 12v6c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-6" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>`,
  clock: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 7v5l3.5 2" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  star: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.8 6.2 20.9l1.1-6.5L2.6 9.8l6.5-.9z" fill="currentColor"/></svg>`,
  package: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5l8 4.5v9.5l-8 4.5-8-4.5V7z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M4 7l8 4.5 8-4.5M12 11.5v9.5" stroke="currentColor" stroke-width="1.4" fill="none"/></svg>`,
  network: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="5" r="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="5" cy="18" r="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="19" cy="18" r="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 7.5v4m0 0l-5.5 4M12 11.5l5.5 4" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>`,
  play: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M10 8l6 4-6 4z" fill="currentColor"/></svg>`,
  list: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><line x1="8" y1="6" x2="20" y2="6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><line x1="8" y1="12" x2="20" y2="12" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><line x1="8" y1="18" x2="20" y2="18" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><circle cx="4" cy="6" r="1.2" fill="currentColor"/><circle cx="4" cy="12" r="1.2" fill="currentColor"/><circle cx="4" cy="18" r="1.2" fill="currentColor"/></svg>`,
  pencil: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M14.5 4.5l5 5L9 20l-5.5.5L4 15z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M13 6l5 5" stroke="currentColor" stroke-width="1.7"/></svg>`,
  // Distribution logos (simplified)
  ubuntu: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11" fill="#E95420"/><circle cx="12" cy="6.5" r="2.2" fill="#fff"/><circle cx="7" cy="15.5" r="2.2" fill="#fff"/><circle cx="17" cy="15.5" r="2.2" fill="#fff"/><circle cx="12" cy="12" r="3.5" fill="none" stroke="#fff" stroke-width="1.4"/></svg>`,
  rhel: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M5 16l1-9a4 4 0 0 1 4-3.5h4A4 4 0 0 1 18 7l1 9z" fill="#CC0000"/><path d="M8 12h2v4m4-4v4m2-4h-4" stroke="#fff" stroke-width="1.4" fill="none" stroke-linecap="round"/></svg>`,
  debian: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11" fill="#A80030"/><path d="M14 6c-2-1-5 0-6 3-1 2 0 5 2 6 2 1 5 0 6-2" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/><path d="M12 6.5c2 1 3 3 2 5" fill="none" stroke="#fff" stroke-width="1.2"/></svg>`,
  rocky: `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11" fill="#10B981"/><path d="M7 14l5-7 5 7-5 3z" fill="#fff"/><path d="M7 14l5 3 5-3" fill="none" stroke="#0f6b3f" stroke-width="1"/></svg>`,
} as const;

// ---------------------------------------------------------------------------
// Helper: page chrome (badges + title + divider + footer)
// ---------------------------------------------------------------------------
function pageChrome(
  pageNum: number,
  totalPages: number,
  topic: string,
  inner: string,
  footerTip?: string,
): string {
  const pn = String(pageNum).padStart(2, "0");
  const tp = String(totalPages).padStart(2, "0");
  return `
<div class="page-wrapper">
  <div class="holes" aria-hidden="true"></div>
  <div class="spiral" aria-hidden="true"></div>
  <div class="page-bend" aria-hidden="true"></div>
  <div class="page">
    <div class="page-top-edge" aria-hidden="true"></div>
    <div class="page-bottom-edge" aria-hidden="true"></div>
    <div class="content">
      <div class="top-strip">
        <div class="badges">
          <span class="badge green">LINUX FOR BEGINNERS</span>
          <span class="badge alt">${topic}</span>
          <span class="badge">PAGE ${pn} / ${tp}</span>
        </div>
      </div>
      ${inner}
      <div class="page-footer">
        <span class="src">Notebook · Practice Daily</span>
        ${footerTip ? `<span class="tip">${footerTip}</span>` : ""}
        <span class="pg">${pn} / ${tp}</span>
      </div>
    </div>
  </div>
</div>`;
}

function titleHtml(title: string, subtitle?: string): string {
  return `<div class="title-block">
    <h1 class="title">${title}</h1>
    ${subtitle ? `<div class="subtitle">${subtitle}</div>` : ""}
  </div>
  <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>`;
}

function sectionHeader(title: string, pill?: string): string {
  return `<div class="section-h">
    <span class="bar"></span>
    <h4>${title}</h4>
    ${pill ? `<span class="pill">${pill}</span>` : ""}
  </div>`;
}

function iconWrap(svg: string, tint: Tint = "neutral"): string {
  return `<span class="icn-mini bg-${tint}" style="color:var(--linux-green);">${svg}</span>`;
}

function calloutBox(c: Callout): string {
  const icons: Record<Callout["type"], string> = {
    tip: ICON.lightbulb,
    warning: ICON.warning,
    note: ICON.book,
    success: ICON.shield,
    goal: ICON.target,
  };
  const titles: Record<Callout["type"], string> = {
    tip: "TIP",
    warning: "WARNING",
    note: "NOTE",
    success: "SUCCESS",
    goal: "GOAL",
  };
  const title = c.title ?? titles[c.type];
  return `<div class="callout ${c.type}">
    <div class="icn">${c.icon ?? icons[c.type]}</div>
    <div class="ct">
      <h5>${title}</h5>
      ${c.text}
    </div>
  </div>`;
}

function conceptCard(c: Concept): string {
  const tint = c.tint ?? "neutral";
  const numHtml = c.num ? `<span class="num">${c.num}</span>` : "";
  const iconHtml = c.icon ? `<span class="icn-mini bg-${tint}" style="color:var(--linux-green);">${c.icon}</span>` : "";
  let bodyHtml = "";
  if (c.body) bodyHtml += `<div class="body-text">${c.body}</div>`;
  if (c.bullets && c.bullets.length) {
    bodyHtml += `<ul>${c.bullets.map((b) => `<li>${b}</li>`).join("")}</ul>`;
  }
  if (c.cmds && c.cmds.length) {
    for (const cmd of c.cmds) {
      const term = cmd.cmd.replace(/\$/g, '<span class="pmt">$</span>');
      const out = cmd.out ? `\n<span class="out">${esc(cmd.out)}</span>` : "";
      const cmt = cmd.desc ? `\n<span class="cmt"># ${esc(cmd.desc)}</span>` : "";
      bodyHtml += `<div class="mini-term">${term}${cmt}${out}</div>`;
    }
  }
  return `<div class="concept-card">
    <div class="ch">${numHtml}${iconHtml}<h3>${c.title}</h3></div>
    ${bodyHtml}
  </div>`;
}

function cmdCard(opts: {
  cmd: string;
  title?: string;
  desc?: string;
  example?: string;
  output?: string;
  comment?: string;
  icon?: string;
  tint?: Tint;
}): string {
  const tint = opts.tint ?? "neutral";
  const title = opts.title ?? opts.cmd;
  const icon = opts.icon ?? ICON.terminal;
  let term = "";
  if (opts.example) {
    const ex = opts.example
      .split("\n")
      .map((ln) => ln.replace(/^\$/, '<span class="pmt">$</span>'))
      .join("\n");
    const out = opts.output ? `\n<span class="out">${esc(opts.output)}</span>` : "";
    const cmt = opts.comment ? `\n<span class="cmt"># ${esc(opts.comment)}</span>` : "";
    term = `<div class="term">${ex}${cmt}${out}</div>`;
  }
  return `<div class="cmd-card">
    <div class="ic bg-${tint}" style="color:var(--linux-green);">${icon}</div>
    <div class="body-text">
      <h4>${esc(title)}</h4>
      ${opts.desc ? `<div class="desc">${opts.desc}</div>` : ""}
      ${term}
    </div>
  </div>`;
}

function termBlock(title: string, lines: string[]): string {
  // Each line: escape, replace $ with prompt span, # with comment span
  const body = lines
    .map((ln) => {
      // handle prompt
      let out = esc(ln);
      // highlight $ at start as prompt
      out = out.replace(/^(\s*)\$/, '$1<span class="pmt">$</span>');
      // highlight # at start as comment
      out = out.replace(/^(\s*)#/, '$1<span class="cmt">#</span>');
      return out;
    })
    .join("\n");
  return `<div class="term-block">
    <div class="term-head">
      <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
      <span class="ttl">${esc(title)}</span>
    </div>
    <pre class="term-body">${body}</pre>
  </div>`;
}

function dataTable(opts: {
  caption?: string;
  headers: string[];
  rows: string[][];
  monoCols?: number[];
}): string {
  const { caption, headers, rows } = opts;
  const monoCols = new Set(opts.monoCols ?? []);
  const head = headers
    .map((h) => `<th>${esc(h)}</th>`)
    .join("");
  const body = rows
    .map(
      (r) =>
        `<tr>${r
          .map(
            (cell, i) =>
              `<td${monoCols.has(i) ? ' class="mono"' : ""}>${cell}</td>`,
          )
          .join("")}</tr>`,
    )
    .join("");
  const table = `<table class="data-table">
    <thead><tr>${head}</tr></thead>
    <tbody>${body}</tbody>
  </table>`;
  if (!caption) return table;
  return `<div class="table-wrap">
    <div class="table-caption">${esc(caption)}</div>
    ${table}
  </div>`;
}

function stepsFlow(steps: Step[]): string {
  return `<div class="steps-flow">${steps
    .map((s) => {
      const term = s.cmd
        ? `<div class="term">${esc(s.cmd).replace(/^\$/, '<span class="pmt">$</span>')}${s.out ? `\n<span class="out">${esc(s.out)}</span>` : ""}</div>`
        : "";
      return `<div class="step">
        <div class="n">${s.n}</div>
        <div class="bd">
          <div class="t">${esc(s.title)}</div>
          ${term}
        </div>
      </div>`;
    })
    .join("")}</div>`;
}

// ---------------------------------------------------------------------------
// PAGE BUILDERS
// ---------------------------------------------------------------------------
function page1Cover(): string {
  const inner = `
  <div class="cover">
    <span class="super">A PRACTICAL GUIDE</span>
    <h1 class="title-big">LINUX</h1>
    <div class="title-sub-wrap">
      <span class="hline"></span>
      <div class="title-sub">FOR COMPLETE BEGINNERS</div>
      <span class="hline"></span>
    </div>
    <div class="sub-box">
      <div class="tux">${ICON.tux}</div>
      <div class="sub-text">A PRACTICAL GUIDE FROM<br>ZERO TO CONFIDENT LINUX USER</div>
    </div>
    <div class="icon-row">
      <div class="icon-pill">
        <div class="icn" style="border-color:#1565C0;color:#1565C0;">${ICON.terminal}</div>
        <div class="lbl">Command Line</div>
      </div>
      <div class="icon-pill">
        <div class="icn" style="border-color:#2E7D32;color:#2E7D32;">${ICON.folder}</div>
        <div class="lbl">File System</div>
      </div>
      <div class="icon-pill">
        <div class="icn" style="border-color:#1565C0;color:#1565C0;">${ICON.users}</div>
        <div class="lbl">Users &amp; Permissions</div>
      </div>
      <div class="icon-pill">
        <div class="icn" style="border-color:#EF6C00;color:#EF6C00;">${ICON.gear}</div>
        <div class="lbl">Services &amp; Processes</div>
      </div>
      <div class="icon-pill">
        <div class="icn" style="border-color:#1565C0;color:#1565C0;">${ICON.cloud}</div>
        <div class="lbl">Networking</div>
      </div>
    </div>
    <div class="features">
      <div>
        <h4>What You'll Get</h4>
        <ul>
          <li><span class="check">${ICON.check}</span> Step-by-step Learning</li>
          <li><span class="check">${ICON.check}</span> Hands-on Examples</li>
          <li><span class="check">${ICON.check}</span> Real-world Scenarios</li>
          <li><span class="check">${ICON.check}</span> Beginner Friendly</li>
          <li><span class="check">${ICON.check}</span> DevOps Ready</li>
          <li><span class="check">${ICON.check}</span> Build Strong Foundation</li>
        </ul>
      </div>
      <div class="laptop-illu">
        ${ICON.laptop}
        <div class="caption">From Zero to Confident</div>
      </div>
    </div>
    <div class="footer-tag">
      ${ICON.target}
      LEARN TODAY. PRACTICE DAILY. USE LINUX ANYWHERE.
    </div>
  </div>`;
  // Cover page doesn't use the standard chrome — render plain
  return `
<div class="page-wrapper">
  <div class="holes" aria-hidden="true"></div>
  <div class="spiral" aria-hidden="true"></div>
  <div class="page-bend" aria-hidden="true"></div>
  <div class="page">
    <div class="page-top-edge" aria-hidden="true"></div>
    <div class="page-bottom-edge" aria-hidden="true"></div>
    <div class="content">
      <div class="top-strip">
        <div class="badges">
          <span class="badge green">LINUX FOR BEGINNERS</span>
          <span class="badge alt">COVER</span>
          <span class="badge">PAGE 01 / 20</span>
        </div>
      </div>
      ${inner}
      <div class="page-footer">
        <span class="src">Notebook · Practice Daily</span>
        <span class="tip">A 20-page practical guide</span>
        <span class="pg">01 / 20</span>
      </div>
    </div>
  </div>
</div>`;
}

// ---------------------------------------------------------------------------
// PAGE 2 — Linux From Zero
// ---------------------------------------------------------------------------
function page2LinuxFromZero(): string {
  const inner = `
  ${titleHtml("LINUX FROM ZERO", "WHAT LINUX IS · HOW IT WORKS · YOUR FIRST COMMANDS")}
  <div class="body cols-2">
    ${conceptCard({
      num: "1", tint: "blue", icon: ICON.tux,
      title: "What Linux Actually Is",
      bullets: [
        "Open-source operating system.",
        "Most popular OS for servers, cloud, DevOps and engineering work.",
        "Stable, secure, fast and highly customizable.",
      ],
    })}
    ${conceptCard({
      num: "2", tint: "green", icon: ICON.gear,
      title: "Linux Kernel vs Operating System",
      bullets: [
        "<b>Kernel:</b> core part of Linux. Talks to hardware (CPU, memory, storage, devices). Manages system resources.",
        "<b>Operating System:</b> everything around the kernel — system tools, libraries, commands, applications, utilities.",
      ],
    })}
    ${conceptCard({
      num: "3", tint: "purple", icon: ICON.package,
      title: "Linux Distributions (Distros)",
      bullets: [
        "Many distributions use the Linux kernel.",
        "Each distro packages tools and software differently.",
      ],
      body: `<div class="distro-row">
          <span class="distro">${ICON.ubuntu}UBUNTU · Beginner friendly</span>
          <span class="distro">${ICON.rhel}RHEL · Enterprise</span>
          <span class="distro">${ICON.debian}DEBIAN · Stable</span>
          <span class="distro">${ICON.rocky}ROCKY · RHEL-compatible</span>
        </div>`,
    })}
    ${conceptCard({
      num: "4", tint: "gold", icon: ICON.server,
      title: "Server Linux vs Desktop Linux",
      bullets: [
        "<b>Server Linux:</b> runs without UI (GUI). Optimized for performance, security and uptime. Used in data centers, cloud and production.",
        "<b>Desktop Linux:</b> has graphical interface (GUI). Designed for end users. Daily tasks like browsers and office apps.",
      ],
    })}
    ${conceptCard({
      num: "5", tint: "blue", icon: ICON.cloud,
      title: "Why DevOps Engineers Use Linux",
      bullets: [
        "Most servers &amp; cloud run Linux.",
        "Automation, scripting and tooling work best on Linux.",
        "Better security and control.",
        "Essential for DevOps, SRE, Cloud &amp; Platform Engineering.",
      ],
    })}
    ${conceptCard({
      num: "6", tint: "green", icon: ICON.terminal,
      title: "Terminal vs Shell",
      bullets: [
        "<b>Terminal:</b> the application you open to interact with Linux. It is the window.",
        "<b>Shell:</b> the program inside the terminal that interprets and executes your commands. Example: bash, zsh, sh.",
      ],
    })}
  </div>

  ${sectionHeader("7. Your First Linux Commands (Practical)", "Cheatsheet")}
  ${dataTable({
    headers: ["COMMAND", "WHAT IT DOES", "EXAMPLE", "SAMPLE OUTPUT (MAY VARY)"],
    monoCols: [0, 2],
    rows: [
      ["whoami", "Shows the current user", "<code>whoami</code>", "ubuntu"],
      ["hostname", "Shows the system hostname", "<code>hostname</code>", "ip-172-31-20-15"],
      ["uname -a", "Shows system &amp; kernel info", "<code>uname -a</code>", "Linux ip-172-31-20-15 5.15.0-101-generic #112~20.04.1-Ubuntu x86_64 GNU/Linux"],
      ["date", "Shows current date and time", "<code>date</code>", "Sat May 11 10:30:45 UTC 2024"],
      ["uptime", "Shows how long the system has been running", "<code>uptime</code>", "10:30:45 up 2 days, 3:15, 1 user, load average: 0.08, 0.07, 0.05"],
    ],
  })}

  <div class="callout-grid" style="margin-top:14px;">
    ${calloutBox({ type: "tip", title: "PRACTICE TIP", text: "<p>Open your terminal and run each command. This builds your confidence and familiarity.</p>" })}
    ${calloutBox({ type: "goal", title: "GOAL", text: "<p>Understand Linux basics and feel comfortable in the terminal.</p>" })}
  </div>`;
  return pageChrome(2, 20, "LINUX FROM ZERO", inner, "Run every command on a real terminal — muscle memory matters.");
}

// ---------------------------------------------------------------------------
// PAGE 3 — Understanding the Linux Filesystem
// ---------------------------------------------------------------------------
function page3Filesystem(): string {
  const inner = `
  ${titleHtml("UNDERSTANDING THE<br>LINUX FILESYSTEM", "THE LINUX FILESYSTEM IS ORGANIZED IN A TREE-LIKE STRUCTURE STARTING FROM THE ROOT DIRECTORY /")}
  <div class="body cols-2-uneven">
    <div>
      ${sectionHeader("Linux Directory Structure")}
      ${dataTable({
        headers: ["DIRECTORY", "PURPOSE", "EXAMPLE CONTENT"],
        monoCols: [0],
        rows: [
          ["/", "Root of the filesystem. Everything starts here.", "All directories and files"],
          ["/home", "Home directories for regular users.", "/home/user1 /home/user2"],
          ["/etc", "System configuration files.", "passwd, hosts, ssh, nginx"],
          ["/var", "Variable data that changes.", "logs, spool, cache, databases"],
          ["/tmp", "Temporary files. Usually cleared on reboot.", "Temporary files from apps"],
          ["/usr", "User programs and applications.", "bin, sbin, lib, share, local"],
          ["/opt", "Optional add-on software packages.", "Third-party applications"],
          ["/bin", "Essential user binaries (commands).", "ls, cp, mv, cat, bash"],
          ["/sbin", "System binaries for administration.", "fdisk, reboot, ifconfig, mkfs"],
          ["/root", "Home directory for the root (admin) user.", "Root's personal files"],
        ],
      })}
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;">
      ${calloutBox({ type: "note", title: "ABSOLUTE PATH", text: "<p>Starts from the root directory <code>/</code> and shows the full location.</p><p><code>/home/user/docs/file.txt</code></p>" })}
      ${calloutBox({ type: "note", title: "RELATIVE PATH", text: "<p>Starts from your current location.</p><p><code>docs/file.txt</code></p>" })}
      ${calloutBox({ type: "note", title: ". (DOT)", text: "<p>Refers to the current directory.</p><p><code>./script.sh</code></p>" })}
      ${calloutBox({ type: "note", title: ".. (DOT DOT)", text: "<p>Refers to the parent directory.</p><p><code>../</code> (go up one level)</p>" })}
      ${calloutBox({ type: "tip", title: "QUICK TIP", text: "<p>Linux is case-sensitive. <code>/Home</code> and <code>/home</code> are different directories.</p>" })}
    </div>
  </div>

  ${sectionHeader("Practical: Navigate Through a Real Linux Filesystem")}
  <div class="body cols-2">
    ${cmdCard({ cmd: "pwd", title: "pwd", desc: "Show your current location", example: "$ pwd", output: "/home/user", tint: "green", icon: ICON.folder })}
    ${cmdCard({ cmd: "ls", title: "ls -l /", desc: "List the root directory", example: "$ ls -l /", tint: "green", icon: ICON.list })}
    ${cmdCard({ cmd: "cd", title: "cd /home", desc: "Enter the /home directory", example: "$ cd /home", tint: "blue", icon: ICON.folder })}
    ${cmdCard({ cmd: "cd ..", title: "cd ..", desc: "Go up one level", example: "$ cd ..", tint: "blue", icon: ICON.folder })}
    ${cmdCard({ cmd: "cd /etc", title: "cd /etc", desc: "Go to /etc and explore", example: "$ cd /etc", tint: "purple", icon: ICON.gear })}
    ${cmdCard({ cmd: "cd /var/log", title: "cd /var/log", desc: "Explore log files", example: "$ cd /var/log", tint: "purple", icon: ICON.folder })}
    ${cmdCard({ cmd: "cd ~", title: "cd ~", desc: "Go to your home directory", example: "$ cd ~", tint: "gold", icon: ICON.folder })}
    ${cmdCard({ cmd: "cd -", title: "cd -", desc: "Go back to previous directory", example: "$ cd -", tint: "gold", icon: ICON.folder })}
  </div>

  <div class="callout-grid cols-2" style="margin-top:14px;">
    ${calloutBox({ type: "goal", title: "GOAL", text: "<p>Understand where important files live so you can work confidently in Linux.</p>" })}
    ${calloutBox({ type: "success", title: "KEY TAKEAWAY", text: "<p>The filesystem hierarchy is the foundation of Linux. Learn it once, use it every day.</p>" })}
  </div>`;
  return pageChrome(3, 20, "FILESYSTEM", inner, "Navigate with cd, ls, pwd every day.");
}

// ---------------------------------------------------------------------------
// PAGE 4 — Moving Around Linux
// ---------------------------------------------------------------------------
function page4MovingAround(): string {
  const inner = `
  ${titleHtml("MOVING AROUND LINUX", "ESSENTIAL COMMANDS TO NAVIGATE LIKE A PRO")}
  <div class="cmd-grid">
    ${cmdCard({ title: "pwd", desc: "Print working directory. Shows your current location.", example: "$ pwd", output: "/home/user", tint: "green", icon: ICON.folder })}
    ${cmdCard({ title: "ls", desc: "List files and directories. Shows the contents of your current location.", example: "$ ls", output: "docs  downloads  file.txt  logs  music  scripts", tint: "green", icon: ICON.list })}
    ${cmdCard({ title: "cd", desc: "Change directory. Move into another directory.", example: "$ cd /var/log\n$ pwd", output: "/var/log", tint: "blue", icon: ICON.folder })}
    ${cmdCard({ title: "clear", desc: "Clear the terminal screen. Makes your screen clean and easy to read.", example: "$ clear", comment: "(screen cleared)", tint: "blue", icon: ICON.terminal })}
    ${cmdCard({ title: "history", desc: "Show previously executed commands. View or reuse past commands.", example: "$ history", output: "1  ls -la\n2  cd /etc\n3  pwd", tint: "purple", icon: ICON.clock })}
    ${cmdCard({ title: "man", desc: "View the manual page for a command. Detailed documentation for any command.", example: "$ man ls", comment: "(manual page appears)", tint: "purple", icon: ICON.book })}
    ${cmdCard({ title: "Tab Completion", desc: "Press Tab to auto-complete commands, filenames, and directories. Saves time and reduces typing errors.", example: "$ cd Doc<Tab>\n$ cd Documents/", tint: "gold", icon: ICON.terminal })}
    ${cmdCard({ title: "Hidden Files", desc: "Files starting with . are hidden. Use -a option with ls to see them.", example: "$ ls -a", output: ".  ..  .bashrc  .config  .git  file.txt  docs", tint: "gold", icon: ICON.magnifier })}
  </div>

  ${sectionHeader("Reading Command Help")}
  <div class="cmd-grid cols-3">
    ${cmdCard({ title: "--help", desc: "Quick help for most commands.", example: "$ ls --help", tint: "blue", icon: ICON.terminal })}
    ${cmdCard({ title: "man", desc: "Full manual page.", example: "$ man ls", tint: "blue", icon: ICON.book })}
    ${cmdCard({ title: "info", desc: "Detailed info (if available).", example: "$ info ls", tint: "blue", icon: ICON.book })}
  </div>
  ${calloutBox({ type: "tip", text: "<p>Whenever you forget a command, use <code>--help</code> or <code>man</code> before guessing.</p>" })}

  ${sectionHeader("Useful ls Options")}
  ${dataTable({
    headers: ["OPTION", "WHAT IT DOES", "EXAMPLE", "OUTPUT (MAY VARY)"],
    monoCols: [0, 2],
    rows: [
      ["ls -l", "Long listing format", "<code>$ ls -l</code>", "Detailed info (perm, owner, size, date)"],
      ["ls -a", "Show hidden files", "<code>$ ls -a</code>", "Shows files starting with ."],
      ["ls -la", "Long format + hidden files", "<code>$ ls -la</code>", "Detailed list including hidden files"],
      ["ls -lh", "Human-readable file sizes", "<code>$ ls -lh</code>", "Shows sizes like 1.2K, 3M"],
      ["ls -lt", "Sorted by modification time", "<code>$ ls -lt</code>", "Newest files first"],
      ["ls -R", "Recursive listing", "<code>$ ls -R</code>", "List all files in subdirectories"],
    ],
  })}

  ${sectionHeader("Practical: Navigate Between Directories Without Using a GUI")}
  ${stepsFlow([
    { n: "1", title: "Start at your home directory", cmd: "$ pwd", out: "/home/user" },
    { n: "2", title: "List files and folders", cmd: "$ ls" },
    { n: "3", title: "Move into a directory", cmd: "$ cd folder_name" },
    { n: "4", title: "Move deeper into subfolders", cmd: "$ cd subfolder" },
    { n: "5", title: "Move back to parent directory", cmd: "$ cd .." },
    { n: "6", title: "Go back to your home", cmd: "$ cd ~" },
  ])}`;
  return pageChrome(4, 20, "NAVIGATION", inner, "Practice daily — the more you use the terminal, the faster you become.");
}

// ---------------------------------------------------------------------------
// PAGE 5 — Creating, Copying, Moving, and Deleting
// ---------------------------------------------------------------------------
function page5FileMgmt(): string {
  const inner = `
  ${titleHtml("CREATING, COPYING,<br>MOVING, AND DELETING", "MASTER THE BASICS OF FILE AND DIRECTORY MANAGEMENT")}
  <div class="cmd-grid">
    ${cmdCard({ title: "touch", desc: "Create an empty file or update file timestamp.", example: "$ touch file.txt\n$ touch notes.md", tint: "green", icon: ICON.terminal })}
    ${cmdCard({ title: "rm", desc: "Remove (delete) files or directories.", example: "$ rm file.txt\n$ rm -r old_project/", tint: "red", icon: ICON.warning })}
    ${cmdCard({ title: "mkdir", desc: "Create a new directory (folder).", example: "$ mkdir project\n$ mkdir src logs", tint: "blue", icon: ICON.folder })}
    ${cmdCard({ title: "rmdir", desc: "Remove an empty directory.", example: "$ rmdir empty_folder", tint: "red", icon: ICON.folder })}
    ${cmdCard({ title: "cp", desc: "Copy files or directories from one place to another.", example: "$ cp file.txt backup.txt\n$ cp -r project/ project_backup/", tint: "green", icon: ICON.package })}
    ${cmdCard({ title: "Recursive Operations", desc: "Use -r (recursive) to operate on directories and their contents.", example: "$ cp -r src/ backup_src/\n$ rm -r logs/", tint: "purple", icon: ICON.gear })}
    ${cmdCard({ title: "mv", desc: "Move or rename files and directories.", example: "$ mv file.txt newname.txt\n$ mv project/ old_project/", tint: "blue", icon: ICON.terminal })}
    ${cmdCard({ title: "Wildcards", desc: "Use * to match multiple characters. ? matches a single character.", example: "$ rm *.log\n$ rm file?.txt docs/", tint: "gold", icon: ICON.list })}
  </div>

  ${sectionHeader("Safe Deletion Habits")}
  ${dataTable({
    headers: ["HABIT", "DESCRIPTION"],
    monoCols: [0],
    rows: [
      ["ls -l *.log", "Always preview before deleting."],
      ["rm -i file.txt", "Use rm -i to confirm each deletion."],
      ["pwd", "Double-check paths and filenames."],
      ["rm -rf / # NEVER DO THIS", "Avoid rm -rf / (very dangerous)."],
    ],
  })}

  ${sectionHeader("Practical: Create, Organize, Copy, and Clean Up a Project")}
  ${stepsFlow([
    { n: "1", title: "Create project directory", cmd: "$ mkdir my_project\n$ cd my_project" },
    { n: "2", title: "Create subdirectories", cmd: "$ mkdir src docs logs" },
    { n: "3", title: "Create some files", cmd: "$ touch src/app.py\n$ touch docs/readme.md\n$ touch logs/app.log" },
    { n: "4", title: "List project structure", cmd: "$ ls -R" },
    { n: "5", title: "Copy a file", cmd: "$ cp docs/readme.md docs/readme_backup.md" },
    { n: "6", title: "Move/rename a file", cmd: "$ mv src/app.py src/main.py" },
    { n: "7", title: "Copy entire directory", cmd: "$ cp -r src/ src_backup/" },
    { n: "8", title: "Delete a file", cmd: "$ rm logs/app.log" },
    { n: "9", title: "Remove empty directory", cmd: "$ rmdir logs" },
    { n: "10", title: "Final project structure", cmd: "my_project/\n├── docs/\n│   └── readme.md\n├── src/\n│   ├── main.py\n│   └── main_backup.py\n└── src_backup/" },
  ])}

  ${calloutBox({ type: "success", title: "KEY TAKEAWAY", text: "<p>Mastering file operations is the foundation of confident Linux administration. Always preview, double-check, and prefer the safe option.</p>" })}`;
  return pageChrome(5, 20, "FILE MANAGEMENT", inner, "Always preview with ls before deleting.");
}

// ---------------------------------------------------------------------------
// PAGE 6 — Reading and Editing Files
// ---------------------------------------------------------------------------
function page6ReadingEditing(): string {
  const inner = `
  ${titleHtml("READING AND<br>EDITING FILES", "VIEW, INSPECT, AND EDIT FILES LIKE A PRO")}
  <div class="cmd-grid cols-3">
    ${cmdCard({ title: "cat", desc: "Display the entire contents of a file.", example: "$ cat file.txt", tint: "green", icon: ICON.terminal })}
    ${cmdCard({ title: "less", desc: "View file content one screen at a time. Navigate easily.", example: "$ less largefile.log\n# Space (down) b (up) q (quit)", tint: "green", icon: ICON.book })}
    ${cmdCard({ title: "head", desc: "Show the first 10 lines of a file (default).", example: "$ head file.txt\n$ head -n 20 file.txt", tint: "blue", icon: ICON.terminal })}
    ${cmdCard({ title: "tail", desc: "Show the last 10 lines of a file (default).", example: "$ tail file.txt\n$ tail -n 50 file.txt", tint: "blue", icon: ICON.terminal })}
    ${cmdCard({ title: "nano", desc: "Simple and user-friendly text editor for beginners.", example: "$ nano config.conf\n# Ctrl+O (save) Ctrl+X (exit)", tint: "purple", icon: ICON.pencil })}
    ${cmdCard({ title: "vim", desc: "Powerful text editor for advanced users. Three modes: Insert · Normal · Command.", example: "$ vim file.txt\n# i (insert) Esc (normal)\n# :w (save) :q (quit) :wq (save & quit)", tint: "purple", icon: ICON.terminal })}
    ${cmdCard({ title: "wc", desc: "Count lines, words, and characters in a file.", example: "$ wc file.txt\n$ wc -l file.txt   # lines only", tint: "gold", icon: ICON.list })}
    ${cmdCard({ title: "Viewing Large Files", desc: "Use less to open large files without loading everything into memory.", example: "$ less very_large.log\n# Search: /error (Enter)\n# Next: n   Prev: N", tint: "green", icon: ICON.book })}
    ${cmdCard({ title: "tail -f", desc: "Monitor logs in real time. New lines appear instantly.", example: "$ tail -f app.log\n# Press Ctrl+C to stop.", tint: "green", icon: ICON.terminal })}
  </div>

  ${sectionHeader("Common tail Options")}
  <div class="concept-grid cols-3">
    ${conceptCard({ tint: "blue", icon: ICON.terminal, title: "-f", body: "Follow the file continuously (live logs)." })}
    ${conceptCard({ tint: "blue", icon: ICON.terminal, title: "-n", body: "Show last n lines." })}
    ${conceptCard({ tint: "blue", icon: ICON.terminal, title: "-F", body: "Follow by name (handle log rotation)." })}
  </div>

  ${sectionHeader("Text Editor Quick Reference")}
  ${dataTable({
    headers: ["NANO ESSENTIALS", "", "VIM ESSENTIALS", ""],
    rows: [
      ["Open file", "<code>$ nano filename</code>", "Open file", "<code>$ vim filename</code>"],
      ["Save file", "Ctrl + O, then Enter", "Insert mode", "Press <code>i</code>"],
      ["Exit editor", "Ctrl + X", "Save file", "<code>:w</code>"],
      ["Cut line", "Ctrl + K", "Save &amp; exit", "<code>:wq</code>"],
      ["Paste line", "Ctrl + U", "Quit (without save)", "<code>:q!</code>"],
      ["Search", "Ctrl + W", "Search", "<code>/text</code> (Enter)"],
      ["", "", "Exit insert mode", "Press <code>Esc</code>"],
    ],
  })}

  ${sectionHeader("Practical: Create, Edit, and Inspect Files")}
  ${stepsFlow([
    { n: "1", title: "Create a directory for the lab", cmd: "$ mkdir file_lab\n$ cd file_lab" },
    { n: "2", title: "Create a configuration file with nano", cmd: "$ nano app.conf\n# add some content\n# Ctrl+O (save) Ctrl+X (exit)" },
    { n: "3", title: "View the file content using cat", cmd: "$ cat app.conf" },
    { n: "4", title: "Check first and last lines of a log file", cmd: "$ head app.log\n$ tail app.log" },
    { n: "5", title: "Monitor a log file in real time", cmd: "$ tail -f app.log" },
    { n: "6", title: "Count lines, words, and characters", cmd: "$ wc app.log" },
  ])}

  ${calloutBox({ type: "success", title: "KEY TAKEAWAY", text: "<p>Master these commands and you can read, inspect, monitor, and edit any file in Linux confidently. These skills are essential for DevOps and system engineering.</p>" })}`;
  return pageChrome(6, 20, "READING & EDITING", inner, "tail -f is your best friend for live logs.");
}

// ---------------------------------------------------------------------------
// PAGE 7 — Linux Users and Groups
// ---------------------------------------------------------------------------
function page7UsersGroups(): string {
  const inner = `
  ${titleHtml("LINUX USERS<br>AND GROUPS", "MANAGE ACCESS, PERMISSIONS, AND OWNERSHIP")}
  <div class="body cols-3">
    <div style="display:flex;flex-direction:column;gap:12px;">
      ${sectionHeader("Key Concepts")}
      ${conceptCard({ tint: "blue", icon: ICON.users, title: "What a Linux user is", body: "A user is an identity that can log in and run processes." })}
      ${conceptCard({ tint: "red", icon: ICON.shield, title: "Root user", body: "The superuser with UID 0. Has unlimited access." })}
      ${conceptCard({ tint: "green", icon: ICON.users, title: "Regular users", body: "Human users with limited permissions." })}
      ${conceptCard({ tint: "purple", icon: ICON.gear, title: "System users", body: "Created by the system or applications. Usually cannot login interactively." })}
      ${conceptCard({ tint: "gold", icon: ICON.key, title: "UID and GID", body: "UID (User ID) uniquely identifies a user. GID (Group ID) identifies a group." })}
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;">
      ${sectionHeader("Important Files")}
      ${termBlock("/etc/passwd", [
        "$ cat /etc/passwd",
        "root:x:0:0:root:/root:/bin/bash",
        "alice:x:1001:1001:Alice:/home/alice:/bin/bash",
        "bob:x:1002:1002:Bob:/home/bob:/bin/bash",
        "# Format: username:x:UID:GID:comment:home:shell",
      ])}
      ${termBlock("/etc/group", [
        "$ cat /etc/group",
        "root:x:0:",
        "developers:x:1001:alice,bob",
        "ops:x:1002:charlie",
        "# Format: groupname:x:GID:user1,user2,user3",
      ])}
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;">
      ${sectionHeader("Essential Commands")}
      ${cmdCard({ title: "useradd", desc: "Create a new user.", example: "$ sudo useradd alice", tint: "blue", icon: ICON.users })}
      ${cmdCard({ title: "usermod", desc: "Modify user properties.", example: "$ sudo usermod -aG developers alice", tint: "blue", icon: ICON.pencil })}
      ${cmdCard({ title: "userdel", desc: "Delete a user account.", example: "$ sudo userdel bob", tint: "red", icon: ICON.warning })}
      ${cmdCard({ title: "groupadd", desc: "Create a new group.", example: "$ sudo groupadd developers", tint: "green", icon: ICON.users })}
      ${cmdCard({ title: "id", desc: "Show user and group IDs.", example: "$ id alice", tint: "gold", icon: ICON.key })}
      ${cmdCard({ title: "groups", desc: "Show groups a user belongs to.", example: "$ groups alice", tint: "gold", icon: ICON.users })}
    </div>
  </div>

  ${sectionHeader("User and Group Information at a Glance")}
  ${dataTable({
    headers: ["TYPE", "DESCRIPTION", "EXAMPLE", "UID", "GID", "LOGIN", "HOME"],
    rows: [
      ["Root User", "Superuser with all privileges", "root", "0", "0", "Yes", "/root"],
      ["Regular User", "Human user for daily tasks", "alice", "1001+", "1001+", "Yes", "/home/alice"],
      ["System User", "Used by system services", "www-data", "1-999", "1-999", "No", "/nonexistent"],
    ],
  })}

  <div class="body cols-2" style="margin-top:14px;">
    <div>
      ${sectionHeader("Common usermod Options")}
      ${dataTable({
        headers: ["Option", "Description"],
        monoCols: [0],
        rows: [
          ["-aG group", "Add user to supplementary group"],
          ["-G group", "Set primary group"],
          ["-l newname", "Change username"],
          ["-d /path", "Change home directory"],
          ["-s /shell", "Change login shell"],
        ],
      })}
    </div>
    <div>
      ${sectionHeader("Check User Details")}
      ${termBlock("id &amp; groups", [
        "$ id alice",
        "uid=1001(alice) gid=1001(alice)",
        "groups=1001(alice),1001(developers)",
        "",
        "$ groups alice",
        "alice : alice developers",
      ])}
    </div>
  </div>

  ${sectionHeader("Best Practices")}
  ${calloutBox({ type: "tip", text: `<ul>
    <li>Use regular users for daily work.</li>
    <li>Give minimum necessary privileges.</li>
    <li>Never share root credentials.</li>
    <li>Audit user access regularly.</li>
    <li>Remove unused accounts.</li>
  </ul>` })}

  ${sectionHeader("Practical: Create a User and Assign to a Group")}
  ${stepsFlow([
    { n: "1", title: "Create a group", cmd: "$ sudo groupadd developers" },
    { n: "2", title: "Create a new user", cmd: "$ sudo useradd -m -s /bin/bash alice" },
    { n: "3", title: "Set a password for the user", cmd: "$ sudo passwd alice" },
    { n: "4", title: "Add user to the group", cmd: "$ sudo usermod -aG developers alice" },
    { n: "5", title: "Verify user details with id", cmd: "$ id alice" },
    { n: "6", title: "Check group membership", cmd: "$ groups alice" },
    { n: "7", title: "List all users", cmd: "$ cat /etc/passwd" },
  ])}

  ${calloutBox({ type: "success", title: "KEY TAKEAWAY", text: "<p>Users and groups control who can access what in Linux. Understanding them is fundamental for system security and administration.</p>" })}`;
  return pageChrome(7, 20, "USERS & GROUPS", inner, "Use minimum necessary privileges — always.");
}

// ---------------------------------------------------------------------------
// PAGE 8 — File Ownership and Permissions
// ---------------------------------------------------------------------------
function page8Permissions(): string {
  const inner = `
  ${titleHtml("FILE OWNERSHIP<br>AND PERMISSIONS", "CONTROL WHO CAN READ, WRITE, AND EXECUTE FILES")}
  <div class="concept-grid cols-3">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.book, title: "Permission Basics", bullets: ["<b>READ (r):</b> View file contents or list directory contents.", "<b>WRITE (w):</b> Modify file contents or create/delete files in a directory.", "<b>EXECUTE (x):</b> Run a file or enter (cd into) a directory."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.users, title: "User, Group, Others", bullets: ["<b>USER (u):</b> The owner of the file or directory.", "<b>GROUP (g):</b> The group that owns the file or directory.", "<b>OTHERS (o):</b> Everyone else on the system."] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.terminal, title: "Understanding rwx", body: "<b>EXAMPLE:</b> <code>-rwxr-x---</code><br><b>USER:</b> rwx · <b>GROUP:</b> r-x · <b>OTHERS:</b> ---<br>Owner: read, write, execute · Group: read, execute · Others: no permission" })}
    ${conceptCard({ num: "4", tint: "gold", icon: ICON.list, title: "Permission Numeric Values", body: "<b>How numeric permissions work</b> — add the values:<br><code>r (4) + w (2) + x (1) = 7 (rwx)</code><br><code>r (4) + x (1) = 5 (r-x)</code><br><code>r (4) = 4 (r--)</code><br><code>w (2) + x (1) = 3 (-wx)</code><br><code>x (1) = 1 (--x)</code><br><code>--- (0) = 0 (---)</code>" })}
    ${conceptCard({ num: "5", tint: "blue", icon: ICON.gear, title: "chmod", body: "Change file or directory permissions.<br><b>Syntax:</b> <code>chmod [options] mode file</code>", cmds: [{ cmd: "$ chmod 755 script.sh" }, { cmd: "$ chmod -R 644 data/" }] })}
    ${conceptCard({ num: "6", tint: "green", icon: ICON.users, title: "chown", body: "Change ownership (user and group).<br><b>Syntax:</b> <code>chown [user][:group] file</code>", cmds: [{ cmd: "$ chown alice file.txt" }, { cmd: "$ chown alice:developers file.txt" }] })}
    ${conceptCard({ num: "7", tint: "purple", icon: ICON.users, title: "chgrp", body: "Change group ownership.<br><b>Syntax:</b> <code>chgrp [group] file</code>", cmds: [{ cmd: "$ chgrp developers file.txt" }, { cmd: "$ chgrp -R developers project/" }] })}
    ${conceptCard({ num: "8", tint: "red", icon: ICON.warning, title: "Why chmod 777 is BAD", bullets: ["Gives full access to everyone.", "Anyone can read, modify, or delete your files.", "Creates security risks.", "Attackers can exploit writable files.", "Use the principle of least privilege."] })}
    ${conceptCard({ num: "9", tint: "gold", icon: ICON.lock, title: "Permission Denied Troubleshooting", bullets: ["1. Check file owner: <code>$ ls -l file</code>", "2. Check permissions: <code>$ ls -l file</code>", "3. Check your user: <code>$ whoami</code>", "4. Check your groups: <code>$ groups</code>", "5. Fix permissions: <code>$ chmod ...</code>", "6. Fix ownership: <code>$ chown ...</code>", "7. Try again."] })}
  </div>

  ${sectionHeader("Common Numeric Permissions")}
  ${dataTable({
    headers: ["NUMERIC", "RWX", "MEANING"],
    monoCols: [0, 1],
    rows: [
      ["755", "rwxr-xr-x", "Owner full, Group read+execute, Others read+execute"],
      ["644", "rw-r--r--", "Owner read+write, Group read, Others read"],
      ["600", "rw-------", "Owner read+write only"],
      ["664", "rw-rw-r--", "Owner read+write, Group read+write, Others read"],
      ["700", "rwx-------", "Owner full only"],
      ["777", "rwxrwxrwx", "Everyone full (DANGEROUS)"],
    ],
  })}

  ${sectionHeader("10. Quick Reference")}
  ${termBlock("Permission Commands", [
    "$ ls -l            # View detailed permissions",
    "$ chmod 755 file   # Change permissions",
    "$ chown user file  # Change owner",
    "$ chgrp group file # Change group",
  ])}

  ${sectionHeader("Practical: Diagnose and Repair a File Permission Problem")}
  ${stepsFlow([
    { n: "1", title: "Create a project directory and file", cmd: "$ mkdir lab\n$ cd lab\n$ touch app.sh" },
    { n: "2", title: "Give wrong permissions", cmd: "$ chmod 000 app.sh\n$ ls -l app.sh", out: "---------- app.sh" },
    { n: "3", title: "Try to run the file", cmd: "$ ./app.sh", out: "bash: ./app.sh: Permission denied" },
    { n: "4", title: "Check ownership and permissions", cmd: "$ ls -l app.sh", out: "---------- 1 alice alice 0 May 24 10:00 app.sh" },
    { n: "5", title: "Fix permissions (owner full)", cmd: "$ chmod 700 app.sh\n$ ls -l app.sh", out: "-rwx------ 1 alice alice 0 May 24 10:00 app.sh" },
    { n: "6", title: "Run again (works now)", cmd: "$ ./app.sh", out: "Hello from app.sh" },
    { n: "7", title: "Change group ownership", cmd: "$ usermod -aG devs bob\n$ ls -l app.sh", out: "-rwx----- 1 alice devs 0 May 24 10:00 app.sh" },
  ])}

  ${calloutBox({ type: "success", title: "KEY TAKEAWAY", text: "<p>Properly managing file ownership and permissions keeps your system secure, stable, and predictable. Grant the minimum access required — nothing more.</p>" })}`;
  return pageChrome(8, 20, "PERMISSIONS", inner, "chmod 777 is almost always a mistake.");
}

// ---------------------------------------------------------------------------
// PAGE 9 — Sudo, Root, and Privilege
// ---------------------------------------------------------------------------
function page9Sudo(): string {
  const inner = `
  ${titleHtml("SUDO, ROOT,<br>AND PRIVILEGE", "CONTROL · SECURITY · RESPONSIBILITY")}
  <div class="concept-grid cols-2">
    ${conceptCard({ num: "1", tint: "red", icon: ICON.shield, title: "What Root Can Do", bullets: ["Install or remove software", "Modify system files", "Manage users and groups", "Start/stop system services", "Change network settings", "Access all files and data", "Bypass normal restrictions"] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.shield, title: "sudo", body: "Run a command as another user (usually root).", bullets: ["Allows limited admin access", "Uses your own password (if configured)", "Safer than using root directly"], cmds: [{ cmd: "$ sudo command" }, { cmd: "$ sudo systemctl restart nginx" }, { cmd: "$ sudo apt update" }] })}
    ${conceptCard({ num: "3", tint: "blue", icon: ICON.key, title: "su", body: "Switch user. Commonly used to become root.", bullets: ["Becomes the target user", "Usually requires the target user's password", "Provides full access of that user"], cmds: [{ cmd: "$ su -", out: "Password:\n# now you are root" }] })}
    ${conceptCard({ num: "4", tint: "purple", icon: ICON.gear, title: "Privilege Escalation", body: "Moving from a normal user to a higher privilege (like root).", bullets: ["<b>Legitimate:</b> sudo, su", "<b>Illegitimate:</b> exploits, misconfigurations", "Always follow least privilege principle"] })}
    ${conceptCard({ num: "5", tint: "gold", icon: ICON.book, title: "/etc/sudoers", body: "File that controls who can run what as root using sudo. Located at <code>/etc/sudoers</code>. Direct editing can break your system!" })}
    ${conceptCard({ num: "6", tint: "green", icon: ICON.terminal, title: "visudo", body: "Safe way to edit /etc/sudoers. Syntax checking, prevents lockout. Use this command always.", cmds: [{ cmd: "$ sudo visudo" }] })}
    ${conceptCard({ num: "7", tint: "blue", icon: ICON.shield, title: "Least Privilege", body: "Give users only the access they need.", bullets: ["Reduces security risks", "Limits damage from mistakes or attacks", "Essential for secure systems"] })}
    ${conceptCard({ num: "8", tint: "red", icon: ICON.warning, title: "Why Running Everything as Root is Dangerous", bullets: ["Any mistake can break the system", "Malware gets full control", "No accountability", "Harder to audit actions", "Violates security best practices"] })}
  </div>

  ${calloutBox({ type: "warning", title: "ROOT HAS UNLIMITED POWER", text: "<p>Use carefully. Never edit <code>/etc/sudoers</code> with a normal text editor — always use <code>visudo</code>.</p>" })}

  ${sectionHeader("9. Quick Command Reference")}
  ${dataTable({
    headers: ["Command", "Description"],
    monoCols: [0],
    rows: [
      ["whoami", "Show current user"],
      ["sudo -l", "List sudo permissions"],
      ["sudo -v", "Refresh sudo token"],
      ["su -", "Switch to root user"],
      ["id", "Show user and groups"],
      ["groups", "Show your groups"],
    ],
  })}

  ${sectionHeader("10. Practical: Allow a User to Perform an Administrative Task Safely")}
  ${calloutBox({ type: "goal", title: "GOAL", text: "<p>Allow user <code>devops</code> to restart <code>nginx</code> without giving full root access.</p>" })}
  ${stepsFlow([
    { n: "1", title: "Create the devops user", cmd: "$ sudo useradd devops\n$ sudo passwd devops" },
    { n: "2", title: "Open sudoers safely", cmd: "$ sudo visudo" },
    { n: "3", title: "Add a specific rule", cmd: "devops ALL=(root) NOPASSWD: /bin/systemctl restart nginx" },
    { n: "4", title: "Save and exit visudo", cmd: "# visudo validates syntax on save" },
    { n: "5", title: "Switch to devops and test", cmd: "$ sudo -u devops -i\n$ sudo systemctl restart nginx" },
    { n: "6", title: "Verify nginx is running", cmd: "$ systemctl status nginx" },
  ])}`;
  return pageChrome(9, 20, "SUDO & ROOT", inner, "Least privilege — grant only what is needed.");
}

// ---------------------------------------------------------------------------
// PAGE 10 — Finding Files and Information
// ---------------------------------------------------------------------------
function page10Finding(): string {
  const inner = `
  ${titleHtml("FINDING FILES<br>AND INFORMATION", "THE RIGHT COMMAND SAVES TIME.")}
  <div class="concept-grid cols-3">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.magnifier, title: "find", body: "Search for files and directories in real time. Very powerful.<br><b>Syntax:</b> <code>find [path] [options] [expression]</code>", cmds: [{ cmd: "$ find /etc -name my.conf" }] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.database, title: "locate", body: "Search using a prebuilt database. Very fast.<br><b>Syntax:</b> <code>locate [filename]</code>", cmds: [{ cmd: "$ locate nginx.conf" }] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.terminal, title: "which", body: "Show the full path of a command.<br><b>Syntax:</b> <code>which [command]</code>", cmds: [{ cmd: "$ which nginx" }] })}
    ${conceptCard({ num: "4", tint: "gold", icon: ICON.magnifier, title: "whereis", body: "Locate binaries, source code and man pages.<br><b>Syntax:</b> <code>whereis [name]</code>", cmds: [{ cmd: "$ whereis python3" }] })}
    ${conceptCard({ num: "5", tint: "red", icon: ICON.magnifier, title: "grep", body: "Search text patterns inside files.<br><b>Syntax:</b> <code>grep [options] \"pattern\" [file]</code>", cmds: [{ cmd: "$ grep \"Listen\" /etc/nginx/nginx.conf" }] })}
  </div>

  ${sectionHeader("6. Common Search Types with find")}
  <div class="concept-grid cols-2">
    ${conceptCard({ tint: "blue", icon: ICON.folder, title: "A. Recursive Search", body: "Search in current directory and all subdirectories.", cmds: [{ cmd: "$ find . -name \"*.log\"" }] })}
    ${conceptCard({ tint: "green", icon: ICON.magnifier, title: "B. Search by Filename", body: "Find a file by its name.", cmds: [{ cmd: "$ find / -name nginx.conf 2>/dev/null" }] })}
    ${conceptCard({ tint: "purple", icon: ICON.folder, title: "C. Search by File Type", body: "<code>f</code> = file, <code>d</code> = directory", cmds: [{ cmd: "$ find /etc -type f -name \"*.conf\"" }, { cmd: "$ find /var -type d -name \"cache\"" }] })}
    ${conceptCard({ tint: "gold", icon: ICON.database, title: "D. Search by Size", body: "<code>+100M</code> = larger than 100MB<br><code>-10M</code> = smaller than 10MB", cmds: [{ cmd: "$ find . -type f -size +100M" }, { cmd: "$ find . -type f -size -10M" }] })}
    ${conceptCard({ tint: "red", icon: ICON.clock, title: "E. Search by Time", body: "Find files modified in the last 1 day.", cmds: [{ cmd: "$ find . -type f -mtime -1" }] })}
  </div>

  ${sectionHeader("7. Combining find and grep (Powerful!)")}
  ${termBlock("Find + grep examples", [
    "$ find /etc -type f -name \"*.conf\" -exec grep -H \"server\" {} \\;",
    "# Find .conf files and search for \"server\" inside them.",
    "",
    "$ grep -R \"root\" /etc/",
    "# Search recursively for \"root\" inside /etc directory.",
    "",
    "$ find /var/log -type f -exec grep -H \"error\" {} \\;",
    "# Find log files containing the word \"error\".",
  ])}

  ${sectionHeader("8. Practical: Find a Configuration File and Locate a Specific Value")}
  ${stepsFlow([
    { n: "1", title: "Find the nginx configuration file", cmd: "$ find /etc -type f -name \"nginx.conf\" 2>/dev/null" },
    { n: "2", title: "Verify the file exists", cmd: "$ ls -l /etc/nginx/nginx.conf" },
    { n: "3", title: "Search for a specific value inside the file", cmd: "$ grep -n \"Listen\" /etc/nginx/nginx.conf" },
    { n: "4", title: "Search recursively in all .conf files for a value", cmd: "$ grep -R \"server_name\" /etc/*.conf" },
    { n: "5", title: "Find files modified in last 1 day", cmd: "$ find /etc -type f -mtime -1" },
  ])}

  <div class="callout-grid cols-3" style="margin-top:14px;">
    ${calloutBox({ type: "success", title: "SUCCESS!", text: "<p>You found the file and the required information using the right tools.</p>" })}
    ${calloutBox({ type: "tip", title: "TIPS", text: `<ul>
      <li>Use <code>find</code> for accurate real-time search.</li>
      <li>Use <code>locate</code> for quick results (after running <code>updatedb</code>).</li>
      <li>Use <code>grep</code> to search inside files.</li>
      <li>Combine commands for powerful results.</li>
    </ul>` })}
    ${calloutBox({ type: "warning", title: "REMEMBER", text: `<ul>
      <li>Searching whole system <code>/</code> can be slow.</li>
      <li>Use <code>2&gt;/dev/null</code> to hide permission denied errors.</li>
    </ul>` })}
  </div>`;
  return pageChrome(10, 20, "FIND & SEARCH", inner, "Combine find + grep for powerful file search.");
}

// ---------------------------------------------------------------------------
// PAGE 11 — Pipes and Redirection
// ---------------------------------------------------------------------------
function page11Pipes(): string {
  const inner = `
  ${titleHtml("PIPES AND<br>REDIRECTION", "CONTROL WHERE COMMAND INPUT AND OUTPUT GO")}
  <div class="concept-grid cols-3">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.terminal, title: "Standard Input (STDIN)", body: "Data that a command receives as input. Usually from keyboard or a file.", cmds: [{ cmd: "$ command < file.txt" }] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.terminal, title: "Standard Output (STDOUT)", body: "Normal output of a command. Displayed on screen by default.", cmds: [{ cmd: "$ command > output.txt" }] })}
    ${conceptCard({ num: "3", tint: "red", icon: ICON.warning, title: "Standard Error (STDERR)", body: "Error messages from a command. Displayed on screen by default.", cmds: [{ cmd: "$ command 2> error.log" }] })}
  </div>

  ${sectionHeader("4. Redirection Operators")}
  ${dataTable({
    headers: ["OPERATOR", "NAME", "DESCRIPTION", "SYNTAX EXAMPLE", "EXAMPLE USE"],
    monoCols: [0, 3],
    rows: [
      [">", "Redirect Output", "Redirect standard output (overwrite).", "<code>$ command &gt; file.txt</code>", "Save output to file.txt (overwrite if file exists)."],
      [">>", "Append Output", "Redirect standard output (append).", "<code>$ command &gt;&gt; file.txt</code>", "Append output to file.txt (create if not exists)."],
      ["<", "Redirect Input", "Use file as standard input instead of keyboard.", "<code>$ command &lt; file.txt</code>", "Read input from file.txt instead of typing."],
      ["2>", "Redirect Error", "Redirect standard error (overwrite).", "<code>$ command 2&gt; error.log</code>", "Save errors to error.log (overwrite if exists)."],
      ["2>>", "Append Error", "Redirect standard error (append).", "<code>$ command 2&gt;&gt; error.log</code>", "Append errors to error.log."],
      ["|", "Pipe", "Send output of one command as input to another.", "<code>$ command1 | command2</code>", "Use output of command1 as input to command2."],
      ["tee", "Tee", "Read from input and write to both output and file.", "<code>$ command | tee file.txt</code>", "Show output on screen and save to file.txt."],
    ],
  })}

  <div class="body cols-2" style="margin-top:14px;">
    ${conceptCard({ num: "5", tint: "purple", icon: ICON.gear, title: "Why Pipelines Matter", bullets: ["Chain multiple commands together.", "Filter and transform data quickly.", "Reduce intermediate files.", "Automate complex tasks easily.", "Essential skill for DevOps, SRE and system administrators."] })}
    ${conceptCard({ num: "6", tint: "gold", icon: ICON.terminal, title: "tee Command (Example)", body: "<code>tee</code> duplicates the input: one copy to screen, one copy to file.", cmds: [{ cmd: "$ ls -l | tee listing.txt" }] })}
  </div>

  ${sectionHeader("7. Practical: Take Command Output, Filter It, and Save to a File")}
  ${stepsFlow([
    { n: "1", title: "List all running processes", cmd: "$ ps aux" },
    { n: "2", title: "Filter lines containing \"nginx\"", cmd: "$ ps aux | grep nginx" },
    { n: "3", title: "Show output on screen and save to a file", cmd: "$ ps aux | grep nginx | tee nginx_processes.txt" },
    { n: "4", title: "Count the number of nginx processes", cmd: "$ ps aux | grep nginx | wc -l" },
    { n: "5", title: "Save only errors to a log file", cmd: "$ some_command 2> errors.log" },
    { n: "6", title: "Append output to log file", cmd: "$ echo \"Done\" >> process.log" },
  ])}

  <div class="callout-grid cols-3">
    ${calloutBox({ type: "note", title: "QUICK REFERENCE", text: `<ul>
      <li><code>&gt;</code> redirect output (overwrite)</li>
      <li><code>&gt;&gt;</code> redirect output (append)</li>
      <li><code>&lt;</code> redirect input</li>
      <li><code>2&gt;</code> redirect error (overwrite)</li>
      <li><code>2&gt;&gt;</code> redirect error (append)</li>
      <li><code>|</code> pipe</li>
      <li><code>tee</code> duplicate to file and screen</li>
    </ul>` })}
    ${calloutBox({ type: "tip", title: "TIPS", text: `<ul>
      <li>Use quotes when searching for text with spaces.</li>
      <li>Combine pipes with grep, awk, sort, uniq, wc, head, tail for powerful text processing.</li>
      <li>Always check your redirections before running important commands.</li>
    </ul>` })}
    ${calloutBox({ type: "success", title: "KEY TAKEAWAY", text: "<p>Pipes and redirection let you control the flow of data between commands, files, and the screen — making you more efficient and powerful on the Linux CLI.</p>" })}
  </div>`;
  return pageChrome(11, 20, "PIPES & REDIRECTION", inner, "Master |, >, >>, <, 2>, tee.");
}

// ---------------------------------------------------------------------------
// PAGE 12 — Processes and Jobs
// ---------------------------------------------------------------------------
function page12Processes(): string {
  const inner = `
  ${titleHtml("PROCESSES<br>AND JOBS", "UNDERSTAND, MONITOR AND CONTROL RUNNING TASKS IN LINUX")}
  <div class="concept-grid cols-3">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.gear, title: "What Is a Process?", bullets: ["A process is an instance of a running program.", "Every process has a unique Process ID (PID).", "The parent process that started it has a Parent Process ID (PPID)."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.terminal, title: "PID and PPID", bullets: ["<b>PID:</b> Unique ID of the process.", "<b>PPID:</b> ID of the parent process.", "All processes (except init/systemd) have a parent."] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.terminal, title: "Foreground vs Background", body: "<b>FOREGROUND:</b> runs in the current terminal. You can see the output. You must wait for it to finish.<br><b>BACKGROUND:</b> runs behind the scenes. Does not block your terminal. You can continue working." })}
  </div>

  ${sectionHeader("4. Key Commands")}
  ${dataTable({
    headers: ["COMMAND", "PURPOSE", "EXAMPLE"],
    monoCols: [0, 2],
    rows: [
      ["ps", "Show running processes snapshot", "<code>ps aux</code>"],
      ["top", "Interactive real-time process monitor", "<code>top</code>"],
      ["pgrep", "Search for processes by name", "<code>pgrep nginx</code>"],
      ["kill", "Send signal to a process using PID", "<code>kill 1234</code>"],
      ["pkill", "Send signal to processes by name", "<code>pkill nginx</code>"],
      ["jobs", "List background and stopped jobs", "<code>jobs</code>"],
      ["bg", "Resume a stopped job in background", "<code>bg %1</code>"],
      ["fg", "Bring a background job to foreground", "<code>fg %1</code>"],
      ["&", "Run a command in background", "<code>sleep 100 &amp;</code>"],
    ],
  })}

  ${sectionHeader("5. Signals (Common Ones)")}
  ${dataTable({
    headers: ["SIGNAL", "NUM", "MEANING"],
    monoCols: [0, 1],
    rows: [
      ["SIGHUP", "1", "Reload / Reopen config"],
      ["SIGINT", "2", "Ctrl + C · Interrupt (terminate)"],
      ["SIGTERM", "15", "Graceful terminate"],
      ["SIGKILL", "9", "Force kill (cannot be ignored)"],
      ["SIGSTOP", "19", "Stop / Pause a process"],
      ["SIGCONT", "18", "Continue a stopped process"],
    ],
  })}
  ${calloutBox({ type: "tip", text: "<p>Use <code>SIGTERM</code> first. Use <code>SIGKILL</code> only when necessary.</p>" })}

  ${sectionHeader("6. Practical: Identify a Running Process and Stop It Safely")}
  ${stepsFlow([
    { n: "1", title: "LIST PROCESSES — Use ps aux or top to find the process", cmd: "$ ps aux" },
    { n: "2", title: "FIND PID — Note the PID of the process", cmd: "$ ps aux | grep nginx" },
    { n: "3", title: "VERIFY PROCESS — Confirm it is the correct process", cmd: "$ ps -p <PID>" },
    { n: "4", title: "GRACEFUL STOP — Try SIGTERM first (graceful stop)", cmd: "$ kill <PID>" },
    { n: "5", title: "FORCE STOP — If still running, use SIGKILL", cmd: "$ kill -9 <PID>" },
    { n: "6", title: "CONFIRM — Check again to make sure it stopped", cmd: "$ ps aux | grep <name>" },
  ])}`;
  return pageChrome(12, 20, "PROCESSES & JOBS", inner, "SIGTERM first, SIGKILL only when necessary.");
}

// ---------------------------------------------------------------------------
// PAGE 13 — Linux Services with Systemd
// ---------------------------------------------------------------------------
function page13Systemd(): string {
  const inner = `
  ${titleHtml("LINUX SERVICES<br>WITH SYSTEMD", "MANAGE, CONTROL AND AUTOMATE SERVICES ON LINUX")}
  <div class="concept-grid cols-3">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.gear, title: "What Is a Service?", bullets: ["A service is a background program that starts, runs and continues working to provide a function.", "Examples: web server, database, SSH server, logging, etc."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.gear, title: "systemd", bullets: ["The init system and service manager for most modern Linux distributions.", "Starts services at boot, supervises them, restarts on failure and manages dependencies."] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.package, title: "Units", bullets: ["systemd manages everything as \"units\".", "Most common unit type is service (.service).", "Other unit types: socket, timer, mount, target, etc."] })}
  </div>

  ${sectionHeader("4. Basic systemctl Commands")}
  ${dataTable({
    headers: ["COMMAND", "PURPOSE", "EXAMPLE", "DESCRIPTION"],
    monoCols: [0, 2],
    rows: [
      ["systemctl status &lt;service&gt;", "Check status of a service", "<code>systemctl status nginx</code>", "Shows if the service is active, inactive, failed, etc. Displays logs and last few messages."],
      ["systemctl start &lt;service&gt;", "Start a service", "<code>systemctl start nginx</code>", "Starts the service immediately."],
      ["systemctl stop &lt;service&gt;", "Stop a running service", "<code>systemctl stop nginx</code>", "Stops the service immediately."],
      ["systemctl restart &lt;service&gt;", "Restart a service", "<code>systemctl restart nginx</code>", "Stops and starts the service again."],
      ["systemctl enable &lt;service&gt;", "Enable service at boot", "<code>systemctl enable nginx</code>", "Ensures the service starts automatically when the system boots. Creates a symlink in system targets."],
      ["systemctl disable &lt;service&gt;", "Disable service at boot", "<code>systemctl disable nginx</code>", "Prevents the service from starting automatically at boot. Removes the symlink."],
    ],
  })}

  <div class="body cols-2" style="margin-top:14px;">
    ${conceptCard({ num: "5", tint: "gold", icon: ICON.gear, title: "Service Startup at Boot", body: "When enabled, the service starts automatically during system boot.", bullets: ["Check if enabled: <code>systemctl is-enabled &lt;service&gt;</code>", "Outputs: <code>enabled</code> / <code>disabled</code> / <code>static</code>"] })}
    ${conceptCard({ num: "6", tint: "red", icon: ICON.warning, title: "Failed Services", body: "If a service fails, systemd will show it as \"failed\".", bullets: ["Check failed services: <code>systemctl --failed</code>", "To see details and logs: <code>systemctl status &lt;service&gt;</code>"] })}
  </div>

  ${sectionHeader("7. Common Service States")}
  ${dataTable({
    headers: ["STATE", "MEANING"],
    monoCols: [0],
    rows: [
      ["active (running)", "Service is running."],
      ["active (exited)", "Service ran and exited."],
      ["inactive (dead)", "Service is stopped."],
      ["failed", "Service failed to start."],
      ["activating", "Service is starting."],
      ["deactivating", "Service is stopping."],
    ],
  })}

  ${sectionHeader("8. Practical: Start, Stop, Enable and Troubleshoot a Service")}
  ${stepsFlow([
    { n: "1", title: "Check current status", cmd: "$ sudo systemctl status nginx" },
    { n: "2", title: "Start the service", cmd: "$ sudo systemctl start nginx" },
    { n: "3", title: "Verify it is running", cmd: "$ systemctl status nginx" },
    { n: "4", title: "Enable at boot", cmd: "$ sudo systemctl enable nginx" },
    { n: "5", title: "Stop / restart", cmd: "$ sudo systemctl stop nginx\n$ sudo systemctl restart nginx" },
    { n: "6", title: "Check logs and errors", cmd: "$ sudo journalctl -u nginx --no-pager" },
  ])}

  <div class="callout-grid cols-3">
    ${calloutBox({ type: "tip", title: "TIPS", text: `<ul><li>Always check status before making changes.</li><li>Use <code>systemctl status &lt;service&gt;</code> to read logs and errors.</li></ul>` })}
    ${calloutBox({ type: "success", title: "BEST PRACTICE", text: `<ul><li>Enable only necessary services.</li><li>Keep your system clean and secure.</li></ul>` })}
    ${calloutBox({ type: "warning", title: "WARNING", text: "<p>Stopping critical services can cause your system or applications to fail.</p>" })}
  </div>`;
  return pageChrome(13, 20, "SYSTEMD", inner, "Always check status before making changes.");
}

// ---------------------------------------------------------------------------
// PAGE 14 — Installing and Managing Software
// ---------------------------------------------------------------------------
function page14Packages(): string {
  const inner = `
  ${titleHtml("INSTALLING AND<br>MANAGING SOFTWARE", "MANAGE PACKAGES, UPDATES AND DEPENDENCIES IN LINUX")}
  <div class="concept-grid cols-3">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.package, title: "What Is a Package?", bullets: ["A package is a pre-compiled software bundle.", "Contains the program and everything it needs to run.", "Includes files, libraries, dependencies and configuration."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.server, title: "Package Repositories", bullets: ["Repositories store packages.", "Your system connects to repos to download and update software.", "Official repos are tested and reliable."] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.gear, title: "Package Managers", body: `<div class="distro-row"><span class="distro">${ICON.ubuntu}apt · Debian/Ubuntu</span><span class="distro">${ICON.rhel}dnf · RHEL/Rocky</span><span class="distro">${ICON.rhel}yum · RHEL/CentOS 7</span></div>` })}
    ${conceptCard({ num: "4", tint: "gold", icon: ICON.gear, title: "What They Do", bullets: ["Install new software", "Update existing software", "Remove software", "Resolve dependencies automatically", "Keep system consistent and secure", "Save time and prevent manual dependency errors"] })}
    ${conceptCard({ num: "5", tint: "red", icon: ICON.warning, title: "Why Production Updates Require Care", bullets: ["Updates can introduce breaking changes.", "May affect application compatibility.", "Always test updates before applying.", "Use backups and maintenance windows.", "Read release notes.", "Update one system at a time."] })}
  </div>

  ${sectionHeader("6. Essential Package Management Commands")}
  ${dataTable({
    headers: ["TASK", "DEBIAN/UBUNTU (apt)", "RHEL/ROCKY (dnf)", "RHEL/CENTOS 7 (yum)"],
    monoCols: [1, 2, 3],
    rows: [
      ["Update package list", "<code>sudo apt update</code>", "<code>sudo dnf makecache</code>", "<code>sudo yum check-update</code>"],
      ["Install package", "<code>sudo apt install nginx</code>", "<code>sudo dnf install nginx</code>", "<code>sudo yum install nginx</code>"],
      ["Update packages", "<code>sudo apt upgrade</code>", "<code>sudo dnf upgrade</code>", "<code>sudo yum update</code>"],
      ["Remove package", "<code>sudo apt remove nginx</code>", "<code>sudo dnf remove nginx</code>", "<code>sudo yum remove nginx</code>"],
      ["Check installed", "<code>dpkg -l | less</code>", "<code>dnf list installed | less</code>", "<code>yum list installed | less</code>"],
      ["Search for package", "<code>apt search nginx</code>", "<code>dnf search nginx</code>", "<code>yum search nginx</code>"],
    ],
  })}

  ${sectionHeader("7. Practical: Install and Verify a Web Server Package (NGINX)")}
  ${stepsFlow([
    { n: "1", title: "UPDATE REPO LIST — Update the package index first", cmd: "$ sudo apt update    # or: sudo dnf makecache" },
    { n: "2", title: "INSTALL NGINX — Install the nginx web server", cmd: "$ sudo apt install nginx    # or: sudo dnf install nginx" },
    { n: "3", title: "START SERVICE — Start nginx immediately", cmd: "$ sudo systemctl start nginx" },
    { n: "4", title: "VERIFY STATUS — Check if nginx is running", cmd: "$ systemctl status nginx" },
    { n: "5", title: "TEST IN BROWSER — Open your server IP in a browser", cmd: "# http://<your-server-ip>\n# You should see the nginx welcome page." },
    { n: "6", title: "ENABLE AT BOOT — Enable nginx to start automatically", cmd: "$ sudo systemctl enable nginx" },
  ])}

  <div class="callout-grid cols-3">
    ${calloutBox({ type: "success", title: "BEST PRACTICE", text: "<p>Always update the package list before installing. Use <code>apt search</code> to find the correct package name.</p>" })}
    ${calloutBox({ type: "warning", title: "SECURITY", text: "<p>Only install packages from trusted repositories. Verify package integrity when possible.</p>" })}
    ${calloutBox({ type: "warning", title: "WARNING", text: "<p>Production updates can break applications. Always test in staging first.</p>" })}
  </div>`;
  return pageChrome(14, 20, "SOFTWARE MGMT", inner, "Always update the package list first.");
}

// ---------------------------------------------------------------------------
// PAGE 15 — Linux Networking Basics
// ---------------------------------------------------------------------------
function page15Networking(): string {
  const inner = `
  ${titleHtml("LINUX NETWORKING<br>BASICS", "THE ESSENTIAL NETWORKING SKILLS FOR EVERY LINUX ENGINEER")}
  <div class="concept-grid cols-4">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.target, title: "IP Addresses", body: "Every device on a network has an IP address.<br><b>IPv4 example:</b> <code>192.168.1.10</code>" })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.shield, title: "Private vs Public IP", body: "<b>PRIVATE IP (internal):</b> 10.0.0.0/8 · 172.16.0.0/12 · 192.168.0.0/16<br><b>PUBLIC IP (internet):</b> assigned by ISP or Cloud" })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.server, title: "Network Interfaces", body: "Linux uses interfaces to connect to networks.<br><b>Examples:</b> <code>eth0</code>, <code>ens33</code>, <code>enp0s3</code>, <code>ens5</code>" })}
    ${conceptCard({ num: "4", tint: "gold", icon: ICON.server, title: "Ports", body: "Ports identify services on a host.<br><b>Examples:</b> 22 (SSH) · 80 (HTTP) · 443 (HTTPS)" })}
    ${conceptCard({ num: "5", tint: "blue", icon: ICON.cloud, title: "DNS (Domain Name System)", body: "Converts domain names (e.g. <code>google.com</code>) to IP addresses. Without DNS, we must remember IPs." })}
    ${conceptCard({ num: "6", tint: "green", icon: ICON.server, title: "Default Gateway", body: "The gateway sends traffic to other networks and the internet. Usually your router IP address." })}
    ${conceptCard({ num: "7", tint: "purple", icon: ICON.terminal, title: "Common Tools", body: "<code>ip addr</code>, <code>ip route</code>, <code>ping</code>, <code>curl</code>, <code>ss</code>, <code>hostname</code>, <code>dig</code><br>These are your daily networking tools." })}
    ${conceptCard({ num: "8", tint: "gold", icon: ICON.list, title: "Common Examples", body: "Ping gateway: <code>ping 192.168.1.1</code><br>Ping internet: <code>ping 8.8.8.8</code><br>Check route: <code>ip route | grep default</code><br>Get public IP: <code>curl ifconfig.me</code>" })}
  </div>

  ${calloutBox({ type: "tip", title: "QUICK TIP", text: "<p>Most connectivity problems fall into four areas: <b>DNS</b>, <b>Network</b>, <b>Port</b>, or <b>Application</b>.</p>" })}

  ${sectionHeader("9. Networking Commands Cheat Sheet")}
  ${dataTable({
    headers: ["COMMAND", "PURPOSE", "EXAMPLE", "SAMPLE OUTPUT (MAY VARY)"],
    monoCols: [0, 2],
    rows: [
      ["ip addr", "Show IP addresses of all interfaces", "<code>ip addr</code>", "2: ens33: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt;<br>inet 192.168.1.10/24 brd 192.168.1.255 scope global ens33"],
      ["ip route", "Show routing table", "<code>ip route</code>", "default via 192.168.1.1 dev ens33<br>192.168.1.0/24 dev ens33 proto kernel scope link src 192.168.1.10"],
      ["ping", "Test connectivity to a host", "<code>ping 8.8.8.8</code>", "64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=20.1 ms"],
      ["curl", "Fetch data from a URL", "<code>curl -I https://google.com</code>", "HTTP/2 200<br>content-type: text/html; charset=UTF-8"],
      ["ss", "Show open ports and connections", "<code>ss -tulnp</code>", "LISTEN 0 128 0.0.0.0:22<br>LISTEN 0 128 0.0.0.0:80"],
      ["hostname", "Show or set system hostname", "<code>hostname</code>", "server01"],
      ["dig", "DNS lookup tool", "<code>dig google.com</code>", "google.com. 142 IN A 142.250.72.206"],
    ],
  })}

  ${sectionHeader("10. Practical: Diagnose Connectivity Problems")}
  ${dataTable({
    headers: ["STEP", "CHECK", "COMMAND", "WHAT TO LOOK FOR", "IF IT FAILS"],
    monoCols: [0, 2],
    rows: [
      ["1", "DNS Resolution", "<code>dig example.com</code>", "IP address in the ANSWER SECTION", "No IP: DNS problem (check DNS server or /etc/resolv.conf)"],
      ["2", "Network Connectivity", "<code>ping &lt;IP-address&gt;</code>", "Replies from the IP address", "No reply: Network problem (routing, firewall, or host down)"],
      ["3", "Port Reachability", "<code>ss -tulnp | grep :&lt;port&gt;</code>", "Port should be LISTENING", "Connection refused/timeout: port blocked or service not listening"],
      ["4", "Application Check", "<code>curl -I http://&lt;IP&gt;:&lt;port&gt;</code>", "HTTP response (200, 301, 403, etc.)", "No response or HTTP errors: application problem (config, service)"],
    ],
  })}

  <div class="callout-grid cols-2">
    ${calloutBox({ type: "note", title: "TROUBLESHOOTING FLOW", text: "<p><b>DNS → NETWORK → PORT → APPLICATION</b></p><p>Fix the first failure before moving to the next step.</p>" })}
    ${calloutBox({ type: "tip", title: "BEST PRACTICES", text: `<ul>
      <li>Always test DNS first.</li>
      <li>Then test network reachability.</li>
      <li>Then test the port.</li>
      <li>Finally test the application.</li>
      <li>Document findings and fix the root cause.</li>
    </ul>` })}
  </div>`;
  return pageChrome(15, 20, "NETWORKING", inner, "DNS → Network → Port → Application.");
}

// ---------------------------------------------------------------------------
// PAGE 16 — SSH and Remote Linux Servers
// ---------------------------------------------------------------------------
function page16SSH(): string {
  const inner = `
  ${titleHtml("SSH AND REMOTE<br>LINUX SERVERS", "CONNECT SECURELY, TRANSFER FILES, AND MANAGE REMOTE SERVERS")}
  <div class="concept-grid cols-2">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.lock, title: "What SSH Does", bullets: ["SSH (Secure Shell) provides secure encrypted communication over insecure networks.", "Replaces insecure protocols like Telnet and rlogin."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.server, title: "SSH Client and Server", bullets: ["<b>Client:</b> your local machine.", "<b>Server:</b> remote Linux server running SSH daemon (sshd).", "Default SSH port: <b>22/TCP</b>."] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.terminal, title: "ssh user@server", body: "<b>Basic syntax:</b> <code>ssh user@server_ip</code><br>Connects to the server as the specified user.<br><b>Example:</b> <code>ssh ubuntu@192.168.1.10</code>", cmds: [{ cmd: "$ ssh ubuntu@192.168.1.10" }] })}
    ${conceptCard({ num: "4", tint: "gold", icon: ICON.lock, title: "Password Authentication", bullets: ["The simplest method.", "You enter the user password when connecting.", "Less secure than key-based authentication."] })}
    ${conceptCard({ num: "5", tint: "blue", icon: ICON.key, title: "SSH Keys", bullets: ["More secure and recommended.", "Uses asymmetric cryptography.", "No password needed after setup."] })}
    ${conceptCard({ num: "6", tint: "green", icon: ICON.key, title: "Public vs Private Keys", body: "<b>PUBLIC KEY:</b> stored on the server. Shared.<br><b>PRIVATE KEY:</b> stored on your local machine. Never shared." })}
    ${conceptCard({ num: "7", tint: "purple", icon: ICON.terminal, title: "ssh-keygen", body: "Generates a key pair.<br><b>Default location:</b> <code>~/.ssh/id_rsa</code><br><code>id_rsa</code> → private key · <code>id_rsa.pub</code> → public key", cmds: [{ cmd: "$ ssh-keygen -t rsa -b 4096" }] })}
    ${conceptCard({ num: "8", tint: "gold", icon: ICON.book, title: "authorized_keys", body: "The server stores your public key in: <code>~/.ssh/authorized_keys</code><br>Allows key-based login. Permissions are critical." })}
    ${conceptCard({ num: "9", tint: "blue", icon: ICON.folder, title: "scp (Secure Copy)", body: "Securely copy files between local and remote systems. Uses SSH for encryption.<br><b>Syntax:</b> <code>scp file user@server:/path</code>" })}
    ${conceptCard({ num: "10", tint: "red", icon: ICON.shield, title: "Secure Key Permissions", body: "Keep keys private!", cmds: [{ cmd: "$ chmod 600 ~/.ssh/id_rsa\n$ chmod 700 ~/.ssh\n$ chmod 644 ~/.ssh/id_rsa.pub" }] })}
  </div>

  ${sectionHeader("11. Essential SSH Commands")}
  ${dataTable({
    headers: ["COMMAND", "PURPOSE", "EXAMPLE", "DESCRIPTION"],
    monoCols: [0, 2],
    rows: [
      ["ssh user@server", "Connect to remote server", "<code>ssh ubuntu@192.168.1.10</code>", "Connect using default port 22."],
      ["ssh -p PORT user@server", "Connect using custom port", "<code>ssh -p 2222 ubuntu@server</code>", "Use when SSH runs on a custom port."],
      ["scp source user@server:/path", "Copy file to remote server", "<code>scp file.txt ubuntu@server:/home/ubuntu/</code>", "Upload file to server."],
      ["scp user@server:/path dest", "Copy file from remote server", "<code>scp ubuntu@server:/etc/hosts ./</code>", "Download file from server."],
      ["ssh-keygen -t rsa -b 4096", "Generate SSH key pair", "<code>ssh-keygen -t rsa -b 4096</code>", "Recommended: 4096-bit RSA."],
      ["ssh-copy-id user@server", "Copy public key to server", "<code>ssh-copy-id ubuntu@server</code>", "Automatically adds key to authorized_keys."],
      ["ssh -i ~/.ssh/id_rsa user@server", "Connect with specific key", "<code>ssh -i ~/.ssh/id_rsa ubuntu@server</code>", "Use a different private key."],
      ["ssh -v user@server", "Verbose connection (debug)", "<code>ssh -v ubuntu@server</code>", "Shows detailed connection info."],
    ],
  })}

  ${sectionHeader("12. Practical: Connect to a Remote Server and Transfer a File Securely")}
  ${stepsFlow([
    { n: "1", title: "GENERATE KEYS — Create a key pair on your local machine", cmd: "$ ssh-keygen -t rsa -b 4096" },
    { n: "2", title: "COPY PUBLIC KEY — Copy your public key to the server", cmd: "$ ssh-copy-id user@server" },
    { n: "3", title: "TEST SSH LOGIN — Login without password", cmd: "$ ssh user@server" },
    { n: "4", title: "CHECK CONNECTION — Verify you are connected", cmd: "$ hostname\n$ whoami" },
    { n: "5", title: "UPLOAD FILE — Transfer file to the server", cmd: "$ scp file.txt user@server:/tmp/" },
    { n: "6", title: "VERIFY FILE — Check file on the server", cmd: "$ ls -l /tmp/file.txt" },
    { n: "7", title: "DOWNLOAD FILE — Download file from server", cmd: "$ scp user@server:/tmp/file.txt ." },
    { n: "8", title: "CLEAN UP — Remove test file (optional)", cmd: "$ rm /tmp/file.txt" },
  ])}

  <div class="callout-grid cols-3">
    ${calloutBox({ type: "note", title: "COMMON SSH FILES", text: `<ul>
      <li><code>~/.ssh/</code> — SSH directory</li>
      <li><code>~/.ssh/id_rsa</code> — Private key</li>
      <li><code>~/.ssh/id_rsa.pub</code> — Public key</li>
      <li><code>~/.ssh/authorized_keys</code> — Authorized public keys (server)</li>
      <li><code>/etc/ssh/sshd_config</code> — SSH server config</li>
    </ul>` })}
    ${calloutBox({ type: "success", title: "BEST PRACTICES", text: `<ul>
      <li>Always use key-based authentication.</li>
      <li>Use strong passphrases for your keys.</li>
      <li>Keep private keys private.</li>
      <li>Disable password authentication on servers.</li>
      <li>Change SSH port from 22 (optional).</li>
      <li>Keep your SSH software updated.</li>
    </ul>` })}
    ${calloutBox({ type: "warning", title: "TROUBLESHOOTING TIPS", text: `<ul>
      <li><b>Permission denied (publickey):</b> check key permissions.</li>
      <li><b>Connection refused:</b> SSH service may not be running.</li>
      <li><b>Timeout:</b> check network, firewall, or IP address.</li>
      <li>Use <code>ssh -v user@server</code> for detailed logs.</li>
      <li>Ensure port 22 (or custom port) is open.</li>
    </ul>` })}
  </div>`;
  return pageChrome(16, 20, "SSH & REMOTE", inner, "Always use key-based authentication.");
}

// ---------------------------------------------------------------------------
// PAGE 17 — Storage and Disk Management
// ---------------------------------------------------------------------------
function page17Storage(): string {
  const inner = `
  ${titleHtml("STORAGE AND<br>DISK MANAGEMENT", "MANAGE DISKS, FILESYSTEMS AND SPACE LIKE A PRO")}
  <div class="concept-grid cols-2">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.database, title: "Filesystems", bullets: ["A filesystem defines how data is stored and organized on disk.", "Common Linux filesystems: <code>ext4</code>, <code>xfs</code>, <code>btrfs</code>.", "Each filesystem has its own features and limits."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.server, title: "Disks and Partitions", bullets: ["A disk (e.g. <code>/dev/sda</code>) can have multiple partitions (e.g. <code>/dev/sda1</code>).", "Each partition can hold a filesystem."] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.folder, title: "Mount Points", bullets: ["A mount point is a directory where a filesystem is attached to the directory tree.", "Example: <code>/</code>, <code>/home</code>, <code>/var</code>, <code>/data</code> are mount points."] })}
    ${conceptCard({ num: "5", tint: "gold", icon: ICON.book, title: "Understanding /etc/fstab", body: "Controls which filesystems are mounted at boot.<br><b>Format:</b> <code>&lt;device&gt; &lt;mount_point&gt; &lt;filesystem&gt; &lt;options&gt; &lt;dump&gt; &lt;pass&gt;</code><br>Use <code>sudo mount -a</code> to test without rebooting. Bad fstab entries can prevent the system from booting." })}
    ${conceptCard({ num: "6", tint: "red", icon: ICON.warning, title: "Disk-Space Troubleshooting", bullets: ["Run out of space in: <code>/</code>, <code>/var</code>, <code>/home</code>, <code>/tmp</code>, or <code>/data</code>.", "Find what is using the most space.", "Clean old logs, caches, temporary files.", "Move or archive data if needed."] })}
    ${conceptCard({ num: "7", tint: "blue", icon: ICON.magnifier, title: "Finding Large Files and Directories", body: "Find what is consuming the most space.", cmds: [{ cmd: "# Top 10 largest files under /var\n$ sudo find /var -type f -exec du -h {} + | sort -rh | head -10", out: "# Top 10 largest directories under /var\n$ sudo du -ah /var 2>/dev/null | sort -rh | head -10" }] })}
  </div>

  ${sectionHeader("4. Key Commands Quick Reference")}
  ${dataTable({
    headers: ["COMMAND", "PURPOSE", "EXAMPLE"],
    monoCols: [0, 2],
    rows: [
      ["df -h", "Show filesystem disk space", "<code>df -h</code>"],
      ["du -sh &lt;dir&gt;", "Show directory size", "<code>du -sh /var</code>"],
      ["du -ah &lt;dir&gt; | sort -h", "Find large files/dirs", "<code>du -ah /var | sort -h</code>"],
      ["lsblk", "List block devices", "<code>lsblk</code>"],
      ["mount", "Show mounted filesystems", "<code>mount</code>"],
      ["mount &lt;device&gt; &lt;dir&gt;", "Mount a filesystem", "<code>mount /dev/sdb1 /data</code>"],
      ["/etc/fstab", "Persistent mounts at boot", "<code>cat /etc/fstab</code>"],
    ],
  })}

  ${sectionHeader("Command Examples")}
  ${termBlock("Check disk usage of all filesystems", [
    "$ df -h",
    "Filesystem      Size  Used Avail Use% Mounted on",
    "/dev/sda1        50G   42G  6.5G  87% /",
    "tmpfs           1.9G  1.2M  1.9G   1% /run",
    "/dev/sda2       100G   20G   75G  22% /home",
  ])}
  ${termBlock("Find size of /var directory", [
    "$ du -sh /var",
    "14G    /var",
  ])}
  ${termBlock("List block devices", [
    "$ lsblk",
    "NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS",
    "sda      8:0    0   150G  0 disk",
    "├─sda1   8:1    0    50G  0 part /",
    "├─sda2   8:2    0   100G  0 part /home",
    "sdb      8:16   0   200G  0 disk",
    "└─sdb1   8:17   0   200G  0 part /data",
  ])}
  ${termBlock("/etc/fstab example", [
    "# <device>      <mount point>  <type>  <options>     <dump> <pass>",
    "UUID=1234-5678  /              ext4    defaults      1      1",
    "UUID=abcd-efgh  /home          ext4    defaults      1      2",
    "/dev/sdb1       /data          xfs     defaults      1      2",
    "tmpfs           /tmp           tmpfs   defaults      0      0",
  ])}

  ${calloutBox({ type: "tip", title: "TIP", text: "<p>Check log files, old application data, backups, docker data and caches.</p>" })}`;
  return pageChrome(17, 20, "STORAGE & DISKS", inner, "Use df -h and du -sh daily to monitor disk space.");
}

// ---------------------------------------------------------------------------
// PAGE 18 — Linux Logs and Troubleshooting
// ---------------------------------------------------------------------------
function page18Logs(): string {
  const inner = `
  ${titleHtml("LINUX LOGS AND<br>TROUBLESHOOTING", "FIND ISSUES FAST. READ LOGS SMART.")}
  <div class="concept-grid cols-2">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.list, title: "Why Linux Logs Matter", bullets: ["Logs tell you what happened, when it happened and why.", "Essential for troubleshooting, security and auditing.", "Everything is a file in Linux — including logs."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.folder, title: "/var/log Directory", bullets: ["Stores system, service and application logs.", "Different logs for different purposes.", "Text files you can read and search."] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.terminal, title: "journalctl (System Logs)", body: "Reads systemd journal logs. Includes boot logs and service logs. Powerful filtering options.", cmds: [{ cmd: "$ journalctl", desc: "View all logs" }, { cmd: "$ journalctl -b", desc: "View logs since boot" }, { cmd: "$ journalctl -u nginx", desc: "View logs for a service" }, { cmd: "$ journalctl -f", desc: "Follow logs in real-time" }] })}
    ${conceptCard({ num: "4", tint: "gold", icon: ICON.terminal, title: "dmesg (Kernel Ring Buffer)", body: "Shows kernel messages. Hardware detection, drivers and boot issues. Very useful for system startup problems.", cmds: [{ cmd: "$ dmesg", desc: "Show all kernel messages" }, { cmd: "$ dmesg | tail -50", desc: "Show last 50 kernel messages" }, { cmd: "$ dmesg -w", desc: "Live kernel messages" }] })}
    ${conceptCard({ num: "5", tint: "blue", icon: ICON.book, title: "tail -f (Follow Logs)", body: "Watches a log file in real time. Great for live troubleshooting. Updates as new lines are written.", cmds: [{ cmd: "$ tail -f /var/log/syslog", desc: "Follow a log file" }, { cmd: "$ tail -f /var/log/nginx/error.log", desc: "Follow service log" }] })}
    ${conceptCard({ num: "6", tint: "red", icon: ICON.magnifier, title: "Searching Logs with grep", body: "Find text, errors or warnings. Case-sensitive by default. Use <code>-i</code> for ignore case. Combine with tail, cat or journalctl.", cmds: [{ cmd: "$ grep \"error\" /var/log/syslog" }, { cmd: "$ grep -i \"failed\" /var/log/syslog" }, { cmd: "$ tail -f /var/log/syslog | grep --line-buffered \"error\"" }] })}
    ${conceptCard({ num: "9", tint: "purple", icon: ICON.list, title: "Reading Errors Systematically", bullets: ["Read the latest entries first.", "Look for ERROR, FAIL, DENIED, WARN.", "Check timestamps.", "Follow the flow of events.", "Cross-check related logs."] })}
  </div>

  <div class="body cols-2">
    <div>
      ${sectionHeader("7. Service Logs (Examples)")}
      ${dataTable({
        headers: ["SERVICE", "LOG FILE"],
        monoCols: [0, 1],
        rows: [
          ["nginx", "/var/log/nginx/error.log"],
          ["apache2", "/var/log/apache2/error.log"],
          ["sshd", "/var/log/secure or /var/log/auth.log"],
          ["mysql", "/var/log/mysql/error.log"],
          ["docker", "journalctl -u docker"],
          ["systemd services", "journalctl -u &lt;service-name&gt;"],
        ],
      })}
    </div>
    <div>
      ${sectionHeader("8. Authentication Logs")}
      ${dataTable({
        headers: ["PURPOSE", "LOG FILE"],
        monoCols: [1],
        rows: [
          ["Auth events", "/var/log/auth.log (Debian/Ubuntu)"],
          ["Auth events", "/var/log/secure (RHEL/CentOS/Rocky)"],
          ["Failed logins", "/var/log/faillog"],
          ["Last logins", "/var/log/lastlog"],
        ],
      })}
    </div>
  </div>

  ${sectionHeader("10. Practical: Investigate Why a Service Failed to Start")}
  ${stepsFlow([
    { n: "1", title: "Check service status", cmd: "$ systemctl status <service-name>", out: "# Check if the service failed to start." },
    { n: "2", title: "Look for the reason in the logs", cmd: "$ journalctl -u <service-name> --no-pager" },
    { n: "3", title: "Filter logs for errors or fails", cmd: "$ journalctl -u <service-name> | grep -i \"error|fail|denied\"" },
    { n: "4", title: "Check system, auth or app logs", cmd: "$ tail -n 100 /var/log/syslog /var/log/auth.log" },
    { n: "5", title: "Restart and confirm service is running", cmd: "$ sudo systemctl restart <service-name>\n$ systemctl status <service-name>" },
  ])}

  <div class="callout-grid cols-3">
    ${calloutBox({ type: "tip", title: "TIP", text: `<ul>
      <li>Identify the problem.</li>
      <li>Check the relevant log files.</li>
      <li>Look for errors or warnings.</li>
      <li>Understand the cause.</li>
      <li>Fix the issue.</li>
      <li>Verify and monitor.</li>
    </ul>` })}
    ${calloutBox({ type: "success", title: "BEST PRACTICE", text: "<p>Use <code>journalctl -u &lt;service&gt; -f</code> to follow a service's logs in real time during restart.</p>" })}
    ${calloutBox({ type: "warning", title: "WARNING", text: "<p>Always read logs from the bottom up — latest events are at the end. Check timestamps!</p>" })}
  </div>`;
  return pageChrome(18, 20, "LOGS & DEBUG", inner, "journalctl + grep + tail -f = your debugging toolkit.");
}

// ---------------------------------------------------------------------------
// PAGE 19 — Environment Variables and Shell Basics
// ---------------------------------------------------------------------------
function page19EnvVars(): string {
  const inner = `
  ${titleHtml("ENVIRONMENT VARIABLES<br>AND SHELL BASICS", "CONTROL YOUR ENVIRONMENT. AUTOMATE YOUR WORK.")}
  <div class="concept-grid cols-3">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.terminal, title: "What the Shell Does", bullets: ["The shell is a program that reads your commands.", "It interprets and executes them.", "It is your interface to Linux.", "It can run programs, scripts and built-ins."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.terminal, title: "bash", bullets: ["Bash (Bourne Again Shell) is the most common shell on Linux.", "Configuration file: <code>~/.bashrc</code>", "Run <code>echo $SHELL</code> to see your current shell."] })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.gear, title: "Environment Variables", bullets: ["Variables store information.", "Environment variables are available to the shell and child processes.", "They control how your system behaves."] })}
    ${conceptCard({ num: "4", tint: "gold", icon: ICON.terminal, title: "echo", body: "Displays text or the value of a variable.", cmds: [{ cmd: "$ echo Hello Linux", out: "Hello Linux" }, { cmd: "$ echo $USER", out: "ubuntu" }] })}
    ${conceptCard({ num: "5", tint: "blue", icon: ICON.list, title: "env", body: "Prints all environment variables.", cmds: [{ cmd: "$ env", out: "USER=ubuntu\nHOME=/home/ubuntu\nPATH=/usr/local/bin:/usr/bin:/bin\nSHELL=/bin/bash" }] })}
    ${conceptCard({ num: "6", tint: "green", icon: ICON.terminal, title: "export", body: "Creates or updates an environment variable.", cmds: [{ cmd: "$ export MYVAR=\"DevOps\"" }, { cmd: "$ echo $MYVAR", out: "DevOps" }] })}
    ${conceptCard({ num: "7", tint: "purple", icon: ICON.folder, title: "$PATH", body: "Tells the shell where to look for executable commands.", cmds: [{ cmd: "$ echo $PATH", out: "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" }] })}
    ${conceptCard({ num: "8", tint: "gold", icon: ICON.book, title: ".bashrc", body: "Runs every time you open a new terminal. Put your custom variables, aliases and settings here. Location: <code>~/.bashrc</code>.", cmds: [{ cmd: "$ nano ~/.bashrc", out: "export DEVOPS=\"Awesome\"\nexport PATH=\"$PATH:/opt/mybin\"" }, { cmd: "$ source ~/.bashrc" }] })}
    ${conceptCard({ num: "9", tint: "blue", icon: ICON.gear, title: "Shell Variables", body: "Variables created by you (not always exported).", cmds: [{ cmd: "$ NAME=\"Linux\"" }, { cmd: "$ echo $NAME", out: "Linux" }] })}
    ${conceptCard({ num: "10", tint: "green", icon: ICON.terminal, title: "Command Substitution", body: "Run a command inside <code>$()</code> and use its output.", cmds: [{ cmd: "$ TODAY=$(date +%Y-%m-%d)" }, { cmd: "$ echo \"Today is $TODAY\"", out: "Today is 2024-05-11" }] })}
    ${conceptCard({ num: "11", tint: "purple", icon: ICON.terminal, title: "Quoting Basics", body: "<b>\"Double quotes\"</b>: expand variables.<br><code>$ echo \"Path: $PATH\"</code><br><b>'Single quotes'</b>: do NOT expand variables.<br><code>$ echo 'Path: $PATH'</code><br><b>'Backticks' (legacy)</b>: same as $() but older." })}
    ${conceptCard({ num: "12", tint: "gold", icon: ICON.list, title: "Useful Built-in Commands", body: "See table below." })}
  </div>

  ${sectionHeader("Useful Built-in Commands")}
  ${dataTable({
    headers: ["Command", "Description"],
    monoCols: [0],
    rows: [
      ["pwd", "Print working directory"],
      ["cd", "Change directory"],
      ["type &lt;cmd&gt;", "Show how a command is interpreted"],
      ["which &lt;cmd&gt;", "Show full path of command"],
      ["alias", "List aliases"],
      ["unalias &lt;name&gt;", "Remove alias"],
    ],
  })}

  ${sectionHeader("13. Practical: Create an Environment Variable and Understand How Linux Locates Executable Commands")}
  ${stepsFlow([
    { n: "1", title: "CREATE DIRECTORY — Create a custom bin directory", cmd: "$ mkdir -p ~/mybin" },
    { n: "2", title: "CREATE SCRIPT — Create a simple script", cmd: "$ nano ~/mybin/hello.sh\n#!/bin/bash\necho 'Hello Linux!'\n$ chmod +x ~/mybin/hello.sh" },
    { n: "3", title: "RUN WITH FULL PATH", cmd: "$ ~/mybin/hello.sh", out: "Hello Linux!" },
    { n: "4", title: "ADD TO PATH", cmd: "$ export PATH=\"$PATH:~/mybin\"\n$ echo $PATH", out: ".../home/ubuntu/mybin" },
    { n: "5", title: "RUN BY COMMAND NAME", cmd: "$ hello.sh", out: "Hello Linux!" },
    { n: "6", title: "PERSISTENT PATH", cmd: "$ echo 'export PATH=\"$PATH:~/mybin\"' >> ~/.bashrc\n$ source ~/.bashrc" },
  ])}

  ${termBlock("Verify how Linux locates commands", [
    "$ which hello.sh",
    "/home/ubuntu/mybin/hello.sh",
    "$ type hello.sh",
    "hello.sh is /home/ubuntu/mybin/hello.sh",
  ])}`;
  return pageChrome(19, 20, "ENV & SHELL", inner, "Add custom scripts to $PATH via ~/.bashrc.");
}

// ---------------------------------------------------------------------------
// PAGE 20 — Your First Bash Script
// ---------------------------------------------------------------------------
function page20BashScript(): string {
  const inner = `
  ${titleHtml("YOUR FIRST<br>BASH SCRIPT", "AUTOMATE TASKS. SAVE TIME. SOLVE REAL PROBLEMS.")}
  <div class="concept-grid cols-2">
    ${conceptCard({ num: "1", tint: "blue", icon: ICON.lightbulb, title: "What Shell Scripting Solves", bullets: ["Automate repetitive tasks.", "Combine commands.", "Reduce human error.", "Monitor and report system status.", "Save time and increase consistency."] })}
    ${conceptCard({ num: "2", tint: "green", icon: ICON.terminal, title: "Shebang (#!)", body: "The shebang tells Linux which interpreter to use. Always the first line.<br><b>Most common:</b> <code>#!/bin/bash</code>" })}
    ${conceptCard({ num: "3", tint: "purple", icon: ICON.gear, title: "Variables", body: "Store data for later use. No spaces around <code>=</code> sign. Use <code>$</code> to access.", cmds: [{ cmd: "NAME=\"Linux\"\nCOUNT=10\necho \"Hello $NAME\"" }] })}
    ${conceptCard({ num: "4", tint: "gold", icon: ICON.terminal, title: "User Input", body: "Accept input from users. Use <code>read</code> command.", cmds: [{ cmd: "echo -n \"Enter your name: \"\nread USER\necho \"Hello $USER\"" }] })}
    ${conceptCard({ num: "5", tint: "blue", icon: ICON.list, title: "If Statements", body: "Make decisions in scripts. Use <code>if</code>, <code>elif</code>, <code>else</code>, <code>fi</code>.", cmds: [{ cmd: "if [ \"$DISK\" -gt 90 ]; then\n  echo \"Disk is full!\"\nelse\n  echo \"Disk is OK\"\nfi" }] })}
    ${conceptCard({ num: "6", tint: "red", icon: ICON.list, title: "Exit Codes", body: "Every command returns an exit status. <b>0 = Success</b>, <b>Non-zero = Error</b>.", cmds: [{ cmd: "command\necho $?   # Check last command status\nexit 1   # Exit with error code" }] })}
    ${conceptCard({ num: "7", tint: "green", icon: ICON.gear, title: "Simple Loops", body: "Repeat tasks easily. Common loop: <code>for</code>.", cmds: [{ cmd: "for i in 1 2 3 4 5; do\n  echo \"Count: $i\"\ndone" }] })}
    ${conceptCard({ num: "8", tint: "purple", icon: ICON.lock, title: "Make Scripts Executable", body: "Scripts need execute permission to run. Use <code>chmod +x</code>.", cmds: [{ cmd: "chmod +x myscript.sh\nls -l myscript.sh" }] })}
    ${conceptCard({ num: "9", tint: "gold", icon: ICON.terminal, title: "Running Scripts", body: "Run using <code>./script.sh</code> or <code>bash script.sh</code>. Current directory needs <code>./</code> prefix.", cmds: [{ cmd: "./myscript.sh\nbash myscript.sh" }] })}
    ${conceptCard({ num: "10", tint: "blue", icon: ICON.shield, title: "Basic Error Handling", body: "Check for errors and handle them. Use exit codes and conditions. Always validate important commands.", cmds: [{ cmd: "if [ $? -ne 0 ]; then\n  echo \"Error: Command failed!\"\n  exit 1\nfi" }] })}
  </div>

  ${sectionHeader("Quick Reference")}
  ${dataTable({
    headers: ["TOPIC", "EXAMPLE"],
    monoCols: [1],
    rows: [
      ["Shebang", "<code>#!/bin/bash</code>"],
      ["Variable", "<code>NAME=\"Linux\"</code>"],
      ["User Input", "<code>read INPUT</code>"],
      ["If Statement", "<code>if [ \"$A\" -eq \"$B\" ]; then</code>"],
      ["For Loop", "<code>for i in {1..5}; do echo $i; done</code>"],
      ["Make Executable", "<code>chmod +x script.sh</code>"],
      ["Run Script", "<code>./script.sh</code>"],
      ["Exit with Error", "<code>exit 1</code>"],
    ],
  })}

  ${sectionHeader("Practical: A Real-World health_check.sh Script")}
  ${termBlock("health_check.sh", [
    "#!/bin/bash",
    "",
    "# Health Check Script",
    "",
    "DISK=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')",
    "MEM=$(free | awk '/Mem:/ {printf \"%.0f\", $3/$2 * 100}')",
    "UPTIME=$(uptime -p)",
    'SERVICE="nginx"',
    "",
    'echo "======== SERVER HEALTH CHECK ========"',
    'echo "Disk Usage       : ${DISK}%"',
    'echo "Memory Usage     : ${MEM}%"',
    'echo "Uptime           : ${UPTIME}"',
    "if systemctl is-active --quiet $SERVICE; then",
    '  echo "${SERVICE} Status : RUNNING (OK)"',
    "  exit 0",
    "else",
    '  echo "${SERVICE} Status : NOT RUNNING (ERROR)"',
    "  exit 1",
    "fi",
  ])}

  ${sectionHeader("Execution Steps")}
  ${stepsFlow([
    { n: "1", title: "Make script executable", cmd: "$ chmod +x health_check.sh" },
    { n: "2", title: "Run the script", cmd: "$ ./health_check.sh" },
    { n: "3", title: "Success output", cmd: "# ======== SERVER HEALTH CHECK ========\n# Disk Usage       : 42%\n# Memory Usage     : 38%\n# Uptime           : up 2 days, 3 hours\n# nginx Status : RUNNING (OK)" },
    { n: "4", title: "Error output (if nginx is down)", cmd: "# ======== SERVER HEALTH CHECK ========\n# nginx Status : NOT RUNNING (ERROR)\n$ echo $?\n1" },
  ])}

  <div class="callout-grid cols-3">
    ${calloutBox({ type: "success", title: "BEST PRACTICE", text: "<p>Always start scripts with a shebang. Use exit codes to signal success (0) or failure (non-zero).</p>" })}
    ${calloutBox({ type: "tip", title: "TIP", text: "<p>Test scripts in a safe directory first. Use <code>set -e</code> to stop on errors in critical scripts.</p>" })}
    ${calloutBox({ type: "warning", title: "WARNING", text: "<p>Always validate user input. Never trust untrusted input in commands — escape variables with quotes.</p>" })}
  </div>`;
  return pageChrome(20, 20, "BASH SCRIPTING", inner, "Automate everything. Start small, build up.");
}

// ---------------------------------------------------------------------------
// MAIN — assemble all pages and write the HTML
// ---------------------------------------------------------------------------
const pages: string[] = [
  page1Cover(),
  page2LinuxFromZero(),
  page3Filesystem(),
  page4MovingAround(),
  page5FileMgmt(),
  page6ReadingEditing(),
  page7UsersGroups(),
  page8Permissions(),
  page9Sudo(),
  page10Finding(),
  page11Pipes(),
  page12Processes(),
  page13Systemd(),
  page14Packages(),
  page15Networking(),
  page16SSH(),
  page17Storage(),
  page18Logs(),
  page19EnvVars(),
  page20BashScript(),
];

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Linux for Complete Beginners — A Practical Notebook</title>
<style>${CSS}</style>
</head>
<body>
${pages.join("\n")}
</body>
</html>
`;

const __dirname = dirname(fileURLToPath(import.meta.url));
const outPath = resolve(__dirname, "..", "public", "uploads", "linux-for-beginners.html");
writeFileSync(outPath, html);
console.log(`Generated ${outPath} with ${pages.length} pages`);
