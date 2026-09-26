import ProbStack.Path
import ProbStack.PathMessage

namespace ProbStack

namespace PathBranch

open TreeStack
open TreeStack.OrientedBranch

variable {V : Type*} [Fintype V] {T : TreeStack.FiniteTree V}

def NoChildren (B : TreeStack.OrientedBranch T) : Prop :=
  ∀ c : B.Child, False

def UniqueChild (B : TreeStack.OrientedBranch T) (c : B.Child) : Prop :=
  ∀ d : B.Child, d = c

theorem occupied_iff_root_of_noChildren
    (C : TreeStack.Configuration V) (B : TreeStack.OrientedBranch T)
    (hno : NoChildren B) :
    B.Occupied C ↔ 0 < C B.root := by
  constructor
  · rintro ⟨v, hv, hpos⟩
    by_cases hvr : v = B.root
    · simpa [hvr] using hpos
    · obtain ⟨c, hc⟩ :=
        B.exists_childBranch_mem_of_mem_vertices_ne_root hv hvr
      exact (hno c).elim
  · intro hpos
    exact ⟨B.root, B.root_mem_vertices, hpos⟩

theorem childMessageSum_eq_zero_of_noChildren
    (C : TreeStack.Configuration V) (B : TreeStack.OrientedBranch T)
    (hno : NoChildren B) :
    B.childMessageSum C = 0 := by
  classical
  rw [TreeStack.OrientedBranch.childMessageSum]
  apply Finset.sum_eq_zero
  intro v hv
  by_cases h : T.graph.Adj B.root v ∧ v ≠ B.parent
  · exact (hno
      { vertex := v
        adj := h.1
        ne_parent := h.2 }).elim
  · simp [h]

theorem branchMessage_eq_pathStep_empty_of_noChildren
    (C : TreeStack.Configuration V) (B : TreeStack.OrientedBranch T)
    (hno : NoChildren B) :
    B.branchMessage C = pathStep TreeStack.EMPTY (C B.root) := by
  by_cases hx : C B.root = 0
  · have hnot : ¬ B.Occupied C := by
      rw [occupied_iff_root_of_noChildren C B hno]
      omega
    rw [B.branchMessage_eq_empty_of_not_occupied C hnot]
    simp [pathStep, TreeStack.EMPTY, hx]
  · have hpos : 0 < C B.root := Nat.pos_of_ne_zero hx
    have hocc : B.Occupied C :=
      (occupied_iff_root_of_noChildren C B hno).2 hpos
    rw [B.branchMessage_eq_some_of_occupied C hocc]
    rw [TreeStack.OrientedBranch.effectiveInput,
      childMessageSum_eq_zero_of_noChildren C B hno]
    rw [pathStep_empty_pos hpos]
    simp

theorem occupied_iff_root_or_uniqueChild
    (C : TreeStack.Configuration V) (B : TreeStack.OrientedBranch T)
    (c : B.Child) (huniq : UniqueChild B c) :
    B.Occupied C ↔ 0 < C B.root ∨ (B.childBranch c).Occupied C := by
  constructor
  · rintro ⟨v, hv, hpos⟩
    by_cases hvr : v = B.root
    · exact Or.inl (by simpa [hvr] using hpos)
    · obtain ⟨d, hdv⟩ :=
        B.exists_childBranch_mem_of_mem_vertices_ne_root hv hvr
      have hd : d = c := huniq d
      subst d
      exact Or.inr ⟨v, hdv, hpos⟩
  · intro h
    rcases h with hroot | hchild
    · exact ⟨B.root, B.root_mem_vertices, hroot⟩
    · rcases hchild with ⟨v, hv, hpos⟩
      exact ⟨v, B.childBranch_vertices_subset c hv, hpos⟩

theorem childMessageSum_eq_uniqueChild
    (C : TreeStack.Configuration V) (B : TreeStack.OrientedBranch T)
    (c : B.Child) (huniq : UniqueChild B c) :
    B.childMessageSum C =
      TreeStack.OrientedBranch.messageContribution
        ((B.childBranch c).branchMessage C) := by
  classical
  rw [TreeStack.OrientedBranch.childMessageSum]
  rw [Fintype.sum_eq_single c.vertex]
  · have h :
        T.graph.Adj B.root c.vertex ∧ c.vertex ≠ B.parent :=
      ⟨c.adj, c.ne_parent⟩
    rw [dite_eq_left h]
  · intro v hvc
    by_cases h : T.graph.Adj B.root v ∧ v ≠ B.parent
    · let d : B.Child :=
        { vertex := v
          adj := h.1
          ne_parent := h.2 }
      have hd : d = c := huniq d
      have hvertex : v = c.vertex := by
        simpa [d] using congrArg (fun e : B.Child => e.vertex) hd
      exact (hvc hvertex).elim
    · simp [h]

theorem branchMessage_eq_pathStep_of_uniqueChild
    (C : TreeStack.Configuration V) (B : TreeStack.OrientedBranch T)
    (c : B.Child) (huniq : UniqueChild B c) :
    B.branchMessage C =
      pathStep ((B.childBranch c).branchMessage C) (C B.root) := by
  cases hchild : (B.childBranch c).branchMessage C with
  | none =>
      have hchildEmpty :
          (B.childBranch c).branchMessage C = TreeStack.EMPTY := by
        simpa [TreeStack.EMPTY] using hchild
      have hchildNot : ¬ (B.childBranch c).Occupied C :=
        ((B.childBranch c).branchMessage_eq_empty_iff C).1 hchildEmpty
      by_cases hx : C B.root = 0
      · have hnot : ¬ B.Occupied C := by
          rw [occupied_iff_root_or_uniqueChild C B c huniq]
          simp [hx, hchildNot]
        rw [B.branchMessage_eq_empty_of_not_occupied C hnot]
        simp [pathStep, TreeStack.EMPTY, hx]
      · have hpos : 0 < C B.root := Nat.pos_of_ne_zero hx
        have hocc : B.Occupied C :=
          (occupied_iff_root_or_uniqueChild C B c huniq).2 (Or.inl hpos)
        rw [B.branchMessage_eq_some_of_occupied C hocc]
        rw [TreeStack.OrientedBranch.effectiveInput,
          childMessageSum_eq_uniqueChild C B c huniq, hchild]
        simp [pathStep, TreeStack.OrientedBranch.messageContribution, hx]
  | some z =>
      have hchildOcc : (B.childBranch c).Occupied C := by
        by_contra hnot
        have hempty :=
          (B.childBranch c).branchMessage_eq_empty_of_not_occupied C hnot
        rw [hchild] at hempty
        simp [TreeStack.EMPTY] at hempty
      have hocc : B.Occupied C :=
        (occupied_iff_root_or_uniqueChild C B c huniq).2 (Or.inr hchildOcc)
      rw [B.branchMessage_eq_some_of_occupied C hocc]
      rw [TreeStack.OrientedBranch.effectiveInput,
        childMessageSum_eq_uniqueChild C B c huniq, hchild]
      simp [pathStep, add_comm]

end PathBranch


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
