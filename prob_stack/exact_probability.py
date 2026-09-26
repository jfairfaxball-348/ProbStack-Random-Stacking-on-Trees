"""Exact counting under the uniform weak-composition model."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Iterable

from .configurations import Configuration, number_of_configurations, weak_compositions
from .families import Tree
from .tree_score import structurally_stackable

StackabilityPredicate = Callable[[Tree, Configuration], bool]


@dataclass(frozen=True)
class ExactProbability:
    n: int
    t: int
    total_configurations: int
    stackable_configurations: int

    @property
    def nonstackable_configurations(self) -> int:
        return self.total_configurations - self.stackable_configurations

    @property
    def probability(self) -> Fraction:
        return Fraction(self.stackable_configurations, self.total_configurations)


def exact_probability(
    tree: Tree,
    t: int,
    predicate: StackabilityPredicate = structurally_stackable,
) -> ExactProbability:
    """Count stackable configurations exactly and return a rational probability."""
    total = number_of_configurations(len(tree), t)
    stackable = sum(predicate(tree, configuration) for configuration in weak_compositions(t, len(tree)))
    return ExactProbability(len(tree), t, total, stackable)


def exact_records(tree: Tree, t_values: Iterable[int]) -> list[ExactProbability]:
    return [exact_probability(tree, t) for t in t_values]
