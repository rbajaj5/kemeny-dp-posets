import unittest

from kemeny_dp.chomp import (
    chomp_grundy,
    chomp_moves,
    chomp_optimal_moves,
    chomp_successor,
    largest_bite_policy,
    lexicographic_oracle_policy,
    play_chomp,
    rectangular_chomp_state,
)
from kemeny_dp.oracle_eval import evaluate_oracle_trace


class ChompTests(unittest.TestCase):
    def test_small_grundy_values(self):
        self.assertEqual(chomp_grundy((1,)), 0)
        self.assertEqual(chomp_grundy((2,)), 1)
        self.assertEqual(chomp_grundy((1, 1)), 1)
        self.assertNotEqual(chomp_grundy((2, 2)), 0)

    def test_diagonal_move_wins_two_by_two(self):
        self.assertEqual(chomp_successor((2, 2), (1, 1)), (2, 1))
        self.assertEqual(chomp_grundy((2, 1)), 0)
        self.assertIn((1, 1), chomp_optimal_moves((2, 2)))

    def test_every_labeled_oracle_move_reaches_zero_exhaustively(self):
        for rows in range(1, 5):
            for columns in range(1, 5):
                state = rectangular_chomp_state(rows, columns)
                for move in chomp_optimal_moves(state):
                    self.assertEqual(
                        chomp_grundy(chomp_successor(state, move)),
                        0,
                    )

    def test_oracle_self_play_is_perfect_on_labeled_turns(self):
        for rows in range(1, 5):
            for columns in range(1, 5):
                state = rectangular_chomp_state(rows, columns)
                winner, _, flags = play_chomp(
                    state,
                    lexicographic_oracle_policy,
                    lexicographic_oracle_policy,
                )
                metrics = evaluate_oracle_trace(flags)
                if chomp_grundy(state) == 0:
                    self.assertEqual(winner, 1)
                else:
                    self.assertEqual(winner, 0)
                if metrics.perfect is not None:
                    self.assertTrue(metrics.perfect)

    def test_largest_bite_policy_returns_safe_legal_move(self):
        state = (4, 4, 4)
        move = largest_bite_policy(state)
        self.assertIn(move, chomp_moves(state))
        self.assertNotEqual(move, (0, 0))

    def test_validation_and_illegal_policy(self):
        with self.assertRaises(ValueError):
            rectangular_chomp_state(0, 2)
        with self.assertRaises(ValueError):
            chomp_moves((1, 2))
        with self.assertRaises(ValueError):
            chomp_successor((2, 2), (0, 0))
        with self.assertRaises(ValueError):
            play_chomp((2,), lambda _: (0, 0), largest_bite_policy)


if __name__ == "__main__":
    unittest.main()
