from fractions import Fraction

from prob_stack.exact_probability import exact_probability
from prob_stack.families import path_tree, star_tree


def test_t_zero_and_one_sanity():
    for n in range(1, 7):
        for tree in (path_tree(n), star_tree(n)):
            assert exact_probability(tree, 0).probability == 0
            assert exact_probability(tree, 1).probability == 1


def test_t_two_exact_formula_for_trees():
    for n in range(1, 8):
        for tree in (path_tree(n), star_tree(n)):
            result = exact_probability(tree, 2)
            assert result.stackable_configurations == n
            assert result.probability == Fraction(2, n + 1)


def test_p2_nonmonotone_probability_profile():
    tree = path_tree(2)
    assert exact_probability(tree, 1).probability == 1
    assert exact_probability(tree, 2).probability == Fraction(2, 3)
    assert exact_probability(tree, 3).probability == 1


def test_path_universal_regime_small_orders():
    # Csernak-Soukup prove stack(P_n)=2^n-1; TreeStack's global bound implies
    # every configuration of mass at least that value is stackable.
    for n in range(2, 5):
        tree = path_tree(n)
        threshold = 2**n - 1
        assert exact_probability(tree, threshold).probability == 1
        assert exact_probability(tree, threshold + 1).probability == 1
