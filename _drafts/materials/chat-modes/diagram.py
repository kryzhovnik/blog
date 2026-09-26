import sys
out = sys.argv[1]
# Prompt sizes in characters, measured in Duck. Tools drawn as equal cells (Duck average ~1100 chars).
BASE = 777
INSTR = {"tutor": 3280, "manage cards": 3342, "showtime": 5645}
TOOLS = {"tutor": [1400, 900], "manage cards": [1300, 1150, 800, 750], "showtime": [900, 700, 950, 700, 1200]}
TURNS = [  # user message, routed mode, reply size (illustrative)
  ("“adjudicate”", "tutor", 1500),
  ("“make cards from Friends S2E3”", "showtime", 4000),
  ("“what does the first one mean?”", "tutor", 1500),
]
USER_W = 300                   # user messages drawn wider than their size so they stay visible
W = 880; X0 = 40; BH = 28; GAP = 14; LABEL = 22   # message label sits above its bar
total_top = BASE + sum(INSTR.values()) + sum(sum(t) for t in TOOLS.values()) + sum(USER_W + r for _, _, r in TURNS[:-1]) + USER_W
K = 800 / total_top

INK="#1f2937"; MUTED="#6b7280"; EDGE="#475569"
PROMPT="#dbeafe"; BASEC="#bfdbfe"; TOOL="#fde68a"; USERC="#94a3b8"; REPLY="#e5e7eb"; NEW="#1f2937"
FONT="ui-sans-serif, -apple-system, Helvetica, Arial, sans-serif"
p=[]
def add(s): p.append(s)
def text(x,y,s,size=14,fill=INK,anchor="start",weight="normal"):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>')
def cell(x,y,w,fill,h=BH):
    add(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" fill="{fill}" stroke="{EDGE}" stroke-width="0.8"/>')
def dashed(x,y):
    add(f'<line x1="{x:.1f}" y1="{y+3}" x2="{x:.1f}" y2="{y+BH-3}" stroke="{EDGE}" stroke-width="1" stroke-dasharray="3 3"/>')

def bar(y, modes, turn):
    x = X0
    # one system prompt: base section, then a section per mode, split by dashed lines
    sections = [("base", BASE)] + [(m, INSTR[m]) for m in modes]
    w = sum(s for _, s in sections) * K
    add(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{BH}" fill="{PROMPT}" stroke="{EDGE}" stroke-width="0.8"/>')
    add(f'<rect x="{x:.1f}" y="{y}" width="{BASE*K:.1f}" height="{BH}" fill="{BASEC}" stroke="none"/>')
    sx = x
    for i, (name, size) in enumerate(sections):
        sw = size * K
        if i > 0: dashed(sx, y)
        if name != "base" and sw > 70: text(sx + sw/2, y + BH/2 + 4, name, 12, INK, "middle")
        sx += sw
    x += w
    # tools: equal cells
    for m in modes:   # union of the modes' tools; each tool appears once
        for t in TOOLS[m]:
            cell(x, y, t*K, TOOL); x += t*K
    prefix_end = x
    # history: earlier user messages and replies, then the new message
    for msg, _, reply in TURNS[:turn]:
        cell(x, y, USER_W*K, USERC); x += USER_W*K
        cell(x, y, reply*K, REPLY); x += reply*K
    cell(x, y, USER_W*K, NEW)
    return prefix_end

rows = len(TURNS); RH = LABEL + BH + GAP
H = 150 + 2*(rows*RH + 90) + 20
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
# Embedded SVG media queries follow the embedding page's CSS color-scheme.
add('''<style>
  @media (prefers-color-scheme: dark) {
    [fill="white"] { fill: #191919; }
    [fill="#1f2937"] { fill: #e6e6e6; }
    [fill="#6b7280"] { fill: #aaa; }
    [fill="#dbeafe"] { fill: #253c55; }
    [fill="#bfdbfe"] { fill: #365d83; }
    [fill="#fde68a"] { fill: #806522; }
    [fill="#94a3b8"] { fill: #7a8ca3; }
    [fill="#e5e7eb"] { fill: #3c424a; }
    [fill="#2563eb"] { fill: #80baff; }
    [stroke="#475569"] { stroke: #8493a5; }
    [stroke="#1f2937"] { stroke: #e6e6e6; }
  }
</style>''')
add(f'<rect width="{W}" height="{H}" fill="white"/>')

def panel(top, title, subtitle, routed):
    text(40, top, title, 20, INK, "start", "bold")
    text(40, top + 22, subtitle, 14, MUTED)
    y0 = top + 46 + LABEL
    ends = []
    for i, (msg, mode, _) in enumerate(TURNS):
        y = y0 + i*RH
        text(X0, y - 8, msg, 14)
        if routed:
            text(X0 + len(msg)*6.7 + 10, y - 8, "router → " + mode, 12, "#2563eb")
            ends.append(bar(y, [mode], i))
        else:
            ends.append(bar(y, list(INSTR), i))
    ylast = y0 + (rows-1)*RH + BH
    if not routed:
        pe = ends[0]
        add(f'<line x1="{pe:.1f}" y1="{y0-LABEL-4}" x2="{pe:.1f}" y2="{ylast+8}" stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 4"/>')
        text(pe - 4, ylast + 24, "same prefix every turn", 12, MUTED, "end")
    else:
        text(X0, ylast + 24, "prefix changes with the mode", 12, MUTED)
    return ylast + 24

b = panel(40, "One configuration", "One system prompt covering every mode, and every tool, on every request", False)
b = panel(b + 50, "Chat Modes", "A router picks one mode per turn; the request carries only that mode", True)

ly = b + 36; x = 40
for c, l in [(BASEC, "base system prompt"), (PROMPT, "mode instructions"), (TOOL, "one tool"), (USERC, "earlier message"), (REPLY, "reply"), (NEW, "new message")]:
    add(f'<rect x="{x}" y="{ly}" width="16" height="16" fill="{c}" stroke="{EDGE}" stroke-width="0.8"/>'); text(x + 22, ly + 13, l, 13, MUTED); x += 22 + len(l)*7 + 26
add('</svg>')
s = "\n".join(p).replace(f'height="{H}" viewBox="0 0 {W} {H}"', f'height="{ly+30:.0f}" viewBox="0 0 {W} {ly+30:.0f}"').replace(f'<rect width="{W}" height="{H}"', f'<rect width="{W}" height="{ly+30:.0f}"')
open(out, "w").write(s)
