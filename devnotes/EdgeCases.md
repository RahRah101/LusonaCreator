# Edge cases

Patterns that break naive models. The format has to hold every one of these before it's called done. One entry per pattern: the image, what it breaks, and the current answer (or "open").

Add to this as you find more. A good edge case is one where you can say *exactly* which part of the model it stresses.

## Multilinearity

### Dos Santos, Fig. 324 and Fig. 325: same dots, different lines
![Fig. 324](images/sources/gerdes_dos_santos_fig324.png) ![Fig. 325](images/sources/gerdes_dos_santos_fig325.png)

*Gerdes, Geometria Sona de Angola, after Dos Santos pp. 57–58.*

- **Same dot layout, two completely different decompositions into lines.** The dots don't determine the lines, so the route has to be stored and can't be derived with a pattern/algorithm all the time.
- **Lines of very different lengths share the grid**
- **324 mixes straight diagonals with curved caps in one line**: shape changes per segment, inside a single line.
- **Tiny curls between two dots** (324, top/bottom and side tips): the line makes a small self-loop that goes around *no* dot.
- **S-shaped snakes with free ends** (325): lines that wind between rows instead of crossing diagonally, and stop with a curl. The waypoints are dots, but the shape between them is a deliberate wave, and the line is open.
- **A marked dot** (324, centre: a dot with a ring): the dot itself is drawn differently. That's a symbol or style on a dot, not a line.
- **4-fold symmetry**: you'd want to shape one quarter and have the rest follow.
- **Not every line is a loop** (325): some lines start and end without the start joining the end again.

**Current answer:** routes are stored (not derived). Per-segment shapes handle the straight/curved mix. Curls are a connection shape (see "Self-loops" below). Open: how a symmetry is declared.

### Pearson, Fig. 326: *ndzango ya makisi* (the council of the dancers)
![Fig. 326](images/sources/gerdes_pearson_fig326_ndzango_ya_makisi.png)

*Gerdes, Geometria Sona de Angola, after Pearson p. 99.*

- **Teardrop petals reaching far outside the grid**, each around a single outlying dot, crossing themselves at the neck.
- **Nested squares in the centre**: two dark-blue diamonds, one inside the other, that never cross each other (they do cross the red and green lines).
- **Smooth bumps inside a straight weave**: the green line runs in straight diagonals but rounds over a dot in a soft arc at four spots near the centre.

**Current answer:** petals are a route around one dot plus an "elongated" shape (or an invisible anchor at the tip). Nested squares are just two routes. Bumps are a per-segment shape change.

### Pearson, Fig. 327: *makisi a VaMbunda* (the Mbunda dancers)
![Fig. 327](images/sources/gerdes_pearson_fig327_makisi_a_vambunda.png)

*Gerdes, Geometria Sona de Angola, after Pearson p. 100. Same layout as Fig. 326, different drawing.*

- **Hammer-head caps with no dots inside at all**: the gold line leaves the grid, draws a flat cap with straight sides and rounded corners, and comes back. Pure aesthetic shape, nothing to anchor it.
- Same dot layout as Fig. 326, drawn with different lines: the same lesson as 324/325.

**Current answer:** open. Invisible anchors at the cap corners plus `rounded-corner` segments would work, but it's a lot of points for one shape. A good test for parametric shapes or tangent handles.

## Shapes not bound to points

See "Shaping curves that no point dictates" in [Reflections.md](Reflections.md) for the options.

### Big curves far from any dot
![cadeira](images/examples/cadeira.png)
![dome over grid](images/examples/dome_over_grid.png)
![stork and leopard](images/sources/gerdes_stork_and_leopard.png)

### Caps with no dot dictating them
Fig. 327: a hammer-head cap with no dots inside.

![Fig. 327 detail](images/sources/detail_fig327_hammer_cap.png)

Fig. 324: an arched cap, straight sides flaring out to a rounded top, over two dots.

![Fig. 324 detail](images/sources/detail_fig324_curl_and_cap.png)

### Tapered tips
![horns](images/examples/horns.png)
![leaf tips](images/examples/leaf_tips.png)

### Straight runs with chosen corner styles
![spiral arms](images/examples/spiral_arms.png)
![diamond wings](images/examples/diamond_wings.png)

### Waves between dots
Fig. 325: the green and black lines wave between the dots, and **they end**: free curled ends inside the frame. Open strokes in a geometric sona, not just in figurative ones.

![Fig. 325 detail](images/sources/detail_fig325_snakes.png)

## Self-loops

Rule: **a loop with no dot inside is a shape; a loop with a dot inside is route.**

Fig. 324, the tip: a small loop around nothing (same crop as the cap above). **Answer:** a normal connection between two neighbouring cells, with the `curl` shape (size, side). The loop's self-crossing is not a route crossing.

![Fig. 324 detail](images/sources/detail_fig324_curl_and_cap.png)

Fig. 326, the petal: a loop around one far dot, crossing itself at the neck. **Answer:** route. It visits the far dot's cells, and the neck crossing is a real crossing.

![Fig. 326 detail](images/sources/detail_fig326_petal.png)

## Open strokes and figurative parts

### Legs, heads, tails: lines with ends
![antelope](images/examples/antelope_figurative.png)
![Mbambi the duiker](images/sources/kubik_mbambi_duiker.png)

### Straight bars inside frames
![frames with bars](images/examples/frames_with_bars.png)

## Out of scope

Textures drawn with several fingers at once.

![Ngandu](images/sources/kubik_ngandu_crocodile.png)
![chikuta changendzi](images/sources/kubik_chikuta_changendzi.png)

## To find

- [ ] A line that **passes through a dot** instead of around it (if that exists).
- [ ] Two lines that **touch without crossing** (tangent).
- [ ] A drawing where the **order of drawing changes the meaning** or the story (Kubik).
- [ ] Dots that belong to **no line** (characters, like the hunter and dog).
- [ ] Very **irregular dot layouts** (not a grid at all).
