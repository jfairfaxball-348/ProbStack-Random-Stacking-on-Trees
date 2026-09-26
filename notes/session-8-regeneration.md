# Session 8 — constant-cost regeneration and theorem convergence

## Boundary and objective

Session 8 starts from ProbStack HEAD 07413bc3e99773ba8168087521433c45e5e2df99.
The authoritative TreeStack dependency remains
f4112f08d42a37c0941bf469ac124621b1f54f22.

The exact structural criterion remains

StackableAt(T,C,r) iff 0 < S_r(C),

and EMPTY remains categorical and distinct from integer zero.

The sole mathematical target in this session is the Session 7 spatial gap

(1/2) log_2 3.

The local linear theorem is not recomputed.

## 1. Exact one-step regeneration lemma

Let mu be a positive integer and let M be an integer message satisfying

-mu < M <= 2 mu.

Define the occupancy interval

I_mu(M) =
[ 2 mu + 2 - M , 4 mu - M ] intersect Z.

If X lies in I_mu(M), then

2 mu + 2 <= M+X <= 4 mu.

For every integer y in [2 mu+2,4 mu], the exact TreeStack transfer satisfies

mu <= F(y) <= 2 mu.

Indeed, for even y one has F(y)=y/2, while for odd y in this range one has
F(y)=(y-3)/2. Therefore

X in I_mu(M)
implies
F(M+X) in [mu,2 mu].

This is an exact integer statement; no affine approximation is used.

The interval is always nonnegative because M<=2mu. Its largest possible
occupancy occurs at M=-mu+1 and is 5mu-1. Thus regeneration uses one
coordinate and O(mu) local mass.

## 2. Uniform probability lower bound

For a geometric occupancy of integer mean mu, write

r = mu/(mu+1).

The interval I_mu(M) has 2mu-1 integer values, so

P[X in I_mu(M)]
=
r^(2mu+2-M) [1-r^(2mu-1)].

This is increasing in M. Hence the worst permitted incoming state is

M=-mu+1,

and the exact worst-case probability is

delta_mu
=
r^(3mu+1) [1-r^(2mu-1)].

For mu>=16 this is bounded below by a positive absolute constant. The elementary
bounds

r^mu > e^(-1),
r >= 16/17,
r^(2mu-1) <= r^mu <= 1/2

give

delta_mu >= 8/(17 e^3) = 0.0234292086....

The exact values in the committed table are already about 0.0434 at mu=16
and decrease slowly toward their positive limit.

Thus regeneration has constant cost, not merely exp(-o(L)) cost.

## 3. Treatment of already negative reset outputs

The Session 4 reset guarantees only an upper bound M<=2mu.

The missing lower bound is not needed.

If the reset output satisfies M<=-mu, it is already a deep seed and the
regeneration coordinate is skipped.

If instead -mu<M<=2mu, apply the one-step regeneration lemma above.

Therefore every reset output has one of two favourable continuations:

1. it is already a deep seed; or
2. with conditional probability at least delta_mu it enters the sharp local
   starting window [mu,2mu] in one exact TreeStack update.

No stationary distribution or mixing statement for the message chain is used.

## 4. Concatenation with the Session 7 local excursion

Let

q_mu(m)
=
P_m[min_{1<=j<=4L} M_j <= -mu],

where L=ceil(log_2 mu).

Session 7 proves uniformly for m in [mu,2mu] that, with x=log_2 mu,

-log_2 q_mu(m)
=
x^2
+
2x log_2 x
-
2 log_2(3e) x
+
o(x).

After regeneration, the future occupancies are independent under the product
law, so the strong Markov property applies directly.

For a fully constructive lower event with deterministic local mass, one may
use the fixed-delay lower constructions from the Session 7 proof rather than
the unrestricted event q_mu itself. For every eta>0, choose the two fixed
delays large enough that the positive-entry and final-low coefficients are
within eta of their limiting coefficients. The resulting event:

- has length 2L+O_eta(1);
- has deterministic mass O_eta(mu);
- ends at a message at most -mu; and
- has logarithmic probability equal to the optimal Session 7 rate up to
  eta L+o(L).

Because eta is arbitrary, the state-independent spatial certificate has the
same limiting linear coefficient as the local q_mu theorem. A standard
diagonal choice would also produce one event family with o(L) excess, but the
fixed-epsilon global theorem below only needs the simpler eta-dependent
construction.

## 5. Conversion of a deep seed to a true front

Once M<=-mu, the Session 4 runaway buffer applies unchanged.

Starting with deficit Z=3-M>=mu+3, impose at each step

X <= floor(D/4),

where D is the current deterministic deficit lower bound. Then the low-phase
recurrence gives growth by at least 3/2 per step. Continue until the certified
deficit exceeds 2nmu+3.

The existing product probability lower bound for this whole runaway stage is
the positive universal constant c_*>0.0095.

Hence reset, regeneration, the sharp local excursion, and runaway concatenate
without any new linear-in-L probability cost.

## 6. Uniform adaptive superblock hazard

Reserve a superblock containing:

- the Session 4 reset block;
- one regeneration coordinate;
- at most 4L local-excursion coordinates;
- the Session 4 runaway buffer.

If the reset output is already at most -mu, the procedure jumps directly to
the runaway stage and ignores the unused reserved coordinates.

Otherwise it requires the regeneration occupancy and then the sharp local
excursion.

For every incoming active integer message at most 2nmu, and also for EMPTY
after the reset activates the branch, the conditional product-law probability
of a successful true-front construction is at least

p_mu,n
>=
c_reset(mu)
delta_mu
q_mu^*
c_run,

where q_mu^* is the minimum of q_mu(m) over m in [mu,2mu], and c_reset and
c_run are positive constants at the required asymptotic scale.

Thus

-log_2 p_mu,n

has exactly the Session 7 local linear coefficient. The reset, regeneration,
and runaway pieces contribute only O(1) to this logarithm.

The event is adaptive in the incoming message. This is intentional and avoids
inventing a stationary law.

## 7. Conditioning argument for adaptive blocks

Because the regeneration interval depends on the incoming message, Session 8
does not pretend that the corresponding success indicators are independent
under the fixed-total law.

Instead return to the global conditioning method used in Session 4.

Under the iid geometric product law, scan disjoint reserved superblocks in one
half of the path. On the event that the total product mass is at most 2nmu,
every prefix mass is at most 2nmu. The message-versus-mass lemma therefore
gives the incoming upper bound required by the reset at every attempted block.

Conditioned on any preceding history with no earlier success and prefix mass at
most 2nmu, the next unused occupancies are independent geometrics, so the
success probability is at least p_mu,n.

Induction gives

P_prod[
 no successful certified front in B blocks
 and total mass <= 2nmu
]
<=
(1-p_mu,n)^B.

Now condition on total mass exactly nmu. Since this conditioning event is a
subset of total mass <=2nmu,

P_cond[no front in the half]
<=
(1-p_mu,n)^B
/
P_prod[total mass=nmu].

The exact negative-binomial point probability from Sessions 4 and 6 has
logarithmic reciprocal O(log n+log mu).

At the fixed-offset subcritical regime proved below, B p_mu,n is
2^{Theta(sqrt(log_2 n))} up to polylogarithmic factors. Therefore

exp(-B p_mu,n)

beats the reciprocal conditioning point probability by an overwhelming
margin. The earlier sqrt(n)-scale conditioning loss is harmless at this
fixed-offset precision.

The same argument is applied to the reversed scan in the other half. A union
bound, not conditioned independence, gives both opposing fronts with
probability tending to one.

Optional local mass truncations remain available: the steering occupancy is
at most 5mu-1; the fixed-delay Session 7 lower event has O_eta(mu) mass; and
the Session 6 reset/runaway truncations keep constant probability with total
superblock mass O(mu log n). They are not needed for the global division
argument, but they verify that the new mechanism remains spatially local.

## 8. Closing the global constant gap

Put

N=log_2 n,
s=sqrt(N),

and define

c_n
=
s
-
log_2 s
+
log_2(3e)

=
sqrt(log_2 n)
-
(1/2) log_2 log_2 n
+
log_2(3e).

The Session 7 local rate is

R(x)
=
x^2
+
2x log_2 x
-
2 log_2(3e)x
+
o(x).

At x=c_n,

R(c_n)=N+o(s).

If x<=c_n-epsilon for fixed epsilon>0, then

N-R(x)
=
(2 epsilon+o(1)) s.

Consequently the expected product-law number of successful reserved blocks in
a half is exponentially large in s, even after the O(log n) block-length
loss. The global conditioning estimate in Section 7 therefore forces a true
front in each half with probability tending to one. Opposing fronts certify
nonstackability.

The Session 7 deep-message necessity and local upper cover already prove the
matching supercritical statement for x>=c_n+epsilon.

Therefore the Session 7 gap

(1/2) log_2 3

is closed.

## 9. Frozen headline theorem

Let C_n be uniformly distributed over weak compositions of total n mu_n on
the path P_n, where mu_n is a positive integer sequence. Define c_n as above.

For every fixed epsilon>0:

- if log_2 mu_n <= c_n-epsilon for all sufficiently large n, then

  P[C_n is stackable] -> 0;

- if log_2 mu_n >= c_n+epsilon for all sufficiently large n, then

  P[C_n is stackable] -> 1.

No assertion is made at epsilon=0.

This is the theorem to freeze for formalisation design.

## 10. Computation and validation

No Monte Carlo was used.

The new exact code is in prob_stack/regeneration.py.

The new targeted test file checks:

- exact steering into [mu,2mu] for every occupancy in the prescribed interval
  across complete integer message ranges for several means;
- the exact worst-case probability formula;
- the location of the worst incoming message;
- the absolute constant lower bound for every integer mean from 16 through
  256; and
- the deterministic O(mu) occupancy cap.

A literal targeted run in the Session 8 validation harness gave

5 passed.

This was not a literal full repository pytest run, so no new full-suite pass is
claimed. The last literal full-suite result recorded by the project remains the
Session 5 result of 54 tests passed.

The exact table data/regeneration_exact.csv was generated with Fraction
arithmetic. Its numerator and denominator columns are exact.

## 11. Literature

No literature search was needed in Session 8. The gap closed by an elementary
exact use of the already-authoritative TreeStack transfer and the existing
Session 4/7 machinery.

No novelty or priority claim is made.

## 12. Formalisation design implications

The theorem is now stable enough to move to formalisation design.

Major deterministic components:

1. exact TreeStack path-message recurrence with categorical EMPTY;
2. global inequality F(x)<=x/2;
3. message-versus-mass lemma;
4. reset contraction;
5. exact regeneration interval lemma;
6. low-phase deficit recurrence;
7. runaway deep-seed-to-front lemma;
8. two opposing fronts imply global nonstackability;
9. deep-message necessity for nonstackability.

Major probabilistic/combinatorial components:

10. geometric representation of the uniform weak-composition law by
    conditioning on the total;
11. reset probability lower bound;
12. exact regeneration probability and uniform minorisation;
13. terminal-specific positive-entry and low-phase excursion bounds;
14. binary-partition / dyadic-simplex asymptotics;
15. adaptive sequential-hazard lemma for disjoint product blocks;
16. negative-binomial point-mass estimate for conditioning;
17. Session 5 deep-message upper cover.

Major asymptotic component:

18. expansion of the local rate around c_n and conversion of fixed offsets into
    exponentially many or vanishing local hazards.

The major external analytic ingredient remains de Bruijn's binary-partition
asymptotic. A complete Lean development will need either a formal replacement
with precisely the required error term or a separately isolated analytic
theorem that is subsequently formalised.

## Decision

FREEZE THEOREM AND MOVE TO FORMALISATION DESIGN.

Do not spend the next session on smaller local corrections, a limiting
critical law, Poisson front processes, finite-n monotonicity, or other tree
families.

The single best next step is to design the Lean theorem dependency graph and
separate the elementary TreeStack/probability lemmas from the binary-partition
asymptotic layer.
