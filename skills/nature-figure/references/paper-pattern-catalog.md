<!-- New in this derivative: faithful real-paper gallery and execution registry; provenance is recorded in ../../../NOTICE. -->

# Faithful real-paper Python gallery

Load this reference after selecting Python when a task would benefit from a
real, paper-specific visual precedent. These examples are not a single house
theme. Preserve each example's composition, palette, typography, line weight,
legend placement, annotations, canvas, and export settings unless the user asks
for a redesign.

The immutable visual baselines live under `assets/paper-patterns/`; the curated
plotting sources live under `scripts/paper_examples/`. They are separated so an
agent can inspect an image before loading code. `assets/paper-patterns/manifest.json`
records the source revision, paths, dimensions, DPI metadata, and SHA-256 values.

## Choose from the full gallery

| Project | Preserved outputs | Source entry points | Visual strengths | Extra runtime needs | Status |
|---|---:|---:|---|---|---|
| Brainteaser | 5 PNG | 5 | dense 2×4 grids, direct values, color+hatch composition, legend-only axes | — | faithful baseline |
| CellSpliceNet | 3 PNG | 2 | wide comparison bars, uncertainty, large labels, annotated ablation | — | faithful baseline |
| Cflows | 4 upstream PNG + 3 PDF + 1 optimized PNG | 4 | diffusion/manifold graph, ultra-wide scientific comparison bars | SciPy for Swiss roll | deterministic Swiss-roll variant added; upstream golden retained |
| Dispersion | 2 PNG | 2 | shaded spheres, 2D/3D geometric mechanisms, arrows and custom camera | LaTeX | faithful baseline |
| ImmunoStruct | 4 PNG | 1 renderer + local data | 600 dpi benchmark grids, tight y ranges, direct method hierarchy | — | neutral `uncertainty` naming; values unchanged |
| ophthal review | 2 upstream PNG + 1 optimized PNG | 2 | annotated heatmap, cumulative event timeline | seaborn, python-dateutil, LaTeX | same-month events and GPT-4v date fixed; localized visual QA passed |
| RNAGenScape | 5 PNG | 4 | manifolds, column-specific metric matrix, relative summary, parameter sweep | LaTeX for comparison/sweep | relative denominator needs review before adaptation |
| VIGIL | 4 upstream PNG + 1 optimized PNG | 4 | radar, gradient line, ablation curves, probability/manifold concept panel | SciPy for concept | duplicate ablation curve removed; radar semantics unchanged |

The 29 Python-rendered PNGs and 3 companion PDFs are under
`assets/paper-patterns/python/<project>/`. Ten additional paper composites that
were only partly produced in Python are retained under
`assets/paper-patterns/hybrid/`; use them as visual references, not as claims of
end-to-end Python reproducibility. User-approved variants live separately under
`assets/paper-patterns/optimized/`; the upstream images are never overwritten.

## Inspect before adapting

1. Open the closest original output at final reading size.
2. Open only its registered source under `scripts/paper_examples/<project>/`.
3. Record the visual invariants that carry the paper's identity: canvas and
   panel geometry, palette/hatch/alpha roles, typography, axes, camera, drawing
   order, annotations, legend placement, and save parameters.
4. Adapt data and labels inside that project-specific renderer. Do not pass the
   example through a shared analytical style or turn it into a uniform grid.
5. Render in an isolated process, compare with the golden output, and inspect
   any difference. Never update a golden merely because a test failed.

List or render a preserved entry point:

```bash
python3 "$SKILL_DIR/scripts/render_paper_example.py" --list
python3 "$SKILL_DIR/scripts/render_paper_example.py" \
  brainteaser-brute-force --output-dir figures/reference-run
```

The runner creates a clean temporary working directory, preserves the source
script's own Matplotlib settings and save calls, and copies only the registered
outputs. It refuses to overwrite files unless `--force` is explicit, and it
refuses to silently substitute a fallback font when a source requires
Helvetica. Install the recorded font and other runtime dependencies before
using a rerender as a fidelity candidate.

Verify the immutable gallery or compare one rerender:

```bash
python3 "$SKILL_DIR/scripts/check_paper_gallery.py"
python3 "$SKILL_DIR/scripts/compare_paper_figure.py" \
  GOLDEN.png RERENDERED.png --require-exact \
  --diff-output qa/diff.png --overlay-output qa/overlay.png
```

Pixel identity is the target when the environment is fixed. Fonts, LaTeX,
Matplotlib, rasterizer, and PDF renderer versions can create environmental
differences; treat a non-exact result as a review item, not permission to
accept a redesigned figure.

`compare_paper_figure.py` compares raster images. The PNGs are executable exact
pixel-regression targets; the three PDFs are protected byte-for-byte by the
manifest hash. For a visual PDF regression, rasterize the golden and candidate
with the same pinned PDF renderer and DPI, then compare those rasters. Do not
claim PDF visual identity from the manifest hash alone.

## Refactoring boundary

Safe first changes are execution isolation, path handling outside the plotting
body, dependency checks, output registration, manifest verification, and
closing figures. Extract a helper only when its call order and arguments remain
identical. Keep paper-specific style constants and layout logic local.

Do not initially centralize or normalize:

- palettes, hatch patterns, alpha values, font sizes, line widths, or rcParams;
- figure size, GridSpec gaps, legend-only panels, label padding, ticks, limits,
  or manual axes repositioning;
- 3D camera/light/mesh settings, KDE grids, path effects, or drawing order;
- `tight_layout`, `subplots_adjust`, `bbox_inches`, `pad_inches`, DPI, or format;
- hard-coded paper data that is necessary to reproduce the preserved output.

The pre-existing CSV-driven volcano, ROC, dot-plot, marginal, and paired
commands remain separate analytical utilities for new data contracts. They are
not substitutes for this gallery and are not fidelity references.

## Curated optimizations

The upstream golden images remain immutable. The user approved these narrow
source changes:

- `ophthal-trend`: represent events as ordered pairs so both Bard and LlaMA 1
  survive the shared `2023-02` date, stagger Bard vertically above LlaMA 1, and
  normalize GPT-4v to `2023-09`. Two independent LaTeX/`helvet` renders are
  pixel-identical; in the controlled upstream/current A/B, all 5,063 changed
  pixels lie inside the two expected annotation regions. The manifest records
  the controlled upstream-source rerender hash separately because
  `baseline_path` remains the immutable upstream golden rather than the
  same-environment verification raster. The approved render is under
  `assets/paper-patterns/optimized/ophthal-review/`.
- `cflows-diffusion-swiss-roll`: use `RandomState(42)`, create the output
  directory, and replace repeated `np.where` calls with one inverse permutation.
  Two independent renders are pixel-identical, and the refactored algorithm is
  pixel-identical to the upstream algorithm when both use seed 42. The approved
  render is under `assets/paper-patterns/optimized/cflows/`.
- `vigil-ablation`: remove the duplicate MathVista `plot` call. A controlled
  same-environment A/B changes 0.1479% of full-image pixels; most changed pixels
  remove the duplicate legend row, while the curve itself only loses the slight
  darkening caused by drawing antialiased edges twice. The approved candidate is
  under `assets/paper-patterns/optimized/vigil/`; its manifest records the exact
  Matplotlib/FreeType and font-fallback environment used for pixel regression.
- `immunostruct-bars`: rename `std` to neutral `uncertainty` without changing
  any array value or the existing Mean PPVn `/sqrt(5)` operation. All four A/B
  renders are pixel-identical; do not infer SD or SEM without experiment data.

## Remaining review items

Keep these original images and sources unchanged until a user approves a
scientific-policy change:

- `vigil-radar`: heterogeneous spokes use mean filling and clipping; verify the
  scientific meaning before applying that policy to new data.
- `rnagenscape-comparison`: confirm relative-percentage semantics when a
  baseline can be negative.

For any future visual or semantic repair, retain the original golden, render a
named candidate variant, and show the original, candidate, and difference.

## Integrated source-skill guidance

The source repository's `scientific-figure-making` skill is not treated as a
separate nested skill. Its useful guidance is organized into this skill's
existing progressive-disclosure references: `design-theory.md`, `api.md`,
`common-patterns.md`, `tutorials.md`, and `demos.md`. The 24 registered plotting
entry points remain the executable high-fidelity examples; documentation
snippets do not replace them.
