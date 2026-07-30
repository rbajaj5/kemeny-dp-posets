"""Local, smooth, and cover-distance sensitivity calculations."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, exp

from .core import KemenyAnalyzer, Profile, Ranking
from .poset import neighbors


@dataclass(frozen=True)
class SmoothSensitivityResult:
    value: float
    explored_radius: int
    profiles_examined: int
    unseen_tail_bound: float


class SensitivityAnalyzer:
    """Sensitivity calculations sharing a memoized Kemeny analyzer."""

    def __init__(self, kemeny: KemenyAnalyzer):
        self.kemeny = kemeny
        self.space = kemeny.space
        self._local_opt_cache: dict[Profile, int] = {}
        self._local_ranking_cache: dict[Profile, int] = {}

    def local_sensitivity_optimum_value(self, profile: Profile) -> int:
        """Exact local sensitivity of the scalar optimal Kemeny cost."""
        cached = self._local_opt_cache.get(profile)
        if cached is not None:
            return cached
        value = self.kemeny.optimum_value(profile)
        sensitivity = max(
            (
                abs(value - self.kemeny.optimum_value(adjacent))
                for adjacent in neighbors(profile)
            ),
            default=0,
        )
        self._local_opt_cache[profile] = sensitivity
        return sensitivity

    def local_sensitivity_optimum_value_from_gaps(self, profile: Profile) -> int:
        """Compute the same scalar local sensitivity from one score landscape.

        This is the closed form proved in ``notes/RESULTS.md`` and avoids
        solving a fresh Kemeny problem at every neighboring profile.
        """
        scores = self.kemeny.scores(profile)
        optimum = min(scores)
        gaps = tuple(score - optimum for score in scores)

        largest_addition_change = max(
            min(
                gap + self.space.distances[ballot_index][output_index]
                for output_index, gap in enumerate(gaps)
            )
            for ballot_index in range(self.space.ranking_count)
        )

        removal_changes = [
            max(
                self.space.distances[ballot_index][output_index] - gap
                for output_index, gap in enumerate(gaps)
            )
            for ballot_index, count in enumerate(profile)
            if count
        ]
        largest_removal_change = max(removal_changes, default=0)
        return max(largest_addition_change, largest_removal_change)

    def local_sensitivity_selected_ranking(self, profile: Profile) -> int:
        """Exact Kendall-metric local sensitivity of lexicographic Kemeny."""
        cached = self._local_ranking_cache.get(profile)
        if cached is not None:
            return cached
        selected = self.kemeny.selected_optimum(profile)
        selected_index = self.space.rankings.index(selected)
        sensitivity = max(
            (
                self.space.distances[selected_index][
                    self.space.rankings.index(
                        self.kemeny.selected_optimum(adjacent)
                    )
                ]
                for adjacent in neighbors(profile)
            ),
            default=0,
        )
        self._local_ranking_cache[profile] = sensitivity
        return sensitivity

    def uniqueness_radius(self, profile: Profile) -> int:
        """Exact cover distance until a unique optimum can lose uniqueness.

        Returns zero when the current profile does not have a unique optimum.
        """
        _, optima = self.kemeny.optimum(profile)
        if len(optima) != 1:
            return 0
        optimum = optima[0]
        optimum_index = self.space.rankings.index(optimum)
        scores = self.kemeny.scores(profile)
        optimum_score = scores[optimum_index]
        radius = self.space.diameter + sum(profile) * self.space.diameter + 1
        for competitor_index, competitor in enumerate(self.space.rankings):
            if competitor == optimum:
                continue
            gap = scores[competitor_index] - optimum_score
            distance = self.space.distances[optimum_index][competitor_index]
            radius = min(radius, ceil(gap / distance))
        return radius

    def smooth_upper_bound_selected_ranking(
        self, profile: Profile, beta: float
    ) -> float:
        """A beta-smooth upper bound derived from the uniqueness radius."""
        if beta <= 0:
            raise ValueError("beta must be positive")
        radius = self.uniqueness_radius(profile)
        exponent = max(radius - 1, 0)
        return self.space.diameter * exp(-beta * exponent)

    def exact_smooth_sensitivity_optimum_value(
        self,
        profile: Profile,
        beta: float,
        *,
        max_radius: int = 64,
    ) -> SmoothSensitivityResult:
        """Compute exact beta-smooth sensitivity of the scalar optimum.

        Breadth-first search explores complete Hasse shells. Since global
        sensitivity is at most ``diameter``, shell ``k`` and every later shell
        contribute at most ``diameter * exp(-beta*k)``. Search stops only when
        that certified unseen tail cannot beat the best value already found.
        """
        if beta <= 0:
            raise ValueError("beta must be positive")
        self.space.validate_profile(profile)
        diameter = self.space.diameter
        if diameter == 0:
            return SmoothSensitivityResult(0.0, 0, 1, 0.0)

        seen = {profile}
        frontier = {profile}
        best = 0.0
        examined = 0

        for radius in range(max_radius + 1):
            decay = exp(-beta * radius)
            for candidate in frontier:
                examined += 1
                contribution = (
                    self.local_sensitivity_optimum_value(candidate) * decay
                )
                best = max(best, contribution)

            unseen_tail = diameter * exp(-beta * (radius + 1))
            if unseen_tail <= best:
                return SmoothSensitivityResult(
                    best, radius, examined, unseen_tail
                )

            next_frontier: set[Profile] = set()
            for candidate in frontier:
                for adjacent in neighbors(candidate):
                    if adjacent not in seen:
                        seen.add(adjacent)
                        next_frontier.add(adjacent)
            frontier = next_frontier

        raise RuntimeError(
            "smooth-sensitivity shell search did not certify the tail; "
            "increase max_radius"
        )

    def brute_force_distance_to_loss_of_uniqueness(
        self, profile: Profile, *, max_radius: int = 16
    ) -> int:
        """BFS oracle used to check the closed-form radius on small inputs."""
        _, optima = self.kemeny.optimum(profile)
        if len(optima) != 1:
            return 0
        optimum: Ranking = optima[0]
        seen = {profile}
        frontier = {profile}
        for radius in range(1, max_radius + 1):
            next_frontier: set[Profile] = set()
            for candidate in frontier:
                for adjacent in neighbors(candidate):
                    if adjacent in seen:
                        continue
                    seen.add(adjacent)
                    next_frontier.add(adjacent)
                    if self.kemeny.optima(adjacent) != (optimum,):
                        return radius
            frontier = next_frontier
        raise RuntimeError("instability not found inside max_radius")
