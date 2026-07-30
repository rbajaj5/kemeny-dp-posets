"""Exhaustive three-candidate cover-poset experiment."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.poset import profiles_of_size
from kemeny_dp.sensitivity import SensitivityAnalyzer


def main() -> None:
    space = RankingSpace.create(3)
    kemeny = KemenyAnalyzer(space)
    sensitivity = SensitivityAnalyzer(kemeny)
    result_dir = ROOT / "results"
    result_dir.mkdir(exist_ok=True)

    rows: list[dict[str, object]] = []
    radius_counts: Counter[int] = Counter()
    local_opt_counts: Counter[int] = Counter()
    unique_count = 0

    for size in range(5):
        for profile in profiles_of_size(space, size):
            optimum_value, optima = kemeny.optimum(profile)
            radius = sensitivity.uniqueness_radius(profile)
            local_opt = sensitivity.local_sensitivity_optimum_value(profile)
            local_ranking = sensitivity.local_sensitivity_selected_ranking(profile)
            if len(optima) == 1:
                unique_count += 1
            radius_counts[radius] += 1
            local_opt_counts[local_opt] += 1
            rows.append(
                {
                    "profile_size": size,
                    "profile_counts": " ".join(map(str, profile)),
                    "profile": space.profile_label(profile),
                    "optimum_value": optimum_value,
                    "optimum_count": len(optima),
                    "selected_optimum": space.ranking_label(optima[0]),
                    "uniqueness_radius": radius,
                    "local_sensitivity_optimum": local_opt,
                    "local_sensitivity_selected_ranking": local_ranking,
                    "smooth_ranking_bound_beta_0_7": (
                        sensitivity.smooth_upper_bound_selected_ranking(
                            profile, 0.7
                        )
                    ),
                }
            )

    csv_path = result_dir / "exhaustive_m3_n0_to_4.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    selected_profiles = {
        "unanimous_3": space.profile_from_ballots([(0, 1, 2)] * 3),
        "polarized_2": space.profile_from_ballots(
            [(0, 1, 2), (2, 1, 0)]
        ),
        "cyclic_3": space.profile_from_ballots(
            [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
        ),
    }
    smooth_examples = {}
    for name, profile in selected_profiles.items():
        smooth = sensitivity.exact_smooth_sensitivity_optimum_value(
            profile, beta=0.7
        )
        smooth_examples[name] = {
            "profile": space.profile_label(profile),
            "local_sensitivity_optimum_score": (
                sensitivity.local_sensitivity_optimum_value(profile)
            ),
            "smooth_sensitivity_beta_0_7": smooth.value,
            "selected_ranking_uniqueness_radius": (
                sensitivity.uniqueness_radius(profile)
            ),
            "local_sensitivity_selected_ranking": (
                sensitivity.local_sensitivity_selected_ranking(profile)
            ),
            "smooth_upper_selected_ranking_beta_0_7": (
                sensitivity.smooth_upper_bound_selected_ranking(profile, 0.7)
            ),
            "explored_radius": smooth.explored_radius,
            "profiles_examined": smooth.profiles_examined,
        }

    summary = {
        "candidate_count": 3,
        "maximum_profile_size": 4,
        "profile_count": len(rows),
        "unique_optimum_profiles": unique_count,
        "uniqueness_radius_histogram": dict(sorted(radius_counts.items())),
        "local_optimum_sensitivity_histogram": dict(
            sorted(local_opt_counts.items())
        ),
        "smooth_examples": smooth_examples,
    }
    summary_path = result_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
