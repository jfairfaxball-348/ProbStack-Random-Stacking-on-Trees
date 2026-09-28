# Session 17: product-geometric local excursion probability

Status: local iid-product probability stage completed at the precision needed by
the frozen path theorem.  This note starts from the exact Session-15 finite
probability formula and the Session-16 binary-partition count theorem.  It does
not start conditioning transfer or global path asymptotics.

The TreeStack semantics are unchanged.  In particular `TreeStack.EMPTY = none`
is categorical and is never identified with integer zero.

## 0. Frozen-center sign check

The incoming Session-17 handover accidentally displayed the frozen center with
a plus sign in front of the half-log-log term.  That conflicts both with the
Session-7 local rate and with the authoritative repository state.  Session 8
froze, and the current README still records,

```
c_n
 = sqrt(log_2 n)
   - (1/2) log_2 log_2 n
   + log_2(3e).
```

Nothing in Session 17 changes that theorem.  The handover typo is recorded here
only so it is not propagated into Session 18.

## 1. Exact product law and the ordinary-mass bound

For

```
E_{k,B}
 = {x in Z_{>=0}^k : sum_{j=0}^{k-1} 2^j x_j <= B},
N_{k,B}=|E_{k,B}|,
```

the iid geometric law with

```
p=1/(1+mu),   r=mu/(1+mu)
```

gives exactly

```
P_mu(E_{k,B})
 = p^k sum_{x in E_{k,B}} r^{|x|_1}.                 (1.1)
```

Every dyadic weight is at least one, hence for every vector in the simplex

```
|x|_1
 <= sum_j 2^j x_j
 <= B.                                             (1.2)
```

The same statement holds after coordinate reversal.  Since `0<r<1`,

```
p^k r^B N_{k,B}
 <= P_mu(E_{k,B})
 <= p^k N_{k,B}.                                  (1.3)
```

Thus, writing `T_{k,B}` for the logarithmic tilt relative to raw counting,

```
T_{k,B}
 = log_2( sum_x r^{|x|_1} / N_{k,B} ),
```

we have the deterministic bounds

```
B log_2 r <= T_{k,B} <= 0.                    (1.4)
```

Moreover

```
0 <= -T_{k,B}
 <= B log_2(1+1/mu)
 <= B/(mu ln 2).                                   (1.5)
```

Consequently, whenever `B=O(mu)`, the entire geometric tilt contributes only
`O(1)` to the base-two logarithm.  This is uniform whenever `B/mu` is
uniformly bounded.

This proves carefully the historical Session-7 statement that the geometric
tilt is lower order.  No concentration theorem for ordinary mass is needed:
the full weighted sum is controlled pointwise.

## 2. General dyadic-simplex probability theorem

Take

```
mu = theta 2^L,
theta in (1/2,1],
k = L+s,
B = lambda 2^L + O(1),
```

where `s` is fixed and `lambda` ranges in a compact subset of
`(0,infinity)`.  Session 16 gives, uniformly on such compact ranges,

```
log_2 N_{k,B}
 = (1/2)L^2
   - L log_2 L
   + [log_2 lambda + 1/2 + log_2 e]L
   + O((log L)^2).                                     (2.1)
```

The geometric atom factor satisfies

```
-k log_2 p
 = k log_2(1+mu)
 = L^2 + [s+log_2 theta]L + O(1).                     (2.2)
```

Combining (1.5), (2.1), and (2.2) yields

```
-log_2 P_mu(E_{k,B})
 = (1/2)L^2
   + L log_2 L
   + gamma(theta;s,lambda)L
   + O((log L)^2),                                    (2.3)
```

with

```
gamma(theta;s,lambda)
 = s
   + log_2 theta
   - log_2 lambda
   - 1/2
   - log_2 e.                                         (2.4)
```

The roles of the three ingredients are therefore completely separated:

- the count contributes `-(1/2)L^2 + L log_2 L` to the negative log after
  inversion, together with `-[log_2 lambda+1/2+log_2 e]L`;
- `p^k` contributes `L^2+[s+log_2 theta]L+O(1)`;
- the factor `r^{|x|_1}` contributes only `O(1)`.

In particular the tilt changes neither the `L^2` coefficient, nor the
`L log_2 L` coefficient, nor the linear coefficient.

The estimate is uniform over all `theta in (1/2,1]` whenever the relevant
`lambda` range is compact and bounded away from zero.

## 3. Sharp Session-6 positive descent

For

```
k_+ = L+2,
B_+ = (4-2theta)2^L - 1,
```

the strict `-1` is exact.  It is only a bounded additive budget shift, so it
does not affect the displayed linear coefficient.  Formula (2.4) gives

```
gamma_sharp^+(theta)
 = 3/2
   + log_2 theta
   - log_2(4-2theta)
   - log_2 e.                                         (3.1)
```

Hence

```
-log_2 P_mu(E_{L+2,B_+})
 = (1/2)L^2
   + L log_2 L
   + gamma_sharp^+(theta)L
   + O((log L)^2).                                    (3.2)
```

This is uniform for `theta in (1/2,1]`, because
`4-2theta in [2,3)`.

## 4. Sharp Session-6 low amplification

The reversed low simplex has

```
k_- = L,
B_- = 2^(L-1) = (1/2)2^L.
```

Coordinate reversal preserves both the ordinary coordinate sum and the
product-geometric atom weight.  Thus its product probability equals that of the
forward simplex exactly.

Formula (2.4) gives

```
gamma_sharp^-(theta)
 = log_2 theta + 1/2 - log_2 e,                       (4.1)
```

and therefore

```
-log_2 P_mu(E_{L,2^(L-1)})
 = (1/2)L^2
   + L log_2 L
   + gamma_sharp^-(theta)L
   + O((log L)^2).                                    (4.2)
```

## 5. Frozen sharp two-simplex seed

The two blocks are disjoint under the product law and have total support

```
(L+2)+L = 2L+2.
```

Therefore the frozen sharp Session-6/15 seed satisfies

```
-log_2 P_seed(mu)
 = L^2
   + 2L log_2 L
   + beta_seed(theta)L
   + O((log L)^2),                                    (5.1)
```

where

```
beta_seed(theta)
 = gamma_sharp^+(theta)+gamma_sharp^-(theta)

 = 2
   + 2 log_2 theta
   - log_2(4-2theta)
   - 2 log_2 e.                                       (5.2)
```

Equivalently,

```
beta_seed(theta)
 = 1
   + 2 log_2 theta
   - log_2(2-theta)
   - 2 log_2 e.
```

This coefficient is intentionally not the optimized one-sided excursion
coefficient from Session 7.  The sharp two-simplex seed is a convenient finite
lower witness, but it is linearly more expensive than the delayed
terminal-specific construction used to obtain the true local excursion rate.

## 6. Necessary positive-entry probabilities

For terminal `a in {0,1}`, Session 7 gives exactly

```
k=L-2,
B_a^+ = (a+3)2^(L-2)-5
      = ((a+3)/4)2^L-5.
```

Formula (2.4) gives

```
gamma_a^+(theta)
 = log_2 theta
   - log_2(a+3)
   - 1/2
   - log_2 e.                                         (6.1)
```

Thus

```
-log_2 P_mu(E_a^+)
 = (1/2)L^2
   + L log_2 L
   + gamma_a^+(theta)L
   + O((log L)^2).                                    (6.2)
```

This exactly recovers the historical Session-7 coefficient.  The Session-16
bounded truncation factors 4 and 6 affect only `O(1)).

## 7. Necessary low-phase probabilities

For low-phase start `a in {0,1}`,

```
k=L-2,
B_a^- = (3-a)2^(L-3)-2
      = ((3-a)/8)2^L-2.
```

Formula (2.4) gives

```
gamma_a^-(theta)
 = log_2 theta
   - log_2(3-a)
   + 1/2
   - log_2 e.                                         (7.1)
```

Hence

```
-log_2 P_mu(E_a^-)
 = (1/2)L^2
   + L log_2 L
   + gamma_a^-(theta)L
   + O((log L)^2).                                    (7.2)
```

Again this exactly matches Session 7.  The exact cutoff for `a=1` and the
factor-two truncation comparison for `a=0` change no linear term.

## 8. Colored positive reverse slack under the product law

For a reverse positive update the slack representation is

```
y = 3-3 epsilon + X.
```

A colored slack object remembers which representation is used.  For a fixed
terminal state this determines the occupancy `X` uniquely.  If a colored
slack vector has total dyadic slack budget `B`, then its ordinary occupancy
mass is at most its ordinary slack mass, which is at most `B`.

Therefore, if `C_d(B)` is the exact Session-15 colored-slack count and the
full block has `k` geometric coordinates,

```
p^k r^B C_d(B)
 <= P_mu(colored event)
 <= p^k C_d(B).                                  (8.1)
```

Session 16 proved

```
log_2 C_d(B)=log_2 N_{d,B}+O(1)
```

in the relevant fixed-scale regime.  Equation (8.1) adds only another bounded
logarithmic error.  Thus colored slack contributes no new quadratic,
`L log L), or linear probability coefficient.  In particular the
combinatorial multiplicity two for large slack must not be confused with a
new geometric atom constant.

## 9. Optimized terminal-specific lower constructions

The necessary events above provide the upper probability bounds.  For matching
lower probability bounds, recover the Session-7 fixed-delay constructions.

### Positive entry

Fix terminal `a in {0,1}`, delay `s>=0`, and start
`m in [mu,2mu]`.  Put `u=m/2^L in [theta,2theta]` and use a positive block
of length `k=L+s`.  Fix the finitely many top reverse slacks required for
positivity and count the remaining `L-2` colored levels.  The active budget
has scale

```
lambda_{a,s}^+(u)
 = (a+3)2^s-u.
```

For each fixed `s`, this stays in a compact positive interval uniformly over
all admissible `theta` and `u`.  Sections 2 and 8 give coefficient

```
g_{a,s}^+(theta,u)
 = s + log_2 theta
   - log_2((a+3)2^s-u)
   - 1/2 - log_2 e.                                  (9.1)
```

Uniformly in `u in [theta,2theta]`,

```
g_{a,s}^+(theta,u) -> gamma_a^+(theta)
```

as fixed `s -> infinity`.

### Low phase

For low start `a in {0,1}`, use `k=L+s`, fix the first `s+2`
occupancies to zero, and impose the remaining reversed simplex from Session 7.
Its scale is

```
lambda_{a,s}^-(theta)
 = (3-a)2^(s-1)-theta/2
```

up to a bounded additive integer correction.  For fixed `s` this is uniformly
bounded away from zero, and its coefficient is

```
g_{a,s}^-(theta)
 = s + log_2 theta
   - log_2((3-a)2^(s-1)-theta/2)
   - 1/2 - log_2 e.                                  (9.2)
```

Uniformly in `theta in (1/2,1]`,

```
g_{a,s}^-(theta) -> gamma_a^-(theta)
```

as fixed `s -> infinity`.

Because Session 16 only requires fixed support offsets, this two-limit
argument proves the local theorem with an `o(L)` remainder.  Session 17 does
not claim an `O((log L)^2)` remainder for the fully optimized excursion.

## 10. Four terminal/start routes and the bridge penalty

Adding (6.1) and (7.1), the four route coefficients before any bridge penalty
are

```
b=a=0:
  2 log_2 theta - log_2 9 - 2 log_2 e;

b=a=1:
  2 log_2 theta - log_2 8 - 2 log_2 e;

b=0,a=1:
  2 log_2 theta - log_2 6 - 2 log_2 e;

b=1,a=0:
  2 log_2 theta - log_2 12 - 2 log_2 e.
```

For the route from positive-entry terminal `1` to final-low start `0`, an
intermediate update must output exactly zero.  Since the TreeStack update has
output zero only at effective input three, the occupancy at that coordinate is
prescribed once the incoming message is known.  Its probability is one
geometric atom

```
p r^x
```

with `x=O(mu)` on the relevant pre-hit range.  Therefore

```
-log_2(p r^x)
 = L + O(1).
```

The bridge adds `+1` to the coefficient of `L`, raising the
`1 -> 0` route to the same `-log_2 6` level or worse.  Polynomially many
possible bridge or entry locations contribute only `O(log L)=o(L)`.

The unique cheapest route at linear order is therefore `0 -> 0`.

## 11. Local one-sided excursion theorem

Let

```
q_mu(m)
 = P_m[min_{1<=j<=4L} M_j <= -mu],
```

with integer `m in [mu,2mu]`.  The necessary terminal decomposition gives
the upper probability bound, while the delayed `0 -> 0` construction gives
the matching lower probability bound.  Hence, uniformly in that starting
window,

```
-log_2 q_mu(m)
 = L^2
   + 2L log_2 L
   + beta(theta)L
   + o(L),                                            (11.1)
```

where

```
beta(theta)
 = 2 log_2 theta
   - 2 log_2(3e).                                     (11.2)
```

This is exactly the historical Session-7 target, now re-derived from the
Session-15 exact product-mass interface and the Session-16 corrected
binary-partition asymptotic.

The theorem is uniform over all integer means, hence over the full dyadic phase
range `theta in (1/2,1]`, and uniformly for `m in [mu,2mu]`.

## 12. Phase-free variable

Put

```
x=log_2 mu=L+log_2 theta.
```

Since `log_2 theta` is bounded, substitution into (11.1) cancels the dyadic
phase at linear order:

```
-log_2 q_mu(m)
 = x^2
   + 2x log_2 x
   - 2 log_2(3e)x
   + o(x),                                            (12.1)
```

uniformly for `m in [mu,2mu]`.

Balancing this rate against `log_2 n` is consistent with the already-frozen
Session-8 center

```
sqrt(log_2 n)
- (1/2) log_2 log_2 n
+ log_2(3e).
```

No global balancing argument is needed or started in this session.

## 13. Exact diagnostics

`prob_stack/product_geometric_asymptotics.py` adds:

- the exact tilt sandwich and its uniform `B/(mu ln 2)` bound;
- the general linear probability coefficient;
- sharp positive, sharp low, sharp-seed, necessary, and final local
  coefficients;
- an efficient one-dimensional weighted generating-function DP;
- a Fraction version for moderate exact checks;
- deterministic diagnostic rows.

`scripts/tabulate_product_geometric_asymptotics.py` uses levels

```
L=4,6,8,10,12
```

and phases

```
theta=9/16, 3/4, 1.
```

The exact Fraction path is enabled through `L=8` by default; larger levels
use exact integer counts and deterministic floating logarithms.  The table
separates the count, `p^k`, tilt, total probability, predicted linear
coefficient, and residual.  No regression is used to infer a theorem.

The new tests also compare the fast exact Fraction DP with the pre-existing
ordinary-mass-profile implementation on exhaustive small instances.

## 14. Lean boundary

`ProbStack/FiniteDyadic.lean` now proves:

- ordinary coordinate mass is bounded by forward dyadic cost;
- ordinary coordinate mass is invariant under reversal;
- the same mass bound holds after reversal.

These are the exact finite inequalities needed by the paper proof of the tilt
sandwich.  De Bruijn's theorem and the analytic probability asymptotics are
intentionally not formalized in Lean.

## 15. Scope preserved

Session 17 does not:

- begin conditioning transfer;
- begin global first/second-moment asymptotics;
- reopen the binary-partition theorem;
- alter the canonical Session-14 seed witness;
- sharpen to zero offset or a limiting law;
- change EMPTY semantics;
- change TreeStack, Mathlib, or Lean pins.

The next mathematical stage is conditioning transfer and global path
asymptotics, using (11.1)--(12.1) as a black box.
