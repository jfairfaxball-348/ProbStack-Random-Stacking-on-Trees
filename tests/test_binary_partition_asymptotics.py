import math

from prob_stack.binary_partition_asymptotics import (
    LOG2_E,
    de_bruijn_linear_coefficient,
    exact_diagnostic,
    low_amplification_regime,
    necessary_low_phase_regime,
    necessary_positive_entry_regime,
    positive_descent_regime,
    truncation_tail_factor_bound,
    unrestricted_cutoff_holds,
)
from prob_stack.finite_dyadic import (
    binary_partition_cumulative_recurrence,
    colored_slack_slice_count,
    dyadic_simplex_count_exact,
)


def test_exact_cutoff_for_sharp_session6_simplices():
    for level in range(4, 11):
        for numerator, denominator in ((9, 16), (3, 4), (1, 1)):
            mean = numerator * (1 << level) // denominator
            descent = positive_descent_regime(mean)
            assert descent.level == level
            assert descent.budget == (1 << (level + 2)) - 2 * mean - 1
            assert descent.cutoff_is_exact
            assert dyadic_simplex_count_exact(
                descent.steps, descent.budget
            ) == binary_partition_cumulative_recurrence(descent.budget)

        low = low_amplification_regime(1 << level)
        assert low.steps == level
        assert low.budget == 1 << (level - 1)
        assert low.cutoff_is_exact


def test_truncation_tail_factor_bound_exhaustive_small():
    for steps in range(0, 6):
        for budget in range(0, 50):
            finite = dyadic_simplex_count_exact(steps, budget)
            unrestricted = binary_partition_cumulative_recurrence(budget)
            factor = truncation_tail_factor_bound(steps, budget)
            assert finite <= unrestricted <= factor * finite
            if unrestricted_cutoff_holds(steps, budget):
                assert finite == unrestricted


def test_session7_necessary_simplex_cutoffs_and_bounded_factors():
    for level in range(6, 11):
        mean = 1 << level

        pos0 = necessary_positive_entry_regime(mean, 0)
        pos1 = necessary_positive_entry_regime(mean, 1)
        assert pos0.steps == pos1.steps == level - 2
        assert pos0.budget == 3 * (1 << (level - 2)) - 5
        assert pos1.budget == 4 * (1 << (level - 2)) - 5
        assert not pos0.cutoff_is_exact
        assert not pos1.cutoff_is_exact
        assert pos0.tail_factor_bound == 4
        assert pos1.tail_factor_bound == 6

        low0 = necessary_low_phase_regime(mean, 0)
        low1 = necessary_low_phase_regime(mean, 1)
        assert low0.budget == 3 * (1 << (level - 3)) - 2
        assert low1.budget == 2 * (1 << (level - 3)) - 2
        assert not low0.cutoff_is_exact
        assert low0.tail_factor_bound == 2
        assert low1.cutoff_is_exact
        assert low1.tail_factor_bound == 1


def test_de_bruijn_linear_coefficient_has_correct_base_two_conversion():
    assert math.isclose(
        de_bruijn_linear_coefficient(0.5), LOG2_E - 0.5
    )
    assert math.isclose(
        de_bruijn_linear_coefficient(1.0), 0.5 + LOG2_E
    )
    assert math.isclose(
        de_bruijn_linear_coefficient(2.0), 1.5 + LOG2_E
    )


def test_positive_descent_theta_dependence_and_strict_minus_one():
    level = 10
    for numerator, denominator, expected_scale in (
        (9, 16, 23 / 8),
        (3, 4, 5 / 2),
        (1, 1, 2.0),
    ):
        mean = numerator * (1 << level) // denominator
        regime = positive_descent_regime(mean)
        assert math.isclose(regime.theta, numerator / denominator)
        assert math.isclose(regime.scale, expected_scale)
        assert regime.budget == int(expected_scale * (1 << level)) - 1


def test_exact_counts_select_negative_L_log_L_sign_and_correct_argument():
    for level in (8, 10, 12):
        mean = 3 * (1 << (level - 2))  # theta=3/4, lambda_+=5/2.
        diagnostic = exact_diagnostic(positive_descent_regime(mean))
        coefficient = diagnostic.linear_coefficient
        correct = (
            0.5 * level**2
            - level * math.log2(level)
            + coefficient * level
        )
        wrong_sign = (
            0.5 * level**2
            + level * math.log2(level)
            + coefficient * level
        )
        wrong_argument = (
            0.5 * level**2
            - level * math.log2(level)
            + de_bruijn_linear_coefficient((5 / 2) / 2) * level
        )
        assert abs(diagnostic.log2_count - correct) < abs(
            diagnostic.log2_count - wrong_sign
        )
        assert abs(diagnostic.log2_count - correct) < abs(
            diagnostic.log2_count - wrong_argument
        )


def test_bounded_step_shifts_do_not_enter_linear_coefficient():
    level = 10
    mean = 1 << level
    regimes = [
        low_amplification_regime(mean),
        necessary_positive_entry_regime(mean, 0),
        necessary_positive_entry_regime(mean, 1),
        necessary_low_phase_regime(mean, 0),
        necessary_low_phase_regime(mean, 1),
    ]
    for regime in regimes:
        assert math.isclose(
            de_bruijn_linear_coefficient(regime.scale),
            math.log2(regime.scale) + 0.5 + LOG2_E,
        )


def test_colored_slack_changes_only_bounded_log_scale_in_diagnostic_range():
    for steps in (4, 5, 6):
        budget = 4 * (1 << steps)
        colored = colored_slack_slice_count(steps, budget)
        cumulative = dyadic_simplex_count_exact(steps, budget)
        log_gap = math.log2(colored) - math.log2(cumulative)
        assert -2.0 < log_gap < 0.0
