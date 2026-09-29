import Lake

open Lake DSL

package "probstack" where
  leanOptions := #[⟨`autoImplicit, false⟩]

require treestack from git
  "https://github.com/jfairfaxball-348/TreeStack-Structural-Certificates-for-Stacking-on-Trees.git" @
  "8fc9fc37a200855ec22579beaeec8f12f94f0310"

@[default_target]
lean_lib ProbStack

/-- Palomar's protected Mathlib-only statement surface. -/
lean_lib ProbStackPalomarChallenge where
  roots := #[`ProbStackPalomar.Challenge]

/-- Palomar's proved solution surface. -/
lean_lib ProbStackPalomarSolution where
  roots := #[`ProbStackPalomar.Solution]
