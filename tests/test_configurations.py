from collections import Counter
from math import comb
from random import Random

import pytest

from prob_stack.configurations import (
    number_of_configurations,
    sample_uniform_weak_composition,
    weak_compositions,
)


def test_weak_composition_count_matches_stars_and_bars():
    for n in range(1, 7):
        for t in range(0, 8):
            configs = list(weak_compositions(t, n))
            assert len(configs) == comb(n + t - 1, t)
            assert len(set(configs)) == len(configs)
            assert all(sum(c) == t and len(c) == n for c in configs)


def test_number_of_configurations():
    assert number_of_configurations(4, 7) == comb(10, 7)
    assert number_of_configurations(1, 0) == 1


def test_uniform_sampler_uses_weak_composition_space():
    rng = Random(1729)
    counts = Counter(sample_uniform_weak_composition(2, 2, rng) for _ in range(6000))
    assert set(counts) == {(0, 2), (1, 1), (2, 0)}
    # Fixed-seed smoke check for gross bias, not a statistical theorem.
    assert all(1800 <= count <= 2200 for count in counts.values())


def test_invalid_parameters_rejected():
    with pytest.raises(ValueError):
        list(weak_compositions(-1, 2))
    with pytest.raises(ValueError):
        sample_uniform_weak_composition(2, 0)
