import Lake

open Lake DSL

package "probstack" where
  leanOptions := #[⟨`autoImplicit, false⟩]

require treestack from git
  "https://github.com/jfairfaxball-348/TreeStack-Structural-Certificates-for-Stacking-on-Trees.git" @
  "f4112f08d42a37c0941bf469ac124621b1f54f22"

@[default_target]
lean_lib ProbStack

/-- Palomar's protected Mathlib-only statement surface. -/
lean_lib Challenge where
  roots := #[`Challenge]

/-- Palomar's proved solution surface. -/
lean_lib Solution where
  roots := #[`Solution]
