"""TreeStack structural branch-message evaluator.

Provenance
----------
This module independently reimplements the mathematical definitions in the
TreeStack repository, inspected at:

    jfairfaxball-348/TreeStack-Structural-Certificates-for-Stacking-on-Trees
    main commit f4112f08d42a37c0941bf469ac124621b1f54f22

Authoritative formal sources at that revision are ``TreeStack/Transfer.lean``,
``TreeStack/Message.lean`` and ``TreeStack/RootScore.lean``.  In particular,
TreeStack proves ``StackableAt(T,C,r) <-> 0 < score(T,C,r)``.

The categorical empty-branch marker is represented by ``None`` and is kept
distinct from the integer message 0.  Do not change the transfer map or merge
those states without revalidating against the authoritative theorem.

This implementation does not call the direct reachability solver.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from .configurations import Configuration, validate_configuration
from .families import Tree, validate_tree

Message = Optional[int]
EMPTY: Message = None


def transfer(x: int) -> int:
    """Exact TreeStack one-edge transfer F: Z -> Z."""
    if x <= 1:
        return 2 * x - 3
    if x == 2:
        return 1
    if x == 3:
        return 0
    if x % 2 == 0:
        return x // 2
    return (x - 3) // 2


def directed_messages(tree: Tree, configuration: Configuration) -> dict[tuple[int, int], Message]:
    """Compute every oriented-edge branch message in linear time.

    The mathematical recurrence is exactly TreeStack's branch-message
    definition.  The implementation is iterative rather than recursively
    descending each branch, which avoids Python recursion-depth limits on long
    paths and other tall trees.
    """
    validate_tree(tree)
    state = validate_configuration(configuration, len(tree))
    n = len(tree)
    if n <= 1:
        return {}

    # Root the tree at 0 solely to schedule the two message-passing sweeps.
    # This auxiliary root has no mathematical role in the resulting oriented
    # messages.
    parent = [-2] * n
    parent[0] = -1
    order = [0]
    for vertex in order:
        for neighbor in tree[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                continue
            parent[neighbor] = vertex
            order.append(neighbor)

    messages: dict[tuple[int, int], Message] = {}

    # Postorder computes every child -> parent message.
    for vertex in reversed(order[1:]):
        par = parent[vertex]
        incoming = [messages[(u, vertex)] for u in tree[vertex] if u != par]
        occupied = state[vertex] > 0 or any(item is not EMPTY for item in incoming)
        if not occupied:
            messages[(vertex, par)] = EMPTY
        else:
            effective = state[vertex] + sum(item for item in incoming if item is not EMPTY)
            messages[(vertex, par)] = transfer(effective)

    # Preorder computes every parent -> child message.  When vertex is reached,
    # all messages into it are already known: descendants from the postorder
    # sweep and the parent-side message from the preceding preorder step.
    for vertex in order:
        total_contribution = state[vertex]
        nonempty_inputs = 0
        if state[vertex] > 0:
            nonempty_inputs += 1
        for neighbor in tree[vertex]:
            msg = messages.get((neighbor, vertex), EMPTY)
            if msg is not EMPTY:
                total_contribution += msg
                nonempty_inputs += 1

        for child in tree[vertex]:
            if parent[child] != vertex:
                continue
            child_msg = messages[(child, vertex)]
            branch_nonempty_inputs = nonempty_inputs - (child_msg is not EMPTY)
            if branch_nonempty_inputs == 0:
                messages[(vertex, child)] = EMPTY
            else:
                effective = total_contribution - (child_msg if child_msg is not EMPTY else 0)
                messages[(vertex, child)] = transfer(effective)

    return messages


def scores(tree: Tree, configuration: Configuration) -> tuple[int, ...]:
    """Return the exact TreeStack rooted scores S_r(C) for all roots."""
    state = validate_configuration(configuration, len(tree))
    messages = directed_messages(tree, state)
    return tuple(
        state[root]
        + sum(messages[(u, root)] for u in tree[root] if messages[(u, root)] is not EMPTY)
        for root in range(len(tree))
    )


def structurally_stackable_at(tree: Tree, configuration: Configuration, root: int) -> bool:
    if not 0 <= root < len(tree):
        raise ValueError("root is not a vertex")
    return scores(tree, configuration)[root] > 0


def structurally_stackable(tree: Tree, configuration: Configuration) -> bool:
    return any(score > 0 for score in scores(tree, configuration))
