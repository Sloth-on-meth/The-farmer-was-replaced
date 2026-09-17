# TheFarmerWasReplaced — Save0 scripts

This folder is the game's save slot (`Save0`), version-controlled with git. `__builtins__.py` is the game's read-only API reference; `f0.py`–`f9.py` are the drone programs assigned to each of the game's script slots, and `save.json` is the game's own save state.

## Scripts

| File | Purpose |
|---|---|
| `f0.py` | Resets the farm (`clear()`). |
| `f1.py` | Mixed farm: cactus band on the west edge, pumpkin band on the east edge, tree/carrot/bush checkerboard in between, with companion-planting support. Multi-drone via chunked column ranges. |
| `f2.py` | Dedicated pumpkin farm. Parallel `plant_pass`/`search_pass` workers pulled from a shared job queue; replants dead pumpkins; harvests once a full round comes back mature and clean. |
| `f3.py` | Multi-crop farm: checkerboard trees/carrots, a cactus band, a pumpkin band, and sunflowers harvested best-first by petal count. Work is distributed across drones via a job queue. |
| `f4.py` | Maze/treasure solver. Grows a bush maze, then explores it with a wall-following drone plus randomized forking drones, until the treasure is found. |
| `f5.py` | Sunflower farm. One drone per column range, replanting and harvesting in a loop. |
| `f6.py` | Cactus farm. Plants in parallel by column, then repeatedly bubble-sorts columns and rows (in parallel) until a full round makes no swaps, then harvests — cacti chain-harvest for a squared yield when the whole grid is sorted. |
| `f7.py` | Carrot farm. Same parallel column-range pattern as `f5`, with a hat that changes per work phase (till/grow/harvest). |
| `f8.py` | Grass farm. Grass grows automatically on Grassland, so each tile just gets re-tilled back to Grassland and harvested when ready. Drones alternate sweep direction, and cycle through a parade of unlocked hats every 10 rows. |
| `f9.py` | Combined grass + tree farm. Trees go on a checkerboard (`x % 2 == 0 and y % 2 == 0`, tilled to Soil so ambient grass can't invade the slot), grass fills every other tile. |

## Conventions used across scripts

- **Watering/fertilizing**: most scripts define a `water_tile()` that tops up water below a threshold and fertilizes anything not yet ready to harvest. Every farm script should call it per tile.
- **Multi-drone parallelism**: the farm is split into column (or row) ranges sized to `max_drones()`, one worker per range, `spawn_drone`'d up front and `wait_for`'d at the end. `spawn_drone` can return `None` if the drone budget is exhausted — always guard against that before `wait_for`.
- **Tick costs matter more than logic complexity**: per the game's own docs, `move()` and `change_hat()` cost 200 ticks each, while most other actions (`till`, `plant`, `harvest`, `measure`, `get_*`) cost ~1 tick. `do_a_flip()` costs a flat 1 real-world second and is *not* sped up by speed upgrades — avoid calling it per-tile.

## Known quirks

- **Grass squats on empty Grassland**: since Grass grows automatically on any Grassland tile, any tile you want to keep for another crop (e.g. `f9`'s tree slots) must be tilled to Soil, or ambient grass will occupy it before you get back to plant.
- **Cactus sorting is move-heavy** (`f6`): the whole-grid bubble sort can take on the order of *field-size* rounds to converge, and each round is dominated by 200-tick moves — this is why cactus farming feels slow on large fields.

## Usage

After editing a script, reload/re-select its slot in-game so the drone picks up the new file contents — the game doesn't hot-reload a running script's already-loaded code from an external edit.
