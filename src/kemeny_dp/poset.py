"""The multiset-profile poset and its Hasse graph."""

from __future__ import annotations

from collections.abc import Iterator

from .core import Profile, RankingSpace


def parents(profile: Profile) -> tuple[Profile, ...]:
    """Profiles covered by ``profile`` (remove one existing ballot)."""
    result: list[Profile] = []
    for index, count in enumerate(profile):
        if count:
            parent = list(profile)
            parent[index] -= 1
            result.append(tuple(parent))
    return tuple(result)


def children(profile: Profile) -> tuple[Profile, ...]:
    """Profiles that cover ``profile`` (add one ballot)."""
    result: list[Profile] = []
    for index in range(len(profile)):
        child = list(profile)
        child[index] += 1
        result.append(tuple(child))
    return tuple(result)


def neighbors(profile: Profile) -> tuple[Profile, ...]:
    """Undirected add/remove-one-ballot DP neighbors."""
    return parents(profile) + children(profile)


def hasse_distance(left: Profile, right: Profile) -> int:
    """Shortest-path distance in the undirected Hasse graph."""
    if len(left) != len(right):
        raise ValueError("profiles must use the same ranking space")
    return sum(abs(a - b) for a, b in zip(left, right))


def weak_compositions(total: int, parts: int) -> Iterator[Profile]:
    """Yield all ``parts``-tuples of nonnegative integers summing to total."""
    if total < 0 or parts < 1:
        raise ValueError("total must be nonnegative and parts positive")
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for suffix in weak_compositions(total - first, parts - 1):
            yield (first,) + suffix


def profiles_of_size(space: RankingSpace, size: int) -> tuple[Profile, ...]:
    return tuple(weak_compositions(size, space.ranking_count))


def profiles_up_to(space: RankingSpace, maximum_size: int) -> tuple[Profile, ...]:
    if maximum_size < 0:
        raise ValueError("maximum_size must be nonnegative")
    return tuple(
        profile
        for size in range(maximum_size + 1)
        for profile in profiles_of_size(space, size)
    )

