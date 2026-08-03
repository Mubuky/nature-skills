<!-- MODIFIED IN THIS DERIVATIVE: single-backend scope now governs generation and layout while permitting neutral QA; see ../../../../../NOTICE (Apache-2.0 section 4(b)). -->

# Backend: Python (matplotlib / seaborn)

**Python generation rule.** When the user has selected Python, keep drawing,
layout semantics, preview generation, and export in Python. Do not call
R/ggplot2, ComplexHeatmap, patchwork, or an R graphics device to create a
fallback rendering or layout approximation. Neutral image/PDF/SVG viewers,
metadata inspectors, and the bundled validator may audit Python outputs. If
Python or required plotting packages are missing, stop before rendering and
report the missing dependency. You may still write the Python script, provide
install commands, or ask permission to install dependencies, but do not
cross-render the figure in R.

## Python quick-start for new figures

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",     # editable text in SVG
    "pdf.fonttype": 42,         # editable TrueType text in PDF
    "font.size": 7,             # journal-scale starting point; not a universal style
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.tiff", dpi=dpi, bbox_inches="tight")
```

Use `text.usetex = True` only when LaTeX is installed and math-rich labels are
required. This preset is only a starting point for a new figure. Never apply it
over a selected paper example: keep that example's original rcParams, canvas,
layout, and save settings.

## Going deeper

- `references/api.md` — Python PALETTE, helper function signatures, validation rules.
- `references/template-catalog.md` — validated CSV-driven volcano, ROC, dot-plot, marginal, and paired templates backed by `scripts/plot_templates.py`.
- `references/paper-pattern-catalog.md` — 8-project faithful gallery, original outputs, registered sources, dependencies, and visual-regression rules.
- `references/common-patterns.md` — hero panels, legend-only axes, dark image plates, asymmetric layouts.
- `references/chart-types.md` — radar, 3D sphere, fill_between, scatter patterns.
- `references/tutorials.md` — end-to-end walkthroughs for bars, trends, heatmaps.
- `references/demos.md` — bundled paper, chart-atlas, and gallery examples with provenance.
- `scripts/render_paper_example.py` — isolate and rerun one preserved paper-specific source without restyling it.
- `scripts/compare_paper_figure.py` — exact raster comparison plus optional difference and overlay diagnostics.
- `scripts/validate_figure.py` — dependency-free source preflight before rendering and visual QA.
<!-- Modified in the context-engineered edition; see repository NOTICE. -->
