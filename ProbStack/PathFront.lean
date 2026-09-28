module

public import ProbStack.PathDeep

@[expose] public section

namespace ProbStack

/-- A certified deficit threshold grows by the integer factor floor(3/2). -/
def runawayNext (D : Int) : Int :=
  D + D / 2

/--
An explicit finite runaway certificate.  At threshold `D`, the next occupancy
`x` must satisfy `4*x <= D`; the certified threshold then becomes
`floor(3D/2)`.
-/
def RunawayBlock : Int → List Nat → Prop
  | _, [] => True
  | D, x :: xs =>
      4 * (x : Int) <= D ∧ RunawayBlock (runawayNext D) xs

/-- The deterministic threshold after `k` certified runaway steps. -/
def runawayThreshold (D : Int) : Nat → Int
  | 0 => D
  | k + 1 => runawayThreshold (runawayNext D) k

/-- A scalar active message has deficit at least `D`. -/
def DeepSeed (D m : Int) : Prop :=
  D <= deficit m

/--
A finite occupancy block sends every starting message in `[lo,hi]` to
deficit at least `D`.  This is the scalar seam used to concatenate the
regeneration window to any later explicit seed construction.
-/
def UniformDeepSeedBlock (lo hi D : Int) (xs : List Nat) : Prop :=
  ∀ m : Int, lo <= m → m <= hi → DeepSeed D (activeScan m xs)

/--
A message is an irreversible front against any future occupancy budget
`budget`: its deficit exceeds that budget by at least two.
-/
def CertifiedFront (budget : Nat) (m : Int) : Prop :=
  (budget : Int) + 2 <= deficit m

theorem four_le_runawayNext {D : Int} (hD : 4 <= D) :
    4 <= runawayNext D := by
  unfold runawayNext
  omega

theorem runaway_step
    {m D : Int} {x : Nat}
    (hD : 4 <= D)
    (hseed : DeepSeed D m)
    (hcap : 4 * (x : Int) <= D) :
    m + (x : Int) <= 1 ∧
      DeepSeed (runawayNext D) (activeStep m x) := by
  have hlow : m + (x : Int) <= 1 := by
    unfold DeepSeed deficit at hseed
    omega
  constructor
  · exact hlow
  · have hhalf : 2 * (x : Int) <= D / 2 := by
      omega
    have hdouble : 2 * (D / 2) <= D := by
      omega
    unfold DeepSeed runawayNext
    rw [deficit_activeStep_of_low hlow]
    unfold DeepSeed deficit at hseed
    unfold deficit
    omega

theorem runawayBlock_lowRun_and_deficit_ge
    {m D : Int} {xs : List Nat}
    (hD : 4 <= D)
    (hseed : DeepSeed D m)
    (hblock : RunawayBlock D xs) :
    LowRun m xs ∧
      runawayThreshold D xs.length <= deficit (activeScan m xs) := by
  induction xs generalizing m D with
  | nil =>
      constructor
      · simp [LowRun]
      · simpa [runawayThreshold, activeScan, DeepSeed] using hseed
  | cons x xs ih =>
      change
        4 * (x : Int) <= D ∧ RunawayBlock (runawayNext D) xs at hblock
      rcases hblock with ⟨hcap, hrest⟩
      have hstep := runaway_step hD hseed hcap
      have hD' : 4 <= runawayNext D := four_le_runawayNext hD
      have htail :=
        ih (m := activeStep m x) (D := runawayNext D)
          hD' hstep.2 hrest
      constructor
      · change
          m + (x : Int) <= 1 ∧ LowRun (activeStep m x) xs
        exact ⟨hstep.1, htail.1⟩
      · simpa [runawayThreshold, activeScan] using htail.2

theorem deepSeed_runaway_to_front
    {m D : Int} {xs : List Nat} {budget : Nat}
    (hD : 4 <= D)
    (hseed : DeepSeed D m)
    (hblock : RunawayBlock D xs)
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D xs.length) :
    CertifiedFront budget (activeScan m xs) := by
  have hgrowth :=
    runawayBlock_lowRun_and_deficit_ge hD hseed hblock
  unfold CertifiedFront
  exact le_trans htarget hgrowth.2

theorem lowRun_of_message_add_sum_le_one
    {m : Int} {xs : List Nat}
    (h : m + (xs.sum : Int) <= 1) :
    LowRun m xs := by
  induction xs generalizing m with
  | nil =>
      simp [LowRun]
  | cons x xs ih =>
      simp only [List.sum_cons, Nat.cast_add] at h
      have hfirst : m + (x : Int) <= 1 := by omega
      have hstep_le : activeStep m x <= m + (x : Int) := by
        unfold activeStep
        rw [TreeStack.F_of_le_one hfirst]
        omega
      have hrest :
          activeStep m x + (xs.sum : Int) <= 1 := by
        omega
      change
        m + (x : Int) <= 1 ∧ LowRun (activeStep m x) xs
      exact ⟨hfirst, ih hrest⟩

theorem certifiedFront_lowRun
    {budget : Nat} {m : Int} {xs : List Nat}
    (hfront : CertifiedFront budget m)
    (hmass : xs.sum <= budget) :
    LowRun m xs := by
  apply lowRun_of_message_add_sum_le_one
  unfold CertifiedFront deficit at hfront
  have hmass' : (xs.sum : Int) <= (budget : Int) := by
    exact_mod_cast hmass
  omega

theorem activeScan_le_neg_one_of_lowRun_nonempty
    {m : Int} {xs : List Nat}
    (hne : xs ≠ [])
    (hlow : LowRun m xs) :
    activeScan m xs <= -1 := by
  induction xs generalizing m with
  | nil =>
      exact (hne rfl).elim
  | cons x xs ih =>
      change
        m + (x : Int) <= 1 ∧ LowRun (activeStep m x) xs at hlow
      rcases hlow with ⟨hfirst, hrest⟩
      cases xs with
      | nil =>
          simp only [activeScan]
          unfold activeStep
          rw [TreeStack.F_of_le_one hfirst]
          omega
      | cons y ys =>
          have htail :
              activeScan (activeStep m x) (y :: ys) <= -1 :=
            ih (m := activeStep m x) (by simp) hrest
          simpa [activeScan] using htail

theorem certifiedFront_dominates
    {budget : Nat} {m : Int} {xs : List Nat}
    (hfront : CertifiedFront budget m)
    (hmass : xs.sum <= budget) :
    LowRun m xs ∧
      (xs = [] ∨ activeScan m xs <= -1) := by
  have hlow := certifiedFront_lowRun hfront hmass
  constructor
  · exact hlow
  · by_cases hnil : xs = []
    · exact Or.inl hnil
    · exact Or.inr
        (activeScan_le_neg_one_of_lowRun_nonempty hnil hlow)

namespace LeftPath

theorem leftBranch_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n)
    (m D : Int) (budget : Nat)
    (hstart :
      (leftBranch n hn start (by omega)).branchMessage C = some m)
    (hD : 4 <= D)
    (hseed : DeepSeed D m)
    (hblock :
      RunawayBlock D (leftBlockValues C start len (by omega)))
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D len) :
    (leftBranch n hn (start + len) h).branchMessage C =
        some (activeScan m (leftBlockValues C start len (by omega))) ∧
      CertifiedFront budget
        (activeScan m (leftBlockValues C start len (by omega))) ∧
      LowRun m (leftBlockValues C start len (by omega)) := by
  have hscan :=
    leftBranch_branchMessage_eq_activeScan_block
      hn C start len h m hstart
  have hgrowth :=
    runawayBlock_lowRun_and_deficit_ge hD hseed hblock
  have hthreshold :
      runawayThreshold D len <=
        deficit (activeScan m (leftBlockValues C start len (by omega))) := by
    simpa using hgrowth.2
  have hfront :
      CertifiedFront budget
        (activeScan m (leftBlockValues C start len (by omega))) := by
    unfold CertifiedFront
    exact le_trans htarget hthreshold
  exact ⟨hscan, hfront, hgrowth.1⟩

theorem leftBranch_certifiedFront_irreversible
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n)
    (m : Int) (budget : Nat)
    (hstart :
      (leftBranch n hn start (by omega)).branchMessage C = some m)
    (hfront : CertifiedFront budget m)
    (hmass :
      (leftBlockValues C start len (by omega)).sum <= budget) :
    (leftBranch n hn (start + len) h).branchMessage C =
        some (activeScan m (leftBlockValues C start len (by omega))) ∧
      LowRun m (leftBlockValues C start len (by omega)) ∧
      (len = 0 ∨
        activeScan m (leftBlockValues C start len (by omega)) <= -1) := by
  have hscan :=
    leftBranch_branchMessage_eq_activeScan_block
      hn C start len h m hstart
  have hdom :=
    certifiedFront_dominates hfront hmass
  constructor
  · exact hscan
  constructor
  · exact hdom.1
  · rcases hdom.2 with hnil | hneg
    · left
      have hlen :=
        leftBlockValues_length C start len (by omega)
      rw [hnil] at hlen
      exact hlen.symm
    · exact Or.inr hneg

theorem leftBranch_seed_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start seedLen runLen : Nat)
    (h : start + seedLen + runLen + 1 < n)
    (m D : Int) (budget : Nat)
    (hstart :
      (leftBranch n hn start (by omega)).branchMessage C = some m)
    (hD : 4 <= D)
    (hseed :
      DeepSeed D
        (activeScan m
          (leftBlockValues C start seedLen (by omega))))
    (hrun :
      RunawayBlock D
        (leftBlockValues C (start + seedLen) runLen (by omega)))
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D runLen) :
    ∃ z : Int,
      (leftBranch n hn (start + seedLen + runLen) (by omega)).branchMessage C =
        some z ∧
      CertifiedFront budget z := by
  have hseedMsg :=
    leftBranch_branchMessage_eq_activeScan_block
      hn C start seedLen (by omega) m hstart
  have hrunFront :=
    leftBranch_runaway_to_front
      hn C (start + seedLen) runLen (by omega)
      (activeScan m (leftBlockValues C start seedLen (by omega)))
      D budget hseedMsg hD hseed hrun htarget
  refine
    ⟨activeScan
        (activeScan m (leftBlockValues C start seedLen (by omega)))
        (leftBlockValues C (start + seedLen) runLen (by omega)),
      ?_, hrunFront.2.1⟩
  simpa [Nat.add_assoc] using hrunFront.1

theorem leftBranch_regeneration_seed_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j seedLen runLen : Nat)
    (h : j + 1 + seedLen + runLen + 1 < n)
    (mu M D : Int) (budget : Nat)
    (hprev :
      (leftBranch n hn j (by omega)).branchMessage C = some M)
    (hmu : 1 <= mu) (hMlo : -mu < M) (hMhi : M <= 2 * mu)
    (hXlo :
      2 * mu + 2 - M <=
        (C (leftBranch n hn (j + 1) (by omega)).root : Int))
    (hXhi :
      (C (leftBranch n hn (j + 1) (by omega)).root : Int) <=
        4 * mu - M)
    (hD : 4 <= D)
    (hseedBlock :
      UniformDeepSeedBlock mu (2 * mu) D
        (leftBlockValues C (j + 1) seedLen (by omega)))
    (hrun :
      RunawayBlock D
        (leftBlockValues C (j + 1 + seedLen) runLen (by omega)))
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D runLen) :
    ∃ z : Int,
      (leftBranch n hn (j + 1 + seedLen + runLen) (by omega)).branchMessage C =
        some z ∧
      CertifiedFront budget z := by
  obtain ⟨M', hreg, hM'lo, hM'hi⟩ :=
    leftBranch_regeneration_step
      hn C j (by omega) mu M hprev hmu hMlo hMhi
        (by simpa using hXlo) (by simpa using hXhi)
  have hseed :
      DeepSeed D
        (activeScan M'
          (leftBlockValues C (j + 1) seedLen (by omega))) :=
    hseedBlock M' hM'lo hM'hi
  have hfront :=
    leftBranch_seed_runaway_to_front
      hn C (j + 1) seedLen runLen (by omega)
      M' D budget hreg hD hseed
      (by simpa [Nat.add_assoc] using hrun) htarget
  simpa [Nat.add_assoc] using hfront

end LeftPath

namespace RightPath

theorem rightBranch_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n)
    (m D : Int) (budget : Nat)
    (hstart :
      (rightBranch n hn start (by omega)).branchMessage C = some m)
    (hD : 4 <= D)
    (hseed : DeepSeed D m)
    (hblock :
      RunawayBlock D (rightBlockValues C start len (by omega)))
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D len) :
    (rightBranch n hn (start + len) h).branchMessage C =
        some (activeScan m (rightBlockValues C start len (by omega))) ∧
      CertifiedFront budget
        (activeScan m (rightBlockValues C start len (by omega))) ∧
      LowRun m (rightBlockValues C start len (by omega)) := by
  have hscan :=
    rightBranch_branchMessage_eq_activeScan_block
      hn C start len h m hstart
  have hgrowth :=
    runawayBlock_lowRun_and_deficit_ge hD hseed hblock
  have hthreshold :
      runawayThreshold D len <=
        deficit (activeScan m (rightBlockValues C start len (by omega))) := by
    simpa using hgrowth.2
  have hfront :
      CertifiedFront budget
        (activeScan m (rightBlockValues C start len (by omega))) := by
    unfold CertifiedFront
    exact le_trans htarget hthreshold
  exact ⟨hscan, hfront, hgrowth.1⟩

theorem rightBranch_certifiedFront_irreversible
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n)
    (m : Int) (budget : Nat)
    (hstart :
      (rightBranch n hn start (by omega)).branchMessage C = some m)
    (hfront : CertifiedFront budget m)
    (hmass :
      (rightBlockValues C start len (by omega)).sum <= budget) :
    (rightBranch n hn (start + len) h).branchMessage C =
        some (activeScan m (rightBlockValues C start len (by omega))) ∧
      LowRun m (rightBlockValues C start len (by omega)) ∧
      (len = 0 ∨
        activeScan m (rightBlockValues C start len (by omega)) <= -1) := by
  have hscan :=
    rightBranch_branchMessage_eq_activeScan_block
      hn C start len h m hstart
  have hdom :=
    certifiedFront_dominates hfront hmass
  constructor
  · exact hscan
  constructor
  · exact hdom.1
  · rcases hdom.2 with hnil | hneg
    · left
      have hlen :=
        rightBlockValues_length C start len (by omega)
      rw [hnil] at hlen
      exact hlen.symm
    · exact Or.inr hneg

theorem rightBranch_seed_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start seedLen runLen : Nat)
    (h : start + seedLen + runLen + 1 < n)
    (m D : Int) (budget : Nat)
    (hstart :
      (rightBranch n hn start (by omega)).branchMessage C = some m)
    (hD : 4 <= D)
    (hseed :
      DeepSeed D
        (activeScan m
          (rightBlockValues C start seedLen (by omega))))
    (hrun :
      RunawayBlock D
        (rightBlockValues C (start + seedLen) runLen (by omega)))
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D runLen) :
    ∃ z : Int,
      (rightBranch n hn (start + seedLen + runLen) (by omega)).branchMessage C =
        some z ∧
      CertifiedFront budget z := by
  have hseedMsg :=
    rightBranch_branchMessage_eq_activeScan_block
      hn C start seedLen (by omega) m hstart
  have hrunFront :=
    rightBranch_runaway_to_front
      hn C (start + seedLen) runLen (by omega)
      (activeScan m (rightBlockValues C start seedLen (by omega)))
      D budget hseedMsg hD hseed hrun htarget
  refine
    ⟨activeScan
        (activeScan m (rightBlockValues C start seedLen (by omega)))
        (rightBlockValues C (start + seedLen) runLen (by omega)),
      ?_, hrunFront.2.1⟩
  simpa [Nat.add_assoc] using hrunFront.1

theorem rightBranch_regeneration_seed_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j seedLen runLen : Nat)
    (h : j + 1 + seedLen + runLen + 1 < n)
    (mu M D : Int) (budget : Nat)
    (hprev :
      (rightBranch n hn j (by omega)).branchMessage C = some M)
    (hmu : 1 <= mu) (hMlo : -mu < M) (hMhi : M <= 2 * mu)
    (hXlo :
      2 * mu + 2 - M <=
        (C (rightBranch n hn (j + 1) (by omega)).root : Int))
    (hXhi :
      (C (rightBranch n hn (j + 1) (by omega)).root : Int) <=
        4 * mu - M)
    (hD : 4 <= D)
    (hseedBlock :
      UniformDeepSeedBlock mu (2 * mu) D
        (rightBlockValues C (j + 1) seedLen (by omega)))
    (hrun :
      RunawayBlock D
        (rightBlockValues C (j + 1 + seedLen) runLen (by omega)))
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D runLen) :
    ∃ z : Int,
      (rightBranch n hn (j + 1 + seedLen + runLen) (by omega)).branchMessage C =
        some z ∧
      CertifiedFront budget z := by
  obtain ⟨M', hreg, hM'lo, hM'hi⟩ :=
    rightBranch_regeneration_step
      hn C j (by omega) mu M hprev hmu hMlo hMhi
        (by simpa using hXlo) (by simpa using hXhi)
  have hseed :
      DeepSeed D
        (activeScan M'
          (rightBlockValues C (j + 1) seedLen (by omega))) :=
    hseedBlock M' hM'lo hM'hi
  have hfront :=
    rightBranch_seed_runaway_to_front
      hn C (j + 1) seedLen runLen (by omega)
      M' D budget hreg hD hseed
      (by simpa [Nat.add_assoc] using hrun) htarget
  simpa [Nat.add_assoc] using hfront

end RightPath

end ProbStack
