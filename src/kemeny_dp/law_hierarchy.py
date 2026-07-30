"""Exact law reconstruction on a finite profile poset.

For a random profile ``X`` in a finite lower ideal, define the upper-set
probabilities

    Z(x) = Pr[X >= x],

where the order is coordinatewise.  The full family ``Z`` determines the law
of ``X`` by finite-poset Möbius inversion.  This module keeps the arithmetic
exact so that the reconstruction is a certificate rather than a tolerance
check.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from fractions import Fraction

from .core import Profile

Probability = int | Fraction


def coordinatewise_leq(left: Profile, right: Profile) -> bool:
    """Return whether ``left <= right`` in the multiset-profile poset."""
    if len(left) != len(right):
        raise ValueError("profiles must have the same dimension")
    return all(a <= b for a, b in zip(left, right))


def _validated_states(states: Sequence[Profile]) -> tuple[Profile, ...]:
    result = tuple(states)
    if not result:
        raise ValueError("state space must be nonempty")
    dimension = len(result[0])
    if dimension == 0:
        raise ValueError("profiles must have positive dimension")
    if len(set(result)) != len(result):
        raise ValueError("state space contains duplicate profiles")
    for profile in result:
        if len(profile) != dimension:
            raise ValueError("profiles must have the same dimension")
        if any(not isinstance(count, int) or count < 0 for count in profile):
            raise ValueError("profile counts must be nonnegative integers")
    return result


def _as_fraction(value: Probability) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise TypeError("probabilities must be integers or fractions")


def validate_probability_mass(
    states: Sequence[Profile],
    mass: Mapping[Profile, Probability],
) -> dict[Profile, Fraction]:
    """Return a complete exact mass function after validating a distribution."""
    state_tuple = _validated_states(states)
    state_set = set(state_tuple)
    unknown = set(mass) - state_set
    if unknown:
        raise ValueError(f"mass contains states outside the state space: {unknown}")

    completed = {
        state: _as_fraction(mass.get(state, 0)) for state in state_tuple
    }
    if any(value < 0 for value in completed.values()):
        raise ValueError("probability masses must be nonnegative")
    if sum(completed.values(), Fraction()) != 1:
        raise ValueError("probability masses must sum exactly to one")
    return completed


def upper_set_probabilities(
    states: Sequence[Profile],
    mass: Mapping[Profile, Probability],
) -> dict[Profile, Fraction]:
    """Compute ``Pr[X >= x]`` at every state using exact arithmetic."""
    state_tuple = _validated_states(states)
    completed = validate_probability_mass(state_tuple, mass)
    return {
        lower: sum(
            (
                completed[upper]
                for upper in state_tuple
                if coordinatewise_leq(lower, upper)
            ),
            Fraction(),
        )
        for lower in state_tuple
    }


def invert_upper_set_probabilities(
    states: Sequence[Profile],
    upper_probabilities: Mapping[Profile, Probability],
) -> dict[Profile, Fraction]:
    """Recover a signed mass function by finite-poset Möbius inversion.

    If ``upper_probabilities`` came from :func:`upper_set_probabilities`, the
    returned values are the original nonnegative masses.  For arbitrary input
    the inverse may be signed; this is useful for diagnosing an inconsistent
    proposed hierarchy.
    """
    state_tuple = _validated_states(states)
    if set(upper_probabilities) != set(state_tuple):
        raise ValueError("one upper-set value is required for every state")
    upper = {
        state: _as_fraction(upper_probabilities[state])
        for state in state_tuple
    }

    descending = sorted(
        state_tuple,
        key=lambda profile: (sum(profile), profile),
        reverse=True,
    )
    mass: dict[Profile, Fraction] = {}
    for lower in descending:
        strict_upper_mass = sum(
            (
                mass[upper_state]
                for upper_state in mass
                if lower != upper_state
                and coordinatewise_leq(lower, upper_state)
            ),
            Fraction(),
        )
        mass[lower] = upper[lower] - strict_upper_mass
    return {state: mass[state] for state in state_tuple}


def expected_profile(
    states: Sequence[Profile],
    mass: Mapping[Profile, Probability],
) -> tuple[Fraction, ...]:
    """Return the coordinatewise expectation of a random profile."""
    state_tuple = _validated_states(states)
    completed = validate_probability_mass(state_tuple, mass)
    dimension = len(state_tuple[0])
    return tuple(
        sum(
            (
                completed[state] * state[index]
                for state in state_tuple
            ),
            Fraction(),
        )
        for index in range(dimension)
    )
