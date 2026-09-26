# Session 10 handover

## Starting state

Session 10 started from verified ProbStack `main`:

`595566b350a6a5b93dd6184dc3bbb99e162e9c7c`.

Authoritative TreeStack:

`f4112f08d42a37c0941bf469ac124621b1f54f22`.

Inherited Mathlib:

`065356127b1dc0016f66b7283ce0ce2c4055aa55`.

Pinned Lean:

`leanprover/lean4:v4.35.0-rc2`.

## What Session 10 completed

The ProbStack Lean package now exists and compiles.

It contains:

- an exact TreeStack import boundary;
- a `TreeStack.FiniteTree (Fin n)` wrapper whose graph is exactly
  `SimpleGraph.pathGraph n`;
- a path-specific acyclicity proof using a maximum vertex of a hypothetical
  cycle;
- a categorical scalar `pathStep : TreeStack.Message → Nat → TreeStack.Message`;
- formal EMPTY persistence/activation for that scalar step;
- `F_le_half` with Lean integer division;
- path-friendly even/odd transfer identities;
- the exact low-phase deficit one-step recurrence;
- an exact two-step low-phase sanity identity;
- deterministic regeneration steering-window arithmetic;
- the exact transfer-window theorem sending effective input
  `[2*mu+2, 4*mu]` into `[mu, 2*mu]`.

The validating source/audit commit before documentation was

`4631e822ee7707c0f7ec89b239e5991dd6dfdec1`.

At that commit `lake build` completed successfully and the CI grep found no
local `sorry` or `axiom`.

## Exact environment

CI reported:

```text
Lean (version 4.35.0-rc2, x86_64-unknown-linux-gnu,
  commit 11acb17ec6b07a8f9e9173e6845197929540936b, Release)
Lake version 5.0.0-src+11acb17 (Lean version 4.35.0-rc2)
elan 4.2.4 (227caca13 2026-08-25)
```

The resolved manifest confirms TreeStack at `f4112f...` and inherited
Mathlib at `065356...`.

## Important incomplete item

Do **not** yet say that the scalar path recurrence is formally the TreeStack
path recurrence.

Session 10 did not prove the general theorem equating the iterated scalar scan
with `TreeStack.OrientedBranch.branchMessage` on oriented path prefixes.

Therefore:

- A2 is partial;
- A3 is local/scalar only;
- A7 has only the two-step sanity theorem, not the general closed form.

## Next dependency order

1. prove the scalar-scan / `branchMessage` prefix equivalence;
2. lift EMPTY persistence/activation to actual path branches;
3. prove the general finite low-phase closed form;
4. prove the message-versus-prefix/suffix-mass bound;
5. then formalise irreversible fronts and the remaining deterministic
   regeneration/front layer.

Do not start probability or binary partitions before this path-message bridge
is secure.

## Frozen target

**YES — the frozen Session 8 headline theorem remains the correct
formalisation target.**

No zero-offset assertion, critical-window law, Poisson process, finite-`n`
monotonicity statement, or arbitrary-tree extension was added.

The headline theorem is not yet formally verified.
