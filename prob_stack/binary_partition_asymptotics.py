"""Session 16 diagnostics for binary-partition asymptotics.

This module keeps the analytic approximation separate from the exact finite
combinatorics in 'finite_dyadic'. Exact counts remain integer-valued; only
logarithms and the displayed de Bruijn main terms use floating point.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from prob_stack.finite_dyadic import (
    binary_partition_cumulative_recurrence,
    dyadic_simplex_count_exact,
)

LOG2_E = math.log2(math.e)


@dataclass(frozen=True)
class DyadicCountRegime:
    """One exact finite N_{k,B} together with its L-scale asymptotic data."""

    family: str
    level: int
    steps: int
    budget: int
    scale: float
    theta: float | None = None

    @property
    def cutoff_is_exact(self) -> bool:
        return unrestricted_cutoff_holds(self.steps, self.budget)

    @property
    def tail_factor_bound(self) -> int:
        return truncation_tail_factor_bound(self.steps, self.budget)


@dataclass(frozen=True)
class AsymptoticDiagnostic:
    """Exact count and the two residuals used by the Session 16 table."""

    regime: DyadicCountRegime
    exact_count: int
    unrestricted_count: int
    log2_count: float
    residual_after_quadratic_and_llogl: float
    linear_coefficient: float
    residual_after_linear_term: float


def dyadic_level_and_phase(mean: int) -> tuple[int, float]:
    """Return L=ceil(log2(mean)) and theta=mean/2^L."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    floor_level = mean.bit_length() - 1
    level = floor_level if mean == 1 << floor_level else floor_level + 1
    return level, mean / (1 << level)


def unrestricted_cutoff_holds(steps: int, budget: int) -> bool:
    """Exact Session 15 criterion: N_{k,B}=A(B) when 2^k>B."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return False
    return (1 << steps) > budget


def truncation_tail_factor_bound(steps: int, budget: int) -> int:
    """Return a rigorous multiplicative bound for truncation.

    If A(B) denotes the unrestricted cumulative binary-partition count, then

        N_{k,B} <= A(B) <= A(floor(B/2^k)) N_{k,B}.

    Thus fixed B/2^k gives a bounded factor even when the exact cutoff does
    not apply.
    """
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    quotient = budget // (1 << steps)
    return binary_partition_cumulative_recurrence(quotient)


def de_bruijn_linear_coefficient(scale: float) -> float:
    """Coefficient of L for B=scale*2^L+O(1).

    For A(B)=p_bin(2B), de Bruijn's formula gives

      log2 A(B)
        = L^2/2 - L log2 L
          + (log2(scale) + 1/2 + log2(e)) L
          + O((log L)^2).

    The same coefficient applies to N_{L+a,B} for every fixed integer a
    because truncation changes the count by at most a bounded factor.
    """
    if scale <= 0:
        raise ValueError("scale must be positive")
    return math.log2(scale) + 0.5 + LOG2_E


def de_bruijn_log2_three_term(level: int, scale: float) -> float:
    """Quadratic, -L log L, and linear terms of log2 N."""
    if level <= 0:
        raise ValueError("level must be positive")
    return (
        0.5 * level * level
        - level * math.log2(level)
        + de_bruijn_linear_coefficient(scale) * level
    )


def positive_descent_regime(mean: int) -> DyadicCountRegime:
    """Sharp Session 6 positive-descent simplex from Session 15."""
    level, theta = dyadic_level_and_phase(mean)
    steps = level + 2
    budget = (1 << steps) - 2 * mean - 1
    return DyadicCountRegime(
        "positive_descent",
        level,
        steps,
        budget,
        4.0 - 2.0 * theta,
        theta,
    )


def low_amplification_regime(mean: int) -> DyadicCountRegime:
    """Sharp Session 6 low-phase amplification simplex."""
    level, theta = dyadic_level_and_phase(mean)
    if level < 1:
        raise ValueError("use mean>=2")
    return DyadicCountRegime(
        "low_amplification",
        level,
        level,
        1 << (level - 1),
        0.5,
        theta,
    )


def necessary_positive_entry_regime(
    mean: int, terminal: int
) -> DyadicCountRegime:
    """Session 7 necessary positive-entry simplex for terminal 0 or 1."""
    if terminal not in (0, 1):
        raise ValueError("terminal must be 0 or 1")
    level, theta = dyadic_level_and_phase(mean)
    if level < 3:
        raise ValueError("use level>=3")
    steps = level - 2
    return DyadicCountRegime(
        f"necessary_positive_entry_{terminal}",
        level,
        steps,
        (terminal + 3) * (1 << steps) - 5,
        (terminal + 3) / 4.0,
        theta,
    )


def necessary_low_phase_regime(mean: int, start: int) -> DyadicCountRegime:
    """Session 7 necessary low-phase simplex for start state 0 or 1."""
    if start not in (0, 1):
        raise ValueError("start must be 0 or 1")
    level, theta = dyadic_level_and_phase(mean)
    if level < 3:
        raise ValueError("use level>=3")
    steps = level - 2
    return DyadicCountRegime(
        f"necessary_low_phase_{start}",
        level,
        steps,
        (3 - start) * (1 << (steps - 1)) - 2,
        (3 - start) / 8.0,
        theta,
    )


def exact_diagnostic(regime: DyadicCountRegime) -> AsymptoticDiagnostic:
    """Compute exact integer counts and floating logarithmic residuals."""
    unrestricted = binary_partition_cumulative_recurrence(regime.budget)
    if regime.cutoff_is_exact:
        exact = unrestricted
    else:
        exact = dyadic_simplex_count_exact(regime.steps, regime.budget)
    log_count = math.log2(exact)
    base = 0.5 * regime.level**2 - regime.level * math.log2(regime.level)
    coefficient = de_bruijn_linear_coefficient(regime.scale)
    return AsymptoticDiagnostic(
        regime=regime,
        exact_count=exact,
        unrestricted_count=unrestricted,
        log2_count=log_count,
        residual_after_quadratic_and_llogl=log_count - base,
        linear_coefficient=coefficient,
        residual_after_linear_term=log_count - base - coefficient * regime.level,
    )
