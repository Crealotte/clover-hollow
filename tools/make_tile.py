"""Turn an AI tile picture into a seamless 2:1 isometric ground tile.

Usage: python3 tools/make_tile.py name   (reads assets/art/<name>_block_full.png)
Finds the top diamond (left, right and bottom corners of the surface), cuts it
out, stretches it to an exact 2:1 diamond and saves assets/art/<name>.png
(256x128). The full block with its dirt edge stays as <name>_block.png for the
farm's outer edge.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

def make(name, size=256, surface_test=None):
    im = Image.open(f'assets/art/{name}_block_full.png').convert('RGBA'); a = np.array(im)
    al = a[..., 3] > 128; H, W = al.shape
    ys, xs = np.nonzero(al)
    ly = int(np.median(ys[xs < xs.min() + 4])); ry = int(np.median(ys[xs > xs.max() - 4]))
    midy = (ly + ry) // 2; cx = (xs.min() + xs.max()) // 2
    col = a[:, cx, :3].astype(int)
    surf = surface_test(col) if surface_test else ((col[:, 1] > col[:, 0] + 15) & (col[:, 1] > col[:, 2] + 15))
    surf &= al[:, cx]
    by = int(np.nonzero(surf)[0].max()); half = by - midy; ty = midy - half
    L, R = xs.min() + 6, xs.max() - 6
    # inset the diamond so the tile's own edge shading and dirt lip are left out
    k = .08; w0, h0 = R - L, by - ty
    L, R = int(L + w0 * k / 2), int(R - w0 * k / 2); ty, by = int(ty + h0 * k / 2), int(by - h0 * k / 2)
    box = im.crop((L, max(0, ty), R, by))
    if ty < 0:
        pad = Image.new('RGBA', (box.width, box.height - ty), (0, 0, 0, 0)); pad.alpha_composite(box, (0, -ty)); box = pad
    box = box.resize((size, size // 2), Image.LANCZOS)
    m = Image.new('L', box.size, 0)
    ImageDraw.Draw(m).polygon([(size / 2, 0), (size, size / 4), (size / 2, size / 2), (0, size / 4)], fill=255)
    out = Image.new('RGBA', box.size, (0, 0, 0, 0)); out.paste(box, (0, 0), m)
    # fill any transparent holes inside the diamond with the average surface color
    arr = np.array(out); inside = np.array(m) > 0; holes = inside & (arr[..., 3] < 250)
    if holes.any():
        avg = arr[inside & (arr[..., 3] >= 250)][:, :3].mean(0).astype(int)
        arr[holes, :3] = avg; arr[holes, 3] = 255
    Image.fromarray(arr).save(f'assets/art/{name}.png', optimize=True)
    return (L, ty, R, by)

if __name__ == '__main__':
    print(make(sys.argv[1]))
