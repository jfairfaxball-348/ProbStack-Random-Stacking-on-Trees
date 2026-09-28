import ProbStack.FiniteProbability

namespace ProbStack

/--
Natural-number form of the Session-14 affine input cost. For
`[x₁, ..., xₖ]` this is `x₁ + 2 x₂ + ... + 2^(k-1) xₖ`.
-/
def dyadicInputCost : List Nat → Nat
  | [] => 0
  | x :: xs => x + 2 * dyadicInputCost xs

/--
The same dyadic weights read in reverse order. For `[x₁, ..., xₖ]` this is
`2^(k-1) x₁ + ... + 2 x_{k-1} + xₖ`.
-/
def reverseDyadicInputCost : List Nat → Nat
  | [] => 0
  | x :: xs => 2 ^ xs.length * x + reverseDyadicInputCost xs

@[simp] theorem affineInputCost_eq_dyadicInputCost (xs : List Nat) :
    affineInputCost xs = (dyadicInputCost xs : Int) := by
  induction xs with
  | nil =>
      simp [affineInputCost, dyadicInputCost]
  | cons x xs ih =>
      simp [affineInputCost, dyadicInputCost, ih]

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
theorem positiveDescentEvent_iff_dyadicInputCost_le
    (mu : Nat) (xs : List Nat) :
    PositiveDescentEvent mu xs ↔
      (dyadicInputCost xs : Int) <=
        positiveDescentBudgetInt mu xs.length := by
  rw [← affineInputCost_eq_dyadicInputCost]
  unfold PositiveDescentEvent positiveDescentBudgetInt
  omega

/--
Given an admissible dyadic-simplex vector of budget `B`, prepend the unique
number of unit parts that turns its doubled weighted mass into exactly `2B`.
This is the finite bridge from ordered dyadic vectors to truncated binary
partitions.
-/
def binaryPartitionEncoding (B : Nat) (xs : List Nat) : List Nat :=
  2 * (B - dyadicInputCost xs) :: xs

/--
The binary-partition encoding has exact dyadic mass `2B`. Interpreting list
coordinate `j` as the multiplicity of the part `2^j`, this says that vectors
with cost at most `B` map to partitions of `2B` using parts no larger than one
dyadic level above the original vector.
-/
theorem binaryPartitionEncoding_cost
    {B : Nat} {xs : List Nat}
    (hcost : dyadicInputCost xs <= B) :
    dyadicInputCost (binaryPartitionEncoding B xs) = 2 * B := by
  simp [binaryPartitionEncoding, dyadicInputCost]
  omega

/--
Conversely, if a multiplicity vector `ones :: xs` has exact dyadic mass `2B`,
then its tail is an admissible ordered dyadic-simplex vector of budget `B`.
-/
theorem binaryPartition_tail_le
    {B ones : Nat} {xs : List Nat}
    (hmass : dyadicInputCost (ones :: xs) = 2 * B) :
    dyadicInputCost xs <= B := by
  simp [dyadicInputCost] at hmass
  omega

/--
The number of unit parts in the converse direction is forced uniquely. This
completes the finite bijective identity behind
`N_{k,B} = [z^(2B)] ∏_{j=0}^k (1-z^(2^j))⁻¹` without introducing polynomial
machinery into the Lean development.
-/
theorem binaryPartition_head_eq_slack
    {B ones : Nat} {xs : List Nat}
    (hmass : dyadicInputCost (ones :: xs) = 2 * B) :
    ones = 2 * (B - dyadicInputCost xs) := by
  simp [dyadicInputCost] at hmass
  omega

/--
Closed form for the Session-14 recursive low-phase certified deficit.
-/
theorem lowBudgetFinal_closed_form (D : Int) (xs : List Nat) :
    lowBudgetFinal D xs =
      (2 : Int) ^ xs.length * D -
        2 * (reverseDyadicInputCost xs : Int) := by
  induction xs generalizing D with
  | nil =>
      simp [lowBudgetFinal, reverseDyadicInputCost]
  | cons x xs ih =>
      simp only [lowBudgetFinal]
      rw [ih]
      simp only [List.length_cons, reverseDyadicInputCost, pow_succ]
      push_cast
      ring

/--
Finite reversed-simplex predicate. Written without `k-1`, it is valid even
for the empty block. For a nonempty block of length `k` it is equivalent to
`reverseDyadicInputCost xs <= (D-2) * 2^(k-1)`.
-/
def LowPhaseSimplex (D : Int) (xs : List Nat) : Prop :=
  2 * (reverseDyadicInputCost xs : Int) <=
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
      2 * (reverseDyadicInputCost xs : Int) <=
        (2 : Int) ^ xs.length * D -
          2 * (2 : Int) ^ xs.length := by
    calc
      2 * (reverseDyadicInputCost xs : Int) <=
          (2 : Int) ^ xs.length * (D - 2) := h
      _ = (2 : Int) ^ xs.length * D -
          2 * (2 : Int) ^ xs.length := by ring
  rw [pow_succ]
  linarith

end ProbStack
