"""Spatial block certificates for the iid geometric path scan.

The events here are sufficient certificates.  They preserve the exact
TreeStack transfer and keep EMPTY distinct from integer zero.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Iterable

from .product_chain import canonical_deep_deficit_witness, cap_event_probability, log2_cap_event_probability


def reset_length(path_length: int) -> int:
    """Burn-in length making a 2*n*mu incoming upper bound contract to mu/2."""
    if path_length <= 0:
        raise ValueError("path_length must be positive")
    return math.ceil(math.log2(4 * path_length))


def affine_weighted_sum(occupancies: Iterable[int]) -> Fraction:
    """Return sum 2^{-(r-j+1)} X_j for a block of length r."""
    values = tuple(occupancies)
    r = len(values)
    if any(x < 0 for x in values):
        raise ValueError("occupancies must be nonnegative")
    return sum((Fraction(x, 2 ** (r - j + 1)) for j, x in enumerate(values, start=1)), Fraction(0, 1))


def reset_event_holds(mean: int, occupancies: Iterable[int]) -> bool:
    """A local reset event with probability bounded below by a constant.

    The first coordinate is required positive so an EMPTY incoming branch is
    activated.  The affine weighted occupancy contribution is at most 3mu/2.
    """
    values = tuple(occupancies)
    if mean <= 0 or not values:
        raise ValueError("mean and a nonempty block are required")
    return values[0] > 0 and affine_weighted_sum(values) <= Fraction(3 * mean, 2)


def reset_probability_lower_bound(mean: int) -> Fraction:
    """Rigorous lower bound P(reset_event) >= 1/3 - 1/(mu+1).

    Markov gives P(weighted sum > 3mu/2) <= 2/3 because its expectation is
    strictly below mu; P(X_1=0)=1/(mu+1).  A union bound gives the result.
    """
    if mean <= 2:
        raise ValueError("the displayed lower bound is positive only for mean > 2")
    return Fraction(1, 3) - Fraction(1, mean + 1)


def runaway_buffer_caps(mean: int, path_length: int) -> tuple[int, ...]:
    """Deterministic caps amplifying Z>=mu+3 to Z>=2*n*mu+3.

    If Z is the current low-phase deficit, requiring X <= floor(D/4), where D
    is a deterministic lower bound on Z, gives Z' >= 3D/2.  The returned caps
    continue until the certified deficit dominates twice the path's mean total
    mass, which is enough for a true irreversible front on the global event
    total_mass <= 2*n*mu.
    """
    if mean <= 0 or path_length <= 0:
        raise ValueError("mean and path_length must be positive")
    target = 2 * path_length * mean + 3
    lower = Fraction(mean + 3, 1)
    caps: list[int] = []
    while lower < target:
        caps.append(math.floor(lower / 4))
        lower *= Fraction(3, 2)
    return tuple(caps)


def runaway_certified_deficit(mean: int, caps: Iterable[int]) -> Fraction:
    """Certified deficit lower bound after the standard 3/2-growth caps."""
    lower = Fraction(mean + 3, 1)
    for cap in caps:
        if cap > math.floor(lower / 4):
            raise ValueError("cap is too large for the certified 3/2-growth step")
        lower *= Fraction(3, 2)
    return lower


def runaway_probability_lower_bound(mean: int, path_length: int) -> Fraction:
    """Exact product probability for moderate finite buffers."""
    return cap_event_probability(mean, runaway_buffer_caps(mean, path_length))


def runaway_log2_probability_lower_bound(mean: int, path_length: int) -> float:
    """Stable log2 probability of the deterministic runaway cap event."""
    return log2_cap_event_probability(mean, runaway_buffer_caps(mean, path_length))


def geometric_sum_double_mean_chernoff(mean: int, path_length: int) -> float:
    """Chernoff upper bound for P[sum_{1..n} X_i > 2*n*mu]."""
    if mean <= 0 or path_length <= 0:
        raise ValueError("mean and path_length must be positive")
    p = 1.0 / (mean + 1.0)
    r = mean / (mean + 1.0)
    theta = 1.0 / (2.0 * (mean + 1.0))
    mgf = p / (1.0 - r * math.exp(theta))
    return math.exp(path_length * (-2.0 * mean * theta + math.log(mgf)))


@dataclass(frozen=True)
class SpatialFrontCertificate:
    mean: int
    path_length: int
    reset_steps: int
    witness_steps: int
    buffer_steps: int
    block_length: int
    disjoint_blocks: int
    reset_probability_lower: float
    witness_log2_probability: float
    buffer_log2_probability: float
    per_block_log2_probability_lower: float
    total_mass_tail_upper: float

    @property
    def front_probability_lower(self) -> float:
        """Lower bound for occurrence of at least one certified true front."""
        if self.disjoint_blocks == 0:
            return 0.0
        log_a = self.per_block_log2_probability_lower * math.log(2.0)
        a = math.exp(log_a) if log_a > -745 else 0.0
        independent = -math.expm1(self.disjoint_blocks * math.log1p(-a)) if a else 0.0
        return max(0.0, independent - self.total_mass_tail_upper)

def spatial_front_certificate(mean: int, path_length: int) -> SpatialFrontCertificate:
    """Build the disjoint-superblock lower bound for a true one-sided front.

    On the global event total mass <= 2*n*mu, every incoming message is at most
    2*n*mu by the message-versus-mass lemma.  A reset block contracts this to
    at most 2mu; the canonical Session-3 witness ends at message <= -mu; the
    runaway buffer then drives the deficit above 2*n*mu+3.  Hence at that cut
    message + all remaining mass <= 0, a genuine irreversible front.
    """
    if mean < 16:
        raise ValueError("use mean >= 16 for the canonical witness")
    if path_length <= 0:
        raise ValueError("path_length must be positive")
    witness = canonical_deep_deficit_witness(mean)
    r = reset_length(path_length)
    buffer_caps = runaway_buffer_caps(mean, path_length)
    block_length = r + witness.horizon + len(buffer_caps)
    blocks = path_length // block_length
    reset_p = float(reset_probability_lower_bound(mean))
    witness_log2 = witness.log2_probability
    buffer_log2 = log2_cap_event_probability(mean, buffer_caps)
    per_log2 = math.log2(reset_p) + witness_log2 + buffer_log2
    return SpatialFrontCertificate(
        mean=mean,
        path_length=path_length,
        reset_steps=r,
        witness_steps=witness.horizon,
        buffer_steps=len(buffer_caps),
        block_length=block_length,
        disjoint_blocks=blocks,
        reset_probability_lower=reset_p,
        witness_log2_probability=witness_log2,
        buffer_log2_probability=buffer_log2,
        per_block_log2_probability_lower=per_log2,
        total_mass_tail_upper=geometric_sum_double_mean_chernoff(mean, path_length),
    )


def universal_runaway_probability_lower_bound(prefix_terms: int = 10) -> float:
    """Explicit analytic lower bound for the universal infinite product.

    Let a_j=exp(-(3/2)^j/4), j>=0.  We use the first ``prefix_terms`` factors
    exactly and bound the remaining sum geometrically; since
    prod(1-a_j) >= 1-sum a_j on the tail, this gives a true lower bound on
    c_* = prod_{j>=0}(1-a_j).
    """
    if prefix_terms <= 0:
        raise ValueError("prefix_terms must be positive")
    product = 1.0
    for j in range(prefix_terms):
        product *= 1.0 - math.exp(-(1.5**j) / 4.0)
    a = math.exp(-(1.5**prefix_terms) / 4.0)
    ratio = math.exp(-(1.5**prefix_terms) / 8.0)
    tail_sum_upper = a / (1.0 - ratio)
    return product * max(0.0, 1.0 - tail_sum_upper)


def conditioned_total_log_probability(mean: int, path_length: int) -> float:
    """Log P[sum X_i = n*mu] for iid geometrics of integer mean mu."""
    if mean <= 0 or path_length <= 0:
        raise ValueError("mean and path_length must be positive")
    n = path_length
    t = n * mean
    return (
        math.lgamma(n + t)
        - math.lgamma(t + 1)
        - math.lgamma(n)
        - n * math.log(mean + 1.0)
        + t * (math.log(mean) - math.log(mean + 1.0))
    )


def spatial_front_certificate_in_segment(
    mean: int,
    total_path_length: int,
    segment_length: int,
) -> SpatialFrontCertificate:
    """Certificate using blocks inside a segment but reserve budget of whole path."""
    if segment_length <= 0 or segment_length > total_path_length:
        raise ValueError("segment_length must lie in [1,total_path_length]")
    base = spatial_front_certificate(mean, total_path_length)
    return SpatialFrontCertificate(
        mean=base.mean,
        path_length=base.path_length,
        reset_steps=base.reset_steps,
        witness_steps=base.witness_steps,
        buffer_steps=base.buffer_steps,
        block_length=base.block_length,
        disjoint_blocks=segment_length // base.block_length,
        reset_probability_lower=base.reset_probability_lower,
        witness_log2_probability=base.witness_log2_probability,
        buffer_log2_probability=base.buffer_log2_probability,
        per_block_log2_probability_lower=base.per_block_log2_probability_lower,
        total_mass_tail_upper=base.total_mass_tail_upper,
    )


def conditioned_two_sided_failure_bound(mean: int, path_length: int) -> float:
    """Upper bound on failure of the two-half certified nonstackability event.

    Under the product law, use disjoint certified blocks in the left half for a
    left-to-right front and in the right half for the reversed scan.  After
    conditioning on total mass n*mu, either local certificate is a true front
    because its final deficit exceeds 2*n*mu.  A union bound gives

        P_cond[missing at least one half-certificate]
        <= 2 * P_prod[no certificate in one half] / P_prod[T=n*mu].

    This bound is primarily asymptotic; finite values can be very crude.
    """
    if mean < 16 or path_length < 2:
        raise ValueError("mean>=16 and path_length>=2 are required")
    cert = spatial_front_certificate_in_segment(mean, path_length, path_length // 2)
    if cert.disjoint_blocks == 0:
        return 1.0
    log_a = cert.per_block_log2_probability_lower * math.log(2.0)
    a = math.exp(log_a) if log_a > -745 else 0.0
    if a == 0.0:
        return 1.0
    log_no = cert.disjoint_blocks * math.log1p(-a)
    log_total_point = conditioned_total_log_probability(mean, path_length)
    log_bound = math.log(2.0) + log_no - log_total_point
    return 1.0 if log_bound >= 0 else math.exp(log_bound)
