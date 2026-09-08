# Polotno JSON Schema (verified)

Source: https://polotno.com/docs/schema (Store, Page, TextElement, FigureElement,
SVGElement, LineElement). Verified against Polotno SDK `store.loadJSON()`.

## Top-level store

```json
{
  "schemaVersion": 4,
  "width": 1080,
  "height": 1750,
  "unit": "px",
  "dpi": 72,
  "fonts": [
    { "fontFamily": "CC Dash To School", "url": "/fonts/CCDashToSchool.woff2" }
  ],
  "pages": [ /* Page objects */ ]
}
```

- `schemaVersion`: integer, use `4`.
- `width`, `height`: default canvas size. Per-page sizes override these.
- `unit`: `"px"` | `"pt"` | `"mm"` | `"cm"` | `"in"`.
- `dpi`: dots-per-inch for print calculations (default 72).
- `fonts`: array of `{ fontFamily, url }` (single-variant) or
  `{ fontFamily, styles: [{ src, fontStyle, fontWeight }] }` (multi-variant).

## Page

```json
{
  "id": "page1",
  "width": 1080,
  "height": 1750,
  "background": "#FDFBF7",
  "children": [ /* elements */ ]
}
```

- `id`: unique page identifier (string).
- `width`, `height`: page-specific size (can override store default; can be
  `"auto"`).
- `background`: color string (hex / named / `transparent`).

## Element base (shared by all element types)

Every element has:

- `id` (string, unique within the page)
- `type` (string — see below)
- `x`, `y` (number, top-left position in px)
- `width`, `height` (number, in px)
- `rotation` (number, degrees; default 0)
- `opacity` (number 0–1; default 1)

## TextElement — `type: "text"`

```json
{
  "id": "text_1",
  "type": "text",
  "x": 70, "y": 248, "width": 940, "height": 60,
  "text": "Cybersecurity is the practice of...",
  "fontSize": 19,
  "fontFamily": "CC Dash To School",
  "fontStyle": "normal",
  "fontWeight": "normal",
  "fill": "#1E293B",
  "align": "left",
  "verticalAlign": "top",
  "textDecoration": "none",
  "lineHeight": 1.5,
  "letterSpacing": 0
}
```

Key properties:

- `text`: the visible text. Use `\n` for explicit line breaks.
- `fontSize`: in px (minimum 1; readability floor 12).
- `fontFamily`: must match a `fonts[].fontFamily` entry, or a system font.
- `fontStyle`: `"normal"` | `"italic"`.
- `fontWeight`: `"normal"` | `"bold"` | numeric string like `"600"`.
- `fill`: text color.
- `align`: `"left"` | `"center"` | `"right"` | `"justify"`.
- `verticalAlign`: `"top"` | `"middle"` | `"bottom"`.
- `textDecoration`: `"none"` | `"underline"` | `"line-through"`.
- `lineHeight`: multiplier (e.g. `1.5`) or `"auto"`.

**Text background** (optional): to give the text element its own background fill,
use all of these together:

```json
"backgroundEnabled": true,
"backgroundColor": "#FEF3C7",
"backgroundCornerRadius": 8,
"backgroundPadding": 6,
"backgroundOpacity": 1
```

Do **not** use a bare `backgroundColor` without `backgroundEnabled: true` —
Polotno ignores it.

## FigureElement — `type: "figure"`

Rectangles, ellipses, triangles, and other shapes all use `type: "figure"` with
a `subType`.

```json
{
  "id": "fig_1",
  "type": "figure",
  "subType": "rect",
  "x": 70, "y": 100, "width": 940, "height": 80,
  "fill": "#DBEAFE",
  "stroke": "#1D4ED8",
  "strokeWidth": 2,
  "cornerRadius": 12,
  "dash": []
}
```

- `subType`: `"rect"` | `"ellipse"` | `"triangle"` | other supported shapes.
  - **rect** → rectangle (use `cornerRadius` for rounded corners).
  - **ellipse** → ellipse/circle (set width == height for a circle).
- `fill`: color or `"transparent"`.
- `stroke`: border color (empty string = no border).
- `strokeWidth`: border width in px.
- `cornerRadius`: corner radius in px (rect only).
- `dash`: array of numbers for dashed border, e.g. `[8, 6]`. Empty `[]` = solid.

### Critical schema notes

- There is **no `type: "rect"`** in Polotno. Use `type: "figure"` with
  `subType: "rect"`.
- There is **no `type: "circle"`**. Use `type: "figure"` with `subType: "ellipse"`.
- The property is **`cornerRadius`**, not `borderRadius`. (Polotno is built on
  Konva, which uses `cornerRadius`.)
- For a filled shape with no border, set `fill` to a color and `stroke` to `""`
  (empty string), `strokeWidth` to `0`.

## SVGElement — `type: "svg"`

```json
{
  "id": "svg_1",
  "type": "svg",
  "x": 120, "y": 280, "width": 240, "height": 220,
  "src": "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' ...>...</svg>"
}
```

- `src`: URL or data URI of the SVG. Data URIs let you embed SVG inline.
- For icons, embed the SVG markup directly as a `data:image/svg+xml;utf8,...`
  URI. URL-encode `#` as `%23` inside the SVG.

## LineElement — `type: "line"`

```json
{
  "id": "line_1",
  "type": "line",
  "x": 70, "y": 240, "width": 940, "height": 0,
  "color": "#B91C1C",
  "dash": []
}
```

- `color`: the line color. (Not `fill` — lines use `color`.)
- `width`: the line length.
- `height`: 0 for a horizontal line.
- `dash`: array for dashed line, e.g. `[6, 8]`.

## Common gotchas

1. **Don't invent element types.** Only `text`, `figure`, `svg`, `line`, `image`,
   `gif`, `video`, `table`, `group`, `table-cell`, `audio` are valid.
2. **Don't use `borderRadius`** anywhere — use `cornerRadius` on figures, and
   `backgroundCornerRadius` on text backgrounds.
3. **Don't put `backgroundColor` on a text element without `backgroundEnabled:
   true`** — it will be ignored.
4. **Lines use `color`, not `fill`.** Mixing these up makes the line invisible.
5. **Every `id` must be unique within its page.** Re-using an ID can cause
   Polotno to drop one of the elements.
6. **Font family must be loaded.** Either list it in the store's `fonts` array
   (with a `url`), or use a system font. Otherwise text falls back to the
   default and looks wrong.

## Minimal valid store

```json
{
  "schemaVersion": 4,
  "width": 1080,
  "height": 1750,
  "unit": "px",
  "fonts": [],
  "pages": [
    {
      "id": "page1",
      "width": 1080,
      "height": 1750,
      "background": "#ffffff",
      "children": [
        {
          "id": "t1",
          "type": "text",
          "x": 70, "y": 70, "width": 940, "height": 60,
          "text": "Hello, Polotno.",
          "fontSize": 24,
          "fill": "#000000"
        }
      ]
    }
  ]
}
```

This is the minimum `store.loadJSON()` accepts. Everything else in this skill is
about laying out the `children` array so it renders cleanly.
