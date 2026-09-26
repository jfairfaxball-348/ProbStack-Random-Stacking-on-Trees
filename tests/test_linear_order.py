from itertools import product
import math

from prob_stack.linear_order import (
    LOG2_E,
    binary_partition_cumulative_exact,
    colored_slack_count_exact,
    dyadic_phase,
    dyadic_simplex_count_exact,
    log_mean_linear_rate,
    low_phase_linear_coefficient,
    one_sided_beta,
    one_sided_linear_rate,
    positive_entry_count_exact,
    positive_entry_linear_coefficient,
    positive_entry_necessary_parameters,
    low_phase_necessary_parameters,
    certified_front_beta,
    certified_global_lower_center,
    refined_global_center,
    refined_global_upper_center,
    robust_descent_linear_coefficient,
)


def transfer(value: int) -> int:
    if value <= 1:
        return 2 * value - 3
    if value == 2:
        return 1
    if value == 3:
        return 0
    if value % 2 == 0:
        return value // 2
    return (value - 3) // 2


def brute_positive_count(start: int, steps: int, terminal: int) -> int:
    maximum_effective = (terminal + 3) * (2**steps) - 3
    occupancy_cap = maximum_effective - start
    result = 0
    for occupancies in product(range(occupancy_cap + 1), repeat=steps):
        message = start
        valid = True
        for index, occupancy in enumerate(occupancies):
            message = transfer(message + occupancy)
            if index < steps - 1 and message <= 1:
                valid = False
                break
        if valid and message == terminal:
            result += 1
    return result


def test_unrestricted_binary_partition_identity_when_cutoff_is_above_budget():
    for budget in range(0, 40):
        steps = max(1, math.ceil(math.log2(budget + 1)))
        assert 2**steps > budget
        assert (
            dyadic_simplex_count_exact(steps, budget)
            == binary_partition_cumulative_exact(budget)
        )


def test_positive_entry_reverse_dp_matches_bruteforce():
    for terminal in (0, 1):
        for steps in (1, 2, 3):
            for start in range(2, 7):
                assert positive_entry_count_exact(start, steps, terminal) == (
                    brute_positive_count(start, steps, terminal)
                )


def test_colored_slack_generating_function_small_cases():
    for steps in (1, 2, 3):
        weights = [2**j for j in range(steps)]
        for budget in range(0, 25):
            direct = 0
            ranges = [range(budget // weight + 1) for weight in weights]
            for ys in product(*ranges):
                if sum(w * y for w, y in zip(weights, ys)) != budget:
                    continue
                multiplicity = math.prod(1 if y <= 2 else 2 for y in ys)
                direct += multiplicity
            assert colored_slack_count_exact(steps, budget) == direct


def test_terminal_specific_coefficients_choose_zero_route():
    for theta in (0.51, 0.6, 0.75, 1.0):
        route_zero = (
            positive_entry_linear_coefficient(theta, 0)
            + low_phase_linear_coefficient(theta, 0)
        )
        route_one = (
            positive_entry_linear_coefficient(theta, 1)
            + low_phase_linear_coefficient(theta, 1)
        )
        mixed_zero_to_one = (
            positive_entry_linear_coefficient(theta, 0)
            + low_phase_linear_coefficient(theta, 1)
        )
        mixed_one_to_zero_with_bridge = (
            positive_entry_linear_coefficient(theta, 1)
            + low_phase_linear_coefficient(theta, 0)
            + 1.0
        )
        assert math.isclose(route_zero, one_sided_beta(theta))
        assert route_zero < route_one
        assert route_zero < mixed_zero_to_one
        assert route_zero < mixed_one_to_zero_with_bridge


def test_phase_cancels_in_log_mean_parameterization():
    for mean in (33, 47, 64, 73, 101, 128, 181, 255, 256, 511):
        level, theta = dyadic_phase(mean)
        ceiling_rate = one_sided_linear_rate(mean)
        x_rate = log_mean_linear_rate(mean)
        assert abs(ceiling_rate - x_rate) < 20 * math.log2(level + 1)
        assert 0.5 < theta <= 1.0


def test_refined_global_centers_and_certificate_gap():
    for log2_n in (400.0, 1600.0, 10000.0):
        root = math.sqrt(log2_n)
        upper = root - math.log2(root) + math.log2(3.0) + LOG2_E
        lower = root - math.log2(root) + 0.5 * math.log2(3.0) + LOG2_E
        assert math.isclose(refined_global_center(log2_n), upper)
        assert math.isclose(refined_global_upper_center(log2_n), upper)
        assert math.isclose(certified_global_lower_center(log2_n), lower)
        assert math.isclose(upper - lower, 0.5 * math.log2(3.0))


def test_state_independent_certificate_linear_coefficient():
    for theta in (0.51, 0.6, 0.75, 1.0):
        assert math.isclose(
            robust_descent_linear_coefficient(theta)
            + low_phase_linear_coefficient(theta, 0),
            certified_front_beta(theta),
        )
        assert certified_front_beta(theta) > one_sided_beta(theta)


def test_terminal_specific_necessary_budgets():
    for mean in (16, 31, 32, 47, 64, 100):
        level, _ = dyadic_phase(mean)
        for terminal in (0, 1):
            steps, budget = positive_entry_necessary_parameters(mean, terminal)
            assert steps == level - 2
            assert budget == (terminal + 3) * 2**steps - 5
        for start in (0, 1):
            steps, budget = low_phase_necessary_parameters(mean, start)
            assert steps == level - 2
            assert budget == (3 - start) * 2 ** (steps - 1) - 2
