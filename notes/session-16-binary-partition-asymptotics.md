# Session 16: isolated binary-partition asymptotics

Status: the analytic input needed for the finite dyadic counts is now isolated
and checked. This note deliberately stops before geometric atom weights, local
seed probabilities, conditioning transfer, or global path asymptotics.

The frozen TreeStack semantics and frozen headline path theorem are unchanged.
In particular `TreeStack.EMPTY = none` remains categorical and is never
identified with integer zero.

## 1. Exact finite object and the four regimes

Recall

```text
N_{k,B}
 = #{x in Z_{\ge 0}^k : sum_{j=0}^{k-1} 2^j x_j <= B}.
```

Session 15 proved the exact coefficient identity

```text
N_{k,B}
 = [z^(2B)] prod_{j=0}^k (1-z^(2^j))^(-1).
```

Write

```text
A(B) = p_bin(2B),
```

where `p_bin(n)` is the unrestricted number of partitions of `n` into powers
of two. Thus `A(B)` is OEIS A000123 at index `B`.

For `L=ceil(log_2 mu)` and `theta=mu/2^L in (1/2,1]`, the finite regimes
needed downstream are:

| family | `k` | `B` | `lambda` in `B=lambda 2^L+O(1)` | truncation |
| --- | ---: | --- | ---: | --- |
| sharp positive descent | `L+2` | `2^(L+2)-2mu-1` | `4-2theta` | disappears exactly |
| sharp low amplification | `L` | `2^(L-1)` | `1/2` | disappears exactly |
| necessary positive entry, terminal `a` | `L-2` | `(a+3)2^(L-2)-5` | `(a+3)/4` | bounded factor |
| necessary low phase, start `a` | `L-2` | `(3-a)2^(L-3)-2` | `(3-a)/8` | exact for `a=1`, bounded factor for `a=0` |

Here `a` is `0` or `1`. The two necessary families are the exact Session 7
ones recovered from `notes/session-7-linear-order.md`; they have not been
reconstructed from an asymptotic guess.

## 2. Truncation versus unrestricted binary partitions

The Session 15 cutoff is sharper than the informal bounded-factor statement
used in Session 7.

### Exact cutoff

The coefficient defining `N_{k,B}` uses binary parts through `2^k` and has
total `2B`. The next omitted part is `2^(k+1)`. Therefore

```text
2^k > B
```

implies `2^(k+1)>2B`, so no omitted part can occur and

```text
N_{k,B}=A(B).                                             (2.1)
```

### General bounded-factor lemma

There is also a useful exact comparison valid without the cutoff:

```text
N_{k,B} <= A(B)
          <= A(floor(B/2^k)) N_{k,B}.                    (2.2)
```

Proof. View `A(B)` as the number of finite dyadic vectors
`(x_0,x_1,...)` with `sum_j 2^j x_j<=B`. Split a vector before coordinate
`k`. After division by `2^k`, its tail is an unrestricted dyadic vector of
budget at most `floor(B/2^k)`, hence has at most that many `A`-possibilities.
For every fixed tail, the first `k` coordinates have a residual budget at
most `B`, hence at most `N_{k,B}` possibilities. The opposite inequality is
inclusion. This proves (2.2).

Consequently, if

```text
k=L+a,
B=lambda 2^L+O(1),
```

with fixed integer `a` and fixed positive `lambda`, then the quotient in
(2.2) is bounded independently of `L`. Truncation therefore changes
`log_2 N_{k,B}` by only `O(1)`. This remains uniform for `lambda` in a fixed
compact subinterval of `(0,infinity)` and a uniformly bounded additive
budget shift.

For the exact downstream regimes this gives more:

- positive descent: `2^(L+2)>B_+` for every `theta in (1/2,1]`, so (2.1) is exact;
- low amplification: `2^L>2^(L-1)`, so (2.1) is exact;
- necessary positive entry with terminal `0`: the factor in (2.2) is at most
  `A(2)=4`;
- necessary positive entry with terminal `1`: the factor is at most
  `A(3)=6`;
- necessary low phase from `0`: the factor is at most `A(1)=2`;
- necessary low phase from `1`: the cutoff is exact.

Thus no later argument needs an unjustified silent replacement of the
truncated generating function by the infinite one.

## 3. The authoritative binary-partition asymptotic

The analytic input is N. G. de Bruijn, *On Mahler's partition problem*,
Indagationes Mathematicae 10 (1948), 210--220. Equation (1.3) gives the
logarithmic expansion for partitions into powers of an integer, and the paper
then refines its bounded term to a periodic function. For the binary case,
OEIS A000123 records the same formula in the convention directly used here:

```text
log p_bin(2n)
 = 1/(2h) (log(n/log n))^2
   + (1/2 + 1/h + log h/h) log n
   - (1 + log h/h) log log n
   + Phi((log n-log log n)/h),                         (3.1)
```

where `h=log 2`, all logarithms in (3.1) are natural, and `Phi` is bounded
and periodic.

The factor of two is now fixed unambiguously: Session 15 has
`A(B)=p_bin(2B)`, while (3.1) is already a formula for `p_bin(2n)`.
Therefore one substitutes

```text
n=B,
```

not `n=2B`. There is no extra `log_2 2` hidden in the linear coefficient.

## 4. Expansion in the ProbStack variables

Let

```text
B=lambda 2^L+O(1)
```

with fixed `lambda>0`, and set

```text
h = log 2,
t = log B = hL + log lambda + O(2^(-L)),
u = log t = log L + log h + O(1/L).
```

The first term in (3.1) is `(t-u)^2/(2h)`. Expand its three pieces:

```text
t^2/(2h)
  = (h/2)L^2 + (log lambda)L + O(1),

-tu/h
  = -L log L - L log h + O(log L),

u^2/(2h)
  = O((log L)^2).
```

The second term of (3.1) contributes

```text
(h/2 + 1 + log h)L + O(log L).
```

Its `+L log h` cancels the `-L log h` above. The third term is only
`O(log L)`, and `Phi` is bounded. Hence

```text
log A(B)
 = (h/2)L^2
   - L log L
   + (log lambda + h/2 + 1)L
   + O((log L)^2).
```

Dividing by `h=log 2` gives the base-two form

```text
log_2 A(B)
 = (1/2)L^2
   - L log_2 L
   + [log_2 lambda + 1/2 + log_2 e] L
   + O((log L)^2).                                    (4.1)
```

This derivation forces the sign

```text
- L log_2 L.
```

A plus sign is incompatible with the `-tu/h` cross term in de Bruijn's
square.

Combining (4.1) with (2.2) proves the exact asymptotic statement needed by
ProbStack:

> For any fixed integer `a`, compact interval
> `J subset (0,infinity)`, and fixed `C<infinity`, uniformly for
> `lambda in J` and integer budgets
> `B_L=lambda 2^L+delta_L` with `|delta_L|<=C`,
> if `k=L+a`, then
>
> ```text
> log_2 N_{k,B_L}
>  = (1/2)L^2
>    - L log_2 L
>    + [log_2 lambda + 1/2 + log_2 e]L
>    + O((log L)^2).
> ```
>
> The fixed support shift `a` does not enter the coefficient of `L`.

The stated compact-uniformity follows because the de Bruijn remainder in
(3.1) is bounded, all substitutions above are uniform on a compact
`lambda`-range away from zero, and the truncation multiplier in (2.2) is
uniformly bounded there.

No `O(1)` remainder is needed for the frozen headline theorem, so none is
pursued.

## 5. Sharp positive-descent count

For the Session 15 sharp descent,

```text
k_+ = L+2,
B_+ = 2^(L+2)-2mu-1
    = (4-2theta)2^L-1.
```

Thus

```text
lambda_+(theta)=4-2theta in [2,3).
```

The cutoff is exact, and uniformly over `theta in (1/2,1]`,

```text
log_2 N_{L+2,B_+}
 = (1/2)L^2
   - L log_2 L
   + [log_2(4-2theta)+1/2+log_2 e]L
   + O((log L)^2).                                    (5.1)
```

The strict `-1` in `B_+` is retained exactly. It is an `O(1)` budget shift
and therefore does not alter the displayed linear term.

## 6. Sharp low-amplification count

For the reversed low simplex, coordinate reversal preserves the count. Its
parameters are

```text
k_- = L,
B_- = 2^(L-1) = (1/2)2^L.
```

The cutoff is exact. Therefore

```text
log_2 N_{L,2^(L-1)}
 = (1/2)L^2
   - L log_2 L
   + [log_2 e-1/2]L
   + O((log L)^2).                                    (6.1)
```

This statement concerns only the number of simplex vectors. No geometric
atom factor is inserted in this session.

## 7. Session 7 necessary positive-entry simplex

Session 7 proves that for terminal `a in {0,1}` the last `d=L-2` positive
updates satisfy the necessary budget

```text
B^+_a = (a+3)2^d-5
      = ((a+3)/4)2^L-5.
```

Although the truncation is not exact, (2.2) gives factors at most `4` and `6`
for `a=0` and `a=1` respectively. Hence

```text
log_2 N_{L-2,B^+_a}
 = (1/2)L^2
   - L log_2 L
   + [log_2((a+3)/4)+1/2+log_2 e]L
   + O((log L)^2).                                    (7.1)
```

Equivalently the linear coefficient is

```text
log_2(a+3) - 3/2 + log_2 e.
```

## 8. Session 7 necessary low-phase simplex

For a low run starting from `a in {0,1}`, Session 7 gives `d=L-2` and

```text
B^-_a = (3-a)2^(d-1)-2
      = ((3-a)/8)2^L-2.
```

For `a=1` the cutoff is exact; for `a=0` the unrestricted/truncated ratio is
at most `A(1)=2`. Consequently

```text
log_2 N_{L-2,B^-_a}
 = (1/2)L^2
   - L log_2 L
   + [log_2((3-a)/8)+1/2+log_2 e]L
   + O((log L)^2).                                    (8.1)
```

Equivalently the linear coefficient is

```text
log_2(3-a) - 5/2 + log_2 e.
```

## 9. Colored reverse slack

Session 15 proved the exact identity

```text
C_d(B)=sum_{q=0}^{2^d-1} b_d(B-3q),                   (9.1)
```

where `b_d(n)` is the exact binary-partition coefficient using parts
`1,2,...,2^(d-1)`. Put

```text
S_d(T)=sum_{n=0}^T b_d(n)=N_{d,T}.
```

Because unit parts are available, `b_d(n)` is nondecreasing. The `2^d`
selected terms in (9.1) are the largest member of consecutive triples in the
top interval. Therefore, whenever `B>=3*2^d`,

```text
(1/3)[S_d(B)-S_d(B-3*2^d)]
 <= C_d(B)
 <= S_d(B).                                            (9.2)
```

Now take `B=c2^d+O(1)` with fixed `c>3`. Applying the theorem above at scales
`c` and `c-3` gives

```text
log_2 S_d(B-3*2^d)-log_2 S_d(B)
 = log_2((c-3)/c) d + O((log d)^2),
```

so the ratio of the lower cumulative term to the upper one tends to zero
exponentially. Thus (9.2) yields

```text
log_2 C_d(B)=log_2 N_{d,B}+O(1).                       (9.3)
```

For `c` in a compact subset of `(3,infinity)`, the bound is uniform.

Therefore colored slack changes none of:

- the quadratic coefficient;
- the `-L log_2 L` term;
- the linear coefficient.

Its effect is bounded on the logarithmic scale needed later. No claim is made
at the boundary `c=3`, because it is not needed here.

## 10. Exact diagnostics

`prob_stack/binary_partition_asymptotics.py` records the exact parameter
families, the cutoff test, the multiplicative truncation bound, and the three
displayed asymptotic terms. Exact counts remain integers.

`scripts/tabulate_binary_partition_asymptotics.py` tabulates levels
`6,8,10,12,14` by default and includes positive-descent phases
`theta=9/16,3/4,1`, together with the low-amplification and Session 7 necessary
families. The table records:

- exact `N_{k,B}`;
- unrestricted `A(B)`;
- exact/bounded truncation status;
- the residual after subtracting
  `(1/2)L^2-L log_2 L`;
- the residual after also subtracting the derived linear term.

The regression tests separately make the wrong `+L log_2 L` sign and a
spurious factor-two change of the partition argument decisively worse over
the diagnostic range. They also freeze the support shifts, theta dependence,
the strict descent `-1`, the exact cutoff criterion, and the explicit
truncation factors.

These computations validate indexing and signs; they are not used as the
proof of (4.1).

## 11. Lean boundary

`ProbStack/FiniteDyadic.lean` gains the exact arithmetic cutoff lemma saying
that `B<2^k` implies `2B<2^(k+1)`. Together with the Session 15
multiplicity-vector encoding, this is the finite fact needed before invoking
an external analytic binary-partition theorem.

The de Bruijn asymptotic itself is not formalised in Lean in Session 16.
Doing so would require analytic infrastructure disproportionate to the
current formalisation target. No `sorry` or new axiom is introduced.

## 12. Scope boundary and Session 17 target

Session 16 does **not** multiply these counts by geometric atom weights, does
not estimate the full local seed probability, does not transfer through the
fixed-total conditioning, and does not start the global path threshold proof.

The exact next target is the local excursion/seed probability asymptotic:
combine the finite ordinary-mass profile from Session 15 with the count
asymptotics proved here, control the geometric weighting without losing the
linear term, and recover the matching positive-entry/low-phase local rates
needed by the frozen headline theorem.

No zero-offset or finer-window question is opened.
