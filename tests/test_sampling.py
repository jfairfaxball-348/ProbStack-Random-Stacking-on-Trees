from prob_stack.families import path_tree
from prob_stack.sampling import sample_stackability


def test_sampling_reproducible():
    tree = path_tree(5)
    a = sample_stackability(tree, t=7, trials=200, seed=12345)
    b = sample_stackability(tree, t=7, trials=200, seed=12345)
    assert a == b


def test_sampling_matches_known_t2_probability_coarsely():
    result = sample_stackability(path_tree(3), t=2, trials=5000, seed=20260926)
    assert abs(result.estimate - 0.5) < 0.04
