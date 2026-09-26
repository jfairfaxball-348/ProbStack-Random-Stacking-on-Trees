# Session 7 handover

## Repository boundary

Session 7 started from ProbStack commit

`6baa6c03827ea634893eb6ce7821230d7f7477e6`.

The authoritative TreeStack dependency remains

`f4112f08d42a37c0941bf469ac124621b1f54f22`.

Do not alter the exact criterion

`StackableAt(T,C,r) iff 0 < S_r(C)`

or identify `EMPTY` with integer zero.

This handover is the final planned Session 7 repository write.  Its commit SHA
is the Session 7 HEAD unless a later corrective commit is explicitly recorded.

## Main local theorem

For iid geometric occupancies of integer mean `mu`, write

`L=ceil(log_2 mu)`, `theta=mu/2^L in (1/2,1]`,

and for `m in [mu,2mu]`

`q_mu(m)=P_m[min_{1<=j<=4L} M_j <= -mu]`.

Session 7 proves, uniformly in that starting window,

`-log_2 q_mu(m)`

`=L^2+2L log_2 L`

` +[2 log_2 theta-2 log_2(3e)]L+o(L)`.

Therefore a single universal coefficient `beta` in the ceiling variable
`L` does not exist over arbitrary integer means.  The exact phase-dependent
coefficient is

`beta(theta)=2 log_2 theta-2 log_2(3e)`.

Along powers of two,

`beta(1)=-2 log_2(3e)=-6.0553150832...`.

In the natural variable `x=log_2 mu`, the phase cancels at linear order:

`-log_2 q_mu(m)`

`=x^2+2x log_2 x-2 log_2(3e)x+o(x)`.

## Separate phase contributions

For terminal/start state `a in {0,1}`, the positive-entry and low-run linear
coefficients are

`gamma^+_a(theta)
 =log_2 theta-log_2(a+3)-1/2-log_2 e`,

`gamma^-_a(theta)
 =log_2 theta-log_2(3-a)+1/2-log_2 e`.

The cheapest complete route is terminal zero followed immediately by a final
low run starting from zero.  The other terminal combinations have strictly
larger linear cost.  A route from entry state 1 to final-low start state 0
must additionally contain an exact output-zero bridge and therefore pays at
least one extra geometric atom at linear order.

## Binary-partition and parity mechanism

For the dyadic simplex count

`N_{k,B}=#{x>=0: sum_{j<k}2^j x_j<=B}`,

truncation at `k=L+O(1)` differs only by a bounded factor from the cumulative
binary-partition count when `B/2^k=O(1)`.  De Bruijn's binary-partition
asymptotic gives, for `B=lambda 2^L+O(1)`,

`log_2 N_{k,B}`

`=L^2/2-L log_2 L`

` +[log_2 lambda+1/2+log_2 e]L+o(L)`.

The positive TreeStack parity term is handled exactly in reverse.  The reverse
slack `y` has multiplicity one for `y=0,1,2` and two for `y>=3`, hence
one-coordinate generating factor

`(1+z^3)/(1-z)`.

Across dyadic weights the numerator telescopes:

`prod_{j<d}(1+z^(3*2^j))/(1-z^(2^j))`

`=(1-z^(3*2^d))/(1-z^3)
  prod_{j<d}(1-z^(2^j))^(-1)`.

Thus parity creates no additional unknown linear constant.

## Global translation

The local rate gives the refined deep-message upper-cover center

`b_n^+=sqrt(log_2 n)-0.5 log_2 log_2 n+log_2(3e)`.

Session 7 sharpens the Session 5 necessity/cover argument to show:

if

`liminf [log_2 mu_n-b_n^+] > 0`,

then the uniform weak composition of total `n mu_n` on `P_n` is stackable
with probability tending to one.

The subcritical spatial certificate cannot simply use the optimal local
start-window theorem, because the Session 4 reset guarantees only an outgoing
message `M<=2mu`, not `M in [mu,2mu]`.

Optimizing the state-independent `F(x)<=x/2` descent over a fixed extra delay
and combining it with the sharp terminal-zero low run gives certified-front
linear coefficient

`2 log_2 theta-log_2 3-2 log_2 e`.

In `x=log_2 mu`, the corresponding certified center is

`b_n^-=sqrt(log_2 n)-0.5 log_2 log_2 n+log_2(e sqrt(3))`.

Session 7 therefore also proves:

if

`limsup [log_2 mu_n-b_n^-] < 0`,

then the uniform weak composition is nonstackable with probability tending to
one.

The remaining rigorous bounded-offset gap is exactly

`b_n^+-b_n^-=(1/2)log_2 3=0.7924812503...`.

Do not claim the actual global center is `b_n^+` until this spatial gap is
closed.

## Conditioning

The Session 6 local equivalence-of-ensembles precision remains sufficient.
The relevant one- and two-block events have `O(L^2)` coordinates and
`O(mu L^2)` capped mass, with conditioned/product distortion `exp(o(1))`.
This is negligible relative to the new `Theta(L)` logarithmic terms.

## Validation

No Monte Carlo was used in Session 7.

New targeted tests validate:

- cumulative binary-partition versus unrestricted dyadic-simplex counts;
- the reverse positive-entry DP against brute-force occupancy enumeration;
- the colored-slack generating function against direct colored enumeration;
- terminal-route coefficient ordering;
- cancellation of dyadic phase in `x=log_2 mu`;
- the refined upper and certified lower global constants;
- the state-independent certificate coefficient;
- terminal-specific necessary budgets.

The literal targeted command

`PYTHONPATH=. pytest -q tests/test_linear_order.py`

passed

`8 tests`

in the Session 7 harness.

This is **not** a full repository pytest claim.  The last literal full-suite
run remains the Session 5 result:

`54 tests passed`.

The independent direct legal-move versus TreeStack structural validator remains
at the previously recorded result:

- 146 labelled trees through order 5;
- 33,711 configurations through total mass 5;
- 166,116 rooted cases;
- zero disagreements.

## Exact computation

The exact diagnostic command is

`python scripts/tabulate_linear_order.py --levels 6,8,10,12 --phase-numerators 9,12,14,16 --phase-denominator 16 --entry-step-offset 0 --output data/linear_order_entry_counts.csv`.

The table contains exact positive-entry integer counts from the reverse
suffix-sum DP and exact finite colored-slack lower-subset counts.  Floating
logs, ratios, and coefficient columns are deterministic transforms.  The table
does not estimate `beta` by regression.

## Literature actually used/searched

The proof uses the classical binary-partition asymptotic attributed to
N. G. de Bruijn, *On Mahler's partition problem*, Indagationes Mathematicae
10 (1948), 210-220, as quoted in the modern A000123 record.  The A000123
record was also used for the cumulative recurrence and generating function.
Direct retrieval of the historical academy-hosted PDF returned HTTP 403 in
this session, so it was not claimed as directly read.

Search also located V. Protasov, *On the Asymptotics of the Binary Partition
Function*, Mathematical Notes 76 (2004), 144-149.  No result from that paper
is used in Session 7.

No novelty or priority claim is made.

## Session 7 files

Principal additions:

- `prob_stack/linear_order.py`
- `tests/test_linear_order.py`
- `scripts/tabulate_linear_order.py`
- `data/linear_order_entry_counts.csv`
- `data/linear_order_entry_counts.csv.meta.json`
- `notes/session-7-linear-order.md`
- `notes/session-7-handover.md`

Updated project records include:

- `README.md`
- `notes/path-dynamics.md`
- `notes/proof-plan.md`
- `notes/conjectures.md`
- `data/README.md`
- `data/experiment_log.jsonl`

## Single best next mathematical step

Close the `(1/2)log_2 3` spatial gap.

The first attack should be a constant-cost regeneration lemma after the
Session 4 reset: either show that every non-front reset output can be brought
into the `[mu,2mu]` local start window with probability bounded below by an
absolute constant while preserving local mass control, or prove an equally
sharp state-independent deep-front witness with local coefficient
`2 log_2 theta-2 log_2(3e)`.

Do not proceed to a limiting transition law until this gap is closed.  If the
gap cannot be closed, determine the true optimal state-independent spatial
coefficient and prove that obstruction instead.
