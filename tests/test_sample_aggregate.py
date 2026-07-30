import unittest
from random import Random

from kemeny_dp.core import RankingSpace
from kemeny_dp.sample_aggregate import (
    center_of_attention,
    exact_block_outputs,
    sample_and_center,
)


class SampleAggregateTests(unittest.TestCase):
    def setUp(self):
        self.space = RankingSpace.create(3)
        self.abc = (0, 1, 2)
        self.acb = (0, 2, 1)
        self.cba = (2, 1, 0)

    def test_center_uses_concentrated_majority(self):
        points = [self.abc] * 4 + [self.cba]
        self.assertEqual(
            center_of_attention(self.space, points, step=1), self.abc
        )

    def test_center_is_an_input_point(self):
        points = [self.abc, self.acb, self.acb, self.cba, self.acb]
        result = center_of_attention(self.space, points, step=1)
        self.assertIn(result, points)

    def test_exact_two_ballot_blocks(self):
        ballots = [self.abc] * 4 + [self.cba] * 2
        outputs = exact_block_outputs(
            self.space, ballots, block_size=2, rng=Random(3)
        )
        self.assertEqual(len(outputs), 3)
        self.assertTrue(all(output in self.space.rankings for output in outputs))

    def test_sample_and_center(self):
        ballots = [self.abc] * 8 + [self.cba] * 2
        output = sample_and_center(
            self.space,
            ballots,
            block_size=2,
            step=1,
            rng=Random(4),
        )
        self.assertEqual(output, self.abc)

    def test_rejects_invalid_step(self):
        with self.assertRaises(ValueError):
            center_of_attention(self.space, [self.abc], step=1)


if __name__ == "__main__":
    unittest.main()
