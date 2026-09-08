# Image/PDF → HTML Conversion Instructions (MEMORY)

**IMPORTANT: These instructions MUST be followed every time we convert an image, PDF, or screenshot into an HTML note. Save and remember for all future uses.**

## Reference design template

The page layout template lives at:
`/home/z/my-project/VERIQTA_Linux_Security_Handbook_Page2.html`

Use this as the **structural + aesthetic baseline** for all converted notes:
- Cream paper background (`#f5f1e8`)
- Graph-paper grid overlay
- Spiral binding on the left edge (SVG rings extending outside the page)
- Navy header badges
- Card-based content sections
- Footer with source attribution

When converting a NEW image set, reuse this notebook aesthetic but adapt the inner content to match the reference images being converted.

---

## The 12 conversion rules

### 1. Exact visual recreation
- Treat the reference image as the **exact visual specification**.
- Do NOT redesign, simplify, modernize, reinterpret, or substitute elements.
- Reproduce EXACTLY: text, colours, typography, font sizes/weights, spacing, alignment, dimensions, proportions, borders, corner radii, backgrounds, shadows, lines, separators, icons, logos, icon colours/sizes/positioning, page structure.
- Goal: **pixel-level visual similarity** to the reference.

### 2. Icons — find the closest/exact match
- Identify EVERY icon, logo, symbol, and vector graphic in the reference.
- For EACH icon, search ALL of these sources (no priority/preference):
  - https://cdn.jsdelivr.net/npm/simple-icons@latest
  - https://xandemon.github.io/developer-icons/
  - https://www.flaticon.com/
  - https://thenounproject.com/
- Compare available icons and select the one **visually closest** to the reference icon — regardless of source.
- Match on: shape, silhouette, geometry, proportions, stroke width, line style, filled/outlined, internal details, negative space, corner treatment, orientation, colour, visual weight.
- If no exact match exists, use the closest vector icon and modify/reconstruct the SVG to match.

### 3. Never embed the reference image
- DO NOT use the reference image itself in the final document.
- No `<img>` of the reference, no background-image, no Base64, no screenshot, no cropped icons, no tracing the whole image.
- Every component must be independently recreated as: HTML text, CSS elements, inline SVG icons, CSS shapes, borders, layout elements.

### 4. Text must be real text
- Every visible piece of text → actual selectable HTML text.
- Do NOT convert text to images.
- Preserve: exact wording, capitalization, punctuation, line breaks, font weight, font size, letter spacing, line height, alignment, colour.

### 5. Icons must be real vector elements
- Every icon = inline SVG or genuine vector/HTML element.
- No rasterized icon screenshots.
- No runtime external icon libraries.
- Place SVG markup directly inside the HTML so it's self-contained.

### 6. Colours
- Analyse and reproduce colours as accurately as possible.
- Use exact HEX/RGB values, opacity, gradients, border colours, text colours, icon colours, backgrounds, accents.
- Do NOT replace specific colours with generic approximations ("red", "blue", "gray").

### 7. Layout
- Measure and reproduce the relative geometry.
- Page dimensions, margins, padding, element widths/heights, gaps, alignment, columns, rows, text wrapping, icon-to-text spacing, vertical rhythm, section spacing.
- Do NOT use approximate spacing when a more accurate measurement is possible.

### 8. Single HTML file
- Final deliverable = exactly ONE self-contained HTML file.
- Everything inline: `<style>` for CSS, inline SVG for icons, HTML for text/structure, inline JS only if genuinely necessary.
- Do NOT depend on: external CSS, external JS, external images, runtime icon libraries, remote assets, remote fonts (unless absolutely unavoidable).
- File must work when opened locally/offline.

### 9. PDF compatibility
- Design so it can be printed/exported to PDF with the same visual appearance.
- Use `@page`, page dimensions, print CSS, `break-inside`, `page-break`, print colours, fixed dimensions where necessary.

### 10. Word compatibility
- Structure with standard document-friendly HTML/CSS so it can convert to .docx.
- Text must remain selectable/editable.
- Do NOT sacrifice visual recreation for Word convertibility.

### 11. Icon licensing
- For every externally sourced icon, verify the license.
- Track: source, icon name, creator, license, attribution requirement.
- If attribution is legally required, include it in the final document.
- Do NOT assume an icon is free just because it's online.

### 12. Final verification
- Before delivering, perform a detailed visual comparison against the reference.
- Check EVERY element including small icons and details.
- Verify: text, font, font size, font weight, colours, icons (shape/colour/size/position), spacing, alignment, borders, backgrounds, shapes, shadows, dimensions, page breaks.
- If something doesn't match, correct it before delivering.

---

## Absolute requirement

The final result must be a **genuine recreation** of the reference design using editable text, HTML/CSS, and vector SVG elements. It must NOT simply contain the original image.

**Goal:** REFERENCE IMAGE → EXACTLY RECREATED HTML → PDF / WORD

**NOT:** REFERENCE IMAGE → IMAGE EMBEDDED INTO HTML/PDF/WORD

---

## Branding removal (ALWAYS apply)

After recreating the page, **remove all branding**:

1. **Remove "VERIQTA"** from everywhere in the HTML:
   - Top-left logo/text
   - Bottom-center branding
   - Watermark / background watermark
   - Footer
   - Any hidden / accessibility text

2. **Remove the entire social-media footer/handle section** at the bottom:
   - YouTube, GitHub, LinkedIn, X, Instagram, Telegram icons
   - All `@veriqta` handles

3. **Do NOT replace removed elements with anything.** Keep the rest of the page exactly as-is: same layout, spacing, typography, colors, cards, diagrams/icons, grid background, page number, and content.

4. After removal, **naturally rebalance** the remaining layout so there is no awkward empty branding space.

---

## Workflow (for future conversions)

1. Receive reference image(s) / PDF.
2. Create `/home/z/my-project/scripts/build-<name>-note.ts` — a bun script that generates the HTML.
3. **Use the notebook template** at `public/uploads/notebook-template/notebook-template.css` — link it externally. Do NOT inline the template CSS.
4. The HTML file should have this structure:
   ```html
   <head>
     <link rel="stylesheet" href="/uploads/notebook-template/notebook-template.css">
     <style>
       /* Note-specific CSS ONLY (cover page, special components) */
       /* Do NOT override body padding, .page-wrapper, .spiral, .holes, etc. */
     </style>
   </head>
   <body class="multi-page">
     <!-- .page-wrapper blocks (one per page) -->
   </body>
   ```
5. Recreate the inner content following the 12 rules above.
6. Remove all VERIQTA branding + social footer.
7. Output to `public/uploads/<note-name>.html`.
8. Place any image assets in `public/uploads/<note-name>/`.
9. Add the note to the database (via a bun script using `db.note.create`).
10. Verify in the browser with agent-browser + VLM.

### Template CSS includes (do NOT override these):
- `:root` color variables (paper, navy, blue, green, purple, red, gold, etc.)
- `body` padding (`24px 48px`) — needed for spiral ring visibility (rings at `left:-30px`)
- `body.multi-page` — column stacking with `gap:24px` for multi-page notes
- `.page-wrapper`, `.page`, `.page::before` (graph grid)
- `.spiral`, `.holes`, `.page-bend` (CSS background-image SVG binding)
- `.page-top-edge`, `.page-bottom-edge` (3D page-stack)
- `.top-strip`, `.badges`, `.badge`
- `.title-block`, `.title`, `.divider`
- `.body` (2-column grid: `1.85fr 1fr`)
- `.rows`, `.row`, `.row .icon` (58×58 pastel boxes), `.row h3`, `.row p`
- `.bg-blue`, `.bg-green`, `.bg-purple`, `.bg-red`, `.bg-gold`
- `.sidebar`, `.card`, `.card .head`, `.card .body-pad`
- `.file-row`, `.ficon`, `.fpath`, `.fdesc`, `.dashed`, `.warn`
- `.cmd-head-row`, `.term-pill`, `.cmd-list`
- `.cmd-row` (vertical: code on line 1, description on line 2 below — tight spacing)
- `.cmd-row code` (`white-space:pre`, `align-self:flex-start`, `font-size:12.5px`)
- `.cmd-row span` (`display:block`, `margin-top:1px`, `line-height:1.4`)
- `.page-wrapper { overflow:visible }` — so rings outside the page are visible
- Print/PDF rules (`@page`, `@media print`, `page-break-after:always`)

---

## Enhancement lessons (LEARNED — apply to ALL future conversions)

These are quality enhancements discovered during the "Linux for Complete Beginners" conversion. **Apply ALL of these to every future note you build.**

### A. Page titles — single-line, compact
- Use `font-size: 38px` for page titles (NOT 42px — too large, causes wrapping).
- Add `white-space: nowrap` to `.title` so titles stay on one line.
- For genuinely long titles (22+ chars at 38px), add a `.title.long { font-size: 32px; }` class — do NOT use `<br>` unless the title is extremely long (30+ chars even at 32px).
- Only 3-4 titles in a 20-page notebook should need `<br>`. If more than that have `<br>`, reduce the font size.
- Single-line titles save vertical space and look cleaner.

### B. Table alignment rules (ALL tables)
- **Header cells**: `text-align: center; vertical-align: middle;`
- **Body cells**: `text-align: left; vertical-align: middle; word-break: break-word;`
- **Code/command cells** (`.mono`, `code`): `white-space: nowrap;` — commands must NEVER wrap mid-word.
- **Font size**: `10.5px` for body cells, `10px` for headers — small enough to fit content without wrapping.
- **Padding**: `7px 10px` — tight but readable.
- **Even rows**: `background: #f8f5ec;` for zebra striping.
- If a table has many columns (7+), reduce font to `10px` and consider `table-layout: fixed` with column widths.

### C. Multi-column layouts for compact sections
- When 3 related sections appear together (e.g., a table + a terminal block + a tip box), use a **3-column flex layout**: `<div style="display:flex; gap:16px;">` with each child `flex:1; min-width:0;`.
- When 2 sections appear together, use **2-column**: `<div style="display:flex; gap:16px;">` with 2 children.
- This saves vertical space vs. stacking each section full-width.

### D. Practical exercise steps — 2-column grid
- Use `display: grid; grid-template-columns: 1fr 1fr; gap: 8px;` for steps-flow (NOT vertical stack).
- Add `.steps-flow .step:last-child:nth-child(odd) { grid-column: 1 / -1; }` so an odd last step spans full width.
- This matches the reference images which show steps flowing horizontally.

### E. Content completeness checklist (per page)
Before finishing each page, verify:
1. **Important Files** — every file mentioned must have a **description** of what it stores/does (e.g., `/etc/passwd — Stores user account information`). Don't just show the file path.
2. **Command tables** — must include BOTH the **generic command** (e.g., `sudo apt install <pkg>`) AND the **specific example** (e.g., `sudo apt install nginx`). Don't show only one.
3. **Practical exercises** — every page that has a practical section in the reference must have it in the HTML. Check for missing steps.
4. **Tips/Notes** — every tip box, note, warning, and "KEY TAKEAWAY" in the reference must be present.
5. **Footer content** — practice tips, goals, and page numbers must match.
6. **No empty space** — if a section in the reference is dense, the HTML should be dense too. Remove unnecessary vertical gaps.

### F. Spacing — compact, reference-matching
- Section gaps: `12-14px` between sections (NOT 20-30px).
- Card padding: `12px 14px` (NOT 20px+).
- Terminal block padding: `8px 10px`.
- Concept card padding: `12px 14px`.
- Title block margin: `14px 0 6px 0`.
- Divider margin: `8px 0`.
- The reference images are DENSE — match that density.

### G. VLM verification per page
- After generating the HTML, use `z-ai vision` to compare EACH page against its reference image.
- Check: title text, section headings, command names, table rows, tips, practical steps.
- If the VLM finds missing or incorrect content, fix it before moving on.
- At minimum, verify: (1) all sections present, (2) all commands present, (3) all tables have correct columns, (4) all practical exercises have the right number of steps.

### H. Structural integrity check
After all pages are built:
1. Count `.page-wrapper` elements — must equal the number of pages.
2. Count `<table>` open/close tags — must balance.
3. Count `<div>` open/close tags — must balance (check with a script).
4. Verify no "VERIQTA" text anywhere.
5. Verify the file is fully self-contained (no external URLs in `<link>`, `<script>`, `<img src>`).

