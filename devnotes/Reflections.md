# Reflections

Thinking out loud as LusonaCreator restarts (November 2026). The 2024 design is in [Blog_draft.md](Blog_draft.md).

## Why this is hard

Sona are part system, part freehand. 
A lot of a drawing follows rules (dots, cells, crossings, the line weaving around points), but parts of it are free with big sweeping curves, horns, legs, heads, sharp tips. 

A format that only knows dots and smooth curves can't hold the real corpus. A format that's pure freehand loses everything that makes sona sona: what the line goes around, the order it's drawn in, and where the story happens.

## Method: design from the hardest cases

Last time the model was built from the simplest sona and extended with add-ons as harder ones showed up, which is a poor approach.

This time it goes the other way: collect the most limiting patterns first ([EdgeCases.md](EdgeCases.md)), define the constraints they impose, and design the minimum-viable-most-generalizable model that holds all of them from the start. 
The simple cases then fall out as specially dumb cases instead of being the foundation everything else gets bolted onto.

**Finding the hard cases: LLM reconnaissance.** Reading every figure in every source by hand doesn't scale, so `tools/edge_cases/` (developed by Claude, to be used by Claude(recursive huh)) extracts every figure and page from `sources/` (1,283 units), has a cheap model (Haiku) screen out pages with no sona (750 left), and has a strong model (Opus) flag what each drawing would break in the *basic naive* model, which it reads from this file and EdgeCases.md. 
Every claim comes with a bounding box, and the gallery shows the crop, so one can confirm or reject it in seconds.

## What the real corpus throws at the model

| What happens | Examples | What the model needs |
|---|---|---|
| Regular weaving around dots | [regular grid](images/examples/regular_grid.png), [patas de antílope](images/examples/patas_de_antilope.png), [hunter and dog](images/sources/gerdes_hunter_and_dog.png) | Cells + smoothing. The easy part |
| Big sweeping curves far from any dot | [cadeira](images/examples/cadeira.png), [dome over grid](images/examples/dome_over_grid.png), [side wings](images/examples/side_wings.png), [large ellipses](images/examples/large_ellipses.png), [double heart wings](images/examples/double_heart_wings.png), [stork and leopard](images/sources/gerdes_stork_and_leopard.png), [Mukanda](images/sources/kubik_mukanda.png) | **Invisible points** as anchors for the shape |
| Shapes that aren't smooth curves | [horns](images/examples/horns.png), [leaf tips](images/examples/leaf_tips.png), [vine](images/examples/vine_triangle_top.png) (triangle top, curved tail), [spiral arms](images/examples/spiral_arms.png) (straight arms, rounded corners), [diamond wings](images/examples/diamond_wings.png) | Edge shapes beyond Bézier: straight / rough, rounded-corner, horn |
| Figurative parts that aren't the woven line | [antelope](images/examples/antelope_figurative.png) (legs, neck, tail), [frames with bars](images/examples/frames_with_bars.png), [Mbambi the duiker](images/sources/kubik_mbambi_duiker.png) (legs, two heads) | Open strokes that start and end, separate from the closed loop |
| Lines that wander between groups | [separated blocks with an outer loop](images/examples/separated_blocks_outer_loop.png) | Same route model; the line just visits several dot groups |
| Not dot-based at all | [Ngandu the crocodile](images/sources/kubik_ngandu_crocodile.png): drawn with **four fingers at once**, so every stroke is four parallel wavy lines. [Chikuta changendzi](images/sources/kubik_chikuta_changendzi.png): a thin one-finger line crossed by a thick two-finger line | **Out of scope.** These are drawing techniques, not line structures. At most, a line can have a thickness |

Invisible points + rough edges handle a lot. For example [Diamond wings](images/examples/diamond_wings.png) is just invisible points with edges set to rough.

## Design v2: bound and free vertices (supersedes parts of the sections below)

November 2026, after the edge-case mining. 
The earlier design kept adding features: invisible points, anchor kinds, shape types (horn, curl, cap, wave). The hard cases ([bird with the long neck](images/examples/bird_long_neck.png), [bird with legs](images/examples/bird_triangle_legs.png), [butterfly](images/examples/butterfly.png), [X with hooks](images/examples/x_long_diagonals_hooks.png), [pinwheel](images/examples/pinwheel_irregular_dots.png), [two blocks](images/examples/two_blocks_sweeping_curves.png), [grid with a cut](images/examples/grid_with_cut.png)) say: stop adding features and make the base general.

![Bird with the long neck](images/examples/bird_long_neck.png)

**A sona is a set of paths. A path is a sequence of vertices. Each vertex is either:**
- **bound** (attached) to something: a dot's cell (NW/NE/SE/SW), a dot's centre, a wall, or a point on another path (T-junctions, legs growing out of a body). It follows that thing when it moves; or
- **free**: just x, y. This is done with a "bag of invisible points", hidden from the user. In the editor they're just how you drag a curve, like the points in a font.

**Gerdes got there first.** In *Geometria Sona de Angola* he shows auxiliary lines (his *linhas* / *segmentos auxiliares*, in orange) that the sona line wraps around. They're **drawn and stay in the finished drawing** (Fig. 198d; Fig. 122: "drawn in advance"), but he leaves them out of the line count. So: **a thing the line goes around can be a point or a segment.** A wall between two dots that the line can't cross is a mirror in the mirror-curve model. In this model, an auxiliary line isn't a path: it's a **wall**, scaffolding like the dots (visible or hidden, drawn first, never counted). It has cells along its sides and past its tips, and the line binds to them the way it binds to a dot's cells. Legs, tails and trunks are something else: extra strokes, which stay paths. See [EdgeCases.md](EdgeCases.md), "Gerdes' auxiliary lines are drawn, not hidden".

**Each segment between two vertices** is `auto` (the smooth default, computed from its neighbours), `straight`, or a curve with explicit handles.

Everything else is **presentation**: dot style (ring, leaf, glyph, size), segment style (colour, thickness, stroke technique), end caps on open paths (arrowheads, forked feet, hooks), which line is on top at a crossing. And **layers** by kind: lines (including Gerdes' auxiliary lines: visible, not counted), construction (editor-only guides, hidden), symbols, annotations/labels, timeline (drawing order, start points), reference photo. Relations between drawings (recorded vs reconstructed, derived from) are file metadata, not drawing content!

**Consequences:**
- **Shape types become editor tools** Horn, curl, cap and wave are tools that *write* vertices and handles. The format never needs a new type for a new shape. A segment can keep an optional tag (`made_with: curl(size=…)`) so it stays editable as a curl; a program that doesn't know the tag still draws it from the stored points.
- **The grid is presentation too.** Dots are free positions, each with its own four cells. The grid is only editor snapping, so the denser dot column and irregular layouts aren't special.
- **Bound vs free is a construction choice, not meaning.** *(Corrected, November 2026: an earlier version said "the meaning lives in the bound vertices". It doesn't.)* The same wing can be free vertices or the cells of a hidden dot or wall. A sona's meaning is what it depicts and the story it tells: labels, story, sources. See [Specs.md](Specs.md), principle 5: one drawing, many constructions.
- **Freehand is fine as long as it's points.** A handful of discrete, editable, animatable free vertices is not the bad kind of freehand; an unstructured scribble would be. The route stays structured.

**Format generality is not generator generality.** The format must *hold* anything; that's bound + free vertices. A generator (mirror curves, plaited mats, Gerdes' chaining rules) only has to *produce* the woven parts. The bird's neck isn't produced by any rule: it's an artist's decision, and the format just stores it.

**Checked against the hard examples:**

| Drawing | How it's held |
|---|---|
| [Bird, long neck](images/examples/bird_long_neck.png) | Body bound; neck, zigzag arms, tail loop free; arrow ends are end caps; eye is a tiny path or a symbol |
| [Bird, triangle](images/examples/bird_triangle_legs.png) | Legs: open paths starting from a vertex bound to a point on the triangle; forked end caps. Wings free |
| [Butterfly](images/examples/butterfly.png) | Wing outline: its own path of free vertices. Heart weaves bound. Small circles: tiny paths or dot style |
| [X with hooks](images/examples/x_long_diagonals_hooks.png) | Diagonals straight to free corner vertices; hooks are end caps; the bottom teardrop has no dot inside, so it's segment shape |
| [Grid with a cut](images/examples/grid_with_cut.png) | A crossing replaced by two turn-backs: a different route, still bound. Ringed column: dot style |
| [Two blocks](images/examples/two_blocks_sweeping_curves.png) | Blocks bound; the sweeping curves between them run through free vertices |
| [Pinwheel](images/examples/pinwheel_irregular_dots.png) | Dots at free positions; arms end on dot centres; kite tips are free vertices with straight segments; ringed centre: dot style |
| [Four-dot knot](images/examples/four_dot_knot.png) | Dots at free positions, loops bound to their cells |

What still needs real thought: the editor UX for binding and unbinding vertices, and how scanning decides bound vs free (probably: near a dot's cell, bound; otherwise free).

## What CAD teaches: procedural

November 2026. Walls, symmetry, gates and generators aren't just features of a drawing; they're **construction techniques**, as in CAD software. The format exposes them, and one drawing can be built several ways ([Specs.md](Specs.md), principle 5).

**Two families of CAD, and which one we are.**
- **Constraint-based** (SolidWorks sketches, AutoCAD's parametric constraints, SolveSpace): declare "parallel, tangent, equal", and a solver finds geometry that satisfies everything. Powerful, but you get over- and under-constrained sketches, solver jumps, "why did everything flip". That's the brain-burster.
- **Procedural / dataflow** (Grasshopper, Houdini, a spreadsheet): every step takes inputs and produces outputs, data flows one way, no cycles, no solving. Change an input and everything downstream recomputes.

**We're the second family.** Grid => gates => generator => paths. Dot => cells => attached vertices. Seed path => symmetry => copies. "Constructions run one way" is exactly this. It's like Grasshopper I guess.

**What CAD already solved, which we'll run into:**
1. **Construction geometry.** Reference lines and points that shape the model but never appear in the output: our hidden dots, hidden walls and `guide` paths. First-class: visible in the editor, toggleable, never rendered.
2. **Snapping instead of constraints.** AutoCAD's object snaps (endpoint, midpoint, intersection, tangent) and SketchUp's inference attach things *as you draw*, with no solver. For us: snap to a cell, a gate, a wall point, the end of a line, tangent continuity. **A snap creates a one-way attachment.** That's how bound vertices get made: the user never thinks "bind", they just snap.
3. **Baking.** Grasshopper "bakes" procedural output into plain geometry, cutting the link. Editing a generated path by hand (dropping its `made_with`) is baking. Make it an explicit action ("detach from generator"), not a surprise.
4. **Pattern the feature, not the result.** In CAD you mirror or pattern the *operation*, so editing the seed updates every copy. That's what `symmetry` means in the editor: draw one quarter of Fig. 324, the other three follow live. Same for "bounce it out": start one path, let the grid fill the rest.
5. **Blocks and instances.** Define once, place many times with a transform. Sona reuse motifs constantly (heads, forked feet, petals, *chingelengele*). A motif library, with drawings placing instances, is a natural v0.2 idea, and good for teaching.
6. **The topological naming problem.** The real warning: FreeCAD fought it for years. When an upstream step recomputes, references to downstream things break. **We have it already:** the rooster's legs attach to `v_d1`, a vertex of the generated body. Flip a gate, the generator rewrites the body, `v_d1` is gone, the legs dangle. Fixes: attach to stable things where possible (a dot's cell survives regeneration, a generated vertex doesn't), and have generators write **deterministic IDs** derived from their inputs (cell + visit count), so the same vertex keeps its ID across re-runs.

**Where sona are not CAD: two timelines.** CAD has no drawing order; sona do.
- **Construction history:** how you *built* it in the editor (grid, gates, generate, walls, edit the wings).
- **Drawing order:** how it's *performed*: in the sand, in the animation, timed to the story.

Never confuse them. A generator can write paths in any order; the drawing order must still be how a drawer would trace it.

**For the format.** v0.1 already has the constructions, scattered: grids hold gates, symmetry is a hint, walls are scaffolding, `made_with` tags paths. Eventually they want **one explicit construction graph**, each construction with its inputs and outputs, like a feature tree: `{ "tool": "mirror_curve", "inputs": { "grid": "g1" }, "outputs": ["p1", "p2"] }`. Like native CAD files, store both the history (for editors) and the result (for readers). Not now: the spec is frozen, and this should come out of building the test files.

**For the UX.** The editor is a tool palette (dots, grid, gate, wall, path, mirror, generate, bake), plus snaps, plus a construction tree you can step back through. A concrete start for M5.

**To read and look at:**
- **Grasshopper** (Rhino): the procedural model itself. Book: Arturo Tedeschi, *AAD: Algorithms-Aided Design* (2014).
- Robert Woodbury, *Elements of Parametric Design* (2010): the theory of procedural/parametric modelling, written for designers. The best single book for this.
- **Cuttle** (cuttle.xyz): 2D parametric CAD for laser cutting, with components and code. The closest domain to ours: flat line art, repeated motifs.
- **Graphite** (graphite.rs): open-source procedural 2D vector editor with a node graph, in Rust. Readable code for exactly this architecture.

## Design: route + shape, per line

Every line has two layers.

**1. Route (topology).** The ordered list of waypoints the line passes: a dot's cell (NW / NE / SE / SW) or an invisible anchor, plus the crossings. This is the *meaning* of the drawing: what it goes around, and in what order. Animation, storytelling and scanning all read this layer.

**2. Shape (geometry), per segment.** Each stretch between two waypoints has a shape type with parameters:
- `smooth`: B-spline default (cell centres as control points);
- `straight` / `rough`: sharp corners, straight runs;
- `rounded-corner`: straight with a corner radius (spiral arms);
- `horn`: tapered spike with direction, length, curl;
- `freehand`: raw Bézier control points stored as-is. The escape hatch, so **anything** can be represented even when no rule fits.

**Modularity:** a new shape is a new segment type. Old files keep working; a generator that doesn't know a shape falls back to `smooth`.

**Lines can be closed loops or open strokes.** Legs, necks, bars and tails are open strokes.

**Out of scope: textured tusona like Ngandu.** Kubik shows some tusona that aren't dot-and-line drawings at all (four-finger wavy textures, trembling-hand lines). They're a different kind of drawing, so the format doesn't try to cover them. A per-line thickness is the most it needs.

## Shaping curves that no point dictates

Some curves are chosen for looks, not dictated by any dot: the arched caps in [Fig. 324](images/sources/gerdes_dos_santos_fig324.png), the hammer-head caps in [Fig. 327](images/sources/gerdes_pearson_fig327_makisi_a_vambunda.png), the snakes in [Fig. 325](images/sources/gerdes_dos_santos_fig325.png), the dome in [cadeira](images/examples/cadeira.png). Invisible points are one tool for this, not the only one. Options, from most structured to least:

1. **Invisible anchors.** Extra waypoints off the grid. Best for big sweeps that need a "place" to go around.
2. **Parametric segment shapes.** `horn`, `rounded-corner`, plus things like `bulge` (how far a curve bows out), `ogee` (an S-curve, as in the necks of the Fig. 327 caps), `wave` (the snakes). Parameters are relative to the segment's own endpoints, so the shape scales and moves with the dots.
3. **Tangent handles on waypoints.** Any waypoint can optionally override the direction and strength the curve leaves and arrives with, like Bézier handles in Illustrator. That gives local control without adding points: pull a cap into a point, flatten a side.
4. **Curls as a connection shape.** The tiny curls in Fig. 324 aren't part of the route: the route is a normal connection between two neighbouring cells, and the curl is just that connection's shape (`curl`, with size and the side it loops toward), the same way a corner is set to rough or square. *(Earlier rule, now just one option: "a loop with no dot inside is a shape; a loop with a dot inside is route". Under principle 5, the same curl can also be built around a hidden dot. The scanner still needs a default choice for loops with no dot inside, and a `curl` on that connection is a reasonable one.)*
5. **Freehand in the segment's local frame.** The escape hatch: raw Bézier control points, but stored relative to the segment's start→end, so they survive moving the dots.
6. **Symmetry declarations.** Say "this drawing has 4-fold symmetry" (or a mirror), shape one part, and the rest follows. Most of the hard aesthetic curves come in symmetric sets.

All of these live in the **shape** layer. The route never changes, so animation, storytelling and scanning don't care which one was used.

## On "non-crossing areas"

Regions the curve isn't allowed to cross would generalize worse and make the curve *solve* for its own shape, which is hard to control. The route already says what the line goes around; the shape layer just draws between waypoints. A checker can still **warn** when a curve clips a dot, without constraining the geometry.

## Scanning (tightened)

The output of a scan is the format itself: dots, anchors and ordered routes.
1. Clean the photo (perspective, contrast).
2. A small segmentation model (TFLite) separates **dot pixels** from **line pixels**. That's where ML earns its keep
3. Dots: connected blobs; fit the grid.
4. Lines: skeletonize to 1-pixel strokes, so junctions become crossings.
5. Trace with the sona rule: **go straight through crossings**. That walks each line in order.
6. Snap the trace to cells. Where it runs far from any dot, add an invisible anchor.
7. The user corrects the result over the photo.

Training data comes from our own renderer (random and real sona, plus sand texture, blur and perspective), with perfect masks for free. Scanning comes after the format and the renderer exist.

## Still open

- **UX:** how a person actually builds all this (placing anchors, choosing segment shapes, drawing open strokes) without it feeling like CAD.
- How labels attach to *regions* (Mukanda's enclosures) as opposed to dots and lines.
