"""Clover Hollow sprite generator.

Hand-drawn style vector sprites: warm brown outlines (never black), soft
top-left light, gradient shading, small highlight strokes and painted texture.
Run:  python3 tools/sprites.py   -> writes assets/sprites/*.svg + manifest.json
"""
import json, math, os, random

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sprites')
os.makedirs(OUT, exist_ok=True)
INK = '#4a2f1d'          # warm outline
INK_SOFT = '#6b4a30'
SPRITES = {}

def svg(name, w, h, body, defs='', anchor=None, group='misc'):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
         f'<defs>{defs}</defs>{body}</svg>')
    SPRITES[name] = {'w': w, 'h': h, 'anchor': anchor or [w / 2, h - 6], 'group': group}
    open(os.path.join(OUT, name + '.svg'), 'w').write(s)

def lg(id, stops, x1=0, y1=0, x2=0, y2=1):
    st = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient>'

def rg(id, stops, cx=.35, cy=.3, r=.75):
    st = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}">{st}</radialGradient>'

def shade(hexc, amt):
    n = int(hexc[1:], 16); r, g, b = n >> 16, (n >> 8) & 255, n & 255
    f = lambda v: max(0, min(255, int(v + amt)))
    return '#%02x%02x%02x' % (f(r), f(g), f(b))

def shadow(cx, cy, rx, ry, op=.22):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#3a2414" opacity="{op}"/>'

# ---------------------------------------------------------------- tiles (128 x 76)
DIAMOND = 'M64 2 L126 33 L64 64 L2 33 Z'
SIDES = 'M2 33 L64 64 L126 33 L126 42 L64 73 L2 42 Z'

def tile(name, top_grad, side_col, detail='', edge=True):
    rnd = random.Random(name)
    defs = top_grad
    body = ''
    if edge:
        body += f'<path d="{SIDES}" fill="{side_col}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
        body += f'<path d="M2 42 L64 73 L126 42" fill="none" stroke="{shade(side_col,-30)}" stroke-width="1.2"/>'
    body += f'<path d="{DIAMOND}" fill="url(#g_{name})" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
    body += f'<clipPath id="c_{name}"><path d="{DIAMOND}"/></clipPath><g clip-path="url(#c_{name})">{detail}</g>'
    body += f'<path d="M6 33 L64 4 L122 33" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="2" stroke-linecap="round"/>'
    svg(name, 128, 76, body, defs, anchor=[64, 33], group='tiles')

def grass_detail(seed, base):
    r = random.Random(seed); s = ''
    for _ in range(46):
        x, y = r.uniform(8, 120), r.uniform(6, 60)
        if abs(x - 64) / 62 + abs(y - 33) / 31 > .92: continue
        h = r.uniform(3, 6); lean = r.uniform(-2, 2)
        c = shade(base, r.choice([-28, -18, 18, 30]))
        s += f'<path d="M{x:.1f} {y:.1f} q{lean/2:.1f} {-h/2:.1f} {lean:.1f} {-h:.1f}" stroke="{c}" stroke-width="1.3" stroke-linecap="round" fill="none"/>'
    for _ in range(4):
        x, y = r.uniform(25, 100), r.uniform(15, 50)
        if abs(x - 64) / 62 + abs(y - 33) / 31 > .8: continue
        col = r.choice(['#fff6d8', '#ffd9e6', '#ffe27a'])
        s += ''.join(f'<circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="1.3" fill="{col}"/>' for dx, dy in [(0, 0), (2, 1), (-1, 2)])
        s += f'<circle cx="{x+.5:.1f}" cy="{y+1:.1f}" r=".8" fill="#e8a22a"/>'
    return s

tile('tile_grass', lg('g_tile_grass', [(0, '#9ed36a'), (1, '#6fae45')], 0, 0, 1, 1), '#8a5a33', grass_detail('a', '#86c25a'))
tile('tile_grass_alt', lg('g_tile_grass_alt', [(0, '#95cc62'), (1, '#68a640')], 0, 0, 1, 1), '#8a5a33', grass_detail('b', '#7fbb54'))

def furrows(col, hl, n=7):
    s = ''
    for i in range(n):
        t = (i + .5) / n
        x1, y1 = 2 + 62 * t, 33 - 31 * t
        x2, y2 = 64 + 62 * t, 64 - 31 * t
        s += f'<path d="M{x1:.1f} {y1+2:.1f} L{x2:.1f} {y2+2:.1f}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
        s += f'<path d="M{x1:.1f} {y1-1.5:.1f} L{x2:.1f} {y2-1.5:.1f}" stroke="{hl}" stroke-width="1.6" stroke-linecap="round" opacity=".55"/>'
    r = random.Random(n)
    for _ in range(30):
        x, y = r.uniform(10, 118), r.uniform(8, 58)
        if abs(x - 64) / 62 + abs(y - 33) / 31 > .9: continue
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(.6,1.3):.1f}" fill="{hl}" opacity=".5"/>'
    return s

tile('tile_plowed', lg('g_tile_plowed', [(0, '#8f5c34'), (1, '#6a3f22')], 0, 0, 1, 1), '#5c3820', furrows('#55331b', '#b07a4a'))
tile('tile_fallow', lg('g_tile_fallow', [(0, '#b58a5a'), (1, '#93683f')], 0, 0, 1, 1), '#6e4a2a',
     furrows('#8a6038', '#d4ad7c', 6) + ''.join(
         f'<path d="M{x} {y} l3 -4 M{x+2} {y} l-1 -4" stroke="#c9a85a" stroke-width="1.2" stroke-linecap="round"/>'
         for x, y in [(30, 30), (50, 20), (70, 40), (88, 26), (60, 50), (96, 36), (40, 42)]))
tile('tile_water', lg('g_tile_water', [(0, '#8fd4ec'), (1, '#4e9ec4')], 0, 0, 1, 1), '#3f7d9c',
     ''.join(f'<path d="M{x} {y} q5 -3 10 0 t10 0" stroke="#e8fbff" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".7"/>' for x, y in [(30, 26), (60, 16), (70, 40), (40, 44), (88, 30)]))

# ---------------------------------------------------------------- crops (128 x 128, base at 64,112)
def stem_leaf(x, y, ang, ln, col, w=None):
    w = w or ln * .42
    a = math.radians(ang)
    tx, ty = x + math.cos(a) * ln, y - math.sin(a) * ln
    nx, ny = -math.sin(a) * w / 2, -math.cos(a) * w / 2
    mx, my = (x + tx) / 2, (y + ty) / 2
    d = f'M{x:.1f} {y:.1f} Q{mx+nx:.1f} {my+ny:.1f} {tx:.1f} {ty:.1f} Q{mx-nx:.1f} {my-ny:.1f} {x:.1f} {y:.1f}Z'
    vein = f'M{x:.1f} {y:.1f} Q{mx+nx*.2:.1f} {my+ny*.2:.1f} {tx:.1f} {ty:.1f}'
    return (f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="{vein}" stroke="{shade(col,-35)}" stroke-width="1" fill="none" opacity=".8"/>'
            f'<path d="{d}" fill="#fff" opacity=".12" transform="translate({-nx*.15:.1f} {-ny*.15:.1f}) scale(1)"/>')

def mound():
    return (shadow(64, 113, 30, 7) +
            '<path d="M38 112 Q64 98 90 112 Q64 118 38 112Z" fill="#6a3f22" stroke="#4a2f1d" stroke-width="1.4"/>'
            '<path d="M46 109 Q64 102 82 109" stroke="#9a6a40" stroke-width="1.5" fill="none" stroke-linecap="round"/>')

def crop(name, leaf, stage, fruit_fn=None, tall=False):
    defs = ''
    b = mound()
    L, Ld = leaf, shade(leaf, -25)
    if stage == 'seed':
        for x in (54, 64, 74):
            b += f'<ellipse cx="{x}" cy="{108 + (x==64)*-2}" rx="3" ry="2" fill="#e2c38a" stroke="{INK}" stroke-width="1"/>'
    elif stage == 'sprout':
        b += f'<path d="M64 110 Q63 100 64 94" stroke="{Ld}" stroke-width="3" fill="none" stroke-linecap="round"/>'
        b += stem_leaf(64, 96, 150, 16, L) + stem_leaf(64, 95, 30, 16, L)
    elif stage == 'young':
        top = 70 if tall else 80
        b += f'<path d="M64 110 Q62 92 64 {top}" stroke="{Ld}" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
        for y, a, l in [(100, 160, 24), (98, 20, 24), (88, 150, 21), (86, 35, 21), (top + 4, 110, 16), (top + 4, 70, 16)]:
            b += stem_leaf(64, y, a, l, L if a < 90 else shade(L, -10))
    else:  # ripe / withered
        wither = stage == 'withered'
        L2 = '#b39255' if wither else L
        Ld2 = '#8a6a3a' if wither else Ld
        top = 46 if tall else 58
        bend = 14 if wither else 0
        b += f'<path d="M64 110 Q60 {top+30} {64+bend} {top+bend*.6}" stroke="{Ld2}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        leaves = [(102, 165, 30), (100, 15, 30), (88, 150, 27), (86, 30, 27), (74, 140, 22), (72, 45, 22)]
        if tall: leaves += [(60, 130, 20), (58, 55, 20)]
        for y, a, l in leaves:
            if wither: a = a - 40 if a > 90 else a - 35
            b += stem_leaf(64, y, a, l, L2 if a % 2 == 0 else shade(L2, -12))
        if fruit_fn and not wither:
            fd, fb = fruit_fn()
            defs += fd; b += fb
        if wither:
            b += '<path d="M50 96 l-6 4 M78 92 l7 5" stroke="#7a5a2a" stroke-width="1.6" stroke-linecap="round"/>'
    svg(f'{name}_{stage}', 128, 128, b, defs, anchor=[64, 112], group='crops')

def berries(id, col, pts, r=6.5):
    d = rg(f'f_{id}', [(0, shade(col, 70)), (.55, col), (1, shade(col, -45))])
    s = ''
    for x, y in pts:
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#f_{id})" stroke="{INK}" stroke-width="1.4"/>'
        s += f'<ellipse cx="{x-2}" cy="{y-2.5}" rx="2" ry="1.3" fill="#fff" opacity=".75"/>'
    return d, s

def sunpea():  # golden pods
    d = rg('f_sp', [(0, '#fff3a6'), (.5, '#f6c51b'), (1, '#c98a06')])
    s = ''
    for x, y, a in [(46, 88, -25), (82, 84, 25), (60, 66, -10), (74, 70, 15)]:
        s += (f'<g transform="rotate({a} {x} {y})"><path d="M{x-5} {y-12} Q{x} {y-16} {x+5} {y-12} Q{x+8} {y} {x} {y+12} Q{x-8} {y} {x-5} {y-12}Z" '
              f'fill="url(#f_sp)" stroke="{INK}" stroke-width="1.4"/>'
              + ''.join(f'<circle cx="{x}" cy="{y+dy}" r="2.4" fill="#ffe680" opacity=".9"/>' for dy in (-6, 0, 6)) + '</g>')
    return d, s

def glowroot():  # orange root peeking out with glow
    d = rg('f_gr', [(0, '#ffd2a1'), (.5, '#ff8a3d'), (1, '#c8521a')]) + rg('f_glow', [(0, '#ffcf7a'), (1, 'rgba(255,207,122,0)')], .5, .5, .5)
    s = (f'<ellipse cx="64" cy="104" rx="26" ry="14" fill="url(#f_glow)" opacity=".9"/>'
         f'<path d="M48 106 Q50 94 64 92 Q78 94 80 106 Q72 116 64 117 Q56 116 48 106Z" fill="url(#f_gr)" stroke="{INK}" stroke-width="1.5"/>'
         f'<path d="M54 102 q4 -2 8 0 M62 108 q4 -2 8 0" stroke="#c8521a" stroke-width="1.2" fill="none"/>'
         f'<ellipse cx="57" cy="98" rx="4" ry="2" fill="#fff" opacity=".6"/>')
    return d, s

def melon():
    d = rg('f_mel', [(0, '#ffd1dc'), (.55, '#e45b78'), (1, '#9e2c47')])
    s = (f'<ellipse cx="64" cy="100" rx="24" ry="15" fill="url(#f_mel)" stroke="{INK}" stroke-width="1.6"/>'
         + ''.join(f'<path d="M{x} 87 Q{x+(x-64)*.25} 100 {x} 113" stroke="#9e2c47" stroke-width="1.4" fill="none" opacity=".7"/>' for x in (50, 58, 66, 74))
         + '<ellipse cx="54" cy="93" rx="7" ry="3" fill="#fff" opacity=".55"/><path d="M64 86 q2 -6 6 -7" stroke="#4f7a2a" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    return d, s

def puffcorn():
    d = lg('f_pc', [(0, '#fff6cf'), (1, '#f0cc5a')], 0, 0, 1, 0)
    s = ''
    for x, y, a in [(76, 56, 12), (52, 64, -14)]:
        s += (f'<g transform="rotate({a} {x} {y})"><path d="M{x-7} {y+16} Q{x-9} {y-6} {x} {y-18} Q{x+9} {y-6} {x+7} {y+16}Z" fill="url(#f_pc)" stroke="{INK}" stroke-width="1.5"/>'
              + ''.join(f'<circle cx="{x+dx}" cy="{y+dy}" r="2.3" fill="#fffbe8" stroke="#d9b24a" stroke-width=".6"/>' for dx in (-3, 3) for dy in (-8, -2, 4, 10))
              + f'<path d="M{x-8} {y+16} Q{x-14} {y} {x-6} {y-8} M{x+8} {y+16} Q{x+14} {y} {x+6} {y-8}" stroke="#7ab04a" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
    return d, s

def frostmint():
    d = rg('f_fm', [(0, '#ffffff'), (.6, '#9fe6ee'), (1, '#4fb6c4')])
    s = ''
    for x, y, r in [(50, 74, 7), (78, 70, 8), (64, 58, 7), (66, 84, 6)]:
        pts = ' '.join(f'{x+math.cos(math.radians(a))*(r if i%2==0 else r*.45):.1f},{y+math.sin(math.radians(a))*(r if i%2==0 else r*.45):.1f}' for i, a in enumerate(range(-90, 270, 45)))
        s += f'<polygon points="{pts}" fill="url(#f_fm)" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'
    return d, s

CROPS = {
    'sunpea': ('#5fa83a', sunpea, False),
    'bramblebean': ('#3f8a3a', lambda: berries('bb', '#7b3fa0', [(46, 86), (80, 82), (56, 70), (72, 66), (64, 80)]), False),
    'glowroot': ('#5aa83a', glowroot, False),
    'puffcorn': ('#6aa53a', puffcorn, True),
    'velvet': ('#3f8a3a', melon, False),
    'frostmint': ('#2f8f74', frostmint, False),
    'emberpepper': ('#4a8a2a', lambda: berries('ep', '#d8322a', [(48, 84), (80, 80), (62, 66), (70, 86)], 7), False),
    'cloudberry': ('#4f9a5f', lambda: berries('cb', '#efe9ff', [(46, 84), (82, 82), (58, 66), (72, 68), (64, 82), (54, 78)], 6), False),
}
for n, (leaf, fn, tall) in CROPS.items():
    for st in ('seed', 'sprout', 'young', 'ripe', 'withered'):
        crop(n, leaf, st, fn, tall)

# ---------------------------------------------------------------- trees (160 x 200)
def tree(name, leaf, fruit, ready):
    defs = (rg(f'cn_{name}', [(0, shade(leaf, 45)), (.6, leaf), (1, shade(leaf, -40))], .38, .3, .8)
            + lg(f'tr_{name}', [(0, '#9a6236'), (1, '#6b3f20')], 0, 0, 1, 0))
    b = shadow(80, 186, 46, 11)
    b += (f'<path d="M70 188 Q72 150 74 120 L86 120 Q88 150 92 188 Q81 192 70 188Z" fill="url(#tr_{name})" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M78 130 Q80 160 78 184" stroke="#4a2f1d" stroke-width="1.2" fill="none" opacity=".5"/>'
          f'<path d="M76 132 Q62 120 56 108 M84 128 Q98 118 104 104" stroke="#6b3f20" stroke-width="5" fill="none" stroke-linecap="round"/>')
    blobs = [(80, 70, 50), (46, 96, 30), (114, 92, 32), (60, 52, 30), (102, 54, 30), (80, 104, 34)]
    for x, y, r in blobs:
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#cn_{name})" stroke="{INK}" stroke-width="1.8"/>'
    for x, y, r in blobs:  # inner repaint to hide inner outlines
        b += f'<circle cx="{x}" cy="{y}" r="{r-1.8}" fill="url(#cn_{name})"/>'
    r = random.Random(name)
    for _ in range(26):  # leaf texture
        x, y = r.uniform(30, 130), r.uniform(28, 128)
        if math.hypot(x - 80, y - 78) > 54: continue
        s = r.uniform(3, 6)
        b += f'<path d="M{x:.0f} {y:.0f} q{s/2:.1f} {-s:.1f} {s:.1f} 0" stroke="{shade(leaf,-38)}" stroke-width="1.4" fill="none" stroke-linecap="round" opacity=".7"/>'
    b += f'<path d="M48 70 Q60 40 92 34" stroke="#fff" stroke-width="5" stroke-linecap="round" fill="none" opacity=".18"/>'
    if ready:
        defs += rg(f'fr_{name}', [(0, shade(fruit, 80)), (.55, fruit), (1, shade(fruit, -50))])
        for x, y in [(50, 90), (70, 60), (98, 70), (112, 96), (84, 96), (60, 112), (94, 46), (40, 104), (104, 116), (74, 80)]:
            b += (f'<circle cx="{x}" cy="{y}" r="7.5" fill="url(#fr_{name})" stroke="{INK}" stroke-width="1.4"/>'
                  f'<ellipse cx="{x-2.5}" cy="{y-3}" rx="2.4" ry="1.5" fill="#fff" opacity=".75"/>'
                  f'<path d="M{x} {y-7} q2 -4 5 -4" stroke="#3f6a20" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    svg(f'{name}_{"ready" if ready else "growing"}', 160, 200, b, defs, anchor=[80, 186], group='trees')

for n, leaf, fruit in [('tree_blushapple', '#5aa83a', '#e2404f'), ('tree_sugarplum', '#4f9a3a', '#7a3e9d'),
                       ('tree_starpeach', '#62b04a', '#ffa56b'), ('tree_mooncitrus', '#4a9a40', '#ffd23a')]:
    tree(n, leaf, fruit, False); tree(n, leaf, fruit, True)

# ---------------------------------------------------------------- animals (128 x 112)
def bubble(prod):
    return (f'<g><path d="M86 6 h30 a7 7 0 0 1 7 7 v16 a7 7 0 0 1 -7 7 h-8 l-6 7 l-2 -7 h-14 a7 7 0 0 1 -7 -7 v-16 a7 7 0 0 1 7 -7z" '
            f'fill="#fffaf0" stroke="{INK}" stroke-width="1.6"/><g transform="translate(101 21)">{prod}</g></g>')

PROD = {
    'egg': f'<ellipse rx="6" ry="7.5" fill="#fff4dc" stroke="{INK}" stroke-width="1.2"/><ellipse cx="-2" cy="-3" rx="1.8" ry="1.2" fill="#fff"/>',
    'milk': f'<path d="M-5 -9 h10 v3 l3 3 v12 h-16 v-12 l3 -3z" fill="#fff" stroke="{INK}" stroke-width="1.2"/><rect x="-8" y="-1" width="16" height="5" fill="#7fb3e8"/>',
    'wool': ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="{INK}" stroke-width="1"/>' for x, y in [(-4, 1), (4, -1), (0, 4)]),
    'truffle': f'<circle r="7" fill="#5a3a22" stroke="{INK}" stroke-width="1.2"/><circle cx="-2" cy="-2" r="2" fill="#8a6040"/>',
}

def animal(name, body, prod):
    for ready in (False, True):
        b = body + (bubble(PROD[prod]) if ready else '')
        svg(f'{name}_{"ready" if ready else "idle"}', 128, 112, b, '', anchor=[64, 102], group='animals')

cow = (shadow(64, 102, 40, 8) +
       ''.join(f'<path d="M{x} 78 L{x+1} 100" stroke="#5a463a" stroke-width="7" stroke-linecap="round"/><path d="M{x-3} 99 h8" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>' for x in (36, 48, 76, 88))
       + f'<ellipse cx="62" cy="68" rx="36" ry="21" fill="#fbf6ee" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M40 56 q10 -8 18 2 q-4 12 -16 9z M66 72 q12 -6 20 3 q-6 9 -18 5z M78 52 q8 -4 12 4 q-6 4 -12 0z" fill="#5a4234"/>'
       f'<ellipse cx="68" cy="88" rx="8" ry="5" fill="#f4b8bf" stroke="{INK}" stroke-width="1.4"/>'
       f'<path d="M26 64 q-8 6 -6 18" stroke="{INK}" stroke-width="2" fill="none"/><circle cx="20" cy="83" r="3" fill="#5a4234"/>'
       f'<ellipse cx="100" cy="56" rx="14" ry="13" fill="#fbf6ee" stroke="{INK}" stroke-width="2"/>'
       f'<ellipse cx="106" cy="64" rx="10" ry="7" fill="#f4b8bf" stroke="{INK}" stroke-width="1.6"/>'
       f'<circle cx="103" cy="64" r="1.4" fill="{INK}"/><circle cx="110" cy="64" r="1.4" fill="{INK}"/>'
       f'<path d="M90 44 q-6 -8 -2 -12 M108 44 q6 -8 2 -12" stroke="#e8c98a" stroke-width="4" fill="none" stroke-linecap="round"/>'
       f'<ellipse cx="86" cy="52" rx="6" ry="3.5" fill="#f2c6b8" stroke="{INK}" stroke-width="1.2" transform="rotate(-25 86 52)"/>'
       f'<circle cx="97" cy="53" r="2.6" fill="{INK}"/><circle cx="96.2" cy="52" r=".9" fill="#fff"/>'
       f'<path d="M36 52 Q60 44 86 50" stroke="#fff" stroke-width="3" fill="none" opacity=".6" stroke-linecap="round"/>')
hen = (shadow(60, 100, 28, 6) +
       f'<path d="M52 88 L50 100 M66 88 L68 100" stroke="#e8a33a" stroke-width="3" stroke-linecap="round"/>'
       f'<path d="M50 100 l-5 1 M50 100 l3 2 M68 100 l5 1 M68 100 l-3 2" stroke="#e8a33a" stroke-width="2" stroke-linecap="round"/>'
       f'<path d="M30 64 Q28 46 42 50 Q34 58 38 66Z" fill="#c9b8a0" stroke="{INK}" stroke-width="1.6"/>'
       f'<ellipse cx="58" cy="72" rx="26" ry="20" fill="#f3ead9" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M44 70 q12 10 26 2" stroke="#c9b8a0" stroke-width="2" fill="none"/>'
       + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#a8835c"/>' for x, y in [(48, 64), (56, 80), (64, 70), (44, 76), (60, 60), (70, 78)])
       + f'<circle cx="80" cy="50" r="13" fill="#f3ead9" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M72 38 q3 -7 6 -1 q3 -7 6 -1 q3 -5 5 1 q-8 4 -17 1z" fill="#d8423a" stroke="{INK}" stroke-width="1.4"/>'
       f'<path d="M92 50 l9 3 l-9 4z" fill="#f2b33a" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"/>'
       f'<path d="M88 58 q3 6 -1 9 q-4 -3 -2 -9z" fill="#d8423a" stroke="{INK}" stroke-width="1.2"/>'
       f'<circle cx="84" cy="48" r="2.3" fill="{INK}"/><circle cx="83.3" cy="47.2" r=".8" fill="#fff"/>'
       f'<ellipse cx="76" cy="56" rx="3" ry="1.8" fill="#f4a0a8" opacity=".7"/>')
sheep = (shadow(62, 102, 36, 7) +
         ''.join(f'<path d="M{x} 80 L{x} 100" stroke="#3a3330" stroke-width="6" stroke-linecap="round"/>' for x in (40, 52, 72, 84))
         + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fdfaf4" stroke="{INK}" stroke-width="1.8"/>' for x, y, r in [(36, 66, 14), (48, 54, 15), (64, 50, 15), (80, 56, 14), (88, 70, 13), (70, 78, 14), (50, 78, 14), (62, 66, 16)])
         + ''.join(f'<circle cx="{x}" cy="{y}" r="{r-2}" fill="#fdfaf4"/>' for x, y, r in [(36, 66, 14), (48, 54, 15), (64, 50, 15), (80, 56, 14), (88, 70, 13), (70, 78, 14), (50, 78, 14), (62, 66, 16)])
         + ''.join(f'<path d="M{x} {y} q3 -3 6 0" stroke="#d9cfbd" stroke-width="1.4" fill="none"/>' for x, y in [(40, 62), (56, 50), (70, 60), (52, 74), (78, 72), (62, 66)])
         + f'<ellipse cx="102" cy="62" rx="11" ry="14" fill="#3a3330" stroke="{INK}" stroke-width="1.8"/>'
         f'<ellipse cx="92" cy="54" rx="7" ry="3.5" fill="#3a3330" stroke="{INK}" stroke-width="1.4" transform="rotate(-30 92 54)"/>'
         f'<circle cx="104" cy="58" r="2.4" fill="#fff"/><circle cx="104.6" cy="58.4" r="1.2" fill="{INK}"/>'
         f'<path d="M96 46 q6 -6 12 -2" stroke="#fdfaf4" stroke-width="5" fill="none" stroke-linecap="round"/>')
pig = (shadow(62, 102, 36, 7) +
       ''.join(f'<path d="M{x} 82 L{x} 100" stroke="#e58f9b" stroke-width="7" stroke-linecap="round"/>' for x in (40, 52, 74, 86))
       + f'<ellipse cx="62" cy="72" rx="36" ry="22" fill="#f7b9c2" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M34 64 Q60 52 90 62" stroke="#fff" stroke-width="3.5" fill="none" opacity=".45" stroke-linecap="round"/>'
       f'<path d="M26 66 q-8 -4 -6 4 q2 6 -4 6" stroke="{INK}" stroke-width="1.8" fill="none"/>'
       f'<ellipse cx="96" cy="66" rx="14" ry="13" fill="#f7b9c2" stroke="{INK}" stroke-width="2"/>'
       f'<path d="M86 52 l2 -10 l8 8z M100 50 l6 -9 l3 11z" fill="#f09aa8" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
       f'<ellipse cx="106" cy="70" rx="8" ry="6.5" fill="#f09aa8" stroke="{INK}" stroke-width="1.6"/>'
       f'<ellipse cx="103.5" cy="70" rx="1.4" ry="2" fill="#8a3a48"/><ellipse cx="108.5" cy="70" rx="1.4" ry="2" fill="#8a3a48"/>'
       f'<circle cx="96" cy="61" r="2.3" fill="{INK}"/><circle cx="95.3" cy="60.3" r=".8" fill="#fff"/>'
       f'<ellipse cx="90" cy="72" rx="3.5" ry="2" fill="#f07e93" opacity=".6"/>')
animal('animal_cow', cow, 'milk'); animal('animal_hen', hen, 'egg'); animal('animal_sheep', sheep, 'wool'); animal('animal_pig', pig, 'truffle')

# ---------------------------------------------------------------- farmer (96 x 150), 2 walk frames + work frame
def farmer(name, frame):
    lift = {'walk1': (0, -4), 'walk2': (-4, 0), 'idle': (0, 0), 'work': (0, 0)}[frame]
    tool_rot = {'work': -40}.get(frame, 10)
    b = shadow(48, 142, 22, 5)
    for i, (x, dy) in enumerate([(38, lift[0]), (54, lift[1])]):
        b += (f'<path d="M{x} 104 L{x} {134+dy}" stroke="#3f6ea8" stroke-width="12" stroke-linecap="round"/>'
              f'<path d="M{x-6} {137+dy} q6 -6 14 0 q0 5 -7 5 q-7 0 -7 -5z" fill="#5a3a22" stroke="{INK}" stroke-width="1.5"/>')
    b += (f'<path d="M28 66 Q48 58 68 66 L70 108 Q48 114 26 108Z" fill="#d8423a" stroke="{INK}" stroke-width="2"/>'
          + ''.join(f'<path d="M{x} 64 L{x} 110" stroke="#b02f28" stroke-width="1.2" opacity=".6"/>' for x in (36, 48, 60))
          + ''.join(f'<path d="M27 {y} L69 {y}" stroke="#b02f28" stroke-width="1.2" opacity=".6"/>' for y in (76, 88, 100))
          + f'<path d="M32 82 L64 82 L66 108 Q48 114 30 108Z" fill="#4f7fc4" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M34 82 L32 64 M62 82 L64 64" stroke="#4f7fc4" stroke-width="5"/>'
          f'<circle cx="35" cy="85" r="2" fill="#f3c623" stroke="{INK}" stroke-width=".8"/><circle cx="61" cy="85" r="2" fill="#f3c623" stroke="{INK}" stroke-width=".8"/>'
          f'<rect x="42" y="90" width="12" height="8" rx="2" fill="#3f6ea8" stroke="{INK}" stroke-width="1.2"/>')
    b += (f'<path d="M28 70 Q18 84 22 96" stroke="#d8423a" stroke-width="10" fill="none" stroke-linecap="round"/>'
          f'<circle cx="22" cy="98" r="5" fill="#f2c39b" stroke="{INK}" stroke-width="1.5"/>')
    b += (f'<circle cx="48" cy="44" r="17" fill="#f2c39b" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M33 40 Q34 28 48 27 Q62 28 63 40 Q58 34 48 35 Q38 34 33 40Z" fill="#8a5a33"/>'
          f'<circle cx="42" cy="46" r="2.4" fill="{INK}"/><circle cx="54" cy="46" r="2.4" fill="{INK}"/>'
          f'<circle cx="41.3" cy="45.2" r=".8" fill="#fff"/><circle cx="53.3" cy="45.2" r=".8" fill="#fff"/>'
          f'<path d="M43 53 q5 4 10 0" stroke="#a5583a" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
          f'<ellipse cx="37" cy="51" rx="3.5" ry="2" fill="#f0908a" opacity=".55"/><ellipse cx="59" cy="51" rx="3.5" ry="2" fill="#f0908a" opacity=".55"/>')
    b += (f'<ellipse cx="48" cy="30" rx="30" ry="7" fill="#f0cf6a" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M33 30 Q33 12 48 11 Q63 12 63 30Z" fill="#f4d97e" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M33.5 26 L62.5 26" stroke="#c4452f" stroke-width="4"/>'
          f'<path d="M24 31 Q48 37 72 31" stroke="#c9a040" stroke-width="1.2" fill="none"/>'
          + ''.join(f'<path d="M{x} {y} l3 1" stroke="#c9a040" stroke-width="1"/>' for x, y in [(40, 18), (50, 16), (56, 20), (44, 22)]))
    b += (f'<g transform="rotate({tool_rot} 70 92)"><path d="M70 92 L84 52" stroke="#8a5a2b" stroke-width="4.5" stroke-linecap="round"/>'
          f'<path d="M80 50 q8 -10 16 -4 q-4 4 -10 8z" fill="#aab3bd" stroke="{INK}" stroke-width="1.5"/></g>'
          f'<path d="M68 70 Q78 82 72 92" stroke="#d8423a" stroke-width="10" fill="none" stroke-linecap="round"/>'
          f'<circle cx="71" cy="93" r="5" fill="#f2c39b" stroke="{INK}" stroke-width="1.5"/>')
    svg(f'{name}_{frame}', 96, 150, b, '', anchor=[48, 142], group='farmer')

for fr in ('idle', 'walk1', 'walk2', 'work'):
    farmer('farmer', fr)

# ---------------------------------------------------------------- buildings & decor
def barn():
    defs = (lg('bw', [(0, '#d9604a'), (1, '#a8382a')], 0, 0, 1, 0) + lg('bs', [(0, '#9e3326'), (1, '#7a2618')], 0, 0, 1, 0)
            + lg('br', [(0, '#7a7f88'), (1, '#50545c')], 0, 0, 1, 1))
    b = shadow(112, 198, 94, 16)
    # left (side) wall and right (gable) wall
    b += f'<path d="M30 124 L110 164 L110 202 L30 162Z" fill="url(#bs)" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    b += ''.join(f'<path d="M{30+i*10} {124+i*5} L{30+i*10} {162+i*5}" stroke="#6a2014" stroke-width="1.2" opacity=".55"/>' for i in range(1, 8))
    b += f'<path d="M110 202 L190 162 L190 124 L150 100 L110 164Z" fill="url(#bw)" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    b += ''.join(f'<path d="M{110+i*10} {202-i*5} L{110+i*10} {max(164-i*5 if i<=4 else 124+(8-i)*0, 0)}" stroke="#8a2a1c" stroke-width="1.1" opacity=".45"/>' for i in range(1, 8))
    # white trim along the gable
    b += f'<path d="M108 166 L150 102 L192 126" fill="none" stroke="#fff6e8" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'
    b += f'<path d="M108 166 L150 102 L192 126" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
    # hayloft window
    b += f'<path d="M142 132 L158 124 L158 108 L142 116Z" fill="#3a1e12" stroke="#fff6e8" stroke-width="3"/>'
    # big door with X brace
    b += f'<path d="M128 194 L172 172 L172 140 L128 162Z" fill="#7a2618" stroke="#fff6e8" stroke-width="4" stroke-linejoin="round"/>'
    b += f'<path d="M128 194 L172 140 M128 162 L172 172 M150 183 L150 151" stroke="#fff6e8" stroke-width="3"/>'
    # roof slope over the side wall
    b += f'<path d="M24 127 L108 169 L150 98 L66 56Z" fill="url(#br)" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    b += ''.join(f'<path d="M{24+42*t:.1f} {127-71*t:.1f} L{108+42*t:.1f} {169-71*t:.1f}" stroke="#8d929b" stroke-width="1.3" opacity=".8"/>' for t in (.25, .5, .75))
    b += f'<path d="M66 56 L150 98" stroke="#3e4148" stroke-width="4" stroke-linecap="round"/>'
    b += f'<path d="M34 120 L64 66" stroke="#fff" stroke-width="3" opacity=".22" stroke-linecap="round"/>'
    # weathervane
    b += f'<path d="M108 78 L108 62" stroke="{INK}" stroke-width="2"/><path d="M100 64 L116 64 L112 60 M104 64 l-3 4" stroke="{INK}" stroke-width="1.8" fill="none"/>'
    svg('building_barn', 220, 214, b, defs, anchor=[110, 192], group='buildings')

def hay():
    b = shadow(48, 70, 34, 7)
    defs = lg('hy', [(0, '#f6d77a'), (1, '#d9a83a')])
    b += (f'<path d="M14 40 L48 24 L82 40 L82 60 L48 76 L14 60Z" fill="url(#hy)" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
          f'<path d="M14 40 L48 56 L82 40 M48 56 L48 76" stroke="{INK}" stroke-width="1.6" fill="none"/>'
          f'<path d="M14 40 L48 24 L82 40 L48 56Z" fill="#f9e39a"/>'
          f'<path d="M24 45 L24 64 M70 45 L70 64" stroke="#b33b2a" stroke-width="3"/>'
          f'<path d="M24 35 L58 51 M38 28 L72 44" stroke="#b33b2a" stroke-width="3"/>'
          + ''.join(f'<path d="M{x} {y} l{d} 2" stroke="#b8862a" stroke-width="1.2" stroke-linecap="round"/>' for x, y, d in [(30, 52, 3), (40, 60, -3), (56, 64, 3), (64, 52, -3), (36, 36, 4), (54, 34, -4), (60, 44, 4)]))
    svg('decor_haybale', 96, 80, b, defs, anchor=[48, 66], group='decor')

def fence():
    b = ''
    for i, x in enumerate((12, 36, 60, 84)):
        y = 60 - i * 12
        b += (f'<path d="M{x-5} {y+18} L{x-5} {y-8} L{x} {y-14} L{x+5} {y-8} L{x+5} {y+18}Z" fill="#fffaf0" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
              f'<path d="M{x+2} {y-8} L{x+2} {y+16}" stroke="#d9cbb0" stroke-width="2"/>')
    b += (f'<path d="M6 62 L90 20 L90 26 L6 68Z" fill="#fffaf0" stroke="{INK}" stroke-width="1.5"/>'
          f'<path d="M6 74 L90 32 L90 38 L6 80Z" fill="#fffaf0" stroke="{INK}" stroke-width="1.5"/>')
    svg('decor_fence', 96, 92, b, '', anchor=[48, 64], group='decor')

def scarecrow():
    b = shadow(48, 136, 22, 5)
    b += (f'<path d="M48 136 L48 40" stroke="#7a4b26" stroke-width="5" stroke-linecap="round"/>'
          f'<path d="M14 66 L82 66" stroke="#7a4b26" stroke-width="4.5" stroke-linecap="round"/>'
          f'<path d="M30 60 L66 60 L70 104 L26 104Z" fill="#4f7fc4" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
          f'<path d="M36 72 h8 v8 h-8z" fill="#d8423a" stroke="{INK}" stroke-width="1.2"/>'
          f'<path d="M26 104 l4 8 l4 -8 l4 8 l4 -8 l4 8 l4 -8 l4 8 l4 -8 l4 8 l4 -8" stroke="#e8c35a" stroke-width="2.4" fill="none" stroke-linejoin="round"/>'
          f'<path d="M12 62 l-6 6 M12 68 l-6 2 M84 62 l6 6 M84 68 l6 2" stroke="#e8c35a" stroke-width="2.4" stroke-linecap="round"/>'
          f'<circle cx="48" cy="44" r="14" fill="#f2dc9a" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M42 42 l4 4 M46 42 l-4 4 M52 42 l4 4 M56 42 l-4 4" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>'
          f'<path d="M40 52 q8 5 16 0" stroke="{INK}" stroke-width="1.6" fill="none"/>'
          f'<ellipse cx="48" cy="32" rx="24" ry="5" fill="#8a5a33" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M36 32 Q36 14 48 12 Q60 14 60 32Z" fill="#9a6a3a" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M38 26 L58 26" stroke="#d8423a" stroke-width="3"/>'
          f'<path d="M62 20 q8 -4 10 4" stroke="#5aa83a" stroke-width="2" fill="none"/><circle cx="73" cy="25" r="3" fill="#f45b8f"/>')
    svg('decor_scarecrow', 96, 144, b, '', anchor=[48, 136], group='decor')

def flowers():
    b = shadow(48, 66, 34, 7)
    b += f'<ellipse cx="48" cy="58" rx="34" ry="12" fill="#6fae45" stroke="{INK}" stroke-width="1.6"/>'
    r = random.Random(7)
    for _ in range(12):
        x, y = r.uniform(22, 74), r.uniform(46, 62)
        col = r.choice(['#f45b8f', '#ffd23f', '#8a6cf0', '#ff8a3d', '#ffffff'])
        b += f'<path d="M{x:.1f} {y+6:.1f} L{x:.1f} {y:.1f}" stroke="#3f8a2f" stroke-width="1.6"/>'
        b += ''.join(f'<circle cx="{x+math.cos(a)*3.2:.1f}" cy="{y+math.sin(a)*3.2-2:.1f}" r="2.6" fill="{col}" stroke="{INK}" stroke-width=".7"/>' for a in [i * 2 * math.pi / 5 for i in range(5)])
        b += f'<circle cx="{x:.1f}" cy="{y-2:.1f}" r="1.8" fill="#f3b80a"/>'
    svg('decor_flowers', 96, 80, b, '', anchor=[48, 60], group='decor')

def well():
    defs = lg('ws', [(0, '#c9c2b6'), (1, '#8f877a')], 0, 0, 1, 0)
    b = shadow(56, 118, 38, 9)
    b += (f'<ellipse cx="56" cy="108" rx="32" ry="12" fill="url(#ws)" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M24 82 L24 108 A32 12 0 0 0 88 108 L88 82Z" fill="url(#ws)" stroke="{INK}" stroke-width="1.8"/>'
          + ''.join(f'<path d="M{x} {y} h12" stroke="#7d756a" stroke-width="1.4"/>' for x, y in [(28, 92), (46, 98), (66, 94), (34, 104), (58, 106)])
          + f'<ellipse cx="56" cy="82" rx="32" ry="12" fill="#bdb5a8" stroke="{INK}" stroke-width="1.8"/>'
          f'<ellipse cx="56" cy="82" rx="24" ry="8" fill="#2f4f66"/>'
          f'<path d="M28 82 L28 30 M84 82 L84 30" stroke="#7a4b26" stroke-width="5" stroke-linecap="round"/>'
          f'<path d="M16 36 L56 14 L96 36" fill="#b8412c" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
          f'<path d="M16 36 L56 14 L96 36 L90 40 L56 22 L22 40Z" fill="#c4452f" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M28 50 L84 50" stroke="#6b3f20" stroke-width="4"/><path d="M56 50 L56 70" stroke="#a58b6b" stroke-width="1.5"/>'
          f'<path d="M50 70 h12 l-2 9 h-8z" fill="#8a5a33" stroke="{INK}" stroke-width="1.4"/>')
    svg('decor_well', 112, 128, b, defs, anchor=[56, 116], group='decor')

barn(); hay(); fence(); scarecrow(); flowers(); well()

# ---------------------------------------------------------------- icons (64 x 64)
def icon(name, body, defs=''):
    svg(name, 64, 64, body, defs, anchor=[32, 32], group='icons')

icon('icon_coin', f'<circle cx="32" cy="32" r="24" fill="url(#ic)" stroke="{INK}" stroke-width="2.4"/><circle cx="32" cy="32" r="17" fill="none" stroke="#c98a06" stroke-width="2"/>'
     f'<path d="M30 20 q-8 4 -6 12 q2 8 10 12 M34 20 q8 4 6 12 q-2 8 -10 12" stroke="#a87404" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
     f'<ellipse cx="24" cy="22" rx="6" ry="3" fill="#fff" opacity=".7" transform="rotate(-30 24 22)"/>',
     rg('ic', [(0, '#fff3a6'), (.55, '#f6c51b'), (1, '#c98a06')]))
icon('icon_xp', f'<path d="M32 6 L39 24 L58 24 L43 36 L49 56 L32 44 L15 56 L21 36 L6 24 L25 24Z" fill="url(#ix)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
     f'<path d="M26 22 L32 10" stroke="#fff" stroke-width="2.4" opacity=".7" stroke-linecap="round"/>',
     rg('ix', [(0, '#d6f0ff'), (.6, '#5aa9e6'), (1, '#2f6f9f')]))
icon('icon_hoe', f'<path d="M14 54 L44 14" stroke="#8a5a2b" stroke-width="6" stroke-linecap="round"/><path d="M38 12 Q52 4 58 16 Q50 16 44 24Z" fill="#aab3bd" stroke="{INK}" stroke-width="2"/>')
icon('icon_seedbag', f'<path d="M18 22 Q32 14 46 22 L50 54 Q32 60 14 54Z" fill="#e8d0a0" stroke="{INK}" stroke-width="2.2"/><path d="M20 22 Q32 28 44 22" stroke="#b8862a" stroke-width="2" fill="none"/>'
     f'<path d="M24 14 Q32 8 40 14 L38 20 Q32 18 26 20Z" fill="#c9a86a" stroke="{INK}" stroke-width="1.8"/><path d="M32 46 Q26 38 32 32 Q38 38 32 46Z" fill="#5fa83a" stroke="{INK}" stroke-width="1.4"/>')
icon('icon_gift', f'<rect x="10" y="26" width="44" height="30" rx="3" fill="#5aa9e6" stroke="{INK}" stroke-width="2.2"/><rect x="7" y="18" width="50" height="11" rx="3" fill="#7fbdf0" stroke="{INK}" stroke-width="2.2"/>'
     f'<rect x="28" y="18" width="8" height="38" fill="#f3c623" stroke="{INK}" stroke-width="1.6"/><path d="M32 18 Q18 4 18 14 Q20 20 32 18 Q46 4 46 14 Q44 20 32 18" fill="#f3c623" stroke="{INK}" stroke-width="1.8"/>')
icon('icon_ribbon', f'<path d="M24 34 L16 60 L24 55 L29 62 L33 38Z M40 34 L48 60 L40 55 L35 62 L31 38Z" fill="#3a78d8" stroke="{INK}" stroke-width="1.8"/>'
     f'<circle cx="32" cy="26" r="18" fill="url(#ir)" stroke="{INK}" stroke-width="2.2"/><circle cx="32" cy="26" r="11" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="3 2.5"/>',
     rg('ir', [(0, '#b9d6ff'), (.6, '#3a78d8'), (1, '#24509a')]))

json.dump(SPRITES, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
print(len(SPRITES), 'sprites')
