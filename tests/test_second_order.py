from itertools import product
import math

from prob_stack.second_order import (
    amplification_witness_parameters,
    conditioned_nonstackable_second_order_log2_upper,
    descent_witness_parameters,
    dyadic_small_ball_log2_bounds,
    dyadic_small_ball_probability_exact,
    dyadic_weighted_sum,
    finite_block_second_order_bounds,
    necessary_entry_parameters,
    necessary_low_parameters,
    second_order_center,
    second_order_deep_cover_holds,
    second_order_deep_message_cover,
    second_order_rate,
)
from prob_stack.tree_score import transfer


def test_dyadic_small_ball_count_bounds_cover_exact_dp():
    for mean in (3, 5, 8):
        for steps in (2, 3, 4):
            for budget in (3, 5, 9, 15):
                exact = float(
                    dyadic_small_ball_probability_exact(
                        mean, steps, budget
                    )
                )
                lower, upper = dyadic_small_ball_log2_bounds(
                    mean, steps, budget
                )
                assert 2**lower <= exact * (1 + 1e-12)
                assert exact <= 2**upper * (1 + 1e-12)


def test_descent_simplex_forces_nonpositive_message_at_mean_16():
    mean = 16
    steps, budget = descent_witness_parameters(mean)
    ranges = [
        range(budget // (2**j) + 1)
        for j in range(steps)
    ]
    checked = 0
    for occupancies in product(*ranges):
        if dyadic_weighted_sum(occupancies) > budget:
            continue
        checked += 1
        for start in (mean, 2 * mean):
            message = start
            for occupancy in occupancies:
                message = transfer(message + occupancy)
            assert message <= 0
    assert checked > 100


def test_amplification_simplex_stays_low_and_forces_deep_at_mean_16():
    mean = 16
    steps, budget = amplification_witness_parameters(mean)
    ranges = [
        range(
            budget // (2 ** (steps - 1 - j)) + 1
        )
        for j in range(steps)
    ]
    checked = 0
    for occupancies in product(*ranges):
        if (
            dyadic_weighted_sum(
                occupancies, reverse=True
            )
            > budget
        ):
            continue
        checked += 1
        message = 0
        for occupancy in occupancies:
            assert message + occupancy <= 1
            message = transfer(message + occupancy)
        assert message <= -mean
    assert checked > 10


def test_necessary_simplex_parameters_are_well_formed():
    for mean in (16, 32, 64, 100):
        steps, entry_budget = necessary_entry_parameters(mean)
        low_steps, low_budget = necessary_low_parameters(
            mean, initial_deficit_cap=3
        )
        assert steps >= 2
        assert low_steps == steps
        assert entry_budget > 0
        assert low_budget > 0


def test_second_order_bounds_are_ordered_and_track_rate():
    for level in (6, 8, 10, 12, 16, 20):
        mean = 2**level
        bounds = finite_block_second_order_bounds(mean)
        assert (
            bounds.lower_log2_probability
            <= bounds.upper_log2_probability
            <= 0
        )
        rate = second_order_rate(level)
        assert (
            abs(
                -bounds.lower_log2_probability
                - rate
            )
            < 20 * level
        )
        assert (
            abs(
                -bounds.upper_log2_probability
                - rate
            )
            < 20 * level
        )


def test_second_order_deep_cover_exhaustive_small_alphabet():
    for occupancies in product(range(7), repeat=6):
        assert second_order_deep_cover_holds(
            occupancies, 16
        )


def test_second_order_supercritical_cover_has_expected_scales():
    for level in (8, 10, 12, 16, 20):
        mean = 2**level
        cover = second_order_deep_message_cover(mean)
        assert (
            cover.cluster_log2_probability
            <= cover.low_log2_probability_upper + 1e-12
        )
        assert (
            cover.max_window_mass
            >= cover.cluster_cap * cover.cluster_steps
        )
        assert (
            abs(
                -cover.interior_log2_probability_upper
                - second_order_rate(level)
            )
            < 20 * level
        )


def test_second_order_conditioned_upper_decays_above_shifted_center():
    for level in (20, 30, 40):
        root = level + math.log2(level) - 5
        log2_n = round(root * root)
        n = 2**log2_n
        assert (
            conditioned_nonstackable_second_order_log2_upper(
                2**level, n
            )
            < -20
        )
    assert (
        second_order_center(400)
        == 20 - math.log2(20)
    )
