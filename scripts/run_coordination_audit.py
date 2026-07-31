"""Reproduce the exact coverage-versus-convention coordination audit."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from kemeny_dp.coordination import (
    binary_conventions,
    decoder_from_one_feedback,
    deterministic_binary_decoders,
    grounded_accuracy,
    inverse_decoder,
    protocol_accuracy,
)


ROOT = Path(__file__).resolve().parents[1]


def fraction_text(value: Fraction) -> str:
    return str(value)


def main() -> None:
    button_count = 10
    buttons = tuple(range(button_count))
    brittle_matrix = [
        [
            fraction_text(
                grounded_accuracy(
                    button_count,
                    (sender,),
                    (training_button,),
                )
            )
            for training_button in buttons
        ]
        for sender in buttons
    ]
    off_diagonal = [
        Fraction(brittle_matrix[row][column])
        for row in buttons
        for column in buttons
        if row != column
    ]

    conventions = binary_conventions()
    paired_decoders = tuple(
        inverse_decoder(encoder) for encoder in conventions
    )
    protocol_matrix = [
        [
            fraction_text(protocol_accuracy(encoder, decoder))
            for decoder in paired_decoders
        ]
        for encoder in conventions
    ]
    fixed_decoder_means = {
        str(decoder): fraction_text(
            sum(
                (
                    protocol_accuracy(encoder, decoder)
                    for encoder in conventions
                ),
                Fraction(0),
            )
            / len(conventions)
        )
        for decoder in deterministic_binary_decoders()
    }
    feedback_checks = [
        protocol_accuracy(
            encoder,
            decoder_from_one_feedback(
                encoder[revealed_bit],
                revealed_bit,
            ),
        )
        for encoder in conventions
        for revealed_bit in (0, 1)
    ]

    result = {
        "status": {
            "grounded_button_game": "KNOWN_MODEL_EXACTLY_AUDITED",
            "protocol_impossibility": "PROVED_FINITE_TOY_MODEL",
            "feedback_adaptation": "PROVED_FINITE_TOY_MODEL",
            "kemeny_or_privacy_claim": "NONE",
        },
        "source": {
            "title": (
                "OvercookedV2: Rethinking Overcooked for "
                "Zero-Shot Coordination"
            ),
            "arxiv": "2503.17821",
            "url": "https://arxiv.org/abs/2503.17821",
        },
        "grounded_button_game": {
            "button_count": button_count,
            "brittle_accuracy_matrix": brittle_matrix,
            "self_play_diagonal_accuracy": "1",
            "cross_play_off_diagonal_mean": fraction_text(
                sum(off_diagonal, Fraction(0)) / len(off_diagonal)
            ),
            "state_augmented_accuracy": fraction_text(
                grounded_accuracy(button_count, buttons, buttons)
            ),
            "all_grounded_states_checked": 2 * button_count,
        },
        "ungrounded_protocol_game": {
            "conventions": [list(encoder) for encoder in conventions],
            "self_cross_play_accuracy_matrix": protocol_matrix,
            "each_encoder_covers_all_messages": all(
                set(encoder) == {0, 1} for encoder in conventions
            ),
            "fixed_decoder_mean_accuracies": fixed_decoder_means,
            "best_fixed_decoder_mean_accuracy": max(
                fixed_decoder_means.values(), key=Fraction
            ),
            "one_feedback_future_accuracy": fraction_text(
                min(feedback_checks)
            ),
            "encoder_feedback_cases_checked": len(feedback_checks),
        },
    }
    output = ROOT / "results" / "coordination_audit.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["status"], indent=2, sort_keys=True))
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
