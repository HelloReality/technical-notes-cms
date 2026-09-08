# Cursor-Based Layout (the core mechanism)

The cursor pattern is the single most important layout idea in this skill. It
makes overlaps **impossible by construction** — every section reports how tall
it rendered, so the next section starts below it.

## The problem it solves

The classic overlap bug:

```python
# BAD — fixed Y coordinates, will overlap when content is taller than expected
y2 = y + 64
els += two_col_compare(70, y2, 940, 200, ...)   # card auto-sizes to 376px tall
y3 = y2 + 216                                    # ← BUG: 216 < 376, next section lands INSIDE the card
els += callout(70, y3, 940, 80, "REMEMBER", ...)  # overlaps the card above
```

The author guessed the card would be 200px tall, but it auto-sized to 376px
(because it has 6 bullets). The next section was placed at a hardcoded Y inside
the card.

## The fix

Every layout helper returns `(elements, bottom_y)` — the Y coordinate of its
own bottom edge. Callers advance a **cursor** by that amount.

```python
# GOOD — cursor pattern, overlap-proof
SECTION_GAP = 26

els, cursor = page_header(N, "title")           # cursor = 248

els_h, bottom = heading("Section", 70, cursor, 940, ...)
els += els_h
cursor = bottom + SECTION_GAP                    # advance by ACTUAL height

els_c, bottom = callout(70, cursor, 940, 80, "REMEMBER", "...", ...)
els += els_c
cursor = bottom + SECTION_GAP                    # callout auto-sized, cursor follows
```

## Helper return contract

Every layout helper MUST return `(els, bottom_y)`:

| Helper | Returns bottom_y of |
|--------|----------------------|
| `heading(content, x, y, w, ...)` | the underline bar (or text bottom if no underline) |
| `callout(x, y, w, h, title, body, ...)` | `y + auto_sized_height` (height computed from body text) |
| `two_col_compare(x, y, w, h, ...)` | `y + max(left_items, right_items) * item_gap + header` |
| `flow_row(x, y, w, steps, ...)` | `y + box_h` |
| `numbered_list(x, y, w, items, ...)` | the final item's bottom Y |
| `bullet_list(x, y, w, items, ...)` | the final item's bottom Y |
| `table_header(x, y, w, cols, ...)` | `y + 34` (header row height) |
| `table_row(x, y, w, cols, vals, ...)` | `y + row_h` |

Low-level primitives that create a single element (`text`, `rect`, `ellipse`,
`svg`, `card`) return just the element — they don't need a bottom_y because
they're usually composed inside a helper that does.

## Auto-sizing helpers

### `callout` — auto-sizes to fit body text

The body height is estimated from:
- explicit newlines in the body text
- wrapping estimate: `chars_per_line = (w - 56) / (body_size * 0.55)`
- `body_line_h = body_size * 1.5`

```python
def callout(x, y, w, h, title, body, fill, accent, body_size=16):
    # estimate body height from text length + wrapping
    chars_per_line = max(20, int((w - 56) / (body_size * 0.55)))
    wrapped_lines = sum(max(1, (len(line) + chars_per_line - 1) // chars_per_line)
                        for line in body.split("\n"))
    body_line_h = int(body_size * 1.5)
    needed_body_h = wrapped_lines * body_line_h + 12
    needed_h = max(h, 48 + needed_body_h + 16)   # title(48) + body + pad(16)
    h = needed_h
    # ... draw card, accent bar, title, body ...
    return els, y + h                              # ← report actual bottom
```

### `two_col_compare` — auto-sizes to the column with more items

```python
def two_col_compare(x, y, w, h, lt, li, rt, ri, ...):
    item_gap = 52
    needed_h = 48 + max(len(li), len(ri)) * item_gap + 16
    h = max(h, needed_h)
    # ... draw both columns ...
    return els, y + h
```

## Side-by-side sections — use `max()`

When two sections sit on the same row, start them at the same cursor Y and
advance the cursor by the **maximum** of their bottoms:

```python
# two callouts side by side
els_c1, b1 = callout(70,  cursor, 460, 80, "KEY POINT", "...", fill=BLUE_SOFT, accent=BLUE)
els_c2, b2 = callout(550, cursor, 460, 80, "REMEMBER",  "...", fill=AMBER_SOFT, accent=RED)
els += els_c1 + els_c2
cursor = max(b1, b2) + SECTION_GAP
```

## Tables — chain rows with the returned bottom

```python
cols = [("Threat", 170), ("Description", 460), ("Example", 310)]

els_th, bottom = table_header(70, cursor, 940, cols, fill=RED)
els += els_th
cursor = bottom

for row in rows:
    els_tr, bottom = table_row(70, cursor, 940, cols, row, font=12)
    els += els_tr
    cursor = bottom
cursor += SECTION_GAP
```

## Plain text blocks — estimate height manually

For a `text(...)` element you create directly (not via a helper), estimate its
height and advance the cursor:

```python
# A text block of fontSize F, lineHeight L, N lines takes about F * L * N px
font_size = 19
line_height = 1.5
lines = 2  # estimate from text length / chars-per-line
text_h = int(font_size * line_height * lines)
els.append(text(70, cursor, 940, text_h, "...", fontSize=font_size, lineHeight=line_height))
cursor += text_h + SECTION_GAP
```

## Page height — fit to content

At the end of the page, set the page height to `cursor + bottom_padding`:

```python
return make_page(pid, els, height=cursor + 40)
```

This avoids both:
- **overflow** (page too short for content)
- **huge empty bottom** (page way taller than content)

## Complete worked example

```python
def build_page(content):
    els, cursor = page_header(N, content["title"])

    # Intro paragraph
    intro_h = estimate_text_height(content["intro"], font_size=19, width=940)
    els.append(text(70, cursor, 940, intro_h, content["intro"], fontSize=19, lineHeight=1.5))
    cursor += intro_h + SECTION_GAP

    # Two-column comparison (auto-sizes)
    els_t, bottom = two_col_compare(70, cursor, 940, 200,
        content["left_title"], content["left_items"],
        content["right_title"], content["right_items"])
    els += els_t
    cursor = bottom + SECTION_GAP

    # Flow diagram
    els_f, bottom = flow_row(70, cursor, 940, content["flow_steps"], box_h=64)
    els += els_f
    cursor = bottom + SECTION_GAP

    # REMEMBER callout (auto-sizes to body text)
    els_c, bottom = callout(70, cursor, 940, 80, "REMEMBER", content["remember"],
                            fill=AMBER_SOFT, accent=RED, body_size=17)
    els += els_c
    cursor = bottom + SECTION_GAP

    return make_page(f"page{N}", els, height=cursor + 40)
```

No section can ever overlap another, because each one's start Y is derived from
the previous one's actual rendered bottom. This is the whole game.
