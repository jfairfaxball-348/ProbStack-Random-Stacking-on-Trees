# Session 15: finite dyadic / binary-partition combinatorics

Status: finite mathematics stabilised. This session deliberately does **not**
start the binary-partition asymptotic. It reconstructs the exact finite
objects used in Sessions 6--7, aligns them with the Session-14 deterministic
probability interface, and freezes the indexing needed by the next stage.

The frozen TreeStack semantics and frozen headline theorem are unchanged.
`TreeStack.EMPTY = none` remains categorical and is never identified with
integer zero.

## 1. Ordered dyadic simplex

For integers `k,B >= 0`, define

```
E_{k,B} = {x in Z_{>=0}^k : sum_{j=0}^{k-1} 2^j x_j <= B},
N_{k,B} = |E_{k,B}|.
```

Zeros are allowed in every coordinate. Coordinates are ordered: coordinate
`j` has weight `2^j`. Reversing the weights changes the predicate on a fixed
vector, although coordinate reversal is a bijection and preserves the total
count.

The endpoint convention is `N_{0,B}=1` for `B>=0`. Negative budgets have
count zero in the executable interface.

Fixing the last coordinate gives the exact recurrence, for `k>=1`,

```
N_{k,B}
 = sum_{q=0}^{floor(B/2^(k-1))}
     N_{k-1, B-q 2^(k-1)}.                            (1)
```

## 2. Exact finite binary-partition coefficient

Let

```
Q_k(n) = [z^n] prod_{j=0}^k (1-z^(2^j))^(-1),
```

the number of binary partitions of `n` using only parts

```
1,2,4,...,2^k
```

with unrestricted multiplicities. Then the exact finite identity is

```
N_{k,B} = Q_k(2B)
        = [z^(2B)] prod_{j=0}^k (1-z^(2^j))^(-1).      (2)
```

The bijection fixes the indexing. Given
`x=(x_0,...,x_{k-1}) in E_{k,B}`, use `x_j` copies of the part
`2^(j+1)` and add

```
2(B - sum_j 2^j x_j)
```

unit parts. This produces a partition of exactly `2B` using parts at most
`2^k`. Conversely, a binary partition of even total `2B` using parts
through `2^k` has an even number of unit parts; remove them and halve the
remaining parts to recover the unique vector in `E_{k,B}`.

Thus the finite object is a **truncated** binary-partition coefficient. It
must not be silently replaced by the infinite generating function.

If `2^k>B`, the next omitted binary part is already larger than `2B`, so
(2) equals the unrestricted binary-partition count of `2B`. Writing
`A(B)=p_bin(2B)` recovers the Session-7 cumulative sequence with exact
recurrence

```
A(0)=1,
A(B)=A(B-1)+A(floor(B/2))  for B>=1.                  (3)
```

## 3. Exact relation to Session-14 positive descent

Session 14 has

```
affineInputCost [x_1,...,x_k]
 = x_1 + 2x_2 + ... + 2^(k-1)x_k
```

and

```
PositiveDescentEvent mu xs
iff 2mu + affineInputCost xs < 2^k.
```

Since all quantities are integral, this is exactly

```
affineInputCost xs <= 2^k - 2mu - 1.                  (4)
```

Therefore, when `B_+(mu,k)=2^k-2mu-1>=0`, the number of positive-descent
vectors of support `k` is exactly `N_{k,B_+(mu,k)}`. If the budget is
negative, the event is empty. The `-1` is forced by the strict inequality.

The sharp Session-6 lower witness uses

```
L = ceil(log_2 mu),
k_+ = L+2,
B_+ = 2^(L+2)-2mu-1.                                  (5)
```

This is not the Session-14 rectangular cap descent, which has support
`L+4` and caps `floor(mu/(L 2^j))`, `j=1,...,L+4`. Both imply
nonpositive descent, but they are distinct finite events and serve different
purposes. The canonical Session-14 cap witness is preserved.

At `mu=16`, the sharp simplex descent has support `6` and budget `31`;
the canonical cap descent has support `8`.

## 4. Exact product-geometric mass

Keep the geometric convention

```
p=1/(1+mu), r=mu/(1+mu), P(X=x)=p r^x.
```

Refine the count by ordinary local mass:

```
N_{k,B}(s)
 = #{x in E_{k,B} : sum_j x_j=s}.
```

Then the exact finite product probability is

```
P(E_{k,B})
 = p^k sum_{s>=0} N_{k,B}(s) r^s.                     (6)
```

This refinement is necessary because the geometric atom depends on the
ordinary coordinate sum, not the dyadic weighted sum. The new Python
`dyadic_simplex_mass_counts` computes this profile exactly and
`geometric_simplex_product_probability_exact` evaluates (6) using
`Fraction` arithmetic.

## 5. Low-phase amplification

Let `D` be the certified deficit. Session 14 uses

```
x_j <= D_{j-1}-2,
D_j = 2(D_{j-1}-x_j).                                 (7)
```

For a length-`k` block,

```
D_k
 = 2^k D_0 - 2 sum_{j=1}^k 2^(k-j)x_j.               (8)
```

Write the reversed dyadic cost as

```
R_k(x)=sum_{j=1}^k 2^(k-j)x_j.
```

For `D_0>=2`, the finite simplex

```
R_k(x) <= (D_0-2)2^(k-1)                              (9)
```

is sufficient for all recursive `LowBudget` constraints. Every prefix
satisfies the corresponding scaled inequality, and (8) gives

```
D_k >= 2^(k+1).                                       (10)
```

For the historical Session-6 start `D_0=3`, (9) becomes

```
sum_{j=1}^k 2^(k-j)x_j <= 2^(k-1).                   (11)
```

Taking `k=L` gives the Session-6 low-phase amplification block. At
`mu=16`, it has support `4` and budget `8`. It is distinct from the
preserved canonical Session-14 amplification rectangle `(0,1,2,4)`.

## 6. Sharp finite two-simplex seed

The finite Session-6 lower event is now frozen as

```
positive descent:  k_+=L+2, B_+=2^(L+2)-2mu-1;
low amplification: k_-=L,  B_-=2^(L-1), reversed weights.
```

Its support length is exactly

```
2L+2.                                                  (12)
```

The two blocks are disjoint under the product law, so the exact probability is

```
P_seed(mu)
 = P(E_{L+2,B_+}) P(E_{L,B_-}),                        (13)
```

with each factor evaluated by (6). No asymptotic estimate is used here.

At `mu=16`, the sharp seed has support `10`, descent budget `31`, and
amplification budget `8`. This must not be confused with the canonical
Session-14 cap seed, whose support is `12`, local cap mass bound is `10`,
and certified final deficit is `24`.

## 7. Session-7 colored reverse slack

The reverse positive-phase slack `y` has multiplicity

```
m(y)=1 for y=0,1,2,
m(y)=2 for y>=3.
```

One dyadic level of weight `w` therefore contributes

```
sum_{y>=0} m(y) z^(wy)
 = (1+z^(3w))/(1-z^w).
```

Across `d` levels,

```
prod_{j=0}^{d-1} (1+z^(3*2^j))/(1-z^(2^j))
 = (1-z^(3*2^d))/(1-z^3)
   prod_{j=0}^{d-1}(1-z^(2^j))^(-1).                 (14)
```

The numerator telescopes exactly. Since

```
(1-z^(3*2^d))/(1-z^3)
 = sum_{q=0}^{2^d-1} z^(3q),
```

if `b_d(n)` counts exact binary partitions using parts
`1,...,2^(d-1)`, then

```
C_d(B)=sum_{q=0}^{2^d-1} b_d(B-3q),                  (15)
```

with `b_d(n)=0` for negative `n`. Equation (15) is the exact finite parity
identity from Session 7; there is no hidden parity constant.

## 8. Lean formalisation

`ProbStack/FiniteDyadic.lean` adds:

- `forwardDyadicInputCost`, alongside the pre-existing reversed `dyadicInputCost` from `ProbStack.Deficit`;
- `affineInputCost_eq_forwardDyadicInputCost`;
- `positiveDescentBudgetInt`;
- `positiveDescentEvent_iff_forwardDyadicInputCost_le`;
- `binaryPartitionEncoding`;
- `binaryPartitionEncoding_cost`;
- `binaryPartition_tail_le`;
- `binaryPartition_head_eq_slack`;
- `lowBudgetFinal_closed_form`;
- `LowPhaseSimplex`;
- `lowPhaseSimplex_final_ge`.

The low-phase closed form deliberately reuses the pre-existing `dyadicInputCost`, whose weights are exactly twice the reversed occupancy weights in (8). The binary-partition encoding lemmas formalise the finite bijection behind
(2) at the multiplicity-vector level without introducing polynomial
coefficient machinery. A full `Fintype.card` theorem can be added later if a
downstream theorem actually requires it.

The full event-level weak-composition conditioning formula remains a secondary
Lean gap. Session 14's exact conditioning algebra and Python count are
unchanged.

## 9. Exact tests

`tests/test_finite_dyadic.py` uses exact integer or `Fraction` arithmetic
and checks:

- the truncated binary-partition coefficient identity (2);
- the cutoff to unrestricted binary partitions and recurrence (3);
- ordered-vector enumeration against the ordinary-mass profile;
- reversed dyadic weights;
- zero-coordinate and empty-vector conventions;
- the strict boundary in (4);
- exact geometric atom summation in (6);
- the deficit closed form (8);
- the low-simplex implication into the recursive budget on exhaustive small
  instances;
- the frozen `mu=16` sharp-seed lengths and budgets;
- the colored-slack identity (15);
- exact finite counts lying on the negative `-L log_2 L` side of the leading
  `L^2/2` count scale for selected even levels.

The standalone Session-15 harness passes 11 tests.

## 10. Scope and next target

This session does not start de Bruijn's asymptotic or any replacement
binary-partition asymptotic, does not start local seed asymptotics, does not
start conditioned global asymptotics, does not revisit the frozen headline
path theorem, and does not alter EMPTY semantics or dependency pins.

The next isolated target is the binary-partition asymptotic starting from the
exact finite coefficient (2), with truncation handled explicitly. The finite
formula already forces the second logarithmic correction to have sign

```
-L log_2 L,
```

not `+L log_2 L`.
