# ProbStack roadmap

## Stage 1 — complete: conjecture discovery and mathematical proof

The path theorem was frozen in Session 8 at fixed (O(1)) offsets. The target
center is

[
sqrt{log_2 n}
-rac12log_2log_2 n
+log_2(3e),
]

with probability tending to 0 below every fixed negative offset and to 1 above
every fixed positive offset. No zero-offset claim is made.

Do not reopen Stage 1 merely to obtain a critical-window law, finer (o(1))
centering, finite-(n) monotonicity, Poisson front processes, or other tree
families.

## Stage 2 — current: formalisation and complete verification

Session 9 fixed the formal dependency architecture. The authoritative plan is
`notes/session-9-formalisation-design.md`.

Session 18 has now assembled the complete mathematical proof of the frozen
path theorem, including the exact conditioning transfer and both global
fixed-offset directions. Session 19 is the theorem/formalisation/reproducibility
closure stage; it should not reopen the probabilistic discovery programme.

Immediate priorities:

1. pin and compile the exact TreeStack/Mathlib/Lean dependency boundary;
2. formalise deterministic path messages/fronts/regeneration;
3. formalise finite weak-composition and geometric conditioning;
4. formalise finite dyadic/binary-partition combinatorics;
5. discharge the isolated compact-uniform binary-partition (o(L))
   asymptotic;
6. assemble local and global asymptotics;
7. expose one small no-sorry headline theorem and run complete Lean CI.

Do not weaken the mathematical theorem to fit the prover. Keep mathematical
proof status, Python validation status, and Lean compilation status separate.

## Stage 3 — comprehensive public-record prior-art/originality audit

Only after complete formal verification, search well beyond arXiv:
MathSciNet/zbMATH where accessible, journals, Scholar-style citation trails,
graph-pebbling bibliographies, author pages, proceedings, theses, terminology
variants, cited/citing papers, and mathematically equivalent formulations.
Log search terms, dates, databases, and findings.

A negative public-record audit cannot rule out private, unpublished, or
unindexed work.

## Stage 4 — standalone paper

Write a self-contained article explaining the model, deterministic TreeStack
input, uniform weak-composition probability space, frozen theorem, proof,
formal verification, only mathematically useful experiments, and the
public-record literature audit. Do not oversell.

## Stage 5 — submission and packaging decisions

Only after the theorem is proved, formally verified, audited, and written as a
standalone paper should the project decide on arXiv, Palomar, journal
submission, or other packaging.

At that time, inspect the then-current specifications rather than reusing old
TreeStack packaging assumptions.
