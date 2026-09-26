from prob_stack.configurations import weak_compositions
from prob_stack.families import all_labeled_trees, path_tree
from prob_stack.reachability import direct_stackability_oracle, direct_stackable
from prob_stack.tree_score import structurally_stackable


def test_coordinatewise_nonmonotonicity_minimal_example():
    tree = path_tree(2)
    assert direct_stackable(tree, (1, 0))
    assert not direct_stackable(tree, (1, 1))


def test_direct_and_structural_agree_on_small_paths():
    for n in range(1, 6):
        tree = path_tree(n)
        direct = direct_stackability_oracle(tree)
        for t in range(0, 6):
            for c in weak_compositions(t, n):
                assert direct(c) == structurally_stackable(tree, c), (n, t, c)


def test_direct_and_structural_agree_on_all_labeled_trees_through_order_4():
    for n in range(1, 5):
        for tree in all_labeled_trees(n):
            direct = direct_stackability_oracle(tree)
            for t in range(0, 5):
                for c in weak_compositions(t, n):
                    assert direct(c) == structurally_stackable(tree, c), (tree, t, c)
