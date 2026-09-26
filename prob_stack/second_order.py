"""Second-order rare-excursion bounds for path stacking.

The key object is a dyadic weighted simplex.  For iid geometric occupancies
X_1,...,X_k of integer mean mu, lattice-volume bounds for

    sum_{j=1}^k 2^(j-1) X_j <= B

recover the factorial term that rectangular cap events lose.  This module
uses that observation to sharpen the Session 3 finite-block probability and
the Session 5 first-deep-message cover.

EMPTY remains categorical.  The exact TreeStack transfer is imported only by
the executable deterministic cover check.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math


def _log2_ratio(mean: int) -> float:
    if mean <= 0:
        raise ValueError("mean must be positive")
    return math.log1p(-1.0 / (mean + 1.0)) / math.log(2.0)


def dyadic_weighted_sum(values, *, reverse: bool = False) -> int:
    xs = tuple(values)
    if any(x < 0 for x in xs):
        raise ValueError("values must be nonnegative")
    k = len(xs)
    if reverse:
        return sum((2 ** (k - 1 - j)) * x for j, x in enumerate(xs))
    return sum((2**j) * x for j, x in enumerate(xs))


def dyadic_small_ball_log2_bounds(
    mean: int, steps: int, budget: int
) -> tuple[float, float]:
    """Rigorous log2 bounds for a dyadic geometric small-ball event.

    Let p=1/(mean+1), r=mean/(mean+1), and
    E={sum 2^j X_j <= budget}.  If N(E) is the number of lattice points in
    the weighted simplex, unit-cube comparison gives

      B^k/(k! prod w_j) <= N(E)
      <= (B+sum w_j)^k/(k! prod w_j).

    Since sum X_j <= B on E, every atom has geometric factor between
    p^k r^B and p^k.  The same bounds apply when the dyadic weights are
    reversed.
    """
    if mean <= 0 or steps <= 0 or budget <= 0:
        raise ValueError("mean, steps, budget must be positive")
    p_log2 = -math.log2(mean + 1.0)
    r_log2 = _log2_ratio(mean)
    weight_sum = 2**steps - 1
    weight_product_log2 = steps * (steps - 1) / 2
    log2_fact = math.lgamma(steps + 1) / math.log(2.0)

    lower = (
        steps * p_log2
        + budget * r_log2
        + steps * math.log2(budget)
        - log2_fact
        - weight_product_log2
    )
    upper = (
        steps * p_log2
        + steps * math.log2(budget + weight_sum)
        - log2_fact
        - weight_product_log2
    )
    return lower, min(0.0, upper)


def dyadic_small_ball_probability_exact(
    mean: int, steps: int, budget: int
) -> Fraction:
    """Exact O(steps*budget) DP for feasible dyadic small-ball instances."""
    if mean <= 0 or steps <= 0 or budget < 0:
        raise ValueError("invalid parameters")
    p = Fraction(1, mean + 1)
    r = Fraction(mean, mean + 1)
    dp = [Fraction(0, 1)] * (budget + 1)
    dp[0] = Fraction(1, 1)
    for j in range(steps):
        weight = 2**j
        nxt = [Fraction(0, 1)] * (budget + 1)
        for s in range(budget + 1):
            value = p * dp[s]
            if s >= weight:
                value += r * nxt[s - weight]
            nxt[s] = value
        dp = nxt
    return sum(dp, Fraction(0, 1))


def second_order_rate(level: int) -> float:
    """L^2+2L log_2 L, the proved second-order local rate."""
    if level <= 1:
        raise ValueError("level must exceed one")
    return level * level + 2.0 * level * math.log2(level)


def descent_witness_parameters(mean: int) -> tuple[int, int]:
    """Weighted-simplex event forcing M<=0 from every M_0<=2*mean."""
    if mean < 16:
        raise ValueError("use mean>=16")
    level = math.ceil(math.log2(mean))
    steps = level + 2
    budget = 2**steps - 2 * mean - 1
    if budget <= 0:
        raise AssertionError("descent budget must be positive")
    return steps, budget


def amplification_witness_parameters(mean: int) -> tuple[int, int]:
    """Reverse-dyadic simplex forcing M<=-mean from every M_0<=0."""
    if mean < 16:
        raise ValueError("use mean>=16")
    level = math.ceil(math.log2(mean))
    return level, 2 ** (level - 1)


def necessary_entry_parameters(mean: int) -> tuple[int, int]:
    """Necessary simplex on the last L-2 positive steps before entry <=1."""
    if mean < 16:
        raise ValueError("use mean>=16")
    level = math.ceil(math.log2(mean))
    steps = level - 2
    return steps, 4 * (2**steps) - 5


def necessary_low_parameters(
    mean: int, *, initial_deficit_cap: int = 3
) -> tuple[int, int]:
    """Necessary reverse-dyadic simplex at the start of a final low run."""
    if mean < 16:
        raise ValueError("use mean>=16")
    if initial_deficit_cap < 2:
        raise ValueError("initial deficit cap must be at least two")
    level = math.ceil(math.log2(mean))
    steps = level - 2
    # Divide the exact deficit identity by two so the weights are
    # 2^(steps-1),...,1.  Every message after the start of the final run is
    # negative, so its deficit is at least four.
    budget = initial_deficit_cap * (2 ** (steps - 1)) - 2
    return steps, budget


@dataclass(frozen=True)
class FiniteBlockSecondOrderBounds:
    mean: int
    level: int
    horizon: int
    lower_log2_probability: float
    upper_log2_probability: float

    @property
    def rate(self) -> float:
        return second_order_rate(self.level)

    @property
    def lower_residual_per_level(self) -> float:
        return (-self.lower_log2_probability - self.rate) / self.level

    @property
    def upper_residual_per_level(self) -> float:
        return (-self.upper_log2_probability - self.rate) / self.level


def finite_block_second_order_bounds(mean: int) -> FiniteBlockSecondOrderBounds:
    """Rigorous uniform bounds for q_mu(m), m in [mu,2mu].

    q_mu(m)=P_m[min_{1<=j<=4L} M_j <= -mu], L=ceil(log2(mu)).

    The lower event is a descent simplex followed by an amplification simplex.
    For the upper bound, every hit supplies a necessary positive-entry simplex
    and a disjoint necessary final-low-run simplex; there are at most (4L)^2
    choices of their locations.
    """
    if mean < 32:
        raise ValueError("use mean>=32")
    level = math.ceil(math.log2(mean))
    horizon = 4 * level

    kd, bd = descent_witness_parameters(mean)
    ka, ba = amplification_witness_parameters(mean)
    descent_lower, _ = dyadic_small_ball_log2_bounds(mean, kd, bd)
    amp_lower, _ = dyadic_small_ball_log2_bounds(mean, ka, ba)
    lower = descent_lower + amp_lower

    k, b_entry = necessary_entry_parameters(mean)
    _, entry_upper = dyadic_small_ball_log2_bounds(mean, k, b_entry)
    _, low_upper = dyadic_small_ball_log2_bounds(
        mean, k, necessary_low_parameters(mean, initial_deficit_cap=3)[1]
    )
    upper = min(
        0.0,
        2.0 * math.log2(horizon) + entry_upper + low_upper,
    )
    return FiniteBlockSecondOrderBounds(
        mean=mean,
        level=level,
        horizon=horizon,
        lower_log2_probability=lower,
        upper_log2_probability=upper,
    )


def _log2_geometric_cdf(mean: int, cap: int) -> float:
    if mean <= 0:
        raise ValueError("mean must be positive")
    if cap < 0:
        return -math.inf
    log_ratio = math.log1p(-1.0 / (mean + 1.0))
    return math.log2(-math.expm1((cap + 1) * log_ratio))


@dataclass(frozen=True)
class SecondOrderDeepMessageCover:
    mean: int
    level: int
    simplex_steps: int
    entry_budget: int
    low_budget: int
    entry_log2_probability_upper: float
    low_log2_probability_upper: float
    cluster_cap: int
    cluster_steps: int
    cluster_log2_probability: float
    max_window_length: int
    max_window_mass: int

    @property
    def interior_log2_probability_upper(self) -> float:
        return (
            self.entry_log2_probability_upper
            + self.low_log2_probability_upper
        )


def second_order_deep_message_cover(mean: int) -> SecondOrderDeepMessageCover:
    """Sharpen the Session 5 cover for first hits <=-(2*mean-1).

    Interior hits require a positive-entry simplex and a final-low-run simplex.
    Boundary-origin hits require only the final-low-run simplex.  The bounded
    middle cluster is unchanged from Session 5.
    """
    if mean < 16:
        raise ValueError("use mean>=16")
    level = math.ceil(math.log2(mean))
    steps, entry_budget = necessary_entry_parameters(mean)
    low_steps, low_budget = necessary_low_parameters(
        mean, initial_deficit_cap=4
    )
    if low_steps != steps:
        raise AssertionError("simplex lengths should agree")

    _, entry_upper = dyadic_small_ball_log2_bounds(
        mean, steps, entry_budget
    )
    _, low_upper = dyadic_small_ball_log2_bounds(
        mean, steps, low_budget
    )
    cap = 4 * mean
    one_step = _log2_geometric_cdf(mean, cap)
    cluster_steps = max(1, math.ceil(low_upper / one_step))
    cluster_log2 = cluster_steps * one_step

    return SecondOrderDeepMessageCover(
        mean=mean,
        level=level,
        simplex_steps=steps,
        entry_budget=entry_budget,
        low_budget=low_budget,
        entry_log2_probability_upper=entry_upper,
        low_log2_probability_upper=low_upper,
        cluster_cap=cap,
        cluster_steps=cluster_steps,
        cluster_log2_probability=cluster_log2,
        max_window_length=2 * steps + cluster_steps,
        max_window_mass=(
            entry_budget + low_budget + cap * cluster_steps
        ),
    )


def log2_product_direction_deep_second_order_upper(
    mean: int, scan_steps: int
) -> float:
    """Sharpened one-direction product upper bound for a first deep hit."""
    if scan_steps < 0:
        raise ValueError("scan_steps must be nonnegative")
    cover = second_order_deep_message_cover(mean)
    boundary = (
        math.log2(cover.cluster_steps + 1)
        + cover.low_log2_probability_upper
    )
    if scan_steps == 0:
        return min(0.0, boundary)

    interior = (
        math.log2(scan_steps)
        + math.log2(cover.cluster_steps + 2)
        + cover.interior_log2_probability_upper
    )
    pivot = max(boundary, interior)
    total = pivot + math.log2(
        2 ** (boundary - pivot) + 2 ** (interior - pivot)
    )
    return min(0.0, total)


def conditioned_nonstackable_second_order_log2_upper(
    mean: int, path_length: int
) -> float:
    """Fixed-total nonstackability upper bound using the sharpened cover."""
    if mean < 32 or path_length < 2:
        raise ValueError("mean>=32 and path_length>=2 are required")
    from .product_chain import conditioning_log_ratio_bound

    cover = second_order_deep_message_cover(mean)
    total = mean * path_length
    delta = conditioning_log_ratio_bound(
        path_length,
        total,
        cover.max_window_length,
        cover.max_window_mass,
    )
    one_direction = log2_product_direction_deep_second_order_upper(
        mean, path_length - 1
    )
    return 1.0 + delta / math.log(2.0) + one_direction


def second_order_center(log2_path_length: float) -> float:
    """Return sqrt(log2 n)-log2(sqrt(log2 n))."""
    if log2_path_length <= 1:
        raise ValueError("log2_path_length must exceed one")
    root = math.sqrt(log2_path_length)
    return root - math.log2(root)


def second_order_deep_cover_holds(occupancies, mean: int) -> bool:
    """Executable check of the sharpened first-deep-hit cover."""
    if mean < 16:
        raise ValueError("use mean>=16")
    from .tree_score import EMPTY, transfer

    values = tuple(occupancies)
    if any(x < 0 for x in values):
        raise ValueError("occupancies must be nonnegative")

    messages = []
    message = EMPTY
    active = False
    for occupancy in values:
        if not active and occupancy == 0:
            message = EMPTY
        else:
            active = True
            message = transfer(
                occupancy + (0 if message is EMPTY else message)
            )
        messages.append(message)

    threshold = 2 * mean - 1
    deep_times = [
        i
        for i, message in enumerate(messages)
        if message is not EMPTY and message <= -threshold
    ]
    if not deep_times:
        return True
    first_deep = deep_times[0]
    cover = second_order_deep_message_cover(mean)
    k = cover.simplex_steps

    nonnegative_times = [
        i
        for i in range(first_deep)
        if messages[i] is not EMPTY and messages[i] >= 0
    ]
    if nonnegative_times:
        low_start = nonnegative_times[-1]
        if messages[low_start] not in (0, 1):
            return False
    else:
        active_times = [
            i for i in range(first_deep)
            if messages[i] is not EMPTY
        ]
        if not active_times:
            return False
        low_start = active_times[0]
        if messages[low_start] != -1:
            return False

    if first_deep - low_start < k:
        return False
    low_block = values[low_start + 1 : low_start + 1 + k]
    if dyadic_weighted_sum(
        low_block, reverse=True
    ) > cover.low_budget:
        return False

    high_times = [
        i
        for i in range(first_deep)
        if messages[i] is not EMPTY and messages[i] >= mean
    ]
    if not high_times:
        if low_start < cover.cluster_steps:
            return all(
                occupancy <= cover.cluster_cap
                for occupancy in values[: low_start + 1]
            )
        return all(
            occupancy <= cover.cluster_cap
            for occupancy in values[: cover.cluster_steps]
        )

    last_high = high_times[-1]
    entry_times = [
        i
        for i in range(last_high + 1, first_deep)
        if messages[i] is not EMPTY and messages[i] <= 1
    ]
    if not entry_times:
        return False
    entry = entry_times[0]
    if messages[entry] not in (0, 1) or entry - last_high < k:
        return False

    entry_block = values[entry - k + 1 : entry + 1]
    if dyadic_weighted_sum(entry_block) > cover.entry_budget:
        return False

    gap = low_start - entry
    if gap <= cover.cluster_steps:
        return all(
            occupancy <= cover.cluster_cap
            for occupancy in values[entry + 1 : low_start + 1]
        )
    return all(
        occupancy <= cover.cluster_cap
        for occupancy
        in values[entry + 1 : entry + cover.cluster_steps + 1]
    )
