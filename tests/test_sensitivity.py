import math
import unittest

from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.poset import children, profiles_of_size
from kemeny_dp.sensitivity import SensitivityAnalyzer


class SensitivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.space = RankingSpace.create(3)
        cls.kemeny = KemenyAnalyzer(cls.space)
        cls.sensitivity = SensitivityAnalyzer(cls.kemeny)

    def test_optimum_global_sensitivity_bound(self):
        diameter = self.space.diameter
        for size in range(5):
            for profile in profiles_of_size(self.space, size):
                neighbor_value = (
                    self.sensitivity.local_sensitivity_optimum_value(profile)
                )
                gap_value = (
                    self.sensitivity.local_sensitivity_optimum_value_from_gaps(
                        profile
                    )
                )
                self.assertEqual(neighbor_value, gap_value)
                self.assertLessEqual(neighbor_value, diameter)

    def test_uniqueness_radius_matches_bfs(self):
        for size in range(5):
            for profile in profiles_of_size(self.space, size):
                if len(self.kemeny.optima(profile)) != 1:
                    continue
                closed_form = self.sensitivity.uniqueness_radius(profile)
                brute_force = (
                    self.sensitivity.brute_force_distance_to_loss_of_uniqueness(
                        profile, max_radius=8
                    )
                )
                self.assertEqual(closed_form, brute_force)

    def test_radius_bound_is_beta_smooth_on_covers(self):
        beta = 0.7
        for size in range(5):
            for profile in profiles_of_size(self.space, size):
                bound = self.sensitivity.smooth_upper_bound_selected_ranking(
                    profile, beta
                )
                self.assertGreaterEqual(
                    bound + 1e-12,
                    self.sensitivity.local_sensitivity_selected_ranking(profile),
                )
                for child in children(profile):
                    child_bound = (
                        self.sensitivity.smooth_upper_bound_selected_ranking(
                            child, beta
                        )
                    )
                    self.assertLessEqual(bound, math.exp(beta) * child_bound + 1e-12)
                    self.assertLessEqual(child_bound, math.exp(beta) * bound + 1e-12)

    def test_exact_scalar_smooth_sensitivity(self):
        profile = self.space.profile_from_ballots([(0, 1, 2)] * 3)
        beta = 0.8
        result = (
            self.sensitivity.exact_smooth_sensitivity_optimum_value(
                profile, beta
            )
        )
        self.assertGreaterEqual(
            result.value,
            self.sensitivity.local_sensitivity_optimum_value(profile),
        )
        self.assertLessEqual(result.unseen_tail_bound, result.value)

    def test_four_candidate_unanimous_radius(self):
        space = RankingSpace.create(4)
        kemeny = KemenyAnalyzer(space)
        sensitivity = SensitivityAnalyzer(kemeny)
        profile = space.profile_from_ballots([(0, 1, 2, 3)] * 4)
        self.assertEqual(sensitivity.uniqueness_radius(profile), 4)

    def test_three_voter_radius_dichotomy(self):
        space = RankingSpace.create(4)
        kemeny = KemenyAnalyzer(space)
        sensitivity = SensitivityAnalyzer(kemeny)
        observed_radii = set()
        for profile in profiles_of_size(space, 3):
            if len(kemeny.optima(profile)) != 1:
                continue
            radius = sensitivity.uniqueness_radius(profile)
            is_unanimous = 3 in profile
            self.assertEqual(radius, 3 if is_unanimous else 1)
            observed_radii.add(radius)
        self.assertEqual(observed_radii, {1, 3})

    def test_nonunanimous_radius_is_at_most_n_minus_two(self):
        for size in (3, 4):
            for profile in profiles_of_size(self.space, size):
                if size in profile:
                    continue
                if len(self.kemeny.optima(profile)) != 1:
                    continue
                self.assertLessEqual(
                    self.sensitivity.uniqueness_radius(profile), size - 2
                )


if __name__ == "__main__":
    unittest.main()
