module

public import ProbStack.PathMessage

public section

namespace ProbStack

def activeStep (m : Int) (x : Nat) : Int :=
  TreeStack.F (m + (x : Int))

def deficit (m : Int) : Int :=
  3 - m

theorem deficit_activeStep_of_low {m : Int} {x : Nat}
    (h : m + (x : Int) <= 1) :
    deficit (activeStep m x) = 2 * (deficit m - (x : Int)) := by
  unfold activeStep
  rw [TreeStack.F_of_le_one h]
  unfold deficit
  ring

theorem deficit_two_steps_of_low {m : Int} {x y : Nat}
    (h1 : m + (x : Int) <= 1)
    (h2 : activeStep m x + (y : Int) <= 1) :
    deficit (activeStep (activeStep m x) y) =
      4 * deficit m - 4 * (x : Int) - 2 * (y : Int) := by
  calc
    deficit (activeStep (activeStep m x) y) =
        2 * (deficit (activeStep m x) - (y : Int)) :=
      deficit_activeStep_of_low h2
    _ = 2 * (2 * (deficit m - (x : Int)) - (y : Int)) := by
      rw [deficit_activeStep_of_low h1]
    _ = 4 * deficit m - 4 * (x : Int) - 2 * (y : Int) := by
      ring


def activeScan (m : Int) : List Nat → Int
  | [] => m
  | x :: xs => activeScan (activeStep m x) xs

def LowRun (m : Int) : List Nat → Prop
  | [] => True
  | x :: xs =>
      m + (x : Int) <= 1 ∧ LowRun (activeStep m x) xs

def dyadicInputCost : List Nat → Int
  | [] => 0
  | x :: xs =>
      (2 : Int) ^ (xs.length + 1) * (x : Int) + dyadicInputCost xs

theorem deficit_activeScan_of_lowRun {m : Int} {xs : List Nat}
    (h : LowRun m xs) :
    deficit (activeScan m xs) =
      (2 : Int) ^ xs.length * deficit m - dyadicInputCost xs := by
  induction xs generalizing m with
  | nil =>
      simp [activeScan, dyadicInputCost]
  | cons x xs ih =>
      change
        m + (x : Int) <= 1 ∧ LowRun (activeStep m x) xs at h
      rcases h with ⟨hfirst, hrest⟩
      rw [activeScan, ih hrest, deficit_activeStep_of_low hfirst]
      simp only [dyadicInputCost, List.length_cons, pow_succ]
      ring

end ProbStack
