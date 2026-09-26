"""Exact direct legal-move search for small instances.

This module deliberately has no dependency on ``tree_score``.  It is the slow
small-instance ground truth used to validate the structural evaluator.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Callable, Iterator

from .configurations import Configuration, validate_configuration
from .families import Tree, validate_tree


def legal_children(tree: Tree, configuration: Configuration) -> Iterator[Configuration]:
    state = validate_configuration(configuration, len(tree))
    for source, value in enumerate(state):
        if value < 2:
            continue
        for target in tree[source]:
            child = list(state)
            child[source] -= 2
            child[target] += 1
            yield tuple(child)


def is_stacked(configuration: Configuration) -> bool:
    """A stacked configuration has positive mass supported on one vertex."""
    return sum(value > 0 for value in configuration) == 1


def direct_stackability_oracle(tree: Tree) -> Callable[[Configuration], bool]:
    """Return a memoized direct stackability predicate for one fixed tree."""
    validate_tree(tree)

    @lru_cache(maxsize=None)
    def search(state: Configuration) -> bool:
        if is_stacked(state):
            return True
        return any(search(child) for child in legal_children(tree, state))

    def checked(configuration: Configuration) -> bool:
        return search(validate_configuration(configuration, len(tree)))

    return checked


def direct_stackable(tree: Tree, configuration: Configuration) -> bool:
    """Decide stackability by exhaustive forward legal-move search."""
    return direct_stackability_oracle(tree)(configuration)


def direct_target_oracle(tree: Tree, root: int) -> Callable[[Configuration], bool]:
    """Return a memoized exact predicate for stackability at ``root``."""
    validate_tree(tree)
    if not 0 <= root < len(tree):
        raise ValueError("root is not a vertex")

    @lru_cache(maxsize=None)
    def search(state: Configuration) -> bool:
        if state[root] > 0 and all(value == 0 for v, value in enumerate(state) if v != root):
            return True
        return any(search(child) for child in legal_children(tree, state))

    def checked(configuration: Configuration) -> bool:
        return search(validate_configuration(configuration, len(tree)))

    return checked


def direct_stackable_at(tree: Tree, configuration: Configuration, root: int) -> bool:
    """Decide whether a positive stack at ``root`` is legally reachable."""
    return direct_target_oracle(tree, root)(configuration)
