import ProbStack.FiniteProbability

namespace ProbStack

/--
Natural-number forward dyadic cost. For `[x₁, ..., xₖ]` this is
`x₁ + 2 x₂ + ... + 2^(k-1) xₖ`.

This is deliberately named separately from the existing `dyadicInputCost` in
`ProbStack.Deficit`, whose weights run in the opposite direction and include
the factor two natural in the deficit identity.
-/
def forwardDyadicInputCost : List Nat → Nat
  | [] => 0
  | x :: xs => x + 2 * forwardDyadicInputCost xs

@[simp] theorem affineInputCost_eq_forwardDyadicInputCost (xs : List Nat) :
    affineInputCost xs = (forwardDyadicInputCost xs : Int) := by
  induction xs with
  | nil =>
      simp [affineInputCost, forwardDyadicInputCost]
  | cons x xs ih =>
      simp [affineInputCost, forwardDyadicInputCost, ih]

/--
The integer budget exactly equivalent to the strict Session-14 positive
descent inequality on a block of length `k`.
-/
def positiveDescentBudgetInt (mu k : Nat) : Int :=
  (2 : Int) ^ k - 2 * (mu : Int) - 1

/--
No off-by-one is hidden in `PositiveDescentEvent`: because all quantities are
integers, its strict inequality is exactly a weak dyadic-simplex inequality
with budget `2^k - 2*mu - 1`.
-/
theorem positiveDescentEvent_iff_forwardDyadicInputCost_le
    (mu : Nat) (xs : List Nat) :
    PositiveDescentEvent mu xs ↔
      (forwardDyadicInputCost xs : Int) <=
        positiveDescentBudgetInt mu xs.length := by
  rw [← affineInputCost_eq_forwardDyadicInputCost]
  unfold PositiveDescentEvent positiveDescentBudgetInt
  omega

/--
Given an admissible forward dyadic-simplex vector of budget `B`, prepend the
unique number of unit parts that turns its doubled weighted mass into exactly
`2B`. This is the finite bridge from ordered dyadic vectors to truncated
binary partitions.
-/
def binaryPartitionEncoding (B : Nat) (xs : List Nat) : List Nat :=
  2 * (B - forwardDyadicInputCost xs) :: xs

/--
The binary-partition encoding has exact dyadic mass `2B`. Interpreting list
coordinate `j` as the multiplicity of the part `2^j`, vectors of forward
cost at most `B` map to partitions of `2B` using one additional dyadic
level.
-/
theorem binaryPartitionEncoding_cost
    {B : Nat} {xs : List Nat}
    (hcost : forwardDyadicInputCost xs <= B) :
    forwardDyadicInputCost (binaryPartitionEncoding B xs) = 2 * B := by
  simp [binaryPartitionEncoding, forwardDyadicInputCost]
  omega

/--
Conversely, if a multiplicity vector `ones :: xs` has exact forward dyadic
mass `2B`, then its tail is an admissible ordered dyadic-simplex vector of
budget `B`.
-/
theorem binaryPartition_tail_le
    {B ones : Nat} {xs : List Nat}
    (hmass : forwardDyadicInputCost (ones :: xs) = 2 * B) :
    forwardDyadicInputCost xs <= B := by
  simp [forwardDyadicInputCost] at hmass
  omega

/--
The number of unit parts in the converse direction is forced uniquely. This
completes the multiplicity-vector bijection behind
`N_{k,B} = [z^(2B)] ∏_{j=0}^k (1-z^(2^j))⁻¹`.
-/
theorem binaryPartition_head_eq_slack
    {B ones : Nat} {xs : List Nat}
    (hmass : forwardDyadicInputCost (ones :: xs) = 2 * B) :
    ones = 2 * (B - forwardDyadicInputCost xs) := by
  have htail : forwardDyadicInputCost xs <= B :=
    binaryPartition_tail_le hmass
  simp [forwardDyadicInputCost] at hmass
  omega

/--
Closed form for the Session-14 recursive low-phase certified deficit. The
existing `dyadicInputCost` is exactly twice the reversed dyadic occupancy
cost required by this recurrence.
-/
theorem lowBudgetFinal_closed_form (D : Int) (xs : List Nat) :
    lowBudgetFinal D xs =
      (2 : Int) ^ xs.length * D - dyadicInputCost xs := by
  induction xs generalizing D with
  | nil =>
      simp [lowBudgetFinal, dyadicInputCost]
  | cons x xs ih =>
      simp only [lowBudgetFinal]
      rw [ih]
      simp only [List.length_cons, dyadicInputCost, pow_succ]
      ring

/--
Finite reversed-simplex predicate in the existing deficit-weight convention.
For a nonempty length-`k` block it is equivalent to
`sum_j 2^(k-j) x_j <= (D-2) 2^(k-1)`.
-/
def LowPhaseSimplex (D : Int) (xs : List Nat) : Prop :=
  dyadicInputCost xs <=
    (2 : Int) ^ xs.length * (D - 2)

/--
Every low-phase simplex vector has the advertised final-deficit lower bound.
For `D=3` this is the Session-6 amplification simplex and yields final deficit
at least `2^(k+1)`.
-/
theorem lowPhaseSimplex_final_ge
    {D : Int} {xs : List Nat}
    (h : LowPhaseSimplex D xs) :
    (2 : Int) ^ (xs.length + 1) <= lowBudgetFinal D xs := by
  rw [lowBudgetFinal_closed_form]
  unfold LowPhaseSimplex at h
  have h' :
      dyadicInputCost xs <=
        (2 : Int) ^ xs.length * D -
          2 * (2 : Int) ^ xs.length := by
    calc
      dyadicInputCost xs <=
          (2 : Int) ^ xs.length * (D - 2) := h
      _ = (2 : Int) ^ xs.length * D -
          2 * (2 : Int) ^ xs.length := by ring
  rw [pow_succ]
  linarith

end ProbStack
