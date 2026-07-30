"""Exact and Monte Carlo tools for the two-color triangular Y game.

Cells use axial coordinates ``(q, r)`` in the triangular region

    q >= 0, r >= 0, q + r < n.

The three sides are ``q = 0``, ``r = 0``, and ``q + r = n - 1``.  A color
wins when one of its connected components meets all three sides.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from math import exp


Cell = tuple[int, int]


def majority_circuit_gate_count(n: int) -> int:
    """Number of ternary gates in the full side-``n`` reduction circuit."""

    if n < 1:
        raise ValueError("side length must be positive")
    return (n - 1) * n * (n + 1) // 6


@dataclass(frozen=True)
class TriangularYBoard:
    """Precomputed geometry for a triangular board of side length ``n``."""

    n: int
    cells: tuple[Cell, ...]
    adjacency: tuple[int, ...]
    sides: tuple[int, int, int]
    reduction_triangles: tuple[tuple[int, int, int], ...]

    @classmethod
    def create(cls, n: int) -> "TriangularYBoard":
        if n < 1:
            raise ValueError("side length must be positive")

        cells = tuple((q, r) for q in range(n) for r in range(n - q))
        index = {cell: i for i, cell in enumerate(cells)}
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))

        adjacency: list[int] = []
        side_q = 0
        side_r = 0
        side_diagonal = 0
        for i, (q, r) in enumerate(cells):
            neighborhood = 0
            for dq, dr in directions:
                neighbor = index.get((q + dq, r + dr))
                if neighbor is not None:
                    neighborhood |= 1 << neighbor
            adjacency.append(neighborhood)

            if q == 0:
                side_q |= 1 << i
            if r == 0:
                side_r |= 1 << i
            if q + r == n - 1:
                side_diagonal |= 1 << i

        reduction_triangles = tuple(
            (index[(q, r)], index[(q + 1, r)], index[(q, r + 1)])
            for q in range(n - 1)
            for r in range(n - 1 - q)
        )

        return cls(
            n=n,
            cells=cells,
            adjacency=tuple(adjacency),
            sides=(side_q, side_r, side_diagonal),
            reduction_triangles=reduction_triangles,
        )

    @property
    def cell_count(self) -> int:
        return len(self.cells)

    @property
    def full_mask(self) -> int:
        return (1 << self.cell_count) - 1

    def _validate_mask(self, blue_mask: int) -> None:
        if blue_mask < 0 or blue_mask & ~self.full_mask:
            raise ValueError("blue mask contains cells outside the board")

    def has_y(self, blue_mask: int, color: int) -> bool:
        """Return whether ``color`` has a component touching all three sides."""

        self._validate_mask(blue_mask)
        if color not in (0, 1):
            raise ValueError("color must be 0 (yellow) or 1 (blue)")

        remaining = blue_mask if color else self.full_mask ^ blue_mask
        while remaining:
            frontier = remaining & -remaining
            component = 0
            remaining ^= frontier

            while frontier:
                component |= frontier
                neighbors = 0
                scan = frontier
                while scan:
                    bit = scan & -scan
                    scan ^= bit
                    neighbors |= self.adjacency[bit.bit_length() - 1]
                frontier = neighbors & remaining
                remaining ^= frontier

            if all(component & side for side in self.sides):
                return True

        return False

    def winner(self, blue_mask: int) -> int:
        """Return the unique Y winner: 0 for yellow and 1 for blue."""

        blue = self.has_y(blue_mask, 1)
        yellow = self.has_y(blue_mask, 0)
        if blue == yellow:
            raise RuntimeError("coloring violates the unique-Y theorem")
        return int(blue)

    def majority_reduce(self, blue_mask: int) -> int:
        """Apply the three-cell majority reduction to a board of size ``n-1``.

        The reduced cell ``(q, r)`` is the majority color of the pairwise
        adjacent input cells ``(q, r)``, ``(q+1, r)``, and ``(q, r+1)``.
        This is a rotated coordinate version of deleting the leftmost column
        in the standard Y-game proof.
        """

        self._validate_mask(blue_mask)
        if self.n == 1:
            raise ValueError("a side-one board cannot be reduced")

        reduced_mask = 0
        for output_index, input_indices in enumerate(self.reduction_triangles):
            blue_count = sum((blue_mask >> i) & 1 for i in input_indices)
            if blue_count >= 2:
                reduced_mask |= 1 << output_index
        return reduced_mask

    def reduce_to_one(self, blue_mask: int) -> int:
        """Evaluate the depth-``n-1`` majority circuit for the winner."""

        self._validate_mask(blue_mask)
        board = self
        mask = blue_mask
        while board.n > 1:
            mask = board.majority_reduce(mask)
            board = cached_y_board(board.n - 1)
        return mask


@lru_cache(maxsize=None)
def cached_y_board(n: int) -> TriangularYBoard:
    """Reuse immutable board geometry across repeated circuit evaluations."""

    return TriangularYBoard.create(n)


def exact_pivotality(board: TriangularYBoard) -> tuple[float, tuple[float, ...]]:
    """Exact uniform one-cell pivotality for a small board.

    The first output is the probability that a uniformly random cell flip
    changes the winner when the coloring is uniform.  The second contains the
    influence of each cell in ``board.cells`` order.
    """

    coloring_count = 1 << board.cell_count
    winners = tuple(board.winner(mask) for mask in range(coloring_count))
    per_cell: list[float] = []
    for cell_index in range(board.cell_count):
        changes = sum(
            winners[mask] != winners[mask ^ (1 << cell_index)]
            for mask in range(coloring_count)
        )
        per_cell.append(changes / coloring_count)
    return sum(per_cell) / board.cell_count, tuple(per_cell)


def exact_winner_radii(board: TriangularYBoard) -> tuple[int, ...]:
    """Return every coloring's Hamming distance to the opposite winner.

    This multi-source hypercube search is intended for small boards.  Its
    memory and running time are both exponential in the number of cells.
    """

    coloring_count = 1 << board.cell_count
    winners = tuple(board.winner(mask) for mask in range(coloring_count))

    def distances_to(target_winner: int) -> list[int]:
        distances = [-1] * coloring_count
        queue: deque[int] = deque()
        for mask, winner in enumerate(winners):
            if winner == target_winner:
                distances[mask] = 0
                queue.append(mask)
        while queue:
            mask = queue.popleft()
            next_distance = distances[mask] + 1
            for cell_index in range(board.cell_count):
                neighbor = mask ^ (1 << cell_index)
                if distances[neighbor] == -1:
                    distances[neighbor] = next_distance
                    queue.append(neighbor)
        return distances

    distance_to_yellow = distances_to(0)
    distance_to_blue = distances_to(1)
    return tuple(
        distance_to_yellow[mask] if winner else distance_to_blue[mask]
        for mask, winner in enumerate(winners)
    )


def binary_winner_smooth_sensitivity(radius: int, beta: float) -> float:
    """Exact beta-smooth sensitivity of a nonconstant binary winner.

    The binary winner has local sensitivity one exactly at pivotal colorings.
    A coloring at distance ``radius`` from the opposite outcome is at distance
    ``max(radius - 1, 0)`` from that pivotal set.
    """

    if radius < 1:
        raise ValueError("a nonconstant binary winner must have positive radius")
    if beta < 0:
        raise ValueError("beta must be nonnegative")
    return exp(-beta * max(radius - 1, 0))
