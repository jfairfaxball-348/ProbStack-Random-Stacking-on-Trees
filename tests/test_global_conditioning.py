import math
from fractions import Fraction

from prob_stack.global_conditioning import (
    LOG2_3E,
    conditioning_point_log2_bounds,
    conditioning_point_probability,
    conditioning_reciprocal_bits_bounds,
    fixed_offset_scaled_residual,
    frozen_center,
    global_balance_diagnostic,
    one_block_transfer_log_bound,
    separated_blocks_transfer_log_bound,
)


def test_exact_negative_binomial_conditioning_point_probability():
    # n=3, mean=2, total=6:
    # choose(8,6) * (1/3)^3 * (2/3)^6.
    assert conditioning_point_probability(2, 3) == Fraction(1792, 19683)


def test_robbins_bounds_contain_exact_conditioning_probability():
    for mean, n in [(1, 2), (2, 3), (5, 8), (16, 20)]:
        exact_log2 = math.log2(float(conditioning_point_probability(mean, n)))
        lower, upper = conditioning_point_log2_bounds(mean, n)
        assert lower <= exact_log2 <= upper
        rec_lower, rec_upper = conditioning_reciprocal_bits_bounds(mean, n)
        assert rec_lower <= -exact_log2 <= rec_upper


def test_one_and_two_block_transfer_do_not_assume_conditional_independence():
    mean = 512
    n = 2**60
    one = one_block_transfer_log_bound(mean, n, 200, 5000)
    two = separated_blocks_transfer_log_bound(
        mean, n, 200, 5000, blocks=2
    )
    assert 0.0 <= one < two
    assert two < 1e-8


def test_frozen_center_has_minus_half_log_log_and_correct_constant():
    N = 4096.0
    expected = math.sqrt(N) - 0.5 * math.log2(N) + math.log2(3.0 * math.e)
    assert frozen_center(N) == expected
    assert math.isclose(LOG2_3E, math.log2(3.0 * math.e), rel_tol=0.0, abs_tol=1e-15)

    wrong_plus = math.sqrt(N) + 0.5 * math.log2(N) + LOG2_3E
    assert math.isclose(
        abs(frozen_center(N) - wrong_plus),
        math.log2(N),
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_fixed_offset_balance_has_the_frozen_signs():
    below = global_balance_diagnostic(4096.0, -0.5)
    above = global_balance_diagnostic(4096.0, 0.5)
    assert below.log2_n_times_local_hazard > 0.0
    assert above.log2_n_times_local_hazard < 0.0
    assert below.log2_spaced_hazard_to_conditioning_cost > 0.0
    assert above.log2_spaced_hazard_to_conditioning_cost < 0.0


def test_fixed_offset_scaled_residual_tends_to_minus_two_delta():
    N = 100_000_000.0
    for delta in (-2.0, -1.0, -0.5, 0.5, 1.0, 2.0):
        observed = fixed_offset_scaled_residual(N, delta)
        assert abs(observed + 2.0 * delta) < 0.05
