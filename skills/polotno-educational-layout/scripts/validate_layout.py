#!/usr/bin/env python3
"""
Polotno Educational Layout Validator.

Validates a Polotno JSON file against the layout rules defined in the
polotno-educational-layout skill. Checks for:
  - overlaps (text/text, text/box, box/box)
  - text overflow / clipping
  - elements outside page boundaries
  - unreadably small text
  - promotional / social-media content (text + svg path signatures)
  - inconsistent margins
  - large empty space at page bottom
  - duplicate element IDs
  - invalid Polotno schema (wrong element types, missing fields, borderRadius misuse)

Exit code 0 = all checks pass; 1 = problems found.
Usage:
    python3 validate_layout.py <file.json> [--strict] [--json]
"""
import json
import re
import sys
import argparse
from collections import Counter, defaultdict

# ---------- Bounding box ----------
def text_content_bbox(el):
    """For a text element, return the bbox of the actual rendered text area,
    not the full element height. Text is rendered from the top, so the
    content height = (number of lines) * (fontSize * lineHeight)."""
    if el.get("type") != "text":
        return bbox(el)
    x, y = el["x"], el["y"]
    w = el["width"]
    fs = el.get("fontSize", 16)
    lh = el.get("lineHeight", 1.4)
    txt = el.get("text", "")
    # count lines: explicit \n + wrapping estimate
    chars_per_line = max(10, int(w / (fs * 0.52)))  # 0.52 for CC Dash To School (narrower than CC Dash To School) (wide font)
    lines = 0
    for line in txt.split("\n"):
        lines += max(1, (len(line) + chars_per_line - 1) // chars_per_line)
    content_h = lines * fs * lh
    return (x, y, x + w, y + content_h)

def bbox(el):
    """Return (x0, y0, x1, y1) for an element."""
    x, y = el["x"], el["y"]
    return (x, y, x + el["width"], y + el["height"])

def overlap_area(a, b):
    """Area of intersection of two bboxes."""
    x0 = max(a[0], b[0]); y0 = max(a[1], b[1])
    x1 = min(a[2], b[2]); y1 = min(a[3], b[3])
    if x1 <= x0 or y1 <= y0:
        return 0
    return (x1 - x0) * (y1 - y0)

def is_inside(inner, outer, tolerance=0):
    """True if bbox `inner` is fully inside bbox `outer` (with tolerance)."""
    return (inner[0] >= outer[0] - tolerance and
            inner[1] >= outer[1] - tolerance and
            inner[2] <= outer[2] + tolerance and
            inner[3] <= outer[3] + tolerance)

# ---------- Promo / social-media detection ----------
# IMPORTANT: LIKE/SHARE/FOLLOW/SUBSCRIBE are matched only as STANDALONE button
# labels (^LIKE$ etc.) or in promo-phrase combinations — NOT as common English
# words like "people like CEO" or "share this data". This prevents false-positive
# flagging (and deletion) of legitimate educational content.
PROMO_TEXT_RE = re.compile(
    r"@aman_views|@aman|aman_views|"
    r"@\w+_(views|notes|study|learning)|"
    r"instagram|youtube|twitter|facebook|tiktok|telegram|whatsapp|snapchat|"
    r"(?:^LIKE$)|(?:^SHARE$)|(?:^FOLLOW$)|(?:^SUBSCRIBE$)|"
    r"TO GET PDF NOTES|GET PDF NOTES|DOWNLOAD PDF|COMMENT\s+PDF|"
    r"(?:^COMMENT$)|"
    r"like.*share.*follow|follow.*for.*more|"
    r"rate\s+aman|rate\s+@\w+",
    re.IGNORECASE)

# Distinctive SVG path `d` attribute substrings for social icons
PROMO_SVG_SIGNATURES = [
    "M2 21h2c.55 0 1-.45 1-1v-9",            # thumbs up (LIKE)
    "M2.01 21L23 12 2.01 3",                 # paper plane (SHARE)
    "M12 12c2.21 0 4-1.79 4-4",              # person (FOLLOW)
    "M12 21.35l-1.45-1.32",                  # heart (LIKE)
]

def is_promo(el):
    if el.get("type") == "text" and el.get("text"):
        if PROMO_TEXT_RE.search(el["text"]):
            return True
    if el.get("type") == "svg" and el.get("src"):
        src = el["src"]
        if PROMO_TEXT_RE.search(src):
            return True
        for sig in PROMO_SVG_SIGNATURES:
            if sig in src:
                return True
    return False

# ---------- Element classification ----------
TEXTUAL = {"text"}
CONTAINER = {"figure"}  # cards/callouts are figure(rect)

# ---------- Validators ----------
def validate_schema(store):
    """Check top-level and per-element schema correctness."""
    problems = []
    valid_types = {"text", "figure", "svg", "line", "image", "gif", "video",
                   "table", "group", "table-cell", "audio"}
    valid_subtypes = {"rect", "ellipse", "triangle", None}
    for req in ("schemaVersion", "width", "height", "fonts", "pages"):
        if req not in store:
            problems.append(f"store: missing required field '{req}'")
    for pi, p in enumerate(store.get("pages", [])):
        for req in ("id", "width", "height", "background", "children"):
            if req not in p:
                problems.append(f"page {pi+1}: missing '{req}'")
        for ci, c in enumerate(p.get("children", [])):
            if c.get("type") not in valid_types:
                problems.append(f"page {pi+1} el {ci}: invalid type '{c.get('type')}'")
            for req in ("id", "type", "x", "y", "width", "height"):
                if req not in c:
                    problems.append(f"page {pi+1} el {ci}: missing '{req}'")
            if c.get("type") == "figure" and c.get("subType") not in valid_subtypes:
                problems.append(f"page {pi+1} el {ci}: figure has bad subType '{c.get('subType')}'")
            if "borderRadius" in c:
                problems.append(f"page {pi+1} el {ci}: uses 'borderRadius' (should be 'cornerRadius')")
            if c.get("type") == "text":
                if "text" not in c:
                    problems.append(f"page {pi+1} text el {ci}: missing 'text' field")
                if c.get("backgroundEnabled") and not c.get("backgroundColor"):
                    problems.append(f"page {pi+1} text el {ci}: backgroundEnabled but no backgroundColor")
            if c.get("type") == "svg" and "src" not in c:
                problems.append(f"page {pi+1} svg el {ci}: missing 'src'")
            if c.get("type") == "line" and "color" not in c and "fill" in c:
                problems.append(f"page {pi+1} line el {ci}: uses 'fill' (should be 'color')")
    return problems

def validate_ids(store):
    """Check for duplicate element IDs within a page."""
    problems = []
    for pi, p in enumerate(store.get("pages", [])):
        ids = [c["id"] for c in p.get("children", []) if "id" in c]
        dupes = [k for k, v in Counter(ids).items() if v > 1]
        if dupes:
            problems.append(f"page {pi+1}: duplicate element IDs: {dupes[:5]}")
    return problems

def validate_boundaries(store):
    """Elements must be inside the page bounds."""
    problems = []
    for pi, p in enumerate(store.get("pages", [])):
        pw, ph = p["width"], p["height"]
        for ci, c in enumerate(p.get("children", [])):
            x0, y0, x1, y1 = bbox(c)
            if x0 < -2 or y0 < -2 or x1 > pw + 2 or y1 > ph + 2:
                problems.append(
                    f"page {pi+1} el {ci} ({c.get('type')}): "
                    f"out of bounds ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) "
                    f"page={pw}x{ph}")
    return problems

def validate_font_sizes(store):
    """Body text ≥ 12px, headings ≥ 14px. Bullet markers (•, ★, ✓, ✗) are exempt."""
    BULLET_MARKERS = {"•", "★", "✓", "✗", "·", "▪", "→", "←", "↓", "↑", "☐"}
    problems = []
    for pi, p in enumerate(store.get("pages", [])):
        for ci, c in enumerate(p.get("children", [])):
            if c.get("type") != "text":
                continue
            sz = c.get("fontSize", 16)
            txt = c.get("text", "").strip()
            if sz < 12:
                problems.append(f"page {pi+1} el {ci}: fontSize {sz} < 12 (unreadable) text='{txt[:30]}'")
            elif sz < 14 and c.get("fontWeight") == "bold" and txt not in BULLET_MARKERS:
                problems.append(f"page {pi+1} el {ci}: heading fontSize {sz} < 14 text='{txt[:30]}'")
    return problems

def validate_promo(store):
    """Detect promotional / social-media content."""
    problems = []
    for pi, p in enumerate(store.get("pages", [])):
        for ci, c in enumerate(p.get("children", [])):
            if is_promo(c):
                preview = (c.get("text") or c.get("src", ""))[:60]
                problems.append(f"page {pi+1} el {ci}: promotional content detected: {preview!r}")
    return problems

def validate_overlaps(store):
    """Detect significant overlaps between text and other elements.

    We skip overlaps where one element is clearly a background (e.g. a big rect
    behind many text elements) — those are intentional. We focus on:
      - text vs text overlap (almost always a bug)
      - text vs figure overlap where the text is NOT inside the figure (likely a bug)
      - figure vs figure overlap where neither is a thin line/bar (likely a bug)
    """
    problems = []
    for pi, p in enumerate(store.get("pages", [])):
        children = p.get("children", [])
        n = len(children)
        # pre-compute content bboxes (text uses content area, not full element height)
        bb = [text_content_bbox(c) if c.get("type") == "text" else bbox(c) for c in children]
        for i in range(n):
            for j in range(i + 1, n):
                a_el, b_el = children[i], children[j]
                a_bb, b_bb = bb[i], bb[j]
                ov = overlap_area(a_bb, b_bb)
                if ov == 0:
                    continue
                # area of the smaller element
                a_area = (a_bb[2]-a_bb[0]) * (a_bb[3]-a_bb[1])
                b_area = (b_bb[2]-b_bb[0]) * (b_bb[3]-b_bb[1])
                smaller_area = min(a_area, b_area)
                if smaller_area == 0:
                    continue
                ratio = ov / smaller_area
                # only flag if overlap is > 20% of the smaller element
                if ratio < 0.20:
                    continue
                a_type, b_type = a_el.get("type"), b_el.get("type")
                # text vs text — almost always a bug
                if a_type == "text" and b_type == "text":
                    problems.append(
                        f"page {pi+1}: text overlaps text "
                        f"({a_el.get('text','')[:25]!r} ↔ {b_el.get('text','')[:25]!r}) "
                        f"{ratio*100:.0f}% overlap")
                    continue
                # figure vs figure — flag if both are substantial rects (not thin bars)
                if a_type == "figure" and b_type == "figure":
                    a_thin = (a_el.get("height", 100) < 12 or a_el.get("width", 100) < 12)
                    b_thin = (b_el.get("height", 100) < 12 or b_el.get("width", 100) < 12)
                    if a_thin or b_thin:
                        continue  # one is a line/bar, skip
                    problems.append(
                        f"page {pi+1}: figure overlaps figure "
                        f"({a_el.get('subType')} ↔ {b_el.get('subType')}) "
                        f"{ratio*100:.0f}% overlap")
                    continue
                # text vs figure — flag if text is NOT mostly inside the figure
                if a_type == "text" and b_type == "figure":
                    if not is_inside(a_bb, b_bb, tolerance=4):
                        problems.append(
                            f"page {pi+1}: text overlaps figure (not contained) "
                            f"{a_el.get('text','')[:25]!r} "
                            f"{ratio*100:.0f}% overlap")
                    continue
                if b_type == "text" and a_type == "figure":
                    if not is_inside(b_bb, a_bb, tolerance=4):
                        problems.append(
                            f"page {pi+1}: text overlaps figure (not contained) "
                            f"{b_el.get('text','')[:25]!r} "
                            f"{ratio*100:.0f}% overlap")
    return problems

def validate_margins(store):
    """Content should respect left/right margins (default 50px on a 1080px page)."""
    problems = []
    margin = 50
    BG_COLORS = {"#FDFBF7", "#FFFFFF", "#ffffff", "transparent", None, ""}
    for pi, p in enumerate(store.get("pages", [])):
        pw = p["width"]
        for ci, c in enumerate(p.get("children", [])):
            # skip full-page backgrounds
            if c.get("type") == "figure" and c.get("fill") in BG_COLORS:
                if c.get("width", 0) >= pw - 10:
                    continue
            x0 = c["x"]
            x1 = c["x"] + c["width"]
            if x0 < margin - 5 and c.get("type") != "figure":
                # allow binder holes (small circles on far left)
                if c.get("width", 100) > 30:
                    problems.append(f"page {pi+1} el {ci}: x={x0:.0f} < left margin {margin}")
            if x1 > pw - margin + 5:
                problems.append(f"page {pi+1} el {ci}: x1={x1:.0f} > right margin {pw-margin}")
    return problems

def validate_bottom_space(store):
    """Flag large empty space at the bottom of a page (> 25% of page height)."""
    problems = []
    BG_COLORS = {"#FDFBF7", "#FFFFFF", "#ffffff", "transparent", None, ""}
    for pi, p in enumerate(store.get("pages", [])):
        ph = p["height"]
        if not p.get("children"):
            continue
        # find the bottom-most element (excluding full-page backgrounds)
        max_bottom = 0
        for c in p["children"]:
            if c.get("type") == "figure" and c.get("fill") in BG_COLORS:
                if c.get("width", 0) >= p["width"] - 10 and c.get("height", 0) >= p["height"] - 10:
                    continue  # full-page background
            b = c["y"] + c["height"]
            if b > max_bottom:
                max_bottom = b
        empty = ph - max_bottom
        if empty > ph * 0.25:
            problems.append(
                f"page {pi+1}: {empty:.0f}px empty at bottom "
                f"({empty/ph*100:.0f}% of page) — content ends at {max_bottom:.0f}, "
                f"page height {ph}")
    return problems

def validate_containment(store):
    """For every text element, check that its RENDERED content height fits
    inside its nearest container card. This catches the 'text extends below
    card' bug that simple bbox checks miss.

    A text element's container is the largest figure(rect) whose bounds contain
    the text element's top-left corner AND which isn't a full-page background.
    """
    problems = []
    BG_COLORS = {"#FDFBF7", "#FFFFFF", "#ffffff", "transparent", None, ""}
    for pi, p in enumerate(store.get("pages", [])):
        children = p.get("children", [])
        # pre-compute candidate container cards
        cards = []
        for c in children:
            if c.get("type") == "figure" and c.get("subType") == "rect":
                if c.get("height", 0) < 30:
                    continue  # thin bar/underline, not a container
                if c.get("fill") in BG_COLORS and c.get("width", 0) >= p["width"] - 10:
                    continue  # full-page background
                cards.append(c)
        # for each text element, find its container
        for ti, t in enumerate(children):
            if t.get("type") != "text" or not t.get("text"):
                continue
            tx, ty = t["x"], t["y"]
            tw = t["width"]
            th = t.get("height", 20)
            # find the container: the card whose bounds contain the text's top-left
            # corner (text must START inside the card, not at its bottom edge)
            best_card = None
            best_area = 0
            for c in cards:
                cx0, cy0 = c["x"], c["y"]
                cx1, cy1 = c["x"] + c["width"], c["y"] + c["height"]
                # text top-left must be INSIDE the card:
                # - tx within card's X range
                # - ty >= card top (below or at the top edge)
                # - ty < card bottom (STRICTLY above the bottom edge — if ty == cy1,
                #   the text belongs to the NEXT card, not this one)
                if (tx >= cx0 - 4 and tx + tw <= cx1 + 4 and
                    ty >= cy0 - 4 and ty < cy1 - 1):
                    area = c["width"] * c["height"]
                    if area > best_area:
                        best_area = area
                        best_card = c
            if best_card is None:
                continue  # text not inside any card (standalone heading, etc.)
            # check: does the text's rendered content fit inside the card?
            content_h = _text_content_height(t)
            text_bottom = ty + content_h
            card_bottom = best_card["y"] + best_card["height"]
            if text_bottom > card_bottom + 2:
                overflow = text_bottom - card_bottom
                problems.append(
                    f"page {pi+1} text '{t['text'][:30]}': content height {content_h:.0f}px "
                    f"overflows container bottom by {overflow:.0f}px "
                    f"(text at y={ty:.0f}, card bottom at y={card_bottom:.0f})")
            # check: does the text element's WIDTH fit inside the card?
            card_right = best_card["x"] + best_card["width"]
            text_right = tx + tw
            if text_right > card_right + 2:
                overflow_x = text_right - card_right
                problems.append(
                    f"page {pi+1} text '{t['text'][:30]}': element width {tw:.0f}px "
                    f"overflows container right edge by {overflow_x:.0f}px "
                    f"(text right={text_right:.0f}, card right={card_right:.0f})")
    return problems

def _text_content_height(el):
    """Estimate rendered height of a text element's content (wrapping-aware)."""
    fs = el.get("fontSize", 16)
    lh = el.get("lineHeight", 1.4)
    txt = el.get("text", "")
    w = el.get("width", 100)
    # CC Dash To School is a wide font — use 0.52 * fs as char width
    chars_per_line = max(10, int(w / (fs * 0.52)))
    lines = 0
    for line in txt.split("\n"):
        lines += max(1, (len(line) + chars_per_line - 1) // chars_per_line)
    return lines * fs * lh

# ---------- Main ----------
def validate(store, strict=False):
    problems = []
    problems += validate_schema(store)
    problems += validate_ids(store)
    problems += validate_boundaries(store)
    problems += validate_font_sizes(store)
    problems += validate_promo(store)
    problems += validate_overlaps(store)
    problems += validate_margins(store)
    problems += validate_bottom_space(store)
    problems += validate_containment(store)
    return problems

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="Polotno JSON file to validate")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--json", action="store_true", help="output JSON instead of text")
    args = ap.parse_args()

    with open(args.file) as f:
        store = json.load(f)

    problems = validate(store, strict=args.strict)

    if args.json:
        print(json.dumps({
            "file": args.file,
            "valid": len(problems) == 0,
            "problem_count": len(problems),
            "problems": problems,
        }, indent=2))
    else:
        if not problems:
            print(f"✅ {args.file}: ALL CHECKS PASS")
            print(f"   Pages: {len(store.get('pages', []))}")
            print(f"   Elements: {sum(len(p.get('children', [])) for p in store.get('pages', []))}")
        else:
            print(f"❌ {args.file}: {len(problems)} PROBLEM(S) FOUND")
            print()
            for p in problems:
                print(f"  - {p}")
    return 0 if not problems else 1

if __name__ == "__main__":
    sys.exit(main())
