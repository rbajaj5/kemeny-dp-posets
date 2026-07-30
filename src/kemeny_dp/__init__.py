"""Small-instance laboratory for private Kemeny aggregation."""

from .breakdown import (
    BreakdownComparison,
    compare_cover_radius_and_breakdown,
)
from .core import KemenyAnalyzer, RankingSpace, kendall_distance
from .geometry import (
    pairwise_sign_vector,
    project_vector,
    rademacher_projection,
    squared_euclidean,
)
from .finite_sample import BernoulliSummary, bernoulli_summary
from .hex_y import (
    TriangularYBoard,
    binary_winner_smooth_sensitivity,
    exact_pivotality,
    exact_winner_radii,
    majority_circuit_gate_count,
)
from .law_hierarchy import (
    coordinatewise_leq,
    expected_profile,
    invert_upper_set_probabilities,
    upper_set_probabilities,
    validate_probability_mass,
)
from .mechanisms import (
    exponential_kemeny,
    exponential_kemeny_probabilities,
    release_optimum_score,
)
from .sample_aggregate import (
    center_of_attention,
    exact_block_outputs,
    sample_and_center,
)
from .sensitivity import SensitivityAnalyzer, SmoothSensitivityResult
from .subset_dp import SubsetDPResult, exact_kemeny_subset_dp

__all__ = [
    "BreakdownComparison",
    "KemenyAnalyzer",
    "BernoulliSummary",
    "RankingSpace",
    "SensitivityAnalyzer",
    "SmoothSensitivityResult",
    "SubsetDPResult",
    "TriangularYBoard",
    "binary_winner_smooth_sensitivity",
    "center_of_attention",
    "bernoulli_summary",
    "compare_cover_radius_and_breakdown",
    "coordinatewise_leq",
    "expected_profile",
    "exact_block_outputs",
    "exact_kemeny_subset_dp",
    "exact_pivotality",
    "exact_winner_radii",
    "majority_circuit_gate_count",
    "invert_upper_set_probabilities",
    "exponential_kemeny",
    "exponential_kemeny_probabilities",
    "kendall_distance",
    "pairwise_sign_vector",
    "project_vector",
    "rademacher_projection",
    "release_optimum_score",
    "sample_and_center",
    "squared_euclidean",
    "upper_set_probabilities",
    "validate_probability_mass",
]
