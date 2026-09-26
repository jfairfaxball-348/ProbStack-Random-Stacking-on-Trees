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
  apply Finset.sum_eq_single c.vertex
  · intro v hv hvc
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
  · have h :
        T.graph.Adj B.root c.vertex ∧ c.vertex ≠ B.parent :=
      ⟨c.adj, c.ne_parent⟩
    simp only [h, dif_pos]
    let d : B.Child :=
      { vertex := c.vertex
        adj := h.1
        ne_parent := h.2 }
    have hd : d = c := huniq d
    simpa [d] using
      congrArg
        (fun e : B.Child =>
          TreeStack.OrientedBranch.messageContribution
            ((B.childBranch e).branchMessage C)) hd
  · intro hnot
    exact (hnot (Finset.mem_univ c.vertex)).elim

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
        rw [hchild]
        simp [pathStep, TreeStack.EMPTY, hx]
      · have hpos : 0 < C B.root := Nat.pos_of_ne_zero hx
        have hocc : B.Occupied C :=
          (occupied_iff_root_or_uniqueChild C B c huniq).2 (Or.inl hpos)
        rw [B.branchMessage_eq_some_of_occupied C hocc]
        rw [TreeStack.OrientedBranch.effectiveInput,
          childMessageSum_eq_uniqueChild C B c huniq, hchild]
        rw [hchild]
        rw [pathStep_empty_pos hpos]
        simp
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
      rw [hchild]
      simp [pathStep, add_comm]

end PathBranch

end ProbStack
