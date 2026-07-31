"""Reproduce the exact finite-stage scaling in Li-Xia's construction."""

from __future__ import annotations

import json
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from kemeny_dp.zero_mass_scaling import zero_mass_scaling_audit


ROOT = Path(__file__).resolve().parents[1]


def json_value(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_value(item) for item in value]
    return value


def main() -> None:
    stages = zero_mass_scaling_audit(20)
    result = {
        "status": {
            "finite_stage_scaling": "KNOWN_FORMULAS_EXACTLY_AUDITED",
            "plurisubharmonic_limit": "NOT_COMPUTATIONALLY_VERIFIED",
            "kemeny_privacy_or_bieberbach_claim": "NONE",
        },
        "source": {
            "title": "A counterexample to the zero-mass conjecture",
            "authors": ["Long Li", "Mingchen Xia"],
            "arxiv": "2607.26549",
            "url": "https://arxiv.org/abs/2607.26549",
        },
        "model": {
            "complex_dimension": 2,
            "stage_map_degree": "4^j",
            "potential_scale": "2^-j",
            "minimum_component_vanishing_order": 1,
            "normalized_mass_formula": "(2^-j)^2 4^j",
            "cutoff": "V_j = max(q_j, -4^j)",
        },
        "stages": [asdict(stage) for stage in stages],
        "checks": {
            "stages_checked": len(stages),
            "all_normalized_masses_equal_one": all(
                stage.normalized_monge_ampere_mass == 1
                for stage in stages
            ),
            "lelong_numbers_strictly_decrease": all(
                left.lelong_number > right.lelong_number
                for left, right in zip(stages, stages[1:])
            ),
            "last_stage_lelong_number": stages[-1].lelong_number,
            "last_stage_mass_to_lelong_ratio": (
                stages[-1].mass_to_lelong_ratio
            ),
        },
        "claim_boundary": (
            "The arithmetic verifies only Proposition 3.2's finite-stage "
            "degree normalization. The decreasing truncations, weak "
            "Monge-Ampere convergence, continuity, isolated pole, and zero "
            "Lelong number of the limit use the paper's analytic arguments."
        ),
    }
    output = ROOT / "results" / "zero_mass_scaling_audit.json"
    output.write_text(
        json.dumps(json_value(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(json_value(result["status"]), indent=2))
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
