import ProbStack.PathMessage

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

end ProbStack
