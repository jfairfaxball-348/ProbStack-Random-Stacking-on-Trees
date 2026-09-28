# Session 15 handover

## Repository boundary

Session 15 starts from validated `main`

`524b8ea3876db97009349971c4bf32b14a899ca2`.

The authoritative TreeStack dependency remains

`f4112f08d42a37c0941bf469ac124621b1f54f22`,

with Mathlib

`065356127b1dc0016f66b7283ce0ce2c4055aa55`

and Lean

`leanprover/lean4:v4.35.0-rc2`.

The final Session-15 `main` SHA and successful Actions run are recorded in the
end-of-session report, since they are properties of the commit containing this
handover rather than inputs to it.

## Finite combinatorics recovered and frozen

For

`N_{k,B}=#{x in Z_{>=0}^k : sum_{j=0}^{k-1}2^j x_j<=B}`,

Session 15 fixes the exact coefficient identity

`N_{k,B}=[z^(2B)] prod_{j=0}^k (1-z^(2^j))^(-1)`.

Thus the relevant object is a truncated binary-partition coefficient: binary
partitions of `2B` using parts at most `2^k`. Only when `2^k>B` may it be
identified with the unrestricted count `p_bin(2B)`.

The finite recurrence is

`N_{k,B}=sum_{q=0}^{floor(B/2^(k-1))} N_{k-1,B-q2^(k-1)}`

for `k>=1`, with `N_{0,B}=1` for `B>=0`.

For the unrestricted cumulative count `A(B)=p_bin(2B)`, the exact recurrence is

`A(0)=1`,
`A(B)=A(B-1)+A(floor(B/2))`.

Zeros are allowed in every coordinate. Coordinates are ordered. Reversing
weights preserves counts only via coordinate reversal; it does not preserve a
fixed-vector predicate.

## Exact relation to Session 14 positive descent

For a block of length `k`,

`PositiveDescentEvent mu xs`

is exactly

`affineInputCost xs <= 2^k-2mu-1`.

The `-1` is mandatory because the original condition is strict.

The historical sharp Session-6 descent uses

`k=L+2`, `B=2^(L+2)-2mu-1`,

where `L=ceil(log_2 mu)`.

It is not the Session-14 rectangular cap witness, whose descent support is
`L+4`. The canonical cap witness remains preserved for the deterministic
front interface.

At `mu=16`, the sharp simplex descent has support `6`, budget `31`; the
canonical cap descent has support `8`.

## Low-phase finite identity

For the Session-14 recursion

`D_next=2(D-x)`,

a length-`k` block has exact final deficit

`D_k=2^k D_0-2 sum_{j=1}^k 2^(k-j)x_j`.

The sufficient low-phase simplex is

`sum_{j=1}^k 2^(k-j)x_j <= (D_0-2)2^(k-1)`.

It implies the recursive `LowBudget` constraints and the final bound

`D_k>=2^(k+1)`.

For `D_0=3`, this is exactly the Session-6 reversed simplex with budget
`2^(k-1)`. Taking `k=L` gives the historical amplification block.

At `mu=16`, the sharp amplification block has support `4`, budget `8`; the
canonical Session-14 amplification caps remain `(0,1,2,4)`.

## Exact product mass

If

`N_{k,B}(s)=#{x in E_{k,B}: sum x_j=s}`,

then under the geometric law with

`p=1/(1+mu)`, `r=mu/(1+mu)`,

the exact finite simplex probability is

`p^k sum_s N_{k,B}(s) r^s`.

The sharp Session-6 finite seed is the independent concatenation of the
`L+2` positive simplex and the `L` reversed-low simplex, so its support is
exactly `2L+2` and its product probability is the product of these two exact
finite sums.

## Session-7 colored slack

The reverse positive-phase slack has multiplicity one for `0,1,2` and two for
all values at least three. Its finite generating function telescopes exactly:

`prod_{j<d}(1+z^(3*2^j))/(1-z^(2^j))`

`=(1-z^(3*2^d))/(1-z^3) prod_{j<d}(1-z^(2^j))^(-1)`.

Hence if `b_d(n)` counts binary partitions of exact mass `n` using parts below
`2^d`, then

`C_d(B)=sum_{q=0}^{2^d-1} b_d(B-3q)`.

This is an exact finite coefficient identity; no parity constant is hidden.

## Code and formalisation

Session 15 adds:

- `ProbStack/FiniteDyadic.lean`;
- `prob_stack/finite_dyadic.py`;
- `tests/test_finite_dyadic.py`;
- `notes/session-15-finite-dyadic.md`;
- this handover note;
- an import of `ProbStack.FiniteDyadic` from `ProbStack.lean`.

Lean formalises a forward natural dyadic cost for positive descent, reuses the pre-existing reversed `dyadicInputCost` from `ProbStack.Deficit`, proves the exact strict positive-descent budget, the binary-partition multiplicity-vector encoding and converse, the recursive low-deficit closed form, and the final-deficit inequality for the reversed simplex.

The standalone exact Python harness passes 11 tests, including exhaustive
small checks of the binary-partition coefficient, strict boundary, ordinary
mass refinement, low-budget recursion, reversed weights, ordered-coordinate
conventions, colored slack, and the negative `-L log_2 L` direction.

A full `Fintype.card` proof of the coefficient identity is intentionally not
added: the multiplicity-vector bijection is formalised, and a cardinality layer
can be added later if a downstream theorem actually needs it.

The full event-level weak-composition conditioning formula also remains a
secondary Lean gap. Session 14's exact finite conditioned count in Python and
its matched-geometric algebra in Lean remain unchanged.

## Scope confirmation

Session 15 does not start the isolated binary-partition asymptotic, does not
start conditioned global asymptotics, does not alter the frozen headline
path theorem, does not touch the path recursion or front construction, does
not change EMPTY semantics, and does not change any dependency pin.

No novelty or priority claim is made.

## Recommended Session 16 target

Start the isolated binary-partition asymptotic from the exact truncated
coefficient

`[z^(2B)] prod_{j=0}^k(1-z^(2^j))^(-1)`

with `k=L+O(1)` and `B=lambda 2^L+O(1)`. Prove carefully when truncation can
be replaced by the unrestricted binary-partition count, then recover the
finite-to-asymptotic expansion with the forced sign

`-L log_2 L`.

Only after that isolated asymptotic is stable should it be inserted into the
positive-descent and low-phase product-mass formulas.
