import unittest
from fractions import Fraction

from kemeny_dp.oracle_eval import (
    aggregate_oracle_traces,
    evaluate_oracle_trace,
    oracle_match_flags,
)


class OracleEvaluationTests(unittest.TestCase):
    def test_match_flags_respect_unlabeled_plies(self):
        self.assertEqual(
            oracle_match_flags(
                ("a", "x", "c"),
                ({"a", "b"}, None, {"d"}),
            ),
            (True, None, False),
        )

    def test_trace_metrics_filter_unlabeled_but_keep_raw_failure_ply(self):
        metrics = evaluate_oracle_trace(
            (True, None, True, False, None, True, True)
        )
        self.assertEqual(metrics.total_plies, 7)
        self.assertEqual(metrics.labeled_plies, 5)
        self.assertEqual(metrics.matches, 4)
        self.assertEqual(metrics.match_rate, Fraction(4, 5))
        self.assertEqual(metrics.longest_consistent_chain, 2)
        self.assertEqual(metrics.first_failure_ply, 3)
        self.assertFalse(metrics.perfect)

    def test_unlabeled_trace_is_not_declared_perfect(self):
        metrics = evaluate_oracle_trace((None, None))
        self.assertIsNone(metrics.match_rate)
        self.assertIsNone(metrics.longest_consistent_chain)
        self.assertIsNone(metrics.first_failure_ply)
        self.assertIsNone(metrics.perfect)

    def test_aggregate_metrics_use_explicit_denominators(self):
        metrics = aggregate_oracle_traces(
            (
                (True, None, True),
                (True, False, True),
                (None,),
            )
        )
        self.assertEqual(metrics.traces, 3)
        self.assertEqual(metrics.eligible_traces, 2)
        self.assertEqual(metrics.perfect_rate, Fraction(1, 2))
        self.assertEqual(metrics.pooled_match_rate, Fraction(4, 5))
        self.assertEqual(
            metrics.mean_longest_consistent_chain, Fraction(3, 2)
        )
        self.assertEqual(metrics.imperfect_traces, 1)
        self.assertEqual(metrics.mean_first_failure_ply, Fraction(1))

    def test_validation(self):
        with self.assertRaises(ValueError):
            oracle_match_flags(("a",), ())
        with self.assertRaises(ValueError):
            oracle_match_flags(("a",), (set(),))
        with self.assertRaises(ValueError):
            evaluate_oracle_trace((True, 1))


if __name__ == "__main__":
    unittest.main()
