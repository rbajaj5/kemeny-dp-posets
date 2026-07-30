import unittest
from itertools import combinations_with_replacement, permutations
from random import Random

from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.poset import profiles_of_size
from kemeny_dp.sample_aggregate import (
    borda_block_outputs,
    borda_ranking,
    center_of_attention,
    center_of_attention_certificate,
    exact_block_outputs,
    sample_and_center,
    two_ballot_kemeny,
    unrestricted_attention_certificate,
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

    def test_center_certificate_and_two_approximation_exhaustively(self):
        for point_count in range(2, 6):
            for indices in combinations_with_replacement(
                range(self.space.ranking_count), point_count
            ):
                points = tuple(self.space.rankings[index] for index in indices)
                for step in range(1, point_count):
                    if (point_count + step) // 2 + 1 > point_count:
                        continue
                    restricted = center_of_attention_certificate(
                        self.space, points, step=step
                    )
                    unrestricted = unrestricted_attention_certificate(
                        self.space, points, step=step
                    )
                    ranking_index = {
                        ranking: index
                        for index, ranking in enumerate(self.space.rankings)
                    }
                    independent_radii = {
                        candidate: sorted(
                            self.space.distances[ranking_index[candidate]][
                                ranking_index[point]
                            ]
                            for point in points
                        )[restricted.target_count - 1]
                        for candidate in set(points)
                    }
                    expected_radius = min(independent_radii.values())
                    self.assertEqual(restricted.radius, expected_radius)
                    self.assertEqual(
                        set(restricted.minimizers),
                        {
                            candidate
                            for candidate, radius in independent_radii.items()
                            if radius == expected_radius
                        },
                    )
                    self.assertIn(restricted.center, points)
                    self.assertGreaterEqual(
                        sum(
                            self.space.distances[
                                self.space.rankings.index(restricted.center)
                            ][self.space.rankings.index(point)]
                            <= restricted.radius
                            for point in points
                        ),
                        restricted.target_count,
                    )
                    self.assertLessEqual(
                        restricted.radius, 2 * unrestricted.radius
                    )

    def test_minimizer_set_is_candidate_relabeling_equivariant(self):
        points = (self.abc, self.acb, self.cba, self.acb)
        original = center_of_attention_certificate(self.space, points)
        for relabeling in permutations(range(self.space.candidate_count)):
            relabel = lambda ranking: tuple(
                relabeling[candidate] for candidate in ranking
            )
            transformed = center_of_attention_certificate(
                self.space, tuple(relabel(point) for point in points)
            )
            self.assertEqual(
                set(transformed.minimizers),
                {relabel(center) for center in original.minimizers},
            )

    def test_exact_two_ballot_blocks(self):
        ballots = [self.abc] * 4 + [self.cba] * 2
        outputs = exact_block_outputs(
            self.space, ballots, block_size=2, rng=Random(3)
        )
        self.assertEqual(len(outputs), 3)
        self.assertTrue(all(output in self.space.rankings for output in outputs))

    def test_two_ballot_shortcut_is_exact(self):
        space = RankingSpace.create(4)
        kemeny = KemenyAnalyzer(space)
        for first in space.rankings:
            for second in space.rankings:
                output = two_ballot_kemeny(space, first, second)
                profile = space.profile_from_ballots((first, second))
                self.assertEqual(
                    kemeny.score(profile, output),
                    kemeny.optimum_value(profile),
                )

    def test_borda_is_unanimous_and_five_approximate_on_small_profiles(self):
        self.assertEqual(
            borda_ranking(self.space, (self.acb,) * 4), self.acb
        )
        kemeny = KemenyAnalyzer(self.space)
        for size in range(1, 6):
            for profile in profiles_of_size(self.space, size):
                ballots = tuple(
                    ranking
                    for count, ranking in zip(profile, self.space.rankings)
                    for _ in range(count)
                )
                borda = borda_ranking(self.space, ballots)
                self.assertLessEqual(
                    kemeny.score(profile, borda),
                    5 * kemeny.optimum_value(profile),
                )

    def test_borda_block_outputs(self):
        ballots = [self.abc] * 5 + [self.cba]
        outputs = borda_block_outputs(
            self.space, ballots, block_size=3, rng=Random(7)
        )
        self.assertEqual(len(outputs), 2)
        self.assertTrue(all(output in self.space.rankings for output in outputs))

    def test_invalid_discarded_ballot_is_rejected(self):
        with self.assertRaises(ValueError):
            exact_block_outputs(
                self.space,
                [self.abc, self.acb, (0, 0, 1)],
                block_size=2,
                rng=Random(1),
            )

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

    def test_sample_and_center_accepts_borda_and_rejects_unknown_estimator(self):
        ballots = [self.abc] * 8 + [self.cba] * 2
        output = sample_and_center(
            self.space,
            ballots,
            block_size=2,
            estimator="borda",
            rng=Random(4),
        )
        self.assertEqual(output, self.abc)
        with self.assertRaises(ValueError):
            sample_and_center(
                self.space,
                ballots,
                block_size=2,
                estimator="unknown",
                rng=Random(4),
            )

    def test_rejects_invalid_step(self):
        with self.assertRaises(ValueError):
            center_of_attention(self.space, [self.abc], step=1)


if __name__ == "__main__":
    unittest.main()
