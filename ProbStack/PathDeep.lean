module

public import ProbStack.PathBridge
public import ProbStack.TransferBounds

@[expose] public section

namespace ProbStack

theorem activeScan_append (m : Int) (xs ys : List Nat) :
    activeScan m (xs ++ ys) = activeScan (activeScan m xs) ys := by
  induction xs generalizing m with
  | nil => simp [activeScan]
  | cons x xs ih =>
      simp [activeScan, ih]

theorem dyadicInputCost_le_of_lowRun_deficit_ge
    {m D : Int} {xs : List Nat}
    (hlow : LowRun m xs)
    (hdeep : D <= deficit (activeScan m xs)) :
    dyadicInputCost xs <= (2 : Int) ^ xs.length * deficit m - D := by
  rw [deficit_activeScan_of_lowRun hlow] at hdeep
  omega

theorem dyadicInputCost_le_of_lowRun_message_le
    {m H : Int} {xs : List Nat}
    (hlow : LowRun m xs)
    (hdeep : activeScan m xs <= -H) :
    dyadicInputCost xs <=
      (2 : Int) ^ xs.length * deficit m - (H + 3) := by
  apply dyadicInputCost_le_of_lowRun_deficit_ge hlow
  unfold deficit
  omega

namespace LeftPath

def leftBlockValues {n : Nat} (C : TreeStack.Configuration (Fin n))
    (start : Nat) : (len : Nat) -> start + len < n -> List Nat
  | 0, _ => []
  | len + 1, h =>
      leftBlockValues C start len (by omega) ++
        [C ⟨start + len + 1, by omega⟩]

@[simp] theorem leftBlockValues_length
    {n : Nat} (C : TreeStack.Configuration (Fin n)) (start len : Nat)
    (h : start + len < n) :
    (leftBlockValues C start len h).length = len := by
  induction len with
  | zero => simp [leftBlockValues]
  | succ len ih =>
      simp [leftBlockValues, ih]

theorem leftBranch_branchMessage_eq_activeScan_block
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n) (m : Int)
    (hstart :
      (leftBranch n hn start (by omega)).branchMessage C = some m) :
    (leftBranch n hn (start + len) h).branchMessage C =
      some (activeScan m (leftBlockValues C start len (by omega))) := by
  induction len with
  | zero =>
      simpa [leftBlockValues, activeScan] using hstart
  | succ len ih =>
      have hprev :
          (leftBranch n hn (start + len) (by omega)).branchMessage C =
            some (activeScan m (leftBlockValues C start len (by omega))) := by
        exact ih (by omega) hstart
      have hstep :=
        leftBranch_branchMessage_succ hn C (start + len) (by omega)
      have hend :
          (leftBranch n hn (start + len + 1) h).branchMessage C =
            some (activeScan m
              (leftBlockValues C start (len + 1) (by omega))) := by
        rw [hstep, hprev]
        simp [pathStep, activeStep, leftBlockValues,
          activeScan_append, activeScan, leftBranch]
      simpa [Nat.add_assoc] using hend

theorem leftBranch_dyadicInputCost_le_of_deep
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n) (m z H : Int)
    (hstart :
      (leftBranch n hn start (by omega)).branchMessage C = some m)
    (hlow : LowRun m (leftBlockValues C start len (by omega)))
    (hend : (leftBranch n hn (start + len) h).branchMessage C = some z)
    (hdeep : z <= -H) :
    dyadicInputCost (leftBlockValues C start len (by omega)) <=
      (2 : Int) ^ len * deficit m - (H + 3) := by
  have hscan :=
    leftBranch_branchMessage_eq_activeScan_block hn C start len h m hstart
  have hz : z = activeScan m (leftBlockValues C start len (by omega)) := by
    rw [hend] at hscan
    exact Option.some.inj hscan
  rw [hz] at hdeep
  simpa using
    (dyadicInputCost_le_of_lowRun_message_le hlow hdeep)

theorem leftBranch_regeneration_step
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hk : (j + 1) + 1 < n) (mu M : Int)
    (hprev : (leftBranch n hn j (by omega)).branchMessage C = some M)
    (hmu : 1 <= mu) (hMlo : -mu < M) (hMhi : M <= 2 * mu)
    (hXlo :
      2 * mu + 2 - M <=
        (C (leftBranch n hn (j + 1) hk).root : Int))
    (hXhi :
      (C (leftBranch n hn (j + 1) hk).root : Int) <= 4 * mu - M) :
    ∃ M' : Int,
      (leftBranch n hn (j + 1) hk).branchMessage C = some M' ∧
      mu <= M' ∧ M' <= 2 * mu := by
  let x := C (leftBranch n hn (j + 1) hk).root
  have hbranch := leftBranch_branchMessage_succ_some hn C j hk M hprev
  have hreg := regeneration_transfer_window
    (X := (x : Int)) hmu hMlo hMhi
      (by simpa [x] using hXlo) (by simpa [x] using hXhi)
  refine ⟨activeStep M x, ?_, ?_, ?_⟩
  · simpa [x] using hbranch
  · simpa [activeStep] using hreg.1
  · simpa [activeStep] using hreg.2

end LeftPath

namespace RightPath

def rightBlockValues {n : Nat} (C : TreeStack.Configuration (Fin n))
    (start : Nat) : (len : Nat) -> start + len < n -> List Nat
  | 0, _ => []
  | len + 1, h =>
      rightBlockValues C start len (by omega) ++
        [C ((⟨start + len + 1, by omega⟩ : Fin n).rev)]

@[simp] theorem rightBlockValues_length
    {n : Nat} (C : TreeStack.Configuration (Fin n)) (start len : Nat)
    (h : start + len < n) :
    (rightBlockValues C start len h).length = len := by
  induction len with
  | zero => simp [rightBlockValues]
  | succ len ih =>
      simp [rightBlockValues, ih]

theorem rightBranch_branchMessage_eq_activeScan_block
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n) (m : Int)
    (hstart :
      (rightBranch n hn start (by omega)).branchMessage C = some m) :
    (rightBranch n hn (start + len) h).branchMessage C =
      some (activeScan m (rightBlockValues C start len (by omega))) := by
  induction len with
  | zero =>
      simpa [rightBlockValues, activeScan] using hstart
  | succ len ih =>
      have hprev :
          (rightBranch n hn (start + len) (by omega)).branchMessage C =
            some (activeScan m (rightBlockValues C start len (by omega))) := by
        exact ih (by omega) hstart
      have hstep :=
        rightBranch_branchMessage_succ hn C (start + len) (by omega)
      have hend :
          (rightBranch n hn (start + len + 1) h).branchMessage C =
            some (activeScan m
              (rightBlockValues C start (len + 1) (by omega))) := by
        rw [hstep, hprev]
        simp [pathStep, activeStep, rightBlockValues,
          activeScan_append, activeScan, rightBranch]
      simpa [Nat.add_assoc] using hend

theorem rightBranch_dyadicInputCost_le_of_deep
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (start len : Nat) (h : start + len + 1 < n) (m z H : Int)
    (hstart :
      (rightBranch n hn start (by omega)).branchMessage C = some m)
    (hlow : LowRun m (rightBlockValues C start len (by omega)))
    (hend : (rightBranch n hn (start + len) h).branchMessage C = some z)
    (hdeep : z <= -H) :
    dyadicInputCost (rightBlockValues C start len (by omega)) <=
      (2 : Int) ^ len * deficit m - (H + 3) := by
  have hscan :=
    rightBranch_branchMessage_eq_activeScan_block hn C start len h m hstart
  have hz : z = activeScan m (rightBlockValues C start len (by omega)) := by
    rw [hend] at hscan
    exact Option.some.inj hscan
  rw [hz] at hdeep
  simpa using
    (dyadicInputCost_le_of_lowRun_message_le hlow hdeep)

theorem rightBranch_regeneration_step
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hk : (j + 1) + 1 < n) (mu M : Int)
    (hprev : (rightBranch n hn j (by omega)).branchMessage C = some M)
    (hmu : 1 <= mu) (hMlo : -mu < M) (hMhi : M <= 2 * mu)
    (hXlo :
      2 * mu + 2 - M <=
        (C (rightBranch n hn (j + 1) hk).root : Int))
    (hXhi :
      (C (rightBranch n hn (j + 1) hk).root : Int) <= 4 * mu - M) :
    ∃ M' : Int,
      (rightBranch n hn (j + 1) hk).branchMessage C = some M' ∧
      mu <= M' ∧ M' <= 2 * mu := by
  let x := C (rightBranch n hn (j + 1) hk).root
  have hbranch :
      (rightBranch n hn (j + 1) hk).branchMessage C =
        some (activeStep M x) := by
    rw [rightBranch_branchMessage_succ hn C j hk, hprev]
    simp [activeStep, x]
  have hreg := regeneration_transfer_window
    (X := (x : Int)) hmu hMlo hMhi
      (by simpa [x] using hXlo) (by simpa [x] using hXhi)
  refine ⟨activeStep M x, hbranch, ?_, ?_⟩
  · simpa [activeStep] using hreg.1
  · simpa [activeStep] using hreg.2

end RightPath

end ProbStack
