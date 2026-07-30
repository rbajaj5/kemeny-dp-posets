import unittest
from random import Random

from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.mechanisms import exponential_kemeny, release_optimum_score
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

    def test_scalar_release_metadata(self):
        output = release_optimum_score(
            self.sensitivity,
            self.profile,
            epsilon=4.0,
            delta=0.2,
            rng=Random(7),
        )
        self.assertEqual(output.exact_value, 0)
        self.assertGreaterEqual(output.smooth_sensitivity, 0)
        self.assertGreaterEqual(output.noise_scale, 0)


if __name__ == "__main__":
    unittest.main()

