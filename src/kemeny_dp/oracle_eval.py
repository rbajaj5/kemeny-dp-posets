"""Exact diagnostics for policies evaluated against a finite action oracle."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Iterable, Sequence, TypeVar

Action = TypeVar("Action", bound=Hashable)


@dataclass(frozen=True)
class TraceOracleMetrics:
    """Oracle-consistency metrics for one sequential decision trace."""

    total_plies: int
    labeled_plies: int
    matches: int
    match_rate: Fraction | None
    longest_consistent_chain: int | None
    first_failure_ply: int | None
    perfect: bool | None


@dataclass(frozen=True)
class AggregateOracleMetrics:
    """Pooled and per-trace oracle-consistency metrics."""

    traces: int
    eligible_traces: int
    perfect_traces: int
    perfect_rate: Fraction | None
    labeled_plies: int
    matches: int
    pooled_match_rate: Fraction | None
    mean_longest_consistent_chain: Fraction | None
    imperfect_traces: int
    mean_first_failure_ply: Fraction | None


def oracle_match_flags(
    actions: Sequence[Action],
    oracle_action_sets: Sequence[Iterable[Action] | None],
) -> tuple[bool | None, ...]:
    """Mark each action as optimal, or ``None`` when the oracle is undefined."""
    if len(actions) != len(oracle_action_sets):
        raise ValueError("actions and oracle_action_sets must have equal length")
    flags: list[bool | None] = []
    for action, oracle_actions in zip(actions, oracle_action_sets):
        if oracle_actions is None:
            flags.append(None)
            continue
        optimal = frozenset(oracle_actions)
        if not optimal:
            raise ValueError("a labeled oracle action set cannot be empty")
        flags.append(action in optimal)
    return tuple(flags)


def evaluate_oracle_trace(
    flags: Sequence[bool | None],
) -> TraceOracleMetrics:
    """Compute exact match, chain, first-failure, and perfection metrics.

    Unlabeled plies are omitted from match and chain calculations. The first
    failure retains its original zero-based ply index. A trace with no labeled
    decisions has ``None`` for rate, chain, first failure, and perfection.
    """
    if any(
        flag is not True and flag is not False and flag is not None
        for flag in flags
    ):
        raise ValueError("flags must contain only booleans or None")

    labeled = tuple(flag for flag in flags if flag is not None)
    if not labeled:
        return TraceOracleMetrics(
            total_plies=len(flags),
            labeled_plies=0,
            matches=0,
            match_rate=None,
            longest_consistent_chain=None,
            first_failure_ply=None,
            perfect=None,
        )

    matches = sum(labeled)
    longest = 0
    current = 0
    for flag in labeled:
        if flag:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    first_failure = next(
        (ply for ply, flag in enumerate(flags) if flag is False),
        None,
    )
    return TraceOracleMetrics(
        total_plies=len(flags),
        labeled_plies=len(labeled),
        matches=matches,
        match_rate=Fraction(matches, len(labeled)),
        longest_consistent_chain=longest,
        first_failure_ply=first_failure,
        perfect=first_failure is None,
    )


def aggregate_oracle_traces(
    traces: Sequence[Sequence[bool | None]],
) -> AggregateOracleMetrics:
    """Aggregate exact metrics without treating unlabeled traces as perfect."""
    metrics = tuple(evaluate_oracle_trace(trace) for trace in traces)
    eligible = tuple(metric for metric in metrics if metric.perfect is not None)
    imperfect = tuple(
        metric for metric in eligible if metric.perfect is False
    )
    labeled_plies = sum(metric.labeled_plies for metric in eligible)
    matches = sum(metric.matches for metric in eligible)
    perfect_traces = sum(metric.perfect is True for metric in eligible)

    return AggregateOracleMetrics(
        traces=len(metrics),
        eligible_traces=len(eligible),
        perfect_traces=perfect_traces,
        perfect_rate=(
            Fraction(perfect_traces, len(eligible)) if eligible else None
        ),
        labeled_plies=labeled_plies,
        matches=matches,
        pooled_match_rate=(
            Fraction(matches, labeled_plies) if labeled_plies else None
        ),
        mean_longest_consistent_chain=(
            Fraction(
                sum(
                    metric.longest_consistent_chain or 0
                    for metric in eligible
                ),
                len(eligible),
            )
            if eligible
            else None
        ),
        imperfect_traces=len(imperfect),
        mean_first_failure_ply=(
            Fraction(
                sum(
                    metric.first_failure_ply
                    for metric in imperfect
                    if metric.first_failure_ply is not None
                ),
                len(imperfect),
            )
            if imperfect
            else None
        ),
    )
