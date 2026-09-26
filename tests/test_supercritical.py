from itertools import product

from prob_stack.supercritical import (
    conditioned_nonstackable_log2_upper,
    deep_cover_holds,
    deep_message_cover,
    product_direction_deep_upper,
)


def test_cover_probability_scales_are_ordered():
    for mean in (16, 32, 64, 128, 256, 1024):
        cover = deep_message_cover(mean)
        assert cover.cluster_log2_probability <= cover.low_log2_probability + 1e-12
        assert cover.max_window_length >= cover.cluster_steps
        assert cover.max_window_mass >= 4 * mean * cover.cluster_steps


def test_cap_cover_deterministically_on_small_exhaustive_sequences():
    mean = 16
    for occupancies in product(range(7), repeat=6):
        assert deep_cover_holds(occupancies, mean)


def test_cap_cover_on_targeted_deep_sequences():
    mean = 16
    cases = [
        (1, 0, 0, 0, 0, 0, 0),
        (3, 0, 0, 0, 0, 0, 0),
        (40, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (100, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0),
    ]
    for occupancies in cases:
        assert deep_cover_holds(occupancies, mean)


def test_product_upper_is_probability():
    for mean in (16, 32, 64, 128):
        assert 0 <= product_direction_deep_upper(mean, 1000) <= 1


def test_conditioned_bound_decays_above_coefficient_one_on_asymptotic_scales():
    for coefficient in (1.10, 1.25, 1.50):
        values = []
        for level in (30, 40, 50):
            mean = 2**level
            log2_n = round((level / coefficient) ** 2)
            n = 2**log2_n
            values.append(conditioned_nonstackable_log2_upper(mean, n))
        assert values[-1] < values[0]
        assert values[-1] < -20
