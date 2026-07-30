import unittest

from kemeny_dp.core import KemenyAnalyzer, RankingSpace, kendall_distance
from kemeny_dp.poset import children, hasse_distance, parents, profiles_of_size


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.space = RankingSpace.create(3)
        self.kemeny = KemenyAnalyzer(self.space)

    def test_kendall_metric(self):
        abc = (0, 1, 2)
        acb = (0, 2, 1)
        cba = (2, 1, 0)
        self.assertEqual(kendall_distance(abc, abc), 0)
        self.assertEqual(kendall_distance(abc, acb), 1)
        self.assertEqual(kendall_distance(abc, cba), 3)
        self.assertEqual(
            kendall_distance(abc, cba), kendall_distance(cba, abc)
        )

    def test_unanimous_optimum(self):
        profile = self.space.profile_from_ballots([(0, 1, 2)] * 5)
        self.assertEqual(self.kemeny.optimum_value(profile), 0)
        self.assertEqual(self.kemeny.optima(profile), ((0, 1, 2),))

    def test_cover_graph(self):
        profile = self.space.profile_from_ballots([(0, 1, 2), (2, 1, 0)])
        self.assertEqual(len(parents(profile)), 2)
        self.assertEqual(len(children(profile)), 6)
        empty = self.space.empty_profile()
        self.assertEqual(hasse_distance(empty, profile), 2)

    def test_profile_layer_size(self):
        # Six rankings; weak compositions of two into six parts.
        self.assertEqual(len(profiles_of_size(self.space, 2)), 21)


if __name__ == "__main__":
    unittest.main()

