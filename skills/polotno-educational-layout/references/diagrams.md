# Diagrams — how to build them safely

Diagrams are the most layout-fragile part of a Polotno design. This file shows
how to build each common diagram type so arrows never collide with boxes,
labels never overlap shapes, and the flow direction is technically correct.

## General principles

1. **Determine relationships first.** What flows into what? What's a node vs
   an edge vs a label? Don't draw until you know the graph.
2. **Use a grid.** Nodes on a row share the same Y and height. Columns share
   the same X and width. This makes alignment trivial.
3. **Arrows live in arrow zones.** Between two boxes, reserve a 40px-wide
   "arrow zone" with padding on both sides. The arrow sits in the center of
   that zone and can never touch either box.
4. **Labels are part of the node.** Put a label inside its node (centered), or
   immediately beside it (with a clear gap). Never let a label float between
   two nodes where an arrow will cross it.
5. **Report your bottom.** Every diagram helper returns `(els, bottom_y)` so
   the next section starts below the diagram.

## 1. Horizontal flow diagram

`[A] → [B] → [C] → [D]`

Use `flow_row`. It computes the box width to fit the available space, places
each box on a shared Y, drops an arrow in the center of each arrow zone, and
returns the bottom of the row.

```python
def flow_row(x, y, w, steps, box_h=64, gap=14, fill=BLUE_SOFT, stroke=BLUE,
             arrow_color="1D4ED8", font=14):
    """Returns (els, bottom_y). Arrow is centered, never touches boxes."""
    els = []
    n = len(steps)
    arrow_w = 40                              # arrow zone width (with padding)
    box_w = (w - (arrow_w + gap) * (n - 1)) / n
    cx = x
    arr = ARROW_SVG.replace("1D4ED8", arrow_color)
    for i, step in enumerate(steps):
        els.append(card(cx, y, box_w, box_h, fill=fill, stroke=stroke, sw=2, radius=10))
        els.append(text(cx+10, y, box_w-20, box_h, step,
                        fontSize=font, fontWeight="600", fill=INK,
                        align="center", verticalAlign="middle", lineHeight=1.2))
        if i < n - 1:
            arrow_size = 28
            ax = cx + box_w + gap + (arrow_w - gap - arrow_size) / 2   # centered in zone
            ay = y + box_h / 2 - arrow_size / 2                          # vertically centered
            els.append(svg(ax, ay, arrow_size, arrow_size, arr))
        cx += box_w + arrow_w + gap
    return els, y + box_h
```

**Arrow SVG** (a right-pointing arrow, recolored by string-replace):

```python
ARROW_SVG = ("data:image/svg+xml;utf8," +
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
    "stroke='%231D4ED8' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'>"
    "<line x1='5' y1='12' x2='19' y2='12'/>"
    "<polyline points='12 5 19 12 12 19'/></svg>")
```

For a left-pointing arrow, mirror the polyline. For bidirectional, add a
polyline on both sides.

### Multi-line box content

Pass `"Threat\n(Attacker)"` — the `\n` becomes a line break inside the box.
The `verticalAlign: "middle"` + `align: "center"` keeps it centered.

## 2. Triangle / polygon diagram (e.g. CIA Triad)

Build the whole shape as one SVG (cleaner than composing shapes), with the
labeled circles as part of the SVG so they can't drift relative to the
triangle.

```python
tri_svg = ("data:image/svg+xml;utf8," +
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 280'>" +
    # triangle
    "<polygon points='150,50 50,225 250,225' fill='%23DBEAFE' " +
    "stroke='%231D4ED8' stroke-width='4' stroke-linejoin='round'/>" +
    # center label
    "<text x='150' y='150' font-size='18' font-weight='bold' " +
    "fill='%231D4ED8' text-anchor='middle' font-family='sans-serif'>CIA</text>" +
    "<text x='150' y='175' font-size='18' font-weight='bold' " +
    "fill='%231D4ED8' text-anchor='middle' font-family='sans-serif'>TRIAD</text>" +
    # vertex circles — white stroke separates them from the triangle lines
    "<circle cx='150' cy='50' r='26' fill='%23B91C1C' stroke='white' stroke-width='3'/>" +
    "<text x='150' y='58' font-size='22' font-weight='bold' fill='white' " +
    "text-anchor='middle' font-family='sans-serif'>C</text>" +
    "<circle cx='50' cy='225' r='26' fill='%23B91C1C' stroke='white' stroke-width='3'/>" +
    "<text x='50' y='233' font-size='22' font-weight='bold' fill='white' " +
    "text-anchor='middle' font-family='sans-serif'>I</text>" +
    "<circle cx='250' cy='225' r='26' fill='%23B91C1C' stroke='white' stroke-width='3'/>" +
    "<text x='250' y='233' font-size='22' font-weight='bold' fill='white' " +
    "text-anchor='middle' font-family='sans-serif'>A</text>" +
    "</svg>")
els.append(svg(110, y, 300, 280, tri_svg))
```

**Why the white stroke on the circles**: it creates a visual gap between the
red circle and the blue triangle line, so the circle reads as "on the vertex"
rather than "cutting the line". This is the fix for the common "C/I/A circles
look stuck to the triangle" bug.

## 3. Tree / hierarchy diagram

A root node above, children below, vertical connectors between them.

```
            [Root]
           /  |  \
       [A]  [B]  [C]
```

Layout:
- Root box centered at the top.
- N child boxes in a row below, evenly spaced.
- For each child, a vertical line from root's bottom-center to child's
  top-center. The line is a `figure` with `subType: "rect"` of width 2px,
  or an SVG path.

Use the cursor pattern: render the root, advance cursor by root height +
connector length, then render the children row.

## 4. Architecture diagram (layered)

Layers stacked vertically, each layer a horizontal card containing 1–N
components.

```
┌─────────── Internet ───────────┐
└───────────────┬────────────────┘
                ↓
┌─────────── Firewall ──────────┐
└───────────────┬────────────────┘
                ↓
┌──────── Internal Network ──────┐
│  [Web]  [App]  [DB]            │
└────────────────────────────────┘
```

Layout:
- Each layer is a `card` (rounded rect with a label inside).
- Between layers, a single down-arrow centered horizontally.
- Inside a layer, components are small boxes in a row.

Use the cursor pattern: card → arrow → card → arrow → card. Each step reports
its bottom, so the next layer starts cleanly below.

## 5. Comparison table

For tabular data (Risk vs Vulnerability vs Threat, Symmetric vs Asymmetric,
etc.):

```python
cols = [("Concept", 200), ("Reversible?", 150), ("Uses Key?", 140),
        ("Purpose", 290), ("Examples", 160)]

els_th, bottom = table_header(70, cursor, 940, cols, fill=RED)
els += els_th
cursor = bottom

for row in rows:
    els_tr, bottom = table_row(70, cursor, 940, cols, row, font=13)
    els += els_tr
    cursor = bottom
cursor += SECTION_GAP
```

**Column widths must sum to the table width.** Before building, verify:
`sum(col_width for _, col_width in cols) == table_width`. If they don't sum,
columns will overlap or leave gaps.

**Row height for wrapping text:** if a cell's text is long, increase `row_h`
for that row. The default 36px only fits one line; for 2-line cells use 48px,
for 3-line use 60px.

## 6. Numbered list / bullet list

Not strictly a "diagram" but a structured layout. Each item is a row with a
marker (numbered circle or bullet) and the text. Use `numbered_list` /
`bullet_list` which return the final item's bottom Y.

For two-column lists, split the items array and place each column side by side,
advancing the cursor by `max(left_bottom, right_bottom) + SECTION_GAP`.

## Anti-patterns to avoid

1. **Floating arrows.** Never place an arrow with a hardcoded X hoping it lands
   between two boxes. Always compute `ax = cx + box_w + gap + (arrow_w - gap -
   arrow_size) / 2` from the actual box positions.

2. **Labels outside nodes.** If a label sits next to a node instead of inside
   it, an arrow will eventually cross it. Put labels inside the node, or leave
   a clear gap (≥ 40px) between the label and any arrow zone.

3. **Random icons.** Don't sprinkle SVG icons "for decoration". Each icon must
   improve comprehension. If it doesn't, remove it.

4. **Social-media icons.** Thumbs-up, paper-plane, person-add, heart-as-like
   are promotional. The validator flags their SVG path signatures. Don't add
   them.

5. **Diagrams that lie.** For technical content, the diagram must match the
   described relationship. If the text says "A feeds into B which feeds into
   C", the arrows must go A→B→C, not A→C with B floating off to the side.
