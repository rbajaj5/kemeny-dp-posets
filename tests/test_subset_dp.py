import unittest
from itertools import combinations_with_replacement
from random import Random

from kemeny_dp.core import KemenyAnalyzer, RankingSpace, kendall_distance
from kemeny_dp.sensitivity import SensitivityAnalyzer
from kemeny_dp.subset_dp import (
    exact_kemeny_stability_subset_dp,
    exact_kemeny_subset_dp,
)


class SubsetDPTests(unittest.TestCase):
    def test_matches_factorial_enumeration(self):
        space = RankingSpace.create(4)
        kemeny = KemenyAnalyzer(space)
        rng = Random(20260730)
        for _ in range(30):
            ballots = tuple(rng.choice(space.rankings) for _ in range(3))
            profile = space.profile_from_ballots(ballots)
            result = exact_kemeny_subset_dp(ballots)
            optimum_cost, optima = kemeny.optimum(profile)
            self.assertEqual(result.optimum_cost, optimum_cost)
            self.assertEqual(result.selected_ranking, optima[0])
            self.assertEqual(result.optimum_count, len(optima))

    def test_unanimous_three_voter_profile(self):
        ballot = (2, 0, 3, 1)
        result = exact_kemeny_subset_dp((ballot, ballot, ballot))
        self.assertEqual(result.optimum_cost, 0)
        self.assertEqual(result.selected_ranking, ballot)
        self.assertEqual(result.optimum_count, 1)

    def test_stability_certificate_matches_factorial_enumeration(self):
        space = RankingSpace.create(4)
        kemeny = KemenyAnalyzer(space)
        sensitivity = SensitivityAnalyzer(kemeny)
        for ballot_indices in combinations_with_replacement(
            range(space.ranking_count), 3
        ):
            ballots = tuple(space.rankings[index] for index in ballot_indices)
            profile = space.profile_from_ballots(ballots)
            certificate = exact_kemeny_stability_subset_dp(ballots)
            selected = certificate.solution.selected_ranking
            competitor_scores = tuple(
                (kemeny.score(profile, ranking), ranking)
                for ranking in space.rankings
                if ranking != selected
            )

            self.assertEqual(
                certificate.second_cost,
                min(cost for cost, _ in competitor_scores),
            )
            self.assertEqual(
                certificate.second_cost,
                kemeny.score(profile, certificate.second_ranking),
            )
            self.assertEqual(
                certificate.second_score_gap,
                certificate.second_cost
                - certificate.solution.optimum_cost,
            )
            self.assertEqual(
                certificate.second_distance,
                kendall_distance(selected, certificate.second_ranking),
            )
            self.assertEqual(
                certificate.destabilizing_cost,
                kemeny.score(profile, certificate.destabilizing_ranking),
            )
            self.assertEqual(
                certificate.destabilizing_distance,
                kendall_distance(
                    selected, certificate.destabilizing_ranking
                ),
            )
            self.assertEqual(
                certificate.uniqueness_radius,
                sensitivity.uniqueness_radius(profile),
            )
            self.assertEqual(
                certificate.minimum_cost_by_distance[
                    certificate.destabilizing_distance
                ],
                certificate.destabilizing_cost,
            )
            self.assertLessEqual(
                certificate.destabilizing_score_gap
                - certificate.added_witness_copies
                * certificate.destabilizing_distance,
                0,
            )

            attacked_ballots = ballots + (
                certificate.destabilizing_ranking,
            ) * certificate.added_witness_copies
            attacked_profile = space.profile_from_ballots(attacked_ballots)
            self.assertNotEqual(kemeny.optima(attacked_profile), (selected,))

    def test_stability_certificate_rejects_single_candidate_space(self):
        with self.assertRaises(ValueError):
            exact_kemeny_stability_subset_dp(((0,),))

    def test_all_distance_layers_match_five_candidate_enumeration(self):
        space = RankingSpace.create(5)
        kemeny = KemenyAnalyzer(space)
        rng = Random(505)
        for _ in range(12):
            ballots = tuple(rng.choice(space.rankings) for _ in range(4))
            profile = space.profile_from_ballots(ballots)
            certificate = exact_kemeny_stability_subset_dp(ballots)
            selected = certificate.solution.selected_ranking
            expected: list[int | None] = [
                None
                for _ in range(space.diameter + 1)
            ]
            for ranking in space.rankings:
                distance = kendall_distance(selected, ranking)
                cost = kemeny.score(profile, ranking)
                current = expected[distance]
                if current is None or cost < current:
                    expected[distance] = cost
            self.assertEqual(
                certificate.minimum_cost_by_distance,
                tuple(expected),
            )

    def test_farther_larger_gap_competitor_can_destabilize_first(self):
        space = RankingSpace.create(3)
        by_label = {
            space.ranking_label(ranking): ranking
            for ranking in space.rankings
        }
        ballots = tuple(
            by_label[label]
            for label in ("ABC", "ABC", "ABC", "BCA", "CAB")
        )
        certificate = exact_kemeny_stability_subset_dp(ballots)
        self.assertEqual(
            certificate.minimum_cost_by_distance,
            (4, 7, 8, 11),
        )
        self.assertEqual(
            space.ranking_label(certificate.second_ranking), "ACB"
        )
        self.assertEqual(certificate.second_score_gap, 3)
        self.assertEqual(certificate.second_distance, 1)
        self.assertEqual(
            space.ranking_label(certificate.destabilizing_ranking), "BCA"
        )
        self.assertEqual(certificate.destabilizing_score_gap, 4)
        self.assertEqual(certificate.destabilizing_distance, 2)
        self.assertEqual(certificate.uniqueness_radius, 2)


if __name__ == "__main__":
    unittest.main()
