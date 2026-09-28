# Session 16 handover

## Repository boundary

Session 16 starts from validated `main`

`734db99717d37146b078220df3fe1156d323596f`.

The authoritative TreeStack dependency remains

`f4112f08d42a37c0941bf469ac124621b1f54f22`,

with Mathlib

`065356127b1dc0016f66b7283ce0ce2c4055aa55`

and Lean

`leanprover/lean4:v4.35.0-rc2`.

The final Session 16 `main` SHA and exact successful Actions run are properties
of the merged commit and are recorded in the end-of-session report.

## Analytic theorem isolated

Let `a` be a fixed integer, let `lambda` range in a fixed compact subset of
`(0,infinity)`, and let

```text
k=L+a,
B_L=lambda 2^L+O(1).
```

Then, uniformly for a uniformly bounded additive budget shift,

```text
log_2 N_{k,B_L}
 = (1/2)L^2
   - L log_2 L
   + [log_2 lambda+1/2+log_2 e]L
   + O((log L)^2).
```

The fixed support shift `a` does not alter the linear coefficient.

The proof first compares the finite truncated count with the unrestricted
binary-partition count:

```text
N_{k,B} <= A(B)
          <= A(floor(B/2^k)) N_{k,B},
A(B)=p_bin(2B).
```

Thus a bounded `B/2^k` changes the logarithm by only `O(1)`, and the Session 15
exact cutoff `2^k>B` gives equality. The unrestricted asymptotic is then a
direct expansion of de Bruijn's 1948 binary-partition formula. The cross term
in the square forces the sign `-L log_2 L`.

The factor of two is fixed as follows: de Bruijn/A000123 is used in the form
for `p_bin(2n)`, while the Session 15 count has `A(B)=p_bin(2B)`, so the
substitution is `n=B`, not `n=2B`.

## Exact downstream specialisations

With `L=ceil(log_2 mu)` and `theta=mu/2^L`:

- sharp positive descent:
  `k=L+2`, `B=(4-2theta)2^L-1`; cutoff exact; linear count coefficient
  `log_2(4-2theta)+1/2+log_2 e`;
- sharp low amplification:
  `k=L`, `B=2^(L-1)`; cutoff exact; coefficient
  `log_2 e-1/2`;
- Session 7 necessary positive entry, terminal `a in {0,1}`:
  `k=L-2`, `B=((a+3)/4)2^L-5`; truncation factor at most `4` or `6`;
- Session 7 necessary low phase, start `a in {0,1}`:
  `k=L-2`, `B=((3-a)/8)2^L-2`; factor at most `2` for `a=0`, exact cutoff
  for `a=1`.

For colored reverse slack, if `B=c2^d+O(1)` with fixed `c>3`, the exact
Session 15 slice identity and monotonicity of the finite binary-partition
coefficients give

```text
log_2 C_d(B)=log_2 N_{d,B}+O(1).
```

So colored slack changes neither the quadratic term, the
`-L log_2 L` term, nor the linear coefficient.

## Code, tests, and formalisation

Session 16 adds:

- `prob_stack/binary_partition_asymptotics.py`;
- `tests/test_binary_partition_asymptotics.py`;
- `scripts/tabulate_binary_partition_asymptotics.py`;
- `data/session16_binary_partition_diagnostics.csv`;
- `notes/session-16-binary-partition-asymptotics.md`;
- this handover.

`ProbStack/FiniteDyadic.lean` gains the exact arithmetic cutoff lemma relating
`B<2^k` to the next omitted binary part being larger than `2B`.

The analytic de Bruijn theorem is intentionally not formalised in Lean.
Session 16 introduces no `sorry` and no new axiom.

## Scope preserved

Session 16 does not start geometric local-seed probability asymptotics,
conditioning transfer, or global path asymptotics. It does not alter the
frozen headline theorem, TreeStack/EMPTY semantics, the canonical Session 14
seed witness, or any dependency pin.

## Session 17 target

The next exact target is the local excursion/seed probability asymptotic.
Starting from the Session 15 ordinary-mass refinement

```text
P(E_{k,B})=p^k sum_s N_{k,B}(s) r^s,
```

combine the now-stable count asymptotic with rigorous control of the geometric
weight. Recover the positive-descent/low-phase local exponents and matching
upper-bound necessary-entry exponents without revisiting any global or
conditioning argument until the local calculation is complete.
