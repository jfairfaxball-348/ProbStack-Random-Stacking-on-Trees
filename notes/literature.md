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
