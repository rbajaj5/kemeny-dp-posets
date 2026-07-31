"""Small-instance laboratory for private Kemeny aggregation."""

from .breakdown import (
    BreakdownComparison,
    compare_cover_radius_and_breakdown,
)
from .coordination import (
    binary_conventions,
    decoder_from_one_feedback,
    deterministic_binary_decoders,
    grounded_accuracy,
    grounded_bulb,
    inverse_decoder,
    memorized_button_guess,
    parity_guess,
    protocol_accuracy,
)
from .chomp import (
    chomp_grundy,
    chomp_moves,
    chomp_optimal_moves,
    chomp_successor,
    largest_bite_policy,
    lexicographic_oracle_policy,
    play_chomp,
    rectangular_chomp_state,
)
from .core import KemenyAnalyzer, RankingSpace, kendall_distance
from .geometry import (
    jl_sufficient_dimension,
    pairwise_sign_vector,
    project_vector,
    rademacher_projection,
    spherical_column_projection,
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
from .oracle_eval import (
    AggregateOracleMetrics,
    TraceOracleMetrics,
    aggregate_oracle_traces,
    evaluate_oracle_trace,
    oracle_match_flags,
)
from .sample_aggregate import (
    AttentionCertificate,
    borda_block_outputs,
    borda_ranking,
    center_of_attention,
    center_of_attention_certificate,
    exact_block_outputs,
    sample_and_center,
    two_ballot_kemeny,
    unrestricted_attention_certificate,
)
from .sensitivity import SensitivityAnalyzer, SmoothSensitivityResult
from .subset_dp import SubsetDPResult, exact_kemeny_subset_dp
from .zero_mass_scaling import (
    ZeroMassFiniteStage,
    zero_mass_finite_stage,
    zero_mass_scaling_audit,
)

__all__ = [
    "BreakdownComparison",
    "AggregateOracleMetrics",
    "AttentionCertificate",
    "KemenyAnalyzer",
    "BernoulliSummary",
    "RankingSpace",
    "SensitivityAnalyzer",
    "SmoothSensitivityResult",
    "SubsetDPResult",
    "TriangularYBoard",
    "TraceOracleMetrics",
    "ZeroMassFiniteStage",
    "aggregate_oracle_traces",
    "binary_winner_smooth_sensitivity",
    "binary_conventions",
    "chomp_grundy",
    "chomp_moves",
    "chomp_optimal_moves",
    "chomp_successor",
    "center_of_attention",
    "bernoulli_summary",
    "borda_block_outputs",
    "borda_ranking",
    "compare_cover_radius_and_breakdown",
    "center_of_attention_certificate",
    "coordinatewise_leq",
    "decoder_from_one_feedback",
    "deterministic_binary_decoders",
    "expected_profile",
    "evaluate_oracle_trace",
    "exact_block_outputs",
    "exact_kemeny_subset_dp",
    "exact_pivotality",
    "exact_winner_radii",
    "grounded_accuracy",
    "grounded_bulb",
    "majority_circuit_gate_count",
    "invert_upper_set_probabilities",
    "inverse_decoder",
    "jl_sufficient_dimension",
    "exponential_kemeny",
    "exponential_kemeny_probabilities",
    "kendall_distance",
    "largest_bite_policy",
    "lexicographic_oracle_policy",
    "memorized_button_guess",
    "pairwise_sign_vector",
    "parity_guess",
    "project_vector",
    "protocol_accuracy",
    "oracle_match_flags",
    "play_chomp",
    "rademacher_projection",
    "release_optimum_score",
    "rectangular_chomp_state",
    "sample_and_center",
    "spherical_column_projection",
    "squared_euclidean",
    "upper_set_probabilities",
    "two_ballot_kemeny",
    "unrestricted_attention_certificate",
    "validate_probability_mass",
    "zero_mass_finite_stage",
    "zero_mass_scaling_audit",
]
