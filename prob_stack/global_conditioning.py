"""Conditioning transfer and global fixed-offset diagnostics for Session 18.

This module does not recompute the Session 17 local excursion exponent. It
packages the exact negative-binomial conditioning point probability, the
existing local likelihood-ratio transfer bound, and the deterministic algebra
around the frozen phase-free rate

    R(x) = x^2 + 2 x log_2 x - 2 log_2(3e) x.

All logarithms returned by this module are base two unless explicitly named
otherwise.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from math import comb

from .product_chain import conditioning_log_ratio_bound
from .product_spatial import conditioned_total_log_probability_bounds


LOG2_3E = math.log2(3.0 * math.e)


def conditioning_point_probability(mean: int, path_length: int) -> Fraction:
    """Exact probability that the iid geometric total equals n times mean.

    The geometric convention is P[X=x]=p r^x with
    p=1/(1+mean), r=mean/(1+mean). Hence the sum has exact
    negative-binomial point mass

        choose(n+n*mean-1, n*mean) p^n r^(n*mean).
    """
    if mean <= 0 or path_length <= 0:
        raise ValueError("mean and path_length must be positive")
    n = path_length
    total = n * mean
    p = Fraction(1, mean + 1)
    r = Fraction(mean, mean + 1)
    return Fraction(comb(n + total - 1, total), 1) * p**n * r**total


def conditioning_point_log2_bounds(
    mean: int, path_length: int
) -> tuple[float, float]:
    """Rigorous stable lower/upper bounds for log2 of the conditioning mass."""
    lower, upper = conditioned_total_log_probability_bounds(mean, path_length)
    factor = 1.0 / math.log(2.0)
    return lower * factor, upper * factor


def conditioning_reciprocal_bits_bounds(
    mean: int, path_length: int
) -> tuple[float, float]:
    """Rigorous bounds for minus log2 of the conditioning mass."""
    lower, upper = conditioning_point_log2_bounds(mean, path_length)
    return -upper, -lower


def one_block_transfer_log_bound(
    mean: int,
    path_length: int,
    block_size: int,
    max_block_mass: int,
) -> float:
    """Natural-log error Delta for one deterministic-support local event.

    If every vector in an event uses block_size displayed coordinates and has
    local mass at most max_block_mass, then the conditioned/product event
    ratio lies between exp(-Delta) and exp(Delta), provided the half-range
    hypotheses checked by conditioning_log_ratio_bound hold.
    """
    if mean <= 0:
        raise ValueError("mean must be positive")
    return conditioning_log_ratio_bound(
        path_length,
        path_length * mean,
        block_size,
        max_block_mass,
    )


def separated_blocks_transfer_log_bound(
    mean: int,
    path_length: int,
    block_size: int,
    max_block_mass: int,
    *,
    blocks: int = 2,
) -> float:
    """Natural-log transfer error for a union of disjoint bounded blocks.

    No conditional independence is asserted. The displayed coordinates are
    simply treated as one local vector of size blocks*block_size and mass at
    most blocks*max_block_mass.
    """
    if blocks <= 0:
        raise ValueError("blocks must be positive")
    return one_block_transfer_log_bound(
        mean,
        path_length,
        blocks * block_size,
        blocks * max_block_mass,
    )


def frozen_center(log2_path_length: float) -> float:
    """Frozen center with the authoritative MINUS half-log-log sign."""
    if log2_path_length <= 1.0:
        raise ValueError("log2_path_length must exceed one")
    return (
        math.sqrt(log2_path_length)
        - 0.5 * math.log2(log2_path_length)
        + LOG2_3E
    )


def phase_free_local_rate_main(log2_mean: float) -> float:
    """Stabilized Session 17 phase-free main rate, without its o(x) term."""
    if log2_mean <= 0.0:
        raise ValueError("log2_mean must be positive")
    x = log2_mean
    return x * x + 2.0 * x * math.log2(x) - 2.0 * LOG2_3E * x


def conditioning_cost_stirling_main_bits(
    log2_path_length: float, log2_mean: float
) -> float:
    """Main Stirling/local-CLT conditioning cost in bits.

    This is 0.5 log2(2*pi*n*mu*(mu+1)) evaluated using real n=2^N and
    mu=2^x. It is a diagnostic main term, not a replacement for the rigorous
    conditioning_reciprocal_bits_bounds function.
    """
    if log2_path_length <= 0.0 or log2_mean <= 0.0:
        raise ValueError("logarithmic parameters must be positive")
    log2_mu_plus_one = log2_mean + math.log2(1.0 + 2.0 ** (-log2_mean))
    return 0.5 * (
        math.log2(2.0 * math.pi)
        + log2_path_length
        + log2_mean
        + log2_mu_plus_one
    )


@dataclass(frozen=True)
class GlobalBalanceDiagnostic:
    log2_path_length: float
    offset: float
    center: float
    log2_mean: float
    local_rate_main: float
    log2_n_times_local_hazard: float
    log2_spaced_block_hazard: float
    conditioning_cost_bits_main: float
    log2_spaced_hazard_to_conditioning_cost: float


def global_balance_diagnostic(
    log2_path_length: float, offset: float
) -> GlobalBalanceDiagnostic:
    """Evaluate the fixed-offset balance around the frozen center.

    log2_spaced_block_hazard subtracts log2(log2 n), corresponding to the
    harmless O(log n) reserved-superblock spacing loss. Its additive O(1)
    constant is intentionally not guessed.

    The final field compares B*q with the logarithmic conditioning cost. A
    positive value means the product no-success exponent is already larger
    than the number of conditioning bits at this main-term diagnostic level.
    """
    N = log2_path_length
    x0 = frozen_center(N)
    x = x0 + offset
    rate = phase_free_local_rate_main(x)
    abundance = N - rate
    spaced = abundance - math.log2(N)
    cond_bits = conditioning_cost_stirling_main_bits(N, x)
    ratio_log2 = spaced - math.log2(cond_bits)
    return GlobalBalanceDiagnostic(
        log2_path_length=N,
        offset=offset,
        center=x0,
        log2_mean=x,
        local_rate_main=rate,
        log2_n_times_local_hazard=abundance,
        log2_spaced_block_hazard=spaced,
        conditioning_cost_bits_main=cond_bits,
        log2_spaced_hazard_to_conditioning_cost=ratio_log2,
    )


def fixed_offset_scaled_residual(
    log2_path_length: float, offset: float
) -> float:
    """Return (N-R(c_N+offset))/sqrt(N) for the main rate.

    Session 18 proves that this tends to -2*offset. This executable quantity is
    only a regression diagnostic for the frozen algebra.
    """
    d = global_balance_diagnostic(log2_path_length, offset)
    return d.log2_n_times_local_hazard / math.sqrt(log2_path_length)
