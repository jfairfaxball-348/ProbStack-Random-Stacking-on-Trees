import ProbStack.PathBridge

namespace ProbStack

open scoped BigOperators Classical
open TreeStack
open TreeStack.OrientedBranch

/--
A directed path message reaches at most `-h`.  The quantification is over an
oriented edge `u -> r` of the actual path tree, so both path orientations are
included.  The witness is explicitly an integer message; `EMPTY` is not
identified with zero.
-/
def HasDirectedPathMessageAtMost {n : Nat} (hn : 0 < n)
    (C : TreeStack.Configuration (Fin n)) (h : Nat) : Prop :=
  ∃ (r u : Fin n)
      (hu : (pathTree n hn).graph.Adj u r)
      (m : Int),
    (TreeStack.incidentBranch (pathTree n hn) r u hu).branchMessage C =
        some m ∧
      m <= -(h : Int)

private theorem rootMessageTerm_eq_branchContribution
    {V : Type*} [Fintype V] {T : TreeStack.FiniteTree V}
    (C : TreeStack.Configuration V) (B : TreeStack.OrientedBranch T) :
    TreeStack.rootMessageTerm T C B.parent B.root =
      TreeStack.OrientedBranch.messageContribution (B.branchMessage C) := by
  rw [TreeStack.rootMessageTerm]
  simp only [dif_pos B.adj]
  rfl

private theorem rootMessageTerm_gt_neg_of_noDeep
    {n h : Nat} (hn : 0 < n)
    (C : TreeStack.Configuration (Fin n))
    (hh : 1 <= h)
    (hnodeep : ¬ HasDirectedPathMessageAtMost hn C h)
    (r u : Fin n) (hu : (pathTree n hn).graph.Adj u r) :
    -(h : Int) < TreeStack.rootMessageTerm (pathTree n hn) C r u := by
  rw [TreeStack.rootMessageTerm]
  simp only [dif_pos hu]
  cases hm :
      (TreeStack.incidentBranch (pathTree n hn) r u hu).branchMessage C with
  | none =>
      simp [TreeStack.OrientedBranch.messageContribution]
      omega
  | some m =>
      simp only [TreeStack.OrientedBranch.messageContribution_some]
      by_contra hnot
      have hmle : m <= -(h : Int) := by omega
      exact hnodeep ⟨r, u, hu, m, hm, hmle⟩

private theorem transfer_dissipation_le
    {h : Nat} (hh : 1 <= h) {y : Int}
    (hy : y <= (h : Int) - 1)
    (hout : -(h : Int) < TreeStack.F y) :
    y - TreeStack.F y <= ((h / 2 + 1 : Nat) : Int) := by
  unfold TreeStack.F at hout ⊢
  split_ifs at hout ⊢ <;> omega

private theorem pathStep_dissipation_le
    {h : Nat} (hh : 1 <= h)
    (m : TreeStack.Message) (x : Nat)
    (hy :
      (x : Int) + TreeStack.OrientedBranch.messageContribution m <=
        (h : Int) - 1)
    (hout :
      -(h : Int) <
        TreeStack.OrientedBranch.messageContribution (pathStep m x)) :
    (x : Int) + TreeStack.OrientedBranch.messageContribution m -
        TreeStack.OrientedBranch.messageContribution (pathStep m x) <=
      ((h / 2 + 1 : Nat) : Int) := by
  cases m with
  | none =>
      by_cases hx : x = 0
      · subst x
        simp [pathStep, TreeStack.EMPTY]
        omega
      · have hy' : (x : Int) <= (h : Int) - 1 := by
          simpa [TreeStack.OrientedBranch.messageContribution,
            TreeStack.EMPTY] using hy
        have hout' : -(h : Int) < TreeStack.F (x : Int) := by
          simpa [pathStep, TreeStack.EMPTY, hx] using hout
        simpa [pathStep, TreeStack.EMPTY, hx] using
          (transfer_dissipation_le hh hy' hout')
  | some z =>
      simp only [TreeStack.OrientedBranch.messageContribution_some] at hy
      simp only [pathStep_some,
        TreeStack.OrientedBranch.messageContribution_some] at hout ⊢
      have hy' : z + (x : Int) <= (h : Int) - 1 := by
        omega
      have hout' : -(h : Int) < TreeStack.F (z + (x : Int)) := hout
      have hbound := transfer_dissipation_le hh hy' hout'
      linarith

private theorem path_score_zero_eq
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (hn2 : 1 < n) :
    TreeStack.score (pathTree n hn) C ⟨0, hn⟩ =
      (C ⟨0, hn⟩ : Int) +
        TreeStack.rootMessageTerm (pathTree n hn) C
          ⟨0, hn⟩ ⟨1, hn2⟩ := by
  rw [TreeStack.score, TreeStack.rootMessageSum]
  rw [Fintype.sum_eq_single (⟨1, hn2⟩ : Fin n)]
  intro u hune
    have hnadj :
        ¬ (pathTree n hn).graph.Adj u (⟨0, hn⟩ : Fin n) := by
      intro hadj
      rw [pathTree_graph, SimpleGraph.pathGraph_adj] at hadj
      rcases hadj with hleft | hright
      · omega
      · apply hune
        apply Fin.ext
        omega
    simp [TreeStack.rootMessageTerm, hnadj]

private theorem path_score_interior_eq
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hj : j + 2 < n) :
    TreeStack.score (pathTree n hn) C ⟨j + 1, by omega⟩ =
      (C ⟨j + 1, by omega⟩ : Int) +
        TreeStack.rootMessageTerm (pathTree n hn) C
          ⟨j + 1, by omega⟩ ⟨j, by omega⟩ +
        TreeStack.rootMessageTerm (pathTree n hn) C
          ⟨j + 1, by omega⟩ ⟨j + 2, by omega⟩ := by
  let r : Fin n := ⟨j + 1, by omega⟩
  let l : Fin n := ⟨j, by omega⟩
  let q : Fin n := ⟨j + 2, by omega⟩
  have hlq : l ≠ q := by
    intro h
    have hv := congrArg Fin.val h
    simp [l, q] at hv
    omega
  have hterm :
      ∀ u : Fin n,
        TreeStack.rootMessageTerm (pathTree n hn) C r u =
          (if u = l then
              TreeStack.rootMessageTerm (pathTree n hn) C r l
            else 0) +
          (if u = q then
              TreeStack.rootMessageTerm (pathTree n hn) C r q
            else 0) := by
    intro u
    by_cases hul : u = l
    · subst u
      simp [hlq]
    · by_cases huq : u = q
      · subst u
        simp [hul]
      · have hnadj : ¬ (pathTree n hn).graph.Adj u r := by
          intro hadj
          rw [pathTree_graph, SimpleGraph.pathGraph_adj] at hadj
          rcases hadj with hleft | hright
          · apply hul
            apply Fin.ext
            simp [r, l] at hleft ⊢
            omega
          · apply huq
            apply Fin.ext
            simp [r, q] at hright ⊢
            omega
        have hnadj' : ¬ (SimpleGraph.pathGraph n).Adj u r := by
          simpa [pathTree_graph] using hnadj
        rw [TreeStack.rootMessageTerm]
        simp only [dif_neg hnadj']
        simp [hul, huq]
  have hsum :
      (∑ u : Fin n,
        TreeStack.rootMessageTerm (pathTree n hn) C r u) =
        TreeStack.rootMessageTerm (pathTree n hn) C r l +
          TreeStack.rootMessageTerm (pathTree n hn) C r q := by
    calc
      (∑ u : Fin n,
          TreeStack.rootMessageTerm (pathTree n hn) C r u) =
          ∑ u : Fin n,
            ((if u = l then
                TreeStack.rootMessageTerm (pathTree n hn) C r l
              else 0) +
             (if u = q then
                TreeStack.rootMessageTerm (pathTree n hn) C r q
              else 0)) := by
            apply Finset.sum_congr rfl
            intro u hu
            exact hterm u
      _ = TreeStack.rootMessageTerm (pathTree n hn) C r l +
            TreeStack.rootMessageTerm (pathTree n hn) C r q := by
            simp [hlq]
  change
    TreeStack.score (pathTree n hn) C r =
      (C r : Int) +
        TreeStack.rootMessageTerm (pathTree n hn) C r l +
        TreeStack.rootMessageTerm (pathTree n hn) C r q
  rw [TreeStack.score, TreeStack.rootMessageSum, hsum]
  ring

private theorem path_score_last_eq
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hjn : j + 2 = n) :
    TreeStack.score (pathTree n hn) C ⟨j + 1, by omega⟩ =
      (C ⟨j + 1, by omega⟩ : Int) +
        TreeStack.rootMessageTerm (pathTree n hn) C
          ⟨j + 1, by omega⟩ ⟨j, by omega⟩ := by
  let r : Fin n := ⟨j + 1, by omega⟩
  let l : Fin n := ⟨j, by omega⟩
  have hsum :
      (∑ u : Fin n,
        TreeStack.rootMessageTerm (pathTree n hn) C r u) =
        TreeStack.rootMessageTerm (pathTree n hn) C r l := by
    rw [Fintype.sum_eq_single l]
    intro u hul
    have hnadj : ¬ (pathTree n hn).graph.Adj u r := by
      intro hadj
      rw [pathTree_graph, SimpleGraph.pathGraph_adj] at hadj
      rcases hadj with hleft | hright
      · apply hul
        apply Fin.ext
        simp [r, l] at hleft ⊢
        omega
      · have hu := u.isLt
        simp [r] at hright
        omega
    have hnadj' : ¬ (SimpleGraph.pathGraph n).Adj u r := by
      simpa [pathTree_graph] using hnadj
    rw [TreeStack.rootMessageTerm]
    simp only [dif_neg hnadj']
  change
    TreeStack.score (pathTree n hn) C r =
      (C r : Int) +
        TreeStack.rootMessageTerm (pathTree n hn) C r l
  rw [TreeStack.score, TreeStack.rootMessageSum, hsum]

noncomputable def pathPrefixMass {n : Nat}
    (C : TreeStack.Configuration (Fin n))
    (k : Nat) (hk : k < n) : Nat :=
  ∑ i : Fin (k + 1),
    C (Fin.castLE (Nat.succ_le_iff.mpr hk) i)

private theorem pathPrefixMass_succ
    {n : Nat} (C : TreeStack.Configuration (Fin n))
    (k : Nat) (hk : k + 1 < n) :
    pathPrefixMass C (k + 1) hk =
      pathPrefixMass C k (by omega) + C ⟨k + 1, hk⟩ := by
  rw [pathPrefixMass, Fin.sum_univ_castSucc]
  change
    (∑ i : Fin (k + 1),
      C (Fin.castLE (Nat.succ_le_iff.mpr hk) i.castSucc)) +
        C (Fin.castLE (Nat.succ_le_iff.mpr hk) (Fin.last (k + 1))) =
      pathPrefixMass C k (by omega) + C ⟨k + 1, hk⟩
  congr 1
  rw [pathPrefixMass]
  apply Finset.sum_congr rfl
  intro i hi
  congr

private theorem pathPrefixMass_add_last_eq_mass
    {n : Nat} (C : TreeStack.Configuration (Fin n))
    (j : Nat) (hjn : j + 2 = n) :
    pathPrefixMass C j (by omega) + C ⟨j + 1, by omega⟩ =
      TreeStack.mass C := by
  subst n
  rw [TreeStack.mass, Fin.sum_univ_castSucc]
  change
    pathPrefixMass C j (by omega) + C ⟨j + 1, by omega⟩ =
      (∑ i : Fin (j + 1), C i.castSucc) + C (Fin.last (j + 1))
  congr 1
  rw [pathPrefixMass]
  apply Finset.sum_congr rfl
  intro i hi
  congr

noncomputable def leftPrefixDissipation
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (k : Nat) (hk : k + 1 < n) : Int :=
  (pathPrefixMass C k (by omega) : Int) -
    TreeStack.OrientedBranch.messageContribution
      ((LeftPath.leftBranch n hn k hk).branchMessage C)

private theorem leftPrefixDissipation_le_of_noDeep
    {n h : Nat} (hn2 : 2 <= n)
    (C : TreeStack.Configuration (Fin n))
    (hh : 1 <= h)
    (hnonstack :
      ¬ TreeStack.Stackable (pathTree n (by omega)).graph C)
    (hnodeep :
      ¬ HasDirectedPathMessageAtMost (n := n) (by omega) C h) :
    ∀ (k : Nat) (hk : k + 1 < n),
      leftPrefixDissipation (by omega) C k hk <=
        (k + 1 : Int) * ((h / 2 + 1 : Nat) : Int) := by
  have hall :
      ∀ r : Fin n,
        TreeStack.score (pathTree n (by omega)) C r <= 0 :=
    (TreeStack.not_stackable_iff_all_scores_nonpos
      (pathTree n (by omega)) C).1 hnonstack
  intro k
  induction k with
  | zero =>
      intro hk
      let r : Fin n := ⟨0, by omega⟩
      let q : Fin n := ⟨1, by omega⟩
      have hqr : (pathTree n (by omega)).graph.Adj q r := by
        rw [pathTree_graph, SimpleGraph.pathGraph_adj]
        exact Or.inr rfl
      have hright :=
        rootMessageTerm_gt_neg_of_noDeep
          (n := n) (h := h) (by omega) C hh hnodeep r q hqr
      have hs := hall r
      have hscore :=
        path_score_zero_eq (n := n) (by omega) C (by omega)
      change
        TreeStack.score (pathTree n (by omega)) C r =
          (C r : Int) +
            TreeStack.rootMessageTerm (pathTree n (by omega)) C r q at hscore
      rw [hscore] at hs
      have hy : (C r : Int) <= (h : Int) - 1 := by omega
      let B := LeftPath.leftBranch n (by omega) 0 hk
      have hstep :
          B.branchMessage C = pathStep TreeStack.EMPTY (C r) := by
        dsimp [B, r]
        rw [LeftPath.leftBranch_branchMessage_eq_prefixScan
          (by omega) C 0 hk]
        rfl
      have houtTerm :=
        rootMessageTerm_gt_neg_of_noDeep
          (n := n) (h := h) (by omega) C hh hnodeep
          B.parent B.root B.adj
      rw [rootMessageTerm_eq_branchContribution C B, hstep] at houtTerm
      have hlocal :=
        pathStep_dissipation_le hh TreeStack.EMPTY (C r)
          (by
            simpa [TreeStack.OrientedBranch.messageContribution,
              TreeStack.EMPTY] using hy)
          houtTerm
      have hprefix0 :
          pathPrefixMass C 0 (by omega) = C r := by
        simp [pathPrefixMass, r]
      dsimp [leftPrefixDissipation]
      rw [hprefix0, hstep]
      simpa [TreeStack.EMPTY,
        TreeStack.OrientedBranch.messageContribution] using hlocal
  | succ j ih =>
      intro hk
      have hprevEdge : j + 1 < n := by omega
      have hnextEdge : (j + 1) + 1 < n := hk
      let Bprev := LeftPath.leftBranch n (by omega) j hprevEdge
      let Bnext := LeftPath.leftBranch n (by omega) (j + 1) hk
      let r : Fin n := ⟨j + 1, by omega⟩
      let q : Fin n := ⟨j + 2, by omega⟩
      have hqr : (pathTree n (by omega)).graph.Adj q r := by
        rw [pathTree_graph, SimpleGraph.pathGraph_adj]
        exact Or.inr rfl
      have hright :=
        rootMessageTerm_gt_neg_of_noDeep
          (n := n) (h := h) (by omega) C hh hnodeep r q hqr
      have hs := hall r
      have hscore :=
        path_score_interior_eq (n := n) (by omega) C j (by omega)
      change
        TreeStack.score (pathTree n (by omega)) C r =
          (C r : Int) +
            TreeStack.rootMessageTerm (pathTree n (by omega)) C
              r Bprev.root +
            TreeStack.rootMessageTerm (pathTree n (by omega)) C r q at hscore
      have hleft :
          TreeStack.rootMessageTerm (pathTree n (by omega)) C
              r Bprev.root =
            TreeStack.OrientedBranch.messageContribution
              (Bprev.branchMessage C) := by
        have hparent : Bprev.parent = r := by
          apply Fin.ext
          rfl
        rw [← hparent]
        exact rootMessageTerm_eq_branchContribution C Bprev
      rw [hscore, hleft] at hs
      have hy :
          (C r : Int) +
              TreeStack.OrientedBranch.messageContribution
                (Bprev.branchMessage C) <=
            (h : Int) - 1 := by
        omega
      have hstep :
          Bnext.branchMessage C =
            pathStep (Bprev.branchMessage C) (C r) := by
        dsimp [Bnext, Bprev, r]
        exact LeftPath.leftBranch_branchMessage_succ
          (by omega) C j hk
      have houtTerm :=
        rootMessageTerm_gt_neg_of_noDeep
          (n := n) (h := h) (by omega) C hh hnodeep
          Bnext.parent Bnext.root Bnext.adj
      rw [rootMessageTerm_eq_branchContribution C Bnext, hstep] at houtTerm
      have hlocal :=
        pathStep_dissipation_le hh (Bprev.branchMessage C) (C r)
          hy houtTerm
      have hih := ih hprevEdge
      have hmass :=
        pathPrefixMass_succ C j (by omega)
      calc
        leftPrefixDissipation (by omega) C (j + 1) hk =
            leftPrefixDissipation (by omega) C j hprevEdge +
              ((C r : Int) +
                TreeStack.OrientedBranch.messageContribution
                  (Bprev.branchMessage C) -
                TreeStack.OrientedBranch.messageContribution
                  (pathStep (Bprev.branchMessage C) (C r))) := by
                  dsimp [leftPrefixDissipation]
                  rw [hmass, hstep]
                  push_cast
                  ring
        _ <=
            (j + 1 : Int) * ((h / 2 + 1 : Nat) : Int) +
              ((h / 2 + 1 : Nat) : Int) := by
                exact add_le_add hih hlocal
        _ = (j + 2 : Int) * ((h / 2 + 1 : Nat) : Int) := by
              ring

private theorem mass_le_threshold_of_nonstackable_noDeep
    {n h : Nat} (hn2 : 2 <= n)
    (C : TreeStack.Configuration (Fin n))
    (hh : 1 <= h)
    (hnonstack :
      ¬ TreeStack.Stackable (pathTree n (by omega)).graph C)
    (hnodeep :
      ¬ HasDirectedPathMessageAtMost (n := n) (by omega) C h) :
    TreeStack.mass C <= (n - 1) * (h / 2 + 1) := by
  let j := n - 2
  have hjn : j + 2 = n := by
    dsimp [j]
    omega
  have hjedge : j + 1 < n := by omega
  let B := LeftPath.leftBranch n (by omega) j hjedge
  let r : Fin n := ⟨j + 1, by omega⟩
  have hall :
      ∀ v : Fin n,
        TreeStack.score (pathTree n (by omega)) C v <= 0 :=
    (TreeStack.not_stackable_iff_all_scores_nonpos
      (pathTree n (by omega)) C).1 hnonstack
  have hs := hall r
  have hscore :=
    path_score_last_eq (n := n) (by omega) C j hjn
  change
    TreeStack.score (pathTree n (by omega)) C r =
      (C r : Int) +
        TreeStack.rootMessageTerm (pathTree n (by omega)) C r B.root at hscore
  have hparent : B.parent = r := by
    apply Fin.ext
    dsimp [B, r, j]
    omega
  have hleft :
      TreeStack.rootMessageTerm (pathTree n (by omega)) C r B.root =
        TreeStack.OrientedBranch.messageContribution (B.branchMessage C) := by
    rw [← hparent]
    exact rootMessageTerm_eq_branchContribution C B
  rw [hscore, hleft] at hs
  have hmassEq :=
    pathPrefixMass_add_last_eq_mass C j hjn
  have hmassEqZ :
      (TreeStack.mass C : Int) =
        (pathPrefixMass C j (by omega) : Int) + (C r : Int) := by
    have hz := congrArg (fun z : Nat => (z : Int)) hmassEq
    push_cast at hz
    simpa [r, add_comm] using hz.symm
  have hmassD :
      (TreeStack.mass C : Int) <=
        leftPrefixDissipation (by omega) C j hjedge := by
    dsimp [leftPrefixDissipation]
    rw [hmassEqZ]
    dsimp [r] at hs
    linarith
  have hdiss :=
    leftPrefixDissipation_le_of_noDeep
      (n := n) (h := h) hn2 C hh hnonstack hnodeep j hjedge
  have hboundZ :
      (TreeStack.mass C : Int) <=
        ((n - 1 : Nat) : Int) * ((h / 2 + 1 : Nat) : Int) := by
    have hjfactor : ((j + 1 : Nat) : Int) = ((n - 1 : Nat) : Int) := by
      dsimp [j]
      omega
    rw [hjfactor] at hdiss
    exact le_trans hmassD hdiss
  exact_mod_cast hboundZ

/--
Session 5 global deep-message necessity on a finite path.

For a positive-mass nonstackable configuration on `P_n`, if `h >= 2` and
the total mass is larger than
`(n - 1) * (floor(h / 2) + 1)`, then some directed path message is at most
`-h`.
-/
theorem nonstackable_exists_directedMessage_le
    {n h : Nat} (hn2 : 2 <= n)
    (C : TreeStack.Configuration (Fin n))
    (hmassPos : 0 < TreeStack.mass C)
    (hnonstack :
      ¬ TreeStack.Stackable (pathTree n (by omega)).graph C)
    (hh : 2 <= h)
    (hlarge :
      (n - 1) * (h / 2 + 1) < TreeStack.mass C) :
    HasDirectedPathMessageAtMost (n := n) (by omega) C h := by
  by_contra hnodeep
  have hbound :=
    mass_le_threshold_of_nonstackable_noDeep
      (n := n) (h := h) hn2 C (by omega) hnonstack hnodeep
  omega

/--
At fixed total mass `n * mu` with `mu >= 1`, nonstackability forces an
actual directed path message at most `-(2*mu - 1)`.

The internal dissipation bound is valid already for `h >= 1`; this covers
the edge case `mu = 1` without weakening the exact target.
-/
theorem nonstackable_total_mul_exists_directedMessage_le
    {n mu : Nat} (hn2 : 2 <= n)
    (C : TreeStack.Configuration (Fin n))
    (hmu : 1 <= mu)
    (hmass : TreeStack.mass C = n * mu)
    (hnonstack :
      ¬ TreeStack.Stackable (pathTree n (by omega)).graph C) :
    ∃ (r u : Fin n)
        (hu : (pathTree n (by omega)).graph.Adj u r)
        (m : Int),
      (TreeStack.incidentBranch (pathTree n (by omega)) r u hu).branchMessage C =
          some m ∧
        m <= -(2 * (mu : Int) - 1) := by
  let h : Nat := 2 * mu - 1
  have hh : 1 <= h := by
    dsimp [h]
    omega
  have hcap : h / 2 + 1 = mu := by
    dsimp [h]
    omega
  have hnlt : n - 1 < n := by omega
  have hlarge : (n - 1) * (h / 2 + 1) < TreeStack.mass C := by
    rw [hcap, hmass]
    exact Nat.mul_lt_mul_of_pos_right hnlt (by omega)
  have hdeep :
      HasDirectedPathMessageAtMost (n := n) (by omega) C h := by
    by_contra hnodeep
    have hbound :=
      mass_le_threshold_of_nonstackable_noDeep
        (n := n) (h := h) hn2 C hh hnonstack hnodeep
    omega
  rcases hdeep with ⟨r, u, hu, m, hmsg, hm⟩
  refine ⟨r, u, hu, m, hmsg, ?_⟩
  dsimp [h] at hm
  push_cast at hm
  omega

end ProbStack
