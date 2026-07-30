import unittest
from random import Random

from kemeny_dp.core import RankingSpace
from kemeny_dp.geometry import (
    pairwise_sign_vector,
    project_vector,
    rademacher_projection,
    squared_euclidean,
)


class GeometryTests(unittest.TestCase):
    def test_sign_embedding_recovers_kendall_distance(self):
        space = RankingSpace.create(4)
        vectors = tuple(pairwise_sign_vector(ranking) for ranking in space.rankings)
        for left_index, left in enumerate(vectors):
            for right_index, right in enumerate(vectors):
                self.assertEqual(
                    squared_euclidean(left, right),
                    4 * space.distances[left_index][right_index],
                )

    def test_rademacher_projection_dimensions(self):
        vector = pairwise_sign_vector((0, 1, 2, 3))
        projection = rademacher_projection(
            len(vector), 5, rng=Random(11)
        )
        projected = project_vector(projection, vector)
        self.assertEqual(len(projection), 5)
        self.assertEqual(len(projected), 5)


if __name__ == "__main__":
    unittest.main()
