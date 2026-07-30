"""Exact Kemeny computations for small candidate sets."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from math import comb
from typing import Iterable, Sequence

Ranking = tuple[int, ...]
Profile = tuple[int, ...]


def kendall_distance(left: Sequence[int], right: Sequence[int]) -> int:
    """Return the number of pairwise disagreements between two rankings."""
    if len(left) != len(right) or set(left) != set(right):
        raise ValueError("rankings must contain the same distinct items")
    right_position = {item: index for index, item in enumerate(right)}
    inversions = 0
    for first_index, first in enumerate(left):
        for second in left[first_index + 1 :]:
            if right_position[first] > right_position[second]:
                inversions += 1
    return inversions


@dataclass(frozen=True)
class RankingSpace:
    """All permutations of ``range(candidate_count)`` and their metric."""

    candidate_count: int
    rankings: tuple[Ranking, ...]
    distances: tuple[tuple[int, ...], ...]

    @classmethod
    def create(cls, candidate_count: int) -> "RankingSpace":
        if candidate_count < 1:
            raise ValueError("candidate_count must be positive")
        rankings = tuple(permutations(range(candidate_count)))
        distances = tuple(
            tuple(kendall_distance(left, right) for right in rankings)
            for left in rankings
        )
        return cls(candidate_count, rankings, distances)

    @property
    def ranking_count(self) -> int:
        return len(self.rankings)

    @property
    def diameter(self) -> int:
        return comb(self.candidate_count, 2)

    def empty_profile(self) -> Profile:
        return (0,) * self.ranking_count

    def profile_from_ballots(self, ballots: Iterable[Sequence[int]]) -> Profile:
        index = {ranking: position for position, ranking in enumerate(self.rankings)}
        counts = [0] * self.ranking_count
        for ballot in ballots:
            ranking = tuple(ballot)
            if ranking not in index:
                raise ValueError(f"invalid ballot: {ranking}")
            counts[index[ranking]] += 1
        return tuple(counts)

    def validate_profile(self, profile: Profile) -> None:
        if len(profile) != self.ranking_count:
            raise ValueError(
                f"profile needs {self.ranking_count} counts, got {len(profile)}"
            )
        if any(not isinstance(count, int) or count < 0 for count in profile):
            raise ValueError("profile counts must be nonnegative integers")

    def ranking_label(self, ranking: Ranking) -> str:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.candidate_count <= len(alphabet):
            return "".join(alphabet[item] for item in ranking)
        return ">".join(str(item) for item in ranking)

    def profile_label(self, profile: Profile) -> str:
        self.validate_profile(profile)
        terms: list[str] = []
        for count, ranking in zip(profile, self.rankings):
            if count:
                terms.append(f"{self.ranking_label(ranking)}:{count}")
        return "empty" if not terms else " ".join(terms)


class KemenyAnalyzer:
    """Memoized exact score and optimum calculations."""

    def __init__(self, space: RankingSpace):
        self.space = space
        self._score_cache: dict[Profile, tuple[int, ...]] = {}
        self._optimum_cache: dict[Profile, tuple[int, tuple[Ranking, ...]]] = {}

    def scores(self, profile: Profile) -> tuple[int, ...]:
        self.space.validate_profile(profile)
        cached = self._score_cache.get(profile)
        if cached is not None:
            return cached
        scores = tuple(
            sum(
                count * self.space.distances[ballot_index][output_index]
                for ballot_index, count in enumerate(profile)
            )
            for output_index in range(self.space.ranking_count)
        )
        self._score_cache[profile] = scores
        return scores

    def score(self, profile: Profile, ranking: Ranking) -> int:
        try:
            index = self.space.rankings.index(tuple(ranking))
        except ValueError as error:
            raise ValueError(f"ranking is not in this space: {ranking}") from error
        return self.scores(profile)[index]

    def optimum(self, profile: Profile) -> tuple[int, tuple[Ranking, ...]]:
        self.space.validate_profile(profile)
        cached = self._optimum_cache.get(profile)
        if cached is not None:
            return cached
        scores = self.scores(profile)
        optimum_value = min(scores)
        optima = tuple(
            ranking
            for ranking, score in zip(self.space.rankings, scores)
            if score == optimum_value
        )
        result = (optimum_value, optima)
        self._optimum_cache[profile] = result
        return result

    def optimum_value(self, profile: Profile) -> int:
        return self.optimum(profile)[0]

    def optima(self, profile: Profile) -> tuple[Ranking, ...]:
        return self.optimum(profile)[1]

    def selected_optimum(self, profile: Profile) -> Ranking:
        """Use lexicographic tie-breaking for a deterministic selector."""
        return self.optima(profile)[0]

