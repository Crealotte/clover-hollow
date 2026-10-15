"""Remove a painted checkerboard / white background from an AI image.

Usage: python3 tools/clean_checker.py input.png name [width]
Any large connected area of near-white or light-grey pixels is treated as
background (this also clears gaps between arms and legs). A light patch near
the feet becomes a soft warm shadow. Saves assets/art/<name>.png and _full.png.
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

def clean(src, name, width=300, min_area=350, ground_from=.9):
    rgb = np.array(Image.open(src).convert('RGB')).astype(int)
    H, W, _ = rgb.shape
    mn, mx = rgb.min(2), rgb.max(2)
    bgish = (mn >= 200) & ((mx - mn) <= 24)
    lab, n = ndimage.label(bgish)
    sizes = ndimage.sum(bgish, lab, range(1, n + 1))
    big = np.zeros(n + 1, bool); big[1:] = sizes >= min_area
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    big[border[border > 0]] = True
    bg = big[lab]
    bg = ndimage.binary_closing(bg, iterations=2)
    bg[:4], bg[-4:], bg[:, :4], bg[:, -4:] = True, True, True, True
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.9))
    out = Image.fromarray(rgb.astype(np.uint8)).convert('RGBA'); out.putalpha(alpha)
    arr = np.array(out).astype(int)
    lightgrey = ((arr[..., :3].max(2) - arr[..., :3].min(2)) < 55) & (arr[..., :3].min(2) > 135) & (arr[..., 3] > 0)
    rows = np.arange(H)[:, None] >= H * ground_from
    sh = lightgrey & rows
    arr[sh, 0], arr[sh, 1], arr[sh, 2] = 58, 36, 20
    arr[sh, 3] = (arr[sh, 3] * .32).astype(int)
    out = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    out = out.crop(out.split()[3].getbbox())
    out.save(f'assets/art/{name}_full.png')
    h = round(out.height * width / out.width)
    out.resize((width, h), Image.LANCZOS).save(f'assets/art/{name}.png', optimize=True)
    return out.size

if __name__ == '__main__':
    print(clean(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 300))
