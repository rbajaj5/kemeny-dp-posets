import unittest
from fractions import Fraction

from kemeny_dp.breakdown import compare_cover_radius_and_breakdown
from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.poset import profiles_of_size
from kemeny_dp.sensitivity import SensitivityAnalyzer


class BreakdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.space = RankingSpace.create(3)
        cls.kemeny = KemenyAnalyzer(cls.space)
        cls.sensitivity = SensitivityAnalyzer(cls.kemeny)

    def test_requires_nonempty_unique_profile(self):
        with self.assertRaises(ValueError):
            compare_cover_radius_and_breakdown(
                self.kemeny, self.space.empty_profile()
            )
        tied = self.space.profile_from_ballots(
            [(0, 1, 2), (2, 1, 0)]
        )
        with self.assertRaises(ValueError):
            compare_cover_radius_and_breakdown(self.kemeny, tied)

    def test_unanimous_profile_has_half_tv_breakdown(self):
        profile = self.space.profile_from_ballots([(0, 1, 2)] * 3)
        result = compare_cover_radius_and_breakdown(self.kemeny, profile)
        self.assertEqual(result.cover_radius, 3)
        self.assertEqual(result.normalized_margin, Fraction(1))
        self.assertEqual(
            result.exact_zero_plus_tv_breakdown, Fraction(1, 2)
        )
        self.assertTrue(result.goibert_sufficient_condition)
        self.assertTrue(result.half_margin_equality)

    def test_cover_identity_and_tv_lower_bound_exhaustively(self):
        condition_count = 0
        for size in range(1, 6):
            for profile in profiles_of_size(self.space, size):
                if len(self.kemeny.optima(profile)) != 1:
                    continue
                result = compare_cover_radius_and_breakdown(
                    self.kemeny, profile
                )
                self.assertEqual(
                    result.cover_radius,
                    self.sensitivity.uniqueness_radius(profile),
                )
                self.assertGreaterEqual(
                    result.exact_zero_plus_tv_breakdown,
                    result.normalized_margin / 2,
                )
                if result.goibert_sufficient_condition:
                    condition_count += 1
                    self.assertTrue(result.half_margin_equality)
                    self.assertEqual(
                        result.standard_tv_of_goibert_attack,
                        result.exact_zero_plus_tv_breakdown,
                    )
        self.assertGreater(condition_count, 0)

    def test_half_margin_equality_need_not_hold(self):
        space = RankingSpace.create(4)
        kemeny = KemenyAnalyzer(space)
        ballots = (
            (0, 1, 2, 3),
            (0, 1, 3, 2),
            (1, 0, 2, 3),
            (1, 0, 3, 2),
            (1, 2, 3, 0),
            (2, 1, 3, 0),
            (2, 3, 1, 0),
            (3, 0, 1, 2),
            (3, 0, 2, 1),
            (3, 2, 0, 1),
        )
        profile = space.profile_from_ballots(ballots)
        result = compare_cover_radius_and_breakdown(kemeny, profile)
        self.assertEqual(result.normalized_margin, Fraction(1, 15))
        self.assertEqual(
            result.exact_zero_plus_tv_breakdown, Fraction(1, 20)
        )
        self.assertFalse(result.goibert_sufficient_condition)
        self.assertFalse(result.half_margin_equality)


if __name__ == "__main__":
    unittest.main()
