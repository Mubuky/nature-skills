<!-- MODIFIED IN THIS DERIVATIVE: bundled asset routing was rewritten; see ../../../NOTICE (Apache-2.0 section 4(b)). -->

# Bundled figure examples

Use bundled assets as visual or structural references. Their byte-level
provenance is recorded in
[`assets/README.md`](../assets/README.md):

- `assets/chart-atlas/`: compact chart-family previews for choosing an encoding;
- `assets/gallery/`: synthetic multi-panel composition examples;
- `assets/paper-patterns/`: 42 original paper outputs and hybrid references,
  three approved optimized outputs, and 25 curated Python files
  under `scripts/paper_examples/`.

Select by evidence structure and intended visual argument, not superficial
resemblance. When a paper-specific example is selected, preserve its deliberate
composition and style while substituting only compatible user data, labels,
statistics, and journal requirements.

The complete curated Python gallery from `ChenLiu-1996/figures4papers` is
documented in `paper-pattern-catalog.md`. Inspect its original output before
loading the corresponding source. Use `render_paper_example.py` for isolated
faithful reruns and `compare_paper_figure.py` for regression review. The five
analytical commands in `plot_templates.py` are separate interfaces; never
substitute their demo values or visual style for a selected paper example. If a user
provides other external code or imagery, use `asset-adaptation.md` before
adapting it.
