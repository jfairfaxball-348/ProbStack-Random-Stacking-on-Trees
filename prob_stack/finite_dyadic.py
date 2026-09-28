"""Exact finite dyadic / binary-partition combinatorics for Session 15.

This module is deliberately finite. It stabilises the exact ordered-vector
counts that underlie the Session 6--7 dyadic-simplex arguments and connects
them to the Session 14 PositiveDescentEvent / LowBudget arithmetic.
No asymptotic approximation is used here.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Iterable


def dyadic_weights(steps: int, *, reverse: bool = False) -> tuple[int, ...]:
    """Return the k dyadic weights 1,2,...,2^(k-1), optionally reversed."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    weights = tuple(1 << j for j in range(steps))
    return tuple(reversed(weights)) if reverse else weights


def dyadic_weighted_sum(values: Iterable[int], *, reverse: bool = False) -> int:
    """Exact ordered-vector dyadic weight."""
    xs = tuple(values)
    if any(x < 0 for x in xs):
        raise ValueError("values must be nonnegative")
    return sum(
        w * x
        for w, x in zip(dyadic_weights(len(xs), reverse=reverse), xs)
    )


def dyadic_simplex_mass_counts(
    steps: int, budget: int, *, reverse: bool = False
) -> tuple[int, ...]:
    """Count simplex vectors by ordinary coordinate sum.

    The coefficient at index s is the number of vectors x with dyadic weighted
    sum at most budget and ordinary sum exactly s.  This bivariate refinement
    is what the exact iid-geometric probability needs.
    """
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return tuple()

    dp: dict[tuple[int, int], int] = {(0, 0): 1}
    for weight in dyadic_weights(steps, reverse=reverse):
        nxt: dict[tuple[int, int], int] = {}
        for (weighted, ordinary), multiplicity in dp.items():
            max_x = (budget - weighted) // weight
            for x in range(max_x + 1):
                key = (weighted + weight * x, ordinary + x)
                nxt[key] = nxt.get(key, 0) + multiplicity
        dp = nxt

    if not dp:
        return tuple()
    max_mass = max(ordinary for _, ordinary in dp)
    counts = [0] * (max_mass + 1)
    for (_, ordinary), multiplicity in dp.items():
        counts[ordinary] += multiplicity
    return tuple(counts)


def dyadic_simplex_count_exact(
    steps: int, budget: int, *, reverse: bool = False
) -> int:
    """Exact ordered-vector count N_{k,B}."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return 0
    if steps == 0:
        return 1

    exact = [0] * (budget + 1)
    exact[0] = 1
    for weight in dyadic_weights(steps, reverse=reverse):
        for total in range(weight, budget + 1):
            exact[total] += exact[total - weight]
    return sum(exact)


def truncated_binary_partition_count(max_exponent: int, total: int) -> int:
    """Partitions of total into powers 1,2,...,2^max_exponent."""
    if total < 0:
        return 0
    if max_exponent < -1:
        raise ValueError("max_exponent must be at least -1")
    if max_exponent == -1:
        return int(total == 0)

    dp = [0] * (total + 1)
    dp[0] = 1
    for exponent in range(max_exponent + 1):
        part = 1 << exponent
        for n in range(part, total + 1):
            dp[n] += dp[n - part]
    return dp[total]


def binary_partition_count(total: int) -> int:
    """Unrestricted binary partitions of an integer total."""
    if total < 0:
        return 0
    if total == 0:
        return 1
    return truncated_binary_partition_count(total.bit_length() - 1, total)


def binary_partition_cumulative_exact(budget: int) -> int:
    """Historical Session-7 cumulative count A(B)=p_bin(2B)."""
    if budget < 0:
        return 0
    return binary_partition_count(2 * budget)


def binary_partition_cumulative_recurrence(budget: int) -> int:
    """Compute A(B) from A(0)=1, A(B)=A(B-1)+A(floor(B/2))."""
    if budget < 0:
        return 0
    values = [1]
    for b in range(1, budget + 1):
        values.append(values[b - 1] + values[b // 2])
    return values[budget]


def dyadic_simplex_binary_partition_coefficient(steps: int, budget: int) -> int:
    """Finite coefficient form of the dyadic-simplex count.

    Exact identity:
      N_{k,B} = [z^(2B)] prod_{j=0}^k (1-z^(2^j))^(-1).
    """
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return 0
    return truncated_binary_partition_count(steps, 2 * budget)


def geometric_simplex_product_probability_exact(
    mean: int, steps: int, budget: int, *, reverse: bool = False
) -> Fraction:
    """Exact iid-geometric mass of one finite dyadic simplex."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return Fraction(0, 1)

    p = Fraction(1, mean + 1)
    r = Fraction(mean, mean + 1)
    counts = dyadic_simplex_mass_counts(steps, budget, reverse=reverse)
    return p**steps * sum(
        (
            multiplicity * r**mass
            for mass, multiplicity in enumerate(counts)
        ),
        Fraction(0, 1),
    )


def positive_descent_budget(mean: int, steps: int) -> int:
    """Integer budget exactly equivalent to Session-14 strict descent."""
    if mean < 0 or steps < 0:
        raise ValueError("mean and steps must be nonnegative")
    return (1 << steps) - 2 * mean - 1


def positive_descent_event(mean: int, values: Iterable[int]) -> bool:
    """Exact condition 2*mu + affineInputCost(xs) < 2^k."""
    xs = tuple(values)
    if mean < 0 or any(x < 0 for x in xs):
        raise ValueError("mean and occupancies must be nonnegative")
    return 2 * mean + dyadic_weighted_sum(xs) < (1 << len(xs))


def positive_descent_count_exact(mean: int, steps: int) -> int:
    """Number of ordered vectors satisfying PositiveDescentEvent."""
    return dyadic_simplex_count_exact(
        steps, positive_descent_budget(mean, steps)
    )


def positive_descent_product_probability_exact(
    mean: int, steps: int
) -> Fraction:
    """Exact product-geometric probability of PositiveDescentEvent."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    return geometric_simplex_product_probability_exact(
        mean, steps, positive_descent_budget(mean, steps)
    )


def low_budget_holds(initial_deficit: int, values: Iterable[int]) -> bool:
    """Exact Session-14 LowBudget predicate."""
    if initial_deficit < 0:
        raise ValueError("initial_deficit must be nonnegative")
    deficit = initial_deficit
    for x in values:
        if x < 0:
            raise ValueError("occupancies must be nonnegative")
        if x > deficit - 2:
            return False
        deficit = 2 * (deficit - x)
    return True


def low_budget_final(initial_deficit: int, values: Iterable[int]) -> int:
    """Exact recursive final deficit from Session 14."""
    if initial_deficit < 0:
        raise ValueError("initial_deficit must be nonnegative")
    deficit = initial_deficit
    for x in values:
        if x < 0:
            raise ValueError("occupancies must be nonnegative")
        deficit = 2 * (deficit - x)
    return deficit


def low_budget_final_closed_form(
    initial_deficit: int, values: Iterable[int]
) -> int:
    """Closed form: 2^k D - 2 * reverseDyadicCost(xs)."""
    xs = tuple(values)
    return (1 << len(xs)) * initial_deficit - 2 * dyadic_weighted_sum(
        xs, reverse=True
    )


def low_phase_simplex_budget(initial_deficit: int, steps: int) -> int:
    """Sufficient reverse-dyadic budget for a complete low-phase block."""
    if initial_deficit < 2:
        raise ValueError("initial_deficit must be at least two")
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if steps == 0:
        return 0
    return (initial_deficit - 2) * (1 << (steps - 1))


def low_phase_simplex_event(
    initial_deficit: int, values: Iterable[int]
) -> bool:
    """The finite reversed simplex used for low-phase amplification."""
    xs = tuple(values)
    return dyadic_weighted_sum(xs, reverse=True) <= low_phase_simplex_budget(
        initial_deficit, len(xs)
    )


def low_phase_simplex_certificate(
    initial_deficit: int, values: Iterable[int]
) -> bool:
    """Check the finite implication into LowBudget and final deficit."""
    xs = tuple(values)
    if not low_phase_simplex_event(initial_deficit, xs):
        return False
    if not low_budget_holds(initial_deficit, xs):
        return False
    if not xs:
        return True
    return low_budget_final(initial_deficit, xs) >= (
        1 << (len(xs) + 1)
    )


def low_phase_simplex_product_probability_exact(
    mean: int, initial_deficit: int, steps: int
) -> Fraction:
    """Exact iid-geometric probability of the low-phase simplex."""
    return geometric_simplex_product_probability_exact(
        mean,
        steps,
        low_phase_simplex_budget(initial_deficit, steps),
        reverse=True,
    )


@dataclass(frozen=True)
class SharpFiniteSeed:
    """The Session-6 sharp two-simplex finite seed (not the cap witness)."""

    mean: int
    level: int
    descent_steps: int
    descent_budget: int
    amplification_steps: int
    amplification_budget: int

    @property
    def support_length(self) -> int:
        return self.descent_steps + self.amplification_steps

    @property
    def product_probability(self) -> Fraction:
        return positive_descent_product_probability_exact(
            self.mean, self.descent_steps
        ) * low_phase_simplex_product_probability_exact(
            self.mean, 3, self.amplification_steps
        )


def sharp_finite_seed(mean: int) -> SharpFiniteSeed:
    """Recover the Session-6 lower witness: (L+2)-descent then L-low."""
    if mean < 16:
        raise ValueError("use mean>=16")
    level = math.ceil(math.log2(mean))
    descent_steps = level + 2
    amplification_steps = level
    return SharpFiniteSeed(
        mean=mean,
        level=level,
        descent_steps=descent_steps,
        descent_budget=positive_descent_budget(mean, descent_steps),
        amplification_steps=amplification_steps,
        amplification_budget=low_phase_simplex_budget(
            3, amplification_steps
        ),
    )


def colored_slack_multiplicity(slack: int) -> int:
    """Reverse positive-phase slack multiplicity."""
    if slack < 0:
        return 0
    return 1 if slack <= 2 else 2


def colored_slack_count_direct(steps: int, budget: int) -> int:
    """Coefficient of prod_j (1+z^(3*2^j))/(1-z^(2^j))."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return 0

    dp = [0] * (budget + 1)
    dp[0] = 1
    for j in range(steps):
        weight = 1 << j
        nxt = [0] * (budget + 1)
        for prior in range(budget + 1):
            if dp[prior] == 0:
                continue
            max_slack = (budget - prior) // weight
            for slack in range(max_slack + 1):
                nxt[prior + slack * weight] += (
                    dp[prior] * colored_slack_multiplicity(slack)
                )
        dp = nxt
    return dp[budget]


def truncated_binary_partition_exact(levels: int, total: int) -> int:
    """b_d(n): partitions using powers 1,...,2^(d-1)."""
    if levels < 0:
        raise ValueError("levels must be nonnegative")
    return truncated_binary_partition_count(levels - 1, total)


def colored_slack_slice_count(steps: int, budget: int) -> int:
    """C_d(B)=sum_{q<2^d} b_d(B-3q), the telescoped coefficient."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    if budget < 0:
        return 0
    return sum(
        truncated_binary_partition_exact(steps, budget - 3 * q)
        for q in range(1 << steps)
        if budget - 3 * q >= 0
    )
