"""Deterministic tree representations and small standard families."""

from __future__ import annotations

from collections import deque
from itertools import product
from typing import Iterable, Iterator, Sequence

Tree = tuple[tuple[int, ...], ...]


def tree_from_edges(n: int, edges: Iterable[tuple[int, int]]) -> Tree:
    """Build and validate a labeled tree on vertices ``0, ..., n-1``."""
    if n <= 0:
        raise ValueError("a tree must have at least one vertex")
    adjacency = [set() for _ in range(n)]
    edge_count = 0
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("edge endpoint outside vertex set")
        if u == v:
            raise ValueError("loops are not allowed")
        if v in adjacency[u]:
            raise ValueError("duplicate edge")
        adjacency[u].add(v)
        adjacency[v].add(u)
        edge_count += 1
    tree = tuple(tuple(sorted(neighbors)) for neighbors in adjacency)
    validate_tree(tree)
    if edge_count != n - 1:
        raise ValueError("a tree on n vertices must have n-1 edges")
    return tree


def validate_tree(tree: Tree) -> Tree:
    """Validate symmetry, connectedness, and the tree edge count."""
    n = len(tree)
    if n == 0:
        raise ValueError("a tree must have at least one vertex")
    degree_sum = 0
    for v, neighbors in enumerate(tree):
        if len(set(neighbors)) != len(neighbors):
            raise ValueError("duplicate neighbor")
        for u in neighbors:
            if not 0 <= u < n:
                raise ValueError("neighbor outside vertex set")
            if u == v:
                raise ValueError("loops are not allowed")
            if v not in tree[u]:
                raise ValueError("adjacency must be symmetric")
        degree_sum += len(neighbors)
    if degree_sum % 2:
        raise ValueError("invalid undirected degree sum")
    if degree_sum // 2 != n - 1:
        raise ValueError("graph does not have n-1 edges")
    seen = {0}
    queue = deque([0])
    while queue:
        v = queue.popleft()
        for u in tree[v]:
            if u not in seen:
                seen.add(u)
                queue.append(u)
    if len(seen) != n:
        raise ValueError("graph is disconnected")
    return tree


def path_tree(n: int) -> Tree:
    if n <= 0:
        raise ValueError("n must be positive")
    return tree_from_edges(n, ((i, i + 1) for i in range(n - 1)))


def star_tree(n: int) -> Tree:
    if n <= 0:
        raise ValueError("n must be positive")
    return tree_from_edges(n, ((0, i) for i in range(1, n)))


def complete_bary_tree(branching: int, height: int) -> Tree:
    """Return the complete rooted b-ary tree of edge-height ``height``."""
    if branching < 1 or height < 0:
        raise ValueError("branching >= 1 and height >= 0 are required")
    if height == 0:
        return ((),)
    n = sum(branching**level for level in range(height + 1))
    edges: list[tuple[int, int]] = []
    next_child = 1
    level_start = 0
    level_size = 1
    for _ in range(height):
        for parent in range(level_start, level_start + level_size):
            for _ in range(branching):
                edges.append((parent, next_child))
                next_child += 1
        level_start += level_size
        level_size *= branching
    return tree_from_edges(n, edges)


def prufer_tree(sequence: Sequence[int], n: int | None = None) -> Tree:
    """Decode a Prüfer sequence into its labeled tree."""
    if n is None:
        n = len(sequence) + 2
    if n == 1:
        if sequence:
            raise ValueError("one-vertex tree has empty Prüfer sequence")
        return ((),)
    if len(sequence) != n - 2:
        raise ValueError("Prüfer sequence length must be n-2")
    if any(not 0 <= x < n for x in sequence):
        raise ValueError("Prüfer symbol outside vertex set")
    degree = [1] * n
    for x in sequence:
        degree[x] += 1
    edges: list[tuple[int, int]] = []
    for x in sequence:
        leaf = next(i for i, d in enumerate(degree) if d == 1)
        edges.append((leaf, x))
        degree[leaf] -= 1
        degree[x] -= 1
    leaves = [i for i, d in enumerate(degree) if d == 1]
    edges.append((leaves[0], leaves[1]))
    return tree_from_edges(n, edges)


def all_labeled_trees(n: int) -> Iterator[Tree]:
    """Enumerate all labeled trees using Prüfer sequences (small n only)."""
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        yield ((),)
        return
    for sequence in product(range(n), repeat=n - 2):
        yield prufer_tree(sequence, n)
