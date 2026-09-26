"""Constant-cost spatial regeneration for the path message chain.

The exact TreeStack transfer is used throughout. EMPTY remains a separate
categorical state in the surrounding path scan; this module applies only after
a reset block has activated the branch and produced an integer message.
"""
from __future__ import annotations

from fractions import Fraction
import math

from .tree_score import transfer


def regeneration_interval(mean: int, message: int) -> tuple[int, int]:
    """Occupancy interval steering message into [mean, 2*mean].

    The lemma applies to the nondeep reset range -mean < message <= 2*mean.
    If X lies in the returned interval then

        message + X in [2*mean+2, 4*mean],

    and the exact TreeStack transfer belongs to [mean, 2*mean].
    """
    if mean <= 0:
        raise ValueError("mean must be positive")
    if not -mean < message <= 2 * mean:
        raise ValueError("message must lie in (-mean, 2*mean]")
    return 2 * mean + 2 - message, 4 * mean - message


def geometric_interval_probability(mean: int, lower: int, upper: int) -> Fraction:
    """Exact probability for a geometric(mean) variable to lie in [lower, upper]."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    if lower < 0 or upper < lower:
        return Fraction(0, 1)
    ratio = Fraction(mean, mean + 1)
    return ratio**lower - ratio ** (upper + 1)


def regeneration_probability(mean: int, message: int) -> Fraction:
    """Exact probability of the one-step steering interval."""
    lower, upper = regeneration_interval(mean, message)
    return geometric_interval_probability(mean, lower, upper)


def worst_case_regeneration_probability(mean: int) -> Fraction:
    """Exact minimum steering probability over -mean < M <= 2*mean.

    The occupancy window has fixed width 2*mean-1 and shifts downward as M
    increases, so the geometric probability is minimized at M=-mean+1.
    """
    if mean <= 0:
        raise ValueError("mean must be positive")
    ratio = Fraction(mean, mean + 1)
    return ratio ** (3 * mean + 1) * (1 - ratio ** (2 * mean - 1))


def absolute_regeneration_lower_bound() -> float:
    """Absolute lower bound valid for all integer mean >= 16.

    For r=mean/(mean+1), r^mean > e^-1, r>=16/17, and
    r^(2*mean-1) <= r^mean <= 1/2. Hence the worst-case probability is at
    least 8/(17 e^3).
    """
    return 8.0 / (17.0 * math.e**3)


def regeneration_forces_window(mean: int, message: int, occupancy: int) -> bool:
    """Check the deterministic implication for one steering occupancy."""
    lower, upper = regeneration_interval(mean, message)
    if not lower <= occupancy <= upper:
        raise ValueError("occupancy does not satisfy the regeneration interval")
    output = transfer(message + occupancy)
    return mean <= output <= 2 * mean
