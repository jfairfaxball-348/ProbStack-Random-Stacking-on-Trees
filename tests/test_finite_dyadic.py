from fractions import Fraction
from itertools import product

from prob_stack.finite_dyadic import (
    binary_partition_cumulative_exact,
    binary_partition_cumulative_recurrence,
    colored_slack_count_direct,
    colored_slack_slice_count,
    dyadic_simplex_binary_partition_coefficient,
    dyadic_simplex_count_exact,
    dyadic_simplex_mass_counts,
    dyadic_weighted_sum,
    geometric_simplex_product_probability_exact,
    low_budget_final,
    low_budget_final_closed_form,
    low_budget_holds,
    low_phase_simplex_budget,
    low_phase_simplex_certificate,
    low_phase_simplex_event,
    positive_descent_budget,
    positive_descent_count_exact,
    positive_descent_event,
    positive_descent_product_probability_exact,
    sharp_finite_seed,
)


def brute_vectors(steps: int, budget: int, *, reverse: bool = False):
    if budget < 0:
        return []
    weights = [2**j for j in range(steps)]
    if reverse:
        weights.reverse()
    ranges = [range(budget // w + 1) for w in weights]
    return [
        xs
        for xs in product(*ranges)
        if sum(w * x for w, x in zip(weights, xs)) <= budget
    ]


def test_binary_partition_coefficient_identity_exhaustive_small():
    for steps in range(0, 6):
        for budget in range(0, 35):
            direct = dyadic_simplex_count_exact(steps, budget)
            coefficient = dyadic_simplex_binary_partition_coefficient(
                steps, budget
            )
            assert direct == coefficient


def test_unrestricted_cumulative_recurrence_and_cutoff_identity():
    for budget in range(0, 80):
        assert binary_partition_cumulative_exact(
            budget
        ) == binary_partition_cumulative_recurrence(budget)
        steps = max(0, budget.bit_length())
        assert (1 << steps) > budget or budget == 0
        assert dyadic_simplex_count_exact(
            steps, budget
        ) == binary_partition_cumulative_exact(budget)


def test_mass_counts_match_ordered_vector_enumeration_and_reversal():
    for steps in range(1, 5):
        for budget in range(0, 20):
            for reverse in (False, True):
                vectors = brute_vectors(steps, budget, reverse=reverse)
                counts = dyadic_simplex_mass_counts(
                    steps, budget, reverse=reverse
                )
                brute = [0] * (
                    max((sum(xs) for xs in vectors), default=0) + 1
                )
                for xs in vectors:
                    brute[sum(xs)] += 1
                assert tuple(brute) == counts
                assert dyadic_simplex_count_exact(
                    steps, budget, reverse=reverse
                ) == dyadic_simplex_count_exact(steps, budget)


def test_positive_descent_strict_inequality_is_exact_budget():
    for mean in range(1, 12):
        for steps in range(0, 7):
            budget = positive_descent_budget(mean, steps)
            vectors = brute_vectors(steps, max(0, budget + 1))
            accepted = [
                xs for xs in vectors if positive_descent_event(mean, xs)
            ]
            assert len(accepted) == positive_descent_count_exact(
                mean, steps
            )
            for xs in accepted:
                assert dyadic_weighted_sum(xs) <= budget
            boundary = [
                xs
                for xs in vectors
                if dyadic_weighted_sum(xs) == budget + 1
            ]
            assert all(
                not positive_descent_event(mean, xs) for xs in boundary
            )


def test_exact_geometric_mass_agrees_with_direct_atom_sum():
    for mean in (2, 3, 5):
        p = Fraction(1, mean + 1)
        r = Fraction(mean, mean + 1)
        for steps in range(1, 4):
            for budget in range(0, 12):
                vectors = brute_vectors(steps, budget)
                direct = sum(
                    (p**steps * r ** sum(xs) for xs in vectors),
                    Fraction(0, 1),
                )
                assert geometric_simplex_product_probability_exact(
                    mean, steps, budget
                ) == direct


def test_positive_descent_product_probability_uses_exact_budget():
    for mean, steps in ((3, 4), (5, 5), (8, 6), (16, 6)):
        budget = positive_descent_budget(mean, steps)
        assert positive_descent_product_probability_exact(
            mean, steps
        ) == geometric_simplex_product_probability_exact(
            mean, steps, budget
        )


def test_low_budget_closed_form_and_simplex_implication_exhaustive():
    for deficit in range(2, 7):
        for steps in range(0, 5):
            budget = low_phase_simplex_budget(deficit, steps)
            for xs in brute_vectors(steps, budget, reverse=True):
                assert low_phase_simplex_event(deficit, xs)
                assert low_budget_final(
                    deficit, xs
                ) == low_budget_final_closed_form(deficit, xs)
                assert low_budget_holds(deficit, xs)
                assert low_phase_simplex_certificate(deficit, xs)


def test_session6_sharp_seed_has_frozen_support_and_budgets():
    seed = sharp_finite_seed(16)
    assert seed.level == 4
    assert seed.descent_steps == 6
    assert seed.descent_budget == 31
    assert seed.amplification_steps == 4
    assert seed.amplification_budget == 8
    assert seed.support_length == 10
    assert seed.product_probability > 0


def test_colored_slack_telescoping_slice_identity_exhaustive_small():
    for steps in range(0, 6):
        for budget in range(0, 45):
            assert colored_slack_count_direct(
                steps, budget
            ) == colored_slack_slice_count(steps, budget)


def test_regressions_for_weight_orientation_zeroes_and_ordering():
    assert dyadic_weighted_sum((1, 0, 0)) == 1
    assert dyadic_weighted_sum((1, 0, 0), reverse=True) == 4
    assert dyadic_simplex_count_exact(4, 0) == 1
    assert dyadic_weighted_sum((2, 0)) <= 2
    assert dyadic_weighted_sum((0, 2)) > 2


def test_exact_counts_have_negative_L_log_L_direction():
    for level in (4, 6, 8, 10):
        count = dyadic_simplex_count_exact(level, 2**level)
        assert count < 2 ** (level * level // 2)
