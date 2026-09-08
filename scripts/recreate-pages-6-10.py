#!/usr/bin/env python3
"""
Recreate carousel pages 6-10 as self-contained HTML files.

Reads:
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/page-06.webp
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/page-07.webp
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/page-08.webp
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/page-09.webp
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/page-10.webp

Writes:
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/recreated-page-06.html
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/recreated-page-07.html
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/recreated-page-08.html
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/recreated-page-09.html
  /home/z/my-project/downloads/instagram-DcaW1UljsVk/recreated-page-10.html

The shared template (`build_shell_scripting_template.py`) provides:
  NOTEBOOK_CSS, ICONS, icon(name), page_wrapper(page_num, total, title, subtitle, body_html)

Note on file/badge numbering:
  - The downloaded files are named page-NN.webp where NN is the carousel image order.
  - The page badge shown ON each image is sometimes off-by-one or off-by-two
    because the Instagram carousel's cover counts as a slide but the badges
    start at "PAGE 1" for the first content slide.
  - We use the actual page badge number from each image (verified via VLM) so
    the recreated HTML matches the original carousel page exactly.
  - File numbering is preserved for the output file names (page-06.html, etc.).
"""

import os
import sys

# Make sibling template importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_shell_scripting_template import icon, page_wrapper  # noqa: E402


# ============================================================
# Extra inline SVGs for icons not in the shared ICONS dict
# ============================================================
def svg(name: str) -> str:
    """Return an inline SVG by name (extra icons + fallback to template dict)."""
    extras = {
        "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><circle cx="7" cy="7" r="1.2" fill="currentColor"/></svg>',
        "refresh": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10"/><path d="M20.49 15A9 9 0 0 1 5.64 18.36L1 14"/></svg>',
        "branch": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>',
        "code-braces": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
        "power": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18.36 6.64a9 9 0 1 1-12.73 0"/><line x1="12" y1="2" x2="12" y2="12"/></svg>',
        "chevron-right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>',
        "stop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="5" width="14" height="14" rx="2"/></svg>',
        "skip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 4 15 12 5 20"/><line x1="19" y1="5" x2="19" y2="19"/></svg>',
        "intersect": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="6"/><circle cx="15" cy="15" r="6"/></svg>',
        "exit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
        "dollar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/></svg>',
        "swap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>',
        "alert-triangle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><circle cx="12" cy="17" r="0.5" fill="currentColor"/></svg>',
    }
    if name in extras:
        return extras[name]
    return icon(name)


# ============================================================
# Helper HTML builders
# ============================================================
def row(icon_name: str, bg: str, ic_color: str, heading: str, body_html: str) -> str:
    """Build a `.row` block with icon + heading + body text."""
    return (
        f'<div class="row">'
        f'<div class="icon {bg} {ic_color}">{svg(icon_name)}</div>'
        f'<div class="text"><h3>{heading}</h3>{body_html}</div>'
        f'</div>'
    )


def terminal(title: str, body_html: str) -> str:
    """Build a `.terminal` block with macOS-style title bar."""
    return (
        f'<div class="terminal">'
        f'<div class="term-bar">'
        f'<span class="term-dot dot-red"></span>'
        f'<span class="term-dot dot-amber"></span>'
        f'<span class="term-dot dot-green"></span>'
        f'<span class="term-title">{title}</span>'
        f'</div>'
        f'<div class="term-body">{body_html}</div>'
        f'</div>'
    )


def card(head_icon: str, head_text: str, body_html: str) -> str:
    """Build a `.card` sidebar item."""
    return (
        f'<div class="card">'
        f'<div class="head">{svg(head_icon)}<span>{head_text}</span></div>'
        f'<div class="body-pad">{body_html}</div>'
        f'</div>'
    )


def callout(kind: str, ico: str, text_html: str) -> str:
    """Build a `.callout` (warn/tip) box."""
    return (
        f'<div class="callout {kind}">'
        f'<span class="ico {("ic-orange" if kind == "warn" else "ic-green")}">{svg(ico)}</span>'
        f'<div>{text_html}</div>'
        f'</div>'
    )


# ============================================================
# PAGE 6  (file: page-06.webp → badge: PAGE 4 OF 20)
# Title: 4. VARIABLES AND ENVIRONMENT VARIABLES
# Subtitle: STORE DATA. REUSE. AUTOMATE.
# ============================================================
def body_page_06() -> str:
    # Left column rows (sections 1-6)
    left_rows = "".join([
        row("tag", "bg-green", "ic-green", "1. Creating Variables",
            '<p>No spaces around <code>=</code> sign.</p>'
            '<div style="margin-top:6px;">' +
            terminal("variables.sh",
                '<span class="cmd">NAME</span>=<span class="str">DevOps</span><br>'
                '<span class="cmd">COUNT</span>=<span class="str">5</span>'
            ) + '</div>'),

        row("chevron-right", "bg-blue", "ic-blue", "2. Reading Variables",
            '<p>Use <code>$</code> to read a variable.</p>'
            '<div style="margin-top:6px;">' +
            terminal("read.sh",
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$NAME</span><br>'
                '<span class="out">DevOps</span>'
            ) + '</div>'),

        row("info", "bg-purple", "ic-purple", "3. Quoting Variables",
            '<ul style="list-style:none;padding:0;margin:0 0 4px 0;font-size:12px;color:var(--ink-2);line-height:1.45;">'
            '<li style="padding-left:12px;position:relative;margin-bottom:2px;"><span style="position:absolute;left:0;">•</span>Use quotes to handle spaces.</li>'
            '<li style="padding-left:12px;position:relative;margin-bottom:2px;"><span style="position:absolute;left:0;">•</span>Prevents word splitting.</li>'
            '<li style="padding-left:12px;position:relative;"><span style="position:absolute;left:0;">•</span>Prevents filename expansion.</li>'
            '</ul>'
            '<div style="margin-top:4px;">' +
            terminal("quote.sh",
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">"$NAME"</span><br>'
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">\'$NAME\'</span>'
            ) + '</div>'),

        row("swap", "bg-gold", "ic-gold", "4. Command Substitution",
            '<p>Store the output of a command.</p>'
            '<div style="margin-top:6px;">' +
            terminal("substitution.sh",
                '<span class="prompt">$</span> <span class="cmd">DATE</span>=$(<span class="cmd">date</span> +%Y-%m-%d)<br>'
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$DATE</span><br>'
                '<span class="out">2025-05-18</span>'
            ) + '</div>'),

        row("arrow-right", "bg-teal", "ic-teal", "5. Export Variables",
            '<ul style="list-style:none;padding:0;margin:0 0 4px 0;font-size:12px;color:var(--ink-2);line-height:1.45;">'
            '<li style="padding-left:12px;position:relative;"><span style="position:absolute;left:0;">•</span>Makes a variable available to child processes.</li>'
            '<li style="padding-left:12px;position:relative;"><span style="position:absolute;left:0;">•</span>Use <code>export</code>.</li>'
            '</ul>'
            '<div style="margin-top:4px;">' +
            terminal("export.sh",
                '<span class="prompt">$</span> <span class="cmd">export</span> PROJECT=<span class="str">MyApp</span><br>'
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$PROJECT</span><br>'
                '<span class="out">MyApp</span>'
            ) + '</div>'),

        row("server", "bg-green", "ic-green", "6. Environment Variables",
            '<p>Set by the system. Available in every shell.</p>'
            '<div style="margin-top:6px;">' +
            terminal("env.sh",
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$HOME</span><br>'
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$USER</span><br>'
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$SHELL</span><br>'
                '<span class="prompt">$</span> <span class="cmd">echo</span> <span class="str">$LANG</span>'
            ) + '</div>'),
    ])

    # Right sidebar cards
    env_table = (
        '<table class="tbl">'
        '<thead><tr><th>Var</th><th>Meaning</th><th>Example</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>$HOME</code></td><td>Your home directory</td><td>/home/user</td></tr>'
        '<tr><td><code>$USER</code></td><td>Current logged-in user</td><td>user</td></tr>'
        '<tr><td><code>$PATH</code></td><td>Command search dirs</td><td>/usr/bin:/bin:/usr/local/bin</td></tr>'
        '</tbody>'
        '</table>'
    )
    full_script = (
        '<span class="comment">#!/bin/bash</span><br>'
        '<span class="cmd">APP_NAME</span>=<span class="str">"MyApp"</span><br>'
        '<span class="cmd">LOG_DIR</span>=<span class="str">"$HOME/logs"</span><br>'
        '<span class="cmd">mkdir</span> -p <span class="str">"$LOG_DIR"</span><br>'
        '<span class="cmd">echo</span> <span class="str">"Starting $APP_NAME...."</span><br>'
        '<span class="cmd">echo</span> <span class="str">"Logs will be saved in $LOG_DIR"</span>'
    )
    best_practices = (
        '<ul style="list-style:none;padding:0;margin:0;font-size:11px;color:var(--ink-2);line-height:1.55;">'
        '<li style="padding-left:16px;position:relative;margin-bottom:2px;"><span style="position:absolute;left:0;color:var(--green);font-weight:700;">✓</span>Always use quotes when in doubt.</li>'
        '<li style="padding-left:16px;position:relative;margin-bottom:2px;"><span style="position:absolute;left:0;color:var(--green);font-weight:700;">✓</span>Use meaningful variable names.</li>'
        '<li style="padding-left:16px;position:relative;margin-bottom:2px;"><span style="position:absolute;left:0;color:var(--green);font-weight:700;">✓</span>Export only what you need.</li>'
        '<li style="padding-left:16px;position:relative;margin-bottom:2px;"><span style="position:absolute;left:0;color:var(--green);font-weight:700;">✓</span>Keep variables uppercase for constants.</li>'
        '<li style="padding-left:16px;position:relative;margin-bottom:2px;"><span style="position:absolute;left:0;color:var(--green);font-weight:700;">✓</span>Use command substitution <code>$( )</code> often.</li>'
        '<li style="padding-left:16px;position:relative;"><span style="position:absolute;left:0;color:var(--green);font-weight:700;">✓</span>Test your scripts with different values.</li>'
        '</ul>'
    )
    sidebar_cards = "".join([
        card("list", "Common Env Variables", env_table),
        card("terminal", "8. Using Variables in Scripts",
             terminal("app.sh", full_script)),
        callout("tip", "lightbulb",
                '<strong>9. Best Practices</strong><br>' + best_practices),
    ])

    body = (
        '<div class="body">'
        f'<div class="rows">{left_rows}</div>'
        f'<div class="sidebar">{sidebar_cards}</div>'
        f'</div>'
    )
    return body


# ============================================================
# PAGE 7  (file: page-07.webp → badge: PAGE 6 OF 20)
# Title: 6. EXIT CODES AND COMMAND SUCCESS
# Subtitle: EVERY COMMAND RETURNS A STATUS.
# ============================================================
def body_page_07() -> str:
    exit_rules_tbl = (
        '<table class="tbl">'
        '<thead><tr><th>Code</th><th>Type</th><th>Meaning</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>0</code></td><td>Success</td><td>Command completed successfully.</td></tr>'
        '<tr><td><code>1+</code></td><td>Non-zero</td><td>Failure — something went wrong. Check the error.</td></tr>'
        '</tbody>'
        '</table>'
    )
    examples_term = (
        '<span class="prompt">$</span> <span class="cmd">ls</span> /home; <span class="cmd">echo</span> <span class="str">$?</span><br>'
        '<span class="out">0</span><br><br>'
        '<span class="prompt">$</span> <span class="cmd">ls</span> /notfoundfolder; <span class="cmd">echo</span> <span class="str">$?</span><br>'
        '<span class="out">2</span><br><br>'
        '<span class="prompt">$</span> <span class="cmd">cat</span> file.txt; <span class="cmd">echo</span> <span class="str">$?</span><br>'
        '<span class="out">0 or 1+</span>'
    )
    exit_cmd_term = (
        '<span class="keyword" style="color:#ff7b72;">if</span> [ ! -f file.txt ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"File not found!"</span><br>'
        '&nbsp;&nbsp;<span class="cmd">exit</span> 1<br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span><br><br>'
        '<span class="comment"># exit 0 = success</span><br>'
        '<span class="comment"># exit 1 = failure</span><br>'
        '<span class="comment"># Ends the script with a status.</span>'
    )
    test_success_term = (
        '<span class="cmd">ls</span> /home<br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ <span class="str">$?</span> -eq 0 ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Success"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Failed"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span>'
    )

    left_rows = "".join([
        row("info", "bg-blue", "ic-blue", "1. What Exit Codes Mean",
            '<p>After any command runs, the system returns a number called an <strong>exit code</strong>. It tells you if the command succeeded or failed.</p>'
            '<p style="margin-top:4px;"><code>echo $?</code> &mdash; Shows the exit code of the last command.</p>'),

        row("list", "bg-green", "ic-green", "2. Basic Exit Code Rules",
            '<p>Codes follow a simple convention:</p>'
            f'<div style="margin-top:6px;">{exit_rules_tbl}</div>'),

        row("terminal", "bg-purple", "ic-purple", "3. Examples",
            '<p>See exit codes in action for common commands.</p>'
            f'<div style="margin-top:6px;">{terminal("examples.sh", examples_term)}</div>'),

        row("power", "bg-gold", "ic-gold", "4. The exit Command",
            '<p>Use <code>exit</code> to end a script and return a code. <code>exit 0</code> = success, <code>exit 1</code> = failure.</p>'
            f'<div style="margin-top:6px;">{terminal("exit-cmd.sh", exit_cmd_term)}</div>'),

        row("check-square", "bg-teal", "ic-teal", "5. Testing Command Success",
            '<p>Use exit codes in conditions. <code>$? -eq 0</code> = success, <code>$? -ne 0</code> = failure.</p>'
            f'<div style="margin-top:6px;">{terminal("test-success.sh", test_success_term)}</div>'),
    ])

    cicd_card = card("rocket", "6. Why CI/CD Pipelines Depend on Exit Codes",
        '<ul style="list-style:none;padding:0;margin:0;font-size:11px;color:var(--ink-2);line-height:1.55;">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">●</span>Each step returns an exit code.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">●</span>CI/CD tools stop the pipeline on failure.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">●</span>Exit code 0 = pipeline continues.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">●</span>Exit code 1+ = pipeline fails.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">●</span>Ensures reliable and consistent deployments.</li>'
        '</ul>')

    prevent_card = card("shield", "7. Preventing Silent Automation Failures",
        '<ul style="list-style:none;padding:0;margin:0;font-size:11px;color:var(--ink-2);line-height:1.5;">'
        '<li style="padding-left:14px;position:relative;margin-bottom:5px;"><span style="position:absolute;left:0;color:var(--green);">✓</span><strong>Always check exit codes.</strong> Don\'t ignore command results.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:5px;"><span style="position:absolute;left:0;color:var(--green);">✓</span><strong>Use <code>set -e</code> to exit on error.</strong> Stops the script on first failure.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:5px;"><span style="position:absolute;left:0;color:var(--green);">✓</span><strong>Log errors clearly.</strong> Makes debugging much easier.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:5px;"><span style="position:absolute;left:0;color:var(--green);">✓</span><strong>Validate inputs before running.</strong> Bad inputs cause unexpected failures.</li>'
        '<li style="padding-left:14px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">✓</span><strong>Test your scripts regularly.</strong> Catches issues early.</li>'
        '</ul>')

    sidebar_cards = "".join([
        cicd_card,
        prevent_card,
        callout("tip", "lightbulb",
                '<strong>TIP:</strong> Never ignore exit codes. Check them, handle them, and your scripts will be reliable and safe.'),
    ])

    body = (
        '<div class="body">'
        f'<div class="rows">{left_rows}</div>'
        f'<div class="sidebar">{sidebar_cards}</div>'
        '</div>'
    )
    return body


# ============================================================
# PAGE 8  (file: page-08.webp → badge: PAGE 7 OF 20)
# Title: 7. CONDITIONAL STATEMENTS
# Subtitle: MAKE SMART DECISIONS IN YOUR SCRIPTS.
# ============================================================
def body_page_08() -> str:
    syntax_term = (
        '<span class="keyword" style="color:#ff7b72;">if</span> [ condition ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;commands<br>'
        '<span class="keyword" style="color:#ff7b72;">elif</span> [ condition ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;commands<br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;commands<br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span>'
    )
    keyword_tbl = (
        '<table class="tbl">'
        '<thead><tr><th>Keyword</th><th>Purpose</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>if</code></td><td>Start condition</td></tr>'
        '<tr><td><code>then</code></td><td>Run if true</td></tr>'
        '<tr><td><code>elif</code></td><td>Else if another condition</td></tr>'
        '<tr><td><code>else</code></td><td>Run if all false</td></tr>'
        '<tr><td><code>fi</code></td><td>End condition</td></tr>'
        '</tbody>'
        '</table>'
    )
    numeric_tbl = (
        '<table class="tbl">'
        '<thead><tr><th>Op</th><th>Meaning</th><th>Example</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>-eq</code></td><td>Equal</td><td><code>[ $a -eq $b ]</code></td></tr>'
        '<tr><td><code>-ne</code></td><td>Not equal</td><td><code>[ $a -ne $b ]</code></td></tr>'
        '<tr><td><code>-gt</code></td><td>Greater than</td><td><code>[ $a -gt $b ]</code></td></tr>'
        '<tr><td><code>-lt</code></td><td>Less than</td><td><code>[ $a -lt $b ]</code></td></tr>'
        '<tr><td><code>-ge</code></td><td>Greater or equal</td><td><code>[ $a -ge $b ]</code></td></tr>'
        '<tr><td><code>-le</code></td><td>Less or equal</td><td><code>[ $a -le $b ]</code></td></tr>'
        '</tbody>'
        '</table>'
    )
    string_tbl = (
        '<table class="tbl">'
        '<thead><tr><th>Op</th><th>Meaning</th><th>Example</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>=</code></td><td>Equal</td><td><code>[ "$a" = "$b" ]</code></td></tr>'
        '<tr><td><code>!=</code></td><td>Not equal</td><td><code>[ "$a" != "$b" ]</code></td></tr>'
        '<tr><td><code>-z</code></td><td>String is empty</td><td><code>[ -z "$a" ]</code></td></tr>'
        '<tr><td><code>-n</code></td><td>String not empty</td><td><code>[ -n "$a" ]</code></td></tr>'
        '</tbody>'
        '</table>'
    )
    file_tbl = (
        '<table class="tbl">'
        '<thead><tr><th>Op</th><th>Meaning</th><th>Example</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>-f</code></td><td>File exists</td><td><code>[ -f file.txt ]</code></td></tr>'
        '<tr><td><code>-d</code></td><td>Directory exists</td><td><code>[ -d /home/user ]</code></td></tr>'
        '<tr><td><code>-e</code></td><td>File or directory exists</td><td><code>[ -e /tmp/log ]</code></td></tr>'
        '<tr><td><code>-r</code></td><td>Readable</td><td><code>[ -r file.txt ]</code></td></tr>'
        '<tr><td><code>-w</code></td><td>Writable</td><td><code>[ -w file.txt ]</code></td></tr>'
        '<tr><td><code>-x</code></td><td>Executable</td><td><code>[ -x script.sh ]</code></td></tr>'
        '<tr><td><code>-s</code></td><td>File is not empty</td><td><code>[ -s file.txt ]</code></td></tr>'
        '</tbody>'
        '</table>'
    )
    checks_term = (
        '<span class="comment"># Check if a file exists</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ -f /etc/passwd ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"File exists"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"File not found"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span><br><br>'
        '<span class="comment"># Check if a directory exists</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ -d /var/log ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Directory exists"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Directory not found"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span><br><br>'
        '<span class="comment"># Check if a service is running</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> <span class="cmd">systemctl</span> is-active --quiet nginx; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Nginx is running"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Nginx is not running"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span>'
    )
    practical_term = (
        '<span class="comment"># Check disk space and act based on the result.</span><br>'
        '<span class="cmd">USAGE</span>=$(<span class="cmd">df</span> / | <span class="cmd">awk</span> <span class="str">\'NR==2 {print $5}\'</span> | <span class="cmd">tr</span> -d <span class="str">\'%\'</span>)<br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ <span class="str">"$USAGE"</span> -gt 80 ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Disk usage is high: ${USAGE}%"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">elif</span> [ <span class="str">"$USAGE"</span> -gt 60 ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Disk usage is moderate: ${USAGE}%"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Disk usage is normal: ${USAGE}%"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span>'
    )

    left_rows = "".join([
        row("code-braces", "bg-green", "ic-green", "1. Basic Syntax",
            '<p>The shell uses <code>if</code>, <code>then</code>, <code>elif</code>, <code>else</code>, and <code>fi</code> to build conditional blocks.</p>'
            f'<div style="margin-top:6px;">{terminal("conditional.sh", syntax_term)}</div>'),

        row("list", "bg-blue", "ic-blue", "2. Numeric Comparisons",
            '<p>Use these operators inside <code>[ ]</code> to compare numbers:</p>'
            f'<div style="margin-top:6px;">{numeric_tbl}</div>'),

        row("info", "bg-purple", "ic-purple", "3. String Comparisons",
            '<p>Compare strings with these operators. <strong>Always quote strings!</strong> Prevents errors with spaces.</p>'
            f'<div style="margin-top:6px;">{string_tbl}</div>'),

        row("file", "bg-gold", "ic-gold", "4. File Tests",
            '<p>Test files and directories before acting on them:</p>'
            f'<div style="margin-top:6px;">{file_tbl}</div>'),
    ])

    sidebar_cards = "".join([
        card("list", "Quick Reference (Keywords)",
             keyword_tbl),
        card("check-square", "5. Checking Services, Files, or Directories",
             terminal("checks.sh", checks_term)),
        card("gear", "6. Practical Example",
             '<p style="font-size:11px;color:var(--ink-2);margin-bottom:6px;">Check disk space and act based on the result.</p>'
             + terminal("disk-check.sh", practical_term)),
        callout("tip", "lightbulb",
                '<strong>TIP:</strong> Conditions make your scripts intelligent. Always test, validate, and handle every situation.'),
    ])

    body = (
        '<div class="body">'
        f'<div class="rows">{left_rows}</div>'
        f'<div class="sidebar">{sidebar_cards}</div>'
        '</div>'
    )
    return body


# ============================================================
# PAGE 9  (file: page-09.webp → badge: PAGE 8 OF 20)
# Title: 8. LOGICAL OPERATORS AND MULTIPLE CONDITIONS
# Subtitle: COMBINE TESTS. MAKE SMARTER DECISIONS.
# ============================================================
def body_page_09() -> str:
    operators_tbl = (
        '<table class="tbl">'
        '<thead><tr><th>Op</th><th>Meaning</th><th>Example</th></tr></thead>'
        '<tbody>'
        '<tr><td><code>&amp;&amp;</code></td><td>AND &mdash; both must be true</td><td><code>if [ $a -gt 5 ] &amp;&amp; [ $b -lt 10 ]</code></td></tr>'
        '<tr><td><code>||</code></td><td>OR &mdash; at least one true</td><td><code>if [ $a -gt 5 ] || [ $b -lt 10 ]</code></td></tr>'
        '<tr><td><code>!</code></td><td>NOT &mdash; reverses the result</td><td><code>if ! [ -f file.txt ]</code></td></tr>'
        '</tbody>'
        '</table>'
    )
    short_circuit = (
        '<ul style="list-style:none;padding:0;margin:0;font-size:11px;color:var(--ink-2);line-height:1.5;">'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><code style="position:absolute;left:0;background:transparent;color:var(--green);">&amp;&amp;</code>If the first condition is false, the second is NOT executed.</li>'
        '<li style="padding-left:14px;position:relative;margin-bottom:3px;"><code style="position:absolute;left:0;background:transparent;color:var(--green);">||</code>If the first condition is true, the second is NOT executed.</li>'
        '<li style="padding-left:14px;position:relative;"><code style="position:absolute;left:0;background:transparent;color:var(--green);">!</code>Flips true to false, and false to true.</li>'
        '</ul>'
    )
    and_term = (
        '<span class="comment"># Both conditions must be true.</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ -f app.sh ] &amp;&amp; [ -x app.sh ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"File exists and is executable"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Check failed"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span>'
    )
    or_term = (
        '<span class="comment"># At least one condition must be true.</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ -f app.sh ] || [ -f app.py ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Script found"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"No script found"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span>'
    )
    not_term = (
        '<span class="comment"># Reverse a condition.</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ ! -f config.env ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Config file missing"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Config file exists"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span>'
    )
    combo_term = (
        '<span class="comment"># EXAMPLE 1: MIX &amp; OR</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ -f deploy.sh ] &amp;&amp; [ -x deploy.sh ] ||<br>'
        '&nbsp;&nbsp;&nbsp;[ -f deploy.py ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Ready to deploy"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Deployment script missing"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span><br>'
        '<span class="comment" style="color:#7ee787;">✓ Executable deploy.sh OR deploy.py exists.</span>'
    )
    combo_term_2 = (
        '<span class="comment"># EXAMPLE 2: NEGATION WITH AND</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ ! -f .lock ] &amp;&amp; [ -d /var/log ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Safe to proceed"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Lock file exists or log directory missing"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span><br>'
        '<span class="comment" style="color:#7ee787;">✓ No lock file AND directory exists.</span>'
    )
    combo_term_3 = (
        '<span class="comment"># EXAMPLE 3: COMPLEX COMBINATION</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ -f app.conf ] &amp;&amp; [ -r app.conf ] &amp;&amp;<br>'
        '&nbsp;&nbsp;&nbsp;! [ -z <span class="str">"$1"</span> ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"All checks passed"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Validation failed"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span><br>'
        '<span class="comment" style="color:#7ee787;">✓ File exists, readable AND first argument is not empty.</span>'
    )
    deploy_term = (
        '<span class="comment"># Before deploying, validate everything.</span><br>'
        '<span class="keyword" style="color:#ff7b72;">if</span> [ -f app.tar.gz ] &amp;&amp; [ -s app.tar.gz ] &amp;&amp; [ -x /usr/bin/docker ] &amp;&amp;<br>'
        '&nbsp;&nbsp;&nbsp;! <span class="cmd">systemctl</span> is-active --quiet app; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"All checks passed. Starting deployment..."</span><br>'
        '&nbsp;&nbsp;<span class="comment"># Your deployment commands here</span><br>'
        '<span class="keyword" style="color:#ff7b72;">else</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Deployment aborted. Check requirements."</span><br>'
        '&nbsp;&nbsp;<span class="cmd">exit</span> 1<br>'
        '<span class="keyword" style="color:#ff7b72;">fi</span>'
    )

    left_rows = "".join([
        row("intersect", "bg-green", "ic-green", "1. Logical Operators",
            '<p>Combine multiple tests with these three operators:</p>'
            f'<div style="margin-top:6px;">{operators_tbl}</div>'),

        row("lightbulb", "bg-gold", "ic-gold", "2. Short-Circuit Execution",
            short_circuit +
            '<p style="margin-top:6px;font-size:11px;color:var(--green);"><strong>💡 Saves time and prevents unnecessary checks.</strong></p>'),

        row("check-square", "bg-blue", "ic-blue", "3. AND Conditions ( &amp;&amp; )",
            '<p>Both conditions must be true.</p>'
            f'<div style="margin-top:6px;">{terminal("and.sh", and_term)}</div>'
            '<p style="margin-top:4px;font-size:11px;color:var(--green);">✅ Use for strict requirements.</p>'),

        row("check-square", "bg-purple", "ic-purple", "4. OR Conditions ( || )",
            '<p>At least one condition must be true.</p>'
            f'<div style="margin-top:6px;">{terminal("or.sh", or_term)}</div>'
            '<p style="margin-top:4px;font-size:11px;color:var(--green);">✅ Use for alternatives.</p>'),

        row("alert-triangle", "bg-gold", "ic-gold", "5. NOT Condition ( ! )",
            '<p>Reverse a condition.</p>'
            f'<div style="margin-top:6px;">{terminal("not.sh", not_term)}</div>'
            '<p style="margin-top:4px;font-size:11px;color:var(--green);">✅ Use to detect missing items.</p>'),
    ])

    sidebar_cards = "".join([
        card("puzzle", "6. Combining Multiple Tests",
             '<p style="font-size:11px;color:var(--ink-2);margin-bottom:6px;">Mix <code>&amp;&amp;</code>, <code>||</code>, and <code>!</code> for powerful checks.</p>'
             + terminal("combo.sh", combo_term)
             + '<div style="height:8px;"></div>'
             + terminal("negation.sh", combo_term_2)
             + '<div style="height:8px;"></div>'
             + terminal("complex.sh", combo_term_3)),
        card("rocket", "7. Safer Deployment Checks",
             '<p style="font-size:11px;color:var(--ink-2);margin-bottom:6px;">Before deploying, validate everything.</p>'
             + terminal("deploy-check.sh", deploy_term)
             + '<ul style="list-style:none;padding:0;margin:6px 0 0 0;font-size:10.5px;color:var(--green);line-height:1.5;">'
             '<li style="padding-left:14px;position:relative;">✓ File exists AND not empty</li>'
             '<li style="padding-left:14px;position:relative;">✓ Docker is installed</li>'
             '<li style="padding-left:14px;position:relative;">✓ App service is not running</li>'
             '<li style="padding-left:14px;position:relative;">✓ Proceed only when everything is correct</li>'
             '<li style="padding-left:14px;position:relative;">✓ Prevents failed or risky deployments</li>'
             '</ul>'),
        callout("tip", "lightbulb",
                '<strong>TIP:</strong> Combine checks, validate early, and fail fast. Smart conditions = reliable automation.'),
    ])

    body = (
        '<div class="body">'
        f'<div class="rows">{left_rows}</div>'
        f'<div class="sidebar">{sidebar_cards}</div>'
        '</div>'
    )
    return body


# ============================================================
# PAGE 10  (file: page-10.webp → badge: PAGE 9 OF 20)
# Title: 9. LOOPS FOR AUTOMATION
# Subtitle: REPEAT TASKS. SAVE TIME. ELIMINATE MANUAL WORK.
# ============================================================
def body_page_10() -> str:
    for_term = (
        '<span class="keyword" style="color:#ff7b72;">for</span> item <span class="keyword" style="color:#ff7b72;">in</span> a b c; <span class="keyword" style="color:#ff7b72;">do</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Item: $item"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">done</span><br><br>'
        '<span class="comment"># Output:</span><br>'
        '<span class="out">Item: a</span>&nbsp;&nbsp;<span class="out">Item: b</span>&nbsp;&nbsp;<span class="out">Item: c</span>'
    )
    while_term = (
        '<span class="cmd">count</span>=1<br>'
        '<span class="keyword" style="color:#ff7b72;">while</span> [ <span class="str">$count</span> -le 5 ]; <span class="keyword" style="color:#ff7b72;">do</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Count: $count"</span><br>'
        '&nbsp;&nbsp;<span class="cmd">count</span>=$((count + 1))<br>'
        '<span class="keyword" style="color:#ff7b72;">done</span><br><br>'
        '<span class="comment"># Output:</span> <span class="out">Count: 1 2 3 4 5</span>'
    )
    files_term = (
        '<span class="keyword" style="color:#ff7b72;">for</span> file <span class="keyword" style="color:#ff7b72;">in</span> *.txt; <span class="keyword" style="color:#ff7b72;">do</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"File: $file"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">done</span><br><br>'
        '<span class="comment"># Prints all .txt files in the current directory.</span>'
    )
    servers_term = (
        '<span class="keyword" style="color:#ff7b72;">for</span> server <span class="keyword" style="color:#ff7b72;">in</span> server1 server2 server3; <span class="keyword" style="color:#ff7b72;">do</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Checking $server..."</span><br>'
        '&nbsp;&nbsp;<span class="cmd">ssh</span> <span class="str">$server</span> <span class="cmd">uptime</span><br>'
        '<span class="keyword" style="color:#ff7b72;">done</span><br><br>'
        '<span class="comment"># Check uptime on many servers.</span>'
    )
    break_term = (
        '<span class="keyword" style="color:#ff7b72;">for</span> i <span class="keyword" style="color:#ff7b72;">in</span> {1..5}; <span class="keyword" style="color:#ff7b72;">do</span><br>'
        '&nbsp;&nbsp;<span class="keyword" style="color:#ff7b72;">if</span> [ <span class="str">$i</span> -eq 3 ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;<span class="keyword" style="color:#ff7b72;">break</span><br>'
        '&nbsp;&nbsp;<span class="keyword" style="color:#ff7b72;">fi</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Number: $i"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">done</span><br><br>'
        '<span class="comment"># Output:</span> <span class="out">Number: 1 2</span><br>'
        '<span class="comment"># STOP THE LOOP</span>'
    )
    continue_term = (
        '<span class="keyword" style="color:#ff7b72;">for</span> i <span class="keyword" style="color:#ff7b72;">in</span> {1..5}; <span class="keyword" style="color:#ff7b72;">do</span><br>'
        '&nbsp;&nbsp;<span class="keyword" style="color:#ff7b72;">if</span> [ <span class="str">$i</span> -eq 3 ]; <span class="keyword" style="color:#ff7b72;">then</span><br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;<span class="keyword" style="color:#ff7b72;">continue</span><br>'
        '&nbsp;&nbsp;<span class="keyword" style="color:#ff7b72;">fi</span><br>'
        '&nbsp;&nbsp;<span class="cmd">echo</span> <span class="str">"Number: $i"</span><br>'
        '<span class="keyword" style="color:#ff7b72;">done</span><br><br>'
        '<span class="comment"># Output:</span> <span class="out">Number: 1 2 4 5</span><br>'
        '<span class="comment"># SKIP AND CONTINUE</span>'
    )

    left_rows = "".join([
        row("refresh", "bg-green", "ic-green", "1. For Loops",
            '<p>Loop through a list of items.</p>'
            f'<div style="margin-top:6px;">{terminal("for.sh", for_term)}</div>'),

        row("refresh", "bg-blue", "ic-blue", "2. While Loops",
            '<p>Repeat while a condition is true.</p>'
            f'<div style="margin-top:6px;">{terminal("while.sh", while_term)}</div>'),

        row("file", "bg-gold", "ic-gold", "3. Looping Through Files",
            '<p>Process each file in a directory.</p>'
            f'<div style="margin-top:6px;">{terminal("files.sh", files_term)}</div>'),

        row("server", "bg-purple", "ic-purple", "4. Looping Through Servers",
            '<p>Run commands on multiple servers.</p>'
            f'<div style="margin-top:6px;">{terminal("servers.sh", servers_term)}</div>'),

        row("stop", "bg-red", "ic-red", "5. Break",
            '<p>Exit the loop immediately.</p>'
            f'<div style="margin-top:6px;">{terminal("break.sh", break_term)}</div>'),

        row("skip", "bg-teal", "ic-teal", "6. Continue",
            '<p>Skip the rest of the loop and continue.</p>'
            f'<div style="margin-top:6px;">{terminal("continue.sh", continue_term)}</div>'),
    ])

    infinite_warn = (
        '<p style="font-size:11px;color:var(--ink-2);margin-bottom:6px;">Always update your condition. Always change the variable inside the loop. Use clear exit conditions. Test with small values first.</p>'
        '<ul style="list-style:none;padding:0;margin:0;font-size:11px;color:var(--ink-2);line-height:1.55;">'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--orange);">⚠</span>Always change the variable inside the loop.</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--orange);">⚠</span>Use clear exit conditions.</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--orange);">⚠</span>Test your loops with small values first.</li>'
        '<li style="padding-left:18px;position:relative;"><span style="position:absolute;left:0;color:var(--orange);">⚠</span>Use <code>break</code> when needed.</li>'
        '</ul>'
    )
    auto_card = card("rocket", "8. Automating Repetitive Tasks",
        '<p style="font-size:11px;color:var(--ink-2);margin-bottom:6px;">Loops help you automate daily tasks:</p>'
        '<ul style="list-style:none;padding:0;margin:0;font-size:11px;color:var(--ink-2);line-height:1.55;">'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✅</span>File management</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✅</span>Server monitoring</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✅</span>User management</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✅</span>Log analysis</li>'
        '<li style="padding-left:18px;position:relative;margin-bottom:3px;"><span style="position:absolute;left:0;color:var(--green);">✅</span>Backups and cleanups</li>'
        '<li style="padding-left:18px;position:relative;"><span style="position:absolute;left:0;color:var(--green);">✅</span>System updates</li>'
        '</ul>')

    sidebar_cards = "".join([
        card("alert-triangle", "7. Avoiding Infinite Loops", infinite_warn),
        auto_card,
    ])

    # Full-width KEY TAKEAWAY banner below the body grid
    takeaway_banner = (
        '<div style="margin-top:4px;">'
        '<div class="callout tip" style="background:var(--green);color:#fff;border-left:none;padding:14px 22px;align-items:center;text-align:center;">'
        '<span class="ico" style="color:#fff;width:28px;height:28px;">' + svg("lightbulb") + '</span>'
        '<div style="flex:1;">'
        '<strong style="font-size:14px;letter-spacing:1px;">💡 KEY TAKEAWAY</strong> '
        '<span style="font-size:13px;">Loops save time, reduce errors, and make your scripts powerful.</span><br>'
        '<strong style="color:#fff;font-size:13px;letter-spacing:1.5px;">REPEAT SMARTER &nbsp;|&nbsp; SAVE TIME EVERY DAY</strong>'
        '</div>'
        '</div>'
        '</div>'
    )

    body = (
        '<div class="body">'
        f'<div class="rows">{left_rows}</div>'
        f'<div class="sidebar">{sidebar_cards}</div>'
        '</div>'
        f'{takeaway_banner}'
    )
    return body


# ============================================================
# MAIN
# ============================================================
PAGES = [
    # (out_filename, badge_page_num, title, subtitle, body_fn)
    ("recreated-page-06.html", 4, "4. VARIABLES AND ENVIRONMENT VARIABLES",
     "STORE DATA. REUSE. AUTOMATE.", body_page_06),
    ("recreated-page-07.html", 6, "6. EXIT CODES AND COMMAND SUCCESS",
     "EVERY COMMAND RETURNS A STATUS.", body_page_07),
    ("recreated-page-08.html", 7, "7. CONDITIONAL STATEMENTS",
     "MAKE SMART DECISIONS IN YOUR SCRIPTS.", body_page_08),
    ("recreated-page-09.html", 8, "8. LOGICAL OPERATORS AND MULTIPLE CONDITIONS",
     "COMBINE TESTS. MAKE SMARTER DECISIONS.", body_page_09),
    ("recreated-page-10.html", 9, "9. LOOPS FOR AUTOMATION",
     "REPEAT TASKS. SAVE TIME. ELIMINATE MANUAL WORK.", body_page_10),
]


def main() -> None:
    out_dir = "/home/z/my-project/downloads/instagram-DcaW1UljsVk"
    total = 20  # carousel total
    for fname, page_num, title, subtitle, body_fn in PAGES:
        body_html = body_fn()
        html = page_wrapper(page_num, total, title, subtitle, body_html)
        out_path = os.path.join(out_dir, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        size = os.path.getsize(out_path)
        print(f"Wrote {out_path}  ({size:,} bytes / {size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
