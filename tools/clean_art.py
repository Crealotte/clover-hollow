"""Clean an AI-generated sprite for Clover Hollow.

Usage: python3 tools/clean_art.py input.png name [width]
- removes the faint colored fringe that image tools leave around edges
- turns a pale ground patch under the object into a soft warm shadow
- trims empty space and saves assets/art/<name>.png (default 440 px wide)
  plus a full-size copy assets/art/<name>_full.png
"""
import sys
from PIL import Image

def clean(src, name, width=440, ground_from=0.65):
    im = Image.open(src).convert('RGBA'); px = im.load(); W, H = im.size
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a < 16: px[x, y] = (0, 0, 0, 0); continue
            if a < 240 and y > H * ground_from:
                px[x, y] = (58, 36, 20, int(a * .42))
            elif a < 240:
                px[x, y] = (r, g, b, min(255, int(a * 1.1)))
    im = im.crop(im.split()[3].getbbox())
    im.save(f'assets/art/{name}_full.png')
    h = round(im.height * width / im.width)
    im.resize((width, h), Image.LANCZOS).save(f'assets/art/{name}.png', optimize=True)
    return im.size

if __name__ == '__main__':
    print(clean(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 440))
