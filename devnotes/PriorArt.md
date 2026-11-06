# Prior art

What already exists (searched November 2026: web, app stores, GitHub).

## Sona

| What                                                                                                      | Notes                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [beloitcollegecomputerscience/Sona-Drawing](https://github.com/beloitcollegecomputerscience/Sona-Drawing) | Java. "Chokwe sona drawings from a layout of dots and walls": the mirror-curve model. Darrah Chavey's group at Beloit                                                                                                                                                                                                                                                                                                   |
| Chavey, Bridges papers                                                                                    | [Mathematical Experiments with African Sona Designs](https://archive.bridgesmathart.org/2009/bridges2009-305.html) (2009), [Strip Symmetry Groups of African Sona Designs](https://archive.bridgesmathart.org/2010/bridges2010-111.html) (2010). An older Java program, *Nitus*, covered kolam and Celtic knots ([JMM 2007 abstract](https://www.jointmathematicsmeetings.org/amsmtgs/2109_abstracts/1035-j1-1925.pdf)) |
| [itlearningcod/Sona-Drawer](https://github.com/itlearningcod/Sona-Drawer)                                 | Small HTML tool to "analyze sona drawing properties".                                                                                                                                                                                                                                                                                                                                                                   |
| Gerdes, Jablan                                                                                            | [Lunda Geometry](https://www.sahistory.org.za/sites/default/files/archive-files3/paulus_gerdes_lunda_geometry_mirror_curves_desbook4you.pdf), [Gerdes' Visual Mathematics pages](https://www.mi.sanu.ac.rs/vismath/paulus/index.html), [Mirror-Curves and Knot Mosaics](https://arxiv.org/pdf/1106.3784), [Mirror-curve codes](https://emis.univie.ac.at/journals/PIMB/108/18.html). Papers                 |
| App stores                                                                                                | No sona app. Only "draw in the sand"                                                                                                                                                                                                                                                                                                                                                                                    |


## Kolam generators (all mirror-curve / gate based)

| What | Notes |
|---|---|
| [evoluteur/kolam-maker](https://github.com/evoluteur/kolam-maker) | MIT, plain JS, offline web app. Square and diamond grids, symmetry, click between dots to toggle cross/bounce, "make it one line", animated stroke, rice-flour textures, PNG/SVG export. Closest UX to the regular-sona part. Same author: Celtic-Knot-Maker |
| [saahily/muggula-prastaram](https://github.com/saahily/muggula-prastaram) | MIT, TypeScript, on npm. Every muggu on a grid as a bit string of gates, with indexing and enumeration. Custom dot shapes with holes, SVG render with stroke animation |
| [SeshadriSivakumar/One-Stroke-Pulli-Kolam-Generation](https://github.com/SeshadriSivakumar/One-Stroke-Pulli-Kolam-Generation) | Code behind the Heritage Science "kolams up to 501 dots" paper ([press](https://theprint.in/india/trading-rice-flour-for-algorithms-now-ai-can-draw-pulli-kolams-beyond-human-imagination/2888329)) |
| Others | [Dhanya-Abhirami/Kolam](https://github.com/dhanya-abhirami/kolam) (L-systems), [devalgupta404/kolam](https://github.com/devalgupta404/kolam), [trishar/KolamGenerator](https://github.com/trishar/KolamGenerator), dozens of 2026 Smart India Hackathon repos |
| Apps | [iRangoli](https://apps.apple.com/mx/app/irangoli/id6757826534) (iOS), [Draw Kolam Rangoli](https://appgoblin.info/apps/com.draw.kolam.rangoli) (Android), [Braindots Kolam Studio](https://chrome-stats.com/d/com.braindots.kolamstudio) (Android): dot grids with snapping and symmetry brushes |

## Scanning and recognition

| What | Notes |
|---|---|
| KolamNet (ICVGIP 2022), [KolamNetV2](https://link.springer.com/10.1186/s40494-024-01167-8) (Heritage Science 2024) | Classifies kolam photos by type. Doesn't reconstruct the line |
| [rajdeep1022/Kolamify](https://github.com/rajdeep1022/Kolamify) | YOLOv8 dot detection, then YOLOv8 line segmentation, then ResNet classification. Close to scanning steps 2–3, but stops at labels: no traced, editable route. Server-based, so not offline |
| Datasets | [Roboflow](https://universe.roboflow.com/pragati/kolam-wlfzw) (CC BY 4.0), [Hugging Face](https://huggingface.co/datasets/sumit-06/kolam-text-to-image) |

Photo → dots + ordered line: nothing found. Still open.

## Formats and editors

| What | Notes |
|---|---|
| [nhtran93/kolam](https://github.com/nhtran93/kolam) | R, AGPL. **The only real kolam file format found**: a drawing is a sequence of gesture tokens (`o1 o3 o4 … c3`) plus a start position and heading (Waring's gesture lexicon). Field dataset from Kodaikanal 2009, used in [Entropy trade-offs in artistic design: Tamil kolam](https://pmc.ncbi.nlm.nih.gov/articles/PMC10427318). Drawing-order-first, like us |
| [Knotter](https://gitlab.com/mattia.basaglia/Knotter) | C++, GPL (moved to GitLab). Interactive Celtic-knot designer on *arbitrary* graphs, SVG export. Best UX reference for editing woven lines off a grid |
| Celtic knot generators | [BorisTheBrave/celtic-knot](https://github.com/BorisTheBrave/celtic-knot), [jamis/celtic_knot](https://github.com/jamis/celtic_knot) (knots from graphs), [Zhiyao-Yan/hanzi-knot](https://github.com/Zhiyao-Yan/hanzi-knot). The same mathematics, another tradition |
| `kolamstudio-master` | Already in `sources/Lusona_translated_Gerdes.zip`: open-source Java kolam editor (2015) |

## What we take from it

- **Don't build the mirror-curve generator from scratch.** Read kolam-maker's `js/kolam.js` and muggula-prastaram's core (both MIT) when we get there. It's an optional tool that writes ordinary paths.
- **Importers worth having:** gate bit strings (muggula, kolam-maker) and Tran's gesture sequences. The second also gives real field data to test the format on.
- **UX references:** kolam-maker (click a gate to change it), Knotter (editing on any graph).
- **Scanning:** Kolamify shows dot detection and line segmentation are feasible; the missing part is tracing into an ordered route, offline.
