import unittest
from fractions import Fraction

from kemeny_dp.coordination import (
    binary_conventions,
    decoder_from_one_feedback,
    deterministic_binary_decoders,
    grounded_accuracy,
    grounded_bulb,
    inverse_decoder,
    memorized_button_guess,
    parity_guess,
    protocol_accuracy,
)


class CoordinationTests(unittest.TestCase):
    def test_grounded_parity_is_partner_independent_exhaustively(self):
        for button_count in range(1, 9):
            for button in range(button_count):
                for hidden_bit in (0, 1):
                    bulb = grounded_bulb(
                        button, hidden_bit, button_count
                    )
                    self.assertEqual(
                        parity_guess(bulb, button_count), hidden_bit
                    )

    def test_brittle_self_play_and_cross_play_matrix(self):
        button_count = 10
        for sender in range(button_count):
            for receiver_training_button in range(button_count):
                accuracy = grounded_accuracy(
                    button_count,
                    (sender,),
                    (receiver_training_button,),
                )
                self.assertEqual(
                    accuracy,
                    Fraction(1)
                    if sender == receiver_training_button
                    else Fraction(1, 2),
                )

    def test_state_augmentation_closes_grounded_coverage_gap(self):
        button_count = 10
        all_buttons = tuple(range(button_count))
        for sender in range(button_count):
            self.assertEqual(
                grounded_accuracy(
                    button_count,
                    (sender,),
                    all_buttons,
                ),
                Fraction(1),
            )

    def test_unseen_button_uses_declared_fallback(self):
        bulb = grounded_bulb(3, 1, 5)
        self.assertEqual(
            memorized_button_guess(
                bulb, 5, (0, 1), fallback_bit=0
            ),
            0,
        )

    def test_ungrounded_protocol_matrix(self):
        conventions = binary_conventions()
        decoders = tuple(inverse_decoder(encoder) for encoder in conventions)
        self.assertEqual(
            tuple(
                tuple(
                    protocol_accuracy(encoder, decoder)
                    for decoder in decoders
                )
                for encoder in conventions
            ),
            ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))),
        )

    def test_no_fixed_decoder_beats_half_across_both_conventions(self):
        conventions = binary_conventions()
        for decoder in deterministic_binary_decoders():
            mean_accuracy = sum(
                (
                    protocol_accuracy(encoder, decoder)
                    for encoder in conventions
                ),
                Fraction(0),
            ) / len(conventions)
            self.assertEqual(mean_accuracy, Fraction(1, 2))

    def test_both_messages_are_covered_but_cross_play_can_fail(self):
        identity, flipped = binary_conventions()
        self.assertEqual(set(identity), {0, 1})
        self.assertEqual(set(flipped), {0, 1})
        self.assertEqual(
            protocol_accuracy(identity, inverse_decoder(flipped)),
            Fraction(0),
        )

    def test_one_feedback_observation_identifies_binary_convention(self):
        for encoder in binary_conventions():
            for revealed_bit in (0, 1):
                observed_message = encoder[revealed_bit]
                decoder = decoder_from_one_feedback(
                    observed_message, revealed_bit
                )
                self.assertEqual(
                    protocol_accuracy(encoder, decoder), Fraction(1)
                )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            grounded_bulb(0, 2, 1)
        with self.assertRaises(ValueError):
            parity_guess(2, 1)
        with self.assertRaises(ValueError):
            grounded_accuracy(2, (), (0,))
        with self.assertRaises(ValueError):
            inverse_decoder((0, 0))
        with self.assertRaises(ValueError):
            protocol_accuracy((0, 2), (0, 1))


if __name__ == "__main__":
    unittest.main()
