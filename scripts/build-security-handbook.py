#!/usr/bin/env python3
"""Build the complete 20-page Linux Security Handbook HTML.
Reads OCR text from /tmp/all_pages_ocr.json, strips VERIQTA branding,
extracts real content, and emits a self-contained notebook-style HTML.
"""
import json
from pathlib import Path

OUT = Path("/home/z/my-project/public/uploads/linux-security-handbook.html")
CSS_HEAD = Path("/tmp/security-css-head.html").read_text() + "\n</head>"

# ============================================================
# ICON LIBRARY — small inline SVGs used across pages
# ============================================================
def ic_shield(c="#16a34a"):
    return f'<svg viewBox="0 0 24 24"><path d="M12 2L3 6v6c0 5 3.5 8.5 9 10 5.5-1.5 9-5 9-10V6l-9-4z" fill="{c}"/><path d="M9 12l2 2 4-4" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def ic_lock(c="#2563eb"):
    return f'<svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2" fill="{c}"/><path d="M8 11V8a4 4 0 0 1 8 0v3" stroke="{c}" stroke-width="2.5" fill="none"/><circle cx="12" cy="16" r="1.5" fill="#fff"/></svg>'

def ic_user(c="#2563eb"):
    return f'<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" fill="{c}"/><path d="M4 20c0-4 4-7 8-7s8 3 8 7" fill="{c}"/></svg>'

def ic_users(c="#16a34a"):
    return f'<svg viewBox="0 0 24 24"><circle cx="9" cy="9" r="3.5" fill="{c}"/><circle cx="16" cy="10" r="2.8" fill="{c}" opacity="0.7"/><path d="M3 19c0-3.3 2.7-6 6-6s6 2.7 6 6" fill="{c}"/><path d="M14 19c0-2.5 1.8-4.5 4-4.5s4 2 4 4.5" fill="{c}" opacity="0.7"/></svg>'

def ic_file(c="#2563eb"):
    return f'<svg viewBox="0 0 24 24"><path d="M6 2h8l4 4v16H6z" fill="#eff6ff" stroke="{c}" stroke-width="1.5"/><path d="M14 2v4h4" fill="#dbeafe"/></svg>'

def ic_folder(c="#d4a017"):
    return f'<svg viewBox="0 0 24 24"><path d="M3 6.5h5.5l1.7 2H21v10.5a1.5 1.5 0 0 1-1.5 1.5H4.5A1.5 1.5 0 0 1 3 19z" fill="{c}"/></svg>'

def ic_key(c="#16a34a"):
    return f'<svg viewBox="0 0 24 24"><circle cx="8" cy="8" r="5" fill="{c}"/><path d="M11 11l8 8M16 16l2-2M18 18l2-2" stroke="{c}" stroke-width="2.5" stroke-linecap="round"/><circle cx="8" cy="8" r="2" fill="#fff"/></svg>'

def ic_term(c="#1e293b"):
    return f'<svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2" fill="{c}"/><path d="M6 9l3 3-3 3M12 15h4" stroke="#22c55e" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def ic_gear(c="#7c3aed"):
    return f'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.5" fill="none" stroke="{c}" stroke-width="2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2" stroke="{c}" stroke-width="2" stroke-linecap="round"/></svg>'

def ic_search(c="#dc2626"):
    return f'<svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="{c}" stroke-width="2.2"/><line x1="15.5" y1="15.5" x2="20" y2="20" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/></svg>'

def ic_eye(c="#7c3aed"):
    return f'<svg viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="{c}"/></svg>'

def ic_server(c="#2563eb"):
    return f'<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="6" rx="1" fill="{c}"/><rect x="3" y="14" width="18" height="6" rx="1" fill="{c}" opacity="0.7"/><circle cx="6" cy="7" r="1" fill="#fff"/><circle cx="6" cy="17" r="1" fill="#fff"/></svg>'

def ic_globe(c="#2563eb"):
    return f'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="2"/><ellipse cx="12" cy="12" rx="4" ry="9" fill="none" stroke="{c}" stroke-width="2"/><line x1="3" y1="12" x2="21" y2="12" stroke="{c}" stroke-width="2"/></svg>'

def ic_book(c="#d4a017"):
    return f'<svg viewBox="0 0 24 24"><path d="M4 4h7v15H4z" fill="none" stroke="{c}" stroke-width="1.6"/><path d="M13 4h7v15h-7z" fill="none" stroke="{c}" stroke-width="1.6"/><line x1="6" y1="8" x2="9" y2="8" stroke="{c}" stroke-width="1.3"/><line x1="6" y1="11" x2="9" y2="11" stroke="{c}" stroke-width="1.3"/><line x1="15" y1="8" x2="18" y2="8" stroke="{c}" stroke-width="1.3"/><line x1="15" y1="11" x2="18" y2="11" stroke="{c}" stroke-width="1.3"/></svg>'

def ic_clock(c="#7c3aed"):
    return f'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5" fill="none" stroke="{c}" stroke-width="1.7"/><path d="M12 7v5l3.5 2" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round"/></svg>'

def ic_warn(c="#dc2626"):
    return f'<svg viewBox="0 0 24 24"><path d="M12 2L2 21h20z" fill="{c}"/><rect x="11" y="9" width="2" height="6" fill="#fff"/><circle cx="12" cy="18" r="1" fill="#fff"/></svg>'

def ic_check(c="#16a34a"):
    return f'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="{c}"/><path d="M7 12l3 3 7-7" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def ic_ban(c="#dc2626"):
    return f'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="2.5"/><line x1="6" y1="6" x2="18" y2="18" stroke="{c}" stroke-width="2.5" stroke-linecap="round"/></svg>'

def ic_database(c="#2563eb"):
    return f'<svg viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="8" ry="3" fill="{c}"/><path d="M4 5v6c0 1.5 3.5 3 8 3s8-1.5 8-3V5" fill="{c}" opacity="0.7"/><path d="M4 11v6c0 1.5 3.5 3 8 3s8-1.5 8-3v-6" fill="{c}" opacity="0.5"/></svg>'

def ic_pkg(c="#16a34a"):
    return f'<svg viewBox="0 0 24 24"><path d="M12 2L3 6v6c0 5 3.5 8.5 9 10 5.5-1.5 9-5 9-10V6l-9-4z" fill="none" stroke="{c}" stroke-width="1.8"/><rect x="9" y="9" width="6" height="6" fill="{c}"/></svg>'

def ic_audit(c="#7c3aed"):
    return f'<svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="1.5" fill="none" stroke="{c}" stroke-width="1.8"/><line x1="8" y1="8" x2="16" y2="8" stroke="{c}" stroke-width="1.5"/><line x1="8" y1="12" x2="16" y2="12" stroke="{c}" stroke-width="1.5"/><line x1="8" y1="16" x2="13" y2="16" stroke="{c}" stroke-width="1.5"/></svg>'

def ic_bug(c="#dc2626"):
    return f'<svg viewBox="0 0 24 24"><ellipse cx="12" cy="13" rx="5" ry="6" fill="{c}"/><line x1="9" y1="6" x2="8" y2="3" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/><line x1="15" y1="6" x2="16" y2="3" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/><line x1="3" y1="11" x2="7" y2="11" stroke="{c}" stroke-width="1.5"/><line x1="3" y1="15" x2="7" y2="15" stroke="{c}" stroke-width="1.5"/><line x1="17" y1="11" x2="21" y2="11" stroke="{c}" stroke-width="1.5"/><line x1="17" y1="15" x2="21" y2="15" stroke="{c}" stroke-width="1.5"/></svg>'

def ic_flag(c="#dc2626"):
    return f'<svg viewBox="0 0 24 24"><path d="M5 21V3h11l-2 4 2 4H5" fill="{c}"/></svg>'

def ic_chain(c="#2563eb"):
    return f'<svg viewBox="0 0 24 24"><path d="M9 15l6-6" stroke="{c}" stroke-width="2" stroke-linecap="round"/><rect x="3" y="9" width="8" height="6" rx="3" fill="none" stroke="{c}" stroke-width="2"/><rect x="13" y="9" width="8" height="6" rx="3" fill="none" stroke="{c}" stroke-width="2"/></svg>'

def ic_doc(c="#1e293b"):
    return f'<svg viewBox="0 0 24 24"><rect x="2.5" y="4" width="19" height="16" rx="2.2" fill="#0d1117"/><rect x="2.5" y="4" width="19" height="3" rx="2.2" fill="#1c2230"/><circle cx="5" cy="5.5" r="0.6" fill="#ff5f56"/><circle cx="6.8" cy="5.5" r="0.6" fill="#ffbd2e"/><circle cx="8.6" cy="5.5" r="0.6" fill="#27c93f"/><path d="M6 11 L9 13.5 L6 16" fill="none" stroke="#7ee787" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><line x1="11" y1="16" x2="17" y2="16" stroke="#e6edf3" stroke-width="1.6" stroke-linecap="round"/></svg>'

def ic_hash(c="#2563eb"):
    return f'<svg viewBox="0 0 24 24"><line x1="9" y1="3" x2="6" y2="21" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/><line x1="18" y1="3" x2="15" y2="21" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/><line x1="3" y1="9" x2="21" y2="9" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/><line x1="3" y1="15" x2="21" y2="15" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/></svg>'

def ic_target(c="#dc2626"):
    return f'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="1.8"/><circle cx="12" cy="12" r="6" fill="none" stroke="{c}" stroke-width="1.8"/><circle cx="12" cy="12" r="3" fill="{c}"/></svg>'

def ic_bolt(c="#d4a017"):
    return f'<svg viewBox="0 0 24 24"><path d="M13 2L4 14h6l-1 8 9-12h-6z" fill="{c}"/></svg>'

def ic_puzzle(c="#7c3aed"):
    return f'<svg viewBox="0 0 24 24"><path d="M9 3h6v3a3 3 0 0 0 3 3 3 3 0 0 0 3-3h0v6h-3a3 3 0 0 0-3 3 3 3 0 0 0 3 3v3H9v-3a3 3 0 0 0-3-3 3 3 0 0 0-3 3H3v-6h3a3 3 0 0 0 3-3 3 3 0 0 0-3-3H3V3h6z" fill="none" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/></svg>'

# Color map
BLUE = "#2563eb"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
RED = "#dc2626"
GOLD = "#d4a017"
NAVY = "#15264d"

# ============================================================
# Component builders
# ============================================================
def wrap_page(num, body_html, ch_badge="CH", ch_label=""):
    """Wrap a body in the standard page-wrapper / page structure."""
    badge_alt = ch_label if ch_label else f"CH {num-1:02d}"
    pg = f"{num:02d} / 20"
    return f'''<div class="page-wrapper">
  <div class="holes" aria-hidden="true"></div>
  <div class="spiral" aria-hidden="true"></div>
  <div class="page-bend" aria-hidden="true"></div>
  <section class="page">
    <div class="page-top-edge" aria-hidden="true"></div>
    <div class="page-bottom-edge" aria-hidden="true"></div>
    <div class="content">
      <div class="top-strip">
        <div class="badges">
          <span class="badge green">LINUX SECURITY</span>
          <span class="badge alt">{badge_alt}</span>
          <span class="badge">PAGE {pg}</span>
        </div>
      </div>
{body_html}
      <div class="page-footer">
        <span class="src">Linux Security Handbook</span>
        <span class="tip">Secure Today. Protect Tomorrow.</span>
        <span class="pg">{pg}</span>
      </div>
    </div>
  </section>
</div>
'''

def title_block(title_text, subtitle, title_class="title"):
    return f'''      <div class="title-block">
        <h1 class="{title_class}">{title_text}</h1>
        <div class="subtitle">{subtitle}</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>'''

def concept_card(icon_svg, bg_class, title, body_html):
    return f'''      <div class="concept-card">
        <div class="ch">
          <span class="icn-mini {bg_class}" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:10px;flex-shrink:0;">{icon_svg}</span>
          <h3>{title}</h3>
        </div>
        <div class="body-text">{body_html}</div>
      </div>'''

def section_h(title, pill=None):
    pill_html = f'<span class="pill">{pill}</span>' if pill else ''
    return f'''      <div class="section-h">
        <span class="bar"></span>
        <h4>{title}</h4>
        {pill_html}
      </div>'''

def callout(kind, icon_svg, h5, body_html):
    return f'''      <div class="callout {kind}">
        <div class="icn">{icon_svg}</div>
        <div class="ct">
          <h5>{h5}</h5>
          {body_html}
        </div>
      </div>'''

def term_block(title, body_lines):
    """title appears in the term-head; body_lines is a list of strings (already HTML-formatted)."""
    body = "\n".join(body_lines)
    return f'''        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">{title}</span></div>
          <pre class="term-body">{body}</pre>
        </div>'''

def cmd_card(ic_bg, icon_svg, name, desc, term_html):
    return f'''        <div class="cmd-card">
          <div class="ic {ic_bg}">{icon_svg}</div>
          <div class="body-text">
            <h4>{name}</h4>
            <div class="desc">{desc}</div>
            <div class="term">{term_html}</div>
          </div>
        </div>'''

def data_table(headers, rows, mono_cols=None):
    """rows: list of row tuples; mono_cols: 0-indexed list of columns that should be code."""
    mono_cols = mono_cols or []
    th = "".join(f"<th>{h}</th>" for h in headers)
    body_rows = []
    for r in rows:
        tds = []
        for i, cell in enumerate(r):
            cls = ' class="mono"' if i in mono_cols else ''
            tds.append(f"<td{cls}>{cell}</td>")
        body_rows.append("<tr>" + "".join(tds) + "</tr>")
    return f'''        <table class="data-table">
          <thead><tr>{th}</tr></thead>
          <tbody>{"".join(body_rows)}</tbody>
        </table>'''

def steps_flow(steps):
    """steps: list of dicts {n, title, term_html}."""
    out = ['      <div class="steps-flow">']
    for s in steps:
        out.append(f'''        <div class="step">
          <div class="n">{s['n']}</div>
          <div class="bd">
            <div class="t">{s['title']}</div>
            <div class="term">{s['term']}</div>
          </div>
        </div>''')
    out.append('      </div>')
    return "\n".join(out)

# ============================================================
# PAGES
# ============================================================
def page_01_cover():
    return f'''<div class="page-wrapper">
  <div class="holes" aria-hidden="true"></div>
  <div class="spiral" aria-hidden="true"></div>
  <div class="page-bend" aria-hidden="true"></div>
  <section class="page">
    <div class="page-top-edge" aria-hidden="true"></div>
    <div class="page-bottom-edge" aria-hidden="true"></div>
    <div class="content">
      <div class="top-strip">
        <div class="badges">
          <span class="badge green">LINUX SECURITY</span>
          <span class="badge alt">HANDBOOK</span>
          <span class="badge">PAGE 01 / 20</span>
        </div>
      </div>
      <div class="cover">
        <span class="super">FROM LINUX HARDENING</span>
        <h1 class="title-big">LINUX SECURITY</h1>
        <div class="title-sub-wrap"><span class="hline"></span><div class="title-sub">HANDBOOK</div><span class="hline"></span></div>
        <div class="sub-box">
          <div class="sub-text">FROM LINUX HARDENING TO<br>PRODUCTION SECURITY</div>
        </div>
        <div style="display:flex;gap:14px;margin-top:24px;flex-wrap:wrap;justify-content:center;">
          <div style="text-align:center;"><div style="width:52px;height:52px;border-radius:12px;background:#cfe0ff;display:flex;align-items:center;justify-content:center;margin:0 auto 4px;">{ic_lock(BLUE)}</div><span style="font-size:10px;font-weight:700;color:#2563eb;">ACCESS CONTROL</span></div>
          <div style="text-align:center;"><div style="width:52px;height:52px;border-radius:12px;background:#cdf3da;display:flex;align-items:center;justify-content:center;margin:0 auto 4px;">{ic_key(GREEN)}</div><span style="font-size:10px;font-weight:700;color:#16a34a;">AUTHENTICATION</span></div>
          <div style="text-align:center;"><div style="width:52px;height:52px;border-radius:12px;background:#e2d4ff;display:flex;align-items:center;justify-content:center;margin:0 auto 4px;">{ic_shield(PURPLE)}</div><span style="font-size:10px;font-weight:700;color:#7c3aed;">FIREWALL</span></div>
          <div style="text-align:center;"><div style="width:52px;height:52px;border-radius:12px;background:#fce9b6;display:flex;align-items:center;justify-content:center;margin:0 auto 4px;">{ic_audit(GOLD)}</div><span style="font-size:10px;font-weight:700;color:#d4a017;">FILE PERMISSIONS</span></div>
          <div style="text-align:center;"><div style="width:52px;height:52px;border-radius:12px;background:#ffd4d4;display:flex;align-items:center;justify-content:center;margin:0 auto 4px;">{ic_shield(RED)}</div><span style="font-size:10px;font-weight:700;color:#dc2626;">HARDENING</span></div>
          <div style="text-align:center;"><div style="width:52px;height:52px;border-radius:12px;background:#eef1f5;display:flex;align-items:center;justify-content:center;margin:0 auto 4px;">{ic_eye(NAVY)}</div><span style="font-size:10px;font-weight:700;color:#15264d;">MONITORING</span></div>
        </div>
        <div style="margin-top:28px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;width:100%;max-width:880px;">
          <div style="background:#fff;border:2px solid var(--linux-green);border-radius:12px;padding:14px 12px;text-align:center;"><div style="font-size:32px;font-weight:900;color:var(--linux-green);">20</div><div style="font-size:10px;font-weight:700;letter-spacing:1.2px;color:var(--ink-2);text-transform:uppercase;margin-top:4px;">CHAPTERS</div></div>
          <div style="background:#fff;border:2px solid var(--linux-green);border-radius:12px;padding:14px 12px;text-align:center;"><div style="font-size:32px;font-weight:900;color:var(--linux-green);">100+</div><div style="font-size:10px;font-weight:700;letter-spacing:1.2px;color:var(--ink-2);text-transform:uppercase;margin-top:4px;">COMMANDS</div></div>
          <div style="background:#fff;border:2px solid var(--linux-green);border-radius:12px;padding:14px 12px;text-align:center;"><div style="font-size:32px;font-weight:900;color:var(--linux-green);">50+</div><div style="font-size:10px;font-weight:700;letter-spacing:1.2px;color:var(--ink-2);text-transform:uppercase;margin-top:4px;">TIPS</div></div>
          <div style="background:#fff;border:2px solid var(--linux-green);border-radius:12px;padding:14px 12px;text-align:center;"><div style="font-size:32px;font-weight:900;color:var(--linux-green);">1</div><div style="font-size:10px;font-weight:700;letter-spacing:1.2px;color:var(--ink-2);text-transform:uppercase;margin-top:4px;">GOAL · SECURE</div></div>
        </div>
        <div class="callout tip" style="margin-top:24px;">
          <div class="icn">{ic_shield(GREEN)}</div>
          <div class="ct">
            <h5>SECURE TODAY. PROTECT TOMORROW.</h5>
            <p>HARDEN &nbsp;·&nbsp; DETECT &nbsp;·&nbsp; PROTECT &nbsp;·&nbsp; RECOVER. Secure systems, find threats, stop attacks, recover fast — for DevOps engineers, system administrators, and security professionals.</p>
          </div>
        </div>
      </div>
      <div class="page-footer">
        <span class="src">Linux Security Handbook</span>
        <span class="tip">Secure Today. Protect Tomorrow.</span>
        <span class="pg">01 / 20</span>
      </div>
    </div>
  </section>
</div>
'''

def page_02_foundations():
    body = f'''      <div class="title-block">
        <h1 class="title long">1. LINUX SECURITY FOUNDATIONS</h1>
        <div class="subtitle">STRONG LINUX SECURITY STARTS WITH UNDERSTANDING THE FUNDAMENTALS OF HOW SYSTEMS, USERS, PROCESSES, AND NETWORKS INTERACT</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="body cols-2">
{concept_card(ic_shield(BLUE), "bg-blue", "Linux Security Layers", "Linux security is built in multiple layers including the kernel, system services, filesystem, users, and network. <strong>Every component interacts. Securing each layer reduces risk across the entire system.</strong>")}
{concept_card(ic_user(BLUE), "bg-blue", "Authentication vs Authorization", "<strong>Authentication</strong> verifies who you are.<br><strong>Authorization</strong> determines what you are allowed to do.<br>Both must be configured correctly.")}
{concept_card(ic_lock(BLUE), "bg-blue", "Least Privilege", "Users, services, and processes should have only the minimum permissions required to perform their tasks. <strong>Limit access. Reduce risk.</strong>")}
{concept_card(ic_target(RED), "bg-red", "Attack Surface", "Any point that can be used to attack your system. <strong>Reduce exposed services, open ports, and unnecessary access</strong> to shrink the attack surface.")}
{concept_card(ic_shield(GREEN), "bg-green", "Defense in Depth", "No single control is perfect. Use multiple layers of security so that if one layer fails, other layers continue to protect the system.")}
{concept_card(ic_eye(GREEN), "bg-green", "Security Baseline vs Monitoring", "A strong baseline sets the foundation. <strong>Continuous monitoring detects changes, threats, and abnormal behavior early.</strong>")}
      </div>
      <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-top:14px;">
        <div class="callout tip">
          <div class="icn">{ic_check(GREEN)}</div>
          <div class="ct">
            <h5>KEY TAKEAWAY</h5>
            <p>Strong Linux security starts with understanding the fundamentals of how systems, users, processes, and networks interact. <strong>Users, processes, files, services, and network boundaries</strong> — every component must be secured.</p>
          </div>
        </div>
        <div class="callout note">
          <div class="icn">{ic_book(GOLD)}</div>
          <div class="ct">
            <h5>SCOPE</h5>
            <p>From Linux hardening to production security.</p>
          </div>
        </div>
      </div>'''
    return wrap_page(2, body, ch_label="FOUNDATIONS")

def page_03_users():
    # Key Account Files table
    files_table = data_table(
        ["FILE", "PURPOSE"],
        [
            ("/etc/passwd", "Stores user account information including username, UID, GID, home directory, and default shell."),
            ("/etc/shadow", "Stores encrypted passwords and password aging information. Access is restricted to the root user."),
            ("/etc/group", "Stores group information including GID and member list."),
        ],
        mono_cols=[0]
    )
    # Key Management Commands table
    cmds_table = data_table(
        ["COMMAND", "DESCRIPTION"],
        [
            ("id", "Show user and group identity information."),
            ("getent", "Query user and group database."),
            ("passwd", "Manage user passwords."),
            ("usermod", "Modify user account properties."),
            ("chage", "Manage password aging and expiry."),
        ],
        mono_cols=[0]
    )
    body = f'''      <div class="title-block">
        <h1 class="title long">2. USERS, GROUPS, AND IDENTITY SECURITY</h1>
        <div class="subtitle">MANAGE ACCESS, PERMISSIONS, AND OWNERSHIP IN LINUX SYSTEMS</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="body cols-2">
{concept_card(ic_users(BLUE), "bg-blue", "Local Users & System Accounts", "Linux uses local users and system accounts to manage access and ownership. <strong>System accounts usually have low UIDs and no login shell.</strong>")}
{concept_card(ic_hash(GREEN), "bg-green", "UID and GID Security", "Every user and group has a unique UID and GID. <strong>Protect UID 0 (root) and other privileged IDs.</strong>")}
{concept_card(ic_search(RED), "bg-red", "Detecting Unexpected Accounts", "Regularly check for <strong>unknown or suspicious user accounts and groups</strong> in /etc/passwd, /etc/shadow, and /etc/group.")}
{concept_card(ic_lock(RED), "bg-red", "Locking & Disabling Accounts", "Lock or disable <strong>unused or compromised accounts</strong> to prevent unauthorized access. Use usermod -L, passwd -l, or usermod -e 1.")}
{concept_card(ic_shield(GOLD), "bg-gold", "Reviewing Privileged Users", "Review users with UID 0 and sudo access. <strong>Limit privileged access to only what is necessary.</strong>")}
{concept_card(ic_key(GREEN), "bg-green", "Key Management Commands", "Use Linux commands to inspect and manage users, groups, and account settings. These files form the foundation for identity security — <strong>protect them carefully.</strong>")}
      </div>
{section_h("Key Account Files", "PROTECT")}
      <div style="display:grid;grid-template-columns:1.4fr 1fr;gap:14px;">
        <div>
          {files_table}
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div class="callout warning">
            <div class="icn">{ic_lock(RED)}</div>
            <div class="ct">
              <h5>PROTECT /etc/shadow</h5>
              <p>Mode 640, owner root, group shadow. Never world-readable.</p>
            </div>
          </div>
          <div class="callout note">
            <div class="icn">{ic_file(BLUE)}</div>
            <div class="ct">
              <h5>OWNERSHIP</h5>
              <p>These three files form the foundation of identity security on every Linux system.</p>
            </div>
          </div>
        </div>
      </div>
{section_h("Key Management Commands", "INSPECT")}
{cmds_table}'''
    return wrap_page(3, body, ch_label="IDENTITY")

def page_04_passwords():
    cmds_table = data_table(
        ["COMMAND", "DESCRIPTION"],
        [
            ("chage -l &lt;user&gt;", "Display password aging information."),
            ("chage -M 90 &lt;user&gt;", "Set password expiration (days)."),
            ("chage -E 2025-12-31 &lt;user&gt;", "Set account expiration date."),
            ("pam-config", "Manage PAM configuration."),
            ('grep "failed password" /var/log/auth.log', "View failed login attempts."),
            ("lastlog", "Check last login time for all users."),
            ("passwd -S &lt;user&gt;", "Show password status."),
            ("usermod -L &lt;user&gt;", "Lock user account."),
            ("usermod -e 1 &lt;user&gt;", "Expire user account immediately."),
        ],
        mono_cols=[0]
    )
    body = f'''      <div class="title-block">
        <h1 class="title long">3. PASSWORD AND ACCOUNT SECURITY</h1>
        <div class="subtitle">ENFORCE STRONG PASSWORD POLICIES AND ACCOUNT LIFECYCLE CONTROLS</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-3">
{concept_card(ic_clock(BLUE), "bg-blue", "Password Aging", "Defines the minimum number of days before a password can be changed again. <strong>Prevents frequent and weak password changes.</strong>")}
{concept_card(ic_clock(GREEN), "bg-green", "Password Expiration", "Forces users to change passwords after a specified number of days. <strong>Reduces risk from compromised passwords.</strong>")}
{concept_card(ic_ban(RED), "bg-red", "Account Expiration", "Sets an expiration date for user accounts. <strong>Prevents unused or unnecessary accounts from remaining active.</strong>")}
{concept_card(ic_lock(PURPLE), "bg-purple", "PAM Password Policies", "Pluggable Authentication Modules (PAM) enforce password strength, complexity, and reuse rules. Configured in <code>/etc/pam.d/</code> and <code>/etc/security/</code>.")}
{concept_card(ic_warn(RED), "bg-red", "Failed Authentication", "Limit and monitor failed login attempts. <strong>Helps prevent brute-force and password guessing attacks.</strong>")}
{concept_card(ic_user(NAVY), "bg-neutral", "Dormant Accounts", "Accounts that have not been used for a long time increase risk. <strong>Identify and disable or remove dormant accounts.</strong>")}
{concept_card(ic_lock(GOLD), "bg-gold", "Login Restrictions", "Restrict login access by time, source IP, or TTY. Enhances security for privileged and system accounts.")}
{concept_card(ic_eye(GREEN), "bg-green", "Reviewing Password Status", "Regularly review password aging, expiration, and account status. <strong>Use tools to ensure policies are enforced.</strong>")}
{concept_card(ic_key(GREEN), "bg-green", "Secure Service-Account Practices", "Use strong, long passwords or keys for service accounts. <strong>Restrict permissions and avoid interactive logins.</strong>")}
      </div>
{section_h("Password & Account Management Commands", "USE")}
{cmds_table}
      <div class="callout warning" style="margin-top:14px;">
        <div class="icn">{ic_warn(RED)}</div>
        <div class="ct">
          <h5>PRODUCTION RULE</h5>
          <p>Enforce minimum password length (12+), complexity, rotation (90 days max), history (last 5), and lockout after 5 failed attempts. <strong>Never share passwords. Never reuse root credentials across systems.</strong></p>
        </div>
      </div>'''
    return wrap_page(4, body, ch_label="PASSWORDS")

def page_05_permissions():
    perm_table = data_table(
        ["PERMISSION", "NUMBER", "SYMBOL"],
        [
            ("READ", "4", "r"),
            ("WRITE", "2", "w"),
            ("EXECUTE", "1", "x"),
        ]
    )
    example_rows = [
        ("FILE", "script.sh", "-rw-r--r--", "644"),
        ("FILE", "application.log", "-rw-rw----", "660"),
        ("DIRECTORY", "/var/www", "drwxr-xr-x", "755"),
        ("DIRECTORY", "/data", "drwx------", "700"),
    ]
    examples_table = data_table(
        ["TYPE", "NAME", "SYMBOLIC", "NUMERIC"],
        example_rows,
        mono_cols=[1, 2, 3]
    )
    cmds_table = data_table(
        ["COMMAND", "DESCRIPTION"],
        [
            ("ls -l", "List files with permissions."),
            ("namei -l /path/to/file", "Show full path permissions."),
            ("stat file.txt", "Detailed file information."),
            ("find / -type f -perm -o+w", "Find world-writable files."),
            ("find / -type d -perm -002", "Find world-writable directories."),
        ],
        mono_cols=[0]
    )
    body = f'''      <div class="title-block">
        <h1 class="title long">4. FILE AND DIRECTORY PERMISSIONS</h1>
        <div class="subtitle">CONTROL WHO CAN READ, WRITE, AND EXECUTE FILES AND DIRECTORIES</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="body cols-2-uneven">
        <div>
{section_h("Permission Model")}
          <div class="concept-grid">
{concept_card(ic_users(BLUE), "bg-blue", "Owner, Group, Other", "Every file and directory has three types of access: <strong>Owner (user), Group, and Other (everyone else)</strong>. Permissions control what each can do.")}
{concept_card(ic_eye(GREEN), "bg-green", "Read, Write, Execute", "<strong>R (read):</strong> View file contents or list directory.<br><strong>W (write):</strong> Modify file or create/delete in directory.<br><strong>X (execute):</strong> Run file or access directory.")}
{concept_card(ic_hash(PURPLE), "bg-purple", "Numeric & Symbolic", "<strong>Numeric:</strong> Use numbers (0–7) to represent permissions.<br><strong>Symbolic:</strong> Use letters (r, w, x) to set permissions.<br>Example: <code>755 = rwxr-xr-x</code>")}
{concept_card(ic_lock(GOLD), "bg-gold", "chmod, chown, chgrp", "<strong>chmod:</strong> Change file or directory permissions.<br><strong>chown:</strong> Change file or directory owner.<br><strong>chgrp:</strong> Change file or directory group.")}
          </div>
{section_h("Directory Permission Behavior")}
          <div class="callout note">
            <div class="icn">{ic_folder(GOLD)}</div>
            <div class="ct">
              <h5>HOW DIRECTORIES BEHAVE</h5>
              <ul>
                <li><strong>Read (r):</strong> List files in the directory.</li>
                <li><strong>Write (w):</strong> Create, delete, or rename files.</li>
                <li><strong>Execute (x):</strong> Enter and access the directory.</li>
                <li><strong>Without x, you cannot access files inside.</strong></li>
              </ul>
            </div>
          </div>
{section_h("umask & Dangerous Permissions")}
          <div class="concept-grid">
{concept_card(ic_gear(BLUE), "bg-blue", "umask", "The umask sets default permissions for new files and directories. It determines what permissions are removed by default. Check with: <code>umask</code>")}
{concept_card(ic_warn(RED), "bg-red", "Finding Dangerous Permissions", "Look for world-writable files and directories. Use tools to find risky permissions. <strong>Example:</strong> chmod 777 or writable system files. <code>find / -type f -perm -002 -ls</code>")}
          </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div class="callout warning">
            <div class="icn">{ic_warn(RED)}</div>
            <div class="ct">
              <h5>PRODUCTION MISTAKES</h5>
              <ul>
                <li>Using 777 permissions.</li>
                <li>Making sensitive files world-readable.</li>
                <li>Incorrect ownership of application files.</li>
                <li>Writable permissions on critical system directories.</li>
                <li>Ignoring umask settings.</li>
              </ul>
            </div>
          </div>
          <div class="callout success">
            <div class="icn">{ic_check(GREEN)}</div>
            <div class="ct">
              <h5>SAFE DEFAULTS</h5>
              <p>Files: <code>644</code>. Dirs: <code>755</code>. Secrets: <code>600</code>. Private dirs: <code>700</code>.</p>
            </div>
          </div>
        </div>
      </div>
{section_h("Permission Reference", "NUMERIC")}
      <div style="display:grid;grid-template-columns:1fr 1.5fr;gap:14px;">
        <div>
          {perm_table}
        </div>
        <div>
          {examples_table}
        </div>
      </div>
{section_h("Quick Check Commands", "INSPECT")}
{cmds_table}'''
    return wrap_page(5, body, ch_label="PERMISSIONS")

def page_06_suid():
    special_table = data_table(
        ["TYPE", "MODE", "DESCRIPTION"],
        [
            ("SUID", "4xxx", "Run as file owner."),
            ("SGID", "2xxx", "Run as group owner."),
            ("STICKY", "1xxx", "Restricted deletion."),
            ("ACLs", "—", "Extended permissions."),
        ],
        mono_cols=[0, 1]
    )
    acl_term = '''<span class="pmt">$</span> getfacl /path/to/file
<span class="cmt"># View ACLs</span>
<span class="pmt">$</span> setfacl -m u:user:rw /path/to/file
<span class="cmt"># Add ACL entry</span>
<span class="pmt">$</span> setfacl -x u:user /path/to/file
<span class="cmt"># Remove ACL entry</span>
<span class="pmt">$</span> setfacl -b /path/to/file
<span class="cmt"># Remove all ACLs</span>'''
    find_term = '''<span class="cmt"># Find all SUID files</span>
<span class="pmt">$</span> find / -type f \\( -perm -4000 \\) \\
    -exec ls -l {{}} \\; 2&gt;/dev/null
<span class="cmt"># Find all SGID files</span>
<span class="pmt">$</span> find / -type f \\( -perm -2000 \\) \\
    -exec ls -l {{}} \\; 2&gt;/dev/null
<span class="cmt"># Find SUID and SGID in common paths</span>
<span class="pmt">$</span> find /bin /sbin /usr/bin /usr/sbin \\
    /usr/local/bin -type f \\( -perm -4000 \\
    -o -perm -2000 \\) -ls 2&gt;/dev/null'''
    body = f'''      <div class="title-block">
        <h1 class="title long">5. SUID, SGID, STICKY BIT, AND ACLs</h1>
        <div class="subtitle">SPECIAL PERMISSIONS THAT GRANT ELEVATED OR FINE-GRAINED ACCESS</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_key(PURPLE), "bg-purple", "SUID Executables", "When a file has the SUID bit set, it runs with the permissions of the file owner (usually root). <strong>Risk:</strong> Can be abused to gain elevated privileges. Check SUID files regularly.")}
{concept_card(ic_users(BLUE), "bg-blue", "SGID Files & Directories", "<strong>SGID on files:</strong> Runs with the group owner's privileges. <strong>SGID on directories:</strong> New files inherit the directory's SGID group ownership. Helps in controlled group collaboration.")}
{concept_card(ic_lock(GREEN), "bg-green", "Sticky Bit", "On directories, only the file owner, directory owner, or root can delete or rename files. <strong>Common on /tmp</strong> to prevent users from deleting each other's files.")}
{concept_card(ic_chain(PURPLE), "bg-purple", "Access Control Lists (ACLs)", "Provide fine-grained permissions beyond the traditional user/group/other model. Useful for granting access to specific users <strong>without changing ownership</strong>.")}
{concept_card(ic_eye(GREEN), "bg-green", "getfacl and setfacl", "<strong>getfacl:</strong> View ACLs on files and directories.<br><strong>setfacl:</strong> Modify ACLs for fine-grained access.<br><strong>ACLs override standard permissions.</strong>")}
{concept_card(ic_search(RED), "bg-red", "Searching for SUID/SGID Binaries", "Regularly search for SUID/SGID files to detect unexpected privilege escalation paths. <strong>New or unknown files can be a security risk.</strong>")}
{concept_card(ic_warn(RED), "bg-red", "Unexpected Privilege Paths", "Attackers exploit misconfigured SUID/SGID files or writable paths to escalate privileges. <strong>Always verify owner, permissions, and purpose.</strong>")}
{concept_card(ic_audit(GOLD), "bg-gold", "Auditing Special Permissions", "Maintain an inventory of all special permission files. Review regularly and document approved exceptions. <strong>Remove unnecessary permissions immediately.</strong>")}
      </div>
{section_h("Special Permission Types", "REFERENCE")}
{special_table}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;">
        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">Find SUID/SGID Files</span></div>
          <pre class="term-body">{find_term}</pre>
        </div>
        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">ACL Commands Examples</span></div>
          <pre class="term-body">{acl_term}</pre>
        </div>
      </div>
      <div class="callout tip" style="margin-top:14px;">
        <div class="icn">{ic_check(GREEN)}</div>
        <div class="ct">
          <h5>AUDIT CHECKLIST</h5>
          <ul>
            <li>Review all SUID, SGID, and Sticky files.</li>
            <li>Verify file purpose and ownership.</li>
            <li>Ensure directories with SGID are required.</li>
            <li>Check ACLs for unnecessary access.</li>
            <li>Document approved exceptions.</li>
            <li>Remove or fix unnecessary entries.</li>
          </ul>
        </div>
      </div>'''
    return wrap_page(6, body, ch_label="SUID/SGID")

def page_07_sudo():
    cmd_table = data_table(
        ["COMMAND", "DESCRIPTION"],
        [
            ("sudo -l", "List allowed sudo commands for current user."),
            ("sudo -ll", "List all privileges in detail."),
            ("sudo -u &lt;user&gt; &lt;command&gt;", "Run command as another user."),
            ("visudo", "Edit /etc/sudoers safely."),
            ("visudo -f /etc/sudoers.d/&lt;file&gt;", "Edit a file in sudoers.d directory."),
            ("sudo -k", "Invalidate password timestamp (next sudo will ask password)."),
            ("sudo -v", "Refresh the sudo timestamp (extend login session)."),
        ],
        mono_cols=[0]
    )
    body = f'''      <div class="title-block">
        <h1 class="title long">6. SUDO AND PRIVILEGE ESCALATION SECURITY</h1>
        <div class="subtitle">CONTROL, RESTRICT, AND AUDIT ROOT-LEVEL ACCESS ON LINUX</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="body cols-2-uneven">
        <div>
{section_h("Root Access & Sudo Configuration")}
          <div class="concept-grid">
{concept_card(ic_warn(RED), "bg-red", "Root Access Risks", "Root has unlimited power on the system. <strong>A single mistake or compromise can lead to full system takeover.</strong> Limit and monitor root access carefully.")}
{concept_card(ic_file(BLUE), "bg-blue", "/etc/sudoers", "Main sudo configuration file. Controls which users or groups can run which commands as root or another user. <strong>Always edit with visudo, never a text editor.</strong>")}
{concept_card(ic_folder(GOLD), "bg-gold", "/etc/sudoers.d/", "Directory for additional sudo configuration files. Used to add custom rules without modifying the main sudoers file. <strong>Each file is included automatically.</strong>")}
{concept_card(ic_lock(GREEN), "bg-green", "visudo", "Safe way to edit sudoers files. <strong>Syntax is checked before saving.</strong> Prevents locking yourself out of sudo access. Always use: <code>visudo</code> or <code>visudo -f &lt;file&gt;</code>")}
{concept_card(ic_key(GREEN), "bg-green", "Command-Specific Sudo", "Grant users access to only the commands they need. <strong>Example:</strong> Allow restart of specific services without full root access. Reduces the attack surface.")}
{concept_card(ic_ban(RED), "bg-red", "Dangerous Configurations", "Avoid broad permissions and wildcard commands. <strong>Dangerous:</strong> <code>ALL=(ALL) ALL</code>, <code>ALL=(ALL) NOPASSWD: ALL</code>, command wildcards like <code>/bin/*</code>. These can lead to full privilege escalation.")}
{concept_card(ic_warn(GOLD), "bg-gold", "NOPASSWD Risks", "NOPASSWD allows running commands without entering a password. If misconfigured, <strong>attackers can escalate privileges without any authentication.</strong> Use only when absolutely necessary.")}
{concept_card(ic_audit(PURPLE), "bg-purple", "Reviewing Sudo Privileges", "Regularly review who has sudo access and what they can run. <strong>Remove unused or excessive privileges.</strong> Use audit logs to monitor sudo activity.")}
{concept_card(ic_shield(GREEN), "bg-green", "Least-Privilege Administration", "Grant only the minimum access required. Remove elevated access when not needed. Use groups, command restrictions, and logging to enforce least-privilege principles.")}
          </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div class="callout warning">
            <div class="icn">{ic_warn(RED)}</div>
            <div class="ct">
              <h5>NEVER DO</h5>
              <ul>
                <li><code>ALL=(ALL) NOPASSWD: ALL</code></li>
                <li>Wildcard commands (<code>/bin/*</code>)</li>
                <li>Edit sudoers without <code>visudo</code></li>
                <li>Grant sudo to shared accounts</li>
              </ul>
            </div>
          </div>
          <div class="callout success">
            <div class="icn">{ic_check(GREEN)}</div>
            <div class="ct">
              <h5>SUDO SECURITY CHECKLIST</h5>
              <ul>
                <li>Limit users with sudo access.</li>
                <li>Use command-specific permissions.</li>
                <li>Avoid NOPASSWD unless required.</li>
                <li>Do not use wildcards carelessly.</li>
                <li>Review /etc/sudoers regularly.</li>
                <li>Audit sudo usage in logs.</li>
                <li>Remove unnecessary privileges.</li>
                <li>Use least-privilege principles.</li>
                <li>Test configurations before deployment.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
{section_h("Sudo Command Examples", "USE")}
{cmd_table}'''
    return wrap_page(7, body, ch_label="SUDO")

def page_08_ssh():
    sshd_settings = data_table(
        ["SETTING", "VALUE"],
        [
            ("Port", "22"),
            ("Protocol", "2"),
            ("PermitRootLogin", "no"),
            ("PasswordAuthentication", "no"),
            ("ChallengeResponseAuthentication", "no"),
            ("UsePAM", "yes"),
            ("AllowUsers", "user1 user2"),
            ("AllowGroups", "sshusers"),
            ("X11Forwarding", "no"),
            ("MaxAuthTries", "3"),
            ("LoginGraceTime", "30s"),
            ("ClientAliveInterval", "300"),
            ("ClientAliveCountMax", "2"),
        ],
        mono_cols=[0, 1]
    )
    keygen_term = '''<span class="pmt">$</span> ssh-keygen -t ed25519 -C "your_email@domain.com" \\
    -f ~/.ssh/id_ed25519'''
    copy_term = '''<span class="cmt"># Copy public key to server</span>
<span class="pmt">$</span> cat ~/.ssh/id_ed25519.pub | ssh user@server_ip \\
    "mkdir -p ~/.ssh && cat &gt;&gt; ~/.ssh/authorized_keys"'''
    validate_term = '''<span class="cmt"># If no output, configuration is valid</span>
<span class="pmt">$</span> sshd -t
<span class="cmt"># Reload SSH service</span>
<span class="pmt">$</span> sudo systemctl reload sshd
<span class="cmt"># Or restart if necessary</span>
<span class="pmt">$</span> sudo systemctl restart sshd'''
    log_term = '''<span class="pmt">$</span> sudo journalctl -u ssh --since "1 hour ago"
<span class="pmt">$</span> sudo grep "sshd" /var/log/auth.log
<span class="pmt">$</span> sudo grep "Failed password" /var/log/auth.log'''
    body = f'''      <div class="title-block">
        <h1 class="title">7. SSH SERVER HARDENING</h1>
        <div class="subtitle">REDUCE SSH ATTACK SURFACE AND ENFORCE KEY-BASED ACCESS</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="body cols-2">
{concept_card(ic_server(RED), "bg-red", "SSH Attack Surface", "SSH is a common target for attackers. <strong>Reduce exposure by limiting access, strengthening authentication, and monitoring activity.</strong>")}
{concept_card(ic_key(GREEN), "bg-green", "Key-Based Authentication", "Use SSH keys instead of passwords. <strong>Stronger, more secure, and resistant to brute-force attacks.</strong>")}
{concept_card(ic_ban(RED), "bg-red", "Disabling Root SSH Login", "Do not allow root to login via SSH. <strong>Use a regular user and sudo for administrative tasks.</strong>")}
{concept_card(ic_lock(RED), "bg-red", "Disabling Password Auth", "Disable password-based login. <strong>Prevents brute-force and credential stuffing attacks.</strong>")}
{concept_card(ic_file(BLUE), "bg-blue", "sshd_config", "Main SSH server configuration file. Harden settings in <code>/etc/ssh/sshd_config</code> and reload SSH service safely.")}
{concept_card(ic_users(GREEN), "bg-green", "Restricting Users & Groups", "Allow only specific users or groups to access SSH. <strong>Deny all others.</strong> Use AllowUsers and AllowGroups.")}
{concept_card(ic_lock(GOLD), "bg-gold", "SSH Key Permissions", "Private key (<code>id_rsa</code>): <strong>600</strong>. Public key (<code>id_rsa.pub</code>): <strong>644</strong>. <code>~/.ssh</code> directory: <strong>700</strong>. <code>authorized_keys</code>: <strong>600</strong>. <em>Wrong permissions = login failure.</em>")}
{concept_card(ic_clock(PURPLE), "bg-purple", "Idle-Session Controls", "Set timeouts for idle sessions. <strong>Disconnect inactive sessions automatically to reduce risk.</strong>")}
      </div>
{section_h("sshd_config — Hardened Settings", "REFERENCE")}
{sshd_settings}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;">
        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">SSH Key Generation</span></div>
          <pre class="term-body">{keygen_term}</pre>
        </div>
        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">Copy Public Key to Server</span></div>
          <pre class="term-body">{copy_term}</pre>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;">
        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">Validate & Reload Configuration</span></div>
          <pre class="term-body">{validate_term}</pre>
        </div>
        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">Review Authentication Logs</span></div>
          <pre class="term-body">{log_term}</pre>
        </div>
      </div>
      <div class="callout warning" style="margin-top:14px;">
        <div class="icn">{ic_warn(RED)}</div>
        <div class="ct">
          <h5>TEST BEFORE RESTART</h5>
          <p>Always validate SSH configuration before restarting to avoid lockout. Use test mode: <code>sshd -t</code>. Monitor SSH login attempts, failed logins, and suspicious activity regularly — <strong>logs help detect brute-force attacks early.</strong></p>
        </div>
      </div>'''
    return wrap_page(8, body, ch_label="SSH")

def page_09_systemd():
    cmd_table = data_table(
        ["COMMAND", "DESCRIPTION"],
        [
            ("systemctl list-units --type=service", "List all services."),
            ("systemctl list-unit-files --type=service", "Show enabled/disabled services."),
            ("systemctl status &lt;service&gt;", "Show service status and logs."),
            ("systemctl start &lt;service&gt;", "Start a service."),
            ("systemctl stop &lt;service&gt;", "Stop a service."),
            ("systemctl restart &lt;service&gt;", "Restart a service."),
            ("systemctl enable &lt;service&gt;", "Enable at boot."),
            ("systemctl disable &lt;service&gt;", "Disable from boot."),
            ("systemctl mask &lt;service&gt;", "Prevent service from starting."),
            ("systemctl unmask &lt;service&gt;", "Unmask a service."),
        ],
        mono_cols=[0]
    )
    check_term = '''<span class="cmt"># List enabled services</span>
<span class="pmt">$</span> systemctl list-unit-files --type=service --state=enabled
<span class="cmt"># List running services</span>
<span class="pmt">$</span> systemctl list-units --type=service --state=running
<span class="cmt"># Compare both to find unused services.</span>'''
    detail_term = '''<span class="cmt"># Show full unit file</span>
<span class="pmt">$</span> systemctl cat &lt;service&gt;
<span class="cmt"># Show all properties</span>
<span class="pmt">$</span> systemctl show &lt;service&gt;'''
    body = f'''      <div class="title-block">
        <h1 class="title long">8. LINUX SERVICES AND SYSTEMD SECURITY</h1>
        <div class="subtitle">MANAGE, ISOLATE, AND HARDEN SYSTEM SERVICES</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="body cols-2">
{concept_card(ic_target(RED), "bg-red", "Identifying Unnecessary Services", "Many services start automatically by default. <strong>Remove or disable services you do not need.</strong> Every unnecessary service increases your attack surface.")}
{concept_card(ic_gear(BLUE), "bg-blue", "systemctl", "The primary tool for managing systemd services. Used to <strong>start, stop, enable, disable, and inspect services.</strong>")}
{concept_card(ic_eye(GREEN), "bg-green", "Enabled vs Running", "<strong>Enabled:</strong> Starts automatically at boot.<br><strong>Running:</strong> Currently active in memory.<br>A service can be enabled, running, both, or neither.")}
{concept_card(ic_ban(RED), "bg-red", "Disabling Unused Services", "Disable services to prevent them from starting at boot. Stop services that are not needed now. <strong>Example:</strong> <code>systemctl disable --now &lt;service&gt;</code>")}
{concept_card(ic_user(GREEN), "bg-green", "Service Users", "Services should run as an unprivileged user. <strong>Avoid running services as root.</strong> Check the <code>User=</code> and <code>Group=</code> settings in unit files.")}
{concept_card(ic_file(GOLD), "bg-gold", "Systemd Unit Permissions", "Unit files control how services run. <strong>Protect unit files from unauthorized changes.</strong> Typical path: <code>/etc/systemd/system/</code>. Use proper file permissions.")}
{concept_card(ic_shield(PURPLE), "bg-purple", "Service Isolation", "Use systemd sandboxing to limit damage. Options: <code>ProtectSystem, ProtectHome, PrivateTmp, NoNewPrivileges, RestrictAddressFamilies</code>, and more. <strong>Stronger isolation = better security.</strong>")}
{concept_card(ic_clock(BLUE), "bg-blue", "Restart Policies", "Configure how services behave when they fail. Common policies: <code>no, on-failure, on-abnormal, on-watchdog, always</code>. Use <code>RestartSec=</code> to set delay between restarts.")}
{concept_card(ic_search(RED), "bg-red", "Inspecting Failed Services", "Check failed services and view recent logs. Look for crash loops, repeated failures, or unexpected behavior. Use: <code>systemctl status &lt;service&gt;</code> and <code>journalctl -u &lt;service&gt;</code>")}
{concept_card(ic_check(GREEN), "bg-green", "Reducing Service Attack Surface", "Run only what you need. Disable, mask, or remove unneeded services. Keep services updated and properly configured. <strong>Fewer services = fewer risks.</strong>")}
      </div>
{section_h("Common systemctl Commands", "MANAGE")}
{cmd_table}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;">
        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">Check Enabled vs Running Services</span></div>
          <pre class="term-body">{check_term}</pre>
        </div>
        <div class="term-block">
          <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">View Service Details</span></div>
          <pre class="term-body">{detail_term}</pre>
        </div>
      </div>
      <div class="callout tip" style="margin-top:14px;">
        <div class="icn">{ic_check(GREEN)}</div>
        <div class="ct">
          <h5>BEST PRACTICES</h5>
          <ul>
            <li>Disable services you do not use.</li>
            <li>Run services as non-root users.</li>
            <li>Harden services with isolation options.</li>
            <li>Limit network and filesystem access.</li>
            <li>Monitor service logs and failures.</li>
            <li>Keep services updated.</li>
            <li>Review services regularly.</li>
            <li>Follow least-privilege principles.</li>
          </ul>
        </div>
      </div>'''
    return wrap_page(9, body, ch_label="SYSTEMD")

def page_10_network():
    body = f'''      <div class="title-block">
        <h1 class="title long">9. NETWORK EXPOSURE AND OPEN PORTS</h1>
        <div class="subtitle">IDENTIFY, AUDIT, AND MINIMIZE LISTENING SERVICES</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="body cols-2">
{concept_card(ic_server(BLUE), "bg-blue", "Listening Sockets", "Listening sockets are endpoints that accept incoming connections or packets on the system. <strong>Identify every listening socket to map your exposure.</strong>")}
{concept_card(ic_globe(RED), "bg-red", "TCP and UDP Exposure", "Open TCP ports establish connections. Open UDP ports receive datagrams. <strong>Both increase the attack surface.</strong>")}
{concept_card(ic_term(BLUE), "bg-blue", "ss", "<strong>ss</strong> is the modern tool to view socket statistics, listening ports, and network connections. Use it to identify what is listening on the system.")}
{concept_card(ic_search(GREEN), "bg-green", "lsof", "<strong>lsof</strong> lists open files and the processes that opened them, including network sockets. <strong>Useful for identifying listening ports and connections.</strong>")}
{concept_card(ic_eye(GOLD), "bg-gold", "Processes Behind Ports", "Find which process is listening on a specific port. <strong>Understand the service, user, and risk associated with that process.</strong>")}
{concept_card(ic_server(NAVY), "bg-neutral", "Loopback vs Public", "Services bound to <code>127.0.0.1</code> are only accessible locally. Services bound to <code>0.0.0.0</code> or public IPs are accessible from the network or internet.")}
{concept_card(ic_warn(RED), "bg-red", "Unexpected Listening Services", "Unexpected or unnecessary services listening on ports may indicate <strong>misconfiguration or potential compromise.</strong> Always review and minimize exposed services.")}
{concept_card(ic_audit(PURPLE), "bg-purple", "Network Exposure Investigation", "Investigate open ports, services, and connections. <strong>Correlate with logs and configurations</strong> to assess the security impact.")}
      </div>
{section_h("Investigation Commands", "INSPECT")}
      <div class="cmd-grid cols-3">
{cmd_card("bg-blue", ic_term(), "ss -tulpen", "List all listening TCP/UDP sockets with process info.", '<span class="pmt">$</span> ss -tulpen')}
{cmd_card("bg-blue", ic_term(), "ss -antp", "Show all TCP connections with processes.", '<span class="pmt">$</span> ss -antp')}
{cmd_card("bg-green", ic_search(GREEN), "lsof -i -P -n", "List open network files/sockets.", '<span class="pmt">$</span> lsof -i -P -n')}
{cmd_card("bg-green", ic_search(GREEN), "netstat -tulpen", "Legacy: list listening sockets.", '<span class="pmt">$</span> netstat -tulpen')}
{cmd_card("bg-purple", ic_eye(PURPLE), "ss -ltnp 'sport = :80'", "Find what listens on port 80.", '<span class="pmt">$</span> ss -ltnp \'sport = :80\'')}
{cmd_card("bg-gold", ic_audit(GOLD), "lsof -i :443", "Identify process on port 443.", '<span class="pmt">$</span> lsof -i :443')}
      </div>
      <div class="callout warning" style="margin-top:14px;">
        <div class="icn">{ic_warn(RED)}</div>
        <div class="ct">
          <h5>PRODUCTION PORT AUDITING</h5>
          <p>Regularly audit open ports and listening services. <strong>Validate that only required services are exposed. Document, monitor, and review continuously.</strong> Bind admin services (SSH, RDP, databases) to loopback or VPN-only interfaces whenever possible.</p>
        </div>
      </div>'''
    return wrap_page(10, body, ch_label="NETWORK")

def page_11_firewall():
    body = f'''      <div class="title-block">
        <h1 class="title">10. LINUX FIREWALL SECURITY</h1>
        <div class="subtitle">FILTER TRAFFIC, ENFORCE POLICIES, AND REDUCE ATTACK SURFACE</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_shield(GREEN), "bg-green", "Host-Based Firewall Purpose", "A host-based firewall controls network traffic to and from your Linux system. <strong>It blocks unauthorized access, reduces attack surface, and enforces security policies at the host level.</strong>")}
{concept_card(ic_gear(PURPLE), "bg-purple", "nftables", "<strong>nftables</strong> is the modern Linux packet filtering framework. It is powerful, fast, and replaces legacy iptables. <strong>It supports complex rules, sets, maps, and stateful filtering.</strong>")}
{concept_card(ic_file(BLUE), "bg-blue", "iptables Concepts", "<strong>iptables</strong> is the legacy firewall tool based on tables, chains, and rules. <strong>Key tables:</strong> filter, nat, mangle, raw. <strong>Key chains:</strong> INPUT, OUTPUT, FORWARD.")}
{concept_card(ic_gear(GREEN), "bg-green", "UFW and firewalld", "<strong>UFW</strong> is a simple frontend for iptables/nftables. <strong>firewalld</strong> provides a dynamic firewall with zones, services, and runtime management.")}
{concept_card(ic_ban(RED), "bg-red", "Default-Deny Strategy", "Start with default deny for incoming connections. <strong>Allow only what is required.</strong> This minimizes risk by blocking everything except explicitly allowed traffic.")}
{concept_card(ic_chain(BLUE), "bg-blue", "Inbound vs Outbound Rules", "<strong>Inbound rules</strong> control traffic coming into the system.<br><strong>Outbound rules</strong> control traffic leaving the system.<br>Both should be defined intentionally.")}
{concept_card(ic_lock(GOLD), "bg-gold", "Restricting Administrative Ports", "Limit access to administrative ports (SSH, RDP, etc.) to trusted IPs or networks only. <strong>Never expose admin ports to the public internet.</strong>")}
{concept_card(ic_eye(GREEN), "bg-green", "Rule Ordering", "Firewall rules are processed in order from top to bottom. <strong>Place specific allow rules before general deny rules.</strong> Incorrect ordering can create security gaps.")}
{concept_card(ic_gear(GOLD), "bg-gold", "Persistent Configuration", "Firewall rules must survive reboots. Use appropriate tools to save rules: <code>nft list ruleset &gt; file</code>, <code>iptables-save</code>, <code>ufw enable</code>, <code>firewalld --permanent</code>.")}
{concept_card(ic_warn(RED), "bg-red", "Testing Without Lockout", "Always test firewall changes carefully. <strong>Use a second SSH session or console access.</strong> Apply changes gradually and verify before closing your session.")}
      </div>
{section_h("Firewall Commands by Tool", "DEPLOY")}
      <div class="cmd-grid cols-3">
{cmd_card("bg-purple", ic_gear(PURPLE), "nft list ruleset", "List current nftables ruleset.", '<span class="pmt">$</span> nft list ruleset')}
{cmd_card("bg-purple", ic_gear(PURPLE), "nft add rule", "Add a new rule to nftables chain.", '<span class="pmt">$</span> nft add rule inet filter input tcp dport 22 accept')}
{cmd_card("bg-blue", ic_term(), "iptables -L -v -n", "List iptables rules with stats.", '<span class="pmt">$</span> iptables -L -v -n')}
{cmd_card("bg-blue", ic_term(), "iptables-save", "Persist iptables rules to file.", '<span class="pmt">$</span> iptables-save &gt; /etc/iptables/rules.v4')}
{cmd_card("bg-green", ic_check(GREEN), "ufw allow", "Allow a port with UFW.", '<span class="pmt">$</span> ufw allow 22/tcp\\n<span class="pmt">$</span> ufw enable')}
{cmd_card("bg-gold", ic_audit(GOLD), "firewall-cmd", "Manage firewalld zones/services.", '<span class="pmt">$</span> firewall-cmd --permanent --add-service=ssh')}
      </div>
      <div class="callout tip" style="margin-top:14px;">
        <div class="icn">{ic_check(GREEN)}</div>
        <div class="ct">
          <h5>FIREWALL HARDENING CHECKLIST</h5>
          <ul>
            <li>Apply <strong>default deny</strong> for inbound traffic.</li>
            <li>Allow only required ports and protocols.</li>
            <li>Restrict admin ports to trusted IPs.</li>
            <li>Order rules: specific allow first, then deny.</li>
            <li>Persist rules across reboots.</li>
            <li>Test changes from a second session.</li>
            <li>Document every rule with a comment.</li>
            <li>Review rules monthly.</li>
          </ul>
        </div>
      </div>'''
    return wrap_page(11, body, ch_label="FIREWALL")

def page_12_process():
    body = f'''      <div class="title-block">
        <h1 class="title long">11. PROCESS AND RUNTIME SECURITY</h1>
        <div class="subtitle">MONITOR, INVESTIGATE, AND CONTAIN RUNNING PROCESSES</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_user(BLUE), "bg-blue", "Process Ownership", "Every process runs as a specific user and group. <strong>Review process ownership to ensure least privilege and detect suspicious activity.</strong>")}
{concept_card(ic_chain(GREEN), "bg-green", "Parent and Child Processes", "Processes are created by other processes. <strong>Understanding parent-child relationships helps trace the origin of a process.</strong>")}
{concept_card(ic_warn(RED), "bg-red", "Privileged Processes", "Processes running as root or with elevated capabilities pose higher risk. <strong>Review and restrict privileged processes.</strong>")}
{concept_card(ic_term(BLUE), "bg-blue", "ps, top, pstree", "Use <strong>ps</strong> to view processes, <strong>top</strong> for live monitoring, and <strong>pstree</strong> to visualize process trees. Essential tools for runtime visibility.")}
{concept_card(ic_file(PURPLE), "bg-purple", "/proc", "The <code>/proc</code> filesystem provides real-time information about processes, memory, mounts, network, and more. <strong>Powerful for investigation.</strong>")}
{concept_card(ic_search(RED), "bg-red", "Suspicious Command Lines", "Review process command lines. <strong>Look for obfuscated, encoded, or unusual commands</strong> that may indicate malicious activity.")}
{concept_card(ic_bug(RED), "bg-red", "Unexpected Binaries", "Processes running from unusual locations (e.g., <code>/tmp</code>, <code>/dev/shm</code>) or unknown binaries may indicate <strong>compromise.</strong>")}
{concept_card(ic_clock(GOLD), "bg-gold", "Long-Running Processes", "Processes running longer than expected can indicate <strong>stuck services or persistence mechanisms.</strong> Review and validate regularly.")}
{concept_card(ic_server(NAVY), "bg-neutral", "Processes on the Network", "Identify processes that have open sockets. <strong>Ensure only required services are listening on expected ports and interfaces.</strong>")}
{concept_card(ic_audit(GREEN), "bg-green", "Investigating Abnormal Activity", "Correlate process behavior, network activity, and logs to detect anomalies. <strong>Investigate immediately and contain threats.</strong>")}
      </div>
{section_h("Process Investigation Commands", "INSPECT")}
      <div class="cmd-grid cols-3">
{cmd_card("bg-blue", ic_term(), "ps aux", "Snapshot all running processes.", '<span class="pmt">$</span> ps aux')}
{cmd_card("bg-blue", ic_term(), "ps -ef --forest", "Show process tree hierarchy.", '<span class="pmt">$</span> ps -ef --forest')}
{cmd_card("bg-blue", ic_term(), "top / htop", "Live interactive process monitor.", '<span class="pmt">$</span> top')}
{cmd_card("bg-green", ic_chain(GREEN), "pstree -p", "Tree view of running processes.", '<span class="pmt">$</span> pstree -p')}
{cmd_card("bg-purple", ic_eye(PURPLE), "ls -la /proc/&lt;pid&gt;", "Inspect process details in /proc.", '<span class="pmt">$</span> ls -la /proc/&lt;pid&gt;')}
{cmd_card("bg-gold", ic_search(GOLD), "cat /proc/&lt;pid&gt;/cmdline", "View full process command line.", '<span class="pmt">$</span> cat /proc/&lt;pid&gt;/cmdline')}
      </div>
      <div class="callout warning" style="margin-top:14px;">
        <div class="icn">{ic_warn(RED)}</div>
        <div class="ct">
          <h5>RED FLAGS — INVESTIGATE IMMEDIATELY</h5>
          <ul>
            <li>Processes from <code>/tmp</code>, <code>/dev/shm</code>, or <code>/var/tmp</code>.</li>
            <li>Encoded/obfuscated command lines (base64, hex).</li>
            <li>Long-running processes with no parent.</li>
            <li>Processes listening on unexpected ports.</li>
            <li>Root processes not in your baseline inventory.</li>
          </ul>
        </div>
      </div>'''
    return wrap_page(12, body, ch_label="PROCESSES")

def page_13_logging():
    body = f'''      <div class="title-block">
        <h1 class="title long">12. LOGGING AND SECURITY INVESTIGATION</h1>
        <div class="subtitle">COLLECT, FILTER, AND CORRELATE LOGS TO BUILD AN INCIDENT TIMELINE</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_file(BLUE), "bg-blue", "Linux Authentication Logs", "Authentication logs record user logins, logouts, and security-relevant events. <strong>Key sources:</strong> <code>/var/log/auth.log</code>, <code>/var/log/secure</code>.")}
{concept_card(ic_term(GREEN), "bg-green", "journalctl", "<strong>journalctl</strong> is the systemd log manager. View system, service, kernel, and boot logs. <strong>Powerful filtering with time, unit, priority, and more.</strong>")}
{concept_card(ic_folder(GOLD), "bg-gold", "/var/log", "Traditional log files stored in <code>/var/log</code>. Contains authentication, system, application, and service logs.")}
{concept_card(ic_server(RED), "bg-red", "SSH Login Events", "Track successful and failed SSH logins. Logs show IP address, user, time, and authentication method. <strong>Helps detect brute-force and suspicious access.</strong>")}
{concept_card(ic_key(PURPLE), "bg-purple", "Sudo Activity", "Monitor sudo command usage and privilege escalation. Logs show <strong>who ran what command and when.</strong> Essential for auditing privileged access.")}
{concept_card(ic_ban(RED), "bg-red", "Failed Authentication", "Failed login attempts indicate attacks or misconfiguration. <strong>Track repeated failures from the same IP or user.</strong> Helps identify brute-force and password attacks.")}
{concept_card(ic_warn(RED), "bg-red", "Service Failures", "Service errors can impact availability and security. Logs show crashes, dependency issues, and start failures. <strong>Helps detect misconfigurations and potential attacks.</strong>")}
{concept_card(ic_gear(NAVY), "bg-neutral", "Kernel Messages", "Kernel logs report hardware, driver, and system events. Important for detecting panics, OOM kills, and security issues. <strong>Access via dmesg or journalctl -k.</strong>")}
{concept_card(ic_search(GREEN), "bg-green", "Searching and Filtering Logs", "Use tools like <strong>grep, awk, sed</strong>, and journalctl filters. Filter by time, user, IP, service, priority, or keywords. <strong>Effective searching speeds up investigation.</strong>")}
{concept_card(ic_audit(GOLD), "bg-gold", "Building an Incident Timeline", "Correlate events from multiple logs to understand what happened. Establish sequence: <strong>initial access → actions → impact.</strong> A clear timeline is critical for response and reporting.")}
      </div>
{section_h("Investigation Commands", "FILTER")}
      <div class="cmd-grid cols-3">
{cmd_card("bg-green", ic_term(), "journalctl -u ssh", "View logs for the SSH service.", '<span class="pmt">$</span> journalctl -u ssh --since "1 hour ago"')}
{cmd_card("bg-blue", ic_term(), "journalctl -p err -b", "View errors from current boot.", '<span class="pmt">$</span> journalctl -p err -b')}
{cmd_card("bg-purple", ic_search(PURPLE), "journalctl -k", "View kernel messages.", '<span class="pmt">$</span> journalctl -k')}
{cmd_card("bg-red", ic_search(RED), "grep auth.log", "Find failed SSH logins.", '<span class="pmt">$</span> grep "Failed password" /var/log/auth.log')}
{cmd_card("bg-gold", ic_audit(GOLD), "ausearch -m USER_CMD", "Search audit log for sudo.", '<span class="pmt">$</span> ausearch -m USER_CMD --start today')}
{cmd_card("bg-blue", ic_term(), "last -a", "Show recent login sessions.", '<span class="pmt">$</span> last -a')}
      </div>
      <div class="callout tip" style="margin-top:14px;">
        <div class="icn">{ic_check(GREEN)}</div>
        <div class="ct">
          <h5>BUILD AN INCIDENT TIMELINE</h5>
          <p>Correlate events from <code>auth.log</code>, <code>journalctl</code>, <code>audit.log</code>, and application logs. <strong>Establish sequence: initial access → actions → impact.</strong> A clear timeline is critical for response and reporting.</p>
        </div>
      </div>'''
    return wrap_page(13, body, ch_label="LOGGING")

def page_14_auditd():
    body = f'''      <div class="title-block">
        <h1 class="title">13. LINUX AUDITING WITH AUDITD</h1>
        <div class="subtitle">KERNEL-LEVEL MONITORING OF SECURITY-RELEVANT EVENTS</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_shield(GREEN), "bg-green", "Linux Audit Framework", "The Linux Audit Framework provides a comprehensive system for monitoring, recording, and reviewing security-relevant events. <strong>It operates at the kernel level for high integrity and reliability.</strong>")}
{concept_card(ic_gear(BLUE), "bg-blue", "auditd", "<strong>auditd</strong> is the user-space service that collects audit events from the kernel and writes them to the audit log. <strong>It is highly configurable and essential for security monitoring.</strong>")}
{concept_card(ic_file(PURPLE), "bg-purple", "Audit Rules", "Audit rules define what events to monitor. Rules can be file watches, syscalls, users, commands, or system calls. <strong>Use auditctl to load and manage rules.</strong>")}
{concept_card(ic_eye(RED), "bg-red", "Watching Sensitive Files", "Monitor critical files and directories for reads, writes, attribute changes, and deletions. <strong>Example:</strong> <code>/etc/passwd</code>, <code>/etc/shadow</code>, <code>/etc/sudoers</code>.")}
{concept_card(ic_key(GOLD), "bg-gold", "Monitoring Privileged Commands", "Track the use of privileged commands such as <code>sudo, su, useradd, chmod, chown, setuid</code>, and more. <strong>Helps detect privilege escalation and misuse.</strong>")}
{concept_card(ic_search(GREEN), "bg-green", "ausearch", "<strong>ausearch</strong> is used to search the audit log. Filter by time, user, event type, file, PID, or command. <strong>Essential for incident investigations.</strong>")}
{concept_card(ic_audit(BLUE), "bg-blue", "aureport", "<strong>aureport</strong> generates summarized reports from audit logs. <strong>Use it for quick insights on logins, commands, files, and SELinux events.</strong>")}
{concept_card(ic_file(RED), "bg-red", "Tracking Configuration Changes", "Monitor changes to critical configuration files. <strong>Detect unauthorized modifications</strong> to system settings, services, and security policies.")}
{concept_card(ic_lock(NAVY), "bg-neutral", "Audit-Log Protection", "Protect audit logs from tampering. <strong>Set proper permissions, enable log rotation, and forward logs to a secure, centralized location.</strong>")}
{concept_card(ic_check(GREEN), "bg-green", "Practical Investigation Examples", "Real-world scenarios: detecting unauthorized access, tracking file modifications, identifying privilege escalation, <strong>and investigating suspicious activity step-by-step.</strong>")}
      </div>
{section_h("Audit Commands & Rules", "USE")}
      <div class="cmd-grid cols-3">
{cmd_card("bg-blue", ic_gear(BLUE), "auditctl -l", "List all currently loaded audit rules.", '<span class="pmt">$</span> auditctl -l')}
{cmd_card("bg-red", ic_eye(RED), "auditctl -w", "Watch a file for changes.", '<span class="pmt">$</span> auditctl -w /etc/passwd -p wa -k identity')}
{cmd_card("bg-green", ic_search(GREEN), "ausearch", "Search audit log by key/event.", '<span class="pmt">$</span> ausearch -k identity')}
{cmd_card("bg-gold", ic_audit(GOLD), "aureport --summary", "Summarize audit activity.", '<span class="pmt">$</span> aureport --summary')}
{cmd_card("bg-purple", ic_term(), "auditctl -e 1", "Enable auditing (lockable).", '<span class="pmt">$</span> auditctl -e 1')}
{cmd_card("bg-blue", ic_file(BLUE), "cat /etc/audit/audit.rules", "Persistent audit rules file.", '<span class="pmt">$</span> cat /etc/audit/audit.rules')}
      </div>
      <div class="callout note" style="margin-top:14px;">
        <div class="icn">{ic_book(BLUE)}</div>
        <div class="ct">
          <h5>WATCH THESE CRITICAL FILES</h5>
          <p><code>/etc/passwd</code>, <code>/etc/shadow</code>, <code>/etc/sudoers</code>, <code>/etc/ssh/sshd_config</code>, <code>/etc/pam.d/</code>, <code>/etc/cron.d/</code>, <code>/etc/systemd/system/</code>. <strong>Add a <code>-k</code> key to every watch</strong> so events are searchable by tag.</p>
        </div>
      </div>'''
    return wrap_page(14, body, ch_label="AUDITD")

def page_15_selinux():
    modes_table = data_table(
        ["MODE", "BEHAVIOR", "RECOMMENDED?"],
        [
            ("Enforcing", "Policies are active and violations are <strong>blocked</strong>.", "Yes"),
            ("Permissive", "Policies are active but violations are only <strong>logged</strong>.", "Troubleshooting only"),
            ("Disabled", "SELinux is turned off entirely.", "Not recommended"),
        ],
        mono_cols=[]
    )
    body = f'''      <div class="title-block">
        <h1 class="title long">14. SELINUX AND APPARMOR</h1>
        <div class="subtitle">MANDATORY ACCESS CONTROL FOR PROCESS-LEVEL CONFINEMENT</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_shield(GREEN), "bg-green", "Mandatory Access Control", "<strong>SELinux and AppArmor</strong> are Mandatory Access Control (MAC) systems that restrict what processes can do, <strong>even if they are compromised or running as root.</strong>")}
{concept_card(ic_gear(BLUE), "bg-blue", "SELinux Modes", "SELinux operates in three main modes that determine how policies are enforced. <strong>Switch with setenforce or /etc/selinux/config.</strong>")}
{concept_card(ic_hash(PURPLE), "bg-purple", "SELinux Contexts", "SELinux uses security contexts (labels) to define what users, roles, types, and levels a process or file has. <strong>Contexts control access decisions.</strong>")}
{concept_card(ic_warn(RED), "bg-red", "Policy Violations", "When a process is blocked by SELinux, <strong>an AVC (Access Vector Cache) denial is logged.</strong> These logs show what was blocked and why.")}
{concept_card(ic_term(GREEN), "bg-green", "getenforce", "<strong>getenforce</strong> shows the current SELinux mode. <strong>Command:</strong> <code>getenforce</code>. Example output: <code>Enforcing | Permissive | Disabled</code>.")}
{concept_card(ic_eye(GREEN), "bg-green", "sestatus", "<strong>sestatus</strong> displays SELinux status, mode, policy type, and other important details. <strong>Command:</strong> <code>sestatus</code>")}
{concept_card(ic_file(BLUE), "bg-blue", "AppArmor Profiles", "AppArmor uses profiles to restrict programs. <strong>Each profile defines what the program can access.</strong> Profiles are stored in <code>/etc/apparmor.d/</code>.")}
{concept_card(ic_check(GREEN), "bg-green", "Enforce vs Complain Mode", "<strong>Enforce:</strong> Violations are blocked.<br><strong>Complain:</strong> Violations are logged but not blocked. <strong>Use complain mode to test profiles before enforcing.</strong>")}
{concept_card(ic_audit(GOLD), "bg-gold", "Troubleshooting Blocked Apps", "Review AVC logs: <code>ausearch -m avc -ts recent</code>. Identify the blocked action and target. Adjust the policy or profile. Use permissive or complain mode during troubleshooting. <strong>Return to Enforcing/Enforce mode after validation.</strong>")}
      </div>
{section_h("SELinux Modes — Reference", "DECIDE")}
{modes_table}
{section_h("SELinux & AppArmor Commands", "INSPECT")}
      <div class="cmd-grid cols-3">
{cmd_card("bg-green", ic_term(), "getenforce", "Show current SELinux mode.", '<span class="pmt">$</span> getenforce')}
{cmd_card("bg-green", ic_eye(GREEN), "sestatus", "Show detailed SELinux status.", '<span class="pmt">$</span> sestatus')}
{cmd_card("bg-purple", ic_gear(PURPLE), "setenforce 0/1", "Toggle SELinux permissive/enforcing.", '<span class="pmt">$</span> setenforce 0\\n<span class="cmt"># 0 = permissive, 1 = enforcing</span>')}
{cmd_card("bg-blue", ic_term(), "ls -Z", "List files with SELinux contexts.", '<span class="pmt">$</span> ls -Z /var/www/html')}
{cmd_card("bg-blue", ic_term(), "ps -eZ", "List processes with SELinux contexts.", '<span class="pmt">$</span> ps -eZ')}
{cmd_card("bg-gold", ic_audit(GOLD), "apparmor_status", "Show AppArmor profile status.", '<span class="pmt">$</span> apparmor_status')}
      </div>
      <div class="callout warning" style="margin-top:14px;">
        <div class="icn">{ic_warn(RED)}</div>
        <div class="ct">
          <h5>NEVER DISABLE SELINUX TO FIX A PROBLEM</h5>
          <p>Disabling SELinux or AppArmor <strong>silently weakens your system</strong>. Instead, use permissive/complain mode during troubleshooting, capture AVC denials, and adjust policies. Return to Enforcing/Enforce mode after validation.</p>
        </div>
      </div>'''
    return wrap_page(15, body, ch_label="SELINUX")

def page_16_packages():
    body = f'''      <div class="title-block">
        <h1 class="title long">15. PACKAGE, REPOSITORY, AND PATCH SECURITY</h1>
        <div class="subtitle">KEEP SYSTEMS UPDATED WITH TRUSTED, SIGNED PACKAGES</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_pkg(GREEN), "bg-green", "Trusted Package Repositories", "<ul><li>Use official and trusted repositories from your distribution.</li><li>Avoid third-party repositories unless absolutely necessary.</li><li><strong>Untrusted repositories can introduce malicious packages.</strong></li></ul>")}
{concept_card(ic_key(GREEN), "bg-green", "Package Signatures", "<ul><li>Packages are cryptographically signed by the repository.</li><li>The system verifies signatures before installing packages.</li><li><strong>Ensures integrity and authenticity of packages.</strong></li></ul>")}
{concept_card(ic_bolt(GOLD), "bg-gold", "Security Updates", "<ul><li>Security updates fix vulnerabilities and reduce risk.</li><li>Apply updates promptly to protect against known threats.</li><li>Subscribe to security advisories for your distribution.</li></ul>")}
{concept_card(ic_audit(BLUE), "bg-blue", "Patch Management", "<ul><li>Establish a process for testing and applying patches.</li><li>Use staging environments before production rollout.</li><li>Document changes and maintain rollback plans.</li></ul>")}
{concept_card(ic_warn(RED), "bg-red", "Vulnerability Exposure", "<ul><li>Outdated packages are a common attack vector.</li><li>Vulnerabilities can lead to privilege escalation or system compromise.</li><li><strong>Regular patching reduces your attack surface.</strong></li></ul>")}
{concept_card(ic_search(PURPLE), "bg-purple", "Detecting Outdated Packages", "<ul><li>Use tools to list outdated or vulnerable packages.</li><li>Examples: <code>dnf check-update</code>, <code>apt list --upgradable</code>.</li><li>Regularly review and prioritize critical updates.</li></ul>")}
{concept_card(ic_gear(GREEN), "bg-green", "Automatic Security Updates", "<ul><li>Enable automatic updates for critical security patches.</li><li>Tools: <code>unattended-upgrades</code>, <code>dnf-automatic</code>, <code>yum-cron</code>.</li><li>Balance automation with change control policies.</li></ul>")}
{concept_card(ic_file(BLUE), "bg-blue", "Repository Configuration", "<ul><li>Configure repositories securely and verify URLs.</li><li>Disable unnecessary or unused repositories.</li><li><strong>Ensure GPG keys are imported and trusted.</strong></li></ul>")}
{concept_card(ic_ban(RED), "bg-red", "Removing Unnecessary Packages", "<ul><li>Remove unused packages and dependencies.</li><li>Reduce system bloat and minimize attack surface.</li><li>Tools: <code>dnf remove</code>, <code>apt autoremove</code>.</li></ul>")}
{concept_card(ic_check(GOLD), "bg-gold", "Production Patching Strategy", "<ul><li>Define patch windows and maintenance schedules.</li><li>Prioritize critical and high-risk vulnerabilities.</li><li>Test, deploy, verify, and monitor after patching.</li><li>Maintain documentation and audit patch compliance.</li></ul>")}
      </div>
{section_h("Package Management Commands", "USE")}
      <div class="cmd-grid cols-3">
{cmd_card("bg-green", ic_term(), "apt update && upgrade", "Update package list and apply upgrades.", '<span class="pmt">$</span> sudo apt update && sudo apt upgrade')}
{cmd_card("bg-green", ic_term(), "apt list --upgradable", "List packages with available updates.", '<span class="pmt">$</span> apt list --upgradable')}
{cmd_card("bg-green", ic_term(), "apt autoremove", "Remove unused dependencies.", '<span class="pmt">$</span> sudo apt autoremove')}
{cmd_card("bg-blue", ic_term(), "dnf check-update", "Check for available updates (RHEL/Fedora).", '<span class="pmt">$</span> sudo dnf check-update')}
{cmd_card("bg-blue", ic_term(), "dnf upgrade --security", "Apply only security updates.", '<span class="pmt">$</span> sudo dnf upgrade --security')}
{cmd_card("bg-gold", ic_audit(GOLD), "unattended-upgrade", "Run automatic security upgrades.", '<span class="pmt">$</span> sudo unattended-upgrade -d')}
      </div>
      <div class="callout success" style="margin-top:14px;">
        <div class="icn">{ic_check(GREEN)}</div>
        <div class="ct">
          <h5>PRODUCTION PATCHING RULE</h5>
          <p><strong>Define patch windows. Prioritize critical and high-risk vulnerabilities. Test in staging → deploy → verify → monitor.</strong> Maintain documentation and audit patch compliance continuously.</p>
        </div>
      </div>'''
    return wrap_page(16, body, ch_label="PACKAGES")

def page_17_integrity():
    crit_table = data_table(
        ["#", "CRITICAL FILE / LOCATION", "WHY PROTECT"],
        [
            ("1", "/etc/passwd", "User database — compromise = total identity takeover."),
            ("2", "/etc/shadow", "Encrypted password hashes — prime crack target."),
            ("3", "/etc/sudoers", "Sudo privilege rules — change = root escalation."),
            ("4", "/etc/ssh/sshd_config", "SSH hardening — change = remote access bypass."),
            ("5", "/bin, /sbin, /usr/bin, /usr/sbin", "System binaries — modification = rootkit."),
            ("6", "/etc/systemd/system/", "Service unit files — change = persistence."),
            ("7", "/boot/", "Kernel + bootloader — modification = boot-level rootkit."),
            ("8", "/var/spool/cron/", "Cron jobs — change = scheduled persistence."),
            ("9", "/root/.bashrc, /root/.ssh/", "Root startup + SSH keys — change = persistent root."),
        ],
        mono_cols=[1]
    )
    persist_table = data_table(
        ["PERSISTENCE TYPE", "INSPECTION COMMANDS", "WHAT TO LOOK FOR"],
        [
            ("Cron Persistence", "crontab -l<br>ls -la /etc/cron.*<br>ls -la /var/spool/cron/", "Malicious or unexpected cron jobs."),
            ("Systemd Persistence", "systemctl list-unit-files --type=service<br>ls -la /etc/systemd/system/", "Malicious or unknown systemd services."),
            ("Shell Startup Files", "cat ~/.bashrc<br>cat ~/.bash_profile<br>ls -la /etc/profile.d/", "Suspicious commands in startup files."),
            ("Suspicious Binaries", "find / -type f -executable -newer /etc/passwd", "Recently added binaries, especially in /tmp, /dev/shm, /opt."),
        ],
        mono_cols=[1]
    )
    hash_term = '''<span class="cmt"># Generate SHA256 hash for a file</span>
<span class="pmt">$</span> sha256sum /etc/passwd
<span class="cmt"># Generate SHA256 hash for a directory (recursive)</span>
<span class="pmt">$</span> sha256sum -r /etc &gt; etc.sha256
<span class="cmt"># Verify against known good hash list</span>
<span class="pmt">$</span> sha256sum -c etc.sha256'''
    body = f'''      <div class="title-block">
        <h1 class="title long">16. FILE INTEGRITY AND PERSISTENCE DETECTION</h1>
        <div class="subtitle">DETECT UNAUTHORIZED MODIFICATIONS AND ATTACKER PERSISTENCE</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="body cols-2-uneven">
        <div>
{section_h("File Integrity Monitoring with sha256sum")}
          <div class="term-block">
            <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">sha256sum — Hash & Verify</span></div>
            <pre class="term-body">{hash_term}</pre>
          </div>
          <div class="callout note" style="margin-top:12px;">
            <div class="icn">{ic_book(BLUE)}</div>
            <div class="ct">
              <h5>FILE INTEGRITY MONITORING</h5>
              <ul>
                <li>Regularly hash critical files.</li>
                <li>Store hashes securely.</li>
                <li>Compare hashes to detect changes.</li>
                <li>Use tools like <strong>AIDE, Tripwire, or OSSEC</strong>.</li>
              </ul>
            </div>
          </div>
        </div>
        <div>
{section_h("Critical System Files")}
          {crit_table}
        </div>
      </div>
{section_h("Persistence Locations", "INSPECT")}
{persist_table}
      <div class="callout warning" style="margin-top:14px;">
        <div class="icn">{ic_warn(RED)}</div>
        <div class="ct">
          <h5>DETECTING UNAUTHORIZED CHANGES</h5>
          <ul>
            <li>Monitor critical files and directories.</li>
            <li>Track new or modified binaries.</li>
            <li>Review file ownership and permissions.</li>
            <li>Alert on unexpected changes.</li>
            <li><strong>Investigate immediately.</strong></li>
          </ul>
        </div>
      </div>
      <div class="callout success" style="margin-top:12px;">
        <div class="icn">{ic_check(GREEN)}</div>
        <div class="ct">
          <h5>PROTECT. MONITOR. VERIFY.</h5>
          <p>Integrity today, security forever. <strong>Hash critical files. Monitor changes. Detect persistence early.</strong></p>
        </div>
      </div>'''
    return wrap_page(17, body, ch_label="INTEGRITY")

def page_18_secrets():
    search_term = '''<span class="cmt"># Search for common patterns</span>
<span class="pmt">$</span> grep -rni "password" /
<span class="pmt">$</span> grep -rni "passwd" /
<span class="pmt">$</span> grep -rni "api_key" /
<span class="pmt">$</span> grep -rni "secret" /
<span class="pmt">$</span> grep -rni "token" /
<span class="cmt"># Use tools</span>
<span class="pmt">$</span> rg "(password|api_key|secret|token)" /
<span class="pmt">$</span> trufflehog filesystem ./
<span class="pmt">$</span> git-secrets --scan-history
<span class="pmt">$</span> gitleaks detect'''
    body = f'''      <div class="title-block">
        <h1 class="title long">17. SECRETS, CREDENTIALS, AND SENSITIVE DATA</h1>
        <div class="subtitle">FIND, PROTECT, AND ROTATE LEAKED CREDENTIALS</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_file(RED), "bg-red", "1 · Secrets in Config Files", "Avoid storing passwords, tokens, and API keys in plain text. <strong>Common files:</strong> <code>/etc/*.conf</code>, <code>~/.config/*</code>, <code>/var/www/html/.php-env</code>, <code>settings.json</code>.")}
{concept_card(ic_term(BLUE), "bg-blue", "2 · Environment Variables", "Environment variables may contain secrets. <strong>Check:</strong> <code>env</code>, <code>printenv</code>, <code>cat /proc/*/environ</code>. Never expose via shell exports to shared systems.")}
{concept_card(ic_key(GREEN), "bg-green", "3 · SSH Private Keys", "Protect private keys at all times. <strong>Default location:</strong> <code>~/.ssh/id_rsa</code>. Permissions <code>600</code>. Store securely. Avoid hardcoding. Rotate regularly. <strong>Never share private keys.</strong>")}
{concept_card(ic_hash(PURPLE), "bg-purple", "4 · API Keys", "Never hardcode API keys in source code. <strong>Store in vault or secret manager.</strong> Rotate regularly. Audit access logs.")}
{concept_card(ic_database(BLUE), "bg-blue", "5 · Database Credentials", "Check config files, scripts, and environment variables. <strong>Credentials should not be stored in plain text.</strong> Use secret managers or vaults.")}
{concept_card(ic_lock(RED), "bg-red", "6 · File Permission Mistakes", "Incorrect permissions can expose secrets. <strong>Sensitive files should be readable by owner only.</strong> Check: <code>ls -l &lt;file&gt;</code>. Fix with: <code>chmod 600 &lt;file&gt;</code>.")}
{concept_card(ic_term(GOLD), "bg-gold", "7 · Shell History Exposure", "Commands containing secrets may be saved in history. <strong>Check:</strong> <code>~/.bash_history</code>, <code>~/.zsh_history</code>. Clear when needed: <code>history -c</code>. Avoid passing secrets as command args.")}
{concept_card(ic_eye(NAVY), "bg-neutral", "8 · Process Argument Exposure", "Secrets passed as arguments can be visible to other users. <strong>Check running processes:</strong> <code>ps aux</code>. Avoid passing secrets as command text. Use stdin or env files instead.")}
{concept_card(ic_clock(GREEN), "bg-green", "9 · Secret Rotation", "Rotate credentials regularly. <strong>Revoke old keys and tokens. Automate rotation where possible. Document rotation procedures. Monitor for unused credentials.</strong>")}
{concept_card(ic_search(RED), "bg-red", "10 · Searching for Exposed Credentials", "Search for common patterns across the filesystem. <strong>Use tools:</strong> grep, ripgrep (rg), trufflehog, git-secrets, gitleaks.")}
      </div>
{section_h("Search the System for Exposed Secrets", "AUDIT")}
      <div class="term-block">
        <div class="term-head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="ttl">Hunt for Exposed Credentials</span></div>
        <pre class="term-body">{search_term}</pre>
      </div>
      <div class="callout warning" style="margin-top:14px;">
        <div class="icn">{ic_warn(RED)}</div>
        <div class="ct">
          <h5>EXPOSED SECRETS = FULL COMPROMISE</h5>
          <p>Exposed secrets can lead to complete system compromise. <strong>STORE SECURELY. LIMIT ACCESS. ROTATE REGULARLY.</strong></p>
        </div>
      </div>'''
    return wrap_page(18, body, ch_label="SECRETS")

def page_19_baseline():
    body = f'''      <div class="title-block">
        <h1 class="title long">18. LINUX SECURITY HARDENING BASELINE</h1>
        <div class="subtitle">A CHECKLIST FOR HARDENING LINUX SYSTEMS IN PRODUCTION</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="concept-grid cols-2">
{concept_card(ic_server(GREEN), "bg-green", "1 · Secure Installation", "<ul><li>Install a minimal OS.</li><li>Use trusted repositories only.</li><li>Configure hostname, timezone, and NTP.</li></ul>")}
{concept_card(ic_pkg(RED), "bg-red", "2 · Remove Unnecessary Software", "<ul><li>Remove unused packages.</li><li>Avoid installing unnecessary tools.</li><li>Reduce attack surface.</li></ul>")}
{concept_card(ic_ban(RED), "bg-red", "3 · Disable Unused Services", "<ul><li>Identify unnecessary services.</li><li>Disable and stop them.</li><li>Prevent unwanted exposure.</li></ul>")}
{concept_card(ic_lock(GOLD), "bg-gold", "4 · Restrict Privileged Access", "<ul><li>Limit root access.</li><li>Use sudo with least privilege.</li><li>Review and tighten sudoers rules.</li></ul>")}
{concept_card(ic_key(BLUE), "bg-blue", "5 · Harden SSH", "<ul><li>Disable root login.</li><li>Disable password authentication.</li><li>Use key-based authentication.</li><li>Restrict users and groups.</li></ul>")}
{concept_card(ic_shield(GREEN), "bg-green", "6 · Secure Filesystem Permissions", "<ul><li>Set correct ownership and permissions.</li><li>Use least-privilege file access.</li><li>Audit critical directories and files.</li></ul>")}
{concept_card(ic_chain(PURPLE), "bg-purple", "7 · Configure Firewall Rules", "<ul><li>Apply default deny policy.</li><li>Allow only required services.</li><li>Restrict admin ports.</li><li>Review rules regularly.</li></ul>")}
{concept_card(ic_audit(BLUE), "bg-blue", "8 · Enable Auditing", "<ul><li>Install and configure auditd.</li><li>Monitor privileged commands.</li><li>Watch critical files and directories.</li><li>Review audit logs regularly.</li></ul>")}
{concept_card(ic_bolt(GOLD), "bg-gold", "9 · Apply Security Updates", "<ul><li>Keep system and packages updated.</li><li>Enable automatic security updates where possible.</li><li>Regularly check for vulnerabilities.</li></ul>")}
{concept_card(ic_check(PURPLE), "bg-purple", "10 · CIS Benchmark Concepts", "<ul><li>Follow CIS Benchmark guidelines.</li><li>Apply secure configurations.</li><li>Validate settings against CIS controls.</li><li>Continuously improve security posture.</li></ul>")}
{concept_card(ic_book(NAVY), "bg-neutral", "11 · Documenting Exceptions", "<ul><li>Document any security exceptions.</li><li>Include business justification.</li><li>Review and revalidate regularly.</li></ul>", )}
      </div>
      <div class="callout success" style="margin-top:14px;">
        <div class="icn">{ic_check(GREEN)}</div>
        <div class="ct">
          <h5>A STRONG BASELINE = A SECURE LINUX SYSTEM</h5>
          <p>Hardening is <strong>not a one-time task</strong>. Continuously review, validate, and improve your security posture. Apply the CIS Benchmarks as a starting point and document every exception with business justification.</p>
        </div>
      </div>'''
    return wrap_page(19, body, ch_label="BASELINE")

def page_20_investigation():
    steps = [
        {"n": "1", "title": "Identify Active Users", "term": '<span class="pmt">$</span> who; whoami; w'},
        {"n": "2", "title": "Search Authentication Logs", "term": '<span class="pmt">$</span> grep -E "sshd|login|su|sudo" /var/log/auth.log'},
        {"n": "3", "title": "Review Recent Logins", "term": '<span class="pmt">$</span> last; last -a; lastlog'},
        {"n": "4", "title": "Check Failed SSH Attempts", "term": '<span class="pmt">$</span> grep "Failed password" /var/log/auth.log'},
        {"n": "5", "title": "Check Cron Jobs & Systemd Units", "term": '<span class="pmt">$</span> crontab -l; ls -la /etc/cron.*\n<span class="pmt">$</span> systemctl list-unit-files --type=service'},
        {"n": "6", "title": "Find Recently Modified Files", "term": '<span class="pmt">$</span> find / -type f -mtime -1 -ls'},
        {"n": "7", "title": "Inspect Sudo Activity", "term": '<span class="pmt">$</span> sudo journalctl -u sudo\n<span class="pmt">$</span> ausearch -m USER_CMD\n<span class="cmt"># Adjust time as needed</span>'},
        {"n": "8", "title": "Review Running Processes", "term": '<span class="pmt">$</span> ps aux; top; pstree -p'},
        {"n": "9", "title": "Identify Open Ports", "term": '<span class="pmt">$</span> ss -tulpen; netstat -tulpen'},
        {"n": "10", "title": "Inspect Network Connections", "term": '<span class="pmt">$</span> ss -antp; lsof -i -P -n'},
        {"n": "11", "title": "Check New/Modified User Accounts", "term": '<span class="pmt">$</span> cut -d: -f1 /etc/passwd\n<span class="pmt">$</span> getent passwd'},
        {"n": "12", "title": "Look for SUID Binaries", "term": '<span class="pmt">$</span> find / -type f -perm -4000 -ls 2&gt;/dev/null'},
        {"n": "13", "title": "Preserve Evidence", "term": '<span class="pmt">$</span> ps aux &gt; /root/evidence_processes_$(date +%F).log\n<span class="pmt">$</span> ss -antp &gt; /root/evidence_connections_$(date +%F).log\n<span class="pmt">$</span> journalctl -u ssh --since "24 hours ago" &gt; /root/evidence_auth_$(date +%F).log\n<span class="pmt">$</span> dmesg &gt; /root/evidence_dmesg_$(date +%F).log'},
    ]
    body = f'''      <div class="title-block">
        <h1 class="title long">19. PRODUCTION SECURITY INCIDENT INVESTIGATION</h1>
        <div class="subtitle">A STEP-BY-STEP RUNBOOK FOR RESPONDING TO SUSPICIOUS ACTIVITY</div>
      </div>
      <div class="divider"><span class="line"></span><span class="dot"></span><span class="line"></span></div>
      <div class="callout warning">
        <div class="icn">{ic_warn(RED)}</div>
        <div class="ct">
          <h5>SCENARIO</h5>
          <p>A Linux server shows suspicious activity. <strong>Follow these 13 investigation steps in order.</strong> Always preserve evidence before taking corrective action.</p>
        </div>
      </div>
{section_h("Investigation Steps", "13 STEPS")}
{steps_flow(steps)}
      <div class="callout tip" style="margin-top:14px;">
        <div class="icn">{ic_check(GREEN)}</div>
        <div class="ct">
          <h5>ALWAYS PRESERVE EVIDENCE FIRST</h5>
          <p>Always preserve evidence before taking corrective action. <strong>Document everything.</strong> Capture process lists, network connections, authentication logs, and kernel messages to timestamped files before rebooting, killing processes, or rolling back changes.</p>
        </div>
      </div>'''
    return wrap_page(20, body, ch_label="INVESTIGATION")

# ============================================================
# ASSEMBLE
# ============================================================
def build():
    pages = [
        page_01_cover(),
        page_02_foundations(),
        page_03_users(),
        page_04_passwords(),
        page_05_permissions(),
        page_06_suid(),
        page_07_sudo(),
        page_08_ssh(),
        page_09_systemd(),
        page_10_network(),
        page_11_firewall(),
        page_12_process(),
        page_13_logging(),
        page_14_auditd(),
        page_15_selinux(),
        page_16_packages(),
        page_17_integrity(),
        page_18_secrets(),
        page_19_baseline(),
        page_20_investigation(),
    ]
    html = CSS_HEAD + "\n<body>\n\n" + "\n\n".join(pages) + "\n\n</body>\n</html>\n"
    OUT.write_text(html)
    return len(pages)

if __name__ == "__main__":
    n = build()
    print(f"Wrote {n} pages to {OUT}")
    print(f"File size: {OUT.stat().st_size:,} bytes")
