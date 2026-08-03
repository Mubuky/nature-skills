"""Registry for visually faithful figures4papers examples.

The plotting sources intentionally keep paper-specific style and layout.  This
registry provides the reusable execution boundary without routing them through
the shared analytical-style system.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaperExample:
    key: str
    project: str
    script: str
    outputs: tuple[str, ...]
    visual_family: str
    requirements: tuple[str, ...] = ("numpy", "matplotlib")
    font_family: str | None = "Helvetica"
    curation_notes: tuple[str, ...] = ()
    review_notes: tuple[str, ...] = ()
    visual_qa_pending: bool = False


EXAMPLES: tuple[PaperExample, ...] = (
    PaperExample("brainteaser-brute-force", "brainteaser", "brainteaser/plot_brute_force.py", ("brute_force.png",), "faceted stacked composition"),
    PaperExample("brainteaser-correctness-category", "brainteaser", "brainteaser/plot_correctness_by_category.py", ("correctness_by_category.png",), "categorical small multiples"),
    PaperExample("brainteaser-correctness-subcategory", "brainteaser", "brainteaser/plot_correctness_by_subcategory.py", ("correctness_by_subcategory.png",), "categorical small multiples"),
    PaperExample("brainteaser-rewriting", "brainteaser", "brainteaser/plot_rewriting.py", ("rewriting.png",), "faceted composition"),
    PaperExample("brainteaser-self-correction", "brainteaser", "brainteaser/plot_selfcorrection_math.py", ("selfcorrection_math.png",), "categorical small multiples"),
    PaperExample("cellsplicenet-ablation", "cellsplicenet", "cellsplicenet/plot_ablation.py", ("ablation.png",), "annotated ablation bars"),
    PaperExample("cellsplicenet-comparison", "cellsplicenet", "cellsplicenet/plot_comparison.py", ("comparison_worm.png", "comparison_human.png"), "multi-metric comparison bars"),
    PaperExample(
        "cflows-diffusion-swiss-roll",
        "cflows",
        "cflows/diffusion_swiss_roll.py",
        ("diffusion_swiss_roll.png",),
        "diffusion and manifold graph",
        requirements=("numpy", "matplotlib", "scipy"),
        font_family=None,
        curation_notes=(
            "Fixed RandomState seed 42 and replaced repeated index searches without changing draw order.",
            "The deterministic optimized output is stored separately from the unknown-seed upstream golden.",
        ),
    ),
    PaperExample("cflows-comparison-ablation", "cflows", "cflows/plot_comparison_Ablation.py", ("figX_comparison_Ablation.png", "figX_comparison_Ablation.pdf"), "ablation comparison bars"),
    PaperExample("cflows-comparison-gene-regulatory", "cflows", "cflows/plot_comparison_GeneRegulatory.py", ("fig2_comparison_GeneRegulatory.png", "fig2_comparison_GeneRegulatory.pdf"), "dataset comparison bars"),
    PaperExample("cflows-comparison-trajectory", "cflows", "cflows/plot_comparison_Trajectory.py", ("fig2_comparison_Trajectory.png", "fig2_comparison_Trajectory.pdf"), "trajectory comparison bars"),
    PaperExample("dispersion-idea", "dispersion", "dispersion/plot_idea.py", ("idea.png",), "shaded sphere concept", requirements=("numpy", "matplotlib", "latex"), font_family=None),
    PaperExample("dispersion-illustration", "dispersion", "dispersion/plot_illustration.py", ("illustration.png",), "2D and 3D geometric mechanism", requirements=("numpy", "matplotlib", "latex"), font_family=None),
    PaperExample(
        "immunostruct-bars",
        "immunostruct",
        "immunostruct/plot_bars.py",
        ("bars_comparison_IEDB.png", "bars_ablation_IEDB.png", "bars_comparison_Cancer.png", "bars_ablation_Cancer.png"),
        "wide benchmark and ablation bars",
        curation_notes=(
            "Renamed std to uncertainty without changing any value because the available source cannot establish SD or SEM.",
        ),
    ),
    PaperExample(
        "ophthal-composition",
        "ophthal-review",
        "ophthal_review/plot_composition.py",
        ("composition_heatmap.png",),
        "annotated review heatmap",
        requirements=("numpy", "matplotlib", "seaborn", "latex"),
        review_notes=("The source mutates stage labels in place; the first rendered output is retained unchanged.",),
    ),
    PaperExample(
        "ophthal-trend",
        "ophthal-review",
        "ophthal_review/plot_trend.py",
        ("trend_by_month.png",),
        "event-annotated cumulative timeline",
        requirements=("numpy", "matplotlib", "python-dateutil", "latex"),
        curation_notes=(
            "Preserve both 2023-02 events, stagger Bard vertically above LlaMA 1, and zero-pad 2023-09 so GPT-4v is annotated.",
            "The LaTeX/helvet optimized render is stored separately from the immutable upstream golden and passed localized pixel-difference QA.",
        ),
    ),
    PaperExample(
        "rnagenscape-comparison",
        "rnagenscape",
        "rnagenscape/plot_comparison.py",
        ("results_comparison_speed.png", "results_comparison_optimization.png"),
        "heatmap-like metric comparison",
        requirements=("numpy", "matplotlib", "latex"),
        review_notes=("A relative-percentage summary may use negative quantities; confirm the denominator semantics before adapting it.",),
    ),
    PaperExample("rnagenscape-hole-manifold", "rnagenscape", "rnagenscape/plot_hole_manifold.py", ("manifold_holes.png",), "3D manifold variants", font_family=None),
    PaperExample("rnagenscape-manifold", "rnagenscape", "rnagenscape/plot_manifold.py", ("manifold.png",), "3D manifold", font_family=None),
    PaperExample("rnagenscape-sweep", "rnagenscape", "rnagenscape/plot_sweep.py", ("results_sweep.png",), "parameter sweep", requirements=("numpy", "matplotlib", "latex")),
    PaperExample(
        "vigil-ablation",
        "vigil",
        "vigil/plot_ablation.py",
        ("ablation_curves.png",),
        "annotated ablation curves",
        curation_notes=(
            "Removed the duplicate MathVista plot call; this removes the repeated legend item and only slightly lightens antialiased line edges.",
        ),
    ),
    PaperExample(
        "vigil-radar",
        "vigil",
        "vigil/plot_comparison_radar.py",
        ("comparison_radar.png",),
        "radar comparison",
        review_notes=("Heterogeneous spokes use benchmark-specific normalization, mean filling, and clipping; verify the scientific comparison semantics before adapting it.",),
    ),
    PaperExample("vigil-concept", "vigil", "vigil/plot_concept.py", ("concept.png",), "probability and manifold concept", requirements=("numpy", "matplotlib", "scipy")),
    PaperExample("vigil-posttraining", "vigil", "vigil/plot_posttraining.py", ("comparison_posttraining.png",), "gradient line comparison"),
)


_BY_KEY = {example.key: example for example in EXAMPLES}


def get_example(key: str) -> PaperExample:
    try:
        return _BY_KEY[key]
    except KeyError as exc:
        choices = ", ".join(sorted(_BY_KEY))
        raise KeyError(f"unknown paper example {key!r}; choose one of: {choices}") from exc
