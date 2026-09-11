#!/usr/bin/env python3
"""
Colorful SVG Icon Library for the Shell Scripting for DevOps Handbook.

These icons are filled/solid multi-color SVGs matching the original
Instagram carousel's visual style (not outline-only). Each icon is
designed to be visually similar to the icons in the reference images.

Colors used:
- Green: #1B5E3F (primary brand green)
- Blue: #2563eb
- Purple: #7c3aed
- Red: #dc2626
- Gold/Amber: #d4a017 / #f9a825
- Orange: #e65100
- Teal: #0d7377
- Navy: #15264d
"""

# ============================================================
# ICON LIBRARY — Multi-color filled SVGs
# ============================================================

ICONS = {
    # ─── Terminal / Shell ───
    "terminal": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="6" width="40" height="30" rx="4" fill="#003366"/><rect x="4" y="6" width="40" height="6" rx="4" fill="#002244"/><circle cx="9" cy="9" r="1.2" fill="#ff5f56"/><circle cx="13" cy="9" r="1.2" fill="#ffbd2e"/><circle cx="17" cy="9" r="1.2" fill="#27c93f"/><rect x="8" y="15" width="32" height="17" rx="2" fill="#1a3a5c"/><path d="M12 20 L17 23 L12 26" fill="none" stroke="#4dabf7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="20" y1="26" x2="32" y2="26" stroke="#e6edf3" stroke-width="2" stroke-linecap="round"/><rect x="18" y="36" width="12" height="3" rx="1" fill="#003366"/><rect x="14" y="39" width="20" height="3" rx="1" fill="#003366"/></svg>''',

    "shell": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="6" width="36" height="36" rx="5" fill="#1B5E3F"/><rect x="6" y="6" width="36" height="8" rx="5" fill="#164a32"/><circle cx="12" cy="10" r="1.2" fill="#ff5f56"/><circle cx="16" cy="10" r="1.2" fill="#ffbd2e"/><circle cx="20" cy="10" r="1.2" fill="#27c93f"/><text x="12" y="30" fill="#7ee787" font-family="monospace" font-size="14" font-weight="bold">$_</text></svg>''',

    # ─── Gear / Cog ───
    "gear": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 6 L26 12 L32 10 L33 16 L39 18 L37 24 L42 28 L37 32 L39 38 L33 40 L32 46 L26 44 L24 50 L22 44 L16 46 L15 40 L9 38 L11 32 L6 28 L11 24 L9 18 L15 16 L16 10 L22 12 Z" fill="#1B5E3F"/><circle cx="24" cy="28" r="7" fill="#f5f1e8"/><circle cx="24" cy="28" r="4" fill="#1B5E3F"/></svg>''',

    # ─── Lightbulb ───
    "lightbulb": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 C16 4 10 10 10 18 C10 24 13 28 16 31 V36 H32 V31 C35 28 38 24 38 18 C38 10 32 4 24 4 Z" fill="#FFD700"/><path d="M16 36 H32 V38 H16 Z" fill="#333333"/><path d="M18 38 H30 V40 H18 Z" fill="#333333"/><path d="M20 40 H28 V42 H20 Z" fill="#333333"/><line x1="24" y1="0" x2="24" y2="2" stroke="#F39C12" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="10" x2="6" y2="8" stroke="#F39C12" stroke-width="2" stroke-linecap="round"/><line x1="40" y1="10" x2="42" y2="8" stroke="#F39C12" stroke-width="2" stroke-linecap="round"/><line x1="4" y1="20" x2="1" y2="20" stroke="#F39C12" stroke-width="2" stroke-linecap="round"/><line x1="44" y1="20" x2="47" y2="20" stroke="#F39C12" stroke-width="2" stroke-linecap="round"/></svg>''',

    # ─── Folder ───
    "folder": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M6 10 H18 L22 14 H42 V38 H6 Z" fill="#f9a825"/><path d="M6 10 H18 L22 14 H42 V18 H6 Z" fill="#d4a017"/></svg>''',

    # ─── File / Document ───
    "file": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M10 4 H28 L38 14 V44 H10 Z" fill="#ffffff" stroke="#1B5E3F" stroke-width="2"/><path d="M28 4 V14 H38" fill="none" stroke="#1B5E3F" stroke-width="2"/><line x1="15" y1="22" x2="33" y2="22" stroke="#1B5E3F" stroke-width="2"/><line x1="15" y1="28" x2="33" y2="28" stroke="#1B5E3F" stroke-width="2"/><line x1="15" y1="34" x2="27" y2="34" stroke="#1B5E3F" stroke-width="2"/></svg>''',

    # ─── Cloud ───
    "cloud": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M12 32 C7 32 4 29 4 25 C4 21 7 18 11 18 C12 13 16 10 21 10 C27 10 32 14 33 20 C38 20 42 23 42 28 C42 32 39 35 34 35 H14 Z" fill="#2563eb"/><text x="17" y="30" fill="#ffffff" font-family="monospace" font-size="12" font-weight="bold">&lt;/&gt;</text></svg>''',

    # ─── Globe ───
    "globe": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="20" fill="#2563eb"/><ellipse cx="24" cy="24" rx="8" ry="20" fill="none" stroke="#ffffff" stroke-width="1.5"/><line x1="4" y1="24" x2="44" y2="24" stroke="#ffffff" stroke-width="1.5"/><line x1="8" y1="14" x2="40" y2="14" stroke="#ffffff" stroke-width="1"/><line x1="8" y1="34" x2="40" y2="34" stroke="#ffffff" stroke-width="1"/><circle cx="24" cy="24" r="20" fill="none" stroke="#1e40af" stroke-width="1"/></svg>''',

    # ─── Rocket ───
    "rocket": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 C18 8 14 16 14 24 L14 32 L20 36 L28 36 L34 32 L34 24 C34 16 30 8 24 4 Z" fill="#1B5E3F"/><path d="M24 4 C21 6 19 8 18 10 L24 4 Z" fill="#C0392B"/><circle cx="24" cy="20" r="4" fill="#FFFFFF"/><path d="M14 32 L10 40 L14 38 Z" fill="#E67E22"/><path d="M34 32 L38 40 L34 38 Z" fill="#E67E22"/><path d="M20 36 L24 44 L28 36 Z" fill="#F39C12"/><path d="M22 36 L24 42 L26 36 Z" fill="#E67E22"/></svg>''',

    # ─── Warning Triangle ───
    "warning": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 L44 40 H4 Z" fill="#F4C430"/><path d="M24 4 L44 40 H4 Z" fill="none" stroke="#000000" stroke-width="1.5"/><line x1="24" y1="18" x2="24" y2="28" stroke="#000000" stroke-width="3" stroke-linecap="round"/><circle cx="24" cy="34" r="2" fill="#000000"/></svg>''',

    # ─── Check in Circle ───
    "check-circle": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="20" fill="#1B5E3F"/><path d="M14 24 L20 30 L34 16" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>''',

    # ─── Bug ───
    "bug": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><ellipse cx="24" cy="26" rx="9" ry="14" fill="#7c3aed"/><circle cx="24" cy="12" r="5" fill="#7c3aed"/><line x1="20" y1="8" x2="16" y2="4" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"/><line x1="28" y1="8" x2="32" y2="4" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"/><line x1="15" y1="18" x2="8" y2="14" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"/><line x1="33" y1="18" x2="40" y2="14" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"/><line x1="15" y1="26" x2="8" y2="26" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"/><line x1="33" y1="26" x2="40" y2="26" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"/><line x1="16" y1="34" x2="10" y2="38" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"/><line x1="32" y1="34" x2="38" y2="38" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"/></svg>''',

    # ─── Key ───
    "key": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="14" cy="14" r="9" fill="none" stroke="#d4a017" stroke-width="3"/><circle cx="14" cy="14" r="3" fill="#d4a017"/><path d="M21 21 L38 38" stroke="#d4a017" stroke-width="3" stroke-linecap="round"/><path d="M34 34 L40 28" stroke="#d4a017" stroke-width="3" stroke-linecap="round"/><path d="M30 38 L36 32" stroke="#d4a017" stroke-width="3" stroke-linecap="round"/></svg>''',

    # ─── Lock ───
    "lock": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="22" width="28" height="20" rx="3" fill="#dc2626"/><path d="M14 22 V16 C14 10 19 6 24 6 C29 6 34 10 34 16 V22" fill="none" stroke="#dc2626" stroke-width="3"/><circle cx="24" cy="30" r="3" fill="#ffffff"/></svg>''',

    # ─── Shield ───
    "shield": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 L40 10 V22 C40 32 33 40 24 44 C15 40 8 32 8 22 V10 Z" fill="#1B5E3F"/><path d="M16 22 L21 27 L32 16" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>''',

    # ─── Database ───
    "database": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><ellipse cx="24" cy="10" rx="14" ry="5" fill="#2563eb"/><path d="M10 10 V20 C10 23 17 26 24 26 C31 26 38 23 38 20 V10" fill="#1e40af"/><path d="M10 20 V30 C10 33 17 36 24 36 C31 36 38 33 38 30 V20" fill="#2563eb"/><path d="M10 30 V38 C10 41 17 44 24 44 C31 44 38 41 38 38 V30" fill="#1e40af"/></svg>''',

    # ─── Server ───
    "server": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="8" width="36" height="12" rx="2" fill="#15264d"/><rect x="6" y="24" width="36" height="12" rx="2" fill="#1e3160"/><circle cx="12" cy="14" r="1.5" fill="#27c93f"/><circle cx="12" cy="30" r="1.5" fill="#27c93f"/><circle cx="18" cy="14" r="1.5" fill="#ffbd2e"/><circle cx="18" cy="30" r="1.5" fill="#ffbd2e"/><rect x="24" y="12" width="14" height="2" rx="1" fill="#e6edf3"/><rect x="24" y="28" width="14" height="2" rx="1" fill="#e6edf3"/></svg>''',

    # ─── Clipboard ───
    "clipboard": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="6" width="28" height="36" rx="3" fill="#1B5E3F"/><rect x="18" y="2" width="12" height="6" rx="2" fill="#164a32"/><line x1="15" y1="16" x2="33" y2="16" stroke="#ffffff" stroke-width="2"/><line x1="15" y1="22" x2="33" y2="22" stroke="#ffffff" stroke-width="2"/><line x1="15" y1="28" x2="29" y2="28" stroke="#ffffff" stroke-width="2"/><circle cx="16" cy="16" r="1.5" fill="#27c93f"/><circle cx="16" cy="22" r="1.5" fill="#27c93f"/><circle cx="16" cy="28" r="1.5" fill="#27c93f"/></svg>''',

    # ─── Calendar / Cron ───
    "calendar": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="8" width="36" height="34" rx="3" fill="#ffffff" stroke="#1B5E3F" stroke-width="2"/><rect x="6" y="8" width="36" height="8" rx="3" fill="#1B5E3F"/><line x1="14" y1="4" x2="14" y2="12" stroke="#1B5E3F" stroke-width="2" stroke-linecap="round"/><line x1="34" y1="4" x2="34" y2="12" stroke="#1B5E3F" stroke-width="2" stroke-linecap="round"/><circle cx="14" cy="22" r="2" fill="#dc2626"/><circle cx="24" cy="22" r="2" fill="#1B5E3F"/><circle cx="34" cy="22" r="2" fill="#1B5E3F"/><circle cx="14" cy="30" r="2" fill="#1B5E3F"/><circle cx="24" cy="30" r="2" fill="#1B5E3F"/><circle cx="34" cy="30" r="2" fill="#1B5E3F"/><circle cx="14" cy="38" r="2" fill="#1B5E3F"/><circle cx="24" cy="38" r="2" fill="#1B5E3F"/><circle cx="34" cy="38" r="2" fill="#1B5E3F"/></svg>''',

    # ─── Clock ───
    "clock": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="20" fill="#1B5E3F"/><circle cx="24" cy="24" r="16" fill="#ffffff"/><line x1="24" y1="24" x2="24" y2="12" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><line x1="24" y1="24" x2="32" y2="28" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><circle cx="24" cy="24" r="2" fill="#1B5E3F"/></svg>''',

    # ─── Search / Magnifying Glass ───
    "search": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="20" cy="20" r="13" fill="none" stroke="#1B5E3F" stroke-width="3"/><line x1="30" y1="30" x2="42" y2="42" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><circle cx="20" cy="20" r="8" fill="#e8f5ee"/></svg>''',

    # ─── Eye ───
    "eye": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M4 24 C10 14 18 10 24 10 C30 10 38 14 44 24 C38 34 30 38 24 38 C18 38 10 34 4 24 Z" fill="#ffffff" stroke="#1B5E3F" stroke-width="2"/><circle cx="24" cy="24" r="7" fill="#2563eb"/><circle cx="24" cy="24" r="3" fill="#1c1c1c"/></svg>''',

    # ─── Code Brackets ───
    "code": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M18 12 L8 24 L18 36" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M30 12 L40 24 L30 36" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><line x1="26" y1="10" x2="22" y2="38" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/></svg>''',

    # ─── Arrow Right ───
    "arrow": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><line x1="6" y1="24" x2="38" y2="24" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><path d="M30 14 L42 24 L30 34" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>''',

    # ─── Star ───
    "star": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 L29 18 L44 18 L32 27 L36 42 L24 33 L12 42 L16 27 L4 18 L19 18 Z" fill="#f9a825"/></svg>''',

    # ─── List ───
    "list": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><line x1="18" y1="12" x2="42" y2="12" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><line x1="18" y1="24" x2="42" y2="24" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><line x1="18" y1="36" x2="42" y2="36" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><circle cx="8" cy="12" r="3" fill="#1B5E3F"/><circle cx="8" cy="24" r="3" fill="#1B5E3F"/><circle cx="8" cy="36" r="3" fill="#1B5E3F"/></svg>''',

    # ─── Wrench ───
    "wrench": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M30 4 C26 4 22 6 20 10 L28 18 L26 20 L18 12 C14 14 12 18 12 22 C12 28 16 32 22 32 L36 46 L42 40 L28 26 C32 22 34 18 34 14 C34 10 32 6 30 4 Z" fill="#1B5E3F"/></svg>''',

    # ─── Question Mark ───
    "question": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="20" fill="#1B5E3F"/><text x="24" y="32" fill="#ffffff" font-family="Arial" font-size="24" font-weight="bold" text-anchor="middle">?</text></svg>''',

    # ─── Play ───
    "play": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="8" width="40" height="32" rx="4" fill="#dc2626"/><path d="M20 16 L20 32 L32 24 Z" fill="#ffffff"/></svg>''',

    # ─── Stop / Hand ───
    "stop": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="20" fill="#D32F2F"/><line x1="16" y1="16" x2="32" y2="32" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/><line x1="32" y1="16" x2="16" y2="32" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/></svg>''',

    # ─── Filter / Funnel ───
    "filter": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M6 8 H42 L28 24 V40 L20 36 V24 Z" fill="#1B5E3F"/></svg>''',

    # ─── Award / Ribbon ───
    "award": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="18" r="12" fill="#f9a825"/><circle cx="24" cy="18" r="8" fill="#d4a017"/><path d="M16 28 L12 44 L20 40 L24 44 L28 40 L36 44 L32 28" fill="#1B5E3F"/><path d="M20 12 L24 8 L28 12 L26 18 L24 16 L22 18 Z" fill="#ffffff"/></svg>''',

    # ─── Crosshair / Target ───
    "target": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="20" fill="none" stroke="#dc2626" stroke-width="2"/><circle cx="24" cy="24" r="14" fill="none" stroke="#dc2626" stroke-width="2"/><circle cx="24" cy="24" r="6" fill="#dc2626"/><line x1="24" y1="0" x2="24" y2="8" stroke="#dc2626" stroke-width="2"/><line x1="24" y1="40" x2="24" y2="48" stroke="#dc2626" stroke-width="2"/><line x1="0" y1="24" x2="8" y2="24" stroke="#dc2626" stroke-width="2"/><line x1="40" y1="24" x2="48" y2="24" stroke="#dc2626" stroke-width="2"/></svg>''',

    # ─── User / Person ───
    "user": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="14" r="8" fill="#1B5E3F"/><path d="M8 42 C8 32 16 28 24 28 C32 28 40 32 40 42" fill="#1B5E3F"/></svg>''',

    # ─── Users (multiple) ───
    "users": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="18" cy="14" r="7" fill="#1B5E3F"/><path d="M4 38 C4 30 11 26 18 26 C25 26 32 30 32 38" fill="#1B5E3F"/><circle cx="34" cy="16" r="5" fill="#2563eb"/><path d="M28 38 C28 32 34 28 40 28 C44 28 46 32 46 38" fill="#2563eb"/></svg>''',

    # ─── Tag ───
    "tag": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M4 24 L24 4 H44 V24 L24 44 Z" fill="#1B5E3F"/><circle cx="36" cy="12" r="3" fill="#ffffff"/></svg>''',

    # ─── Power ───
    "power": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 V24" stroke="#dc2626" stroke-width="3" stroke-linecap="round"/><path d="M14 10 C8 14 4 20 4 28 C4 38 13 46 24 46 C35 46 44 38 44 28 C44 20 40 14 34 10" fill="none" stroke="#dc2626" stroke-width="3" stroke-linecap="round"/></svg>''',

    # ─── Bell ───
    "bell": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 C18 4 14 8 14 14 V24 L10 32 H38 L34 24 V14 C34 8 30 4 24 4 Z" fill="#f9a825"/><circle cx="24" cy="38" r="3" fill="#e65100"/></svg>''',

    # ─── Refresh / Recycle ───
    "refresh": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M40 24 C40 32 33 40 24 40 C16 40 9 33 8 25" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><path d="M8 24 C8 16 15 8 24 8 C32 8 39 15 40 23" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><path d="M34 6 L40 23 L23 18" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 42 L8 25 L25 30" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>''',

    # ─── Scissors ───
    "scissors": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="34" r="6" fill="none" stroke="#dc2626" stroke-width="3"/><circle cx="12" cy="14" r="6" fill="none" stroke="#dc2626" stroke-width="3"/><line x1="17" y1="17" x2="42" y2="38" stroke="#dc2626" stroke-width="3" stroke-linecap="round"/><line x1="17" y1="31" x2="42" y2="10" stroke="#dc2626" stroke-width="3" stroke-linecap="round"/></svg>''',

    # ─── Download ───
    "download": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 V32" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round"/><path d="M14 22 L24 32 L34 22" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 38 V44 H40 V38" fill="none" stroke="#1B5E3F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>''',

    # ─── Branch (Git) ───
    "branch": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="14" cy="10" r="5" fill="#1B5E3F"/><circle cx="14" cy="38" r="5" fill="#1B5E3F"/><circle cx="34" cy="14" r="5" fill="#2563eb"/><line x1="14" y1="15" x2="14" y2="33" stroke="#1B5E3F" stroke-width="3"/><path d="M14 24 C14 18 24 14 29 14" fill="none" stroke="#2563eb" stroke-width="3"/></svg>''',

    # ─── Dollar ───
    "dollar": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="20" fill="#1B5E3F"/><text x="24" y="32" fill="#ffffff" font-family="Arial" font-size="24" font-weight="bold" text-anchor="middle">$</text></svg>''',

    # ─── Chart / Graph ───
    "chart": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="28" width="8" height="14" rx="1" fill="#1B5E3F"/><rect x="18" y="20" width="8" height="22" rx="1" fill="#2563eb"/><rect x="30" y="12" width="8" height="30" rx="1" fill="#f9a825"/><line x1="4" y1="42" x2="44" y2="42" stroke="#1c1c1c" stroke-width="2"/></svg>''',

    # ─── Terminal Cube (3D) ───
    "cube": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4 L42 12 V36 L24 44 L6 36 V12 Z" fill="#003366"/><path d="M24 4 L42 12 L24 20 L6 12 Z" fill="#0055AA"/><path d="M24 20 L42 12 V36 L24 44 Z" fill="#002288"/><path d="M24 20 L6 12 V36 L24 44 Z" fill="#004499"/><text x="24" y="32" fill="#ffffff" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">$</text></svg>''',

    # ─── Monitor / Screen ───
    "monitor": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="6" width="40" height="28" rx="3" fill="#15264d"/><rect x="8" y="10" width="32" height="20" rx="1" fill="#0d1117"/><path d="M16 18 L20 20 L16 22" fill="none" stroke="#7ee787" stroke-width="1.5" stroke-linecap="round"/><line x1="22" y1="22" x2="30" y2="22" stroke="#e6edf3" stroke-width="1.5"/><path d="M18 34 H30 V40 H18 Z" fill="#15264d"/><rect x="14" y="40" width="20" height="3" rx="1" fill="#1e3160"/></svg>''',

    # ─── Network ───
    "network": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="8" r="4" fill="#1B5E3F"/><circle cx="8" cy="24" r="4" fill="#2563eb"/><circle cx="40" cy="24" r="4" fill="#2563eb"/><circle cx="24" cy="40" r="4" fill="#1B5E3F"/><line x1="24" y1="12" x2="10" y2="22" stroke="#1c1c1c" stroke-width="2"/><line x1="24" y1="12" x2="38" y2="22" stroke="#1c1c1c" stroke-width="2"/><line x1="10" y1="26" x2="22" y2="38" stroke="#1c1c1c" stroke-width="2"/><line x1="38" y1="26" x2="26" y2="38" stroke="#1c1c1c" stroke-width="2"/></svg>''',

    # ─── Book ───
    "book": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M6 8 H20 C22 8 24 10 24 12 V42 C24 40 22 38 20 38 H6 Z" fill="#1B5E3F"/><path d="M42 8 H28 C26 8 24 10 24 12 V42 C24 40 26 38 28 38 H42 Z" fill="#164a32"/><line x1="10" y1="14" x2="20" y2="14" stroke="#ffffff" stroke-width="1.5"/><line x1="10" y1="20" x2="20" y2="20" stroke="#ffffff" stroke-width="1.5"/><line x1="28" y1="14" x2="38" y2="14" stroke="#ffffff" stroke-width="1.5"/><line x1="28" y1="20" x2="38" y2="20" stroke="#ffffff" stroke-width="1.5"/></svg>''',

    # ─── Pencil / Edit ───
    "pencil": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M36 4 L44 12 L16 40 L4 44 L8 32 Z" fill="#f9a825"/><path d="M36 4 L44 12 L38 18 L30 10 Z" fill="#d4a017"/><line x1="8" y1="32" x2="16" y2="40" stroke="#e0a517" stroke-width="2"/></svg>''',

    # ─── Copy ───
    "copy": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="14" y="14" width="24" height="28" rx="2" fill="#ffffff" stroke="#1B5E3F" stroke-width="2"/><rect x="8" y="8" width="24" height="28" rx="2" fill="#1B5E3F"/><line x1="14" y1="16" x2="26" y2="16" stroke="#ffffff" stroke-width="2"/><line x1="14" y1="22" x2="26" y2="22" stroke="#ffffff" stroke-width="2"/><line x1="14" y1="28" x2="22" y2="28" stroke="#ffffff" stroke-width="2"/></svg>''',

    # ─── Check Square ───
    "check-square": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="6" width="36" height="36" rx="4" fill="#1B5E3F"/><path d="M14 24 L20 30 L34 16" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>''',

    # ─── Flag ───
    "flag": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="4" x2="10" y2="44" stroke="#1c1c1c" stroke-width="3" stroke-linecap="round"/><path d="M10 6 H38 L32 16 L38 26 H10 Z" fill="#dc2626"/></svg>''',

    # ─── Docker / Container ───
    "container": '''<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="16" width="8" height="8" rx="1" fill="#2563eb"/><rect x="14" y="16" width="8" height="8" rx="1" fill="#2563eb"/><rect x="24" y="16" width="8" height="8" rx="1" fill="#2563eb"/><rect x="14" y="6" width="8" height="8" rx="1" fill="#2563eb"/><rect x="24" y="6" width="8" height="8" rx="1" fill="#2563eb"/><path d="M2 28 C2 28 8 34 16 34 C28 34 38 28 46 34" fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round"/></svg>''',
}


def icon(name: str, size: int = 48) -> str:
    """Return inline SVG for a named icon at the given size."""
    svg = ICONS.get(name, ICONS.get("terminal", ""))
    return svg.replace('viewBox="0 0 48 48"', f'viewBox="0 0 48 48" width="{size}" height="{size}"')


def list_icons():
    """Print all available icon names."""
    for name in sorted(ICONS.keys()):
        print(f"  {name}")
    print(f"\nTotal: {len(ICONS)} icons")


if __name__ == "__main__":
    list_icons()
