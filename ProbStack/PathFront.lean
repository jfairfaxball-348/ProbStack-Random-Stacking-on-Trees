import ProbStack.PathDeep

namespace ProbStack

/-- Exact deterministic deficit threshold after one runaway step.  The input
cap is `X ≤ D / 4`, with integer division, so this definition records the
floor convention used by the finite cylinder event. -/
def runawayNext (D : Int) : Int :=
  2 * (D - D / 4)

/-- Certified deficit threshold after `k` runaway coordinates. -/
def runawayDeficit : Int → Nat → Int
  | D, 0 => D
  | D, k + 1 => runawayDeficit (runawayNext D) k

/-- Explicit finite coordinate caps for a runaway block.  At each coordinate
`X`, the required cap is the integer floor `D / 4` of the current certified
deficit threshold; the next threshold is `runawayNext D`. -/
def RunawayCaps : Int → List Nat → Prop
  | _, [] => True
  | D, x :: xs => (x : Int) ≤ D / 4 ∧ RunawayCaps (runawayNext D) xs

@[simp] theorem runawayDeficit_zero (D : Int) :
    runawayDeficit D 0 = D := rfl

@[simp] theorem runawayDeficit_succ (D : Int) (k : Nat) :
    runawayDeficit D (k + 1) = runawayDeficit (runawayNext D) k := rfl

@[simp] theorem RunawayCaps_nil (D : Int) : RunawayCaps D [] := trivial

@[simp] theorem RunawayCaps_cons {D : Int} {x : Nat} {xs : List Nat} :
    RunawayCaps D (x :: xs) ↔
      (x : Int) ≤ D / 4 ∧ RunawayCaps (runawayNext D) xs := by
  rfl

theorem runawayNext_growth {D : Int} (hD : 0 ≤ D) :
    3 * D ≤ 2 * runawayNext D := by
  have hfloor : (D / 4) * 4 ≤ D := by
    rw [← Int.le_ediv_iff_mul_le (by norm_num : (0 : Int) < 4)]
  unfold runawayNext
  omega

theorem runawayNext_ge {D : Int} (hD : 0 ≤ D) : D ≤ runawayNext D := by
  have h := runawayNext_growth hD
  omega

theorem runawayNext_ge_four {D : Int} (hD : 4 ≤ D) :
    4 ≤ runawayNext D := by
  exact le_trans hD (runawayNext_ge (by omega))

/-- One exact scalar runaway step.  A certified deficit `D ≥ 4`, together
with the floor cap `X ≤ D/4`, keeps the transfer in the low phase and raises
the certified deficit to `runawayNext D`. -/
theorem deficit_activeStep_ge_runawayNext
    {m D : Int} {x : Nat}
    (hD : 4 ≤ D)
    (hdeep : D ≤ deficit m)
    (hcap : (x : Int) ≤ D / 4) :
    m + (x : Int) ≤ 1 ∧ runawayNext D ≤ deficit (activeStep m x) := by
  have hcap4 : (x : Int) * 4 ≤ D := by
    exact (Int.le_ediv_iff_mul_le (by norm_num : (0 : Int) < 4)).1 hcap
  have hlow : m + (x : Int) ≤ 1 := by
    unfold deficit at hdeep
    omega
  constructor
  · exact hlow
  · rw [deficit_activeStep_of_low hlow]
    unfold runawayNext
    omega

/-- Iterated finite runaway certificate.  The conclusion simultaneously
records that every step was genuinely low-phase and that the final deficit
meets the exact recursively certified threshold. -/
theorem lowRun_and_deficit_ge_of_runawayCaps
    {m D : Int} {xs : List Nat}
    (hD : 4 ≤ D)
    (hdeep : D ≤ deficit m)
    (hcaps : RunawayCaps D xs) :
    LowRun m xs ∧ runawayDeficit D xs.length ≤ deficit (activeScan m xs) := by
  induction xs generalizing m D with
  | nil =>
      simp [LowRun, activeScan, runawayDeficit]
      exact hdeep
  | cons x xs ih =>
      rcases hcaps with ⟨hcap, hrest⟩
      have hstep := deficit_activeStep_ge_runawayNext hD hdeep hcap
      have hnextD : 4 ≤ runawayNext D := runawayNext_ge_four hD
      have htail := ih hnextD hstep.2 hrest
      constructor
      · exact ⟨hstep.1, htail.1⟩
      · simpa [activeScan, runawayDeficit] using htail.2

/-- A message is a certified irreversible front relative to a remaining mass
budget `T` when its deficit dominates that budget by the exact `+3` margin. -/
def CertifiedFront (T m : Int) : Prop :=
  T + 3 ≤ deficit m

/-- Deficit domination by the total mass of an explicit continuation forces
the whole continuation to stay in the low phase and preserves the domination
invariant at its end. -/
theorem lowRun_and_front_of_mass_domination
    {m : Int} {xs : List Nat}
    (hfront : (xs.sum : Int) + 3 ≤ deficit m) :
    LowRun m xs ∧ 3 ≤ deficit (activeScan m xs) := by
  induction xs generalizing m with
  | nil =>
      simp [LowRun, activeScan] at *
  | cons x xs ih =>
      have hlow : m + (x : Int) ≤ 1 := by
        unfold deficit at hfront
        simp only [List.sum_cons, Nat.cast_add, Nat.cast_ofNat] at hfront
        omega
      have hnext : (xs.sum : Int) + 3 ≤ deficit (activeStep m x) := by
        rw [deficit_activeStep_of_low hlow]
        simp only [List.sum_cons, Nat.cast_add, Nat.cast_ofNat] at hfront
        omega
      have htail := ih hnext
      constructor
      · exact ⟨hlow, htail.1⟩
      · simpa [activeScan] using htail.2

/-- Reusable irreversibility statement: once the current deficit exceeds an
arbitrary remaining-mass budget by `3`, every explicit continuation whose
total occupancy is within that budget ends nonpositive, and the entire block
is certified low-phase. -/
theorem activeScan_nonpos_of_certifiedFront
    {m T : Int} {xs : List Nat}
    (hfront : CertifiedFront T m)
    (hmass : (xs.sum : Int) ≤ T) :
    LowRun m xs ∧ activeScan m xs ≤ 0 := by
  have hdom : (xs.sum : Int) + 3 ≤ deficit m := by
    unfold CertifiedFront at hfront
    omega
  have h := lowRun_and_front_of_mass_domination hdom
  constructor
  · exact h.1
  · unfold deficit at h
    omega

/-- A finite block is an explicit deep-seed certificate when its scalar scan
ends with deficit at least `D`.  This contains no existential intermediate
state and is designed to compose with an explicit runaway cap block. -/
def DeepSeedBlock (m D : Int) (xs : List Nat) : Prop :=
  D ≤ deficit (activeScan m xs)

/-- Scalar concatenation of an explicit deep-seed block and an explicit
runaway-cap block. -/
theorem deepSeed_runaway_to_front
    {m D T : Int} {seed run : List Nat}
    (hD : 4 ≤ D)
    (hseed : DeepSeedBlock m D seed)
    (hcaps : RunawayCaps D run)
    (hreaches : T + 3 ≤ runawayDeficit D run.length) :
    CertifiedFront T (activeScan m (seed ++ run)) := by
  have hrun := lowRun_and_deficit_ge_of_runawayCaps
    hD hseed hcaps
  rw [activeScan_append]
  unfold CertifiedFront
  exact le_trans hreaches hrun.2

namespace LeftPath

/-- Genuine left-branch runaway theorem. -/
theorem leftBranch_runaway_block
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n) (m D : Int)
    (hstart :
      (leftBranch n hn start (by omega)).branchMessage C = some m)
    (hD : 4 ≤ D)
    (hdeep : D ≤ deficit m)
    (hcaps : RunawayCaps D (leftBlockValues C start len (by omega))) :
    ∃ z : Int,
      (leftBranch n hn (start + len) h).branchMessage C = some z ∧
      LowRun m (leftBlockValues C start len (by omega)) ∧
      runawayDeficit D len ≤ deficit z := by
  let xs := leftBlockValues C start len (by omega)
  have hscan := leftBranch_branchMessage_eq_activeScan_block
    hn C start len h m hstart
  have hrun := lowRun_and_deficit_ge_of_runawayCaps hD hdeep hcaps
  refine ⟨activeScan m xs, ?_, hrun.1, ?_⟩
  · simpa [xs] using hscan
  · simpa [xs] using hrun.2

/-- Explicit left finite-block event predicate. -/
def LeftRunawayBlock
    {n : Nat} (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len < n) (D : Int) : Prop :=
  RunawayCaps D (leftBlockValues C start len h)

/-- A genuine left branch reaches a certified front after an explicit runaway
block whenever the deterministic threshold overtakes the declared remaining
mass budget. -/
theorem leftBranch_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n) (m D T : Int)
    (hstart :
      (leftBranch n hn start (by omega)).branchMessage C = some m)
    (hD : 4 ≤ D)
    (hdeep : D ≤ deficit m)
    (hcaps : LeftRunawayBlock C start len (by omega) D)
    (hreaches : T + 3 ≤ runawayDeficit D len) :
    ∃ z : Int,
      (leftBranch n hn (start + len) h).branchMessage C = some z ∧
      CertifiedFront T z := by
  rcases leftBranch_runaway_block hn C start len h m D hstart hD hdeep hcaps with
    ⟨z, hz, _, hzdeep⟩
  refine ⟨z, hz, ?_⟩
  unfold CertifiedFront
  exact le_trans hreaches hzdeep

end LeftPath

namespace RightPath

/-- Genuine right-branch runaway theorem in the established `Fin.rev`
orientation. -/
theorem rightBranch_runaway_block
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n) (m D : Int)
    (hstart :
      (rightBranch n hn start (by omega)).branchMessage C = some m)
    (hD : 4 ≤ D)
    (hdeep : D ≤ deficit m)
    (hcaps : RunawayCaps D (rightBlockValues C start len (by omega))) :
    ∃ z : Int,
      (rightBranch n hn (start + len) h).branchMessage C = some z ∧
      LowRun m (rightBlockValues C start len (by omega)) ∧
      runawayDeficit D len ≤ deficit z := by
  let xs := rightBlockValues C start len (by omega)
  have hscan := rightBranch_branchMessage_eq_activeScan_block
    hn C start len h m hstart
  have hrun := lowRun_and_deficit_ge_of_runawayCaps hD hdeep hcaps
  refine ⟨activeScan m xs, ?_, hrun.1, ?_⟩
  · simpa [xs] using hscan
  · simpa [xs] using hrun.2

/-- Explicit right finite-block event predicate. -/
def RightRunawayBlock
    {n : Nat} (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len < n) (D : Int) : Prop :=
  RunawayCaps D (rightBlockValues C start len h)

theorem rightBranch_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n) (m D T : Int)
    (hstart :
      (rightBranch n hn start (by omega)).branchMessage C = some m)
    (hD : 4 ≤ D)
    (hdeep : D ≤ deficit m)
    (hcaps : RightRunawayBlock C start len (by omega) D)
    (hreaches : T + 3 ≤ runawayDeficit D len) :
    ∃ z : Int,
      (rightBranch n hn (start + len) h).branchMessage C = some z ∧
      CertifiedFront T z := by
  rcases rightBranch_runaway_block hn C start len h m D hstart hD hdeep hcaps with
    ⟨z, hz, _, hzdeep⟩
  refine ⟨z, hz, ?_⟩
  unfold CertifiedFront
  exact le_trans hreaches hzdeep

end RightPath

end ProbStack
