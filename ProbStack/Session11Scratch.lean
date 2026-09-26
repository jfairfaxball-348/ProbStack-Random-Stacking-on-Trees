import ProbStack.PathBranch

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
  · have hv : c.vertex.val = 1 := by omega
    have hp : (leftBranch n hn 0 hk).parent.val = 1 := rfl
    apply c.ne_parent
    apply Fin.ext
    simpa [hp] using hv
  · omega

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
  rcases hadj with hright | hleft
  · exfalso
    apply d.ne_parent
    apply Fin.ext
    simp only [leftBranch_parent_val]
    omega
  · simp only [leftChildSucc]
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
      simpa [prefixScan] using
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

end LeftPath

end ProbStack
