module

public import ProbStack.PathBranch
public import ProbStack.Deficit

@[expose] public section

-- Session 11 path-specific bridge development.

namespace ProbStack

namespace LeftPath

def leftBranch (n : Nat) (hn : 0 < n) (k : Nat) (hk : k + 1 < n) :
    TreeStack.OrientedBranch (pathTree n hn) where
  root := ⟨k, by omega⟩
  parent := ⟨k + 1, hk⟩
  adj := by
    rw [pathTree_graph, SimpleGraph.pathGraph_adj]
    exact Or.inl rfl

@[simp] theorem leftBranch_root_val
    (n : Nat) (hn : 0 < n) (k : Nat) (hk : k + 1 < n) :
    (leftBranch n hn k hk).root.val = k := rfl

@[simp] theorem leftBranch_parent_val
    (n : Nat) (hn : 0 < n) (k : Nat) (hk : k + 1 < n) :
    (leftBranch n hn k hk).parent.val = k + 1 := rfl

def prefixScan {n : Nat} (C : TreeStack.Configuration (Fin n)) :
    (k : Nat) → k < n → TreeStack.Message
  | 0, hk => pathStep TreeStack.EMPTY (C ⟨0, hk⟩)
  | j + 1, hk =>
      pathStep
        (prefixScan C j (by omega))
        (C ⟨j + 1, hk⟩)

theorem leftBranch_zero_noChildren
    {n : Nat} (hn : 0 < n) (hk : 0 + 1 < n) :
    PathBranch.NoChildren (leftBranch n hn 0 hk) := by
  intro c
  have hadj := c.adj
  rw [pathTree_graph, SimpleGraph.pathGraph_adj] at hadj
  rcases hadj with hright | hleft
  · change 1 = c.vertex.val at hright
    apply c.ne_parent
    apply Fin.ext
    change c.vertex.val = 1
    omega
  · change c.vertex.val + 1 = 0 at hleft
    omega

def leftChildSucc
    {n : Nat} (hn : 0 < n) (j : Nat) (hk : (j + 1) + 1 < n) :
    (leftBranch n hn (j + 1) hk).Child where
  vertex := ⟨j, by omega⟩
  adj := by
    rw [pathTree_graph, SimpleGraph.pathGraph_adj]
    exact Or.inr (by simp)
  ne_parent := by
    intro h
    have hv := congrArg Fin.val h
    simp at hv
    omega

theorem leftBranch_succ_uniqueChild
    {n : Nat} (hn : 0 < n) (j : Nat) (hk : (j + 1) + 1 < n) :
    PathBranch.UniqueChild
      (leftBranch n hn (j + 1) hk)
      (leftChildSucc hn j hk) := by
  intro d
  apply TreeStack.OrientedBranch.Child.eq_of_vertex_eq
  apply Fin.ext
  have hadj := d.adj
  rw [pathTree_graph, SimpleGraph.pathGraph_adj] at hadj
  simp only [leftBranch_root_val] at hadj
  rcases hadj with hright | hleft
  · change (j + 1) + 1 = d.vertex.val at hright
    exfalso
    apply d.ne_parent
    apply Fin.ext
    change d.vertex.val = (j + 1) + 1
    omega
  · change d.vertex.val + 1 = j + 1 at hleft
    change d.vertex.val = j
    omega

theorem childBranch_leftChildSucc
    {n : Nat} (hn : 0 < n) (j : Nat) (hk : (j + 1) + 1 < n) :
    (leftBranch n hn (j + 1) hk).childBranch (leftChildSucc hn j hk) =
      leftBranch n hn j (by omega) := by
  rfl

theorem leftBranch_branchMessage_eq_prefixScan
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n)) :
    ∀ (k : Nat) (hk : k + 1 < n),
      (leftBranch n hn k hk).branchMessage C =
        prefixScan C k (by omega) := by
  intro k
  induction k with
  | zero =>
      intro hk
      rw [prefixScan]
      have hroot :
          (leftBranch n hn 0 hk).root = (⟨0, by omega⟩ : Fin n) := by
        apply Fin.ext
        rfl
      rw [← hroot]
      exact
        PathBranch.branchMessage_eq_pathStep_empty_of_noChildren
          C (leftBranch n hn 0 hk) (leftBranch_zero_noChildren hn hk)
  | succ j ih =>
      intro hk
      let c : (leftBranch n hn (j + 1) hk).Child :=
        leftChildSucc hn j hk
      have hstep :=
        PathBranch.branchMessage_eq_pathStep_of_uniqueChild
          C (leftBranch n hn (j + 1) hk) c
          (leftBranch_succ_uniqueChild hn j hk)
      rw [hstep]
      have hc :
          (leftBranch n hn (j + 1) hk).childBranch c =
            leftBranch n hn j (by omega) := by
        simpa [c] using childBranch_leftChildSucc hn j hk
      rw [hc]
      rw [ih (by omega)]
      rfl


theorem prefixScan_eq_empty_iff
    {n : Nat} (C : TreeStack.Configuration (Fin n)) :
    ∀ (k : Nat) (hk : k < n),
      prefixScan C k hk = TreeStack.EMPTY ↔
        ∀ v : Fin n, v.val <= k → C v = 0 := by
  intro k
  induction k with
  | zero =>
      intro hk
      constructor
      · intro hscan
        have hstep :
            pathStep TreeStack.EMPTY (C ⟨0, hk⟩) = TreeStack.EMPTY := by
          simpa only [prefixScan] using hscan
        have hzero :=
          (pathStep_eq_empty_iff TreeStack.EMPTY (C ⟨0, hk⟩)).1 hstep
        intro v hv
        have hv0 : v.val = 0 := by omega
        have heq : v = (⟨0, hk⟩ : Fin n) := by
          apply Fin.ext
          exact hv0
        rw [heq]
        exact hzero.2
      · intro hall
        have hzero : C ⟨0, hk⟩ = 0 :=
          hall ⟨0, hk⟩ (by simp)
        have hstep :
            pathStep TreeStack.EMPTY (C ⟨0, hk⟩) = TreeStack.EMPTY :=
          (pathStep_eq_empty_iff TreeStack.EMPTY (C ⟨0, hk⟩)).2
            ⟨rfl, hzero⟩
        simpa only [prefixScan] using hstep
  | succ j ih =>
      intro hk
      constructor
      · intro hscan
        have hstep :
            pathStep
                (prefixScan C j (by omega))
                (C ⟨j + 1, hk⟩) =
              TreeStack.EMPTY := by
          simpa only [prefixScan] using hscan
        have hparts :=
          (pathStep_eq_empty_iff
            (prefixScan C j (by omega))
            (C ⟨j + 1, hk⟩)).1 hstep
        have hprev :
            ∀ v : Fin n, v.val <= j → C v = 0 :=
          (ih (by omega)).1 hparts.1
        intro v hv
        by_cases htop : v.val = j + 1
        · have heq : v = (⟨j + 1, hk⟩ : Fin n) := by
            apply Fin.ext
            exact htop
          rw [heq]
          exact hparts.2
        · exact hprev v (by omega)
      · intro hall
        have hprevAll :
            ∀ v : Fin n, v.val <= j → C v = 0 := by
          intro v hv
          exact hall v (by omega)
        have hprev :
            prefixScan C j (by omega) = TreeStack.EMPTY :=
          (ih (by omega)).2 hprevAll
        have hroot : C ⟨j + 1, hk⟩ = 0 :=
          hall ⟨j + 1, hk⟩ (by simp)
        have hstep :
            pathStep
                (prefixScan C j (by omega))
                (C ⟨j + 1, hk⟩) =
              TreeStack.EMPTY :=
          (pathStep_eq_empty_iff
            (prefixScan C j (by omega))
            (C ⟨j + 1, hk⟩)).2
              ⟨hprev, hroot⟩
        simpa only [prefixScan] using hstep

theorem leftBranch_branchMessage_eq_empty_iff
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (k : Nat) (hk : k + 1 < n) :
    (leftBranch n hn k hk).branchMessage C = TreeStack.EMPTY ↔
      ∀ v : Fin n, v.val <= k → C v = 0 := by
  rw [leftBranch_branchMessage_eq_prefixScan hn C k hk]
  exact prefixScan_eq_empty_iff C k (by omega)

theorem leftBranch_branchMessage_succ
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hk : (j + 1) + 1 < n) :
    (leftBranch n hn (j + 1) hk).branchMessage C =
      pathStep
        ((leftBranch n hn j (by omega)).branchMessage C)
        (C (leftBranch n hn (j + 1) hk).root) := by
  let c : (leftBranch n hn (j + 1) hk).Child :=
    leftChildSucc hn j hk
  have hstep :=
    PathBranch.branchMessage_eq_pathStep_of_uniqueChild
      C (leftBranch n hn (j + 1) hk) c
      (leftBranch_succ_uniqueChild hn j hk)
  have hc :
      (leftBranch n hn (j + 1) hk).childBranch c =
        leftBranch n hn j (by omega) := by
    simpa [c] using childBranch_leftChildSucc hn j hk
  rw [hstep, hc]

theorem leftBranch_branchMessage_succ_some
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hk : (j + 1) + 1 < n) (m : Int)
    (hprev :
      (leftBranch n hn j (by omega)).branchMessage C = some m) :
    (leftBranch n hn (j + 1) hk).branchMessage C =
      some
        (activeStep m
          (C (leftBranch n hn (j + 1) hk).root)) := by
  rw [leftBranch_branchMessage_succ hn C j hk, hprev]
  simp [activeStep]

theorem leftBranch_deficit_succ_of_low
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hk : (j + 1) + 1 < n) (m : Int)
    (hprev :
      (leftBranch n hn j (by omega)).branchMessage C = some m)
    (hlow :
      m + (C (leftBranch n hn (j + 1) hk).root : Int) <= 1) :
    ∃ m' : Int,
      (leftBranch n hn (j + 1) hk).branchMessage C = some m' ∧
      deficit m' =
        2 *
          (deficit m -
            (C (leftBranch n hn (j + 1) hk).root : Int)) := by
  refine
    ⟨activeStep m (C (leftBranch n hn (j + 1) hk).root),
      leftBranch_branchMessage_succ_some hn C j hk m hprev, ?_⟩
  exact deficit_activeStep_of_low hlow

end LeftPath


namespace RightPath

def reverseConfig {n : Nat} (C : TreeStack.Configuration (Fin n)) :
    TreeStack.Configuration (Fin n) :=
  fun i => C i.rev

def rightBranch (n : Nat) (hn : 0 < n) (k : Nat) (hk : k + 1 < n) :
    TreeStack.OrientedBranch (pathTree n hn) where
  root := (⟨k, by omega⟩ : Fin n).rev
  parent := (⟨k + 1, hk⟩ : Fin n).rev
  adj := by
    rw [pathTree_graph, SimpleGraph.pathGraph_adj]
    apply Or.inr
    simp only [Fin.val_rev, Fin.val_mk]
    omega

@[simp] theorem rightBranch_root_val
    (n : Nat) (hn : 0 < n) (k : Nat) (hk : k + 1 < n) :
    (rightBranch n hn k hk).root.val = n - (k + 1) := by
  simp [rightBranch, Fin.val_rev]

@[simp] theorem rightBranch_parent_val
    (n : Nat) (hn : 0 < n) (k : Nat) (hk : k + 1 < n) :
    (rightBranch n hn k hk).parent.val = n - ((k + 1) + 1) := by
  simp [rightBranch, Fin.val_rev]

theorem rightBranch_zero_noChildren
    {n : Nat} (hn : 0 < n) (hk : 0 + 1 < n) :
    PathBranch.NoChildren (rightBranch n hn 0 hk) := by
  intro c
  have hadj := c.adj
  rw [pathTree_graph, SimpleGraph.pathGraph_adj] at hadj
  simp only [rightBranch_root_val] at hadj
  rcases hadj with hright | hleft
  · have hvlt := c.vertex.isLt
    omega
  · apply c.ne_parent
    apply Fin.ext
    simp only [rightBranch_parent_val]
    omega

def rightChildSucc
    {n : Nat} (hn : 0 < n) (j : Nat) (hk : (j + 1) + 1 < n) :
    (rightBranch n hn (j + 1) hk).Child where
  vertex := (⟨j, by omega⟩ : Fin n).rev
  adj := by
    rw [pathTree_graph, SimpleGraph.pathGraph_adj]
    apply Or.inl
    simp only [rightBranch_root_val, Fin.val_rev, Fin.val_mk]
    omega
  ne_parent := by
    intro h
    have hv := congrArg Fin.val h
    simp only [Fin.val_rev, Fin.val_mk, rightBranch_parent_val] at hv
    omega

theorem rightBranch_succ_uniqueChild
    {n : Nat} (hn : 0 < n) (j : Nat) (hk : (j + 1) + 1 < n) :
    PathBranch.UniqueChild
      (rightBranch n hn (j + 1) hk)
      (rightChildSucc hn j hk) := by
  intro d
  apply TreeStack.OrientedBranch.Child.eq_of_vertex_eq
  apply Fin.ext
  have hadj := d.adj
  rw [pathTree_graph, SimpleGraph.pathGraph_adj] at hadj
  simp only [rightBranch_root_val] at hadj
  rcases hadj with hright | hleft
  · change
      d.vertex.val =
        ((⟨j, by omega⟩ : Fin n).rev).val
    simp only [Fin.val_rev, Fin.val_mk]
    omega
  · exfalso
    apply d.ne_parent
    apply Fin.ext
    simp only [rightBranch_parent_val]
    omega

theorem childBranch_rightChildSucc
    {n : Nat} (hn : 0 < n) (j : Nat) (hk : (j + 1) + 1 < n) :
    (rightBranch n hn (j + 1) hk).childBranch (rightChildSucc hn j hk) =
      rightBranch n hn j (by omega) := by
  rfl

theorem rightBranch_branchMessage_eq_reversePrefixScan
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n)) :
    ∀ (k : Nat) (hk : k + 1 < n),
      (rightBranch n hn k hk).branchMessage C =
        LeftPath.prefixScan (reverseConfig C) k (by omega) := by
  intro k
  induction k with
  | zero =>
      intro hk
      rw [LeftPath.prefixScan]
      change
        (rightBranch n hn 0 hk).branchMessage C =
          pathStep TreeStack.EMPTY (C ((⟨0, by omega⟩ : Fin n).rev))
      have hroot :
          (rightBranch n hn 0 hk).root =
            (⟨0, by omega⟩ : Fin n).rev := by
        rfl
      rw [← hroot]
      exact
        PathBranch.branchMessage_eq_pathStep_empty_of_noChildren
          C (rightBranch n hn 0 hk) (rightBranch_zero_noChildren hn hk)
  | succ j ih =>
      intro hk
      let c : (rightBranch n hn (j + 1) hk).Child :=
        rightChildSucc hn j hk
      have hstep :=
        PathBranch.branchMessage_eq_pathStep_of_uniqueChild
          C (rightBranch n hn (j + 1) hk) c
          (rightBranch_succ_uniqueChild hn j hk)
      rw [hstep]
      have hc :
          (rightBranch n hn (j + 1) hk).childBranch c =
            rightBranch n hn j (by omega) := by
        simpa [c] using childBranch_rightChildSucc hn j hk
      rw [hc]
      rw [ih (by omega)]
      rfl

theorem rightBranch_branchMessage_eq_empty_iff
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (k : Nat) (hk : k + 1 < n) :
    (rightBranch n hn k hk).branchMessage C = TreeStack.EMPTY ↔
      ∀ i : Fin n, i.val <= k → C i.rev = 0 := by
  rw [rightBranch_branchMessage_eq_reversePrefixScan hn C k hk]
  exact LeftPath.prefixScan_eq_empty_iff (reverseConfig C) k (by omega)

theorem rightBranch_branchMessage_succ
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hk : (j + 1) + 1 < n) :
    (rightBranch n hn (j + 1) hk).branchMessage C =
      pathStep
        ((rightBranch n hn j (by omega)).branchMessage C)
        (C (rightBranch n hn (j + 1) hk).root) := by
  let c : (rightBranch n hn (j + 1) hk).Child :=
    rightChildSucc hn j hk
  have hstep :=
    PathBranch.branchMessage_eq_pathStep_of_uniqueChild
      C (rightBranch n hn (j + 1) hk) c
      (rightBranch_succ_uniqueChild hn j hk)
  have hc :
      (rightBranch n hn (j + 1) hk).childBranch c =
        rightBranch n hn j (by omega) := by
    simpa [c] using childBranch_rightChildSucc hn j hk
  rw [hstep, hc]

theorem rightBranch_deficit_succ_of_low
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hk : (j + 1) + 1 < n) (m : Int)
    (hprev :
      (rightBranch n hn j (by omega)).branchMessage C = some m)
    (hlow :
      m + (C (rightBranch n hn (j + 1) hk).root : Int) <= 1) :
    ∃ m' : Int,
      (rightBranch n hn (j + 1) hk).branchMessage C = some m' ∧
      deficit m' =
        2 *
          (deficit m -
            (C (rightBranch n hn (j + 1) hk).root : Int)) := by
  let x := C (rightBranch n hn (j + 1) hk).root
  refine ⟨activeStep m x, ?_, deficit_activeStep_of_low hlow⟩
  rw [rightBranch_branchMessage_succ hn C j hk, hprev]
  simp [activeStep, x]

end RightPath

end ProbStack
