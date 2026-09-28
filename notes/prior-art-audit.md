# Session 20 public-record prior-art / originality audit

Date of audit: 2026-09-28

Status: public-record literature audit in progress. This document is an audit record, not a novelty, priority, originality, publication, or submission claim.

## 1. Frozen project boundary

This audit starts from validated main commit:

d03b8381eb1b4cc100146cadbed3035c31c7016d

The audit does not change the frozen theorem, the Session 17 local rate, EMPTY semantics, dependency pins, Lean semantics, Python mathematics, or permanent CI.

The frozen path theorem remains:

c_n = sqrt(log_2 n) - (1/2) log_2 log_2 n + log_2(3e),

with the two fixed-epsilon implications recorded in docs/FINAL_THEOREM_STATUS.md and no theorem at epsilon = 0.

The exact event studied by ProbStack is stackability: a configuration is stackable if legal pebbling moves can reach a configuration supported on one vertex. The random law is the uniform law on weak compositions of the fixed total n*mu over the n path vertices.

A negative literature search is not evidence of novelty. All "no match located" statements below mean only "no match located in the public sources searched during this audit".

## 2. Executive comparison

The audit found three especially close but distinct prior-art lines.

1. Exact event terminology and deterministic problem: Csernák and Soukup, "Stacking and clearing in graph pebbling" (arXiv:2604.22341, 2026), defines a configuration to be stackable when a stacked configuration, i.e. one supported on a single vertex, is reachable. This is the same event definition as ProbStack. Their paper studies worst-case stacking numbers and deterministic graph classes, not the probability of stackability under a uniform fixed-total random configuration.

2. Exact probability law, exact graph family, and very close asymptotic scale: the random graph-pebbling threshold literature, from Czygrinow-Eaton-Hurlbert-Kayll and Bekmetjev-Brightwell-Czygrinow-Hurlbert through Moews and Bushaw-Kettle, uses the uniform multiset law on t indistinguishable pebbles over n vertices. Thus this is the same weak-composition probability law as ProbStack. However its event is graph/root solvability, not stackability. For paths, Moews obtains threshold order n*2^{sqrt(log_2 n)}/sqrt(log_2 n), and Bushaw-Kettle obtains a strong path threshold with the same leading square-root-log and minus-half-log-log structure that appears in ProbStack's density coordinate. Bushaw-Kettle also uses binary/power-of-q partition counts in its sharp path analysis.

3. Exact analytic ingredient: the binary-partition asymptotics used in ProbStack lie in the Mahler/de Bruijn/Pennington/Protasov line. The quadratic logarithmic term, log-log correction structure, and bounded periodic correction are classical. ProbStack's use of these facts inside its particular rare local deficit/front event is an application, not a new binary-partition asymptotic.

No inspected source combined all of the following in one theorem: the stackability event, the uniform fixed-total weak-composition law, paths, and the frozen fixed-offset center with additive constant log_2(3e). That statement is only a search outcome, not an originality conclusion.

## 3. Model and event distinctions that must be preserved

### 3.1 Uniform fixed-total law

For n vertices and total t, both ProbStack and the classical multiset random-pebbling papers choose uniformly among the binomial(n+t-1,t) weak compositions. This is also the Bose-Einstein/equiprobable balls-in-boxes model.

This is not the Maxwell-Boltzmann/multinomial model obtained by independently placing t labelled pebbles.

This distinction is already explicit in the pebbling literature. Cover-pebbling threshold work by Godbole, Watson, and Yerger treats Bose-Einstein and Maxwell-Boltzmann models separately.

### 3.2 Stackability versus solvability

ProbStack stackability:
there exists a vertex r such that legal moves can transform the configuration into one whose entire surviving support is {r}.

Csernák-Soukup stackability:
the same deterministic event definition.

Classical pebbling solvability:
for every prescribed root r, it is possible, potentially using a different sequence for each r, to move at least one pebble to r.

These are not interchangeable. The random-solvability threshold literature is therefore close prior art but not an exact theorem match.

### 3.3 Cover pebbling

Cover pebbling asks for a move sequence ending with every vertex occupied, or more generally meeting a target demand. Sjöstrand's "Cover Pebbling Theorem" is sometimes described via a stacking principle because worst-case cover demand can be tested by configurations initially stacked at one vertex. That use of "stacking" is different from ProbStack's random stackability event.

## 4. Closest prior art

### 4.1 Tamás Csernák and Lajos Soukup — Stacking and clearing in graph pebbling

Primary source:
Tamás Csernák and Lajos Soukup, "Stacking and clearing in graph pebbling", arXiv:2604.22341 (2026).
https://arxiv.org/abs/2604.22341

Exact model:
deterministic pebble configurations on finite graphs under the standard move removing two pebbles at a vertex and adding one at an adjacent vertex.

Theorem/problem:
introduces stack(G), the least t >= 2 such that every size-t configuration is stackable; proves exact values for several graph classes, including stack(P_n)=2^n-1. The paper also proposes an Almost Stacked Hypothesis and a conjectural tree formula supported computationally on small trees.

Probability law:
none for the main stacking-number problem. It is worst-case over all configurations of a given size.

Asymptotic scale:
the path result is the deterministic worst-case value 2^n-1, not a random high-density transition.

Deterministic mechanism:
global pebbling arguments, almost-stacked reductions, distance/degree quantities for trees.

Overlap with ProbStack:
the word "stackable" and its event definition are an exact match.

Concrete difference:
ProbStack asks for the probability that a uniform weak composition of total n*mu on P_n is stackable and proves a high-density fixed-offset transition. The Csernák-Soukup paper does not study that random probability law or that threshold theorem. Its tree discussion does not provide the TreeStack arbitrary-configuration Option-Z branch-message/root-score certificate used by ProbStack.

Audit status:
close prior-art result requiring explicit comparison in any eventual paper.

### 4.2 Neal Bushaw and Nathan Kettle — Thresholds for pebbling on grids

Primary source:
Neal Bushaw and Nathan Kettle, "Thresholds for pebbling on grids", Discrete Mathematics 348(10) (2025), 114519.
DOI: https://doi.org/10.1016/j.disc.2025.114519
arXiv: https://arxiv.org/abs/2309.01762

Exact model:
uniform random distribution of t unlabelled pebbles over the vertices. Their notation D_{G,t} has cardinality binomial(n+t-1,t), exactly the same fixed-total multiset/weak-composition law used by ProbStack.

Theorem/problem:
random q-pebbling solvability on grids and a strong threshold for paths.

Probability law:
exactly the same uniform fixed-total law as ProbStack.

Asymptotic scale:
for paths their strong threshold has density of stretched-logarithmic type with square-root-log leading term and a minus one-half log-log correction. For q=2 this is the same leading and second-order shape as the ProbStack center in log-density coordinates. Their result is for solvability, not stackability, and the inspected source does not state ProbStack's additive constant log_2(3e).

Deterministic mechanism:
pebbling-weight necessary/sufficient conditions, central vertices, and local weighted regions.

Analytic mechanism:
the path sharpening counts partitions of powers of q into powers of q; it explicitly invokes the Mahler binary/q-ary partition asymptotic. The paper also proves a local fixed-total probability estimate for specified occupancies when the average density lambda grows with the graph size.

Overlap with ProbStack:
same path family, same probability law, same leading stretched-log scale, same minus-half-log-log shape, same broad power-of-two partition analytic family, and a directly relevant growing-density local-conditioning estimate.

Concrete difference:
different random event and different deterministic local certificate. ProbStack's proof uses exact TreeStack messages, deep deficit/front events, regeneration, opposing fronts, and the fixed additive constant log_2(3e).

Audit status:
one of the mathematically closest sources and mandatory comparison material.

### 4.3 David Moews — The pebbling threshold spectrum and paths

Primary source:
David Moews, "The pebbling threshold spectrum and paths", arXiv:1905.13730 (2019).
https://arxiv.org/abs/1905.13730

Exact model:
random pebbling solvability under the multiset model inherited from the threshold literature.

Theorem/problem:
among other results, obtains path pebbling threshold order

Theta(n * 2^{sqrt(log_2 n)} / sqrt(log_2 n)).

Probability law:
uniform multiset/fixed-total model.

Asymptotic scale:
the same first two visible density scales as the later sharp path work, but only order-level precision relative to ProbStack's fixed-offset statement.

Deterministic mechanism:
root solvability, not stacking the whole configuration to one root.

Overlap with ProbStack:
same graph family, probability model, and leading stretched-log density scale.

Concrete difference:
solvability event and coarser asymptotic precision.

Audit status:
close path-threshold precedent.

### 4.4 Earlier random-pebbling threshold lineage

Primary sources inspected:

- Andrzej Czygrinow, Nancy Eaton, Glenn Hurlbert, P. Mark Kayll, "On pebbling threshold functions for graph sequences", Discrete Mathematics 247 (2002), 93-105. DOI https://doi.org/10.1016/S0012-365X(01)00163-7.
- Airat Bekmetjev, Graham Brightwell, Andrzej Czygrinow, Glenn Hurlbert, "Thresholds for families of multisets, with an application to graph pebbling", Discrete Mathematics 269 (2003), 21-34. DOI https://doi.org/10.1016/S0012-365X(02)00745-8; arXiv:math/0406068.
- Adam Wierman, Julia Salzman, Michael Jablonski, Anant P. Godbole, "An improved upper bound for the pebbling threshold of the n-path", Discrete Mathematics 275 (2004), 367-373. DOI https://doi.org/10.1016/j.disc.2002.10.001.
- Andrzej Czygrinow and Glenn Hurlbert, "Girth, pebbling, and grid thresholds", SIAM Journal on Discrete Mathematics 20(1) (2006), 1-10. DOI https://doi.org/10.1137/S0895480102416374.
- Andrzej Czygrinow and Glenn Hurlbert, "On the pebbling threshold of paths and the pebbling threshold spectrum", Discrete Mathematics 308 (2008), 3297-3307. DOI https://doi.org/10.1016/j.disc.2007.06.045.

These papers establish that "random pebbling" has long meant random solvability in the uniform multiset model and that paths have been a central threshold example since the early literature. Bekmetjev et al. also place the model in a general multiset-threshold framework.

## 5. Weak compositions, conditioned geometrics, and occupancy literature

### 5.1 Exact iid-geometric conditioning representation is classical

A standard balls-in-boxes formulation uses weights w_k=1. In the notation surveyed by Svante Janson, this is the Bose-Einstein model in which allocations of a fixed total are equiprobable. Such an allocation can be represented as iid geometric variables conditioned on their sum.

Primary/major survey source:
Svante Janson, "Simply generated trees, conditioned Galton-Watson trees, random allocations and condensation", Probability Surveys 9 (2012), 103-252.
DOI https://doi.org/10.1214/11-PS188
arXiv https://arxiv.org/abs/1112.0510

Classical book trail:
V. F. Kolchin, B. A. Sevastyanov, V. P. Chistyakov, Random Allocations, 1978.

Consequence for ProbStack audit:
the fixed-total weak-composition = conditioned iid-geometric identity is a clearly classical ingredient. ProbStack should not present that identity as a project-specific probabilistic discovery.

### 5.2 Growing-density local conditioning

Bushaw-Kettle is particularly relevant because its Lemma 3 works directly in the same uniform fixed-total pebble space with density lambda growing, under support/mass hypotheses such as lambda=o(sqrt(N)), local support t=o(lambda), and local mass m=o(lambda^2). It derives asymptotic local probabilities of specified occupancies.

This is closer to Session 18 than generic finite-density equivalence-of-ensembles references. The exact hypotheses and event families differ from ProbStack's transfer arguments, so any eventual comparison should state both sets of assumptions rather than citing "equivalence of ensembles" generically.

### 5.3 Random-composition extremes and geometric samples

Primary sources inspected for terminology and nearby methods include:

- Paweł Hitczenko and Carla D. Savage, "On the multiplicity of parts in a random composition of a large integer", SIAM Journal on Discrete Mathematics 18(2) (2004), 418-435. DOI https://doi.org/10.1137/S0895480199363155.
- Paweł Hitczenko and Arnold Knopfmacher, "Gap-free compositions and gap-free samples of geometric random variables", Discrete Mathematics 294(3) (2005), 225-239. DOI https://doi.org/10.1016/j.disc.2005.02.008.
- Paweł Hitczenko and Guy Louchard, "Distinctness of compositions of an integer: A probabilistic analysis", Random Structures & Algorithms 19 (2001), 407-437. DOI https://doi.org/10.1002/rsa.10008.

These papers reinforce the standard connection between composition statistics and geometric random variables. The inspected sources do not give an exact random-stackability threshold generated by rare local multiscale patterns at the ProbStack growing density.

Audit classification:
classical background and methodology; no exact theorem match located.

## 6. Graph pebbling, cover pebbling, and stacking

### 6.1 Random pebbling law

The older threshold literature already uses the same fixed-total multiset law, so the eventual ProbStack paper must not contrast itself with random pebbling by saying random pebbling normally uses multinomial placement. That would be false.

A safe distinction is:

"Existing random-pebbling threshold work studies solvability under the same uniform multiset law; ProbStack studies the different stackability event."

### 6.2 Cover pebbling

Primary sources:

- Betsy Crull et al., "The Cover Pebbling Number of Graphs", Discrete Mathematics 296 (2005), 15-23. DOI https://doi.org/10.1016/j.disc.2005.03.009.
- Jonas Sjöstrand, "The Cover Pebbling Theorem", Electronic Journal of Combinatorics 12 (2005), N22. DOI https://doi.org/10.37236/1989; arXiv:math/0410129.
- Anant Godbole, Nathaniel Watson, Carl Yerger, "Threshold and Complexity Results for the Cover Pebbling Game", arXiv:math/0510394; later Discrete Mathematics 309 (2009), 3609-3624.

Cover pebbling is a separate target event. Sjöstrand's theorem makes "stacked initial configurations" extremal for a cover-demand problem, which creates a terminology risk but not an event equivalence.

### 6.3 General target framework

Glenn Hurlbert, "General graph pebbling", Discrete Applied Mathematics 161(9) (2013), 1221-1231.
DOI https://doi.org/10.1016/j.dam.2012.03.010.

This is relevant to situating reachability targets but does not turn stackability into ordinary root solvability.

## 7. Tree structural-certificate analogues

### 7.1 Target pebbling in trees

Matheus Adauto, Viktoriya Bardenova, Yunus Bidav, Glenn Hurlbert, "Target Pebbling in Trees", Discrete Mathematics 349(7) (2026), 115029.
DOI https://doi.org/10.1016/j.disc.2026.115029
arXiv:2504.10460.

This work gives polynomial-time structural methods for target pebbling numbers on trees, using path partitions and extremal target configurations.

Overlap:
tree pebbling, structural decomposition, target feasibility.

Difference:
it computes worst-case target pebbling numbers rather than an exact arbitrary-configuration stackability predicate. No inspected statement matches TreeStack's categorical branch-message/root-score recursion.

### 7.2 Weight-function/tree-strategy literature

Pebbling weight functions and tree strategies are established certificate methods for root solvability. Bushaw-Kettle uses a weight-function necessary/sufficient comparison on grids/paths, and later algorithmic work automates weight-function generation.

These are mathematical analogues of "structural certificates" in a broad sense but are not the same exact message algebra as TreeStack.

### 7.3 Csernák-Soukup tree formula

Csernák-Soukup's 2026 paper proposes a tree stacking-number formula in terms of distances, degrees, and leaves relative to a root, conditional on its Almost Stacked Hypothesis, with small-tree computational evidence.

That is close by event and graph family, but it concerns the worst-case number sufficient to make every configuration stackable. It does not replace the exact per-configuration TreeStack criterion.

Audit status for TreeStack-style messages:
no exact public-record counterpart located in the searched sources. This remains unresolved rather than a novelty claim; terminology and algorithmic literatures outside pebbling could still contain equivalent recurrences.

## 8. Binary partitions and dyadic counting

### 8.1 Classical sources

Primary sources inspected:

- Kurt Mahler, "On a Special Functional Equation", Journal of the London Mathematical Society s1-15 (1940), 115-123. DOI https://doi.org/10.1112/jlms/s1-15.2.115.
- N. G. de Bruijn, "On Mahler's partition problem", Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen 51(6) (1948), 659-669.
- W. B. Pennington, "On Mahler's Partition Problem", Annals of Mathematics 57(3) (1953), 531-546. DOI https://doi.org/10.2307/1969735.
- Vladimir Yu. Protasov, "Asymptotic behaviour of the partition function", Sbornik: Mathematics 191(3) (2000), 381-414. DOI https://doi.org/10.1070/SM2000v191n03ABEH000464.
- Vladimir Yu. Protasov, "On the Asymptotics of the Binary Partition Function", Mathematical Notes 76(1) (2004), 144-149. DOI https://doi.org/10.1023/B:MATN.0000036752.47140.98.
- Vladimir Yu. Protasov, "The Euler binary partition function and subdivision schemes", Mathematics of Computation 86 (2017), 1499-1524. DOI https://doi.org/10.1090/mcom/3128.

### 8.2 What is classical versus project-specific

Clearly classical:
the Mahler/de Bruijn asymptotic regime for partitions into powers of two, including the quadratic logarithmic main term, log-log structure, and bounded periodic correction/refinement framework.

Small deduction/specialization:
passing from published asymptotic formulas to the compact-uniform evaluation needed for arguments of the form lambda*2^L+O(1), for lambda restricted to a fixed compact interval, appears to be a specialization of classical estimates rather than a new binary-partition theorem. This should be checked line-by-line when preparing citations.

Project-specific application:
identifying the relevant truncated dyadic simplex arising from the ProbStack deficit recurrence and feeding the classical binary-partition estimates into the local stackability rare-event calculation.

Audit warning:
do not claim novelty for the binary-partition asymptotic itself.

## 9. Random recurrences, deficit/front analogues

Searches were made under random affine recursions, perpetuities, Lindley recurrences, random difference equations, rare excursions, ruin/barrier events, renewal/front propagation, and thin-tailed stochastic fixed points.

Representative primary sources inspected:

- Maria Vlasiou and Zbigniew Palmowski, "Tail asymptotics for a random sign Lindley recursion", Journal of Applied Probability 47(1) (2010), 72-83. DOI https://doi.org/10.1239/jap/1269610817.
- Paweł Hitczenko and Jacek Wesołowski, "Perpetuities with thin tails revisited", Annals of Applied Probability 19(6) (2009), 2080-2101. DOI https://doi.org/10.1214/09-AAP603.
- Charles M. Goldie and Rudolf Grübel, "Perpetuities with thin tails", Advances in Applied Probability 28(2) (1996), 463-480. DOI https://doi.org/10.1017/S0001867800048576.
- Bartosz Kołodziejek, "Logarithmic tails of sums of products of positive random variables bounded by one", Annals of Applied Probability 27(2) (2017), 1171-1189. arXiv:1510.01066.

These provide broad stochastic-recursion analogues and logarithmic-tail technology, but the searched sources did not yield an equivalent integer-valued recurrence with ProbStack's alternating contraction, low-phase dyadic deficit amplification, regeneration window, and irreversible two-sided front mechanism.

Classification:
background only / partially overlapping at the stochastic-recursion level.

## 10. Stretched-logarithmic thresholds

The strongest analogue is not an unrelated application: it is the path random-pebbling literature itself.

Moews:
threshold order n*2^{sqrt(log_2 n)}/sqrt(log_2 n).

Bushaw-Kettle:
strong path threshold with density of the form exp(sqrt(log q * log n) - (1/2) log log n + lower-order terms) for q-pebbling, with a sharper path analysis based on partitions into powers of q.

Thus an exp(sqrt(log n)) density and a minus-half-log-log correction are already established phenomena in random path pebbling under the same multiset law.

At a generic extreme-value level, tails whose logarithm is quadratic in log of the scale also invert at exp(const*sqrt(log n)); therefore the mere stretched-log scale should not be treated as distinctive by itself.

The comparison that matters is the event, deterministic mechanism, exact local rate, and fixed additive centering constant.

## 11. Model-comparison table

| Source/line | Same probability law | Same graph | Same event | Same deterministic certificate | Same binary-partition ingredient | Same threshold scale | Classification |
|---|---|---|---|---|---|---|---|
| Csernák-Soukup 2026 | No random law | Paths/trees included | Yes: stackable | No exact TreeStack match located | No | Deterministic worst case instead | Exact event; different probabilistic problem |
| Bushaw-Kettle 2025 | Yes | Yes, paths | No: solvability | No | Yes, powers-of-q partitions | Yes at leading/second-order shape | Closest asymptotic/probability-law analogue |
| Moews 2019 | Yes | Yes, paths | No: solvability | No | Indirectly related | Yes at order level | Close asymptotic analogue |
| Czygrinow et al. 2002 | Yes | Paths among families | No: solvability | No | No | Early bounds | Foundational random-pebbling background |
| Bekmetjev et al. 2003 | Yes | Paths among families | No: solvability | No | No | Early bounds | Multiset-threshold foundation |
| Czygrinow-Hurlbert 2008 | Yes | Yes | No: solvability | No | No exact match | Earlier path bounds | Close historical path work |
| Cover pebbling line | Sometimes same law in random variants | Various | No: cover demand | No | No | Different | Terminology/background |
| Janson allocations | Yes as Bose-Einstein model | Not graph-specific | Not pebbling | N/A | N/A | Not this threshold | Exact probability-model background |
| Mahler/de Bruijn/Protasov | N/A | N/A | N/A | N/A | Yes | Provides local count asymptotics | Classical analytic ingredient |
| Adauto et al. 2026 | Deterministic | Trees | Target reachability, not stackability | Structural but different | No | Worst-case target number | Tree-structural analogue |
| Perpetuity/Lindley line | Different | N/A | Different | Recurrence analogue only | No | Different | Background only |

## 12. Citation-network tracing

### 12.1 Random pebbling

Backward trail:
Czygrinow-Eaton-Hurlbert-Kayll (2002) -> Bekmetjev-Brightwell-Czygrinow-Hurlbert (2003) -> Wierman-Salzman-Jablonski-Godbole (2004), Czygrinow-Hurlbert (2006, 2008) -> Moews (2019) -> Bushaw-Kettle (arXiv 2023; journal 2025).

Bushaw-Kettle explicitly situates its grid/path results as improvements/generalizations of the earlier random-pebbling path/grid work and invokes Chung's classical deterministic q-pebbling work.

Forward trail:
public search found Bushaw-Kettle listed as a citing successor of the 2006 grid-threshold paper. Because Bushaw-Kettle was published only in 2025 and Csernák-Soukup appeared in 2026, forward citation coverage is necessarily immature. No later public paper was located that combines Bushaw-Kettle's random path model with Csernák-Soukup's stackability event.

### 12.2 Stackability

Backward trail from Csernák-Soukup:
standard graph pebbling, Hurlbert's general-target viewpoint, cover-pebbling results including Sjöstrand's theorem, and prior deterministic graph-pebbling literature.

Forward trail:
the 2026 paper is too recent for a stable citation network. Public-web searches did not reveal a substantive later random-stackability theorem. This remains unresolved because indexing lag is significant.

### 12.3 Binary partitions

Backward:
Mahler 1940 -> de Bruijn 1948.

Forward/refinement:
Pennington 1953 and later Protasov papers refine/revisit partition-function asymptotics. Bushaw-Kettle 2025 explicitly uses the powers-of-q partition asymptotic in random path pebbling, which makes this citation trail directly relevant to ProbStack rather than merely adjacent number theory.

### 12.4 Random allocations

Janson's survey consolidates the iid-conditioned allocation representation and points backward to the classical random-allocation literature including Kolchin-Sevastyanov-Chistyakov. Random-composition papers use closely related geometric-variable encodings.

## 13. Terminology risk

### "stackable"

Risk: low for event meaning, high for priority of terminology.
Csernák-Soukup 2026 uses "stackable" for the same deterministic event. The eventual paper should cite and align with that established public usage rather than present the word as project-specific.

### "stacking number"

Risk: high.
Csernák-Soukup uses stack(G) for the worst-case number of pebbles guaranteeing every configuration is stackable. ProbStack should avoid using "stacking number" for a random threshold quantity.

### "stacking theorem"

Risk: high.
Cover-pebbling literature uses stacking language for the extremal all-pebbles-at-one-vertex starting configuration. This is not ProbStack's event.

### "solvable"

Risk: high if conflated with stackable.
In graph pebbling, solvable means every root is individually reachable. The eventual paper should define the contrast explicitly.

### "random configuration"

Risk: high unless probability law is stated.
Use "uniform fixed-total multiset configuration", "uniform weak composition", or "Bose-Einstein allocation" at first occurrence. Do not imply classical random pebbling uses only independent labelled placement.

### "threshold"

Risk: medium/high.
Random-pebbling literature has an established monotone-family threshold vocabulary. ProbStack's finite stackability probability is not monotone in total mass. Prefer wording such as "high-density stackability transition" or "recovery transition" in expository text, and state the exact fixed-offset theorem when using "threshold".

### "recovery threshold"

Risk: medium.
No established graph-pebbling usage was located during this audit. If retained, define it explicitly rather than treating it as standard terminology.

### "weak composition" / "Bose-Einstein"

Risk: low.
Both are standard descriptors of the probability law and help disambiguate it from multinomial placement.

### "message", "deficit", "front"

Risk: medium.
These appear to be useful project terms for the deterministic mechanism, but this audit did not establish them as standard pebbling vocabulary. Define them locally and avoid suggesting that the same names occur in prior pebbling literature.

## 14. Conservative originality-status matrix

| Component | Audit status |
|---|---|
| Uniform weak composition / Bose-Einstein allocation | Clearly classical ingredient |
| iid geometric variables conditioned on their sum | Clearly classical ingredient |
| Multiset random-pebbling probability space | Clearly classical in graph pebbling |
| Random path pebbling threshold near n*2^{sqrt(log_2 n)}/sqrt(log_2 n) | Existing close prior art for a different event |
| Minus-half-log-log correction in random path pebbling | Existing close prior art for a different event |
| Binary/q-ary partition asymptotics | Clearly classical ingredient |
| Use of binary partitions in random path pebbling | Existing close prior art (Bushaw-Kettle) |
| Stackability event | Publicly studied explicitly by Csernák-Soukup 2026 |
| Worst-case stacking number on paths/trees | Publicly studied by Csernák-Soukup 2026 |
| Exact random stackability theorem under the uniform fixed-total law with ProbStack center | No exact public-record match located in searched sources |
| Exact TreeStack arbitrary-configuration message/root-score certificate outside the TreeStack project | No exact public-record match located in searched sources |
| Combination of exact stackability + weak-composition law + deficit/front mechanism + fixed-offset center | Classical and close ingredients combined in a way for which no exact public-record match was located |
| Forward citation coverage of 2025-2026 closest papers | Unresolved because the sources are recent and indexing is incomplete |
| MathSciNet/zbMATH exhaustive coverage | Unresolved; public search did not produce a reliable exhaustive index search |

None of these classifications establishes novelty, priority, originality, or publishability.

## 15. Reproducible search log

All searches below were run on 2026-09-28. Search systems actually used: public-web search, arXiv, publisher pages surfaced by public search (Elsevier/ScienceDirect, SIAM, EJC, AMS/MathComp metadata where available), university repositories/author-hosted copies, DBLP, and public bibliographic metadata. Search attempts restricted to public MathSciNet/zbMATH pages returned no useful indexed records and are recorded as incomplete coverage.

Each "record" below is a query batch executed for one audit question. Exact query strings are preserved.

### Record A — random pebbling/path threshold lineage

Queries:
- "Thresholds for Pebbling on Grids" Bushaw Kettle path strong threshold q-pebbling
- "pebbling threshold" path strong threshold Bushaw Kettle
- "On the pebbling threshold of paths and the pebbling threshold spectrum" PDF
- "The pebbling threshold spectrum and paths" Moews PDF
- "For q-pebbling on" "P_n" "strong threshold" Bushaw Kettle
- "Theorem 2" "Thresholds for Pebbling on Grids" path lambda
- "q-pebbling" paths "log log n" threshold
- "On pebbling threshold functions for graph sequences" pdf
- "Thresholds for families of multisets, with an application to graph pebbling" arxiv
- "An improved upper bound for pebbling threshold of the n-path" 2004 Godbole Jablonski Salzman Wierman
- "Girth Pebbling and Grid Thresholds" Czygrinow Hurlbert 2006
- "On the pebbling threshold of paths and the pebbling threshold spectrum" 2008 Czygrinow Hurlbert

Promising results:
Bushaw-Kettle 2025; Moews 2019; 2002/2003 foundational multiset papers; 2004/2006/2008 path/grid papers.

Inspected:
primary pages/preprints for all named sources, with substantial body text available for Bushaw-Kettle, Moews, Czygrinow et al. 2002, and Czygrinow-Hurlbert 2008.

Backward references followed:
Chung; Bekmetjev et al.; Wierman et al.; Czygrinow-Hurlbert.

Forward references followed:
Bushaw-Kettle as a later successor to older path/grid threshold work; no post-2025 exact stackability extension located.

Relevance:
very high, because the probability law is identical and the path scale is exceptionally close.

Unresolved:
full forward citation network after 2025; whether any 2026 preprint imports the Bushaw-Kettle machinery specifically for stackability.

### Record B — stacking/stackability terminology

Queries:
- "Stacking and Clearing in Graph Pebbling" Csernak Soukup arXiv
- "random" "stackable" "graph pebbling"
- "stackability" "graph pebbling" random
- "stackable" "uniform" pebbling configuration
- "stacking and clearing" random pebbling
- "stacking" pebbling threshold random configuration

Promising result:
Csernák-Soukup 2026.

Inspected:
arXiv abstract and full HTML/body, including definitions, path results, tree section, Almost Stacked Hypothesis, and conjectural tree formula.

Backward references followed:
cover pebbling, Hurlbert general targets, standard pebbling.

Forward references followed:
public searches; no substantive later random-stackability theorem found.

Relevance:
highest for exact event and terminology.

Unresolved:
forward citations due recency.

### Record C — tree certificates / target pebbling

Queries:
- "stackable" tree graph pebbling algorithm configuration tree dynamic programming
- "stacking" "tree" "pebbling" algorithm configuration
- "pebbling" tree "linear time" solvability configuration
- "pebbling" "trees" "solvability" algorithm configuration
- "graph pebbling" tree dynamic programming root solvable certificate
- "tree pebbling" weight function configuration solvable root
- "Target pebbling in trees" 2026 pebbling trees
- "Target Pebbling in Trees" algorithm polynomial dynamic tree partition formula
- "General graph pebbling" Hurlbert 2013 target family
- "The cover pebbling number of graphs" Crull 2005
- "The Cover Pebbling Theorem" Sjostrand stacking theorem cover pebbling 2005

Promising results:
Adauto-Bardenova-Bidav-Hurlbert 2026; Hurlbert 2013; Sjöstrand 2005; Csernák-Soukup tree section; weight-function literature.

Inspected:
publisher/arXiv records and available body excerpts.

Backward references followed:
Chung/path partitions; target and cover pebbling.

Relevance:
partial structural overlap.

Unresolved:
equivalent exact per-configuration tree dynamic programs may exist under algorithmic rather than pebbling terminology.

### Record D — weak compositions / conditioned geometrics

Queries:
- "uniform random weak composition" probability geometric conditioned on sum
- "weak compositions" "geometric" conditioned sum random
- "uniform composition" "conditioned geometric" random allocation
- "Bose-Einstein" random allocation geometric conditioned sum
- "balls-in-boxes" uniform allocation geometric conditioned sum Janson
- "local limit" "Bose-Einstein" random allocations
- "equivalence of ensembles" geometric variables conditioned on sum zero range
- "random allocation" conditioned i.i.d. geometric sum local limit theorem
- "uniform random weak composition" maximum part asymptotic
- "uniform weak compositions" longest run
- "random weak composition" "geometric" maximum
- "random compositions" fixed number of parts maximum part geometric conditioning
- "Bose-Einstein" maximum occupancy uniform compositions
- "random allocation" Bose Einstein maximum box occupancy
- "weak composition" rare pattern probability
- "Random Allocations" Kolchin Sevastyanov Chistyakov 1978 Bose Einstein
- "uniform random composition" fixed number of parts largest part Hitczenko Savage

Promising results:
Janson 2012; Kolchin-Sevastyanov-Chistyakov; Hitczenko-Savage; Hitczenko-Knopfmacher; Hitczenko-Louchard.

Inspected:
Janson full survey text/sections where publicly surfaced; primary bibliographic/abstract records for the random-composition papers; book metadata.

Backward references followed:
classical balls-in-boxes/random-allocation literature.

Forward references followed:
composition/geometric-sample literature.

Relevance:
high for probability-model identity; moderate for rare local events.

Unresolved:
a dedicated theorem for ProbStack-sized O(log n) rare local blocks at growing density might exist in occupancy/local-limit literature but was not located.

### Record E — Bose-Einstein versus Maxwell-Boltzmann in pebbling

Queries:
- "Threshold and Complexity Results for the Cover Pebbling Game" Bose Einstein Maxwell Boltzmann
- "Bose-Einstein" pebbling threshold configuration
- "Maxwell-Boltzmann" pebbling threshold

Promising result:
Godbole-Watson-Yerger cover-pebbling threshold work explicitly distinguishes both allocation models.

Relevance:
important terminology/probability-law control.

Unresolved:
none for the basic distinction.

### Record F — binary partitions

Queries:
- "On Mahler's partition problem" de Bruijn 1948 pdf
- "Mahler's partition problem" Protasov binary partitions asymptotic
- Protasov binary partitions Mahler partition problem asymptotics
- "binary partitions" Protasov asymptotic periodic
- "A000123" de Bruijn Protasov
- "partitions into powers of 2" asymptotic de Bruijn later refinements
- "Mahler partition" Pennington asymptotic powers of 2
- "On a special functional equation" Mahler 1940 partition problem pdf
- "On Mahler's partition problem" Pennington 1953 Annals
- "truncated binary partitions" asymptotic
- "Asymptotic behaviour of the partition function" Protasov 2000 binary partition
- "On the Asymptotics of the Binary Partition Function" Protasov 2004

Promising results:
Mahler 1940; de Bruijn 1948; Pennington 1953; Protasov 2000/2004/2017.

Inspected:
de Bruijn full primary PDF/page images; primary publisher/bibliographic records for the other sources.

Backward/forward trail:
Mahler -> de Bruijn -> Pennington/Protasov; Bushaw-Kettle is a graph-pebbling application of the same powers-of-q partition asymptotics.

Relevance:
very high for analytic ingredient, but classical.

Unresolved:
precise best citation for compact-uniform lambda*2^L+O(1) specialization and for any explicitly truncated variant exactly matching the ProbStack finite simplex.

### Record G — random recurrences / fronts

Queries:
- "random affine recursion" log squared tail perpetuity
- perpetuity "log^2" tail probability
- "perpetuity" "log^2 x" tail
- "random difference equation" "log squared" tail perpetuity
- "perpetuities" "lognormal" tail
- "thin-tailed perpetuities" log x log x
- "random affine recursion" "lognormal" stationary tail
- "iterated random functions" "logarithmic asymptotics" perpetuity
- "Lindley recursion" lognormal tail asymptotic
- "Perpetuities with thin tails revisited" authors
- "Perpetuities with thin tails" authors logarithmic tail
- "Logarithmic tails of sums of products of positive random variables bounded by one" authors

Promising results:
Vlasiou-Palmowski; Goldie-Grübel; Hitczenko-Wesołowski; Kołodziejek.

Relevance:
background stochastic-recursion analogues only.

Unresolved:
no exact alternating contraction/dyadic-deficit/front recurrence located.

### Record H — stretched-logarithmic thresholds

Queries:
- "exp(sqrt(log n))" threshold probability
- "sqrt(log n)" "log log n" threshold rare event
- "exp(sqrt(log n))" random structures threshold
- "2^{sqrt(log_2 n)}" probability threshold
- "2^sqrt(log n)" threshold combinatorics
- "log^2 x" rare event probability "threshold" random
- "-(log x)^2" probability tail threshold

Promising result:
the closest useful hits loop back to path random pebbling itself; generic lognormal/thin-tail examples share only the inversion pattern.

Relevance:
supports treating the scale as a general rare-event inversion phenomenon, not a standalone distinctive feature.

Unresolved:
none needed for the main comparison; unrelated examples are lower priority.

### Record I — public bibliographic-index coverage

Queries:
- site:zbmath.org "Stacking and Clearing in Graph Pebbling"
- site:zbmath.org "Thresholds for Pebbling on Grids"
- site:zbmath.org "The pebbling threshold spectrum and paths"
- site:zbmath.org "On Mahler's partition problem" de Bruijn
- site:mathscinet.ams.org "Thresholds for Pebbling on Grids"
- site:mathscinet.ams.org "Stacking and Clearing in Graph Pebbling"

Result:
no useful public search results surfaced.

Classification:
coverage unresolved. This is not evidence that the papers are absent from those databases.

Follow-up:
perform authenticated/direct MathSciNet and zbMATH searches if available in the next audit pass.

## 16. Primary-source inventory

Twenty-seven primary-source records were inspected at least at the abstract, publisher-metadata, preprint, or full-text level during the audit. Substantial body/full-text material was available for a smaller core including Csernák-Soukup, Bushaw-Kettle, Moews, Czygrinow et al. 2002, Czygrinow-Hurlbert 2008, Janson, de Bruijn, Sjöstrand, and the 2026 target-pebbling work.

Inventory:

1. Csernák-Soukup 2026, Stacking and clearing in graph pebbling.
2. Bushaw-Kettle 2025, Thresholds for pebbling on grids.
3. Moews 2019, The pebbling threshold spectrum and paths.
4. Czygrinow-Eaton-Hurlbert-Kayll 2002.
5. Bekmetjev-Brightwell-Czygrinow-Hurlbert 2003.
6. Wierman-Salzman-Jablonski-Godbole 2004.
7. Czygrinow-Hurlbert 2006.
8. Czygrinow-Hurlbert 2008.
9. Crull et al. 2005.
10. Sjöstrand 2005.
11. Godbole-Watson-Yerger 2009 / arXiv:math/0510394.
12. Hurlbert 2013.
13. Adauto-Bardenova-Bidav-Hurlbert 2026.
14. Janson 2012.
15. Hitczenko-Savage 2004.
16. Hitczenko-Knopfmacher 2005.
17. Hitczenko-Louchard 2001.
18. Mahler 1940.
19. de Bruijn 1948.
20. Pennington 1953.
21. Protasov 2000.
22. Protasov 2004.
23. Protasov 2017.
24. Vlasiou-Palmowski 2010.
25. Hitczenko-Wesołowski 2009.
26. Goldie-Grübel 1996.
27. Kołodziejek 2017.

The Kolchin-Sevastyanov-Chistyakov book was also inspected as a secondary/classical book trail rather than counted in the article inventory.

## 17. Unresolved follow-ups

1. Direct authenticated searches in MathSciNet and zbMATH for: stackable pebbling; random stacking pebbling; multiset pebbling path threshold; target pebbling trees; binary partition asymptotics.
2. Citation-index forward searches for Bushaw-Kettle 2025 and Csernák-Soukup 2026 after allowing for indexing lag.
3. Search dissertations/theses by authors in the random-pebbling path lineage and recent target/stacking authors.
4. Inspect every reference in Csernák-Soukup's tree section that bears on stackability, almost-stacked reductions, or cover-stacking.
5. Inspect Bushaw-Kettle's exact strong-path theorem and proof in a typeset/full PDF to record the constant-level comparison without relying on HTML math elision.
6. Determine the strongest published compact-uniform consequence of de Bruijn/Protasov for arguments lambda*2^L+O(1).
7. Search algorithmic tree-pebbling / chip-firing / resource-transfer dynamic programming for a recurrence equivalent to TreeStack messages despite different terminology.
8. Search non-English and older proceedings/theses for "stacking" or support-collapse pebbling problems before 2026.
9. Search the 2026 directed-stacking follow-up by Csernák-Soukup and any related preprints for probabilistic variants.
10. Verify whether any cover-pebbling threshold source treats a support-collapse event as an intermediate random variable.

## 18. Recommendation

The audit is sufficient to identify the main public-record collision risks and the closest sources, but it is not yet sufficient to close the originality audit.

A focused follow-up literature-audit session is warranted before standalone paper preparation, principally because:

- Csernák-Soukup 2026 is an exact event/terminology match and is very recent;
- Bushaw-Kettle 2025 is an unusually close same-law, same-path, same-stretched-log, same-binary-partition analogue for a different event;
- direct MathSciNet/zbMATH coverage was not obtained;
- forward citation networks for the 2025-2026 closest sources are immature;
- the compact-uniform binary-partition citation and possible equivalent tree dynamic programs deserve one more targeted pass.

The next audit should be narrower than this one: it should resolve those specific citation and equivalence questions rather than reopen the mathematics.

## 19. Explicit safeguards

- A negative search cannot establish novelty.
- No novelty, priority, originality, publication, or submission claim is made.
- The frozen theorem is unchanged.
- Session 17 was not reopened.
- EMPTY semantics are untouched.
- TreeStack/Mathlib/Lean dependency pins are untouched.
- Permanent CI is untouched.
- No Python or Lean mathematical code is changed by this audit.
