from prob_stack.configurations import weak_compositions
from prob_stack.path_score import path_structurally_stackable
from prob_stack.soft_front import (
    bounded_dissipation,
    forced_message_threshold,
    has_message_at_most,
    necessity_theorem_holds,
)
from prob_stack.tree_score import transfer


def test_local_dissipation_bound_exhaustively():
    for threshold in range(2, 80):
        for effective in range(-200, threshold):
            if transfer(effective) >= 1 - threshold:
                assert bounded_dissipation(threshold, effective)


def test_forced_message_theorem_exhaustively():
    for n in range(2, 9):
        for t in range(1, 10):
            for configuration in weak_compositions(t, n):
                if not path_structurally_stackable(configuration):
                    assert necessity_theorem_holds(configuration), (n, t, configuration)


def test_integer_mean_corollary():
    for n in range(2, 7):
        for mean in range(1, 4):
            total = n * mean
            for configuration in weak_compositions(total, n):
                if not path_structurally_stackable(configuration):
                    assert has_message_at_most(configuration, 2 * mean - 1), (
                        n,
                        mean,
                        configuration,
                    )
