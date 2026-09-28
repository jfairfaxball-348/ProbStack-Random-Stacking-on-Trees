module

public import Mathlib.Combinatorics.SimpleGraph.Hasse
public import ProbStack.TreeStackBoundary

public section

namespace ProbStack

theorem pathGraph_isAcyclic (n : ℕ) :
    (SimpleGraph.pathGraph n).IsAcyclic := by
  intro v c hc
  classical
  let s : Finset (Fin n) := c.support.toFinset
  have hv_s : v ∈ s := by
    simp [s]
  have hs : s.Nonempty := ⟨v, hv_s⟩
  let w : Fin n := s.max' hs
  have hw_s : w ∈ s := s.max'_mem hs
  have hw : w ∈ c.support := by
    simpa [s] using hw_s
  let d := c.rotate w hw
  have hd : d.IsCycle := hc.rotate hw
  have hdn : ¬ d.Nil := hd.not_nil
  have hsnd_d : d.snd ∈ d.support :=
    List.mem_of_mem_tail (d.snd_mem_tail_support hdn)
  have hpen_d : d.penultimate ∈ d.support :=
    List.mem_of_mem_dropLast (d.penultimate_mem_dropLast_support hdn)
  have hsnd_c : d.snd ∈ c.support := by
    rw [← c.mem_support_rotate_iff w hw]
    simpa [d] using hsnd_d
  have hpen_c : d.penultimate ∈ c.support := by
    rw [← c.mem_support_rotate_iff w hw]
    simpa [d] using hpen_d
  have hsnd_s : d.snd ∈ s := by
    simpa [s] using hsnd_c
  have hpen_s : d.penultimate ∈ s := by
    simpa [s] using hpen_c
  have hsnd_le : d.snd ≤ w := by
    simpa [w] using s.le_max' d.snd hsnd_s
  have hpen_le : d.penultimate ≤ w := by
    simpa [w] using s.le_max' d.penultimate hpen_s
  have hadj_snd := d.adj_snd hdn
  have hadj_pen := d.adj_penultimate hdn
  rw [SimpleGraph.pathGraph_adj] at hadj_snd hadj_pen
  have hsnd_val : d.snd.val + 1 = w.val := by
    rcases hadj_snd with h | h
    · have hle : d.snd.val ≤ w.val := hsnd_le
      omega
    · exact h
  have hpen_val : d.penultimate.val + 1 = w.val := by
    rcases hadj_pen with h | h
    · exact h
    · have hle : d.penultimate.val ≤ w.val := hpen_le
      omega
  have heq : d.snd = d.penultimate := by
    apply Fin.ext
    omega
  exact hd.snd_ne_penultimate heq

theorem pathGraph_connected_of_pos {n : ℕ} (hn : 0 < n) :
    (SimpleGraph.pathGraph n).Connected := by
  cases n with
  | zero => omega
  | succ k =>
      simpa [Nat.succ_eq_add_one] using SimpleGraph.pathGraph_connected k

noncomputable def pathTree (n : ℕ) (hn : 0 < n) :
    TreeStack.FiniteTree (Fin n) where
  graph := SimpleGraph.pathGraph n
  isTree := ⟨pathGraph_connected_of_pos hn, pathGraph_isAcyclic n⟩

@[simp] theorem pathTree_graph (n : ℕ) (hn : 0 < n) :
    (pathTree n hn).graph = SimpleGraph.pathGraph n := rfl

end ProbStack
