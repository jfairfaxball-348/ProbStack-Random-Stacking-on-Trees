"""Exact finite probability interfaces for Session 14.

This module deliberately stays finite.  It packages exact geometric atom,
interval, cap-product and weak-composition probabilities around the explicit
coordinate certificates used by the deterministic path-front layer.  No
asymptotic approximation or Monte Carlo enters these identities.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb
from typing import Iterable

from .product_chain import (
    canonical_deep_deficit_witness,
    cap_event_probability,
    local_conditioning_ratio,
)
from .tree_score import transfer


def geometric_point_probability(mean: int, value: int) -> Fraction:
    """Exact P[X=value] for X geometric on {0,1,...} with integer mean."""
    if mean <= 0:
        raise ValueError("mean must be a positive integer")
    if value < 0:
        return Fraction(0, 1)
    p = Fraction(1, mean + 1)
    r = Fraction(mean, mean + 1)
    return p * r**value


def geometric_interval_probability(mean: int, lower: int, upper: int) -> Fraction:
    """Exact P[lower <= X <= upper] for the same geometric law."""
    if mean <= 0:
        raise ValueError("mean must be a positive integer")
    if lower < 0:
        lower = 0
    if upper < lower:
        return Fraction(0, 1)
    r = Fraction(mean, mean + 1)
    return r**lower - r ** (upper + 1)


def weak_composition_count(parts: int, total: int) -> int:
    """Exact number of weak compositions, including the zero-part edge case."""
    if parts < 0 or total < 0:
        raise ValueError("parts and total must be nonnegative")
    if parts == 0:
        return int(total == 0)
    return comb(parts + total - 1, total)


def cap_mass_counts(caps: Iterable[int]) -> tuple[int, ...]:
    """Count cap-satisfying local vectors by their exact total mass.

    The coefficient at index s is the number of vectors x with
    0 <= x_i <= caps[i] and sum(x)=s.
    """
    cap_tuple = tuple(caps)
    if any(cap < 0 for cap in cap_tuple):
        raise ValueError("caps must be nonnegative")
    counts = [1]
    for cap in cap_tuple:
        nxt = [0] * (len(counts) + cap)
        running = 0
        for s in range(len(nxt)):
            if s < len(counts):
                running += counts[s]
            if 0 <= s - cap - 1 < len(counts):
                running -= counts[s - cap - 1]
            nxt[s] = running
        counts = nxt
    return tuple(counts)


def product_cap_probability_from_counts(mean: int, caps: Iterable[int]) -> Fraction:
    """Exact iid geometric probability of coordinatewise finite caps."""
    if mean <= 0:
        raise ValueError("mean must be a positive integer")
    cap_tuple = tuple(caps)
    counts = cap_mass_counts(cap_tuple)
    p = Fraction(1, mean + 1)
    r = Fraction(mean, mean + 1)
    return p ** len(cap_tuple) * sum(
        (count * r**mass for mass, count in enumerate(counts)),
        Fraction(0, 1),
    )


def conditioned_cap_probability_from_counts(
    n: int, total: int, caps: Iterable[int]
) -> Fraction:
    """Exact cap-event probability for a uniform weak composition.

    The displayed capped coordinates occupy the first k positions.  Counting
    is by local mass s and exact stars-and-bars completion of the remaining
    n-k coordinates.
    """
    if n <= 0 or total < 0:
        raise ValueError("n must be positive and total nonnegative")
    cap_tuple = tuple(caps)
    if len(cap_tuple) > n:
        raise ValueError("local block does not fit in the composition")
    counts = cap_mass_counts(cap_tuple)
    remaining = n - len(cap_tuple)
    favorable = 0
    for mass, multiplicity in enumerate(counts):
        if mass > total or multiplicity == 0:
            continue
        favorable += multiplicity * weak_composition_count(
            remaining, total - mass
        )
    return Fraction(favorable, weak_composition_count(n, total))


@dataclass(frozen=True)
class LocalComparison:
    """Exact finite conditioned/product comparison for a cap event."""

    conditioned_probability: Fraction
    product_probability: Fraction
    event_ratio: Fraction
    min_atom_ratio: Fraction
    max_atom_ratio: Fraction


def exact_local_cap_comparison(
    n: int, total: int, caps: Iterable[int]
) -> LocalComparison:
    """Compare a bounded local event under the two exact finite laws.

    For p=n/(n+total), the conditioned/product ratio for an atom depends only
    on its local mass.  The event ratio is therefore a product-law weighted
    average of those atom ratios, so it lies between their exact minimum and
    maximum.  The intended half-range applications have sum(caps) <= total.
    """
    if n <= 0 or total <= 0:
        raise ValueError("n and total must be positive")
    cap_tuple = tuple(caps)
    if len(cap_tuple) >= n:
        raise ValueError("need at least one coordinate outside the local block")
    counts = cap_mass_counts(cap_tuple)
    conditioned = conditioned_cap_probability_from_counts(n, total, cap_tuple)

    p = Fraction(n, n + total)
    r = Fraction(total, n + total)
    product_probability = p ** len(cap_tuple) * sum(
        (count * r**mass for mass, count in enumerate(counts)),
        Fraction(0, 1),
    )
    ratios = [
        local_conditioning_ratio(n, total, len(cap_tuple), mass)
        for mass, count in enumerate(counts)
        if count
    ]
    event_ratio = conditioned / product_probability
    return LocalComparison(
        conditioned_probability=conditioned,
        product_probability=product_probability,
        event_ratio=event_ratio,
        min_atom_ratio=min(ratios),
        max_atom_ratio=max(ratios),
    )


@dataclass(frozen=True)
class ExplicitSeedCaps:
    """The explicit Session-3/14 cap certificate from [mean,2*mean]."""

    mean: int
    level: int
    descent_caps: tuple[int, ...]
    amplification_caps: tuple[int, ...]
    certified_final_deficit: int

    @property
    def caps(self) -> tuple[int, ...]:
        return self.descent_caps + self.amplification_caps

    @property
    def support_length(self) -> int:
        return len(self.caps)

    @property
    def local_mass_bound(self) -> int:
        return sum(self.caps)

    @property
    def product_probability(self) -> Fraction:
        return cap_event_probability(self.mean, self.caps)


def explicit_seed_caps(mean: int) -> ExplicitSeedCaps:
    """Recover exactly the canonical finite cap witness already used in Python."""
    witness = canonical_deep_deficit_witness(mean)
    return ExplicitSeedCaps(
        mean=mean,
        level=witness.log_level,
        descent_caps=witness.descent_caps,
        amplification_caps=witness.amplification_caps,
        certified_final_deficit=witness.certified_final_deficit,
    )


def capped_seed_final_message(
    mean: int, start_message: int, occupancies: Iterable[int]
) -> int:
    """Evaluate one explicit capped seed trajectory exactly."""
    seed = explicit_seed_caps(mean)
    values = tuple(occupancies)
    if not mean <= start_message <= 2 * mean:
        raise ValueError("start message must lie in [mean,2*mean]")
    if len(values) != seed.support_length:
        raise ValueError("wrong seed support length")
    if any(x < 0 or x > cap for x, cap in zip(values, seed.caps)):
        raise ValueError("occupancy vector violates an explicit seed cap")
    message = start_message
    for occupancy in values:
        message = transfer(message + occupancy)
    return message


def runaway_caps(initial_deficit: int, length: int) -> tuple[int, ...]:
    """Exact finite Session-13 runaway caps floor(D_j/4)."""
    if initial_deficit < 0 or length < 0:
        raise ValueError("deficit and length must be nonnegative")
    deficit = initial_deficit
    caps: list[int] = []
    for _ in range(length):
        caps.append(deficit // 4)
        deficit = deficit + deficit // 2
    return tuple(caps)


def runaway_product_probability(
    mean: int, initial_deficit: int, length: int
) -> Fraction:
    """Exact iid geometric probability of the finite runaway block."""
    return cap_event_probability(mean, runaway_caps(initial_deficit, length))
