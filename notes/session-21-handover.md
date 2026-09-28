# Session 21 handover — targeted prior-art audit completion

Date: 2026-09-28

Status: targeted public-record audit completed. This handover records search and repository state only. It is not a novelty, priority, originality, publication or submission claim.

## Repository boundary

Validated Session 19 main remains:

d03b8381eb1b4cc100146cadbed3035c31c7016d

Session 20 starting branch tip:

2b7df6de75aac414a0db8808465ff877cfa3c467

Session 21 branch:

session-21-prior-art-audit-completion

The Session 21 branch was created directly from the Session 20 tip.

The Session 21 audit-content commit is:

dde6ecda8c59e98070fffe0de5c6fc90edb689f7

The final branch SHA is recorded in the external end-of-session report because a Git commit cannot self-contain its own SHA: changing the handover text to insert that SHA would itself change the SHA.

Merge status: unmerged. Main was not modified.

## Files changed in Session 21

Modified:

- notes/prior-art-audit.md

Added:

- notes/session-21-handover.md

No mathematical code, Python, Lean, test, data, dependency, or workflow file was changed.

The authoritative audit remains notes/prior-art-audit.md.

## Starting-state verification

The Session 20 tip has merge base exactly

d03b8381eb1b4cc100146cadbed3035c31c7016d

against main.

At Session 21 start it was:

- 2 commits ahead of main;
- 0 commits behind main.

Only the two Session 20 documentation files differed from Session 19 main.

## Databases and search systems actually used

Substantive/public search:

- arXiv;
- publisher pages, especially ScienceDirect/Elsevier;
- DBLP;
- author publication pages;
- university/thesis repositories;
- public web search;
- public DOI/bibliographic metadata;
- MaRDI-propagated bibliographic metadata where it exposed a zbMATH Open record.

Direct/database-native attempts:

- MathSciNet;
- zbMATH;
- Google Scholar;
- Semantic Scholar;
- Crossref.

Access limitations:

- direct MathSciNet exact-title searches were not accessible in this environment;
- direct zbMATH exact-title result pages were not accessible;
- Google Scholar citation access hit HTTP 429 rate limiting;
- Semantic Scholar direct/API access was unavailable;
- Crossref direct API access was unavailable.

These failures were recorded explicitly and were not silently replaced by ordinary web search. They are not evidence that a source is absent from a database.

## Important query families

The targeted pass used combinations including:

- stackable graph pebbling
- stacking graph pebbling
- random stackable pebbling
- random stacking pebbling
- pebbling threshold path
- multiset pebbling threshold
- uniform pebble configuration
- weak composition graph pebbling
- Bose Einstein pebbling
- support collapse pebbling
- all pebbles to one vertex
- gathering pebbling
- concentration pebbling
- coalescing pebbling
- target pebbling tree configuration algorithm
- pebbling dynamic programming tree
- tree pebbling message passing
- signed surplus deficit pebbling tree
- factor two resource flow tree
- exact titles/DOIs/arXiv IDs for Bushaw-Kettle, Csernák-Soukup and Adauto et al.

## Sources inspected in full or substantial body

The core sources read at substantial mathematical-body level include:

1. Neal Bushaw and Nathan Kettle, “Thresholds for pebbling on grids,” 2025 / arXiv:2309.01762.
2. Tamás Csernák and Lajos Soukup, “Stacking and clearing in graph pebbling,” arXiv:2604.22341.
3. Csernák and Soukup, “Stacking and Clearing in Directed Graph Pebbling,” arXiv:2606.04659, for continuation/status.
4. Jonas Sjöstrand, “The Cover Pebbling Theorem,” 2005.
5. Nathaniel Watson, “The Complexity of Pebbling and Cover Pebbling,” arXiv:math/0503511.
6. Svante Janson, “Simply generated trees, conditioned Galton-Watson trees, random allocations and condensation,” 2012.
7. N. G. de Bruijn, “On Mahler’s partition problem,” 1948.
8. Matheus Adauto, Viktoriya Bardenova, Yunus Bidav and Glenn Hurlbert, “Target Pebbling in Trees,” 2026, through preprint/author material.
9. the already-inspected Moews and classical random-pebbling lineage carried forward from Session 20.

## Sources inspected at metadata, abstract, author-page or searchable-text level

The supplementary pass included:

- David Moews author/publication pages and alternate historical titles;
- Glenn Hurlbert publication/proceedings listings and the 2023 seminar listing;
- Neal Bushaw author/publication page;
- Carl Yerger, “Extensions of Graph Pebbling” thesis;
- Jerad Scott DeVries, “Pebbling of Oriented Graphs” thesis;
- Haynes-Keaton, “Cover rubbling and stacking”;
- DBLP records for the relevant journal papers;
- direct-index search pages where access succeeded only at metadata level.

## Bushaw-Kettle exact comparison

Their random law is exactly the uniform fixed-total multiset / weak-composition law used by ProbStack.

Their event is different: q-pebbling solvability requires one pebble to be deliverable to each prescribed root, potentially by different sequences. It does not require support collapse.

Their sharp path theorem is:

P_{1/2}(P_n)
=
n exp(
  sqrt(log q log n)
  - (1/2) log log n
  + o(1)
).

For q=2, writing N=log_2 n and lambda_n=P_{1/2}(P_n)/n gives

log_2 lambda_n
=
sqrt(N)
-
(1/2) log_2 N
-
(1/2) log_2(log 2)
+
o(1).

Thus the first two scales match ProbStack’s frozen center, but their fixed additive constant is -1/2 log_2(log 2), not log_2(3e), and their event is solvability rather than stackability.

Their Lemma 3 is a growing-density local point-occupancy estimate with representative conditions

lambda=o(sqrt N), t=o(lambda), m=o(lambda^2).

ProbStack Session 18 instead uses an exact finite likelihood-ratio bound uniform over capped local event classes.

## Csernák-Soukup exact comparison

Their definitions match the deterministic ProbStack event:

- stacked = support size one;
- stackable = a stacked configuration is reachable;
- stack(G) = worst-case size threshold guaranteeing stackability.

They prove stack(P_n)=2^n-1 by a lower-bound family c_n^m controlled by valuation/imbalance/induction and an endpoint-elimination induction for the upper bound.

They relate stack(G) to the ordinary pebbling number, introduce the Almost Stacked Hypothesis motivated by Sjöstrand’s cover pebbling theorem, and conjecture a distance/degree formula for tree stacking numbers. Their computations cover trees/ASH through seven vertices.

They do not provide a random fixed-total stackability transition or a TreeStack arbitrary-configuration branch-message criterion.

The exact support-collapse terminology is therefore a mandatory citation precedent.

## Backward and forward trails

Backward:

- Csernák-Soukup -> Hurlbert target framework;
- Csernák-Soukup -> Sjöstrand cover-pebbling stacking principle;
- cover/rubbling “stacking number” terminology -> Haynes-Keaton;
- thesis/proceedings/author-page trails -> DeVries, Yerger, Moews, Hurlbert.

These uses do not collapse the distinction between initially concentrated cover-pebbling configurations and the final support-collapse event.

Forward:

- Csernák-Soukup’s directed-paper continuation was located;
- no reliable independent forward-citing item bearing on random stackability was found for the 2026 papers;
- public citation counts for Bushaw-Kettle were incomplete/inconsistent across accessible surfaces;
- indexing lag is explicitly material because the closest papers are from 2025-2026.

Forward-citation checks should be rerun immediately before submission/public posting.

## Tree-certificate search conclusion

Watson 2005 supplies the closest recurrence precedent located: on a tree cover-demand instance, leaf surplus is halved before transfer and leaf deficit is doubled before transfer, with equivalence of the reduced and original cover-solvability instances.

This is mathematically close to signed factor-two resource propagation but differs in event, target semantics, leftovers, and TreeStack’s categorical branch-message semantics.

Final required search-status wording:

no exact public-record match located in the searched sources

for an arbitrary-configuration support-collapse criterion equivalent to

StackableAt(T,C,r) iff 0 < score(T,C,r)

with recursively computed branch messages.

This is not a novelty claim.

## Binary-partition citation conclusion

Use de Bruijn 1948, especially equations (1.3)-(1.4), as the primary direct source for the unrestricted partitions-into-powers asymptotic.

For B=lambda 2^L+O(1) with lambda in a fixed compact positive interval:

- the de Bruijn theorem is published literature;
- specialization to binary partitions is immediate;
- compact-uniform substitution is a small uniformity deduction;
- the truncation comparison and deficit/front application are project-specific uses.

Protasov remains useful supplementary context. No new binary-partition theorem is claimed.

## Conditioning-literature conclusion

Janson/random-allocation literature supplies the classical exact model identity:

uniform weak composition = iid geometric allocation conditioned on the total.

Bushaw-Kettle supply a directly relevant growing-density local specified-vector asymptotic.

ProbStack Session 18’s exact finite capped-event likelihood-ratio estimate is best described as a short project-specific deduction from the exact fixed-total/product formulas. It should not be advertised as a new general allocation theorem.

## Terminology recommendation

Preferred:

- random stackability;
- stackability probability;
- high-density stackability transition;
- fixed-offset high-density stackability transition.

Use “stackable” with a Csernák-Soukup citation.

Avoid reusing “stacking number” for a random quantity.

Do not make unqualified “stackability threshold” the primary term, because the finite stackability probability is not being treated as an upward-monotone threshold family.

Avoid “recovery transition” as the principal public term because it obscures established pebbling terminology.

## Conservative classification

Classical:

- weak compositions/Bose-Einstein allocations;
- conditioned geometrics;
- uniform multiset random pebbling;
- binary/power partition asymptotics.

Exact event precedent with a different question:

- Csernák-Soukup deterministic stackability/stack(G).

Same random law/path and close asymptotic structure with a different event:

- Bushaw-Kettle;
- Moews and the classical path-threshold lineage.

Close mechanism precedents:

- powers-of-q partitions;
- local fixed-total occupancy conditioning;
- Watson signed halve/double tree recurrence.

No exact public-record match located in searched sources:

- random fixed-total support-collapse stackability theorem on paths;
- TreeStack-equivalent arbitrary-configuration branch certificate.

Unresolved because of access/indexing limitations:

- direct authenticated MathSciNet/zbMATH coverage;
- stable recent forward-citation networks.

Negative search does not establish novelty.

## Roadmap decision

YES — the public-record audit is sufficiently mature to begin standalone paper preparation, while continuing to avoid categorical novelty claims.

The closest collision risks are now explicit and citable, and the remaining gaps are ordinary citation-maintenance items rather than reasons for another broad audit.

The next stage should be STANDALONE PAPER PREPARATION using the frozen theorem and a carefully sourced related-work section.

## Frozen-state confirmations

- The theorem is unchanged.
- The center remains sqrt(log_2 n) - (1/2) log_2 log_2 n + log_2(3e).
- There is no epsilon=0 theorem.
- Session 17 was not reopened.
- EMPTY remains categorical.
- TreeStack.Message remains Option Z and EMPTY remains none.
- TreeStack, Mathlib and Lean pins are unchanged.
- Permanent CI remains .github/workflows/lean-bootstrap.yml.
- No Python, Lean, theorem-code, test, data or workflow file was changed.
- No novelty, priority, originality, publication or submission claim was made.
