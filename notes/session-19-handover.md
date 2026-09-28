# Session 19 handover — closure to prior-art audit

## Repository boundary

Session 19 started from exact validated `main`

`28d4dbf0e4692e544324fa7810c90791de4cd648`.

The final merged SHA, final successful GitHub Actions run ID, and exact final
Python test count are recorded in the external Session 19 end-of-session
report, because a committed handover cannot self-contain the SHA of the commit
that contains itself.

Dependency pins remain:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean: `leanprover/lean4:v4.35.0-rc2`.

The permanent workflow remains `.github/workflows/lean-bootstrap.yml`.

## Authoritative theorem

For uniform weak compositions of total (nmu_n) on (P_n),

[
c_n=sqrt{log_2 n}
-rac12log_2log_2 n
+log_2(3e).
]

For every fixed (arepsilon>0), means below (c_n-arepsilon) eventually
give stackability probability tending to zero, while means above
(c_n+arepsilon) eventually give stackability probability tending to one.
There is no zero-offset claim.

The MINUS half-log-log sign and (log_2(3e)) constant are frozen.

## Authoritative maps

- final status: `docs/FINAL_THEOREM_STATUS.md`;
- proof dependency map: `docs/PROOF_DEPENDENCY_MAP.md`;
- reproducibility entry point: `docs/REPRODUCIBILITY.md`;
- Session 19 audit/closure note: `notes/session-19-closure.md`.

Historical Session 6/7 documents remain unchanged in mathematical content but
are explicitly labelled as historical where current-facing readers could
otherwise mistake them for the final theorem.

## Exact imported local theorem

Session 17 is a black box:

[
-log_2 q_mu(m)
=x^2+2xlog_2x-2log_2(3e)x+o(x),
qquad x=log_2mu,
]

uniformly over the full dyadic phase range and all integer
(min[mu,2mu]).

Session 19 does not recompute it.

## Exact regeneration statement

For (-mu<Mle2mu), an occupancy

[
2mu+2-Mle Xle4mu-M
]

forces the next message into ([mu,2mu]). The largest steering occupancy is
(5mu-1), and the exact worst-case probability is

[
left(rac{mu}{mu+1}ight)^{3mu+1}
left[1-left(rac{mu}{mu+1}ight)^{2mu-1}ight],
]

at least (8/(17e^3)) for integer (muge16). If reset already yields
(Mle-mu), steering is skipped.

## Subcritical architecture

Use fresh product-law coordinates in each unused reserved superblock. Obtain
the no-success bound under the product law first, with
(Omega(n/log n)) candidates per half. Only then condition on total
(nmu). The product no-success exponent overwhelms the (O(log n))-bit
conditioning cost at every fixed negative offset. Repeat in the reversed half
and use the opposing-front deterministic theorem.

Conditioned independence is not used.

## Supercritical architecture

Nonstackability forces the exact target (-(2mu-1)). The optimized
terminal-specific cover has the Session 17 interior rate. The (0	o0) route
is cheapest. The (1	o0) route requires an exact-output-zero bridge; since
(F(y)=0) only for (y=3), one occupancy is fixed once the incoming message
is known, costing (L+O(1)) bits. Interior locations receive the (O(n))
multiplicity; physical-boundary events have only (O(1)) locations. Local
conditioning transfer is applied to bounded support/mass events.

## Fixed-offset calculation

With (N=log_2n), (s=sqrt N), and

[
x=s-log_2s+log_2(3e)+delta,
]

the local main rate satisfies

[
R(x)=N+2delta s+o(s),
qquad
N-R(x)=-2deltasqrt N+o(sqrt N).
]

This is the final balance used on both sides.

## Formalisation boundary

The finite Lean layer is exact and no-`sorry`/no-new-axiom. The final
analytic theorem remains paper mathematics. Session 19 also records accurately
that the full Session 5 global deep-message necessity and the global
opposing-front implication are paper deterministic results rather than
currently packaged ProbStack Lean theorems.

No dependency semantics, EMPTY semantics, frozen theorem, or permanent CI
design is changed.

## Next stage

The next session is an **extensive public-record prior-art/originality audit**.
It should investigate, without making novelty claims:

- random weak compositions and conditioned geometric vectors;
- graph pebbling/stacking on paths and trees;
- TreeStack-style structural/root-score certificates;
- binary partitions and de Bruijn-type asymptotics;
- random affine/message recurrences and rare deficit-front mechanisms;
- threshold phenomena at stretched-logarithmic densities;
- equivalent formulations under occupancy, composition, queueing, branching,
  renewal, or extreme-value terminology.

The audit should search journals, arXiv, MathSciNet/zbMATH where accessible,
Google-Scholar-style citation trails, proceedings, theses, author pages, and
references/citing references, and maintain a reproducible search log. It must
not infer novelty from a negative search.
