#!/usr/bin/env python3
"""
Recreate Instagram carousel pages 16-20 (file index) as self-contained
notebook-style HTML files using the shared shell-scripting template.

Each page is recreated from the original WebP image content (analyzed via
VLM) and rendered using NOTEBOOK_CSS + page_wrapper from
build_shell_scripting_template.py.

File index → carousel page mapping (derived from the original images):
  page-16.webp  → "15. Networking with Shell Scripts"
  page-17.webp  → "16. Error Handling and Safer Scripts"
  page-18.webp  → "18. Scheduling Scripts with Cron"
  page-19.webp  → "17. Debugging Shell Scripts"
  page-20.webp  → "19. Shell Scripting in DevOps Workflows"
"""

import os
import sys

# Import shared template
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_shell_scripting_template import (
    NOTEBOOK_CSS, ICONS, icon, page_wrapper,
)

OUT_DIR = "/home/z/my-project/downloads/instagram-DcaW1UljsVk"

# ---------------------------------------------------------------------------
# Extra icons specific to these pages (added on top of ICONS dict)
# ---------------------------------------------------------------------------
EXTRA_ICONS = {
    "ping": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 18 0"/><path d="M7 12a5 5 0 0 1 10 0"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/><line x1="12" y1="13.5" x2="12" y2="20"/></svg>',
    "dns": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M4 8h16M4 16h16M8 4c-2 2.5-2 13.5 0 16M16 4c2 2.5 2 13.5 0 16"/></svg>',
    "http": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10v4M9 10v4M6 12h3"/><path d="M13 10v4h3"/><path d="M18 10v4"/></svg>',
    "shield-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 L20 5 V12 C20 17 16 20.5 12 22 C8 20.5 4 17 4 12 V5 Z"/><path d="M8.5 12 L11 14.5 L15.5 9.5" stroke-width="2.5"/></svg>',
    "clipboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="18" rx="2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M8.5 11h7M8.5 14h7M8.5 17h4"/></svg>',
    "broom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 4 L12 11"/><path d="M3 21 L8 16"/><path d="M8 16 L10 12 L14 12 L16 16 L14 20 L8 20 Z"/></svg>',
    "predictable": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="9 12 11 14 15 9"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/></svg>',
    "log": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="7" y1="8" x2="17" y2="8"/><line x1="7" y1="12" x2="17" y2="12"/><line x1="7" y1="16" x2="13" y2="16"/></svg>',
    "calendar-x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/><line x1="9" y1="13" x2="15" y2="19"/><line x1="15" y1="13" x2="9" y2="19"/></svg>',
    "code-braces": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4c-2 0-3 1-3 3v3c0 1.5-1 2-2 2 1 0 2 .5 2 2v3c0 2 1 3 3 3"/><path d="M16 4c2 0 3 1 3 3v3c0 1.5 1 2 2 2-1 0-2 .5-2 2v3c0 2-1 3-3 3"/></svg>',
    "quote": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7H4a3 3 0 0 0-3 3v3a3 3 0 0 0 3 3h3V10"/><path d="M7 4v3h3"/><path d="M20 7h-3a3 3 0 0 0-3 3v3a3 3 0 0 0 3 3h3V10"/><path d="M20 4v3h3"/></svg>',
    "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>',
    "step": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20 L8 14 L13 17 L21 6"/><circle cx="3" cy="20" r="1.5" fill="currentColor"/><circle cx="8" cy="14" r="1.5" fill="currentColor"/><circle cx="13" cy="17" r="1.5" fill="currentColor"/><circle cx="21" cy="6" r="1.5" fill="currentColor"/></svg>',
    "infinity": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 12c-2 0-3.5-1.5-3.5-3.5S5 5 7 5s4 1.5 5 3.5 3 3.5 5 3.5 3.5-1.5 3.5-3.5S19 5 17 5s-4 1.5-5 3.5-3 3.5-5 3.5z"/></svg>',
    "gear-cog": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v3M12 20v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M1 12h3M20 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/></svg>',
    "heart-pulse": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1l1.4 1.4"/><path d="M3 13h4l2-4 4 8 2-4h6"/></svg>',
    "rocket-up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l-2 5 5-2 9-9c1-1 1-3 0-4s-3-1-4 0l-9 9z"/><path d="M14 7l3 3"/><path d="M5 13c-1 1-1 4-1 4s3 0 4-1"/><circle cx="14.5" cy="9.5" r="1"/></svg>',
    "stack": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 L22 7 L12 12 L2 7 Z"/><path d="M2 12 L12 17 L22 12"/><path d="M2 17 L12 22 L22 17"/></svg>',
    "lock-key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/><circle cx="12" cy="16" r="1.5"/></svg>',
    "github-actions": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9 17c-1 0-2-1-2-2v-1"/><path d="M9 13v-2"/><circle cx="9" cy="9" r="1" fill="currentColor"/><path d="M14 8v6M14 8h2a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-3 0z"/></svg>',
    "jenkins": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M8 12l-2 9 6-2 6 2-2-9"/><path d="M10 6c0-2 4-2 4 0"/></svg>',
    "docker": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11h16a3 3 0 0 1 0 6h-2c-1 1-3 2-5 2H8c-3 0-5-2-5-5z"/><rect x="5" y="7" width="3" height="3"/><rect x="9" y="7" width="3" height="3"/><rect x="13" y="7" width="3" height="3"/><rect x="9" y="3.5" width="3" height="3"/></svg>',
    "k8s": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 L21 7 V17 L12 22 L3 17 V7 Z"/><circle cx="12" cy="12" r="3"/><path d="M12 2 L12 9M21 7 L15 11M21 17 L15 13M12 22 L12 15M3 17 L9 13M3 7 L9 11"/></svg>',
    "vm-cloud": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19a4.5 4.5 0 0 0 0-9 6 6 0 0 0-11.5 1.5A4 4 0 0 0 6 19z"/><rect x="9" y="12" width="6" height="5" rx="1"/><line x1="9" y1="14" x2="15" y2="14"/></svg>',
}
ICONS.update(EXTRA_ICONS)


# ---------------------------------------------------------------------------
# Helper builders
# ---------------------------------------------------------------------------

def row(icon_name, heading, desc_html, icon_bg="bg-green", icon_color="ic-green"):
    """Standard icon row."""
    return f"""
      <div class="row">
        <div class="icon {icon_bg} {icon_color}">{icon(icon_name)}</div>
        <div class="text">
          <h3>{heading}</h3>
          {desc_html}
        </div>
      </div>"""


def terminal(title, lines, term_title="bash"):
    """Build a terminal block. `lines` is a list of HTML strings (already
    wrapped in spans if you want syntax highlighting)."""
    body = "\n".join(lines)
    return f"""
        <div class="terminal">
          <div class="term-bar">
            <div class="term-dot dot-red"></div>
            <div class="term-dot dot-amber"></div>
            <div class="term-dot dot-green"></div>
            <span class="term-title">{term_title}</span>
          </div>
          <div class="term-body">{body}</div>
        </div>"""


def card(head_icon, head_text, body_html):
    """Sidebar card."""
    return f"""
        <div class="card">
          <div class="head">{icon(head_icon)}<span>{head_text}</span></div>
          <div class="body-pad">{body_html}</div>
        </div>"""


def callout(kind, ico_name, body_html):
    """kind: 'warn' or 'tip'."""
    return f"""
      <div class="callout {kind}">
        <div class="ico">{icon(ico_name)}</div>
        <div>{body_html}</div>
      </div>"""


def steps(items):
    """Numbered steps list."""
    out = ['<div class="steps">']
    for i, txt in enumerate(items, 1):
        out.append(f'        <div class="step"><div class="n">{i}</div><div>{txt}</div></div>')
    out.append('        </div>')
    return "\n".join(out)


def tbl(headers, rows):
    """Table with green header."""
    th = "".join(f"<th>{h}</th>" for h in headers)
    body_rows = []
    for r in rows:
        tds = "".join(f"<td>{c}</td>" for c in r)
        body_rows.append(f"          <tr>{tds}</tr>")
    return f"""
        <table class="tbl">
          <thead><tr>{th}</tr></thead>
          <tbody>
{chr(10).join(body_rows)}
          </tbody>
        </table>"""


# ---------------------------------------------------------------------------
# PAGE 16 — 15. Networking with Shell Scripts
# (file page-16.webp, original badge "PAGE 15")
# ---------------------------------------------------------------------------

def build_page_16():
    title = "15. Networking with Shell Scripts"
    subtitle = "TEST. MONITOR. ENSURE AVAILABILITY."

    rows_left = []
    # 1. CURL
    rows_left.append(row(
        "globe",
        "1. CURL – SEND HTTP REQUESTS",
        '<p>Send HTTP requests to endpoints.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">curl</span> <span class="str">https://example.com</span>',
            '<span class="prompt">$</span> <span class="cmd">curl</span> -I <span class="str">https://example.com</span>',
            '<span class="prompt">$</span> <span class="cmd">curl</span> -s -o /dev/null -w <span class="str">"%{http_code}"</span> <span class="str">https://example.com</span>',
            '<div class="comment"># -I headers only · -s silent · -o /dev/null discard body · -w status code</div>',
        ])
    ))
    # 2. PING
    rows_left.append(row(
        "ping",
        "2. PING – TEST CONNECTIVITY",
        '<p>Test whether a host is reachable.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">ping</span> -c 4 google.com',
            '<span class="prompt">$</span> <span class="cmd">ping</span> -c 4 8.8.8.8',
            '<div class="comment"># Check connectivity · Troubleshoot reachability · Measure response time</div>',
        ])
    ))
    # 3. SS
    rows_left.append(row(
        "server",
        "3. SS – CHECK CONNECTIONS",
        '<p>Show network sockets and connections.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">ss</span> -tuln     <span class="comment"># Listening ports</span>',
            '<span class="prompt">$</span> <span class="cmd">ss</span> -tnp      <span class="comment"># All connections</span>',
            '<span class="prompt">$</span> <span class="cmd">ss</span> -ltnp     <span class="comment"># Listening with PID</span>',
        ])
    ))
    # 4. HOSTNAME
    rows_left.append(row(
        "info",
        "4. HOSTNAME – SHOW SYSTEM NAME",
        '<p>Get or set the system hostname.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">hostname</span>       <span class="comment"># Show hostname</span>',
            '<span class="prompt">$</span> <span class="cmd">hostname</span> -I     <span class="comment"># Show IP addresses</span>',
            '<span class="prompt">$</span> <span class="cmd">hostnamectl</span>    <span class="comment"># Detailed info</span>',
        ])
    ))
    # 5. DNS CHECKS
    rows_left.append(row(
        "dns",
        "5. DNS CHECKS – RESOLVE NAMES",
        '<p>Check DNS resolution.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">nslookup</span> example.com',
            '<span class="prompt">$</span> <span class="cmd">dig</span> example.com',
            '<span class="prompt">$</span> <span class="cmd">host</span> example.com',
        ])
    ))
    # 6. HTTP STATUS CODES
    rows_left.append(row(
        "http",
        "6. HTTP STATUS CODES",
        '<p>Check HTTP response codes.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">curl</span> -o /dev/null -s -w <span class="str">"%{http_code}"</span> <span class="str">https://example.com</span>',
            '<div class="comment"># 200 OK · 301/302 Redirect · 404 Not Found · 500 Server Error</div>',
        ])
        + callout("warn", "warning",
                  "Always check status codes, not just ping!")
    ))
    # 7. TEST ENDPOINT AVAILABILITY
    rows_left.append(row(
        "check-square",
        "7. TEST ENDPOINT AVAILABILITY",
        '<p>Quickly test if an endpoint is up.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">curl</span> -s -o /dev/null -w <span class="str">"%{http_code}"</span> <span class="str">https://example.com</span>',
            '<div class="comment"># 200–399 = Available · 400–599 = Not Available · 000 = No Response</div>',
        ])
    ))
    # 8. CHECK APPLICATION HEALTH
    rows_left.append(row(
        "heart-pulse",
        "8. CHECK APPLICATION HEALTH",
        '<p>Check if application health endpoint is OK.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">curl</span> -s <span class="str">https://example.com/health</span>',
            '<span class="prompt">$</span> <span class="cmd">curl</span> -s -f <span class="str">https://example.com/health</span> <span class="prompt">&amp;&amp;</span> <span class="cmd">echo</span> <span class="str">"Healthy"</span> <span class="prompt">||</span> <span class="cmd">echo</span> <span class="str">"Unhealthy"</span>',
        ])
        + callout("tip", "lightbulb",
                  "<strong>Best practice:</strong> Expose a <code class='inline'>/health</code> endpoint in apps.")
    ))
    # 9. SIMPLE WEBSITE AVAILABILITY SCRIPT
    rows_left.append(row(
        "terminal",
        "9. SIMPLE WEBSITE AVAILABILITY SCRIPT",
        '<p>Example: Check website availability.</p>'
        + terminal("script.sh", [
            '<span class="comment">#!/bin/bash</span>',
            '<span class="cmd">URL</span>=<span class="str">"https://example.com"</span>',
            '<span class="cmd">STATUS</span>=$(<span class="cmd">curl</span> -s -o /dev/null -w <span class="str">"%{http_code}"</span> <span class="str">"$URL"</span>)',
            '<span class="prompt">if</span> [ <span class="str">"$STATUS"</span> = <span class="str">"200"</span> ]; <span class="prompt">then</span>',
            '  <span class="cmd">echo</span> <span class="str">"[OK] $URL is UP (200)"</span>',
            '<span class="prompt">else</span>',
            '  <span class="cmd">echo</span> <span class="str">"[DOWN] $URL is DOWN (Code: $STATUS)"</span>',
            '<span class="prompt">fi</span>',
        ])
    ))

    # Sidebar: quick reference table + best practices
    quick_ref_rows = [
        ("curl URL", "Send HTTP request"),
        ("ping HOST", "Test connectivity"),
        ("ss -tuln", "Show listening ports"),
        ("hostname", "Show hostname"),
        ("nslookup DOMAIN", "DNS lookup (basic)"),
        ("dig DOMAIN", "DNS lookup (advanced)"),
        ("host DOMAIN", "DNS lookup (simple)"),
        ("curl -I URL", "Fetch HTTP headers"),
        ('curl -o /dev/null -w "%{http_code}" URL', "Get HTTP status code"),
    ]
    best_practices = (
        "<ul style='list-style:none;padding:0;margin:0;'>"
        "<li style='padding-left:14px;position:relative;margin-bottom:4px;'>"
        "<span style='position:absolute;left:0;color:var(--green);'>✓</span> Always check HTTP status codes.</li>"
        "<li style='padding-left:14px;position:relative;margin-bottom:4px;'>"
        "<span style='position:absolute;left:0;color:var(--green);'>✓</span> Use timeouts to avoid hanging scripts.</li>"
        "<li style='padding-left:14px;position:relative;margin-bottom:4px;'>"
        "<span style='position:absolute;left:0;color:var(--green);'>✓</span> Check both connectivity and application health.</li>"
        "<li style='padding-left:14px;position:relative;margin-bottom:4px;'>"
        "<span style='position:absolute;left:0;color:var(--green);'>✓</span> Log results for monitoring and alerting.</li>"
        "<li style='padding-left:14px;position:relative;margin-bottom:4px;'>"
        "<span style='position:absolute;left:0;color:var(--green);'>✓</span> Use meaningful alerts when a service is down.</li>"
        "<li style='padding-left:14px;position:relative;margin-bottom:4px;'>"
        "<span style='position:absolute;left:0;color:var(--green);'>✓</span> Test from the same network as users.</li>"
        "<li style='padding-left:14px;position:relative;'>"
        "<span style='position:absolute;left:0;color:var(--green);'>✓</span> Keep scripts simple, clear, and maintainable.</li>"
        "</ul>"
    )
    sidebar = (
        card("list", "10. Quick Reference", tbl(["Command", "Description"], quick_ref_rows))
        + card("lightbulb", "Best Practices", best_practices)
    )

    key_takeaway = callout("tip", "lightbulb",
        "<strong>KEY TAKEAWAY:</strong> Automate your network checks. Detect issues early. "
        "Keep your systems and services reliable.")

    body = f"""
      <div class="body">
        <div class="rows">
{chr(10).join(rows_left)}
        </div>
        <div class="sidebar">
{sidebar}
        </div>
      </div>
      {key_takeaway}"""

    return page_wrapper(16, 20, title, subtitle, body)


# ---------------------------------------------------------------------------
# PAGE 17 — 16. Error Handling and Safer Scripts
# (file page-17.webp, original badge "PAGE 16")
# ---------------------------------------------------------------------------

def build_page_17():
    title = "16. Error Handling and Safer Scripts"
    subtitle = "WRITE PREDICTABLE. RELIABLE. SAFE AUTOMATION."

    # Use body single (full-width) — content is dense and vertical
    # We'll lay out 10 numbered sections, then safe-script example, then key takeaway.
    sec = []

    # 1. WHY SCRIPTS FAIL SILENTLY
    sec.append(row(
        "warning",
        "1. WHY SCRIPTS FAIL SILENTLY",
        '<p>By default, Bash continues even when commands fail.</p>'
        + terminal("bash", [
            '<span class="cmd">rm</span> file.txt',
            '<span class="cmd">echo</span> <span class="str">"Deleted"</span>',
            '<span class="cmd">echo</span> <span class="str">"Script finished"</span>',
        ])
        + callout("warn", "warning",
            "<strong>Problem:</strong> If <code class='inline'>rm</code> fails, the script keeps running and hides the error.")
    ))
    # 2. SET -E
    sec.append(row(
        "shield",
        "2. SET -E: EXIT ON ERROR",
        '<p>Exit immediately if any command fails.</p>'
        + terminal("bash", [
            '<span class="cmd">set</span> -e',
            '<span class="cmd">rm</span> file.txt',
            '<span class="cmd">echo</span> <span class="str">"This runs only if rm succeeds"</span>',
        ])
        + callout("tip", "check",
            "<strong>Benefit:</strong> Stops the script when a command fails.")
    ))
    # 3. SET -U
    sec.append(row(
        "lock-key",
        "3. SET -U: ERROR ON UNSET VARIABLES",
        '<p>Exit if you use a variable that is not set.</p>'
        + terminal("bash", [
            '<span class="cmd">set</span> -u',
            '<span class="cmd">echo</span> $UNSET_VAR',
        ])
        + callout("tip", "check",
            "<strong>Benefit:</strong> Catches typos and missing variables early.")
    ))
    # 4. SET -O PIPEFAIL
    sec.append(row(
        "arrow-right",
        "4. SET -O PIPEFAIL: CATCH PIPE ERRORS",
        '<p>Detect failures inside pipelines.</p>'
        + terminal("bash", [
            '<span class="cmd">set</span> -o pipefail',
            '<span class="cmd">cat</span> file.txt <span class="prompt">|</span> <span class="cmd">grep</span> <span class="str">"ERROR"</span> <span class="prompt">|</span> <span class="cmd">wc</span> -l',
        ])
        + callout("tip", "check",
            "<strong>Benefit:</strong> Without pipefail, only the last command's status is checked.")
    ))
    # 5. SET -EUO PIPEFAIL
    sec.append(row(
        "shield-check",
        "5. SET -EUO PIPEFAIL: STRONG & SAFE MODE",
        '<p>Best practice for safer scripts.</p>'
        + terminal("bash", [
            '<span class="cmd">set</span> -euo pipefail',
        ])
        + '<ul style="list-style:none;padding:0;margin:6px 0 0 0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:18px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Exit on any command error</li>'
        '<li style="padding-left:18px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Error on unset variables</li>'
        '<li style="padding-left:18px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Catch pipeline failures</li>'
        '</ul>'
    ))
    # 6. VALIDATING INPUTS
    sec.append(row(
        "clipboard",
        "6. VALIDATING INPUTS",
        '<p>Always verify inputs before using them.</p>'
        + terminal("bash", [
            '<span class="prompt">if</span> [ -z <span class="str">"$1"</span> ]; <span class="prompt">then</span>',
            '  <span class="cmd">echo</span> <span class="str">"Usage: $0 &lt;url&gt;"</span>',
            '  <span class="cmd">exit</span> 1',
            '<span class="prompt">fi</span>',
        ])
        + callout("tip", "check",
            "<strong>Benefit:</strong> Prevents errors and makes scripts user-friendly.")
    ))
    # 7. CHECKING DEPENDENCIES
    sec.append(row(
        "gear",
        "7. CHECKING DEPENDENCIES",
        '<p>Ensure required commands exist before running.</p>'
        + terminal("bash", [
            '<span class="prompt">if</span> ! <span class="cmd">command</span> -v curl <span class="prompt">&gt;/dev/null</span> 2&gt;&amp;1; <span class="prompt">then</span>',
            '  <span class="cmd">echo</span> <span class="str">"curl not found!"</span>',
            '  <span class="cmd">exit</span> 1',
            '<span class="prompt">fi</span>',
        ])
        + callout("tip", "check",
            "<strong>Benefit:</strong> Avoids failures due to missing tools.")
    ))
    # 8. HANDLING FAILED COMMANDS
    sec.append(row(
        "bug",
        "8. HANDLING FAILED COMMANDS",
        '<p>Check command results and handle failures.</p>'
        + terminal("bash", [
            '<span class="prompt">if</span> ! <span class="cmd">rm</span> file.txt; <span class="prompt">then</span>',
            '  <span class="cmd">echo</span> <span class="str">"Failed to remove file.txt"</span>',
            '  <span class="cmd">exit</span> 1',
            '<span class="prompt">fi</span>',
        ])
        + callout("tip", "check",
            "<strong>Benefit:</strong> React to failures and prevent bad outcomes.")
    ))
    # 9. CLEANING UP AFTER FAILURES
    sec.append(row(
        "broom",
        "9. CLEANING UP AFTER FAILURES",
        '<p>Use traps to clean up on exit or error.</p>'
        + terminal("bash", [
            '<span class="cmd">cleanup</span>() {',
            '  <span class="cmd">echo</span> <span class="str">"Cleaning up..."</span>',
            '  <span class="cmd">rm</span> -f temp.log',
            '}',
            '<span class="cmd">trap</span> cleanup EXIT',
        ])
        + callout("tip", "check",
            "<strong>Benefit:</strong> Keeps systems clean even when scripts fail.")
    ))
    # 10. WRITING PREDICTABLE AUTOMATION
    sec.append(row(
        "predictable",
        "10. WRITING PREDICTABLE AUTOMATION",
        '<div>'
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Fail fast</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Validate inputs</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Check dependencies</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Handle errors</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Clean up properly</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Log what happens</li>'
        '<li style="padding-left:18px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">✔</span> Exit with the right status code</li>'
        '</ul>'
        '<p style="margin-top:6px;font-size:12px;color:var(--ink-2);"><strong>Result:</strong> Reliable and predictable automation every time.</p>'
        '</div>'
    ))

    # EXAMPLE: SAFE SCRIPT TEMPLATE
    safe_script = f"""
      <div class="row" style="align-items:flex-start;">
        <div class="icon bg-green ic-green">{icon("terminal")}</div>
        <div class="text">
          <h3>EXAMPLE: SAFE SCRIPT TEMPLATE</h3>
          {terminal("safe-script.sh", [
            '<span class="comment">#!/bin/bash</span>',
            '<span class="cmd">set</span> -euo pipefail',
            '<span class="comment"># Check input</span>',
            '<span class="prompt">if</span> [ -z <span class="str">"$1"</span> ]; <span class="prompt">then</span>',
            '  <span class="cmd">echo</span> <span class="str">"Usage: $0 &lt;url&gt;"</span>',
            '  <span class="cmd">exit</span> 1',
            '<span class="prompt">fi</span>',
            '<span class="comment"># Check dependency</span>',
            '<span class="cmd">command</span> -v curl <span class="prompt">&gt;/dev/null</span> 2&gt;&amp;1 <span class="prompt">||</span> { <span class="cmd">echo</span> <span class="str">"curl not found!"</span>; <span class="cmd">exit</span> 1; }',
            '<span class="comment"># Function to cleanup</span>',
            '<span class="cmd">cleanup</span>() { <span class="cmd">echo</span> <span class="str">"Cleaning up..."</span>; <span class="cmd">rm</span> -f temp.log; }',
            '<span class="cmd">trap</span> cleanup EXIT',
            '<span class="comment"># Main logic</span>',
            '<span class="cmd">URL</span>=<span class="str">"$1"</span>',
            '<span class="cmd">HTTP_CODE</span>=$(<span class="cmd">curl</span> -s -o /dev/null -w <span class="str">"%{http_code}"</span> <span class="str">"$URL"</span>)',
            '<span class="prompt">if</span> [ <span class="str">"$HTTP_CODE"</span> -ge 200 ] <span class="prompt">&amp;&amp;</span> [ <span class="str">"$HTTP_CODE"</span> -lt 400 ]; <span class="prompt">then</span>',
            '  <span class="cmd">echo</span> <span class="str">"[$URL] is UP (HTTP $HTTP_CODE)"</span>',
            '<span class="prompt">else</span>',
            '  <span class="cmd">echo</span> <span class="str">"[$URL] is DOWN (HTTP $HTTP_CODE)"</span>',
            '  <span class="cmd">exit</span> 1',
            '<span class="prompt">fi</span>',
          ])}
        </div>
      </div>"""

    key_takeaway = callout("tip", "lightbulb",
        "<strong>KEY TAKEAWAY:</strong> Safe scripts = Less downtime, fewer bugs, and happier users. "
        "Always handle errors. Always clean up. Always be predictable.")

    body = f"""
      <div class="body single">
        <div class="rows">
{chr(10).join(sec)}
{safe_script}
        </div>
      </div>
      {key_takeaway}"""

    return page_wrapper(17, 20, title, subtitle, body)


# ---------------------------------------------------------------------------
# PAGE 18 — 18. Scheduling Scripts with Cron
# (file page-18.webp, original badge "PAGE 18")
# ---------------------------------------------------------------------------

def build_page_18():
    title = "18. Scheduling Scripts with Cron"
    subtitle = "AUTOMATE TASKS. SAVE TIME. STAY RELIABLE."

    sec = []
    # 1. WHAT CRON DOES
    sec.append(row(
        "clock",
        "1. WHAT CRON DOES",
        '<p>Cron runs commands or scripts automatically at scheduled times. '
        'Perfect for backups, cleanup, monitoring, reports, and more.</p>'
    ))
    # 2. UNDERSTANDING CRONTAB
    sec.append(row(
        "calendar",
        "2. UNDERSTANDING CRONTAB",
        '<p>Crontab is your personal cron schedule.</p>'
        + terminal("bash", [
            '<span class="cmd">crontab</span> -e    <span class="comment"># Edit</span>',
            '<span class="cmd">crontab</span> -l    <span class="comment"># List jobs</span>',
            '<span class="cmd">crontab</span> -r    <span class="comment"># Remove all jobs</span>',
        ])
    ))
    # 3. CRON TIMING SYNTAX
    sec.append(row(
        "list",
        "3. CRON TIMING SYNTAX",
        '<p>Five fields: <code class="inline">MIN HOUR DAY MONTH DOW</code></p>'
        + tbl(
            ["Field", "Range"],
            [
                ("MIN",   "0–59"),
                ("HOUR",  "0–23"),
                ("DAY",   "1–31"),
                ("MONTH", "1–12"),
                ("DOW",   "0–6 (0=Sun)"),
            ]
        )
        + '<p style="font-size:11px;margin-top:6px;font-weight:700;color:var(--green);">EXAMPLES</p>'
        + tbl(
            ["Pattern", "Meaning"],
            [
                ("* * * * *",   "Every minute"),
                ("0 * * * *",   "Every hour at :00"),
                ("0 2 * * *",   "Every day at 2:00 AM"),
                ("30 1 * * 1",  "Every Monday at 1:30 AM"),
                ("0 3 1 * *",   "1st day of every month at 3 AM"),
            ]
        )
    ))
    # 4. RUNNING SCRIPTS AUTOMATICALLY
    sec.append(row(
        "play",
        "4. RUNNING SCRIPTS AUTOMATICALLY",
        '<p>Add your cron job with <code class="inline">crontab -e</code>. '
        'Cron runs jobs in the background. No need to keep your terminal open. '
        'Great for hands-off automation.</p>'
    ))
    # 5. ENVIRONMENT DIFFERENCES IN CRON
    sec.append(row(
        "gear",
        "5. ENVIRONMENT DIFFERENCES IN CRON",
        '<p>Cron runs with a minimal environment. Your PATH, variables, and shell may be different. '
        'Use full paths in scripts. Set needed variables inside the script.</p>'
        + terminal("bash", [
            '<span class="cmd">PATH</span>=/usr/local/bin:/usr/bin:/bin',
            '<span class="cmd">export</span> PATH',
        ])
    ))
    # 6. LOGGING CRON OUTPUT
    sec.append(row(
        "log",
        "6. LOGGING CRON OUTPUT",
        '<p>Always log output for debugging. Redirect output and errors.</p>'
        + terminal("bash", [
            '<span class="comment">*/5 * * * * /path/to/script.sh \\</span>',
            '  <span class="prompt">&gt;&gt;</span> /var/log/mycron.log 2&gt;&amp;1',
        ])
    ))
    # 7. COMMON CRON FAILURES
    sec.append(row(
        "calendar-x",
        "7. COMMON CRON FAILURES",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--red);">✕</span> Wrong timing syntax</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--red);">✕</span> Script path incorrect</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--red);">✕</span> Script not executable</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--red);">✕</span> Missing environment variables</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--red);">✕</span> No permissions to run script</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--red);">✕</span> Output not logged</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--red);">✕</span> Mail not configured</li>'
        '<li style="padding-left:18px;position:relative;"><span style="position:absolute;left:0;color:var(--red);">✕</span> Cron service not running</li>'
        '</ul>'
    ))
    # 8. SCHEDULING BACKUP AND CLEANUP JOBS
    sec.append(row(
        "rocket",
        "8. SCHEDULING BACKUP AND CLEANUP JOBS",
        '<p>Two practical scheduled-job examples:</p>'
        + terminal("backup.log", [
            '<span class="comment"># EXAMPLE BACKUP JOB</span>',
            '0 2 * * * /backup.sh \\',
            '  <span class="prompt">&gt;&gt;</span> /var/log/backup.log 2&gt;&amp;1',
        ])
        + terminal("cleanup.log", [
            '<span class="comment"># EXAMPLE CLEANUP JOB</span>',
            '30 3 * * 0 /cleanup.sh \\',
            '  <span class="prompt">&gt;&gt;</span> /var/log/cleanup.log 2&gt;&amp;1',
        ])
    ))

    # Sidebar: cron syntax quick ref + best practices
    cron_ref_rows = [
        ("*", "Any value"),
        (",", "Values list (1,2,3)"),
        ("-", "Range (1-5)"),
        ("/", "Step values (*/10)"),
        ("0-59", "Minute"),
        ("0-23", "Hour"),
        ("1-31", "Day of month"),
        ("1-12", "Month"),
        ("0-6", "Day of week (0=Sun)"),
        ("@daily", "Same as 0 0 * * *"),
        ("@weekly", "Same as 0 0 * * 0"),
        ("@reboot", "Run once at startup"),
    ]
    best_practices = (
        "<ul style='list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);'>"
        "<li style='padding-left:18px;position:relative;margin-bottom:5px;'><span style='position:absolute;left:0;color:var(--green);'>✓</span> Use full paths for commands and scripts.</li>"
        "<li style='padding-left:18px;position:relative;margin-bottom:5px;'><span style='position:absolute;left:0;color:var(--green);'>✓</span> Log all cron outputs.</li>"
        "<li style='padding-left:18px;position:relative;margin-bottom:5px;'><span style='position:absolute;left:0;color:var(--green);'>✓</span> Test scripts manually before scheduling.</li>"
        "<li style='padding-left:18px;position:relative;margin-bottom:5px;'><span style='position:absolute;left:0;color:var(--green);'>✓</span> Keep cron jobs simple and reliable.</li>"
        "<li style='padding-left:18px;position:relative;'><span style='position:absolute;left:0;color:var(--green);'>✓</span> Review your crontab regularly.</li>"
        "</ul>"
    )
    sidebar = (
        card("list", "Cron Syntax Quick Reference",
             tbl(["Symbol", "Meaning"], cron_ref_rows))
        + card("lightbulb", "Best Practices", best_practices)
    )

    body = f"""
      <div class="body">
        <div class="rows">
{chr(10).join(sec)}
        </div>
        <div class="sidebar">
{sidebar}
        </div>
      </div>"""

    return page_wrapper(18, 20, title, subtitle, body)


# ---------------------------------------------------------------------------
# PAGE 19 — 17. Debugging Shell Scripts
# (file page-19.webp, original badge "PAGE 17")
# ---------------------------------------------------------------------------

def build_page_19():
    title = "17. Debugging Shell Scripts"
    subtitle = "FIND ISSUES. UNDERSTAND CAUSES. FIX FAST."

    sec = []
    # 1. READING SHELL ERRORS
    sec.append(row(
        "bug",
        "1. READING SHELL ERRORS",
        '<p>Errors tell you what went wrong. Read them carefully.</p>'
        + terminal("bash", [
            './script.sh: <span class="comment">line 10: mycmd: command not found</span>',
            './script.sh: <span class="comment">line 15: [ : : integer expression expected</span>',
            '<span class="comment">Permission denied</span>',
            '<span class="comment">No such file or directory</span>',
        ])
        + callout("tip", "lightbulb",
            "<strong>TIP:</strong> The error message always gives a clue.")
    ))
    # 2. DEBUG MODE WITH bash -x
    sec.append(row(
        "terminal",
        "2. DEBUG MODE WITH bash -x",
        '<p>Run your script with <code class="inline">bash -x</code> to see each command.</p>'
        + terminal("bash", [
            '<span class="prompt">$</span> <span class="cmd">bash</span> -x script.sh',
            '<div class="comment"># Example output:</div>',
            '+ <span class="cmd">echo</span> <span class="str">"Starting"</span>',
            'Starting',
            '+ VAR=hello',
            '+ <span class="cmd">echo</span> $VAR',
            'hello',
            '+ <span class="cmd">ls</span> /not/exist',
            'ls: cannot access <span class="str">\'/not/exist\'</span>: No such file or directory',
        ])
    ))
    # 3. DEBUG MODE INSIDE SCRIPT
    sec.append(row(
        "gear",
        "3. DEBUG MODE INSIDE SCRIPT",
        '<p>Use <code class="inline">set -x</code> to enable debug inside the script.</p>'
        + terminal("bash", [
            '<span class="cmd">set</span> -x',
            '<span class="comment"># Your commands here</span>',
            '<span class="cmd">set</span> +x   <span class="comment"># Turn off debug</span>',
        ])
        + callout("tip", "check",
            "<strong>BENEFIT:</strong> Shows each command as it runs. Very helpful to trace issues.")
    ))
    # 4. COMMON PROBLEMS AND HOW TO FIND THEM
    problems_html = (
        '<p style="font-size:12px;color:var(--ink-2);">Six common failure categories:</p>'
        '<div class="compare">'
        '<div class="col left">'
        '<h4>A. SYNTAX ERRORS</h4>'
        '<p>Missing symbols or wrong structure.</p>'
        '<div style="font-family:monospace;font-size:10px;background:#fff;padding:6px;border-radius:4px;margin-top:4px;">'
        'if [ "${VAR}" = "test" ]<br>echo "Missing fi"<br><span style="color:var(--red);"># Error here</span>'
        '</div>'
        '<p style="margin-top:4px;font-size:10px;"><strong>Fix:</strong> Check brackets, quotes, then/fi, do/done.</p>'
        '</div>'
        '<div class="col left">'
        '<h4>B. QUOTING PROBLEMS</h4>'
        '<p>Wrong quotes break the script.</p>'
        '<div style="font-family:monospace;font-size:10px;background:#fff;padding:6px;border-radius:4px;margin-top:4px;">'
        'echo "Hello $USER"    # Good<br>'
        'echo \'Hello $USER\'    # Literal<br>'
        'echo "He said "hi""   # Bad'
        '</div>'
        '<p style="margin-top:4px;font-size:10px;"><strong>FIX:</strong> Use double quotes for variables. Escape inner quotes.</p>'
        '</div>'
        '</div>'
        '<div class="compare" style="margin-top:8px;">'
        '<div class="col left">'
        '<h4>C. MISSING VARIABLES</h4>'
        '<p>Using variables that are not set.</p>'
        '<div style="font-family:monospace;font-size:10px;background:#fff;padding:6px;border-radius:4px;margin-top:4px;">'
        'echo $NAME<br>'
        './script.sh: line 5: NAME: unbound variable'
        '</div>'
        '<p style="margin-top:4px;font-size:10px;"><strong>Fix:</strong> Define the variable or use default: ${NAME:-John}</p>'
        '</div>'
        '<div class="col left">'
        '<h4>D. PERMISSION ERRORS</h4>'
        '<p>Script or files are not executable.</p>'
        '<div style="font-family:monospace;font-size:10px;background:#fff;padding:6px;border-radius:4px;margin-top:4px;">'
        './script.sh: line 3:<br>./other.sh: Permission denied'
        '</div>'
        '<p style="margin-top:4px;font-size:10px;"><strong>Fix:</strong> Use chmod +x script.sh and check file permissions.</p>'
        '</div>'
        '</div>'
        '<div class="compare" style="margin-top:8px;">'
        '<div class="col left">'
        '<h4>E. PATH PROBLEMS</h4>'
        '<p>Command not found.</p>'
        '<div style="font-family:monospace;font-size:10px;background:#fff;padding:6px;border-radius:4px;margin-top:4px;">'
        'mycmd: command not found'
        '</div>'
        '<p style="margin-top:4px;font-size:10px;"><strong>Fix:</strong> Check PATH or use full path: /usr/bin/mycmd</p>'
        '</div>'
        '<div class="col left">'
        '<h4>F. FILE OR DIRECTORY MISSING</h4>'
        '<p>File or directory does not exist.</p>'
        '<div style="font-family:monospace;font-size:10px;background:#fff;padding:6px;border-radius:4px;margin-top:4px;">'
        'cat: file.txt: No such file or directory'
        '</div>'
        '<p style="margin-top:4px;font-size:10px;"><strong>Fix:</strong> Check the path and filename. Use absolute path if needed.</p>'
        '</div>'
        '</div>'
    )
    sec.append(row(
        "puzzle",
        "4. COMMON PROBLEMS AND HOW TO FIND THEM",
        problems_html
    ))
    # 5. DEBUGGING SCRIPTS STEP BY STEP
    sec.append(row(
        "step",
        "5. DEBUGGING SCRIPTS STEP BY STEP",
        steps([
            "<strong>Read the error</strong> — Understand what the error is saying. Look at the line number and message.",
            "<strong>Reproduce the issue</strong> — Run the script and confirm the error happens again.",
            "<strong>Run with bash -x</strong> — Use <code class='inline'>bash -x script.sh</code> to see each command and where it fails.",
            "<strong>Check variables and quotes</strong> — Make sure variables are set and quoted correctly.",
            "<strong>Fix and test again</strong> — Make the change and run again. Repeat until the error is gone.",
            "<strong>Remove debug</strong> — Remove <code class='inline'>set -x</code> or stop using <code class='inline'>bash -x</code> after fixing.",
        ])
    ))

    key_takeaway = callout("tip", "lightbulb",
        "<strong>KEY TAKEAWAY:</strong> Good debugging saves hours. "
        "Read errors. Use tools. Fix the root cause.")

    body = f"""
      <div class="body single">
        <div class="rows">
{chr(10).join(sec)}
        </div>
      </div>
      {key_takeaway}"""

    return page_wrapper(19, 20, title, subtitle, body)


# ---------------------------------------------------------------------------
# PAGE 20 — 19. Shell Scripting in DevOps Workflows
# (file page-20.webp, original badge "PAGE 19")
# ---------------------------------------------------------------------------

def build_page_20():
    title = "19. Shell Scripting in DevOps Workflows"
    subtitle = "AUTOMATE. INTEGRATE. DEPLOY."

    # 10 cards arranged in a 2-col grid. We'll model each card as a row.
    cards = []

    # 1. SHELL SCRIPTS IN CI/CD
    cards.append(row(
        "infinity",
        "1. SHELL SCRIPTS IN CI/CD",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Automate build, test, and deploy.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Run commands at every stage.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Make pipelines reliable and repeatable.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Handle setup, checks, and notifications.</li>'
        '</ul>'
    ))
    # 2. GITHUB ACTIONS
    cards.append(row(
        "github-actions",
        "2. GITHUB ACTIONS",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Use shell scripts in workflow steps.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Run custom commands easily.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Prepare environments.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Build, test, and deploy apps.</li>'
        '</ul>'
        + terminal("workflow.yml", [
            '- <span class="cmd">name</span>: Run script',
            '  <span class="cmd">run</span>: ./deploy.sh',
        ])
    ))
    # 3. JENKINS
    cards.append(row(
        "jenkins",
        "3. JENKINS",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Execute shell scripts in build steps.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Automate jobs and deployments.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Manage environments.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Integrate with other tools.</li>'
        '</ul>'
        + terminal("jenkins.sh", [
            '<span class="comment">#!/bin/bash</span>',
            './build.sh <span class="prompt">&amp;&amp;</span> ./deploy.sh',
        ])
    ))
    # 4. DOCKER
    cards.append(row(
        "docker",
        "4. DOCKER",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Build and push images.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Prepare container environments.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Clean up unused resources.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Manage volumes and networks.</li>'
        '</ul>'
        + terminal("docker.sh", [
            '<span class="comment">#!/bin/bash</span>',
            '<span class="cmd">docker</span> build -t myapp .',
            '<span class="cmd">docker</span> push myapp:latest',
        ])
    ))
    # 5. KUBERNETES
    cards.append(row(
        "k8s",
        "5. KUBERNETES",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Automate kubectl commands.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Deploy and update applications.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Manage configs and secrets.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Check pod and service status.</li>'
        '</ul>'
        + terminal("k8s.sh", [
            '<span class="cmd">kubectl</span> apply -f app.yaml',
            '<span class="cmd">kubectl</span> rollout status deploy/app',
        ])
    ))
    # 6. CLOUD VM INITIALIZATION
    cards.append(row(
        "vm-cloud",
        "6. CLOUD VM INITIALIZATION",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Run scripts on first boot.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Install packages and tools.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Configure users and services.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Set up security and updates.</li>'
        '</ul>'
        + terminal("cloud-init.sh", [
            '<span class="comment">#!/bin/bash</span>',
            '<span class="cmd">apt</span> update <span class="prompt">&amp;&amp;</span> <span class="cmd">apt</span> install -y nginx',
            '<span class="cmd">systemctl</span> enable nginx',
        ])
    ))
    # 7. DEPLOYMENT SCRIPTS
    cards.append(row(
        "rocket-up",
        "7. DEPLOYMENT SCRIPTS",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Automate deployments.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Backup before updates.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Rollback on failure.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Zero- or low-downtime.</li>'
        '</ul>'
        + terminal("deploy.sh", [
            './deploy.sh --env prod',
            './rollback.sh',
        ])
    ))
    # 8. HEALTH CHECKS
    cards.append(row(
        "heart-pulse",
        "8. HEALTH CHECKS",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Check app and services.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Validate endpoints.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Alert on failure.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Keep systems reliable.</li>'
        '</ul>'
        + terminal("health.sh", [
            '<span class="comment">#!/bin/bash</span>',
            '<span class="cmd">curl</span> -f http://localhost/ <span class="prompt">||</span> <span class="cmd">exit</span> 1',
        ])
    ))
    # 9. ENVIRONMENT VALIDATION
    cards.append(row(
        "clipboard",
        "9. ENVIRONMENT VALIDATION",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Verify required tools.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Check variables and configs.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Validate dependencies.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Fail fast if something is wrong.</li>'
        '</ul>'
        + terminal("validate.sh", [
            '<span class="cmd">command</span> -v docker <span class="prompt">&gt;/dev/null</span> <span class="prompt">||</span> { <span class="cmd">echo</span> <span class="str">"Docker not found"</span>; <span class="cmd">exit</span> 1; }',
        ])
    ))
    # 10. WHERE SHELL SCRIPTING FITS IN DEVOPS
    cards.append(row(
        "puzzle",
        "10. WHERE SHELL SCRIPTING FITS IN DEVOPS",
        '<ul style="list-style:none;padding:0;margin:0;font-size:12px;color:var(--ink-2);">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Glue between tools.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Automate small and big tasks.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Provide flexibility.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">•</span> Save time and reduce errors.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">•</span> Core skill for every DevOps engineer.</li>'
        '</ul>'
    ))

    # Bottom summary section: workflow icons + callout
    flow_html = (
        '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;'
        'background:#fff;border:2px solid var(--green);border-radius:12px;padding:12px 16px;margin-top:14px;">'
        '<div style="display:flex;align-items:center;gap:10px;flex:1;">'
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;">{icon("terminal")}<span>Code</span></div>'
        f'<span style="color:var(--green);font-weight:800;">→</span>'
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;">{icon("gear")}<span>Build</span></div>'
        f'<span style="color:var(--green);font-weight:800;">→</span>'
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;">{icon("clipboard")}<span>Test</span></div>'
        f'<span style="color:var(--green);font-weight:800;">→</span>'
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;">{icon("rocket")}<span>Deploy</span></div>'
        f'<span style="color:var(--green);font-weight:800;">→</span>'
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;">{icon("server")}<span>Monitor</span></div>'
        '</div>'
        '<div style="display:flex;align-items:center;gap:8px;padding-left:14px;border-left:2px solid var(--green-light);">'
        f'<div style="width:32px;height:32px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;">{icon("check")}</div>'
        '<div style="font-size:11px;font-weight:700;color:var(--green);text-transform:uppercase;line-height:1.3;">One simple script can<br>automate hours of work.</div>'
        '</div>'
        '</div>'
    )
    summary = (
        f'<div style="margin-top:14px;">'
        f'<h3 style="font-size:14px;font-weight:800;color:var(--green);text-transform:uppercase;'
        f'letter-spacing:.5px;text-align:center;margin-bottom:8px;">'
        f'Shell Scripting is Everywhere in DevOps</h3>'
        f'{flow_html}'
        f'</div>'
    )

    body = f"""
      <div class="body single">
        <div class="rows">
{chr(10).join(cards)}
        </div>
      </div>
      {summary}"""

    return page_wrapper(20, 20, title, subtitle, body)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    builders = [
        (16, build_page_16),
        (17, build_page_17),
        (18, build_page_18),
        (19, build_page_19),
        (20, build_page_20),
    ]
    for n, fn in builders:
        html = fn()
        out = os.path.join(OUT_DIR, f"recreated-page-{n}.html")
        with open(out, "w") as f:
            f.write(html)
        size_kb = os.path.getsize(out) / 1024
        print(f"  wrote {out}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
