"""Exact toy models separating state coverage from true coordination."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from fractions import Fraction

BinaryProtocol = tuple[int, int]


def _validate_bit(value: int, *, name: str) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be zero or one")


def _validate_buttons(
    buttons: Iterable[int], button_count: int
) -> tuple[int, ...]:
    if button_count < 1:
        raise ValueError("button_count must be positive")
    normalized = tuple(buttons)
    if not normalized:
        raise ValueError("at least one sender button is required")
    if any(
        not isinstance(button, int)
        or not 0 <= button < button_count
        for button in normalized
    ):
        raise ValueError("button index is outside the game")
    return normalized


def grounded_bulb(button: int, hidden_bit: int, button_count: int) -> int:
    """Return the OvercookedV2 Button Game observation ``2a + bit``."""
    _validate_bit(hidden_bit, name="hidden_bit")
    normalized = _validate_buttons((button,), button_count)
    return 2 * normalized[0] + hidden_bit


def parity_guess(bulb: int, button_count: int) -> int:
    """Decode the grounded bit from the parity of a valid bulb index."""
    if not isinstance(bulb, int) or not 0 <= bulb < 2 * button_count:
        raise ValueError("bulb index is outside the game")
    return bulb % 2


def memorized_button_guess(
    bulb: int,
    button_count: int,
    known_buttons: Iterable[int],
    *,
    fallback_bit: int = 0,
) -> int:
    """Use parity on covered buttons and a fixed guess on unseen buttons."""
    _validate_bit(fallback_bit, name="fallback_bit")
    if not isinstance(bulb, int) or not 0 <= bulb < 2 * button_count:
        raise ValueError("bulb index is outside the game")
    known = set(_validate_buttons(known_buttons, button_count))
    button = bulb // 2
    return bulb % 2 if button in known else fallback_bit


def grounded_accuracy(
    button_count: int,
    sender_buttons: Sequence[int],
    known_buttons: Iterable[int],
    *,
    fallback_bit: int = 0,
) -> Fraction:
    """Exact uniform-bit, uniform-sender-button accuracy of a brittle decoder."""
    senders = _validate_buttons(sender_buttons, button_count)
    known = tuple(known_buttons)
    successes = 0
    trials = 0
    for button in senders:
        for hidden_bit in (0, 1):
            bulb = grounded_bulb(button, hidden_bit, button_count)
            guess = memorized_button_guess(
                bulb,
                button_count,
                known,
                fallback_bit=fallback_bit,
            )
            successes += int(guess == hidden_bit)
            trials += 1
    return Fraction(successes, trials)


def _validate_protocol(protocol: BinaryProtocol, *, name: str) -> None:
    if len(protocol) != 2 or any(value not in (0, 1) for value in protocol):
        raise ValueError(f"{name} must map two binary inputs to binary outputs")


def binary_conventions() -> tuple[BinaryProtocol, BinaryProtocol]:
    """Return the identity and flipped bijective signalling conventions."""
    return ((0, 1), (1, 0))


def deterministic_binary_decoders() -> tuple[BinaryProtocol, ...]:
    """Return all deterministic decoders from one bit to one bit."""
    return ((0, 0), (0, 1), (1, 0), (1, 1))


def inverse_decoder(encoder: BinaryProtocol) -> BinaryProtocol:
    """Return the decoder paired with a bijective binary encoder."""
    _validate_protocol(encoder, name="encoder")
    if set(encoder) != {0, 1}:
        raise ValueError("encoder must be a bijective binary convention")
    result = [0, 0]
    for hidden_bit, message in enumerate(encoder):
        result[message] = hidden_bit
    return (result[0], result[1])


def protocol_accuracy(
    encoder: BinaryProtocol, decoder: BinaryProtocol
) -> Fraction:
    """Exact accuracy under a uniform hidden bit."""
    _validate_protocol(encoder, name="encoder")
    _validate_protocol(decoder, name="decoder")
    successes = sum(
        decoder[encoder[hidden_bit]] == hidden_bit
        for hidden_bit in (0, 1)
    )
    return Fraction(successes, 2)


def decoder_from_one_feedback(
    observed_message: int, revealed_bit: int
) -> BinaryProtocol:
    """Infer a bijective convention from one labeled interaction."""
    _validate_bit(observed_message, name="observed_message")
    _validate_bit(revealed_bit, name="revealed_bit")
    if observed_message == revealed_bit:
        return (0, 1)
    return (1, 0)
