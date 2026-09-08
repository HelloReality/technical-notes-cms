---
name: polotno-educational-layout
description: >
  Generate render-safe, overlap-free Polotno JSON for educational notes, technical
  documents, diagrams, and infographics. Use this skill whenever the user asks to
  convert content (PDF, notes, lecture material, technical docs) into Polotno JSON,
  to "make a Polotno design", to generate a study-note / cheat-sheet / infographic
  layout, to fix overlapping or clipped Polotno layouts, or to reflow/redesign an
  existing Polotno design for readability. Also use it when generating Polotno
  pages for cybersecurity, networking, programming, cloud, system design, exam
  prep, or any technical educational content. Triggers on phrases like "polotno
  json", "polotno design", "convert to polotno", "study notes layout", "fix
  overlap in polotno", "educational infographic", "reflow the layout".
---

# Polotno Educational Layout Generation

This skill turns GLM into a **professional educational-document layout engine**
for Polotno JSON. Instead of placing independent elements on a canvas, you
analyze the content, determine the document structure, calculate the space each
section needs, and only then emit Polotno JSON — so the output renders cleanly
in any Polotno-compatible viewer without overlap, clipping, or manual fix-up.

## The mindset shift (read this first)

Stop thinking: *"Where should I place this element?"*

Start thinking: *"What is the structure of this section, how much space does it
require, and where should the next section begin after this section has
completely finished?"*

Every layout decision flows from that question. If you find yourself assigning
a hardcoded Y coordinate to a section whose height depends on rendered text,
stop — that is the root cause of every overlap bug. Use the cursor pattern
described in `references/cursor-layout.md`.

## When this skill applies

Apply this skill automatically to **every** task that produces or modifies
Polotno JSON for an educational / technical document:

- new document generation
- page generation
- regeneration
- content expansion
- layout correction / overlap fixes
- document enhancement

Do not hardcode domain-specific layouts (e.g. cybersecurity-only). The same rules
apply to networking notes, programming notes, cloud architecture, system
design, exam prep, lecture notes, process diagrams, flowcharts, comparison
sections, and educational infographics.

## The generation pipeline

```
BASE POLOTNO GENERATION RULES   (schema — see references/polotno-schema.md)
        +
POLOTNO EDUCATIONAL LAYOUT SKILL  (this file — layout rules)
        +
USER CONTENT                       (the source material to lay out)
        +
REFERENCE IMAGE / DESIGN REQUIREMENTS   (style guidance, not coordinates)
        ↓
      GLM
        ↓
POLOTNO JSON  →  validator (scripts/validate_layout.py)  →  fix & ship
```

**Always run the validator before returning JSON.** It detects overlaps,
overflow, out-of-bounds elements, unreadably small text, and promotional content
programmatically. If it reports problems, fix them and re-run. See
"Render validation" below.

## Design priority (in strict order)

When two concerns conflict, the earlier one wins. Never trade an earlier
concern for a later one. **Never sacrifice #1–#7 merely to preserve the
original coordinates or card dimensions.**

1. **Content fitting inside containers** — every text element must fit inside
   its card (height + width), with wrapping accounted for.
2. **No overlap** — no element may cover another.
3. **No clipping / overflow** — all text fully visible inside its container;
   no text extends below a card or page boundary.
4. **Readable typography** — body ≥ 12px, headings ≥ 14px; never shrink to fit
   coordinates.
5. **Correct spacing** — compact, consistent gaps; no stretching to fill.
6. **Correct alignment** — shared grid; columns share top/bottom edges.
7. **Diagram correctness** — arrows point the right way; nodes connect
   logically; labels don't overlap shapes.
8. **Balanced composition** — fill the page naturally; no large empty bottom.
9. **Visual similarity to reference** — reproduce the design *language*, not
   the coordinates. If the reference has an obvious defect, improve it.
10. **Decorative details** — only after everything above is satisfied.

## Core layout rules

### 1. No overlapping

Never allow: text over text, text over diagrams, text over arrows, text over
icons, cards over cards, sections over sections, labels over diagram lines, or
elements extending into another section. Every element needs its own space.

### 2. No text clipping

Every text element must fit completely inside its intended container. Never
allow: truncated text, hidden bullet points, text extending outside cards,
text hidden behind shapes, or text cut off at the bottom of a section. If a
text block would overflow its box, **grow the box** — don't shrink the font.

### 3. Dynamic vertical layout (the cursor pattern)

Do **not** blindly assign fixed Y coordinates to sections. Conceptually:

```
sectionHeight = titleHeight + contentHeight + padding + spacing
nextSectionY  = previousSectionY + previousSectionHeight + sectionGap
```

Later sections must move downward when earlier content becomes taller. The
mechanism for this is the **cursor pattern** — every layout helper returns the
Y coordinate of its own bottom edge, and the caller advances a cursor by that
amount before placing the next section. Full details and a worked example:
`references/cursor-layout.md`.

### 4. Content-aware containers

Container height is based on the amount of content. If a card holds more text,
increase its height, reflow the content, and push following sections downward.
**Do not** solve overflow by making the font extremely small.

### 5. Readability over compression

Use readable font sizes (body text ≥ 14px for dense pages, ≥ 16px preferred;
headings 18–28px; titles 36–48px). If content does not fit, in order:

1. increase the available space (grow the container / page height)
2. reflow the layout (move a section to its own row, switch 1-col → 2-col)
3. reorganize sections (split a long section, reorder for balance)
4. intelligently shorten redundant wording (preserve all facts)
5. only then consider a minor font reduction (never below 12px body)

Never aggressively shrink text just to preserve coordinates.

### 6. Content-fit rule (containers must fit their content)

Every card/container must be **content-aware**. Before generating the final
coordinates, calculate the space required by:

```
topPadding
+ headingHeight
+ headingGap (heading → first bullet)
+ sum(eachItemHeight + itemGap)   ← every bullet, with wrapping
+ bottomPadding (last bullet → card bottom)
```

Then enforce: `cardHeight >= requiredHeight`. **Never generate a card whose
content requires more height than the card provides.**

If the content is longer:
1. Increase the card height.
2. Recalculate the positions of all elements below it (cursor advances).
3. Move subsequent sections downward.
4. Recalculate the overall page layout.

**Never allow content to escape the card.** Empty space inside a card is
acceptable; overflow is not.

### 7. Text wrapping is part of the height calculation

A text block containing `"Protects sensitive data (personal, financial, business)."`
may occupy one line at one width and multiple lines at another width. Therefore
estimate/derive the rendered line count from:

- text length
- font size
- font family (CC Dash To School is a **wide** handwritten font — use
  `0.52 × fontSize` as the average character width, not the usual `0.55`)
- text box width
- character density (lowercase narrow, uppercase/MW wide)

Use the resulting height when positioning the next item. **Never calculate
vertical positions assuming every bullet is one line.** The skill's validator
(`scripts/validate_layout.py`) uses `_text_content_height()` to do this
estimate and flags any text whose content extends below its container — treat
those flags as hard failures, not warnings.

### 8. Bullet-list sequential flow (no distribution)

Do **not** position bullets using arbitrary fixed Y coordinates, and **never**
distribute bullets evenly across the card's available height (no
`justify-content: space-between`-style logic). Instead use sequential flow:

```
heading
  ↓ (small heading-to-content gap)
bullet 1
  ↓ (small consistent gap)
bullet 2
  ↓ (small consistent gap)
bullet 3
  ↓ (small consistent gap)
bullet 4
  ↓ (medium bottom padding)
card bottom
```

Each item's Y position depends on the **actual height of the previous item**
(wrapping-aware), not on a fixed pitch. Conceptually:

```
currentY = contentStartY
for each item:
    place item at currentY
    currentY += actualItemHeight + itemGap
# then verify:
currentY + bottomPadding <= cardBottom
# if it fails, grow the card — never shrink the gap to force-fit
```

Compact, consistent spacing. Unused card space at the bottom is acceptable.

### 9. Cards with different content lengths (no artificial stretching)

Do **not** force every card to have identical internal spacing. Card A (4 short
bullets) and Card B (3 long bullets) may require different content heights.

For side-by-side cards where equal height is visually desirable:
1. Calculate each card's **required** height independently (from its own
   content, with its own wrapping).
2. `sharedHeight = max(requiredA, requiredB)`.
3. Vertically flow each card's content naturally from the top within that shared
   height — compact gaps, top-aligned.
4. **Never** make the shorter card's bullets widely separated just because the
   card is taller. The shorter card's bullets stay compact at the top; the
   extra height becomes bottom padding.

### 10. Render-first thinking

A JSON structure is **not** correct just because every object has valid x/y
values, every object is inside the page, and the schema is valid. It is correct
only when the **rendered result** is visually correct.

The final rendered result must have:
- NO overflow
- NO clipping
- NO overlapping
- NO hidden bullets
- NO text outside cards
- NO section collisions

Always validate with `scripts/validate_layout.py` before returning JSON, and
treat any reported problem as a hard failure that must be fixed.

## Grid and spacing

Use a consistent page grid. Maintain:

- consistent left/right margins (suggest 70px on a 1080px-wide page)
- consistent section spacing (suggest `SECTION_GAP = 26px`)
- consistent card padding (suggest 16–20px internal padding)
- consistent heading spacing (heading bar + 10px gap to content)
- consistent alignment (columns share top edges; rows share left edges)
- consistent gaps between columns (suggest 20–24px)
- consistent diagram spacing (nodes in a row share the same Y and height)

Elements in the same section should share alignment boundaries. Avoid arbitrary
positioning unless the diagram genuinely requires it.

## Diagram rules

Treat diagrams as structured systems, not decorations. For every diagram:

1. Determine the logical relationships first (what flows into what).
2. Position nodes/components on a grid.
3. Position labels.
4. Position connecting lines/arrows.
5. Verify lines do not cross text unnecessarily.
6. Verify arrows do not touch or obscure labels.
7. Keep sufficient spacing between nodes.
8. Ensure the diagram communicates the intended technical relationship
   accurately.

Do not add a diagram merely because it would look attractive. For technical
subjects (cybersecurity, networking, cloud architecture, authentication, APIs,
databases, protocols), prioritize technical correctness over decoration.

For the supported diagram types and how to build them safely, see
`references/diagrams.md`.

## Arrow rules

Arrows must:

- point in the correct direction
- be centered relative to the connected objects (vertically centered with
  boxes of equal height; horizontally centered between two boxes)
- have sufficient spacing from text (never touch a box border)
- not overlap labels
- not disappear underneath boxes
- clearly communicate flow

For flow diagrams, use a consistent visual pattern:

```
[Component] → [Component] → [Component]
```

Each arrow sits in its own "arrow zone" with padding on both sides, so it can
never collide with neighbouring boxes. See `flow_row` in
`references/cursor-layout.md`.

## Icons and symbols

Use icons/symbols only when they improve comprehension. Icons should:

- match the visual style (line weight, color palette)
- have consistent sizing across the document
- be aligned with their related text (vertically centered with the label)
- not interfere with surrounding content

Do not use random decorative icons. Do not introduce social-media branding (see
next section).

## Remove promotional content

Automatically prevent the following from appearing in generated educational
documents:

- `@creator` handles (e.g. `@aman_views`, `@anything_views`)
- Instagram / YouTube / Twitter-X / Facebook / TikTok / Telegram / WhatsApp /
  Snapchat / LinkedIn handles
- LIKE / SHARE / FOLLOW / SUBSCRIBE buttons
- creator branding, promotional CTAs
- "Get PDF", "Download PDF", "TO GET PDF NOTES", "COMMENT PDF"
- social-media icons used for promotion (thumbs-up, paper-plane, person-add,
  heart-as-like)
- unrelated promotional graphics

The educational content itself must remain fully intact. The validator script
(`scripts/validate_layout.py`) includes a generic promo detector that flags
these by text pattern and SVG path signature — so even if the exact handle or
icon differs, it is still caught.

## Page space management

Use the available page space intelligently:

- Do **not** compress content into the top of the page while leaving a large
  empty area at the bottom.
- Do **not** stretch content artificially just to fill the page.
- Aim for balanced visual density — the page should end shortly after the last
  section's bottom edge (e.g. `pageHeight = cursor + 40px` bottom padding).
- If content naturally requires more space, allow the layout to use it (grow
  the page height rather than truncating content).

## Section management

Each section has:

- a clear heading
- clear boundaries (card / callout / underline)
- appropriate spacing (SECTION_GAP above and below)
- predictable internal padding
- sufficient height (auto-sized to its content)
- an independent layout (its height is reported back so the next section starts
  below it)

A section must never visually cover another section. If a section becomes
taller, every subsequent section moves accordingly (cursor advances by the
returned bottom Y).

## Render validation (mandatory before returning JSON)

Before returning the final Polotno JSON, run the validator and confirm every
check passes:

```bash
python3 /home/z/my-project/skills/polotno-educational-layout/scripts/validate_layout.py <file.json>
```

The validator checks:

**Per-card containment (the most important checks):**
- [ ] Every text element fits inside its container card — content height (with
  wrapping) ≤ card bottom
- [ ] Every text element's width fits inside its container card — element right
  edge ≤ card right edge
- [ ] The bottom of the last bullet is above the card bottom (with padding)
- [ ] Wrapped lines are accounted for (using `0.52 × fontSize` char width for
  CC Dash To School)
- [ ] Bullets are positioned sequentially (each Y depends on the previous
  item's actual height)
- [ ] No text outside its intended container

**Per-page checks:**
- [ ] No text overlaps (bounding-box intersection of text elements, using
  content bounding boxes not full element height)
- [ ] No text is clipped (text content height fits inside its assigned box)
- [ ] No container overflow (every child fits inside its parent's bounds)
- [ ] No section overlap (cards / callouts don't intersect)
- [ ] No diagram overlap (flow boxes + arrows don't collide)
- [ ] No arrow collision (arrow zones don't overlap boxes)
- [ ] No label collision (diagram labels don't overlap shapes)
- [ ] No elements outside page boundaries
- [ ] No unreadably small text (body ≥ 12px, headings ≥ 14px; bullet markers
  like • ★ ✓ ✗ are exempt)
- [ ] No accidental promotional/social elements (text + SVG path signatures)
- [ ] Consistent margins (content within left/right margin)
- [ ] Consistent spacing (section gaps within tolerance)
- [ ] Correct diagram relationships (arrows point along the flow direction)
- [ ] Balanced page composition (no huge empty bottom area > 25% of page)
- [ ] All important educational content is visible

**Per-section checks:**
- [ ] Does it overlap the previous section?
- [ ] Does it overlap the next section?
- [ ] Does any child element extend outside its section?

If any check fails, **revise the layout and re-run the validator** before
returning JSON. Do not return JSON that fails validation. The validator exit
code is 0 only when every check passes.

## Reference image handling

When a reference image is provided, extract from it:

- overall page structure (section order, column counts)
- typography hierarchy (title / heading / body sizes)
- color palette (backgrounds, accents, text colors)
- section hierarchy (which sections are cards, which are plain)
- card structure (border radius, fill, stroke)
- diagram structure (node shape, arrow style, label placement)
- spacing relationships (gap between sections, padding inside cards)
- alignment (left/center/right; shared edges)
- visual style (handwritten vs formal, playful vs technical)

Reproduce the **design language**, not the coordinates. The reference image is a
design reference, not a coordinate map. If the original layout contains an
obvious overlap or unreadable area, improve it rather than reproducing the
defect.

## Reusability — keep it generic

This skill is generic and applies to:

- cybersecurity notes
- networking notes
- programming notes
- cloud architecture
- system design
- exam preparation
- lecture notes
- technical documentation
- process diagrams
- flowcharts
- comparison sections
- architecture diagrams
- educational infographics

Do **not** hardcode domain-specific layouts. The cursor pattern, the diagram
builders, the validator, and the promo filter are all domain-agnostic.

## Integration with the existing pipeline

This skill layers onto the base Polotno schema (see
`references/polotno-schema.md`) without changing it. The schema stays valid for
`store.loadJSON()`, Polotno Studio, and `@polotno/store`. The skill only
constrains *how* elements are positioned and *which* elements are allowed — it
does not invent new element types or properties.

When integrating into a code generator (like the Python generator in
`/home/z/my-project/output/cybersecurity/generate_polotno.py`):

1. Load this SKILL.md as the system instruction for the layout pass.
2. Generate the JSON using the cursor pattern.
3. Run `scripts/validate_layout.py` on the output.
4. If validation fails, re-prompt with the failure report and regenerate.
5. Ship only after validation passes.

## Final reminder

The most important behaviour: **the layout is a chain of sections, each one
reporting how tall it is, so the next one knows where to start.** Get that
right and overlaps become impossible by construction. Everything else in this
skill supports that one idea.
