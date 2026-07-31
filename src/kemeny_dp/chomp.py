"""A small exact Chomp oracle for finite diagnostic experiments."""

from __future__ import annotations

from functools import cache
from typing import Callable

ChompState = tuple[int, ...]
ChompMove = tuple[int, int]
ChompPolicy = Callable[[ChompState], ChompMove]


def normalize_chomp_state(state: ChompState) -> ChompState:
    """Validate a left-justified Young diagram containing the poison square."""
    if not isinstance(state, tuple) or not state:
        raise ValueError("state must be a nonempty tuple")
    if any(not isinstance(length, int) or length < 0 for length in state):
        raise ValueError("row lengths must be nonnegative integers")
    if any(left < right for left, right in zip(state, state[1:])):
        raise ValueError("row lengths must be nonincreasing")
    normalized = tuple(length for length in state if length > 0)
    if not normalized:
        raise ValueError("state must contain the poison square")
    return normalized


def rectangular_chomp_state(rows: int, columns: int) -> ChompState:
    """Return the full ``rows`` by ``columns`` Chomp board."""
    if (
        not isinstance(rows, int)
        or not isinstance(columns, int)
        or rows < 1
        or columns < 1
    ):
        raise ValueError("rows and columns must be positive integers")
    return (columns,) * rows


def chomp_moves(state: ChompState) -> tuple[ChompMove, ...]:
    """Return every safe move, excluding the poisoned upper-left square."""
    normalized = normalize_chomp_state(state)
    return tuple(
        (row, column)
        for row, length in enumerate(normalized)
        for column in range(length)
        if (row, column) != (0, 0)
    )


def chomp_successor(state: ChompState, move: ChompMove) -> ChompState:
    """Apply a move, removing its square and every square below and right."""
    normalized = normalize_chomp_state(state)
    if (
        not isinstance(move, tuple)
        or len(move) != 2
        or any(not isinstance(coordinate, int) for coordinate in move)
    ):
        raise ValueError("move must be an integer (row, column) pair")
    if move not in chomp_moves(normalized):
        raise ValueError("move is not a safe legal move")
    row, column = move
    successor = list(normalized)
    for affected_row in range(row, len(successor)):
        successor[affected_row] = min(successor[affected_row], column)
    return normalize_chomp_state(tuple(successor))


@cache
def chomp_grundy(state: ChompState) -> int:
    """Return the exact Sprague-Grundy number with taking poison a loss."""
    normalized = normalize_chomp_state(state)
    successor_values = {
        chomp_grundy(chomp_successor(normalized, move))
        for move in chomp_moves(normalized)
    }
    value = 0
    while value in successor_values:
        value += 1
    return value


def chomp_optimal_moves(state: ChompState) -> tuple[ChompMove, ...]:
    """Return moves to Grundy zero, or no labeled moves from a losing state."""
    normalized = normalize_chomp_state(state)
    if chomp_grundy(normalized) == 0:
        return ()
    return tuple(
        move
        for move in chomp_moves(normalized)
        if chomp_grundy(chomp_successor(normalized, move)) == 0
    )


def lexicographic_oracle_policy(state: ChompState) -> ChompMove:
    """Choose the first oracle-optimal move, falling back on losing states."""
    normalized = normalize_chomp_state(state)
    optimal = chomp_optimal_moves(normalized)
    moves = optimal or chomp_moves(normalized)
    if not moves:
        raise ValueError("terminal Chomp state has no safe move")
    return moves[0]


def largest_bite_policy(state: ChompState) -> ChompMove:
    """Choose a safe move removing the most squares, lexicographically tied."""
    normalized = normalize_chomp_state(state)
    moves = chomp_moves(normalized)
    if not moves:
        raise ValueError("terminal Chomp state has no safe move")
    size = sum(normalized)
    return min(
        moves,
        key=lambda move: (
            -(size - sum(chomp_successor(normalized, move))),
            move,
        ),
    )


def play_chomp(
    state: ChompState,
    first_policy: ChompPolicy,
    second_policy: ChompPolicy,
) -> tuple[int, tuple[ChompMove, ...], tuple[bool | None, ...]]:
    """Play to the forced-poison terminal state and return winner and audit."""
    current = normalize_chomp_state(state)
    actions: list[ChompMove] = []
    flags: list[bool | None] = []
    player = 0
    while chomp_moves(current):
        policy = first_policy if player == 0 else second_policy
        move = policy(current)
        if move not in chomp_moves(current):
            raise ValueError("policy returned an illegal or poisoned move")
        optimal = chomp_optimal_moves(current)
        flags.append(move in optimal if optimal else None)
        actions.append(move)
        current = chomp_successor(current, move)
        player = 1 - player
    return 1 - player, tuple(actions), tuple(flags)
