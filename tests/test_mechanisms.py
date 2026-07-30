import math
import unittest
from math import log
from random import Random

from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.mechanisms import (
    exponential_kemeny,
    exponential_kemeny_probabilities,
    release_optimum_score,
)
from kemeny_dp.poset import neighbors, profiles_of_size
from kemeny_dp.sensitivity import SensitivityAnalyzer


class MechanismTests(unittest.TestCase):
    def setUp(self):
        self.space = RankingSpace.create(3)
        self.kemeny = KemenyAnalyzer(self.space)
        self.sensitivity = SensitivityAnalyzer(self.kemeny)
        self.profile = self.space.profile_from_ballots([(0, 1, 2)] * 3)

    def test_exponential_mechanism_returns_ranking(self):
        output = exponential_kemeny(
            self.kemeny, self.profile, 1.0, rng=Random(7)
        )
        self.assertIn(output, self.space.rankings)

    def test_exponential_distribution_is_normalized(self):
        probabilities = exponential_kemeny_probabilities(
            self.kemeny, self.profile, 1.0
        )
        self.assertAlmostEqual(sum(probabilities), 1.0)
        self.assertTrue(all(probability > 0 for probability in probabilities))

    def test_exponential_mechanism_privacy_on_three_voter_profiles(self):
        epsilon = 1.3
        privacy_factor = math.exp(epsilon)
        for profile in profiles_of_size(self.space, 3):
            distribution = exponential_kemeny_probabilities(
                self.kemeny, profile, epsilon
            )
            for adjacent in neighbors(profile):
                adjacent_distribution = exponential_kemeny_probabilities(
                    self.kemeny, adjacent, epsilon
                )
                for probability, adjacent_probability in zip(
                    distribution, adjacent_distribution
                ):
                    self.assertLessEqual(
                        probability,
                        privacy_factor * adjacent_probability + 1e-12,
                    )

    def test_scalar_release_metadata(self):
        output = release_optimum_score(
            self.sensitivity,
            self.profile,
            epsilon=4.0,
            delta=0.2,
            rng=Random(7),
        )
        self.assertEqual(output.exact_value, 0)
        self.assertAlmostEqual(output.beta, 4.0 / (2 * log(2 / 0.2)))
        self.assertGreaterEqual(output.smooth_sensitivity, 0)
        self.assertGreaterEqual(output.noise_scale, 0)


if __name__ == "__main__":
    unittest.main()
