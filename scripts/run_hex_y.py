"""Reproduce the triangular Hex/Y majority-reduction experiments."""

from __future__ import annotations

import argparse
import json
import platform
import random
import statistics
import time
from pathlib import Path

from kemeny_dp.finite_sample import bernoulli_summary
from kemeny_dp.hex_y import (
    TriangularYBoard,
    binary_winner_smooth_sensitivity,
    exact_pivotality,
    exact_winner_radii,
    majority_circuit_gate_count,
)


ROOT = Path(__file__).resolve().parents[1]


def summary_dict(successes: int, trials: int) -> dict[str, float | int]:
    return bernoulli_summary(successes, trials).as_dict()


def exhaustive_certificate(max_side: int) -> list[dict[str, int]]:
    rows = []
    for n in range(1, max_side + 1):
        board = TriangularYBoard.create(n)
        reduced = TriangularYBoard.create(n - 1) if n > 1 else None
        unique_failures = 0
        reduction_failures = 0
        blue_wins = 0
        for mask in range(1 << board.cell_count):
            blue = board.has_y(mask, 1)
            yellow = board.has_y(mask, 0)
            unique_failures += int(blue == yellow)
            blue_wins += int(blue)
            if reduced is not None:
                reduced_mask = board.majority_reduce(mask)
                reduction_failures += int(
                    blue != reduced.has_y(reduced_mask, 1)
                    or yellow != reduced.has_y(reduced_mask, 0)
                )
        rows.append({
            "side": n,
            "cells": board.cell_count,
            "colorings": 1 << board.cell_count,
            "blue_wins": blue_wins,
            "yellow_wins": (1 << board.cell_count) - blue_wins,
            "unique_winner_failures": unique_failures,
            "majority_reduction_failures": reduction_failures,
        })
        print("exhaustive", rows[-1])
    return rows


def exact_influences(max_side: int) -> list[dict[str, object]]:
    rows = []
    for n in range(1, max_side + 1):
        board = TriangularYBoard.create(n)
        average, per_cell = exact_pivotality(board)
        radii = exact_winner_radii(board)
        radius_histogram = {
            str(radius): radii.count(radius)
            for radius in sorted(set(radii))
        }
        row = {
            "side": n,
            "cells": board.cell_count,
            "uniform_random_cell_flip_probability": average,
            "winner_radius_histogram": radius_histogram,
            "mean_smooth_sensitivity_beta_0_5": sum(
                binary_winner_smooth_sensitivity(radius, 0.5)
                for radius in radii
            ) / len(radii),
            "per_cell": [
                {"cell": list(cell), "influence": influence}
                for cell, influence in zip(board.cells, per_cell)
            ],
        }
        rows.append(row)
        print("pivotality", n, average)
    return rows


def monte_carlo(
    sides: list[int],
    probabilities: list[float],
    trials: int,
    seed: int,
) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rows = []
    for n in sides:
        board = TriangularYBoard.create(n)
        for probability in probabilities:
            blue_wins = 0
            pivotal_flips = 0
            for _ in range(trials):
                mask = 0
                for i in range(board.cell_count):
                    if rng.random() < probability:
                        mask |= 1 << i
                winner = board.winner(mask)
                blue_wins += winner
                chosen = rng.randrange(board.cell_count)
                pivotal_flips += int(
                    winner != board.winner(mask ^ (1 << chosen))
                )
            row = {
                "side": n,
                "blue_probability": probability,
                "blue_win": summary_dict(blue_wins, trials),
                "random_cell_pivotal": summary_dict(pivotal_flips, trials),
            }
            rows.append(row)
            print(
                "monte-carlo",
                n,
                probability,
                row["blue_win"]["rate"],
                row["random_cell_pivotal"]["rate"],
            )
    return rows


def algorithm_benchmark(
    sides: list[int],
    trials: int,
    repeats: int,
    seed: int,
) -> list[dict[str, float | int]]:
    """Compare exact connectivity and majority-circuit evaluation fairly."""

    rng = random.Random(seed)
    rows = []
    for n in sides:
        board = TriangularYBoard.create(n)
        masks = []
        for _ in range(trials):
            mask = 0
            for i in range(board.cell_count):
                if rng.getrandbits(1):
                    mask |= 1 << i
            masks.append(mask)

        direct_outputs = [board.winner(mask) for mask in masks]
        circuit_outputs = [board.reduce_to_one(mask) for mask in masks]
        mismatches = sum(a != b for a, b in zip(direct_outputs, circuit_outputs))

        direct_times = []
        circuit_times = []
        for _ in range(repeats):
            start = time.perf_counter()
            checksum_direct = sum(board.winner(mask) for mask in masks)
            direct_times.append(time.perf_counter() - start)

            start = time.perf_counter()
            checksum_circuit = sum(board.reduce_to_one(mask) for mask in masks)
            circuit_times.append(time.perf_counter() - start)
            if checksum_direct != checksum_circuit:
                raise RuntimeError("benchmark algorithms disagree")

        direct_seconds = statistics.median(direct_times)
        circuit_seconds = statistics.median(circuit_times)
        row = {
            "side": n,
            "cells": board.cell_count,
            "majority_gates_per_board": majority_circuit_gate_count(n),
            "boards": trials,
            "repeats": repeats,
            "mismatches": mismatches,
            "direct_connectivity_median_seconds": direct_seconds,
            "majority_circuit_median_seconds": circuit_seconds,
            "majority_circuit_over_direct_time": (
                circuit_seconds / direct_seconds
                if direct_seconds
                else float("inf")
            ),
        }
        rows.append(row)
        print("benchmark", row)
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exhaustive-max",
        type=int,
        default=5,
        help="largest side length for full enumeration (6 takes about two minutes)",
    )
    parser.add_argument("--trials", type=int, default=2000)
    parser.add_argument("--benchmark-trials", type=int, default=1000)
    parser.add_argument("--benchmark-repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "hex_y.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = {
        "status": "COMPUTATIONAL",
        "seed": args.seed,
        "exhaustive": exhaustive_certificate(args.exhaustive_max),
        "exact_pivotality": exact_influences(min(args.exhaustive_max, 5)),
        "monte_carlo": monte_carlo(
            sides=[8, 12, 16, 24],
            probabilities=[0.40, 0.45, 0.50, 0.55, 0.60],
            trials=args.trials,
            seed=args.seed,
        ),
        "algorithm_benchmark": {
            "status": "COMPUTATIONAL; MACHINE-DEPENDENT",
            "python": platform.python_version(),
            "platform": platform.platform(),
            "rows": algorithm_benchmark(
                sides=[8, 12, 16, 24],
                trials=args.benchmark_trials,
                repeats=args.benchmark_repeats,
                seed=args.seed + 1,
            ),
        },
        "interpretation_limits": [
            "The exhaustive rows certify only the enumerated finite boards.",
            "Monte Carlo rows are finite-sample estimates, not asymptotic proofs.",
            "The Y local majority rule does not imply three-voter Kemeny hardness.",
            "Timing ratios are environment-specific and are not complexity bounds.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print("wrote", args.output)


if __name__ == "__main__":
    main()
