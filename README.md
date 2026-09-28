# ProbStack — Random Stacking on Trees

**Status: frozen path theorem with complete mathematical proof; formalisation / reproducibility closure in progress.**

ProbStack studies random pebble configurations on deterministic trees.  The
first target is the path sequence \(P_n\).  This repository is intentionally
independent of TreeStack: it has its own Git history, tests, experiments, notes,
and future proof development.  TreeStack is used only as the authoritative
source of the deterministic structural theorem described below.

No novelty, priority, publication, formal-verification, or Palomar claim is
made here.  Numerical evidence is recorded as evidence, not as proof.

Session 18 closes the global conditioning-transfer step: the stabilized local
product-law excursion rate is now connected rigorously to the fixed-total
weak-composition path theorem.  The global asymptotic proof remains paper
mathematics; the Lean development records the exact finite deterministic and
probability interfaces without `sorry` or new axioms.

## Random model

For a graph \(G\) with \(n\) vertices and an integer \(t\ge 0\), let
\(\mathcal D_{G,t}\) be the uniform distribution on all configurations
\(C:V(G)\to\mathbb Z_{\ge0}\) with total mass \(t\).  Thus

\[
|\mathcal D_{G,t}|=\binom{n+t-1}{t}.
\]

For a tree \(T\),

\[
p_T(t)=\Pr_{C\sim\mathcal D_{T,t}}[C\text{ is stackable}].
\]

This is the standard **uniform multiset / weak-composition model**, not the
multinomial model obtained by independently placing labeled pebbles.

The probability profile must not be assumed monotone.  Already on \(P_2\),
\(p(1)=1\), \(p(2)=2/3\), and \(p(3)=1\).  The project therefore studies a
possible high-density *recovery regime* without assuming in advance that a
standard threshold theorem is the right final statement.

## Deterministic TreeStack boundary

The structural evaluator in `prob_stack/tree_score.py` reimplements the exact
TreeStack definitions inspected at

`jfairfaxball-348/TreeStack-Structural-Certificates-for-Stacking-on-Trees`
`main` commit `f4112f08d42a37c0941bf469ac124621b1f54f22`.

The authoritative formal sources at that revision are
`TreeStack/Transfer.lean`, `TreeStack/Message.lean`, and
`TreeStack/RootScore.lean`.  TreeStack proves, for a finite tree and proposed
root \(r\),

\[
\operatorname{StackableAt}(T,C,r)\iff 0<S_r(C).
\]

ProbStack does **not** silently modify those definitions.  In particular, an
empty branch is a categorical state distinct from integer message zero, and
the transfer function is the exact five-case integer map from TreeStack.

## Independent validation strategy

Two conceptually independent decision procedures are maintained:

1. `prob_stack/reachability.py` performs exhaustive forward search using only
   legal pebbling moves.  It knows nothing about TreeStack messages.
2. `prob_stack/tree_score.py` computes TreeStack branch messages and rooted
   scores.  It does not call the reachability solver.

`python scripts/validate_small.py --max-order 5 --max-total 5` currently
checks every labeled tree through order 5 and every weak composition through
mass 5, comparing both the global and every rooted decision.  Any disagreement
is treated as a blocking error.

## Elementary checks already established

For every nonempty tree, \(p_T(1)=1\).  For every tree on \(n\) vertices,
exactly the \(n\) configurations with both pebbles on one vertex are stackable
at total mass two, so

\[
p_T(2)=\frac{n}{\binom{n+1}{2}}=\frac{2}{n+1}.
\]

Coordinatewise stackability is not upward closed: on \(P_2\), `(1, 0)` is
already stacked while `(1, 1)` has no legal move and is not stackable.

## Current experimental baseline

The committed exact-atlas generator defaults to
\(2\le n\le9\) and \(0\le t\le12\).  The range was chosen after timing larger
rectangles rather than hard-coded in advance.  Exact rows contain integer
counts and rational probabilities; floating point is presentation only.

The first atlas shows a low-density spike at \(t=1\), a non-stackable trough,
and then recovery for the path orders visible in the rectangle.  It also finds
an additional aggregate nonmonotonicity on \(P_3\): the exact probability drops
from \(19/21\) at \(t=5\) to \(25/28\) at \(t=6\) before reaching 1 at \(t=7\).
These are finite facts, not asymptotic claims.

A subsequent Monte Carlo orientation experiment, performed only after the
exact/direct validation above, suggests that the high-density path recovery is
better normalized by a mixed scale near \(n\log n\) than by a fixed multiple
of \(n\).  That observation is currently a **candidate mechanism, not a
settled theorem or promoted asymptotic formula**; see `notes/conjectures.md`.

## Reproduce

Python 3.11+ is supported; the current development run used Python 3.13.
Runtime dependencies are empty and pytest is the only test extra.

```bash
python -m pip install -e '.[test]'
pytest
python scripts/validate_small.py --max-order 5 --max-total 5
python scripts/enumerate_paths.py --min-n 2 --max-n 9 --max-t 12
python scripts/scan_probability_profile.py data/path_exact_atlas.csv
python scripts/compare_path_scalings.py
python scripts/analyze_product_excursion.py
python scripts/tabulate_product_excursion_bounds.py
python scripts/compare_conditioned_product_local.py
```

All stochastic scripts accept explicit seeds.  Generated numerical datasets
carry sidecar metadata with the generating command and Git revision.  The
machine-readable experiment ledger is `data/experiment_log.jsonl`.

## Research discipline and scope

The path theorem is now frozen at the intended fixed-offset precision. The
current stage is **formalisation and complete verification**. The project
should not reopen the theorem merely for a finer critical window, zero-offset
law, finite-n monotonicity, Poisson front process, or arbitrary-tree extension.

Session 9 records the formal dependency architecture in
`notes/session-9-formalisation-design.md`. The immediate implementation task
is to configure the exact pinned Lean/TreeStack/Mathlib boundary and compile
the deterministic path-message scaffold. A comprehensive public-record
prior-art/originality audit and standalone paper come only after complete
formal verification. See `docs/ROADMAP.md`.

## Session 7 theorem status

The path programme now has a linear-order theorem for the one-sided
deep-deficit probability.  If `L=ceil(log_2 mu)`,
`theta=mu/2^L`, and `m in [mu,2mu]`, then

```
-log2 q_mu(m)
= L^2 + 2 L log2 L
  + [2 log2(theta) - 2 log2(3e)] L + o(L).
```

Thus there is no universal linear coefficient in the ceiling variable `L`;
the coefficient depends on dyadic phase.  Rewriting with `x=log_2 mu`
removes that phase at linear order:

```
-log2 q_mu(m)
= x^2 + 2 x log2 x - 2 log2(3e) x + o(x).
```

The global bounded-offset regime is narrowed but not closed.  The refined
deep-message upper cover proves stackability above

```
sqrt(log2 n) - 0.5 log2 log2 n + log2(3e)
```

by any fixed positive offset.  The best current state-independent certified
front proves nonstackability below

```
sqrt(log2 n) - 0.5 log2 log2 n + log2(e sqrt(3))
```

by any fixed negative offset.  The remaining rigorous gap is
`0.5 log2(3)` in `log_2 mu`.

See `notes/session-7-linear-order.md`.  The new exact diagnostic table is
reproduced by:

```bash
python scripts/tabulate_linear_order.py \
  --levels 6,8,10,12 \
  --phase-numerators 9,12,14,16 \
  --phase-denominator 16 \
  --entry-step-offset 0 \
  --output data/linear_order_entry_counts.csv
```

No Monte Carlo was used for Session 7.  The targeted Session 7 test file
passes 8 tests locally; this is not a claim of a post-Session-7 full-suite run.


## Session 8 decision — the O(1)-refined path theorem is frozen

Session 8 closes the remaining spatial constant gap. After the Session 4 reset,
every output M<=-mu is already a deep seed. For every remaining output
-mu<M<=2mu, one fresh geometric occupancy in the exact interval

2mu+2-M <= X <= 4mu-M

sends the exact TreeStack message into [mu,2mu]. The worst conditional
probability is bounded below by the positive absolute constant 8/(17e^3) for
mu>=16, so this regeneration step has no linear-in-L exponent cost.

Consequently the spatial lower certificate inherits the sharp Session 7 local
linear coefficient. The lower and upper global centers now coincide at

sqrt(log_2 n)
- (1/2) log_2 log_2 n
+ log_2(3e).

For every fixed epsilon>0, integer means eventually below this center by
epsilon give nonstackability with probability tending to one, while means
eventually above it by epsilon give stackability with probability tending to
one. No assertion is made at zero offset.

This theorem is now frozen. The project should move next to formalisation
design rather than finer asymptotics.
