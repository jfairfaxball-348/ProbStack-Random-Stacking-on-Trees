module

public import ProbStack

public section

/-!
# Palomar solution surface for ProbStack P6

The definitions below intentionally duplicate the protected Challenge API.
Comparator checks their exported forms.  The two advertised theorems are then
proved from the already-formalised ProbStack P6 theorem, with explicit bridge
lemmas identifying the path-only message scan and ordinary pebbling
stackability with the TreeStack/ProbStack implementation.
-/

abbrev ProbStack.Palomar.Configuration (n : Nat) := Fin n → Nat

open ProbStack.Palomar

@[expose] def ProbStack.Palomar.mass {n : Nat} (C : Configuration n) : Nat :=
  ∑ v, C v

@[expose] def ProbStack.Palomar.transfer (x : Int) : Int :=
  if x <= 1 then
    2 * x - 3
  else if x = 2 then
    1
  else if x = 3 then
    0
  else if x % 2 = 0 then
    x / 2
  else
    (x - 3) / 2

abbrev ProbStack.Palomar.Message := Option Int

@[expose] def ProbStack.Palomar.EMPTY : Message := none

@[expose] def ProbStack.Palomar.pathStep (m : Message) (x : Nat) : Message :=
  match m with
  | none =>
      if x = 0 then EMPTY
      else some (transfer (x : Int))
  | some z => some (transfer (z + (x : Int)))

@[expose] def ProbStack.Palomar.prefixScan {n : Nat} (C : Configuration n) :
    (k : Nat) → k < n → Message
  | 0, hk => pathStep EMPTY (C ⟨0, hk⟩)
  | j + 1, hk =>
      pathStep
        (prefixScan C j (by omega))
        (C ⟨j + 1, hk⟩)

@[expose] def ProbStack.Palomar.reverseConfig {n : Nat} (C : Configuration n) : Configuration n :=
  fun i => C i.rev

@[expose] def ProbStack.Palomar.directedMessage {n : Nat} (C : Configuration n) (u r : Fin n) : Message :=
  if hleft : u.val + 1 = r.val then
    prefixScan C u.val u.isLt
  else if hright : r.val + 1 = u.val then
    prefixScan (reverseConfig C) (n - (u.val + 1)) (by omega)
  else
    EMPTY

@[expose] def ProbStack.Palomar.move {n : Nat} (C : Configuration n) (u v : Fin n) : Configuration n :=
  Function.update (Function.update C u (C u - 2)) v (C v + 1)

@[expose] def ProbStack.Palomar.PebbleStep {n : Nat} (C D : Configuration n) : Prop :=
  ∃ u v : Fin n,
    (SimpleGraph.pathGraph n).Adj u v ∧
      2 <= C u ∧
      D = move C u v

@[expose] def ProbStack.Palomar.Reach {n : Nat} (C D : Configuration n) : Prop :=
  Relation.ReflTransGen PebbleStep C D

@[expose] def ProbStack.Palomar.StackedAt {n : Nat} (C : Configuration n) (r : Fin n) : Prop :=
  0 < C r ∧ ∀ v, v ≠ r → C v = 0

@[expose] def ProbStack.Palomar.StackableAt {n : Nat} (C : Configuration n) (r : Fin n) : Prop :=
  ∃ D, Reach C D ∧ StackedAt D r

def ProbStack.Palomar.Stackable {n : Nat} (C : Configuration n) : Prop :=
  ∃ r, StackableAt C r

private theorem mass_eq_treeStack {n : Nat} (C : Configuration n) :
    mass C = TreeStack.mass C := by
  rfl

private theorem stackable_iff_treeStack {n : Nat} (C : Configuration n) :
    Stackable C ↔ TreeStack.Stackable (SimpleGraph.pathGraph n) C := by
  rfl

private theorem prefixScan_eq_probStack {n : Nat} (C : Configuration n) :
    ∀ (k : Nat) (hk : k < n),
      prefixScan C k hk = ProbStack.LeftPath.prefixScan C k hk := by
  intro k
  induction k with
  | zero =>
      intro hk
      rfl
  | succ j ih =>
      intro hk
      change
        pathStep (prefixScan C j (by omega)) (C ⟨j + 1, hk⟩) =
          ProbStack.pathStep
            (ProbStack.LeftPath.prefixScan C j (by omega))
            (C ⟨j + 1, hk⟩)
      rw [ih (by omega)]
      rfl

private theorem orientedBranch_eq_of_root_parent_eq
    {V : Type*} [Fintype V] {T : TreeStack.FiniteTree V}
    (A B : TreeStack.OrientedBranch T)
    (hroot : A.root = B.root)
    (hparent : A.parent = B.parent) :
    A = B := by
  cases A with
  | mk ar ap aadj =>
      cases B with
      | mk br bp badj =>
          simp only at hroot hparent
          subst br
          subst bp
          rfl

private theorem directedMessage_eq_incident
    {n : Nat} (hn : 0 < n) (C : Configuration n)
    (r u : Fin n)
    (hu : (ProbStack.pathTree n hn).graph.Adj u r) :
    directedMessage C u r =
      (TreeStack.incidentBranch (ProbStack.pathTree n hn) r u hu).branchMessage C := by
  have hpath : (SimpleGraph.pathGraph n).Adj u r := by
    simpa [ProbStack.pathTree_graph] using hu
  rw [SimpleGraph.pathGraph_adj] at hpath
  rcases hpath with hleft | hright
  · have hk : u.val + 1 < n := by
      omega
    have hB :
        TreeStack.incidentBranch (ProbStack.pathTree n hn) r u hu =
          ProbStack.LeftPath.leftBranch n hn u.val hk := by
      apply orientedBranch_eq_of_root_parent_eq
      · apply Fin.ext
        rfl
      · apply Fin.ext
        exact hleft.symm
    calc
      directedMessage C u r =
          prefixScan C u.val u.isLt := by
            simp [directedMessage, hleft]
      _ = ProbStack.LeftPath.prefixScan C u.val u.isLt :=
            prefixScan_eq_probStack C u.val u.isLt
      _ =
          (ProbStack.LeftPath.leftBranch n hn u.val hk).branchMessage C := by
            symm
            simpa using
              ProbStack.LeftPath.leftBranch_branchMessage_eq_prefixScan
                hn C u.val hk
      _ =
          (TreeStack.incidentBranch (ProbStack.pathTree n hn) r u hu).branchMessage C := by
            rw [hB]
  · have hnotleft : ¬ u.val + 1 = r.val := by
      omega
    let k : Nat := n - (u.val + 1)
    have hk : k + 1 < n := by
      dsimp [k]
      omega
    have hB :
        TreeStack.incidentBranch (ProbStack.pathTree n hn) r u hu =
          ProbStack.RightPath.rightBranch n hn k hk := by
      apply orientedBranch_eq_of_root_parent_eq
      · apply Fin.ext
        simp [TreeStack.incidentBranch, ProbStack.RightPath.rightBranch,
          k, Fin.val_rev]
        omega
      · apply Fin.ext
        simp [TreeStack.incidentBranch, ProbStack.RightPath.rightBranch,
          k, Fin.val_rev]
        omega
    calc
      directedMessage C u r =
          prefixScan (reverseConfig C) k (by omega) := by
            simp [directedMessage, hnotleft, hright, k]
      _ =
          ProbStack.LeftPath.prefixScan
            (reverseConfig C) k (by omega) :=
            prefixScan_eq_probStack (reverseConfig C) k (by omega)
      _ =
          ProbStack.LeftPath.prefixScan
            (ProbStack.RightPath.reverseConfig C) k (by omega) := by
            rfl
      _ =
          (ProbStack.RightPath.rightBranch n hn k hk).branchMessage C := by
            symm
            simpa using
              ProbStack.RightPath.rightBranch_branchMessage_eq_reversePrefixScan
                hn C k hk
      _ =
          (TreeStack.incidentBranch (ProbStack.pathTree n hn) r u hu).branchMessage C := by
            rw [hB]

theorem nonstackable_exists_directedMessage_le
    {n h : Nat} (hn2 : 2 <= n)
    (C : Configuration n)
    (hmassPos : 0 < mass C)
    (hnonstack : ¬ Stackable C)
    (hh : 2 <= h)
    (hlarge : (n - 1) * (h / 2 + 1) < mass C) :
    ∃ (r u : Fin n)
        (hu : (SimpleGraph.pathGraph n).Adj u r)
        (m : Int),
      directedMessage C u r = some m ∧
        m <= -(h : Int) := by
  have hnonstack' :
      ¬ TreeStack.Stackable (ProbStack.pathTree n (by omega)).graph C := by
    intro hs
    apply hnonstack
    apply (stackable_iff_treeStack C).2
    simpa [ProbStack.pathTree_graph] using hs
  have hdeep :=
    ProbStack.nonstackable_exists_directedMessage_le
      hn2 C
      (by simpa [mass_eq_treeStack C] using hmassPos)
      hnonstack' hh
      (by simpa [mass_eq_treeStack C] using hlarge)
  rcases hdeep with ⟨r, u, hu, m, hmsg, hm⟩
  have huPath : (SimpleGraph.pathGraph n).Adj u r := by
    simpa [ProbStack.pathTree_graph] using hu
  refine ⟨r, u, huPath, m, ?_, hm⟩
  rw [directedMessage_eq_incident (by omega) C r u hu]
  exact hmsg

theorem nonstackable_total_mul_exists_directedMessage_le
    {n mu : Nat} (hn2 : 2 <= n)
    (C : Configuration n)
    (hmu : 1 <= mu)
    (hmass : mass C = n * mu)
    (hnonstack : ¬ Stackable C) :
    ∃ (r u : Fin n)
        (hu : (SimpleGraph.pathGraph n).Adj u r)
        (m : Int),
      directedMessage C u r = some m ∧
        m <= -(2 * (mu : Int) - 1) := by
  have hnonstack' :
      ¬ TreeStack.Stackable (ProbStack.pathTree n (by omega)).graph C := by
    intro hs
    apply hnonstack
    apply (stackable_iff_treeStack C).2
    simpa [ProbStack.pathTree_graph] using hs
  have hmass' : TreeStack.mass C = n * mu := by
    simpa [mass_eq_treeStack C] using hmass
  have hdeep :=
    ProbStack.nonstackable_total_mul_exists_directedMessage_le
      hn2 C hmu hmass' hnonstack'
  rcases hdeep with ⟨r, u, hu, m, hmsg, hm⟩
  have huPath : (SimpleGraph.pathGraph n).Adj u r := by
    simpa [ProbStack.pathTree_graph] using hu
  refine ⟨r, u, huPath, m, ?_, hm⟩
  rw [directedMessage_eq_incident (by omega) C r u hu]
  exact hmsg

