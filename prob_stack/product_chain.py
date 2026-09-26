"""Product-geometric message-chain tools for path rare excursions.

This module studies the exact scalar chain

    M_{j+1} = F(M_j + X_{j+1}),

where F is the TreeStack transfer map and X_j are iid geometric variables with
P(X=k)=p(1-p)^k, p=1/(1+mu).  These routines do not replace the fixed-total
weak-composition model; they are for the unconditioned product law only.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Iterable

from .tree_score import transfer


def geometric_cdf(mean: int, cap: int) -> Fraction:
    """Exact P[X <= cap] for a geometric variable of integer mean ``mean``."""
    if mean <= 0:
        raise ValueError("mean must be a positive integer")
    if cap < 0:
        return Fraction(0, 1)
    ratio = Fraction(mean, mean + 1)
    return 1 - ratio ** (cap + 1)


def cap_event_probability(mean: int, caps: Iterable[int]) -> Fraction:
    """Exact probability that independent geometrics obey deterministic caps."""
    probability = Fraction(1, 1)
    for cap in caps:
        probability *= geometric_cdf(mean, cap)
    return probability


def log2_cap_event_probability(mean: int, caps: Iterable[int]) -> float:
    """Stable floating log2 of ``cap_event_probability`` for large parameters."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    log_ratio = math.log1p(-1.0 / (mean + 1.0))
    total = 0.0
    for cap in caps:
        if cap < 0:
            return -math.inf
        cdf = -math.expm1((cap + 1) * log_ratio)
        total += math.log2(cdf)
    return total


def transfer_upper_half(x: int) -> bool:
    """Check the deterministic inequality F(x) <= x/2 at one integer x."""
    return 2 * transfer(x) <= x


def low_phase_budget(initial_deficit: int, occupancies: Iterable[int]) -> tuple[Fraction, ...]:
    """Return normalized deficits W_j=Z_j/2^j along a low-phase block.

    Algebraically,

        W_j = Z_0 - sum_{r=1}^j 2^(1-r) X_r.

    The block is in the low phase through step j exactly when
    W_j >= 2^(2-j).  This function returns W_1,...,W_k without assuming those
    inequalities hold, so callers can test the exact nested-budget criterion.
    """
    if initial_deficit < 2:
        raise ValueError("initial deficit must be at least 2")
    weighted = Fraction(initial_deficit, 1)
    values: list[Fraction] = []
    for j, occupancy in enumerate(occupancies, start=1):
        if occupancy < 0:
            raise ValueError("occupancies must be nonnegative")
        weighted -= Fraction(occupancy, 2 ** (j - 1))
        values.append(weighted)
    return tuple(values)


def low_phase_budget_holds(initial_deficit: int, occupancies: Iterable[int]) -> bool:
    """Exact nested criterion for a block to remain wholly in the low phase."""
    values = low_phase_budget(initial_deficit, occupancies)
    return all(value >= Fraction(4, 2**j) for j, value in enumerate(values, start=1))


@dataclass(frozen=True)
class CanonicalDeepDeficitWitness:
    """A deterministic-cap event forcing M to hit at most -mean.

    Starting from any integer message M_0 <= 2*mean, the first cap block uses
    F(x) <= x/2 to force M <= 0.  The second cap block stays in the low phase
    and grows a certified deficit lower bound until it reaches mean+3.
    """

    mean: int
    log_level: int
    horizon: int
    descent_caps: tuple[int, ...]
    amplification_caps: tuple[int, ...]
    certified_final_deficit: int

    @property
    def all_caps(self) -> tuple[int, ...]:
        return self.descent_caps + self.amplification_caps

    @property
    def exact_probability(self) -> Fraction:
        return cap_event_probability(self.mean, self.all_caps)

    @property
    def log2_probability(self) -> float:
        return log2_cap_event_probability(self.mean, self.all_caps)


def canonical_deep_deficit_witness(mean: int) -> CanonicalDeepDeficitWitness:
    """Construct the finite-block lower-bound event used in the Session 3 proof.

    The construction is intended for the asymptotic regime; ``mean >= 16``
    keeps the finite constants simple.  Its horizon is always at most 4L for
    L=ceil(log2(mean)).
    """
    if mean < 16:
        raise ValueError("canonical witness is defined for mean >= 16")
    level = math.ceil(math.log2(mean))
    descent_length = level + 4
    descent_caps = tuple(mean // (level * (2**j)) for j in range(1, descent_length + 1))

    deficit = 3
    amplification: list[int] = []
    while deficit < mean + 3:
        cap = deficit // level
        if cap > deficit - 2:
            raise AssertionError("constructed cap left the low phase")
        amplification.append(cap)
        deficit = 2 * (deficit - cap)
        if len(amplification) > 2 * level:
            raise AssertionError("amplification construction exceeded 2L steps")

    horizon = descent_length + len(amplification)
    if horizon > 4 * level:
        raise AssertionError("canonical witness exceeded the 4L theorem horizon")
    return CanonicalDeepDeficitWitness(
        mean=mean,
        log_level=level,
        horizon=horizon,
        descent_caps=descent_caps,
        amplification_caps=tuple(amplification),
        certified_final_deficit=deficit,
    )


def witness_forces_deep_deficit(mean: int, start_message: int, occupancies: Iterable[int]) -> bool:
    """Verify the canonical deterministic implication for one capped sequence."""
    witness = canonical_deep_deficit_witness(mean)
    values = tuple(occupancies)
    if len(values) != len(witness.all_caps):
        raise ValueError("occupancy sequence has the wrong length")
    if any(x < 0 or x > cap for x, cap in zip(values, witness.all_caps)):
        raise ValueError("occupancy sequence does not satisfy the witness caps")
    if start_message > 2 * mean:
        raise ValueError("start message lies outside the certified upper window")

    message = start_message
    hit = message <= -mean
    for x in values:
        message = transfer(message + x)
        hit = hit or message <= -mean
    return hit


def finite_block_upper_log2_bound(mean: int) -> float:
    """Rigorous union-bound log2 upper bound for a 4L-step deep excursion.

    For integer ``mean`` and any starting message in [mean, 2*mean], let q be
    the probability of hitting M <= -mean within K=4L steps, where
    L=ceil(log2(mean)).  This returns log2(U) with q <= U.

    The proof splits the excursion at the first visit to {0,1}.  Backward
    TreeStack preimage bounds cost one dyadic small-deviation block; the final
    negative low-phase run costs a second.  Polynomial-in-L union factors are
    retained explicitly here.
    """
    if mean < 32:
        raise ValueError("upper-bound constants are stated for mean >= 32")
    level = math.ceil(math.log2(mean))
    horizon = 4 * level

    entry_caps = [5]
    entry_caps.extend(8 * (2**r) - 3 for r in range(1, level - 3))
    negative_run_caps = [3 * (2 ** (r - 1)) - 2 for r in range(1, level - 2)]

    log2_bound = 2 * math.log2(horizon)
    log2_bound += log2_cap_event_probability(mean, entry_caps)
    log2_bound += log2_cap_event_probability(mean, negative_run_caps)
    return min(0.0, log2_bound)


def local_conditioning_ratio(n: int, t: int, block_size: int, block_mass: int) -> Fraction:
    """Exact conditioned/product likelihood ratio for one local block vector.

    Let X_1,...,X_n be iid geometric with p=n/(n+t), so their mean is t/n.
    Conditional on total t they are uniform over weak compositions.  For any
    fixed values of the first ``block_size`` coordinates with total
    ``block_mass``, this returns

        P_conditioned[block vector] / P_product[block vector].

    The ratio depends only on the block mass, not on the vector itself.
    """
    if n <= 0 or t <= 0:
        raise ValueError("n and t must be positive")
    if not 0 <= block_size < n:
        raise ValueError("block_size must lie in [0,n)")
    if not 0 <= block_mass <= t:
        return Fraction(0, 1)

    from math import comb

    conditioned = Fraction(
        comb(n - block_size + t - block_mass - 1, t - block_mass),
        comb(n + t - 1, t),
    )
    p = Fraction(n, n + t)
    r = Fraction(t, n + t)
    product_probability = (p**block_size) * (r**block_mass)
    return conditioned / product_probability


def conditioning_log_ratio_bound(n: int, t: int, block_size: int, max_block_mass: int) -> float:
    """Uniform bound |log R| <= Delta for local vectors of mass at most S.

    This uses the exact falling-factorial likelihood ratio and
    ``|log(1-x)| <= 2x`` for x<=1/2.  It is deliberately elementary; sharper
    constants are unnecessary for the equivalence-of-ensembles application.
    """
    k = block_size
    s = max_block_mass
    if n <= 0 or t <= 0 or k < 0 or s < 0:
        raise ValueError("invalid parameters")
    if k >= n or s > t:
        raise ValueError("block does not fit inside the conditioned composition")
    if k > n // 2 or s > t // 2 or k + s > (n + t) // 2:
        raise ValueError("simple half-range logarithm bound does not apply")
    return (
        k * (k + 1) / n
        + s * max(0, s - 1) / t
        + (k + s) * (k + s + 1) / (n + t)
    )


def conditioned_cap_event_probability(n: int, t: int, caps: Iterable[int]) -> Fraction:
    """Exact cap-event probability under the uniform weak-composition law.

    The event is ``C_i <= caps[i]`` for the displayed local coordinates.  A
    bounded-composition convolution counts cap-satisfying local vectors by
    their total mass, after which the remaining coordinates are counted by
    stars and bars.
    """
    from math import comb

    cap_tuple = tuple(caps)
    if any(cap < 0 for cap in cap_tuple):
        return Fraction(0, 1)
    k = len(cap_tuple)
    if n <= k or t < 0:
        raise ValueError("need at least one coordinate outside the local block")

    counts = [1]
    for cap in cap_tuple:
        next_counts = [0] * (len(counts) + cap)
        running = 0
        for s in range(len(next_counts)):
            if s < len(counts):
                running += counts[s]
            if s - cap - 1 >= 0 and s - cap - 1 < len(counts):
                running -= counts[s - cap - 1]
            next_counts[s] = running
        counts = next_counts

    favorable = 0
    for s, multiplicity in enumerate(counts):
        if s > t or multiplicity == 0:
            continue
        favorable += multiplicity * comb(n - k + t - s - 1, t - s)
    return Fraction(favorable, comb(n + t - 1, t))


def product_cap_event_probability_nt(n: int, t: int, caps: Iterable[int]) -> Fraction:
    """Exact matching product-geometric cap probability with mean t/n."""
    if n <= 0 or t <= 0:
        raise ValueError("n and t must be positive")
    ratio = Fraction(t, n + t)
    probability = Fraction(1, 1)
    for cap in caps:
        if cap < 0:
            return Fraction(0, 1)
        probability *= 1 - ratio ** (cap + 1)
    return probability
