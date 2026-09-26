import ProbStack.TreeStackBoundary

namespace ProbStack

def pathStep (m : TreeStack.Message) (x : Nat) : TreeStack.Message :=
  match m with
  | none =>
      if x = 0 then TreeStack.EMPTY
      else some (TreeStack.F (x : Int))
  | some z => some (TreeStack.F (z + (x : Int)))

@[simp] theorem pathStep_empty_zero :
    pathStep TreeStack.EMPTY 0 = TreeStack.EMPTY := by
  simp [pathStep, TreeStack.EMPTY]

theorem pathStep_empty_pos {x : Nat} (hx : 0 < x) :
    pathStep TreeStack.EMPTY x = some (TreeStack.F (x : Int)) := by
  have hne : Ne x 0 := Nat.ne_of_gt hx
  simp [pathStep, TreeStack.EMPTY, hne]

@[simp] theorem pathStep_some (m : Int) (x : Nat) :
    pathStep (some m) x = some (TreeStack.F (m + (x : Int))) := by
  simp [pathStep]


theorem pathStep_eq_empty_iff (m : TreeStack.Message) (x : Nat) :
    pathStep m x = TreeStack.EMPTY ↔
      m = TreeStack.EMPTY ∧ x = 0 := by
  cases m with
  | none =>
      by_cases hx : x = 0
      · simp [pathStep, TreeStack.EMPTY, hx]
      · simp [pathStep, TreeStack.EMPTY, hx]
  | some z =>
      simp [pathStep, TreeStack.EMPTY]

end ProbStack
