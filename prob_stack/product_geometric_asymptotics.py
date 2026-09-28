"""Session 17 product-geometric dyadic-simplex probability asymptotics.

The finite combinatorics live in finite_dyadic and the binary-partition count
asymptotics live in binary_partition_asymptotics.  This module supplies the
missing probability interface: the iid geometric atom factor p^k and rigorous
control of the tilt r^(sum x_j).

All exact combinatorics remain integer/Fraction valued.  Floating point is
used only for logarithms and deterministic displayed diagnostics.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

from prob_stack.binary_partition_asymptotics import (
    DyadicCountRegime,
    low_amplification_regime,
    positive_descent_regime,
)
from prob_stack.finite_dyadic import (
    dyadic_simplex_count_exact,
    dyadic_weights,
)


LOG2_E = math.log2(math.e)


def _check_theta(theta: float) -> None:
    if not 0.5 < theta <= 1.0:
        raise ValueError("theta must lie in (1/2, 1]")


def geometric_parameters(mean: int) -> tuple[float, float]:
    """Return p=1/(1+mu), r=mu/(1+mu)."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    return 1.0 / (mean + 1), mean / (mean + 1)


def simplex_probability_linear_coefficient(
    theta: float, *, step_offset: int, budget_scale: float
) -> float:
    """Coefficient of L in -log2 P(E_{L+s,lambda 2^L+O(1)}).

    Session 16 gives the count coefficient

        log2(lambda) + 1/2 + log2(e).

    The factor p^(L+s) contributes +(s+log2(theta)) L to the negative
    logarithm.  The geometric tilt contributes only O(1), so the resulting
    linear coefficient is

        s + log2(theta) - log2(lambda) - 1/2 - log2(e).
    """
    _check_theta(theta)
    if budget_scale <= 0:
        raise ValueError("budget_scale must be positive")
    return (
        step_offset
        + math.log2(theta)
        - math.log2(budget_scale)
        - 0.5
        - LOG2_E
    )


def sharp_positive_linear_coefficient(theta: float) -> float:
    """Sharp Session-6 positive-descent block, k=L+2."""
    _check_theta(theta)
    return simplex_probability_linear_coefficient(
        theta,
        step_offset=2,
        budget_scale=4.0 - 2.0 * theta,
    )


def sharp_low_linear_coefficient(theta: float) -> float:
    """Sharp Session-6 low-amplification block, k=L."""
    _check_theta(theta)
    return simplex_probability_linear_coefficient(
        theta,
        step_offset=0,
        budget_scale=0.5,
    )


def sharp_seed_beta(theta: float) -> float:
    """Linear coefficient for the frozen sharp two-simplex Session-6 seed."""
    _check_theta(theta)
    return (
        2.0
        + 2.0 * math.log2(theta)
        - math.log2(4.0 - 2.0 * theta)
        - 2.0 * LOG2_E
    )


def necessary_positive_linear_coefficient(theta: float, terminal: int) -> float:
    """Session-7 necessary positive-entry coefficient for terminal 0 or 1."""
    _check_theta(theta)
    if terminal not in (0, 1):
        raise ValueError("terminal must be 0 or 1")
    return (
        math.log2(theta)
        - math.log2(terminal + 3)
        - 0.5
        - LOG2_E
    )


def necessary_low_linear_coefficient(theta: float, start: int) -> float:
    """Session-7 necessary low-phase coefficient for start 0 or 1."""
    _check_theta(theta)
    if start not in (0, 1):
        raise ValueError("start must be 0 or 1")
    return (
        math.log2(theta)
        - math.log2(3 - start)
        + 0.5
        - LOG2_E
    )


def local_excursion_beta(theta: float) -> float:
    """Final Session-7/17 one-sided excursion coefficient."""
    _check_theta(theta)
    return 2.0 * math.log2(theta) - 2.0 * math.log2(3.0 * math.e)


def geometric_tilt_log2_bounds(mean: int, budget: int) -> tuple[float, float]:
    """Rigorous log2 bounds for the geometric tilt relative to raw counting.

    Every x in a dyadic simplex satisfies

        sum_j x_j <= sum_j 2^j x_j <= budget,

    and the same statement holds for reversed dyadic weights.  Since 0<r<1,

        r^budget N_{k,B}
          <= sum_{x in E_{k,B}} r^(sum x_j)
          <= N_{k,B}.

    This function returns the corresponding lower and upper bounds on the
    log2 ratio between the weighted sum and N_{k,B}.
    """
    if mean <= 0:
        raise ValueError("mean must be positive")
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    r = mean / (mean + 1)
    return budget * math.log2(r), 0.0


def geometric_tilt_uniform_constant(mean: int, budget: int) -> float:
    """Upper bound on the magnitude of the tilt logarithm.

    The exact bound is B log2(1+1/mu), and log(1+t)<=t also gives
    B/(mu ln 2).  The latter makes the O(1) nature transparent when B=O(mu).
    """
    if mean <= 0:
        raise ValueError("mean must be positive")
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    return budget / (mean * math.log(2.0))


def weighted_simplex_sum_float(
    mean: int, steps: int, budget: int, *, reverse: bool = False
) -> float:
    """Compute sum_{x in E} r^(sum x_j) by a one-dimensional DP.

    This is deterministic validation code.  It is much faster than the
    bivariate ordinary-mass profile for the Session-17 diagnostic range.
    """
    if mean <= 0:
        raise ValueError("mean must be positive")
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return 0.0

    r = mean / (mean + 1)
    exact_weight = [0.0] * (budget + 1)
    exact_weight[0] = 1.0
    for weight in dyadic_weights(steps, reverse=reverse):
        for total in range(weight, budget + 1):
            exact_weight[total] += r * exact_weight[total - weight]
    return sum(exact_weight)


def weighted_simplex_sum_exact(
    mean: int, steps: int, budget: int, *, reverse: bool = False
) -> Fraction:
    """Exact Fraction version of weighted_simplex_sum_float.

    This is intended for moderate finite diagnostics, not large asymptotic
    levels.
    """
    if mean <= 0:
        raise ValueError("mean must be positive")
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return Fraction(0, 1)

    r = Fraction(mean, mean + 1)
    exact_weight = [Fraction(0, 1)] * (budget + 1)
    exact_weight[0] = Fraction(1, 1)
    for weight in dyadic_weights(steps, reverse=reverse):
        for total in range(weight, budget + 1):
            exact_weight[total] += r * exact_weight[total - weight]
    return sum(exact_weight, Fraction(0, 1))


def geometric_simplex_product_probability_exact_fast(
    mean: int, steps: int, budget: int, *, reverse: bool = False
) -> Fraction:
    """Exact product-geometric simplex probability using the 1D weighted DP."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    return Fraction(1, mean + 1) ** steps * weighted_simplex_sum_exact(
        mean, steps, budget, reverse=reverse
    )


def _log2_positive_int(value: int) -> float:
    """Stable floating log2 of a positive arbitrary-precision integer."""
    if value <= 0:
        raise ValueError("value must be positive")
    bits = value.bit_length()
    if bits <= 53:
        return math.log2(value)
    shift = bits - 53
    return shift + math.log2(value >> shift)


def log2_positive_fraction(value: Fraction) -> float:
    """Stable floating log2 of a positive Fraction."""
    if value <= 0:
        raise ValueError("value must be positive")
    return _log2_positive_int(value.numerator) - _log2_positive_int(
        value.denominator
    )


@dataclass(frozen=True)
class ProductProbabilityDiagnostic:
    """One finite product-probability check against the Session-17 theorem."""

    family: str
    level: int
    theta: float
    mean: int
    steps: int
    budget: int
    scale: float
    reverse: bool
    count: int
    log2_count: float
    log2_p_factor: float
    tilt_log2: float
    tilt_lower_bound: float
    log2_probability: float
    linear_coefficient: float
    residual_after_probability_linear_term: float
    exact_fraction_checked: bool
    exact_log2_probability: float | None


def probability_diagnostic(
    mean: int,
    regime: DyadicCountRegime,
    *,
    reverse: bool = False,
    exact_fraction: bool = False,
) -> ProductProbabilityDiagnostic:
    """Build one exact-count / weighted-probability diagnostic row."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    if regime.budget < 0:
        raise ValueError("diagnostic regime must have nonnegative budget")
    if regime.theta is None:
        raise ValueError("regime must carry theta")

    count = dyadic_simplex_count_exact(
        regime.steps, regime.budget, reverse=reverse
    )
    p, _ = geometric_parameters(mean)
    weighted = weighted_simplex_sum_float(
        mean, regime.steps, regime.budget, reverse=reverse
    )
    log2_count = math.log2(count)
    log2_p_factor = regime.steps * math.log2(p)
    log2_probability = log2_p_factor + math.log2(weighted)
    unweighted_log2_probability = log2_p_factor + log2_count
    tilt_log2 = log2_probability - unweighted_log2_probability
    tilt_lower, _ = geometric_tilt_log2_bounds(mean, regime.budget)
    step_offset = regime.steps - regime.level
    coefficient = simplex_probability_linear_coefficient(
        regime.theta,
        step_offset=step_offset,
        budget_scale=regime.scale,
    )
    leading_cost = (
        0.5 * regime.level**2
        + regime.level * math.log2(regime.level)
        + coefficient * regime.level
    )

    exact_log = None
    if exact_fraction:
        exact_probability = geometric_simplex_product_probability_exact_fast(
            mean,
            regime.steps,
            regime.budget,
            reverse=reverse,
        )
        exact_log = log2_positive_fraction(exact_probability)

    return ProductProbabilityDiagnostic(
        family=regime.family,
        level=regime.level,
        theta=regime.theta,
        mean=mean,
        steps=regime.steps,
        budget=regime.budget,
        scale=regime.scale,
        reverse=reverse,
        count=count,
        log2_count=log2_count,
        log2_p_factor=log2_p_factor,
        tilt_log2=tilt_log2,
        tilt_lower_bound=tilt_lower,
        log2_probability=log2_probability,
        linear_coefficient=coefficient,
        residual_after_probability_linear_term=-log2_probability - leading_cost,
        exact_fraction_checked=exact_fraction,
        exact_log2_probability=exact_log,
    )


def sharp_seed_probability_diagnostic(
    mean: int, *, exact_fraction: bool = False
) -> tuple[ProductProbabilityDiagnostic, ProductProbabilityDiagnostic]:
    """Return the two independent block diagnostics for the frozen sharp seed."""
    positive = probability_diagnostic(
        mean,
        positive_descent_regime(mean),
        exact_fraction=exact_fraction,
    )
    low = probability_diagnostic(
        mean,
        low_amplification_regime(mean),
        reverse=True,
        exact_fraction=exact_fraction,
    )
    return positive, low
