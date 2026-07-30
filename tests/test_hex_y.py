import math
import unittest

from kemeny_dp.hex_y import (
    TriangularYBoard,
    binary_winner_smooth_sensitivity,
    exact_pivotality,
    exact_winner_radii,
    majority_circuit_gate_count,
)


class HexYTests(unittest.TestCase):
    def test_geometry(self):
        board = TriangularYBoard.create(4)
        self.assertEqual(board.cell_count, 10)
        self.assertEqual(set(board.cells), {
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1),
            (3, 0),
        })

    def test_majority_circuit_size(self):
        self.assertEqual(
            [majority_circuit_gate_count(n) for n in range(1, 6)],
            [0, 1, 4, 10, 20],
        )
        with self.assertRaises(ValueError):
            majority_circuit_gate_count(0)

    def test_side_one(self):
        board = TriangularYBoard.create(1)
        self.assertEqual(board.winner(0), 0)
        self.assertEqual(board.winner(1), 1)
        with self.assertRaises(ValueError):
            board.majority_reduce(0)

    def test_unique_winner_and_reduction_exhaustively_through_side_five(self):
        for n in range(1, 6):
            board = TriangularYBoard.create(n)
            reduced = TriangularYBoard.create(n - 1) if n > 1 else None
            for mask in range(1 << board.cell_count):
                winner = board.winner(mask)
                self.assertEqual(winner, board.reduce_to_one(mask))
                if reduced is not None:
                    reduced_mask = board.majority_reduce(mask)
                    self.assertEqual(winner, reduced.winner(reduced_mask))

    def test_color_complement_symmetry(self):
        board = TriangularYBoard.create(5)
        for mask in range(0, 1 << board.cell_count, 97):
            self.assertNotEqual(
                board.winner(mask),
                board.winner(board.full_mask ^ mask),
            )

    def test_exact_pivotality_side_one(self):
        average, per_cell = exact_pivotality(TriangularYBoard.create(1))
        self.assertEqual(average, 1.0)
        self.assertEqual(per_cell, (1.0,))

    def test_winner_radii_and_exact_smooth_sensitivity(self):
        board = TriangularYBoard.create(3)
        radii = exact_winner_radii(board)
        winners = tuple(board.winner(mask) for mask in range(1 << board.cell_count))
        local_sensitivities = tuple(
            int(any(
                winners[mask] != winners[mask ^ (1 << cell_index)]
                for cell_index in range(board.cell_count)
            ))
            for mask in range(1 << board.cell_count)
        )
        beta = 0.7
        for mask, radius in enumerate(radii):
            brute_force = max(
                math.exp(-beta * (mask ^ other).bit_count())
                * local_sensitivities[other]
                for other in range(1 << board.cell_count)
            )
            self.assertAlmostEqual(
                binary_winner_smooth_sensitivity(radius, beta),
                brute_force,
            )

    def test_smooth_sensitivity_input_validation(self):
        with self.assertRaises(ValueError):
            binary_winner_smooth_sensitivity(0, 1.0)
        with self.assertRaises(ValueError):
            binary_winner_smooth_sensitivity(1, -0.1)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            TriangularYBoard.create(0)
        board = TriangularYBoard.create(2)
        with self.assertRaises(ValueError):
            board.winner(-1)
        with self.assertRaises(ValueError):
            board.winner(1 << board.cell_count)
        with self.assertRaises(ValueError):
            board.has_y(0, 2)


if __name__ == "__main__":
    unittest.main()
