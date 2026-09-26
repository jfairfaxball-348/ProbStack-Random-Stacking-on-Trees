from prob_stack.configurations import weak_compositions
from prob_stack.families import path_tree
from prob_stack.path_score import (
    fronts_certify_nonstackability,
    irreversible_deficit_fronts,
    left_incoming_messages,
    low_phase_closed_form,
    low_phase_deficit_update,
    path_scores,
    path_structurally_stackable,
    path_structurally_stackable_pruned,
    right_incoming_messages,
)
from prob_stack.tree_score import EMPTY, directed_messages, scores, transfer


def test_path_messages_match_general_tree_evaluator_exhaustively():
    for n in range(1, 9):
        tree = path_tree(n)
        for t in range(0, 9):
            for c in weak_compositions(t, n):
                left = left_incoming_messages(c)
                right = right_incoming_messages(c)
                messages = directed_messages(tree, c)
                for i in range(1, n):
                    assert left[i] == messages[(i - 1, i)]
                for i in range(n - 1):
                    assert right[i] == messages[(i + 1, i)]
                assert path_scores(c) == scores(tree, c)
                assert path_structurally_stackable(c) == any(x > 0 for x in scores(tree, c))


def test_empty_is_not_integer_zero_on_path():
    assert left_incoming_messages((0, 0, 0)) == (EMPTY, EMPTY, EMPTY)
    assert right_incoming_messages((0, 0, 0)) == (EMPTY, EMPTY, EMPTY)
    assert left_incoming_messages((3, 0))[1] == 0


def test_low_phase_deficit_identity_against_transfer():
    for incoming in range(-20, 6):
        deficit = 3 - incoming
        for occupancy in range(0, 10):
            if occupancy + incoming <= 1:
                next_message = transfer(occupancy + incoming)
                assert 3 - next_message == low_phase_deficit_update(deficit, occupancy)


def test_low_phase_closed_form():
    initial = 11
    block = (0, 1, 0, 2)
    iterative = low_phase_closed_form(initial, block)
    explicit = (2 ** len(block)) * initial - sum(
        (2 ** (len(block) - j)) * 2 * occupancy
        for j, occupancy in enumerate(block, start=1)
    )
    assert iterative == explicit


def test_irreversible_front_certificate_is_sound_exhaustively():
    for n in range(2, 9):
        for t in range(1, 9):
            for c in weak_compositions(t, n):
                if fronts_certify_nonstackability(c):
                    assert not path_structurally_stackable(c), c


def test_front_examples_and_nonconverse():
    assert fronts_certify_nonstackability((1, 0, 1))
    assert not path_structurally_stackable((1, 0, 1))
    assert not fronts_certify_nonstackability((1, 0, 2))
    assert not path_structurally_stackable((1, 0, 2))
    assert irreversible_deficit_fronts((1, 0, 2)) == (2, 0)


def test_pruned_evaluator_matches_full_path_scores_exhaustively():
    for n in range(1, 10):
        for t in range(0, 11):
            for c in weak_compositions(t, n):
                assert path_structurally_stackable_pruned(c) == path_structurally_stackable(c), c
