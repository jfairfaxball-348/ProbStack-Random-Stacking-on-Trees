"""Deterministic deep-message necessity for nonstackable paths.

This module keeps EMPTY categorical.  Integer zero is used only as the
arithmetic contribution of an absent branch when writing a rooted score.
"""
from __future__ import annotations

from .configurations import Configuration, validate_configuration
from .path_score import (
    left_incoming_messages,
    path_scores,
    right_incoming_messages,
)
from .tree_score import EMPTY, transfer


def transfer_dissipation(effective: int) -> int:
    """Return the one-step loss effective - F(effective)."""
    return effective - transfer(effective)


def dissipation_cap(threshold: int) -> int:
    """The sharp cap floor(h/2)+1 used in the necessity argument."""
    if threshold < 2:
        raise ValueError("threshold must be at least 2")
    return threshold // 2 + 1


def bounded_dissipation(threshold: int, effective: int) -> bool:
    """Check the local implication behind the global necessity theorem.

    If h>=2, effective<=h-1, and F(effective)>=1-h, then

        effective - F(effective) <= floor(h/2)+1.
    """
    if threshold < 2:
        raise ValueError("threshold must be at least 2")
    if effective > threshold - 1 or transfer(effective) < 1 - threshold:
        raise ValueError("hypotheses of the dissipation bound are not met")
    return transfer_dissipation(effective) <= dissipation_cap(threshold)


def forced_message_threshold(order: int, total_mass: int) -> int:
    """Largest threshold certified by the prefix-dissipation argument.

    For h>=2 the theorem applies whenever

        total_mass > (order-1) * (floor(h/2)+1).

    The h=1 case is handled separately: a positive-mass nonstackable path
    cannot have every directed integer message nonnegative.
    """
    if order < 2 or total_mass <= 0:
        raise ValueError("order>=2 and positive total mass are required")
    quotient = (total_mass - 1) // (order - 1)
    return max(1, 2 * quotient - 1)


def has_message_at_most(configuration: Configuration, threshold: int) -> bool:
    """Whether either directional scan contains an integer message <= -threshold."""
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    state = validate_configuration(configuration)
    messages = left_incoming_messages(state) + right_incoming_messages(state)
    return any(message is not EMPTY and message <= -threshold for message in messages)


def necessity_theorem_holds(configuration: Configuration) -> bool:
    """Executable bounded-instance check of the deterministic theorem.

    Stackable configurations return True vacuously.  Positive-mass
    nonstackable configurations must contain a directed message at most the
    negative forced threshold.
    """
    state = validate_configuration(configuration)
    if len(state) < 2 or sum(state) == 0:
        return True
    if max(path_scores(state)) > 0:
        return True
    threshold = forced_message_threshold(len(state), sum(state))
    return has_message_at_most(state, threshold)
