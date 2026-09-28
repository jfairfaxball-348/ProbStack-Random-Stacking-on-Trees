# Session 20 handover — public-record prior-art audit

## Repository boundary

Session 20 started from exact validated main:

d03b8381eb1b4cc100146cadbed3035c31c7016d

A dedicated branch was created directly from that SHA:

session-20-prior-art-audit

The authoritative audit document is:

notes/prior-art-audit.md

Its first committed audit version is:

7f2a8ba53fadceb5d3d35cc1ac7b1af24d08b138

The final branch SHA is reported in the external Session 20 end-of-session report because a committed handover cannot self-contain the SHA of the commit that contains itself.

No merge to main was performed in Session 20.

## Frozen project state

The theorem remains unchanged:

c_n = sqrt(log_2 n)
      - (1/2) log_2 log_2 n
      + log_2(3e).

For every fixed epsilon > 0, the same two eventual fixed-offset implications remain authoritative, with no theorem at epsilon = 0.

Session 17 was not reopened.

EMPTY remains categorical:

TreeStack.Message = Option Z
TreeStack.EMPTY = none

No identification of none with some 0 or any integer message was made.

Dependency pins remain unchanged:

- TreeStack: f4112f08d42a37c0941bf469ac124621b1f54f22
- Mathlib: 065356127b1dc0016f66b7283ce0ce2c4055aa55
- Lean: leanprover/lean4:v4.35.0-rc2

Permanent CI remains:

.github/workflows/lean-bootstrap.yml

No code, theorem, test, data, Lean, dependency, or workflow file was edited.

## Main audit findings

### 1. Exact event terminology already exists

Csernák and Soukup, "Stacking and clearing in graph pebbling" (arXiv:2604.22341, 2026), defines "stackable" by reachability of a configuration supported on one vertex. This matches the deterministic event studied by ProbStack.

Their principal object is the worst-case stacking number stack(G), not a random stackability probability. They prove stack(P_n)=2^n-1 and give tree results/conjectures, but the inspected paper does not state ProbStack's random weak-composition path theorem.

This is the strongest terminology/event precedent and must be cited explicitly in eventual paper preparation.

### 2. Classical random pebbling uses the same probability law

The random-pebbling threshold literature beginning at least with Czygrinow-Eaton-Hurlbert-Kayll and Bekmetjev-Brightwell-Czygrinow-Hurlbert uses uniform distributions of indistinguishable pebbles, equivalently uniform weak compositions / multisets.

Therefore the eventual paper must not say that prior random pebbling normally uses only multinomial labelled-pebble placement.

The distinguishing feature is the event: classical random pebbling asks for solvability, not support-collapse stackability.

### 3. Path random-pebbling thresholds are unusually close asymptotically

Moews gives path threshold order

n * 2^{sqrt(log_2 n)} / sqrt(log_2 n).

Bushaw and Kettle's 2025 strong path threshold has the same square-root-log leading scale and minus-one-half-log-log shape in density coordinates.

Bushaw-Kettle also uses partitions into powers of q and a same-law local fixed-total occupancy estimate at growing density.

This is the closest asymptotic/probability-law comparison found and requires a careful side-by-side treatment.

### 4. Conditioned geometric / weak-composition representation is classical

Janson's random-allocation survey and the classical balls-in-boxes literature identify the uniform fixed-total allocation as the Bose-Einstein/equiprobable model and relate it to iid geometric variables conditioned on their sum.

This is a classical ingredient, not a project-specific discovery.

### 5. Binary-partition asymptotics are classical

Mahler, de Bruijn, Pennington, and Protasov form the relevant analytic lineage. The quadratic logarithmic term, log-log structure, and bounded periodic correction framework are classical.

ProbStack's project-specific role is the application of these counts to its deterministic deficit/front event, not the binary-partition asymptotic itself.

### 6. No exact TreeStack-message analogue was located

Tree target-pebbling and weight-function literatures contain structural certificates and algorithms. Csernák-Soukup also develops a tree stacking-number formula conditional on an Almost Stacked Hypothesis.

No inspected public source supplied an exact arbitrary-configuration tree certificate equivalent to TreeStack's categorical Option-Z branch-message/root-score recursion.

This is only a "no match located" status and remains an unresolved search item.

### 7. Random-recurrence analogues are broad, not exact

Perpetuity, Lindley, and random affine-recursion papers provide tail/recurrence analogues, but no exact match to ProbStack's alternating contraction, dyadic deficit amplification, regeneration, and opposing irreversible fronts was located.

## Closest prior-art set

The current small set requiring mandatory comparison is:

1. Csernák-Soukup 2026 — exact stackability event/terminology; deterministic worst-case problem.
2. Bushaw-Kettle 2025 — same probability law, paths, strong stretched-log threshold, growing-density local conditioning, power-of-q partition counting; different event.
3. Moews 2019 — same law/path and threshold order; different event and coarser precision.
4. Czygrinow-Eaton-Hurlbert-Kayll 2002 and Bekmetjev-Brightwell-Czygrinow-Hurlbert 2003 — foundational multiset random-pebbling threshold framework.
5. Mahler/de Bruijn/Protasov — classical analytic source line for binary partitions.
6. Janson 2012 / classical random allocations — classical probability-model source line.

## Search systems used

Public sources actually searched/inspected included:

- arXiv;
- public web search;
- ScienceDirect / Elsevier article pages;
- SIAM article pages;
- Electronic Journal of Combinatorics;
- author-hosted and university-repository copies;
- DBLP;
- public bibliographic metadata and DOI records.

Public site-restricted searches aimed at MathSciNet and zbMATH did not surface usable results. No claim of exhaustive coverage of those databases is made.

## Primary-source count

The audit document records 27 primary-source article records inspected at least at abstract, metadata, preprint, or full-text level. A smaller core was inspected through substantial body/full-text material.

The audit distinguishes this level of access explicitly rather than treating all records as full-text inspections.

## Terminology risks

The eventual paper should:

- use "stackable" with a citation to Csernák-Soukup;
- avoid repurposing "stacking number";
- distinguish stackability from pebbling solvability;
- distinguish stackability from cover pebbling and the cover-pebbling "stacking" principle;
- state "uniform fixed-total multiset / weak-composition law" explicitly;
- avoid implying prior random pebbling is multinomial-only;
- be cautious with "threshold" because finite stackability probability is not monotone;
- define "recovery transition" or "recovery threshold" if such wording is retained.

## Conservative originality status

Clearly classical ingredients:
uniform weak compositions/Bose-Einstein allocations, conditioned iid geometric representation, multiset random-pebbling probability spaces, binary-partition asymptotics.

Close prior art requiring careful comparison:
Csernák-Soukup's stackability problem; Bushaw-Kettle and Moews path solvability thresholds.

No exact public-record match located in searched sources:
a random stackability theorem on paths under the uniform fixed-total law with the frozen ProbStack center; an external exact TreeStack-style arbitrary-configuration message/root-score certificate.

Unresolved:
authenticated MathSciNet/zbMATH coverage, recent forward citations, theses/proceedings, equivalent tree algorithms under different terminology, and the best compact-uniform binary-partition citation.

A negative search cannot establish novelty.

## Recommendation

Do not move directly to full paper preparation yet.

Run one narrower follow-up literature-audit session focused on:

1. direct MathSciNet/zbMATH searches where access permits;
2. forward citations of Bushaw-Kettle 2025 and Csernák-Soukup 2026;
3. full-PDF constant-level comparison with Bushaw-Kettle's strong path theorem;
4. Csernák-Soukup tree references and related/directed follow-ups;
5. equivalent tree dynamic programs under pebbling/chip-firing/resource-transfer terminology;
6. the strongest published compact-uniform de Bruijn/Protasov consequence actually needed by ProbStack;
7. relevant theses and proceedings.

If that targeted pass does not uncover a closer theorem, the project would then have a substantially firmer public-record basis for beginning standalone paper preparation while still avoiding any categorical novelty claim.

## Explicit closure statements

- No mathematical theorem was changed.
- Session 17 was not reopened.
- The frozen center was not modified.
- EMPTY semantics were untouched.
- Dependency pins were untouched.
- Permanent CI was untouched.
- No unnecessary code/Lean changes were made.
- No novelty, priority, originality, publication, or submission claim was made.
- A negative search is not treated as evidence of novelty.
