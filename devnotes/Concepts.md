# Concepts

A primer for anyone who just found this repo. [Reflections.md](Reflections.md) is where the thinking happens, [EdgeCases.md](EdgeCases.md) are edge cases the software must handle, and [Specs.md](Specs.md) is the file format, and [Prototype.md](Prototype.md) is the build plan. This file gives the big picture: what LusonaCreator is, the ideas it's built on, how the pieces fit, and a glossary.

*Draft, November 2026.*

---

## The ideas it's built on

**1. The file is the product.** Apps come and go; a good format outlives them. Every other piece reads or writes `.sona.json` files, so any of them can be rewritten in any language without losing the drawings.

**2. A line is points, attached or free.** A line is a sequence of vertices. A vertex is either *attached* to something (a dot's cell, a dot's centre, a wall, a point on another line) and follows it when it moves, or *free*: just a position. Neither carries more meaning than the other. They're two ways to place a point.

**3. One drawing, many constructions.** The format doesn't pick one correct way to define a drawing; it exposes construction techniques: dots, hidden dots, walls, grids and gates, symmetry, generators. The same sona can be built with walls or with hidden dots, by hand or by bouncing one path out across a grid, like in CAD software. Constructions run one way (inputs → drawing, both stored), with no constraint solving.

**4. Design from the hardest cases.** The model is built to hold the most difficult real sona first ([EdgeCases.md](EdgeCases.md)). The simple ones are special cases of it, not the foundation.

**5. Sona are not one algorithm.** Mirror curves explain a big family of regular sona, but not the figurative ones. Rule-based generators are *tools that write ordinary lines*, never the model itself.

**6. Drawing order is part of the drawing.** Kubik recorded how sona are actually drawn: what comes first, where the line starts, which way it goes. That order drives the animation and the timing of the story.

**7. Sources matter.** Every drawing keeps where it came from (collector, page, meaning), and drawings can have several sources and meanings. Reconstructions are marked as reconstructions.

**8. Offline first.** Files are small and self-contained, and the app and scanner have to work without a connection.

---

## How the pieces fit

```
  hand-written ─┐
  editor ───────┤
  scanner ──────┼──►  .sona.json  ──►  core  ──►  geometry  ──►  renderers
  generators ───┘     (the format)    (library)   (ordered        · static SVG
  (mirror curves,                                  curves, in      · animated SVG
                                                   drawing order,  · video
                                                   with lengths,   · Flutter / Godot / Python / …
                                                   caps, story
                                                   positions)
  catalogue = a folder of .sona.json files + an index
```

### The four steps, kept separate

| Step | Question | Where it lives |
|---|---|---|
| 1. Topology | What's in the drawing: dots, their cells, what each vertex is bound to | The file |
| 2. Traversal | In what order and direction | The file: path order + vertex order |
| 3. Geometry | How that becomes curves | Core: resolve vertices to points, smooth into curves |
| 4. Rendering | How it's shown | Renderers: SVG, animation, video, apps |

### The core library

One small library, no drawing code, no UI. What it does:

| Function | Does |
|---|---|
| `load` | Read a file and validate it against the JSON Schema |
| `cells` | A dot's four cell positions, from local spacing |
| `resolve` | Every vertex of a path → a point (follows bindings) |
| `curve` | A path -> an ordered list of cubic Bézier segments (`auto` = quadratic B-spline, `straight`, `curve` with handles; `sharp` corners) |
| `measure` | Arc length, and "where is position `at` on this path" (for junctions, labels, story beats) |
| `crossings` | Where lines cross, and which is on top (later stroke by default) |
| `linearity` | How many lines (walls and extra strokes never count) |
| `check` | Warnings: a curve clipping a dot, dangling references, unclosed loops |

**The geometry it outputs is the contract for renderers.** A renderer only needs: per path, in drawing order, a list of cubic segments with arc lengths, plus caps, styles and story beats as positions along the line. The core can also **export that as JSON ("baked geometry")**, so a renderer in another language (a Godot scene, a Python video script) doesn't need its own copy of the core.

---

## Glossary

| Term | Meaning |
|---|---|
| **Lusona / sona / tusona** | The drawing (singular), drawings (plural); *tusona* in Luchazi (Kubik) |
| **Dot** | A point laid out first, with the fingertips. Free position; visible or invisible |
| **Cell** | One of a dot's four corners (NW, NE, SE, SW) that the line passes through. ID: `d12:NE`. Derived, never stored |
| **Path** | One line: an ordered list of vertices, closed or open |
| **Bound vertex** | A vertex attached to a dot's cell, a dot's centre, a wall cell, or a point on another path. Follows it when it moves |
| **Free vertex** | A vertex that's just x, y |
| **Construction** | A way of building part of a drawing: by hand, hidden dots, walls, a grid and gates, symmetry, a generator. One drawing can be built several ways |
| **Segment** | The stretch between two vertices: `auto`, `straight` or `curve`, plus a stroke style |
| **Wall** | Gerdes' *linha auxiliar*: a line laid down before the sona line, which the line wraps around and doesn't cross. Scaffolding, like dots: it has cells, and it's never counted. Can be hidden (a pure mirror) |
| **Extra stroke** | A drawn stroke that doesn't constrain the line (legs, tails, bars, a tree's trunk). A path, not counted |
| **Linearity** | The number of separate lines. *Monolinear* = one line |
| **Mirror curve** | The model where a line bounces between dots off small two-sided mirrors. Explains regular sona, kolam and Celtic knots |
| **Gate** | The place between two neighbouring dots where a mirror can sit or not (kolam generators) |
| **Cap** | The decoration on the end of an open line: arrow, fork, knob… |
| **Story beat** | A piece of text or audio tied to a position along a line |
| **Dot layer** | A group of dots, e.g. invisible scaffolding for one line (proposed) |

## Prior systems

See [PriorArt.md](PriorArt.md). Short version: mirror-curve generators for kolam and regular sona exist (kolam-maker, muggula-prastaram, Chavey's Sona-Drawing); a kolam gesture format exists (Tran's R package); nothing covers figurative sona, stories, provenance or offline photo → editable line.
