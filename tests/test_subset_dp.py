import unittest
from random import Random

from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.subset_dp import exact_kemeny_subset_dp


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


if __name__ == "__main__":
    unittest.main()
