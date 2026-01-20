---
name: diagram
description: Create SVG diagrams from ASCII art using svgbob. Use when drawing flowcharts, architecture diagrams, sequence diagrams, or any visual illustration for blog posts.
allowed-tools: Read, Write, Bash, Glob
---

# ASCII Diagram Skill

Create professional SVG diagrams from ASCII art for blog posts using svgbob.

## Workflow

1. **Create ASCII art** in a `.txt` file (usually in `_drafts/materials/<post-slug>/`)
2. **Convert to SVG** using `bin/diagram`
3. **Embed in post** with markdown image syntax

## Tool Usage

```bash
# Basic conversion
bin/diagram input.txt                     # → assets/images/diagrams/input.svg

# Custom output name
bin/diagram input.txt my-diagram.svg      # → assets/images/diagrams/my-diagram.svg

# From stdin
echo "A --> B" | bin/diagram - flow.svg

# Recommended: transparent background for dark mode
BACKGROUND=none bin/diagram input.txt

# Other options (rarely needed)
STROKE_COLOR=#333 bin/diagram input.txt   # Custom line color
```

## Options

| Variable | Default | Description |
|----------|---------|-------------|
| `SCALE` | 1 | Scale factor (2 = double size) |
| `BACKGROUND` | white | Background color (`none` for transparent) |
| `STROKE_COLOR` | black | Line/stroke color |
| `FILL_COLOR` | black | Shape fill color |
| `FONT_SIZE` | 14 | Text size in pixels |

## Embedding in Posts

```markdown
![Architecture diagram](/assets/images/diagrams/architecture.svg)
```

## Quick Reference

See [REFERENCE.md](REFERENCE.md) for complete svgbob ASCII syntax.

### Essential Characters

| Char | Purpose | Example |
|------|---------|---------|
| `-` | Horizontal line | `----` |
| `\|` | Vertical line | `\|` |
| `+` | Corner/intersection | `+--+` |
| `.` `'` | Rounded corners | `.--. '--'` |
| `>` `<` `^` `v` | Arrows | `-->` `<--` |
| `/` `\` | Diagonal lines | `/` `\` |
| `*` | Filled circle | `--*--` |
| `o` | Open circle | `--o--` |

### Common Patterns

**Box:**
```
+-------+
|  Box  |
+-------+
```

**Rounded box:**
```
.-------.
|  Box  |
'-------'
```

**Arrow:**
```
A -----> B
```

**Diamond (decision):**
```
   /\
  /  \
 /    \
 \    /
  \  /
   \/
```

**Flow:**
```
.---.     .---.     .---.
| A |---->| B |---->| C |
'---'     '---'     '---'
```

## Best Practices

1. **Use monospace font** when editing ASCII art
2. **Use spaces, not tabs** - tabs have inconsistent widths and break alignment
3. **Avoid parentheses `()` inside boxes** - svgbob interprets them as curves; use `[]` or omit
4. **Keep it simple** - svgbob works best with clean, well-spaced diagrams
5. **Test incrementally** - convert often to catch rendering issues early
6. **Use transparent background** (`BACKGROUND=none`) for dark mode compatibility
7. **Use default scale** (`SCALE=1`) - SVGs are vector and scale naturally
8. **Place labels beside lines, not crossing them** - put captions above or below arrows, not on the same line
9. **Don't let arrows touch boxes** - leave a gap between arrow endpoints and box borders
10. **Use smooth corners for arrows** - use `'` and `.` for rounded turns instead of `+`

### Arrow Corners

**Good - smooth corners:**
```
    .---->
    |
----'
```

**Bad - sharp corners:**
```
    +---->
    |
----+
```

### Labels and Arrows

**Good - label below the line:**
```
.-----.                .-----.
|  A  |--------------->|  B  |
'-----'  sends data    '-----'
```

**Bad - label crosses the line:**
```
.-----.                .-----.
|  A  |-- sends data ->|  B  |
'-----'                '-----'
```

**Good - arrow ends before box:**
```
.-----.
|  A  |
'-----'
   ^
   |
   | label
   |
.--+--.
|  B  |
'-----'
```

**Bad - arrow touches/enters box:**
```
.-----.
|  A  |
'--^--'
   |
.--+--.
|  B  |
'-----'
```

## Adding Colors to Diagrams

svgbob doesn't support native coloring (the legend syntax shown on svgbob-editor demo page is not implemented). Use manual SVG editing instead:

### Workflow

1. Generate the SVG with `bin/diagram`
2. Open the SVG and find the `<rect class="backdrop">` element
3. Add colored `<rect>` elements right after it (before other shapes)
4. Position and size them to match target boxes

### Example

```xml
<rect class="backdrop" x="0" y="0" width="496" height="336"></rect>
<!-- Colored backgrounds (add these) -->
<rect x="4" y="8" width="112" height="64" fill="#e8f4fc" rx="4"></rect>
<rect x="284" y="152" width="144" height="48" fill="#e8f5e9" rx="4"></rect>
```

### Finding Coordinates

1. Look for `<text>` elements with the box label to find x/y position
2. Look for the box's `<path>` or `<line>` elements to find dimensions
3. Add small padding (4px) and round corners (`rx="4"`)

### Recommended Colors

Use subtle, light colors that work on white backgrounds:
- Light blue: `#e8f4fc` (primary elements)
- Light green: `#e8f5e9` (secondary elements)
- Light yellow: `#fff9e6` (highlights)
- Light gray: `#f5f5f5` (neutral)
