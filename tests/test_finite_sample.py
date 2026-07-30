import unittest

from kemeny_dp.finite_sample import bernoulli_summary


class FiniteSampleTests(unittest.TestCase):
    def test_balanced_rate(self):
        summary = bernoulli_summary(50, 100)
        self.assertEqual(summary.rate, 0.5)
        self.assertAlmostEqual(summary.standard_error, 0.05)
        self.assertLess(summary.wilson_95_lower, 0.5)
        self.assertGreater(summary.wilson_95_upper, 0.5)
        self.assertIsNotNone(
            summary.plugin_berry_esseen_ratio_without_constant
        )

    def test_boundary_rate(self):
        summary = bernoulli_summary(100, 100)
        self.assertEqual(summary.rate, 1.0)
        self.assertLess(summary.wilson_95_lower, 1.0)
        self.assertEqual(summary.wilson_95_upper, 1.0)
        self.assertIsNone(
            summary.plugin_berry_esseen_ratio_without_constant
        )

    def test_rejects_invalid_counts(self):
        with self.assertRaises(ValueError):
            bernoulli_summary(2, 1)


if __name__ == "__main__":
    unittest.main()
