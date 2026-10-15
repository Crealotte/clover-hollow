# Clover Hollow art (hand-painted)

AI-generated sprites made with `docs/art-prompt-kit.html`, cleaned with `tools/clean_art.py`.

| File | What |
|---|---|
| building_barn.png | The style master. Every other sprite should match this look and camera angle. |
| farmer_idle.png | Farmer standing, hoe in hand |
| farmer_walk1.png | Farmer walking (alternate with idle for steps; mirror for the opposite direction) |
| farmer_work.png | Farmer hoeing the soil (plow, plant, harvest action) |

`*_full.png` keeps the full resolution, and `source_*.png` is the untouched original from the image tool.

Images with a painted checkerboard or white background are cleaned with `tools/clean_checker.py` instead of `clean_art.py`.
