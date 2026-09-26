"""Linear-order rare-excursion asymptotics for path stacking.

Session 7 sharpens the Session 6 dyadic-simplex rate from O(L) uncertainty to
an explicit linear coefficient. The key combinatorial input is the classical
binary-partition asymptotic of de Bruijn, together with an exact reverse-slack
encoding of the positive TreeStack phase.

EMPTY remains categorical. This module does not alter the TreeStack transfer.
"""
from __future__ import annotations

import math


LOG2_E = math.log2(math.e)


def dyadic_phase(mean: int) -> tuple[int, float]:
    """Return L=ceil(log2(mean)) and theta=mean/2^L in (1/2,1]."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    floor_level = mean.bit_length() - 1
    level = floor_level if mean == 2**floor_level else floor_level + 1
    theta = mean / (2**level)
    return level, theta


def binary_partition_cumulative_exact(budget: int) -> int:
    """Exact unrestricted dyadic-simplex count.

    This is the number of nonnegative integer vectors of arbitrary finite
    support satisfying sum_j 2^j x_j <= budget. Equivalently it is the number
    of binary partitions of 2*budget (OEIS A000123 convention).
    """
    if budget < 0:
        return 0
    values = [0] * (budget + 1)
    values[0] = 1
    for n in range(1, budget + 1):
        values[n] = values[n - 1] + values[n // 2]
    return values[budget]


def dyadic_simplex_count_exact(steps: int, budget: int) -> int:
    """Exact count of sum_{j<steps} 2^j x_j <= budget."""
    if steps <= 0:
        raise ValueError("steps must be positive")
    if budget < 0:
        return 0
    exact = [0] * (budget + 1)
    exact[0] = 1
    for j in range(steps):
        weight = 2**j
        for total in range(weight, budget + 1):
            exact[total] += exact[total - weight]
    return sum(exact)


def binary_partition_linear_log_count_coefficient(budget_scale: float) -> float:
    """Coefficient c(lambda) in the dyadic-simplex count expansion.

    If B=lambda*2^L+O(1), k=L+O(1), and B/2^k stays bounded, then

      log2 N_{k,B}
      = L^2/2 - L log2 L + c(lambda) L + o(L),

    where c(lambda)=log2(lambda)+1/2+log2(e).
    """
    if budget_scale <= 0:
        raise ValueError("budget_scale must be positive")
    return math.log2(budget_scale) + 0.5 + LOG2_E


def geometric_simplex_linear_cost_coefficient(
    theta: float, *, step_offset: int, budget_scale: float
) -> float:
    """Linear coefficient in -log2 probability for a dyadic simplex."""
    if not 0.5 < theta <= 1.0:
        raise ValueError("theta must lie in (1/2, 1]")
    if budget_scale <= 0:
        raise ValueError("budget_scale must be positive")
    return (
        step_offset
        + math.log2(theta)
        - math.log2(budget_scale)
        - 0.5
        - LOG2_E
    )


def positive_entry_necessary_parameters(mean: int, terminal: int) -> tuple[int, int]:
    """Necessary terminal-specific simplex for the last L-2 positive steps."""
    if mean < 16:
        raise ValueError("use mean>=16")
    if terminal not in (0, 1):
        raise ValueError("terminal must be 0 or 1")
    level, _ = dyadic_phase(mean)
    steps = level - 2
    return steps, (terminal + 3) * (2**steps) - 5


def low_phase_necessary_parameters(mean: int, start: int) -> tuple[int, int]:
    """Necessary reversed simplex for a final low run starting at 0 or 1."""
    if mean < 16:
        raise ValueError("use mean>=16")
    if start not in (0, 1):
        raise ValueError("start must be 0 or 1")
    level, _ = dyadic_phase(mean)
    steps = level - 2
    return steps, (3 - start) * (2 ** (steps - 1)) - 2


def positive_entry_linear_coefficient(theta: float, terminal: int) -> float:
    """Linear cost for first positive-phase entry at terminal 0 or 1."""
    if terminal not in (0, 1):
        raise ValueError("terminal must be 0 or 1")
    if not 0.5 < theta <= 1.0:
        raise ValueError("theta must lie in (1/2, 1]")
    return math.log2(theta) - math.log2(terminal + 3) - 0.5 - LOG2_E


def low_phase_linear_coefficient(theta: float, start: int) -> float:
    """Linear cost for a final all-low run starting from message 0 or 1."""
    if start not in (0, 1):
        raise ValueError("start must be 0 or 1")
    if not 0.5 < theta <= 1.0:
        raise ValueError("theta must lie in (1/2, 1]")
    return math.log2(theta) - math.log2(3 - start) + 0.5 - LOG2_E


def one_sided_beta(theta: float) -> float:
    """Session 7 linear coefficient for q_mu in the ceiling-level variable L."""
    if not 0.5 < theta <= 1.0:
        raise ValueError("theta must lie in (1/2, 1]")
    return 2.0 * math.log2(theta) - 2.0 * math.log2(3.0 * math.e)


def one_sided_linear_rate(mean: int) -> float:
    """L^2+2L log2 L+beta(theta)L for the Session 7 local theorem."""
    level, theta = dyadic_phase(mean)
    if level <= 1:
        raise ValueError("mean is too small for the asymptotic rate")
    return (
        level * level
        + 2.0 * level * math.log2(level)
        + one_sided_beta(theta) * level
    )


def log_mean_linear_rate(mean: int) -> float:
    """Phase-free form through linear order in x=log2(mean)."""
    if mean <= 1:
        raise ValueError("mean must exceed one")
    x = math.log2(mean)
    return x * x + 2.0 * x * math.log2(x) - 2.0 * math.log2(3.0 * math.e) * x


def refined_global_center(log2_path_length: float) -> float:
    """Session 7 O(1)-refined center for x=log2(mean)."""
    if log2_path_length <= 1:
        raise ValueError("log2_path_length must exceed one")
    root = math.sqrt(log2_path_length)
    return root - math.log2(root) + math.log2(3.0 * math.e)


def positive_entry_count_exact(start: int, steps: int, terminal: int) -> int:
    """Exact integer count of positive-phase occupancy strings.

    Count nonnegative occupancy strings of the given length that start from
    start >= 2, have messages >=2 before the final update, and first enter
    {0,1} at the final update with the specified terminal value.

    The reverse recurrence uses the two effective preimages 2v and 2v+3 of a
    positive output v. Suffix sums make the dynamic programme O(steps*2^steps)
    rather than enumerating occupancy strings.
    """
    if start < 2:
        raise ValueError("start must be at least two")
    if steps <= 0:
        raise ValueError("steps must be positive")
    if terminal == 0:
        preimages = (3,)
    elif terminal == 1:
        preimages = (2, 5)
    else:
        raise ValueError("terminal must be 0 or 1")

    maximum = max(preimages)
    counts = [0] * (maximum + 1)
    for message in range(2, maximum + 1):
        counts[message] = sum(y >= message for y in preimages)

    for _ in range(2, steps + 1):
        previous_maximum = len(counts) - 1
        suffix = [0] * (previous_maximum + 2)
        running = 0
        for value in range(previous_maximum, 1, -1):
            running += counts[value]
            suffix[value] = running

        maximum = 2 * previous_maximum + 3
        nxt = [0] * (maximum + 1)
        for message in range(2, maximum + 1):
            even_floor = max(2, (message + 1) // 2)
            odd_floor = max(2, (message - 2) // 2)
            if even_floor <= previous_maximum:
                nxt[message] += suffix[even_floor]
            if odd_floor <= previous_maximum:
                nxt[message] += suffix[odd_floor]
        counts = nxt

    return counts[start] if start < len(counts) else 0


def colored_slack_count_exact(steps: int, budget: int) -> int:
    """Exact coefficient of the positive-phase reverse-slack product.

    A reverse slack y has one color for y=0,1,2 and two colors for y>=3, so

      prod_j (1 + z^(3*2^j)) / (1 - z^(2^j))

    is the generating function. The numerator telescopes, giving the exact
    arithmetic-slice representation implemented here.
    """
    if steps <= 0:
        raise ValueError("steps must be positive")
    if budget < 0:
        return 0

    exact = [0] * (budget + 1)
    exact[0] = 1
    for j in range(steps):
        weight = 2**j
        for total in range(weight, budget + 1):
            exact[total] += exact[total - weight]

    total = 0
    for q in range(2**steps):
        value = budget - 3 * q
        if value < 0:
            break
        total += exact[value]
    return total
