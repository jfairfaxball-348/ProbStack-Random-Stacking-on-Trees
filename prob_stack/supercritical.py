"""Local cap covering for the Session 5 supercritical path theorem.

The product-law estimates here are upper bounds for occurrence of a directed
message <= -(2*mean-1).  They are then transferred to the fixed-total weak
composition model by the exact local likelihood-ratio estimate from Session 3.

EMPTY remains categorical throughout the scan.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

from .product_chain import (
    conditioning_log_ratio_bound,
    log2_cap_event_probability,
)
from .tree_score import EMPTY, transfer


def deep_threshold(mean: int) -> int:
    if mean <= 0:
        raise ValueError("mean must be positive")
    return 2 * mean - 1


def entry_caps(mean: int) -> tuple[int, ...]:
    """Forward-order caps forced by an interior descent from M>=mean to M<=1."""
    if mean < 16:
        raise ValueError("use mean>=16")
    level = math.ceil(math.log2(mean))
    length = max(1, level - 3)

    # Backward from the entry step the effective-value bounds are
    # 5, 13, 29, ... = 8*2^j-3.  Reverse them to match coordinate order.
    backward = [5]
    backward.extend(8 * (2**j) - 3 for j in range(1, length))
    return tuple(reversed(backward))


def low_run_caps(mean: int) -> tuple[int, ...]:
    """Caps forced at the start of a final low run to depth 2*mean-1.

    A run beginning from message in {-1,0,1} has initial deficit at most 4.
    Before the j-th low-phase update its deficit is at most 4*2^(j-1), so the
    occupancy must be at most 4*2^(j-1)-2.
    """
    if mean < 16:
        raise ValueError("use mean>=16")
    level = math.ceil(math.log2(mean))
    length = max(1, level - 2)
    return tuple(4 * (2 ** (j - 1)) - 2 for j in range(1, length + 1))


def cluster_cap(mean: int) -> int:
    """Occupancy cap necessary to avoid an immediate return to M>=mean."""
    if mean <= 0:
        raise ValueError("mean must be positive")
    return 4 * mean


def _log2_geometric_cdf(mean: int, cap: int) -> float:
    if mean <= 0:
        raise ValueError("mean must be positive")
    if cap < 0:
        return -math.inf
    log_ratio = math.log1p(-1.0 / (mean + 1.0))
    return math.log2(-math.expm1((cap + 1) * log_ratio))


def cluster_length(mean: int) -> int:
    """Choose R so P[X<=4*mean]^R <= P[the forced low-run caps]."""
    low_log2 = log2_cap_event_probability(mean, low_run_caps(mean))
    one_step_log2 = _log2_geometric_cdf(mean, cluster_cap(mean))
    return max(1, math.ceil(low_log2 / one_step_log2))


@dataclass(frozen=True)
class DeepMessageCover:
    mean: int
    entry_caps: tuple[int, ...]
    low_caps: tuple[int, ...]
    cluster_cap: int
    cluster_steps: int
    entry_log2_probability: float
    low_log2_probability: float
    cluster_log2_probability: float
    max_window_length: int
    max_window_mass: int

    @property
    def interior_log2_probability(self) -> float:
        return self.entry_log2_probability + self.low_log2_probability


def deep_message_cover(mean: int) -> DeepMessageCover:
    """Construct the cap families used in the product and conditioned bounds."""
    entry = entry_caps(mean)
    low = low_run_caps(mean)
    middle_cap = cluster_cap(mean)
    middle_steps = cluster_length(mean)
    middle_log2 = middle_steps * _log2_geometric_cdf(mean, middle_cap)
    return DeepMessageCover(
        mean=mean,
        entry_caps=entry,
        low_caps=low,
        cluster_cap=middle_cap,
        cluster_steps=middle_steps,
        entry_log2_probability=log2_cap_event_probability(mean, entry),
        low_log2_probability=log2_cap_event_probability(mean, low),
        cluster_log2_probability=middle_log2,
        max_window_length=len(entry) + middle_steps + len(low),
        max_window_mass=sum(entry) + middle_cap * middle_steps + sum(low),
    )


def log2_product_direction_deep_upper(mean: int, steps: int) -> float:
    """Log2 union upper bound for a deep message in one directional scan.

    Boundary-origin witnesses contribute (R+1)b.  Interior witnesses contribute
    at most steps*(R+2)ab, where a is the entry-cap probability and b is the
    final low-run probability.
    """
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    cover = deep_message_cover(mean)
    boundary = math.log2(cover.cluster_steps + 1) + cover.low_log2_probability
    if steps == 0:
        return boundary
    interior = (
        math.log2(steps)
        + math.log2(cover.cluster_steps + 2)
        + cover.interior_log2_probability
    )
    pivot = max(boundary, interior)
    return pivot + math.log2(
        2 ** (boundary - pivot) + 2 ** (interior - pivot)
    )


def product_direction_deep_upper(mean: int, steps: int) -> float:
    """Probability upper bound corresponding to log2_product_direction_deep_upper."""
    log2_bound = log2_product_direction_deep_upper(mean, steps)
    if log2_bound >= 0:
        return 1.0
    if log2_bound < -1074:
        return 0.0
    return 2**log2_bound


def _scan_messages(occupancies: Iterable[int]) -> tuple[int | None, ...]:
    """Exact one-sided scan from EMPTY, used only by deterministic tests."""
    messages: list[int | None] = []
    message = EMPTY
    active = False
    for occupancy in occupancies:
        if occupancy < 0:
            raise ValueError("occupancies must be nonnegative")
        if not active and occupancy == 0:
            message = EMPTY
        else:
            active = True
            message = transfer(occupancy + (message if message is not EMPTY else 0))
        messages.append(message)
    return tuple(messages)


def deep_cover_holds(occupancies: Iterable[int], mean: int) -> bool:
    """Executable check of the deterministic cap-cover implication.

    If no deep message occurs the result is vacuous.  Otherwise the first deep
    message must be covered by either a boundary-origin witness or an interior
    entry + bounded-cluster + low-run witness.
    """
    values = tuple(occupancies)
    messages = _scan_messages(values)
    threshold = deep_threshold(mean)
    deep_times = [
        i for i, message in enumerate(messages)
        if message is not EMPTY and message <= -threshold
    ]
    if not deep_times:
        return True

    first_deep = deep_times[0]
    cover = deep_message_cover(mean)

    high_times = [
        i for i in range(first_deep)
        if messages[i] is not EMPTY and messages[i] >= mean
    ]

    nonnegative_times = [
        i for i in range(first_deep)
        if messages[i] in (0, 1)
    ]
    if nonnegative_times:
        low_start = nonnegative_times[-1]
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

    if low_start + len(cover.low_caps) > first_deep:
        return False
    if any(
        values[low_start + 1 + j] > cap
        for j, cap in enumerate(cover.low_caps)
    ):
        return False

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
        i for i in range(last_high + 1, first_deep)
        if messages[i] is not EMPTY and messages[i] <= 1
    ]
    if not entry_times:
        return False
    entry = entry_times[0]
    if messages[entry] not in (0, 1):
        return False

    entry_start = entry - len(cover.entry_caps) + 1
    if entry_start < 0:
        return False
    if any(
        values[entry_start + j] > cap
        for j, cap in enumerate(cover.entry_caps)
    ):
        return False

    gap = low_start - entry
    if gap <= cover.cluster_steps:
        return all(
            occupancy <= cover.cluster_cap
            for occupancy in values[entry + 1 : low_start + 1]
        )
    return all(
        occupancy <= cover.cluster_cap
        for occupancy in values[
            entry + 1 : entry + cover.cluster_steps + 1
        ]
    )


def conditioned_nonstackable_log2_upper(mean: int, path_length: int) -> float:
    """Log2 upper bound for fixed-total nonstackability at total n*mean.

    The deterministic necessity theorem reduces nonstackability to a deep
    message in one of the two directional scans.  Every cap witness has block
    length at most max_window_length and block mass at most max_window_mass, so
    the Session 3 local likelihood-ratio bound transfers the product union
    bound.  Values >=0 should be read as the trivial probability bound 1.
    """
    if mean < 16 or path_length < 2:
        raise ValueError("mean>=16 and path_length>=2 are required")
    cover = deep_message_cover(mean)
    total = mean * path_length
    delta = conditioning_log_ratio_bound(
        path_length,
        total,
        cover.max_window_length,
        cover.max_window_mass,
    )
    one_direction = log2_product_direction_deep_upper(mean, path_length - 1)
    return 1.0 + delta / math.log(2.0) + one_direction
