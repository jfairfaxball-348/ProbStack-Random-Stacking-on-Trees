# Session 7: linear-order local theorem and refined recovery center

Status: proved mathematics, with exact integer validation of the new positive-phase
reverse recurrence.  This note sharpens Session 6 from an unspecified `O(L)`
term to an explicit linear term.  Globally it sharpens both sides to explicit
O(1) centers but leaves a bounded constant gap; it does **not** identify a
limiting critical-window law.

Throughout, `X` is geometric on `{0,1,...}` with integer mean `mu`,

`P(X=x)=p r^x`,  `p=1/(mu+1)`,  `r=mu/(mu+1)`,

and

`L=ceil(log_2 mu)`,  `theta=mu/2^L in (1/2,1]`.

The TreeStack transfer is unchanged and `EMPTY` remains categorical.

## 1. Binary-partition sharpening of the dyadic simplex

For

`N_{k,B}=#{x>=0: sum_{j=0}^{k-1} 2^j x_j <= B}`,

let `A(B)` be the same count with all powers of two allowed.  If `B/2^k`
is bounded, then

`N_{k,B} <= A(B) <= C N_{k,B}`

for a constant `C` depending only on that bound.  Indeed, an unrestricted
partition splits uniquely into its parts below `2^k` and a vector of omitted
parts `2^k,2^(k+1),...`; only boundedly many omitted vectors are possible when
`B/2^k=O(1)`.

The unrestricted cumulative count is the classical binary-partition sequence

`A(B)=p_bin(2B)`.

The exact recurrence is the A000123 recurrence

`A(0)=1`,  `A(B)=A(B-1)+A(floor(B/2))`.

De Bruijn's 1948 asymptotic for binary partitions gives, uniformly for
`lambda` in any fixed compact subset of `(0,infinity)`,

`log_2 A(lambda 2^L+O(1))`

`= L^2/2 - L log_2 L`

`  + [log_2 lambda + 1/2 + log_2 e] L`

`  + O((log L)^2)`.

Consequently, whenever `k=L+s` with fixed integer `s` and
`B=lambda 2^L+O(1)` with `B/2^k=O(1)`, the geometric dyadic-simplex probability
has linear coefficient

`gamma(theta;s,lambda)`

`= s + log_2 theta - log_2 lambda - 1/2 - log_2 e`,                 (1)

meaning

`-log_2 P(E_{k,B})`

`= L^2/2 + L log_2 L + gamma(theta;s,lambda)L + o(L)`.

For fixed `s`, the atom factor `r^(sum X_j)` changes the logarithm by only
`O_s(1)`, because `B=O_s(mu)`.

This is the first place where the Session 6 `O(L)` becomes explicit.

## 2. Exact reverse-slack encoding of the positive phase

For a positive-phase update, write

`2 M_j = M_{j-1}+X_j-3 epsilon_j`,

where `epsilon_j` is `1` exactly when the effective value is odd.
Reversing gives

`M_{j-1}=2M_j-X_j+3 epsilon_j`.

Fix a terminal state `a in {0,1}`.  The maximal predecessor obtained by taking
`epsilon=1` and `X=0` at every reverse step is

`U_k(a)=(a+3)2^k-3`.

Define the reverse slack

`y_j=3-3 epsilon_j+X_j`.

Then `y_j>=0`, and

- `y=0,1,2` has one representation;
- every `y>=3` has two representations.

Moreover a length-`k` positive segment from starting message `m` to terminal
`a` satisfies the exact global identity

`sum_{j=1}^k 2^(j-1)y_j = U_k(a)-m`.                              (2)

The one-coordinate slack generating function is therefore

`1+z+z^2+2z^3+2z^4+... = (1+z^3)/(1-z)`.

Across dyadic weights,

`prod_{j=0}^{d-1} (1+z^(3*2^j))/(1-z^(2^j))`

`= (1-z^(3*2^d))/(1-z^3) * prod_{j=0}^{d-1}(1-z^(2^j))^(-1)`.     (3)

Thus the parity numerator telescopes exactly.  There is no separate unknown
linear parity constant.

If `b_d(n)` counts binary partitions of `n` using parts below `2^d`, then the
coefficient of (3) at `B` is exactly

`C_d(B)=sum_{q=0}^{2^d-1} b_d(B-3q)`.                            (4)

This is one residue class modulo three in the top interval of width
`3*2^d`.  Adding at most two unit parts compares the residue-class sum with
the whole interval up to a constant multiplicity.  De Bruijn's expansion then
shows, whenever `B/2^d` is a fixed constant larger than three,

`log_2 C_d(B)=log_2 N_{d,B}+o(L)`.                               (5)

### Positivity of the reverse path

The only remaining issue in (2) is that every intermediate predecessor must
stay at least `2`.  A reverse suffix of length `r` has maximal message
`U_r(a)`; if it violates positivity, its local slack is at least
`U_r(a)-1`.  Comparing that suffix contribution with the total slack in (2)
shows that, for `k=L+s`, a violation is possible only in the first `s+2`
reverse steps.  Therefore fixing the last `s+2` forward slacks to zero makes
all intermediate messages positive.  The remaining number of active dyadic
levels is exactly `L-2`.

For fixed `s`, this restriction only removes finitely many top dyadic levels,
so (5) still gives the full linear coefficient.

## 3. Terminal-specific positive-entry theorem

Let `P^+_a(mu,m)` be the probability that a chain started at
`m in [mu,2mu]` first enters `{0,1}` at terminal state `a`, within `4L` steps,
while all preceding messages on that positive segment are at least `2`.
Then, uniformly in `m`,

`-log_2 P^+_a(mu,m)`

`= L^2/2 + L log_2 L + gamma^+_a(theta)L + o(L)`,                 (6)

where

`gamma^+_a(theta)`

`= log_2 theta - log_2(a+3) - 1/2 - log_2 e`.                    (7)

**Upper bound.**  Session 6 already implies that the last `d=L-2` positive
updates before entry form a necessary simplex.  Keeping the terminal value
rather than discarding it sharpens its budget to

`sum 2^(j-1) X_j <= (a+3)2^d-5`.

In (1), `s=-2` and `lambda=(a+3)/4`, which gives (7).  There are only `O(L)`
possible entry times.

**Lower bound.**  Fix an integer delay `s>=0` and put `k=L+s`.  Use (2), set
the last `s+2` slacks to zero, and count the remaining colored slack vectors
by (3)-(5).  The budget is

`B=(a+3)2^(L+s)-3-m`

`=[(a+3)2^s-m/2^L]2^L+O(1)`.

The resulting coefficient is

`s+log_2 theta-log_2((a+3)2^s-m/2^L)-1/2-log_2 e`.

Letting the fixed `s` tend to infinity after the `L -> infinity` estimate
converges uniformly in `m/2^L in [theta,2theta]` to (7).  For fixed `s`, the
geometric weighting differs from the unweighted colored count by only
`O_s(1)` in the logarithm.

## 4. Terminal-specific low-phase theorem

Let `P^-_a(mu)` be the probability that, starting from `a in {0,1}`, the chain
stays in the low phase up to its first hit of `M<=-mu`.  Then

`-log_2 P^-_a(mu)`

`= L^2/2 + L log_2 L + gamma^-_a(theta)L + o(L)`,                 (8)

where

`gamma^-_a(theta)`

`= log_2 theta - log_2(3-a) + 1/2 - log_2 e`.                    (9)

**Upper bound.**  Any successful low run has at least `L-2` initial updates.
Writing `Z=3-M`, its first `d=L-2` occupancies satisfy the exact necessary
reversed simplex

`sum 2^(d-j)X_j <= (3-a)2^(d-1)-2`.

Equation (1) with `s=-2` and `lambda=(3-a)/8` gives (9).

**Lower bound.**  Fix `s`, take `k=L+s`, and set the first `s+2` occupancies
to zero.  On the remaining `L-2` coordinates impose the final reversed
simplex

`sum 2^(k-j)X_j`

`<= (3-a)2^(k-1)-ceil((mu+3)/2)`.

The first `s+2` zero updates are low.  Afterwards the final normalized deficit
lower bound is already larger than every remaining low-phase threshold, so the
whole block stays low and finishes at `M<=-mu`.  Its fixed-`s` coefficient is

`s+log_2 theta`

`-log_2((3-a)2^(s-1)-theta/2)`

`-1/2-log_2 e`.

Letting fixed `s -> infinity` gives (9).

The same linear coefficient holds if the target is `-c mu+O(1)` for any fixed
`c>0`; the target changes only the vanishing-in-`s` part of the sufficient
budget and does not affect the necessary first `L-2` low steps.

## 5. Full one-sided linear theorem

Return to

`q_mu(m)=P_m[min_{1<=j<=4L} M_j <= -mu]`.

For any hit, take the first entry `b in {0,1}` into the low set and let
`a in {0,1}` be the last nonnegative message before the final low run.  The
terminal-specific positive-entry block and the terminal-specific low block are
disjoint.

The four linear costs are obtained by adding (7) and (9).  If `b=1` and
`a=0`, the middle segment must contain an update whose output is exactly zero.
Since `F(y)=0` only for `y=3`, that bridge coordinate has one prescribed
geometric occupancy and costs an additional

`-log_2 p = L+log_2 theta+o(1)`

at linear order.  Polynomially many possible bridge locations do not alter the
linear term.

The competing coefficients are therefore:

- `b=a=0`: `2 log_2 theta - log_2 9 - 2 log_2 e`;
- `b=a=1`: `2 log_2 theta - log_2 8 - 2 log_2 e`;
- `b=0,a=1`: `2 log_2 theta - log_2 6 - 2 log_2 e`;
- `b=1,a=0`: after the exact-atom bridge penalty, again no smaller than the
  `log_2 6` coefficient.

The `0 -> 0` route is uniquely cheapest at linear order.  A matching lower
event is obtained by concatenating the positive-entry lower construction with
terminal zero and the low-phase lower construction starting from zero.  Its
total length is `2L+O_s(1)<4L` for fixed delays.

Hence the Session 7 local theorem is:

**Linear-order one-sided theorem.**  Uniformly for integer
`m in [mu,2mu]`,

`-log_2 q_mu(m)`

`= L^2 + 2L log_2 L + beta(theta)L + o(L)`,                       (10)

with

`beta(theta)=2 log_2 theta - 2 log_2(3e)`.                        (11)

A universal beta in the ceiling variable `L=ceil(log_2 mu)` therefore does
**not** exist over arbitrary integer means.  The dependence is the explicit
dyadic phase `theta=mu/2^L`.

Along powers of two, `theta=1` and

`beta(1)=-2 log_2(3e) = -6.0553150832...`.

## 6. Phase cancellation in the natural mean variable

Put

`x=log_2 mu=L+log_2 theta`.

Substituting (11) into (10) cancels the phase at linear order:

`-log_2 q_mu(m)`

`= x^2 + 2x log_2 x - 2 log_2(3e) x + o(x)`.                      (12)

Thus the dyadic oscillation is real in the artificial ceiling coordinate `L`
but disappears from the linear term in the natural coordinate `log_2 mu`.
The bounded periodic term in de Bruijn's expansion is only `O(1)` locally and
therefore can shift the global center by at most `O(1/sqrt(log n))` at this
precision.

## 7. Global translation: a rigorous bounded gap remains

The local theorem has the phase-free natural-variable rate

`R_q(x)=x^2+2x log_2 x-2 log_2(3e)x+o(x)`,

where `x=log_2 mu`.  If one balances the local hazard against `n`, its nominal
center is

`b_n^+=sqrt(log_2 n)-log_2 sqrt(log_2 n)+log_2(3e)`.              (13)

The Session 5 deep-message **upper** cover can be sharpened to this same linear
rate.  Split the positive-entry and final-low blocks by their terminal/start
states `0` and `1`.  The target `-(2mu-1)` changes no low-phase linear
coefficient, and the `0 -> 0` route is again the largest-probability interior
route.  The bounded middle cluster contributes only `o(L)` to the logarithm;
the physical-boundary term still has no factor `n`.  Session 6 local
conditioning remains `exp(o(1))`.

Consequently the following one-sided global refinement is rigorous:

**Refined supercritical theorem.**  If

`liminf [log_2 mu_n-b_n^+] > 0`,

then a uniformly random weak composition of total `n mu_n` on `P_n` is
stackable with probability tending to one.

The subcritical spatial certificate needs an extra state-independent step that
the local theorem itself does not provide.  Session 4/6 reset blocks guarantee
only an outgoing message `M<=2mu`; they do not guarantee
`M in [mu,2mu]`.  Therefore the optimal local coefficient (10) cannot simply
be inserted into the old certified-front proof.

A sharpened **state-independent** descent is nevertheless available.  For any
fixed `s>=2`, take `k=L+s` and impose

`sum_{j=1}^k 2^(j-1)X_j <= 2^k-2mu-1`.                           (14)

The global inequality `F(y)<=y/2` forces the output to be at most zero for
every incoming integer message `M<=2mu`.  Formula (1), followed by fixed
`s -> infinity`, gives descent coefficient

`gamma_rob(theta)=log_2 theta-1/2-log_2 e`.                       (15)

From any output `M<=0`, the sharp terminal-zero low-phase lower event from
Section 4 is still valid, since a larger initial deficit only helps.  Hence a
state-independent two-block deep witness has rate

`-log_2 w_mu`

`=L^2+2L log_2 L`

` + [2 log_2 theta-log_2 3-2 log_2 e]L+o(L)`.                    (16)

In `x=log_2 mu` this is

`R_cert(x)=x^2+2x log_2 x-(log_2 3+2 log_2 e)x+o(x)`.             (17)

The reset and runaway pieces of the Session 6 true-front certificate have
constant probability and do not change this linear term.  Its local mass and
length remain within the Session 6 conditioning regime, so the conditioned
second-moment proof applies unchanged.  Thus, with

`b_n^-=sqrt(log_2 n)-log_2 sqrt(log_2 n)+log_2(e sqrt(3))`,       (18)

we obtain:

**Refined certified subcritical theorem.**  If

`limsup [log_2 mu_n-b_n^-] < 0`,

then a uniformly random weak composition of total `n mu_n` on `P_n` is
nonstackable with probability tending to one.

The two rigorous centers differ by

`b_n^+-b_n^-= (1/2) log_2 3 = 0.792481...`.                      (19)

Thus Session 7 resolves the local linear term completely and narrows the
global bounded-offset uncertainty to an explicit constant gap, but it does
**not** yet prove that the actual global recovery center is (13).  Closing
(19) requires a spatial regeneration/reset argument that reaches the
`[mu,2mu]` starting window without paying an additional linear cost, or an
equally sharp state-independent front certificate.

## 8. Conditioning precision

No stronger equivalence-of-ensembles estimate is needed for the two global
one-sided refinements above.  Session 6 gives multiplicative `exp(o(1))`
conditioning error for one- and two-block events with `O(L^2)` coordinates and
`O(mu L^2)` capped mass.  The new linear terms are of size `Theta(L)`, so an
`o(1)` logarithmic conditioning error is far smaller than the precision
required here.

A limiting law inside any eventual smaller critical window would require finer
local remainders and may require finer conditioning as well.

## 9. Exact computation and validation

No Monte Carlo was used.

New exact code includes:

- the A000123 cumulative binary-partition recurrence;
- exact finite dyadic-simplex counts;
- an exact reverse positive-entry dynamic programme using suffix sums;
- the exact colored-slack coefficient formula from the telescoping product;
- executable local coefficients, the state-independent certificate coefficient,
  and both global center constants.

Targeted Session 7 tests verify:

- the unrestricted dyadic-simplex / binary-partition identity on small budgets;
- the reverse positive-entry DP against brute-force occupancy enumeration;
- the colored-slack generating function against direct colored enumeration;
- the four terminal-route coefficient comparisons;
- cancellation of dyadic phase after changing from `L` to `log_2 mu`;
- the two global center constants and their exact half-log-three gap;
- the state-independent certificate coefficient;
- the terminal-specific necessary budgets.

The targeted Session 7 test file passed `8` tests locally.  This is not a
claim that the repository's full pytest suite was run in the Session 7 harness.
The last literal full-suite result remains the Session 5 result recorded in the
repository unless a later CI/full run succeeds.

The exact table `data/linear_order_entry_counts.csv` records positive-entry
integer counts and a finite colored-slack lower subset for selected levels and
dyadic phases.  Those counts validate the reverse recurrence and the exact
generating identity; they are not a regression and are not used to infer
(10).

## 10. Literature actually searched/read

The literature search was deliberately narrow and tied to the needed lattice
asymptotic.

- N. G. de Bruijn, *On Mahler's partition problem*, Indagationes Mathematicae
  10 (1948), 210-220.  The bibliographic record and the explicit asymptotic
  formula were located through the modern A000123 index.  Direct retrieval of
  the historical PDF from the academy host was blocked by HTTP 403 in this
  session, so no claim is made to having inspected that scan directly.
- OEIS A000123 was read for the exact cumulative recurrence, generating
  function, identification with binary partitions of `2n`, and its quotation
  of de Bruijn's asymptotic.
- Search results also identified V. Protasov, *On the Asymptotics of the Binary
  Partition Function*, Mathematical Notes 76 (2004), 144-149.  It was not
  needed for the proof and no result from it is used here.

No novelty or priority claim is made.

## 11. What remains open

Session 7 determines the full linear local term, proves that a universal beta
in the ceiling variable does not exist, and gives a phase-free coefficient in
`x=log_2 mu`.  Globally it proves the refined supercritical center (13) and the
refined certified subcritical center (18), leaving the explicit constant gap
(19).

The single best next target is therefore **spatial, not local**: close the
`(1/2)log_2 3` gap by constructing a constant-cost regeneration from the
Session 4 reset output into the `[mu,2mu]` local starting window, or by finding
a state-independent deep-front witness with the same linear coefficient as
`q_mu`.  Only after that should the first sublinear local correction and a
limiting critical-window law be attacked.
