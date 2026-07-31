"""Run exact Chomp traces and oracle-consistency diagnostics."""

from __future__ import annotations

import json
from dataclasses import asdict
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
from typing import Any

from kemeny_dp.chomp import (
    ChompState,
    chomp_grundy,
    chomp_moves,
    chomp_optimal_moves,
    chomp_successor,
    largest_bite_policy,
    lexicographic_oracle_policy,
    play_chomp,
    rectangular_chomp_state,
)
from kemeny_dp.oracle_eval import aggregate_oracle_traces


ROOT = Path(__file__).resolve().parents[1]


def json_value(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_value(item) for item in value]
    return value


def states_in_box(max_rows: int, max_columns: int) -> tuple[ChompState, ...]:
    states: set[ChompState] = set()
    for rows in range(1, max_rows + 1):
        for increasing in combinations_with_replacement(
            range(1, max_columns + 1),
            rows,
        ):
            states.add(tuple(reversed(increasing)))
    return tuple(sorted(states))


def sampled_state_accuracy(
    states: tuple[ChompState, ...],
    *,
    oracle: bool,
) -> tuple[int, int, Fraction]:
    labeled = 0
    matches = 0
    policy = (
        lexicographic_oracle_policy if oracle else largest_bite_policy
    )
    for state in states:
        optimal = chomp_optimal_moves(state)
        if not optimal:
            continue
        labeled += 1
        matches += policy(state) in optimal
    return labeled, matches, Fraction(matches, labeled)


def policy_trace_audit(
    starts: tuple[ChompState, ...],
    *,
    oracle: bool,
) -> dict[str, Any]:
    policy = lexicographic_oracle_policy if oracle else largest_bite_policy
    traces: list[tuple[bool | None, ...]] = []
    outcome_matches = 0
    board_records: list[dict[str, Any]] = []
    for state in starts:
        winner, actions, flags = play_chomp(state, policy, policy)
        expected_winner = 0 if chomp_grundy(state) != 0 else 1
        outcome_matches += winner == expected_winner
        traces.append(flags)
        board_records.append(
            {
                "state": state,
                "grundy": chomp_grundy(state),
                "plies": len(actions),
                "winner": winner,
                "oracle_start_value_winner": expected_winner,
                "outcome_matches_oracle_start_value": (
                    winner == expected_winner
                ),
            }
        )
    aggregate = aggregate_oracle_traces(traces)
    return {
        "aggregate_oracle_metrics": asdict(aggregate),
        "outcome_matches_oracle_start_value": outcome_matches,
        "starts": len(starts),
        "outcome_match_rate": Fraction(outcome_matches, len(starts)),
        "boards": board_records,
    }


def main() -> None:
    starts = tuple(
        rectangular_chomp_state(rows, columns)
        for rows in range(2, 7)
        for columns in range(2, 7)
    )
    states = states_in_box(6, 6)
    oracle_labeled, oracle_matches, oracle_sample_rate = (
        sampled_state_accuracy(states, oracle=True)
    )
    greedy_labeled, greedy_matches, greedy_sample_rate = (
        sampled_state_accuracy(states, oracle=False)
    )
    oracle_traces = policy_trace_audit(starts, oracle=True)
    greedy_traces = policy_trace_audit(starts, oracle=False)

    result = {
        "status": {
            "chomp_grundy_oracle": "KNOWN_THEORY_EXACTLY_IMPLEMENTED",
            "trace_metrics": "SOURCE_DEFINITIONS_IMPLEMENTED",
            "finite_results": "EXACT_COMPUTATIONAL",
            "alphazero_reproduction": "NOT_ATTEMPTED",
            "kemeny_or_privacy_claim": "NONE",
        },
        "source": {
            "title": (
                "AlphaZero in Sparsely Rewarded Games: "
                "Limits and Auxiliary Supervision"
            ),
            "arxiv": "2607.08984",
            "url": "https://arxiv.org/abs/2607.08984",
        },
        "scope": {
            "rectangular_start_rows": [2, 6],
            "rectangular_start_columns": [2, 6],
            "full_board_starts": len(starts),
            "all_partition_states_in_6_by_6_box": len(states),
        },
        "full_game_trace_audit": {
            "oracle_self_play": oracle_traces,
            "largest_bite_self_play": greedy_traces,
        },
        "exhaustive_sampled_state_audit": {
            "oracle_policy": {
                "labeled_winning_states": oracle_labeled,
                "oracle_matches": oracle_matches,
                "match_rate": oracle_sample_rate,
            },
            "largest_bite_policy": {
                "labeled_winning_states": greedy_labeled,
                "oracle_matches": greedy_matches,
                "match_rate": greedy_sample_rate,
            },
        },
        "checks": {
            "oracle_policy_perfect_on_every_eligible_trace": (
                oracle_traces["aggregate_oracle_metrics"]["perfect_rate"]
                == Fraction(1)
            ),
            "oracle_policy_exact_on_every_labeled_sampled_state": (
                oracle_sample_rate == 1
            ),
            "largest_bite_is_not_universally_oracle_consistent": (
                greedy_sample_rate < 1
            ),
            "every_optimal_move_reaches_grundy_zero": all(
                chomp_grundy(chomp_successor(state, move)) == 0
                for state in states
                for move in chomp_optimal_moves(state)
            ),
            "all_nonterminal_states_have_a_safe_move": all(
                bool(chomp_moves(state)) == (state != (1,))
                for state in states
            ),
        },
    }
    output = ROOT / "results" / "oracle_consistency_audit.json"
    output.write_text(
        json.dumps(json_value(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(json_value(result["status"]), indent=2))
    print(
        "Largest-bite sampled-state oracle match:",
        greedy_sample_rate,
    )
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
