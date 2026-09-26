from fractions import Fraction
from itertools import product
import math

from prob_stack.product_chain import canonical_deep_deficit_witness
from prob_stack.product_spatial import (
    affine_weighted_sum,
    geometric_sum_double_mean_chernoff,
    reset_event_holds,
    reset_length,
    runaway_buffer_caps,
    runaway_certified_deficit,
    runaway_log2_probability_lower_bound,
    spatial_front_certificate,
    spatial_front_certificate_in_segment,
    conditioned_total_log_probability,
    universal_runaway_probability_lower_bound,
)
from prob_stack.tree_score import transfer


def test_affine_weighted_sum_matches_half_recursion():
    for block in product(range(4), repeat=5):
        y = Fraction(0, 1)
        for x in block:
            y = (y + x) / 2
        assert affine_weighted_sum(block) == y


def test_reset_event_contracts_any_bounded_active_message():
    mean, n = 16, 37
    r = reset_length(n)
    for block in product(range(4), repeat=r):
        if not reset_event_holds(mean, block):
            continue
        for start in (-20, 0, 1, 2 * n * mean):
            message = start
            for x in block:
                message = transfer(message + x)
            assert message <= 2 * mean


def test_runaway_caps_grow_deficit_and_stay_low_phase():
    for mean in (16, 32):
        for n in (10, 1000):
            caps = runaway_buffer_caps(mean, n)
            deficit = mean + 3
            for cap in caps:
                assert cap <= deficit - 2
                deficit = 2 * (deficit - cap)
            assert deficit >= 2 * n * mean + 3
            assert runaway_certified_deficit(mean, caps) >= 2 * n * mean + 3


def test_runaway_probability_has_constant_scale_on_large_n():
    p1 = 2 ** runaway_log2_probability_lower_bound(16, 10**3)
    p2 = 2 ** runaway_log2_probability_lower_bound(16, 10**9)
    assert p2 > 0.009
    assert p1 >= p2


def test_chernoff_tail_is_exponentially_small():
    assert geometric_sum_double_mean_chernoff(16, 100) < math.exp(-20)


def test_spatial_certificate_keeps_session3_leading_exponent():
    n = 10**6
    previous = None
    for mean in (32, 64, 128, 256):
        cert = spatial_front_certificate(mean, n)
        witness = canonical_deep_deficit_witness(mean)
        assert cert.block_length == cert.reset_steps + cert.witness_steps + cert.buffer_steps
        assert math.isfinite(cert.per_block_log2_probability_lower)
        extra = cert.per_block_log2_probability_lower - witness.log2_probability
        assert extra > -10
        if previous is not None:
            assert cert.buffer_steps >= 1
        previous = cert


def test_universal_runaway_constant_is_explicitly_positive():
    c = universal_runaway_probability_lower_bound()
    assert 0.0095 < c < 0.0097


def test_conditioning_point_probability_has_expected_scale():
    for mean in (16, 64):
        for n in (100, 1000):
            p = math.exp(conditioned_total_log_probability(mean, n))
            scaled = p * mean * math.sqrt(n)
            assert 0.2 < scaled < 1.0


def test_segment_certificate_uses_global_reserve_budget():
    cert = spatial_front_certificate_in_segment(32, 10000, 5000)
    full = spatial_front_certificate(32, 10000)
    assert cert.block_length == full.block_length
    assert cert.disjoint_blocks == 5000 // full.block_length


def test_canonical_witness_ends_deep_not_only_hits_deep_small_means():
    for mean in (16, 32):
        witness = canonical_deep_deficit_witness(mean)
        for occupancies in product(*[range(cap + 1) for cap in witness.all_caps]):
            for start in range(mean, 2 * mean + 1):
                message = start
                for occupancy in occupancies:
                    message = transfer(message + occupancy)
                assert message <= -mean

from prob_stack.product_spatial import (
    conditioned_total_log_probability_bounds,
    conditioned_two_sided_failure_bound,
)


def test_conditioning_log_bounds_enclose_direct_formula_on_moderate_sizes():
    for mean in (1, 16, 64):
        for n in (2, 10, 100, 1000):
            t=n*mean
            direct=(math.lgamma(n+t)-math.lgamma(t+1)-math.lgamma(n)
                    -n*math.log(mean+1.0)+t*(math.log(mean)-math.log(mean+1.0)))
            lower,upper=conditioned_total_log_probability_bounds(mean,n)
            # lgamma subtraction itself accumulates about 1e-11 error by n=1000.
            assert lower-5e-10 <= direct <= upper+5e-10


def test_conditioned_two_sided_bound_is_stable_at_stretched_log_scale():
    mean=2**16
    n=2**456  # coefficient c=16/sqrt(456) about 0.75
    bound=conditioned_two_sided_failure_bound(mean,n)
    assert 0.0 <= bound < 1e-50
