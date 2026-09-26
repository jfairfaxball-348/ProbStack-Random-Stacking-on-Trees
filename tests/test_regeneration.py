from fractions import Fraction

from prob_stack.regeneration import (
    absolute_regeneration_lower_bound,
    regeneration_forces_window,
    regeneration_interval,
    regeneration_probability,
    worst_case_regeneration_probability,
)


def test_regeneration_interval_forces_optimal_window_exhaustively():
    for mean in (16, 17, 24, 31, 32, 47, 64):
        for message in range(-mean + 1, 2 * mean + 1):
            lower, upper = regeneration_interval(mean, message)
            for occupancy in range(lower, upper + 1):
                assert regeneration_forces_window(mean, message, occupancy)


def test_worst_case_probability_is_exactly_at_left_endpoint():
    for mean in (16, 17, 24, 32, 48, 64):
        probabilities = [
            regeneration_probability(mean, message)
            for message in range(-mean + 1, 2 * mean + 1)
        ]
        assert min(probabilities) == probabilities[0]
        assert probabilities[0] == worst_case_regeneration_probability(mean)


def test_uniform_absolute_constant_is_valid():
    lower = absolute_regeneration_lower_bound()
    assert 0.023 < lower < 0.024
    for mean in range(16, 257):
        assert float(worst_case_regeneration_probability(mean)) >= lower


def test_regeneration_mass_is_constant_multiple_of_mean():
    for mean in range(16, 80):
        for message in (-mean + 1, 0, mean, 2 * mean):
            lower, upper = regeneration_interval(mean, message)
            assert 0 <= lower <= upper <= 5 * mean - 1


def test_exact_probability_formula():
    for mean in (16, 32, 64):
        r = Fraction(mean, mean + 1)
        message = -mean + 1
        expected = r ** (3 * mean + 1) * (1 - r ** (2 * mean - 1))
        assert regeneration_probability(mean, message) == expected
