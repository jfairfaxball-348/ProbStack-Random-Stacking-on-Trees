module

public import Mathlib

public section

/-!
# Palomar statement surface for ProbStack P6

This file states the deterministic finite-path deep-message necessity theorem
without importing the ProbStack or TreeStack proof developments.

A configuration is a function `Fin n → Nat`.  Stackability is defined by the
ordinary legal pebbling move: remove two pebbles from one endpoint of a path
edge and add one pebble at the other endpoint.  A stacked configuration has
positive support at exactly one root.

Directed messages use the exact categorical message type `Option Int`:
`none` is EMPTY and is distinct from every integer message, including
`some 0`.  The transfer map and path scan below are exactly the finite-path
specialization of the TreeStack message recursion.  The directed message
`u → r` uses the left scan when `u+1=r` and the reversed right scan when
`r+1=u`, so both path orientations are included.
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

/--
The actual directed message on the ordered adjacent pair `u → r`.
For non-adjacent pairs the value is defined as EMPTY only to make this a total
function; every theorem below quantifies an adjacency proof.
-/
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

@[expose] def ProbStack.Palomar.Stackable {n : Nat} (C : Configuration n) : Prop :=
  ∃ r, StackableAt C r

/--
Global deep-message necessity on a finite path.

For a positive-mass nonstackable configuration on `P_n`, if `h >= 2` and
the mass is larger than `(n-1) * (floor(h/2)+1)`, some actual directed path
message is an integer at most `-h`.
-/
theorem ProbStack.Palomar.nonstackable_exists_directedMessage_le
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
  sorry

/--
Exact fixed-total corollary of P6.

If `mass C = n * mu` with `mu >= 1` and the path configuration is
nonstackable, some actual directed path message is at most
`-(2*mu-1)`.
-/
theorem ProbStack.Palomar.nonstackable_total_mul_exists_directedMessage_le
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
  sorry

