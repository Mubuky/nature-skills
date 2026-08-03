<!-- MODIFIED IN THIS DERIVATIVE: persistence and neutral-QA rules were clarified; see ../../../NOTICE (Apache-2.0 section 4(b)). -->

# Backend selection

Prefer continuity with the user's project.

| Prefer R when | Prefer Python when |
|---|---|
| Existing R/RDS/Seurat/DESeq2 workflow | Existing Python/NumPy/Pandas/ML workflow |
| ggplot2, patchwork, ComplexHeatmap, ggtree, survival ecosystem | Custom low-level layout, image plates, overlays, simulation, Matplotlib ecosystem |
| Team-maintained R templates or downstream R analysis | Team-maintained notebooks/packages or downstream Python analysis |
| | A semantic match to a faithful bundled paper example or maintained analytical CSV template |

Both can produce publication-grade output. If either is equally suitable, use
the saved preference. If none exists and integration is unaffected, prefer
Python when a faithful example or maintained template matches; otherwise
recommend the simpler fit and proceed. A paper example keeps its own visual
settings and is not routed through a generic theme. Ask only when the choice has
a material tradeoff the user must decide.

Persist the selected backend only when the user explicitly asks to make it the
future default. Once chosen, keep plotting, layout decisions, preview
generation, and export in that backend. Neutral viewers and validators may
inspect its outputs. A second language may perform non-visual data preparation
when it does not change presentation semantics. Preserve the intermediate
source-data file and transformation record.

If dependencies are missing, state the exact blocker. Install with permission
or deliver the selected-backend source and instructions. Do not silently render
a substitute in another backend and claim equivalence.
