# Pipeline

*Draft, November 2026.*


## V1

We will start with a Dart core.
1. **`sona_core`: a pure Dart package**: It's tested with `dart test` and usable from command-line tools (e.g. SVG export for the website).
2. **The app starts as one screen** that loads a hand-written `.sona.json` from assets and paints it. No Riverpod, routing, repositories or validation stubs until M3 passes.
3. **Every milestone has an exit test.** Don't start the next one until it passes.

## Milestones

**M1. The test set: four hand-written files + the schema.**

| File | Why |
|---|---|
| `figure_eight.sona.json` | The smallest closed line: cells, one crossing, smoothing |
| `hambelo.sona.json` (Kubik, *Tusona* p. 38, the pen of goats) | Small, with a recorded story, a start arrow and the zigzag decoration |
| `fig324.sona.json` (Dos Santos via Gerdes, the eagle's nest) | Multilinear, curls, caps, straight + curved in one line, a ringed dot, 4-fold symmetry |
| `creation.sona.json` (the logo) | Big free sweeps, glyphs, a start arrow, the central dot column |

Authoring aid: the source image drawn faintly under the render (the format's `reference` key), so free vertices can be placed by eye. If writing coordinates by hand gets too slow, a small Dart script with loops for grids and names for cells.
*Exit:* all four validate against `sona_core/spec/sona.schema.json`.

**M2. `sona_core` + a static painter.**
`sona_core`: load, cells, resolve, curve, check. Flutter app: a `CustomPainter` that draws the geometry.
*Exit:* each test file renders recognisably next to its source image. The cell-offset constant is chosen and frozen. Specs.md goes to v0.2 with whatever broke.

**M3. Animation + story.**
The line appears in drawing order (`extractPath`), and story text appears when the line reaches its position. Then a first Flame experiment: something travelling along the path (serpent or bouncing light).
*Exit:* *hambelo* plays with Kubik's Luchazi and English text at the right moments, ending on *kelekeche!*; the logo plays from its start arrow.

**M4. Stress the format.**
One file per entry in [EdgeCases.md](EdgeCases.md), plus two importers in `sona_core`: a mirror-curve generator that writes paths, and Tran's kolam gesture sequences (see [PriorArt.md](PriorArt.md)).
*Exit:* every edge case has a file that renders, or an issue is written into Specs.md.

**M5. Interaction design, then the editor.**
On paper first: how a person lays out dots, draws a line *around* them by dragging through cells, adds free points, binds and unbinds, uses invisible-dot layers, undoes a whole gesture. Then the smallest editor that can recreate the test set (this is where state management and undo commands come in).
*Exit:* the four test files can be rebuilt in the editor without touching JSON.

**Later:** the catalogue (a folder of files, an index, a website with exported animations), the scanner (trained on images our own renderer generates, with perfect masks for free), community and sharing.

## Repo layout

Two repos. **`sona_core`** ([RahRah101/sona_core](https://github.com/RahRah101/sona_core), private for now) is the format and its reference implementation, so it can be opened up on its own later. **LusonaCreator** holds it as a git submodule at `src/sona_core`, plus everything that stays private.

```
LusonaCreator/
  src/
    sona_core/            submodule: its own repo
      spec/
        sona.schema.json  JSON Schema for the format
        validate.py       schema + reference checks (Python tooling)
        examples/         the test set (*.sona.json)
      lib/                pure Dart: model, cells, geometry, measure, check, importers
      bin/                command-line tool (validate, export SVG)
      test/
  app/                    Flutter (+ Flame later)
  devnotes/
  tools/                  local only (edge-case miner, Python)
```

- **Working with the submodule:** commit inside `src/sona_core` first, push it, then commit the updated pointer in LusonaCreator. Clone with `git clone --recursive`, or run `git submodule update --init` after a plain clone.
- **Keep `sona_core` free of copyrighted material** (book crops, Kubik's story text), so it can go public. Reference images and recorded stories for the test files stay in LusonaCreator.

## Testing

- Schema validation of every example file.
- `dart test` on `sona_core`: cell positions, a closed loop is smooth where it joins itself, `at` positions resolve to the right point.
- Golden tests in Flutter: each example's render doesn't change by accident.
- A side-by-side screen: render vs source image, for the human eye. That's the real test.

## Decisions to lock now vs later

| Lock now | Decide later |
|---|---|
| JSON + JSON Schema, y down, one unit = dot spacing | Walls that meet or branch (Figs. 198, 174b) |
| `auto` segments = quadratic B-spline through cells | Grids: other lattices (triangular, hexagonal), mirror names |
| Vertex IDs; line positions land on the drawn line; grids with sparse gates | |
| Bound / free vertices as in Specs.md | Dot layers: in v0.1 or v0.2 |
| Flutter / Dart, pure-Dart core | State management, undo design (M5) |
| The four test files | Symmetry beyond an editor hint; bundles (`.sona.zip`) |

