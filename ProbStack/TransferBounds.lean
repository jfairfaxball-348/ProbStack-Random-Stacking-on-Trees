module

public import ProbStack.TreeStackBoundary

public section

namespace ProbStack

theorem F_le_half (x : Int) : TreeStack.F x <= x / 2 := by
  unfold TreeStack.F
  split_ifs <;> omega

theorem F_eq_half_of_ge_four_even {x : Int}
    (h4 : 4 <= x) (he : x % 2 = 0) :
    TreeStack.F x = x / 2 :=
  TreeStack.F_of_ge_four_even h4 he

theorem F_eq_shifted_half_of_ge_five_odd {x : Int}
    (h5 : 5 <= x) (ho : Ne (x % 2) 0) :
    TreeStack.F x = (x - 3) / 2 :=
  TreeStack.F_of_ge_five_odd h5 ho

theorem steering_input_window {mu M X : Int}
    (_hMlo : -mu < M) (_hMhi : M <= 2 * mu)
    (hXlo : 2 * mu + 2 - M <= X)
    (hXhi : X <= 4 * mu - M) :
    And (2 * mu + 2 <= M + X) (M + X <= 4 * mu) := by
  constructor <;> omega

theorem F_mem_mu_two_mu {mu y : Int}
    (_hmu : 1 <= mu)
    (hlo : 2 * mu + 2 <= y)
    (hhi : y <= 4 * mu) :
    And (mu <= TreeStack.F y) (TreeStack.F y <= 2 * mu) := by
  have hy4 : 4 <= y := by omega
  by_cases he : y % 2 = 0
  · rw [TreeStack.F_of_ge_four_even hy4 he]
    constructor
    · rw [Int.le_ediv_iff_mul_le (by norm_num : (0 : Int) < 2)]
      omega
    · apply Int.ediv_le_of_le_mul (by norm_num : (0 : Int) < 2)
      omega
  · have hy5 : 5 <= y := by omega
    rw [TreeStack.F_of_ge_five_odd hy5 he]
    constructor
    · rw [Int.le_ediv_iff_mul_le (by norm_num : (0 : Int) < 2)]
      omega
    · apply Int.ediv_le_of_le_mul (by norm_num : (0 : Int) < 2)
      omega

theorem regeneration_transfer_window {mu M X : Int}
    (hmu : 1 <= mu)
    (hMlo : -mu < M) (hMhi : M <= 2 * mu)
    (hXlo : 2 * mu + 2 - M <= X)
    (hXhi : X <= 4 * mu - M) :
    And (mu <= TreeStack.F (M + X)) (TreeStack.F (M + X) <= 2 * mu) := by
  have hwindow := steering_input_window hMlo hMhi hXlo hXhi
  exact F_mem_mu_two_mu hmu hwindow.1 hwindow.2

end ProbStack
