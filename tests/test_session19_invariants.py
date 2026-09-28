from pathlib import Path

from prob_stack.global_conditioning import (
    global_balance_diagnostic,
    one_block_transfer_log_bound,
    separated_blocks_transfer_log_bound,
)
from prob_stack.supercritical import deep_threshold


TREE_STACK_PIN = "f4112f08d42a37c0941bf469ac124621b1f54f22"
MATHLIB_PIN = "065356127b1dc0016f66b7283ce0ce2c4055aa55"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.35.0-rc2"


def test_exact_supercritical_deep_target_is_two_mu_minus_one():
    for mean in (2, 16, 31, 64, 257):
        assert deep_threshold(mean) == 2 * mean - 1
        assert deep_threshold(mean) != mean


def test_global_balance_keeps_the_spatial_factor_n():
    for N in (256.0, 1024.0, 4096.0):
        diagnostic = global_balance_diagnostic(N, -0.5)
        assert diagnostic.log2_n_times_local_hazard == (
            N - diagnostic.local_rate_main
        )


def test_separated_conditioned_blocks_are_concatenated_not_independent():
    mean = 512
    n = 2**60
    k = 200
    mass = 5000
    two = separated_blocks_transfer_log_bound(
        mean, n, k, mass, blocks=2
    )
    concatenated = one_block_transfer_log_bound(
        mean, n, 2 * k, 2 * mass
    )
    assert two == concatenated


def test_dependency_pins_and_permanent_workflow_semantics_are_frozen():
    lakefile = Path("lakefile.lean").read_text()
    manifest = Path("lake-manifest.json").read_text()
    toolchain = Path("lean-toolchain").read_text().strip()
    workflow = Path(".github/workflows/lean-bootstrap.yml").read_text()

    assert TREE_STACK_PIN in lakefile
    assert TREE_STACK_PIN in manifest
    assert MATHLIB_PIN in manifest
    assert toolchain == LEAN_TOOLCHAIN
    assert (
        "key: treestack-"
        + TREE_STACK_PIN
        + "-lean-4.35.0-rc2"
    ) in workflow
    assert "Found forbidden sorry/axiom" in workflow
