"""Configurations, exact weak-composition enumeration, and uniform sampling."""

from __future__ import annotations

from math import comb
from random import Random
from typing import Iterator

Configuration = tuple[int, ...]


def validate_configuration(configuration: Configuration, n: int | None = None) -> Configuration:
    if n is not None and len(configuration) != n:
        raise ValueError("configuration length does not match graph order")
    if not configuration:
        raise ValueError("configuration must have at least one coordinate")
    if any((not isinstance(x, int)) or x < 0 for x in configuration):
        raise ValueError("configuration entries must be nonnegative integers")
    return configuration


def mass(configuration: Configuration) -> int:
    return sum(configuration)


def number_of_configurations(n: int, t: int) -> int:
    """Return |D_{G,t}| = binom(n+t-1,t)."""
    if n <= 0 or t < 0:
        raise ValueError("n must be positive and t nonnegative")
    return comb(n + t - 1, t)


def weak_compositions(t: int, n: int) -> Iterator[Configuration]:
    """Yield every weak composition of ``t`` into ``n`` parts exactly once."""
    if n <= 0 or t < 0:
        raise ValueError("n must be positive and t nonnegative")
    if n == 1:
        yield (t,)
        return
    prefix = [0] * n

    def rec(index: int, remaining: int) -> Iterator[Configuration]:
        if index == n - 1:
            prefix[index] = remaining
            yield tuple(prefix)
            return
        for value in range(remaining + 1):
            prefix[index] = value
            yield from rec(index + 1, remaining - value)

    yield from rec(0, t)


def sample_uniform_weak_composition(t: int, n: int, rng: Random | None = None) -> Configuration:
    """Sample uniformly from weak compositions using the stars-and-bars bijection.

    This is *not* the multinomial model obtained by independently placing t
    labeled pebbles at uniformly random vertices.
    """
    if n <= 0 or t < 0:
        raise ValueError("n must be positive and t nonnegative")
    if n == 1:
        return (t,)
    if rng is None:
        rng = Random()
    separators = sorted(rng.sample(range(t + n - 1), n - 1))
    values = [separators[0]]
    values.extend(separators[i] - separators[i - 1] - 1 for i in range(1, n - 1))
    values.append(t + n - 2 - separators[-1])
    return tuple(values)
