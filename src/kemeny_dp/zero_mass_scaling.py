"""Exact arithmetic behind the finite stages of Li-Xia's construction."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class ZeroMassFiniteStage:
    """Degree and normalized local invariants at one finite stage.

    This records Proposition 3.2 of Li-Xia arXiv:2607.26549. It does not
    verify plurisubharmonicity, Monge-Ampere continuity, or the limiting
    counterexample.
    """

    stage: int
    map_degree: int
    potential_scale: Fraction
    minimum_component_vanishing_order: int
    lelong_number: Fraction
    normalized_monge_ampere_mass: Fraction
    mass_to_lelong_ratio: int
    cutoff_depth: int


def zero_mass_finite_stage(stage: int) -> ZeroMassFiniteStage:
    """Return the exact finite-stage scaling invariants in dimension two."""
    if isinstance(stage, bool) or not isinstance(stage, int) or stage < 1:
        raise ValueError("stage must be a positive integer")
    degree = 4**stage
    scale = Fraction(1, 2**stage)
    minimum_order = 1
    lelong_number = scale * minimum_order
    normalized_mass = scale**2 * degree
    return ZeroMassFiniteStage(
        stage=stage,
        map_degree=degree,
        potential_scale=scale,
        minimum_component_vanishing_order=minimum_order,
        lelong_number=lelong_number,
        normalized_monge_ampere_mass=normalized_mass,
        mass_to_lelong_ratio=int(normalized_mass / lelong_number),
        cutoff_depth=4**stage,
    )


def zero_mass_scaling_audit(
    max_stage: int,
) -> tuple[ZeroMassFiniteStage, ...]:
    """Return all exact finite stages from one through ``max_stage``."""
    if (
        isinstance(max_stage, bool)
        or not isinstance(max_stage, int)
        or max_stage < 1
    ):
        raise ValueError("max_stage must be a positive integer")
    return tuple(
        zero_mass_finite_stage(stage)
        for stage in range(1, max_stage + 1)
    )
