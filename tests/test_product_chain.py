import math
from fractions import Fraction
from itertools import product
from math import comb

from prob_stack.configurations import weak_compositions
from prob_stack.path_score import low_phase_deficit_update
from prob_stack.product_chain import (
    canonical_deep_deficit_witness,
    cap_event_probability,
    conditioned_cap_event_probability,
    conditioning_log_ratio_bound,
    finite_block_upper_log2_bound,
    geometric_cdf,
    local_conditioning_ratio,
    low_phase_budget_holds,
    transfer_upper_half,
    witness_forces_deep_deficit,
)
from prob_stack.tree_score import transfer


def test_transfer_is_globally_at_most_half():
    assert all(transfer_upper_half(x) for x in range(-100, 201))


def test_positive_phase_transfer_has_exact_parity_penalty():
    for effective in range(2, 501):
        expected_penalty = 3 if effective % 2 else 0
        assert 2 * transfer(effective) == effective - expected_penalty


def test_affine_companion_stays_within_three_before_low_phase():
    for start in range(2, 20):
        for block in product(range(5), repeat=4):
            message = start
            companion = Fraction(start, 1)
            for occupancy in block:
                if message < 2:
                    break
                companion = (companion + occupancy) / 2
                message = transfer(message + occupancy)
                gap = companion - message
                assert 0 <= gap < 3


def test_low_phase_budget_is_exact_nested_criterion_exhaustively():
    for initial_deficit in range(2, 12):
        for block in product(range(6), repeat=4):
            deficit = initial_deficit
            direct = True
            for occupancy in block:
                if occupancy > deficit - 2:
                    direct = False
                    break
                deficit = low_phase_deficit_update(deficit, occupancy)
            assert low_phase_budget_holds(initial_deficit, block) == direct


def test_geometric_cap_probability_exact():
    assert geometric_cdf(3, 0) == Fraction(1, 4)
    assert geometric_cdf(3, 1) == Fraction(7, 16)
    assert cap_event_probability(3, (0, 1)) == Fraction(7, 64)


def test_canonical_witness_forces_deep_deficit_exhaustively_at_mean_16():
    mean = 16
    witness = canonical_deep_deficit_witness(mean)
    for occupancies in product(*[range(cap + 1) for cap in witness.all_caps]):
        for start in range(mean, 2 * mean + 1):
            assert witness_forces_deep_deficit(mean, start, occupancies)


def test_finite_block_bounds_are_ordered_on_sample_scales():
    for mean in (32, 64, 256, 1024):
        witness = canonical_deep_deficit_witness(mean)
        assert witness.horizon <= 4 * witness.log_level
        assert witness.log2_probability <= finite_block_upper_log2_bound(mean) <= 0


def test_local_conditioning_ratio_matches_exact_vector_probability():
    n, t, k, s = 8, 24, 3, 5
    ratio = local_conditioning_ratio(n, t, k, s)
    conditioned = Fraction(comb(n - k + t - s - 1, t - s), comb(n + t - 1, t))
    p = Fraction(n, n + t)
    r = Fraction(t, n + t)
    assert ratio == conditioned / (p**k * r**s)


def test_conditioned_cap_probability_matches_bruteforce_small_case():
    n, t = 5, 7
    caps = (1, 2)
    all_configs = list(weak_compositions(t, n))
    brute = Fraction(sum(c[0] <= 1 and c[1] <= 2 for c in all_configs), len(all_configs))
    assert conditioned_cap_event_probability(n, t, caps) == brute


def test_conditioning_ratio_bound_covers_all_supported_local_masses():
    n, t, k, max_mass = 200, 3200, 12, 20
    delta = conditioning_log_ratio_bound(n, t, k, max_mass)
    for mass in range(max_mass + 1):
        ratio = float(local_conditioning_ratio(n, t, k, mass))
        assert abs(math.log(ratio)) <= delta + 1e-12
