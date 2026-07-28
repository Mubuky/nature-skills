<!-- MODIFIED IN THIS DERIVATIVE: scientific-design guidance was rewritten; see ../../../NOTICE (Apache-2.0 section 4(b)). -->

# Scientific figure design

Use this reference for visual hierarchy, typography, color, composition, and
export decisions. Scientific validity and the figure contract remain primary.

## Start from the claim

A figure is a visual argument:

1. State the conclusion in one sentence.
2. Identify the minimum evidence needed to support it.
3. Give each panel one evidentiary job.
4. Order panels by the reader's reasoning path, not by experiment chronology.
5. Remove elements that neither identify evidence nor help interpretation.

The title/caption makes the claim; the panels expose evidence; annotations
explain only the inference the data support.

## Hierarchy and composition

- Give the most consequential evidence the most area and the clearest position.
- Use alignment, shared scales, and whitespace to show grouping.
- Keep comparison panels visually comparable: same plot area, axis logic,
  normalization, and encoding unless a difference is explicitly meaningful.
- Put legends close to the evidence or label series directly when that reduces
  eye travel.
- Avoid decorative depth, texture, or perspective when it changes apparent
  magnitude.
- A schematic should clarify variables, flow, or mechanism; it should not
  decorate an otherwise complete quantitative panel.

For multi-panel figures, test three reading distances:

- thumbnail: conclusion and hero panel remain apparent;
- final journal size: labels and encodings are readable;
- enlarged: data, uncertainty, and image details remain honest.

## Typography

Use one sans-serif family unless notation requires another. Build a small,
consistent hierarchy for panel labels, axes, ticks, annotations, legends, and
caption-adjacent labels. Measure at final physical size.

- Panel labels are easy to locate and do not compete with data.
- Axis labels include units and avoid unexplained abbreviations.
- Text is horizontal where practical.
- Mathematical symbols, gene/protein names, and capitalization follow the
  manuscript terminology ledger.
- Vector exports preserve editable text or embed fonts as required.

Do not enlarge a whole canvas merely to make tiny text look acceptable in a
preview; design at the target width.

## Color

Assign color by semantic role:

- one restrained accent for the focal method/group;
- neutrals for context and baselines;
- a second hue only when it encodes a distinct variable;
- sequential maps for ordered magnitude;
- diverging maps only around a meaningful midpoint;
- categorical maps for unordered classes.

Check color-vision robustness and grayscale whenever identity or ordering must
survive without color. Redundant encoding—shape, line style, direct label, or
position—is preferable for critical distinctions.

Do not use color to imply significance, causality, or quality that the analysis
does not establish.

## Quantitative graphics

- Show raw observations or distribution structure when sample size permits.
- Define error bars, intervals, box elements, `n`, tests, corrections, and
  comparison scope in the legend.
- Share axes only when the quantities and transformations are comparable.
- Start bar axes at zero unless a non-zero baseline is necessary and clearly
  marked; line/scatter ranges may follow the scientific question without
  exaggerating changes.
- Avoid dual axes unless the variables are genuinely coupled and the mapping is
  unambiguous.
- Preserve missing data and censored observations visibly.

Choose an encoding by task: position for precise comparison, length for ordered
magnitude, area only when area is the intended quantity, and color for support
rather than fine numeric reading.

## Images and spatial data

- Preserve aspect ratio, bit depth, and meaningful intensity relationships.
- State whether contrast is globally or locally adjusted.
- Use consistent display windows for comparisons unless a difference is
  disclosed.
- Include scale bars with units and verify calibration.
- Separate representative images from quantified summaries.
- Mark crops, composites, registration, pseudocolor, and reused controls.
- Keep original data and transformations auditable.

## Schematics and graphical abstracts

Treat a generated or manually composed schematic as an explanatory model, not
experimental evidence. Distinguish observed steps from hypothesized mechanisms.
Do not add unsupported molecular interactions, anatomical detail, logos, or
quantitative values. Use editable vector shapes for final author review when
possible.

## Export

Determine journal requirements before implementation:

- physical width and height;
- vector versus raster deliverables;
- raster resolution and color mode;
- font embedding/editability;
- line-weight and minimum-text constraints;
- transparency and clipping behavior;
- source-data and accessibility requirements.

Export from the source-of-truth backend, then inspect the actual PDF/SVG/TIFF at
final size. A successful save call is not visual QA.

## Final questions

- Can a reader state the conclusion without reading the manuscript?
- Can every panel be mapped to a claim and source?
- Are comparisons perceptually and statistically fair?
- Are uncertainty, sample size, transformations, and exclusions visible?
- Could color, scale, cropping, normalization, or annotation mislead?
- Does the final exported artifact, not just the interactive preview, pass?
