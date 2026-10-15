# Clover Hollow art (hand-painted)

AI-generated sprites made with `docs/art-prompt-kit.html`, cleaned with `tools/clean_art.py`.

| File | What |
|---|---|
| building_barn.png | The style master. Every other sprite should match this look and camera angle. |
| farmer_idle.png | Farmer standing, hoe in hand |
| farmer_walk1.png | Farmer walking (alternate with idle for steps; mirror for the opposite direction) |
| farmer_work.png | Farmer hoeing the soil (plow, plant, harvest action) |
| tile_grass.png | Seamless 2:1 grass tile, 256x128 (made with `tools/make_tile.py`). Mirror it at random to hide repetition. |
| tile_grass_block.png | The full grass block with dirt sides. Scale it under the whole field to give the farm its island edge. |

`*_full.png` keeps the full resolution, and `source_*.png` is the untouched original from the image tool.

Images with a painted checkerboard or white background are cleaned with `tools/clean_checker.py` instead of `clean_art.py`.

Preview of the art together: `docs/art-preview-farm.png`.
