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
3. Use the notebook aesthetic from `VERIQTA_Linux_Security_Handbook_Page2.html` as the page template.
4. Recreate the inner content following the 12 rules above.
5. Remove all VERIQTA branding + social footer.
6. Output to `public/uploads/<note-name>.html`.
7. Place any image assets in `public/uploads/<note-name>/`.
8. Add the note to the database (via a bun script using `db.note.create`).
9. Verify in the browser with agent-browser + VLM.
