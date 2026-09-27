from fractions import Fraction
from itertools import product

from prob_stack.configurations import weak_compositions
from prob_stack.finite_probability import (
    cap_mass_counts,
    capped_seed_final_message,
    conditioned_cap_probability_from_counts,
    exact_local_cap_comparison,
    explicit_seed_caps,
    geometric_interval_probability,
    geometric_point_probability,
    product_cap_probability_from_counts,
    runaway_caps,
    runaway_product_probability,
    weak_composition_count,
)
from prob_stack.product_chain import (
    cap_event_probability,
    conditioned_cap_event_probability,
)


def test_geometric_point_and_interval_law_exact():
    assert geometric_point_probability(3, 0) == Fraction(1, 4)
    assert geometric_point_probability(3, 2) == Fraction(9, 64)
    assert geometric_interval_probability(3, 1, 2) == Fraction(21, 64)


def test_weak_composition_count_including_zero_part_edge():
    assert weak_composition_count(0, 0) == 1
    assert weak_composition_count(0, 4) == 0
    assert weak_composition_count(1, 7) == 1
    assert weak_composition_count(4, 7) == 120


def test_cap_mass_counts_and_product_probability_are_exact():
    caps = (1, 2, 0)
    counts = cap_mass_counts(caps)
    assert sum(counts) == 6
    assert product_cap_probability_from_counts(5, caps) == cap_event_probability(5, caps)


def test_conditioned_cap_count_matches_existing_formula_and_bruteforce():
    n, total = 5, 7
    caps = (1, 2)
    exact = conditioned_cap_probability_from_counts(n, total, caps)
    assert exact == conditioned_cap_event_probability(n, total, caps)
    configs = list(weak_compositions(total, n))
    brute = Fraction(
        sum(c[0] <= caps[0] and c[1] <= caps[1] for c in configs),
        len(configs),
    )
    assert exact == brute


def test_exact_event_ratio_lies_between_atom_ratios():
    comparison = exact_local_cap_comparison(12, 48, (1, 2, 3))
    assert comparison.min_atom_ratio <= comparison.event_ratio
    assert comparison.event_ratio <= comparison.max_atom_ratio
    assert comparison.conditioned_probability > 0
    assert comparison.product_probability > 0


def test_canonical_seed_caps_force_final_deep_message_at_mean_16():
    mean = 16
    seed = explicit_seed_caps(mean)
    assert seed.certified_final_deficit >= mean + 3
    assert seed.support_length == len(seed.descent_caps) + len(seed.amplification_caps)
    assert seed.local_mass_bound == sum(seed.caps)

    for occupancies in product(*[range(cap + 1) for cap in seed.caps]):
        for start in range(mean, 2 * mean + 1):
            assert capped_seed_final_message(mean, start, occupancies) <= -mean


def test_runaway_caps_and_probability_match_direct_product():
    caps = runaway_caps(19, 6)
    assert caps == (4, 7, 10, 16, 24, 37)
    assert runaway_product_probability(16, 19, 6) == cap_event_probability(16, caps)
