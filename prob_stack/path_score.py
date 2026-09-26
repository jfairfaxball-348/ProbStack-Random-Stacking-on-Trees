"""Path-specialized TreeStack message dynamics.

Vertices are indexed 0,...,n-1.  ``EMPTY`` is categorical and is never
identified with integer zero.
"""
from __future__ import annotations

from .configurations import Configuration, validate_configuration
from .tree_score import EMPTY, Message, transfer


def left_incoming_messages(configuration: Configuration) -> tuple[Message, ...]:
    """Return L_i, the message from the left component into vertex i.

    L_0 = EMPTY.  For i<n-1, the outgoing prefix message from i to i+1 is
    EMPTY exactly while C_0=...=C_i=0; otherwise it is

        F(C_i + L_i),

    where the EMPTY contribution is omitted rather than replaced as a state.
    """
    state = validate_configuration(configuration)
    n = len(state)
    incoming: list[Message] = [EMPTY] * n
    active = False
    message: Message = EMPTY
    for i in range(n - 1):
        if not active and state[i] == 0:
            message = EMPTY
        else:
            active = True
            effective = state[i] + (message if message is not EMPTY else 0)
            message = transfer(effective)
        incoming[i + 1] = message
    return tuple(incoming)


def right_incoming_messages(configuration: Configuration) -> tuple[Message, ...]:
    """Return R_i, the message from the right component into vertex i."""
    state = validate_configuration(configuration)
    n = len(state)
    incoming: list[Message] = [EMPTY] * n
    active = False
    message: Message = EMPTY
    for i in range(n - 1, 0, -1):
        if not active and state[i] == 0:
            message = EMPTY
        else:
            active = True
            effective = state[i] + (message if message is not EMPTY else 0)
            message = transfer(effective)
        incoming[i - 1] = message
    return tuple(incoming)


def path_scores(configuration: Configuration) -> tuple[int, ...]:
    """Return all rooted TreeStack scores on the path in two linear scans."""
    state = validate_configuration(configuration)
    left = left_incoming_messages(state)
    right = right_incoming_messages(state)
    return tuple(
        state[i]
        + (left[i] if left[i] is not EMPTY else 0)
        + (right[i] if right[i] is not EMPTY else 0)
        for i in range(len(state))
    )


def path_structurally_stackable(configuration: Configuration) -> bool:
    """Exact path stackability predicate via max_i S_i > 0."""
    return any(score > 0 for score in path_scores(configuration))


def low_phase_deficit_update(deficit: int, occupancy: int) -> int:
    """Update Z=3-m in the low phase C+m<=1.

    If m is the incoming integer message and Z=3-m, then the TreeStack
    transfer is in its x<=1 branch exactly when occupancy <= Z-2.  In that
    branch the next deficit is 2*(Z-occupancy).
    """
    if occupancy < 0:
        raise ValueError("occupancy must be nonnegative")
    if occupancy > deficit - 2:
        raise ValueError("update is only valid in the low phase")
    return 2 * (deficit - occupancy)


def low_phase_closed_form(initial_deficit: int, occupancies: tuple[int, ...]) -> int:
    """Closed form for a block that remains wholly in the low phase.

    The caller supplies Z_0=3-m_0.  The function checks the low-phase
    inequalities along the way and returns

        Z_k = 2^k Z_0 - sum_{j=1}^k 2^(k-j+1) C_j.
    """
    deficit = initial_deficit
    for occupancy in occupancies:
        deficit = low_phase_deficit_update(deficit, occupancy)
    return deficit


def irreversible_deficit_fronts(configuration: Configuration) -> tuple[int | None, int | None]:
    """Return one-sided exclusion fronts certified by remaining total mass.

    The first component is the smallest vertex j such that the prefix message
    L_j plus all mass on vertices j,...,n-1 is <= 0.  Then every target at or
    to the right of j has nonpositive score.

    The second component is the largest vertex j such that R_j plus all mass
    on vertices 0,...,j is <= 0.  Then every target at or to the left of j has
    nonpositive score.  Scans stop at the first such certificate, before the
    negative recurrence can grow to enormous integers.
    """
    state = validate_configuration(configuration)
    n = len(state)
    total = sum(state)

    active = False
    message: Message = EMPTY
    prefix_mass = 0
    left_front: int | None = None
    for i in range(n - 1):
        prefix_mass += state[i]
        if not active and state[i] == 0:
            message = EMPTY
        else:
            active = True
            message = transfer(state[i] + (message if message is not EMPTY else 0))
        if message is not EMPTY and message + (total - prefix_mass) <= 0:
            left_front = i + 1
            break

    active = False
    message = EMPTY
    suffix_mass = 0
    right_front: int | None = None
    for i in range(n - 1, 0, -1):
        suffix_mass += state[i]
        if not active and state[i] == 0:
            message = EMPTY
        else:
            active = True
            message = transfer(state[i] + (message if message is not EMPTY else 0))
        if message is not EMPTY and message + (total - suffix_mass) <= 0:
            right_front = i - 1
            break

    return left_front, right_front


def fronts_certify_nonstackability(configuration: Configuration) -> bool:
    """Whether the two irreversible one-sided exclusion regions cover the path."""
    left_front, right_front = irreversible_deficit_fronts(configuration)
    return (
        left_front is not None
        and right_front is not None
        and left_front <= right_front + 1
    )


def path_structurally_stackable_pruned(configuration: Configuration) -> bool:
    """Exact stackability decision with irreversible-deficit pruning.

    A left scan stops after an outgoing prefix message m satisfies
    m + (all mass still to its right) <= 0; every root farther right is then
    impossible.  The symmetric right scan gives a left exclusion region.
    Only roots not excluded by either front need their exact two-sided scores.

    This returns exactly the same predicate as ``path_structurally_stackable``
    but avoids constructing exponentially large negative messages after a
    deficit becomes irreversible.
    """
    state = validate_configuration(configuration)
    n = len(state)
    total = sum(state)
    if total == 0:
        return False

    left: list[Message] = [EMPTY] * n
    active = False
    message: Message = EMPTY
    prefix_mass = 0
    left_front: int | None = None
    for i in range(n - 1):
        prefix_mass += state[i]
        if not active and state[i] == 0:
            message = EMPTY
        else:
            active = True
            effective = state[i] + (message if message is not EMPTY else 0)
            message = transfer(effective)
        left[i + 1] = message
        remaining = total - prefix_mass
        if message is not EMPTY and message + remaining <= 0:
            left_front = i + 1
            break

    right: list[Message] = [EMPTY] * n
    active = False
    message = EMPTY
    suffix_mass = 0
    right_front: int | None = None
    for i in range(n - 1, 0, -1):
        suffix_mass += state[i]
        if not active and state[i] == 0:
            message = EMPTY
        else:
            active = True
            effective = state[i] + (message if message is not EMPTY else 0)
            message = transfer(effective)
        right[i - 1] = message
        remaining = total - suffix_mass
        if message is not EMPTY and message + remaining <= 0:
            right_front = i - 1
            break

    lo = 0 if right_front is None else right_front + 1
    hi = n - 1 if left_front is None else left_front - 1
    if lo > hi:
        return False

    for i in range(lo, hi + 1):
        score = state[i]
        if left[i] is not EMPTY:
            score += left[i]
        if right[i] is not EMPTY:
            score += right[i]
        if score > 0:
            return True
    return False
