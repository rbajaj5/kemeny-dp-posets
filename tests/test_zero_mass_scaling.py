import unittest
from fractions import Fraction

from kemeny_dp.zero_mass_scaling import (
    zero_mass_finite_stage,
    zero_mass_scaling_audit,
)


class ZeroMassScalingTests(unittest.TestCase):
    def test_source_formulas_hold_exactly(self):
        for stage in range(1, 25):
            result = zero_mass_finite_stage(stage)
            self.assertEqual(result.map_degree, 4**stage)
            self.assertEqual(
                result.potential_scale,
                Fraction(1, 2**stage),
            )
            self.assertEqual(
                result.lelong_number,
                Fraction(1, 2**stage),
            )
            self.assertEqual(
                result.normalized_monge_ampere_mass,
                Fraction(1),
            )
            self.assertEqual(result.mass_to_lelong_ratio, 2**stage)
            self.assertEqual(result.cutoff_depth, 4**stage)

    def test_lelong_numbers_strictly_decrease_while_mass_stays_one(self):
        stages = zero_mass_scaling_audit(20)
        self.assertTrue(
            all(
                left.lelong_number > right.lelong_number
                for left, right in zip(stages, stages[1:])
            )
        )
        self.assertEqual(
            {stage.normalized_monge_ampere_mass for stage in stages},
            {Fraction(1)},
        )

    def test_stage_validation(self):
        for invalid in (0, -1, 1.5, True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    zero_mass_finite_stage(invalid)
                with self.assertRaises(ValueError):
                    zero_mass_scaling_audit(invalid)


if __name__ == "__main__":
    unittest.main()
