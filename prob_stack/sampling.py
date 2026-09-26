"""Monte Carlo sampling for validated larger instances."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .configurations import sample_uniform_weak_composition
from .families import Tree
from .tree_score import structurally_stackable


@dataclass(frozen=True)
class SamplingResult:
    trials: int
    successes: int
    seed: int | None

    @property
    def estimate(self) -> float:
        return self.successes / self.trials


def sample_stackability(tree: Tree, t: int, trials: int, seed: int | None = None) -> SamplingResult:
    if trials <= 0:
        raise ValueError("trials must be positive")
    rng = Random(seed)
    successes = 0
    for _ in range(trials):
        configuration = sample_uniform_weak_composition(t, len(tree), rng)
        successes += structurally_stackable(tree, configuration)
    return SamplingResult(trials=trials, successes=successes, seed=seed)
