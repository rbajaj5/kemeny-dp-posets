import unittest
from fractions import Fraction

from kemeny_dp.core import RankingSpace
from kemeny_dp.law_hierarchy import (
    coordinatewise_leq,
    expected_profile,
    invert_upper_set_probabilities,
    upper_set_probabilities,
)
from kemeny_dp.poset import profiles_up_to


class LawHierarchyTests(unittest.TestCase):
    def setUp(self):
        self.space = RankingSpace.create(3)
        self.states = profiles_up_to(self.space, 3)

    def test_coordinatewise_order(self):
        self.assertTrue(
            coordinatewise_leq(
                (0, 1, 0, 0, 0, 0),
                (2, 1, 0, 0, 0, 0),
            )
        )
        self.assertFalse(
            coordinatewise_leq(
                (1, 1, 0, 0, 0, 0),
                (2, 0, 1, 0, 0, 0),
            )
        )
        with self.assertRaises(ValueError):
            coordinatewise_leq((0,), (0, 0))

    def test_full_upper_set_hierarchy_recovers_law_exactly(self):
        weights = {
            state: 1 + sum(
                (index + 1) * count
                for index, count in enumerate(state)
            )
            for state in self.states
        }
        total = sum(weights.values())
        mass = {
            state: Fraction(weight, total)
            for state, weight in weights.items()
        }

        hierarchy = upper_set_probabilities(self.states, mass)
        recovered = invert_upper_set_probabilities(
            self.states, hierarchy
        )
        self.assertEqual(recovered, mass)

    def test_first_moments_do_not_characterize_three_voter_law(self):
        middle = (1, 1, 1, 0, 0, 0)
        left = (2, 1, 0, 0, 0, 0)
        right = (0, 1, 2, 0, 0, 0)
        point_mass = {middle: Fraction(1)}
        mixture = {
            left: Fraction(1, 2),
            right: Fraction(1, 2),
        }

        self.assertEqual(
            expected_profile(self.states, point_mass),
            expected_profile(self.states, mixture),
        )
        point_hierarchy = upper_set_probabilities(
            self.states, point_mass
        )
        mixture_hierarchy = upper_set_probabilities(
            self.states, mixture
        )
        self.assertNotEqual(point_hierarchy, mixture_hierarchy)
        self.assertEqual(point_hierarchy[left], 0)
        self.assertEqual(mixture_hierarchy[left], Fraction(1, 2))

    def test_inconsistent_hierarchy_inverts_to_signed_mass(self):
        hierarchy = {
            state: Fraction(0) for state in self.states
        }
        zero = self.space.empty_profile()
        child = (1, 0, 0, 0, 0, 0)
        hierarchy[zero] = Fraction(1)
        hierarchy[child] = Fraction(2)

        recovered = invert_upper_set_probabilities(
            self.states, hierarchy
        )
        self.assertTrue(any(value < 0 for value in recovered.values()))


if __name__ == "__main__":
    unittest.main()
