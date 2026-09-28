import math
from fractions import Fraction
from itertools import product

from prob_stack.binary_partition_asymptotics import (
    low_amplification_regime,
    necessary_low_phase_regime,
    necessary_positive_entry_regime,
    positive_descent_regime,
)
from prob_stack.finite_dyadic import (
    dyadic_weighted_sum,
    geometric_simplex_product_probability_exact,
)
from prob_stack.linear_order import (
    geometric_simplex_linear_cost_coefficient,
    low_phase_linear_coefficient,
    one_sided_beta,
    positive_entry_linear_coefficient,
)
from prob_stack.product_geometric_asymptotics import (
    geometric_simplex_product_probability_exact_fast,
    geometric_tilt_log2_bounds,
    geometric_tilt_uniform_constant,
    local_excursion_beta,
    necessary_low_linear_coefficient,
    necessary_positive_linear_coefficient,
    probability_diagnostic,
    sharp_low_linear_coefficient,
    sharp_positive_linear_coefficient,
    sharp_seed_beta,
    simplex_probability_linear_coefficient,
)


def brute_vectors(steps: int, budget: int, *, reverse: bool = False):
    weights = [1 << j for j in range(steps)]
    if reverse:
        weights.reverse()
    ranges = [range(budget // weight + 1) for weight in weights]
    for xs in product(*ranges):
        if sum(weight * x for weight, x in zip(weights, xs)) <= budget:
            yield xs


def test_ordinary_mass_is_bounded_by_dyadic_budget_in_both_orientations():
    for steps in range(1, 5):
        for budget in range(0, 15):
            for reverse in (False, True):
                for xs in brute_vectors(steps, budget, reverse=reverse):
                    assert sum(xs) <= dyadic_weighted_sum(xs, reverse=reverse)
                    assert sum(xs) <= budget


def test_fast_exact_weighted_dp_matches_existing_mass_profile_probability():
    for mean in (2, 3, 5):
        for steps in range(0, 4):
            for budget in range(0, 12):
                for reverse in (False, True):
                    assert geometric_simplex_product_probability_exact_fast(
                        mean, steps, budget, reverse=reverse
                    ) == geometric_simplex_product_probability_exact(
                        mean, steps, budget, reverse=reverse
                    )


def test_reversal_preserves_product_geometric_simplex_probability():
    for mean in (3, 8, 16):
        for steps, budget in ((1, 5), (3, 9), (4, 13)):
            forward = geometric_simplex_product_probability_exact_fast(
                mean, steps, budget
            )
            reverse = geometric_simplex_product_probability_exact_fast(
                mean, steps, budget, reverse=True
            )
            assert forward == reverse


def test_geometric_tilt_is_rigourously_sandwiched_and_nontrivial():
    mean = 16
    regime = positive_descent_regime(mean)
    diagnostic = probability_diagnostic(mean, regime, exact_fraction=True)
    lower, upper = geometric_tilt_log2_bounds(mean, regime.budget)
    assert lower <= diagnostic.tilt_log2 <= upper
    assert diagnostic.tilt_log2 < 0.0
    assert diagnostic.tilt_log2 > lower
    assert geometric_tilt_uniform_constant(mean, regime.budget) < 3.0
    assert math.isclose(
        diagnostic.log2_probability,
        diagnostic.exact_log2_probability,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_general_probability_linear_coefficient_matches_session7_formula():
    for theta in (9 / 16, 3 / 4, 1.0):
        for step_offset, scale in ((-2, 3 / 4), (0, 1 / 2), (2, 5 / 2)):
            assert math.isclose(
                simplex_probability_linear_coefficient(
                    theta,
                    step_offset=step_offset,
                    budget_scale=scale,
                ),
                geometric_simplex_linear_cost_coefficient(
                    theta,
                    step_offset=step_offset,
                    budget_scale=scale,
                ),
            )


def test_sharp_positive_and_low_coefficients_and_strict_budget():
    for theta in (9 / 16, 3 / 4, 1.0):
        mean = int(theta * (1 << 8))
        positive = positive_descent_regime(mean)
        low = low_amplification_regime(mean)
        assert positive.steps == 10
        assert positive.budget == (1 << 10) - 2 * mean - 1
        assert low.steps == 8
        assert low.budget == 1 << 7

        expected_positive = (
            1.5
            + math.log2(theta)
            - math.log2(4.0 - 2.0 * theta)
            - math.log2(math.e)
        )
        expected_low = math.log2(theta) + 0.5 - math.log2(math.e)
        assert math.isclose(
            sharp_positive_linear_coefficient(theta), expected_positive
        )
        assert math.isclose(sharp_low_linear_coefficient(theta), expected_low)


def test_necessary_coefficients_rederive_session7_exactly():
    for theta in (9 / 16, 3 / 4, 1.0):
        for terminal in (0, 1):
            assert math.isclose(
                necessary_positive_linear_coefficient(theta, terminal),
                positive_entry_linear_coefficient(theta, terminal),
            )
        for start in (0, 1):
            assert math.isclose(
                necessary_low_linear_coefficient(theta, start),
                low_phase_linear_coefficient(theta, start),
            )


def test_sharp_seed_beta_is_not_the_optimized_local_excursion_beta():
    for theta in (9 / 16, 3 / 4, 1.0):
        beta_seed = sharp_seed_beta(theta)
        beta_local = local_excursion_beta(theta)
        assert math.isclose(beta_local, one_sided_beta(theta))
        assert beta_seed > beta_local
        assert math.isclose(
            beta_seed,
            sharp_positive_linear_coefficient(theta)
            + sharp_low_linear_coefficient(theta),
        )


def test_probability_diagnostic_selects_positive_L_log_L_and_p_factor():
    level = 10
    theta = 3 / 4
    mean = 3 * (1 << (level - 2))
    regime = positive_descent_regime(mean)
    diagnostic = probability_diagnostic(mean, regime)
    coefficient = sharp_positive_linear_coefficient(theta)

    correct = (
        0.5 * level**2
        + level * math.log2(level)
        + coefficient * level
    )
    wrong_sign = (
        0.5 * level**2
        - level * math.log2(level)
        + coefficient * level
    )
    actual = -diagnostic.log2_probability
    assert abs(actual - correct) < abs(actual - wrong_sign)

    # Omitting p^k would miss a contribution of order L^2.
    assert -diagnostic.log2_p_factor > 0.8 * level**2


def test_sharp_and_necessary_simplices_cannot_be_confused():
    mean = 1 << 8
    sharp = positive_descent_regime(mean)
    necessary = necessary_positive_entry_regime(mean, 0)
    low_sharp = low_amplification_regime(mean)
    low_necessary = necessary_low_phase_regime(mean, 0)

    assert sharp.steps == 10
    assert necessary.steps == 6
    assert sharp.budget != necessary.budget
    assert low_sharp.steps == 8
    assert low_necessary.steps == 6
    assert low_sharp.budget != low_necessary.budget
