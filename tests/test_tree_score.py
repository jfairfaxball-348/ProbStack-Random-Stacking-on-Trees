from prob_stack.families import path_tree, star_tree
from prob_stack.tree_score import EMPTY, directed_messages, scores, structurally_stackable, transfer


def test_transfer_exact_cases():
    expected = {
        -2: -7,
        -1: -5,
        0: -3,
        1: -1,
        2: 1,
        3: 0,
        4: 2,
        5: 1,
        6: 3,
        7: 2,
    }
    assert {x: transfer(x) for x in expected} == expected


def test_empty_message_distinct_from_integer_zero():
    tree = path_tree(2)
    messages = directed_messages(tree, (0, 0))
    assert messages[(0, 1)] is EMPTY
    assert messages[(1, 0)] is EMPTY


def test_single_supported_configuration_is_structurally_stackable():
    for tree in (path_tree(5), star_tree(5)):
        for root in range(len(tree)):
            c = tuple(3 if v == root else 0 for v in range(len(tree)))
            assert structurally_stackable(tree, c)
            assert scores(tree, c)[root] > 0


def test_iterative_messages_handle_long_paths_without_recursion_failure() -> None:
    tree = path_tree(1500)
    configuration = (0,) * 1499 + (1,)
    assert structurally_stackable(tree, configuration)
