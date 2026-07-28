<!-- MODIFIED IN THIS DERIVATIVE: backend persistence and neutral-QA rules were revised; see ../../../../NOTICE (Apache-2.0 section 4(b)). -->

# Figure contract before plotting

A scientific figure is a visual argument. Establish its claim, evidence, and
review risks before code or styling.

## Backend

Resolve Python or R from:

1. explicit user choice;
2. existing source files and project dependencies;
3. saved preference;
4. a recommendation when the user delegates the choice.

Ask only when both remain viable and the choice materially affects integration
or maintenance. Save a choice with `scripts/nature_figure_backend.py` only when
the user explicitly asks to make it the future default.

Keep drawing, layout semantics, and export in one source-of-truth backend.
Neutral image/PDF/SVG viewers and deterministic validators may inspect the
outputs; they must not redraw or alter presentation semantics. If the selected
runtime is missing, report the blocker and offer to install it or provide a
runnable selected-backend script; do not silently substitute a
different-looking figure.

## Data integrity

Use all supplied observations and variables unless an exclusion is scientifically
justified or requested. Preserve the source. Record before/after counts, rule,
and reason for every exclusion or aggregation. Large data should use an honest
backend-native representation, not silent subsampling for convenience.

## Contract

1. **Conclusion:** one sentence the figure must defend.
2. **Evidence chain:** each panel has one unique evidentiary role.
3. **Archetype:** quantitative grid, schematic-led composite, image plate plus
   quantification, or asymmetric mixed modality.
4. **Backend/source:** one source of truth for drawing, layout, and export;
   neutral tools may inspect the final files.
5. **Journal/export:** dimensions, formats, editable text, statistics, source
   data, accessibility, and image-integrity requirements.

The chart serves the scientific logic. Aesthetic polish and template matching
are subordinate to clarity, defensibility, and reviewability.
