# Svgbob ASCII Syntax Reference

Complete reference for svgbob drawing characters and patterns.

## Lines

### Horizontal Lines
```
Solid:      -------- or ========
Broken:     - - - - - (spaces between)
Low line:   ________
```

### Vertical Lines
```
Solid:      |        Broken:     :        or    !
            |                    :              !
            |                    :              !
```

### Diagonal Lines
```
Forward:    /        Backslash:  \
           /                      \
          /                        \
```

## Corners

### Sharp Corners (using `+`)
```
+--+    +--+
|  |    |  +--
+--+    +--+
```

### Rounded Corners
```
Top-left:     .    or    ,
Top-right:    .    or    ,
Bottom-left:  `    or    '
Bottom-right: `    or    '

Example rounded box:
.--------.
|        |
'--------'
```

### Corner Connection Rules
| Character | Rounded corner when connected from... |
|-----------|--------------------------------------|
| `.` `,` | bottom AND right → top-left corner |
| `.` `,` | bottom AND left → top-right corner |
| `` ` `` `'` | top AND right → bottom-left corner |
| `` ` `` `'` | top AND left → bottom-right corner |

## Arrows

### Horizontal Arrows
```
Right:   ---->    or    -->    or    ->
Left:    <----    or    <--    or    <-
Both:    <--->
```

### Vertical Arrows
```
Down:    |        Up:      ^
         |                 |
         v                 |
```

### Diagonal Arrows
```
        ^                         ^
       /                           \
Down-left:  \      Down-right:  /
             v                 v
```

## Shapes

### Boxes
```
Sharp:              Rounded:
+-------+           .-------.
|       |           |       |
+-------+           '-------'

Double-line:
+========+
‖        ‖
+========+
```

### Circles
```
Small filled:    *       (connected to line)
Small open:      o       (connected to line)
Large open:      O       (connected to line)

Example:
    *----o----O
```

### Diamond
```
     /\
    /  \
   /    \
   \    /
    \  /
     \/
```

### Parallelogram
```
   .-----.
  /     /
 /     /
'-----'
```

## Text

### Regular Text
Text that doesn't match drawing characters renders as-is:
```
+-------------+
|  Hello      |
|  World      |
+-------------+
```

### Escaping Characters
Use double quotes to prevent interpretation:
```
"+" renders as literal +
"-" renders as literal -
```

## Common Diagram Patterns

### Flowchart
```
        .---.
        | A |
        '---'
          |
          v
        .---.
    +-->| B |--+
    |   '---'  |
    |     |    |
    |     v    |
    |   .---.  |
    +---| C |<-+
        '---'
```

### Sequence Diagram
```
 Client              Server
   |                    |
   |    request         |
   |------------------->|
   |                    |
   |    response        |
   |<-------------------|
   |                    |
```

### Tree Structure
```
        Root
       /    \
      /      \
   Child1   Child2
    /  \       \
   A    B       C
```

### Architecture Diagram
```
.---------.     .---------.     .---------.
|   UI    |---->|   API   |---->|   DB    |
'---------'     '---------'     '---------'
                    |
                    v
               .---------.
               |  Cache  |
               '---------'
```

### State Machine
```
          start
            |
            v
    .---------------.
    |    Idle       |<---------+
    '---------------'          |
            |                  |
            | event            | done
            v                  |
    .---------------.          |
    |   Working     |----------+
    '---------------'
            |
            | error
            v
    .---------------.
    |    Error      |
    '---------------'
```

### Network Topology
```
                  .-------.
                  | Router|
                  '---+---'
                      |
        +-------------+-------------+
        |             |             |
    .---+---.     .---+---.     .---+---.
    | PC 1  |     | PC 2  |     | PC 3  |
    '-------'     '-------'     '-------'
```

### Class Diagram
```
    .-----------------.
    |     Animal      |
    |-----------------|
    | + name: string  |
    | + age: int      |
    |-----------------|
    | + speak()       |
    '-----------------'
            ^
            |
    .-------+-------.
    |               |
.---+---.       .---+---.
|  Dog  |       |  Cat  |
'-------'       '-------'
```

### ER Diagram
```
.---------.          .----------.          .---------.
|  User   |1--------*|  Order   |*--------1| Product |
'---------'          '----------'          '---------'
```

## Tips

1. **Alignment matters** - characters must align on the grid
2. **Spacing** - use consistent spacing for clean output
3. **Connections** - lines must touch corners/endpoints
4. **Testing** - use the [online editor](https://ivanceras.github.io/svgbob-editor/) to preview

## Online Resources

- [Svgbob Editor](https://ivanceras.github.io/svgbob-editor/) - Live preview
- [GitHub Repository](https://github.com/ivanceras/svgbob) - Source and docs
