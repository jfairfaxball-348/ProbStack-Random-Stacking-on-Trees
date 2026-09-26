# Literature orientation log

**Status:** limited seed/orientation pass only.  This is not the later
comprehensive prior-art/originality audit, and no novelty or priority conclusion
is drawn from it.

Date of pass: 2026-09-26.

## Seed papers inspected

1. Gábor Csernák and Lajos Soukup, *Stacking and Clearing in Graph Pebbling*,
   arXiv:2604.22341.  Read the definitions of configurations, legal pebbling
   moves, stacked/stackable configurations, the stacking number, the path
   formula, and the discussion of the tree conjecture.  The paper defines
   `stack(P_n)=2^n-1` for `n>=2` and supplies the source terminology used here.
   <https://arxiv.org/abs/2604.22341>

2. Nathaniel Bushaw and Nathan Kettle, *Thresholds for Pebbling on Grids*,
   arXiv:2309.01762.  Read the random model, weak/strong threshold discussion,
   path result, and local fixed-total occupancy estimate.  It uses the same
   uniform law on distributions of `t` unlabeled pebbles and explicitly counts
   `binom(n+t-1,t)` configurations.
   <https://arxiv.org/abs/2309.01762>

3. Airat Bekmetjev, Graham Brightwell, Andrzej Czygrinow, and Glenn Hurlbert,
   *Thresholds for families of multisets, with an application to graph
   pebbling*, arXiv:math/0406068.  Read the multiset probability-space setup,
   the explicit warning that independent labeled-pebble placement is a
   different model, and the increasing-family threshold theorem.  The latter
   cannot simply be imported into ProbStack because stackability is not an
   increasing family under coordinatewise addition.
   <https://arxiv.org/abs/math/0406068>

4. Glenn Hurlbert, *A Survey of Graph Pebbling*, arXiv:math/0406024.  Inspected
   the survey as an orientation source for the history and probabilistic
   pebbling/threshold literature.
   <https://arxiv.org/abs/math/0406024>

## Follow-reference orientation

Searches also followed path-threshold references and located, among others,
Czygrinow--Hurlbert, *On the pebbling threshold of paths and the pebbling
threshold spectrum* (Discrete Mathematics, 2008), and the later improved upper
bound by Godbole--Jablonski--Salzman--Wierman.  These are context for ordinary
pebbling on paths, not evidence that the stacking problem has the same scale.

## Search log

Queries used in the orientation pass included the four exact paper titles / arXiv
identifiers, `graph pebbling random configurations threshold paths`, `pebbling
threshold paths`, `pebbling threshold spectrum`, `uniform multiset pebbling`,
and citation trails from the seed papers to path-threshold work.

The eventual prior-art audit must be much broader: journal databases,
MathSciNet/zbMATH where accessible, Scholar-style citation trails,
bibliographies, author pages, proceedings, theses, terminology variants, and
mathematically equivalent formulations.  A negative later audit can support
only a qualified public-record statement; it cannot rule out unpublished or
unindexed work.


## Session 3 orientation: dyadic small deviations and Mahler partitions

Date of pass: 2026-09-26. This was a narrow mechanism-oriented search, not a
novelty audit.

The exact dyadic low-phase budget suggested checking classical work on powers-
of-two partitions and modern weighted-small-deviation results.

1. Kurt Mahler, *On a Special Functional Equation*, Journal of the London
   Mathematical Society 15 (1940), 115–123,
   DOI `10.1112/jlms/s1-15.2.115`. Bibliographic record inspected at the
   publisher. This is the source cited by de Bruijn for Mahler's partition
   problem.

2. N. G. de Bruijn, *On Mahler's partition problem*, Proceedings of the Section
   of Sciences of the Koninklijke Nederlandse Akademie van Wetenschappen te
   Amsterdam 51(6) (1948), 659–669. The publisher-version PDF introduction and
   displayed asymptotic were inspected. For partitions into powers of an
   integer `r`, de Bruijn records a leading term
   `(2 log r)^{-1}(log(h/log h))^2` in `log p(rh)`, with refined lower-order and
   periodic terms. For `r=2`, the corresponding quadratic-log coefficient is
   consistent with the half-quadratic cost that appears in each phase of the
   ProbStack cap calculation. This is an analogy, not an invocation of de
   Bruijn's theorem for the message chain.

3. L. V. Rozovsky, *Small Deviations of Probabilities for Weighted Sum of
   Independent Positive Random Variables with a Common Distribution That
   Decreases at Zero Not Faster than a Power*, Theory of Probability & Its
   Applications 60 (2016), 142–150, DOI `10.1137/S0040585X97T987545`.
   Publisher abstract inspected; it studies small deviations for weighted sums
   of independent positive random variables under power-type behavior near
   zero.

4. L. V. Rozovsky, *Small Deviation Probabilities for a Weighted Sum of
   Independent Positive Random Variables with Common Distribution Function
   That Can Decrease at Zero Fast Enough*, Theory of Probability & Its
   Applications 63(1) (2018), 155–163,
   DOI `10.1137/S0040585X97T988976`. Publisher abstract and reference list
   inspected. This gives broader context for weighted small deviations,
   including distributions with faster decay near zero.

The Session 3 proof in ProbStack remains elementary and self-contained: it
uses exact TreeStack recurrences plus direct geometric-CDF inequalities. No
claim is made that the cited small-deviation theorems apply verbatim, and no
novelty or priority conclusion is drawn from this limited search.
