import unittest
from random import Random

from kemeny_dp.core import RankingSpace
from kemeny_dp.geometry import (
    jl_sufficient_dimension,
    pairwise_sign_vector,
    project_vector,
    rademacher_projection,
    spherical_column_projection,
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

    def test_spherical_projection_has_unit_columns(self):
        input_dimension = 7
        output_dimension = 5
        projection = spherical_column_projection(
            input_dimension,
            output_dimension,
            rng=Random(19),
        )
        self.assertEqual(len(projection), output_dimension)
        self.assertTrue(
            all(len(row) == input_dimension for row in projection)
        )
        for column in range(input_dimension):
            norm_squared = sum(
                projection[row][column] ** 2
                for row in range(output_dimension)
            )
            self.assertAlmostEqual(norm_squared, 1.0, places=12)

    def test_spherical_projection_is_seed_reproducible(self):
        first = spherical_column_projection(4, 3, rng=Random(23))
        second = spherical_column_projection(4, 3, rng=Random(23))
        self.assertEqual(first, second)

    def test_explicit_jl_dimension_bound_and_union_bound(self):
        fixed = jl_sufficient_dimension(0.25, 0.1)
        finite = jl_sufficient_dimension(
            0.25,
            0.1,
            finite_set_size=100,
        )
        self.assertEqual(fixed, 3068)
        self.assertEqual(finite, 7784)
        self.assertGreater(finite, fixed)

    def test_jl_input_validation(self):
        with self.assertRaises(ValueError):
            jl_sufficient_dimension(0.5, 0.1)
        with self.assertRaises(ValueError):
            jl_sufficient_dimension(0.1, 0.5)
        with self.assertRaises(ValueError):
            jl_sufficient_dimension(0.1, 0.1, finite_set_size=True)
        with self.assertRaises(ValueError):
            spherical_column_projection(0, 2, rng=Random(1))


if __name__ == "__main__":
    unittest.main()
