import ProbStack.PathFront

namespace ProbStack

/--
Reverse-dyadic affine input cost for the global half-contraction recurrence.
For [x_1,...,x_k], the weights are 1,2,...,2^(k-1).
-/
def affineInputCost : List Nat → Int
  | [] => 0
  | x :: xs => (x : Int) + 2 * affineInputCost xs

theorem two_mul_activeStep_le (m : Int) (x : Nat) :
    2 * activeStep m x <= m + (x : Int) := by
  have hhalf := F_le_half (m + (x : Int))
  have hdiv : 2 * ((m + (x : Int)) / 2) <= m + (x : Int) := by
    omega
  unfold activeStep
  omega

/--
Iterated global half-contraction, with all integer/parity effects retained on
the left-hand side.
-/
theorem activeScan_affine_bound (m : Int) (xs : List Nat) :
    (2 : Int) ^ xs.length * activeScan m xs <=
      m + affineInputCost xs := by
  induction xs generalizing m with
  | nil =>
      simp [activeScan, affineInputCost]
  | cons x xs ih =>
      have htail := ih (activeStep m x)
      have htail2 :
          2 * ((2 : Int) ^ xs.length *
            activeScan (activeStep m x) xs) <=
          2 * (activeStep m x + affineInputCost xs) :=
        mul_le_mul_of_nonneg_left htail (by norm_num)
      have hstep := two_mul_activeStep_le m x
      calc
        (2 : Int) ^ (x :: xs).length *
            activeScan m (x :: xs) =
            2 * ((2 : Int) ^ xs.length *
              activeScan (activeStep m x) xs) := by
                simp only [List.length_cons, activeScan, pow_succ]
                ring
        _ <= 2 * (activeStep m x + affineInputCost xs) := htail2
        _ <= (m + (x : Int)) + 2 * affineInputCost xs := by
          omega
        _ = m + affineInputCost (x :: xs) := by
          simp [affineInputCost]
          ring

/--
An explicit positive-scale descent event.  It is a reverse-dyadic weighted
simplex in the occupancies, not a hitting-time or Markov-chain event.
-/
def PositiveDescentEvent (mu : Nat) (xs : List Nat) : Prop :=
  2 * (mu : Int) + affineInputCost xs <
    (2 : Int) ^ xs.length

theorem positiveDescentEvent_forces_nonpositive
    {mu : Nat} {m : Int} {xs : List Nat}
    (hm : m <= 2 * (mu : Int))
    (hdescent : PositiveDescentEvent mu xs) :
    activeScan m xs <= 0 := by
  have hbound := activeScan_affine_bound m xs
  have hp : 0 < (2 : Int) ^ xs.length := by
    positivity
  have hlt :
      (2 : Int) ^ xs.length * activeScan m xs <
        (2 : Int) ^ xs.length := by
    unfold PositiveDescentEvent at hdescent
    omega
  have hlt' :
      (2 : Int) ^ xs.length * activeScan m xs <
        (2 : Int) ^ xs.length * 1 := by
    simpa using hlt
  have hscan : activeScan m xs < 1 :=
    (Int.mul_lt_mul_left hp).mp hlt'
  omega

/--
A completely explicit low-phase dyadic budget.  The state variable is only a
certified numerical deficit lower bound.  At each coordinate x the visible
constraint is x <= D-2, after which the certified bound becomes 2(D-x).
-/
def LowBudget : Int → List Nat → Prop
  | _, [] => True
  | D, x :: xs =>
      (x : Int) <= D - 2 ∧
        LowBudget (2 * (D - (x : Int))) xs

/-- The deterministic final deficit certified by a LowBudget block. -/
def lowBudgetFinal : Int → List Nat → Int
  | D, [] => D
  | D, x :: xs =>
      lowBudgetFinal (2 * (D - (x : Int))) xs

theorem lowBudget_lowRun_and_deficit_ge
    {m D : Int} {xs : List Nat}
    (hseed : D <= deficit m)
    (hbudget : LowBudget D xs) :
    LowRun m xs ∧
      lowBudgetFinal D xs <= deficit (activeScan m xs) := by
  induction xs generalizing m D with
  | nil =>
      constructor
      · simp [LowRun]
      · simpa [lowBudgetFinal, activeScan] using hseed
  | cons x xs ih =>
      change
        (x : Int) <= D - 2 ∧
          LowBudget (2 * (D - (x : Int))) xs at hbudget
      rcases hbudget with ⟨hcap, hrest⟩
      have hlow : m + (x : Int) <= 1 := by
        unfold deficit at hseed
        omega
      have hnext :
          2 * (D - (x : Int)) <=
            deficit (activeStep m x) := by
        rw [deficit_activeStep_of_low hlow]
        omega
      have htail :=
        ih (m := activeStep m x)
          (D := 2 * (D - (x : Int))) hnext hrest
      constructor
      · change
          m + (x : Int) <= 1 ∧
            LowRun (activeStep m x) xs
        exact ⟨hlow, htail.1⟩
      · simpa [lowBudgetFinal, activeScan] using htail.2

/--
The Session-14 scalar seed certificate.  It separates:
* reverse-dyadic positive descent from [mu,2mu] to a nonpositive message;
* exact low-phase dyadic deficit amplification from the universal deficit 3.

Every constrained coordinate is exposed through one of those two arithmetic
predicates.
-/
def ExplicitDeepSeedEvent
    (mu : Nat) (D : Int)
    (descent amplification : List Nat) : Prop :=
  PositiveDescentEvent mu descent ∧
    LowBudget 3 amplification ∧
    D <= lowBudgetFinal 3 amplification

def explicitSeedSupportLength
    (descent amplification : List Nat) : Nat :=
  descent.length + amplification.length

def explicitSeedMass
    (descent amplification : List Nat) : Nat :=
  descent.sum + amplification.sum

theorem explicitDeepSeedEvent_uniform
    {mu : Nat} {D : Int}
    {descent amplification : List Nat}
    (hevent :
      ExplicitDeepSeedEvent mu D descent amplification) :
    UniformDeepSeedBlock
      (mu : Int) (2 * (mu : Int)) D
      (descent ++ amplification) := by
  unfold ExplicitDeepSeedEvent at hevent
  rcases hevent with ⟨hdescent, hamp, htarget⟩
  unfold UniformDeepSeedBlock
  intro m _hmlo hmhi
  have hnonpos :
      activeScan m descent <= 0 :=
    positiveDescentEvent_forces_nonpositive hmhi hdescent
  have hthree :
      3 <= deficit (activeScan m descent) := by
    unfold deficit
    omega
  have hlow :=
    lowBudget_lowRun_and_deficit_ge
      (m := activeScan m descent) (D := 3)
      hthree hamp
  unfold DeepSeed
  rw [activeScan_append]
  exact le_trans htarget hlow.2

/--
Coordinatewise finite cap event.  This exposes every constrained occupancy:
the two lists must have the same support and each actual coordinate is at most
its displayed cap.
-/
def CoordwiseLe : List Nat → List Nat → Prop
  | [], [] => True
  | x :: xs, a :: caps =>
      x <= a ∧ CoordwiseLe xs caps
  | _, _ => False

theorem coordwiseLe_length
    {xs caps : List Nat} (h : CoordwiseLe xs caps) :
    xs.length = caps.length := by
  induction xs generalizing caps with
  | nil =>
      cases caps <;> simp [CoordwiseLe] at h ⊢
  | cons x xs ih =>
      cases caps with
      | nil =>
          simp [CoordwiseLe] at h
      | cons a caps =>
          change x <= a ∧ CoordwiseLe xs caps at h
          simp [ih h.2]

theorem coordwiseLe_sum
    {xs caps : List Nat} (h : CoordwiseLe xs caps) :
    xs.sum <= caps.sum := by
  induction xs generalizing caps with
  | nil =>
      cases caps <;> simp [CoordwiseLe] at h ⊢
  | cons x xs ih =>
      cases caps with
      | nil =>
          simp [CoordwiseLe] at h
      | cons a caps =>
          change x <= a ∧ CoordwiseLe xs caps at h
          have htail := ih h.2
          simp only [List.sum_cons]
          omega

theorem affineInputCost_mono
    {xs caps : List Nat} (h : CoordwiseLe xs caps) :
    affineInputCost xs <= affineInputCost caps := by
  induction xs generalizing caps with
  | nil =>
      cases caps <;> simp [CoordwiseLe, affineInputCost] at h ⊢
  | cons x xs ih =>
      cases caps with
      | nil =>
          simp [CoordwiseLe] at h
      | cons a caps =>
          change x <= a ∧ CoordwiseLe xs caps at h
          have hx : (x : Int) <= (a : Int) := by
            exact_mod_cast h.1
          have htail := ih h.2
          simp only [affineInputCost]
          omega

theorem positiveDescentEvent_of_coordwise
    {mu : Nat} {xs caps : List Nat}
    (hcap : PositiveDescentEvent mu caps)
    (hle : CoordwiseLe xs caps) :
    PositiveDescentEvent mu xs := by
  have hlen := coordwiseLe_length hle
  have hcost := affineInputCost_mono hle
  unfold PositiveDescentEvent at hcap ⊢
  rw [hlen]
  omega

theorem lowBudget_mono
    {D E : Int} {xs : List Nat}
    (hDE : D <= E) (hbudget : LowBudget D xs) :
    LowBudget E xs := by
  induction xs generalizing D E with
  | nil =>
      simp [LowBudget]
  | cons x xs ih =>
      change
        (x : Int) <= D - 2 ∧
          LowBudget (2 * (D - (x : Int))) xs at hbudget
      change
        (x : Int) <= E - 2 ∧
          LowBudget (2 * (E - (x : Int))) xs
      constructor
      · omega
      · exact ih (by omega) hbudget.2

theorem lowBudgetFinal_mono
    {D E : Int} {xs : List Nat}
    (hDE : D <= E) (hbudget : LowBudget D xs) :
    lowBudgetFinal D xs <= lowBudgetFinal E xs := by
  induction xs generalizing D E with
  | nil =>
      simpa [lowBudgetFinal] using hDE
  | cons x xs ih =>
      change
        (x : Int) <= D - 2 ∧
          LowBudget (2 * (D - (x : Int))) xs at hbudget
      have htail :=
        ih (D := 2 * (D - (x : Int)))
          (E := 2 * (E - (x : Int)))
          (by omega) hbudget.2
      simpa [lowBudgetFinal] using htail

theorem lowBudget_of_coordwise
    {D : Int} {xs caps : List Nat}
    (hcap : LowBudget D caps)
    (hle : CoordwiseLe xs caps) :
    LowBudget D xs ∧
      lowBudgetFinal D caps <= lowBudgetFinal D xs := by
  induction xs generalizing caps D with
  | nil =>
      cases caps with
      | nil =>
          simp [LowBudget, lowBudgetFinal]
      | cons a caps =>
          simp [CoordwiseLe] at hle
  | cons x xs ih =>
      cases caps with
      | nil =>
          simp [CoordwiseLe] at hle
      | cons a caps =>
          change x <= a ∧ CoordwiseLe xs caps at hle
          change
            (a : Int) <= D - 2 ∧
              LowBudget (2 * (D - (a : Int))) caps at hcap
          have hxa : (x : Int) <= (a : Int) := by
            exact_mod_cast hle.1
          have hthreshold :
              2 * (D - (a : Int)) <=
                2 * (D - (x : Int)) := by
            omega
          have hcapActual :
              LowBudget (2 * (D - (x : Int))) caps :=
            lowBudget_mono hthreshold hcap.2
          have htail :=
            ih (D := 2 * (D - (x : Int)))
              hcapActual hle.2
          have hcapFinal :
              lowBudgetFinal (2 * (D - (a : Int))) caps <=
                lowBudgetFinal (2 * (D - (x : Int))) caps :=
            lowBudgetFinal_mono hthreshold hcap.2
          constructor
          · change
              (x : Int) <= D - 2 ∧
                LowBudget (2 * (D - (x : Int))) xs
            exact ⟨by omega, htail.1⟩
          · simpa [lowBudgetFinal] using
              (le_trans hcapFinal htail.2)

/--
A coordinate-cap certificate is sufficient for the scalar deep-seed event.
This is the finite seam used by the probability layer: the caps are
deterministic and visible, while the actual occupancies need only lie below
them coordinatewise.
-/
theorem cappedSeed_uniformDeepSeedBlock
    {mu : Nat} {D : Int}
    {descent amplification descentCaps amplificationCaps : List Nat}
    (hcert :
      ExplicitDeepSeedEvent mu D descentCaps amplificationCaps)
    (hdescent : CoordwiseLe descent descentCaps)
    (hamplification : CoordwiseLe amplification amplificationCaps) :
    UniformDeepSeedBlock
      (mu : Int) (2 * (mu : Int)) D
      (descent ++ amplification) := by
  unfold ExplicitDeepSeedEvent at hcert
  rcases hcert with ⟨hdescentCaps, hampCaps, htarget⟩
  have hdescentActual :
      PositiveDescentEvent mu descent :=
    positiveDescentEvent_of_coordwise hdescentCaps hdescent
  have hampActual :=
    lowBudget_of_coordwise hampCaps hamplification
  have htargetActual :
      D <= lowBudgetFinal 3 amplification :=
    le_trans htarget hampActual.2
  exact explicitDeepSeedEvent_uniform
    ⟨hdescentActual, hampActual.1, htargetActual⟩

theorem cappedSeed_support_length
    {descent amplification descentCaps amplificationCaps : List Nat}
    (hdescent : CoordwiseLe descent descentCaps)
    (hamplification : CoordwiseLe amplification amplificationCaps) :
    (descent ++ amplification).length =
      descentCaps.length + amplificationCaps.length := by
  rw [List.length_append, coordwiseLe_length hdescent,
    coordwiseLe_length hamplification]

theorem cappedSeed_mass_le
    {descent amplification descentCaps amplificationCaps : List Nat}
    (hdescent : CoordwiseLe descent descentCaps)
    (hamplification : CoordwiseLe amplification amplificationCaps) :
    (descent ++ amplification).sum <=
      descentCaps.sum + amplificationCaps.sum := by
  rw [List.sum_append]
  have h1 := coordwiseLe_sum hdescent
  have h2 := coordwiseLe_sum hamplification
  omega

/-- Geometric success parameter p=1/(mu+1), supported on {0,1,2,...}. -/
def geometricP (mu : Nat) : Rat :=
  1 / ((mu : Rat) + 1)

/-- Geometric ratio r=mu/(mu+1). -/
def geometricR (mu : Nat) : Rat :=
  (mu : Rat) / ((mu : Rat) + 1)

/-- Exact point mass P(X=k)=p r^k. -/
def geometricPointMass (mu k : Nat) : Rat :=
  geometricP mu * geometricR mu ^ k

/-- Exact lower-tail mass P(X<=a)=1-r^(a+1). -/
def geometricCDFMass (mu a : Nat) : Rat :=
  1 - geometricR mu ^ (a + 1)

/-- Exact interval mass P(lo<=X<=hi), with the empty interval assigned 0. -/
def geometricIntervalMass (mu lo hi : Nat) : Rat :=
  if lo <= hi then
    geometricR mu ^ lo - geometricR mu ^ (hi + 1)
  else
    0

/--
Exact product-law atom mass for a finite occupancy vector.  It depends only on
the support length and total local mass.
-/
def geometricVectorMass (mu : Nat) (xs : List Nat) : Rat :=
  geometricP mu ^ xs.length * geometricR mu ^ xs.sum

/-- Exact product probability of coordinatewise cap constraints. -/
def geometricCapProduct : Nat → List Nat → Rat
  | _, [] => 1
  | mu, a :: caps =>
      geometricCDFMass mu a * geometricCapProduct mu caps

@[simp] theorem geometricCapProduct_nil (mu : Nat) :
    geometricCapProduct mu [] = 1 := rfl

@[simp] theorem geometricCapProduct_cons
    (mu a : Nat) (caps : List Nat) :
    geometricCapProduct mu (a :: caps) =
      geometricCDFMass mu a * geometricCapProduct mu caps := rfl

theorem geometricCapProduct_append
    (mu : Nat) (caps₁ caps₂ : List Nat) :
    geometricCapProduct mu (caps₁ ++ caps₂) =
      geometricCapProduct mu caps₁ * geometricCapProduct mu caps₂ := by
  induction caps₁ with
  | nil =>
      simp [geometricCapProduct]
  | cons a caps₁ ih =>
      simp [geometricCapProduct, ih, mul_assoc]

/--
Exact iid product-law mass of the visible two-stage coordinate-cap seed event.
The equality below records the independence factorisation between descent and
amplification coordinates.
-/
def cappedSeedProductMass
    (mu : Nat) (descentCaps amplificationCaps : List Nat) : Rat :=
  geometricCapProduct mu (descentCaps ++ amplificationCaps)

theorem cappedSeedProductMass_factor
    (mu : Nat) (descentCaps amplificationCaps : List Nat) :
    cappedSeedProductMass mu descentCaps amplificationCaps =
      geometricCapProduct mu descentCaps *
        geometricCapProduct mu amplificationCaps := by
  exact geometricCapProduct_append mu descentCaps amplificationCaps

/--
Runaway caps read directly from the Session-13 deterministic thresholds.
For positive D, Int.toNat (D/4) is exactly floor(D/4).
-/
def runawayCaps : Int → Nat → List Nat
  | _, 0 => []
  | D, k + 1 =>
      Int.toNat (D / 4) :: runawayCaps (runawayNext D) k

@[simp] theorem runawayCaps_length (D : Int) (k : Nat) :
    (runawayCaps D k).length = k := by
  induction k generalizing D with
  | zero =>
      simp [runawayCaps]
  | succ k ih =>
      simp [runawayCaps, ih]

theorem four_mul_le_of_le_runawayCap
    {D : Int} {x : Nat}
    (hD : 0 <= D)
    (hx : x <= Int.toNat (D / 4)) :
    4 * (x : Int) <= D := by
  have hq : 0 <= D / 4 := by
    omega
  have hx' : (x : Int) <= (Int.toNat (D / 4) : Int) := by
    exact_mod_cast hx
  rw [Int.toNat_of_nonneg hq] at hx'
  omega

/--
The deterministic Session-13 runaway block is exactly implied by the visible
coordinate caps used in the product probability.
-/
theorem runawayBlock_of_coordwise_runawayCaps
    {D : Int} {k : Nat} {xs : List Nat}
    (hD : 4 <= D)
    (hle : CoordwiseLe xs (runawayCaps D k)) :
    RunawayBlock D xs := by
  induction k generalizing D xs with
  | zero =>
      cases xs with
      | nil =>
          simp [RunawayBlock]
      | cons x xs =>
          simp [CoordwiseLe, runawayCaps] at hle
  | succ k ih =>
      cases xs with
      | nil =>
          simp [CoordwiseLe, runawayCaps] at hle
      | cons x xs =>
          change
            x <= Int.toNat (D / 4) ∧
              CoordwiseLe xs (runawayCaps (runawayNext D) k) at hle
          change
            4 * (x : Int) <= D ∧
              RunawayBlock (runawayNext D) xs
          constructor
          · exact four_mul_le_of_le_runawayCap (by omega) hle.1
          · exact
              ih (D := runawayNext D) (xs := xs)
                (four_le_runawayNext hD) hle.2

def runawayProductMass (mu : Nat) (D : Int) (k : Nat) : Rat :=
  geometricCapProduct mu (runawayCaps D k)

/-- A concrete finite vector is a weak composition of total t into n parts. -/
def IsWeakComposition (n t : Nat) (xs : List Nat) : Prop :=
  xs.length = n ∧ xs.sum = t

/--
Weak-composition count with the zero-coordinate edge case made explicit.
For n>0 this is the stars-and-bars number choose(n+t-1,n-1).
-/
def weakCompositionCount (n t : Nat) : Nat :=
  if n = 0 then
    if t = 0 then 1 else 0
  else
    Nat.choose (n + t - 1) (n - 1)

theorem weakCompositionCount_of_pos
    {n t : Nat} (hn : 0 < n) :
    weakCompositionCount n t =
      Nat.choose (n + t - 1) (n - 1) := by
  simp [weakCompositionCount, Nat.ne_of_gt hn]

@[simp] theorem weakCompositionCount_zero_zero :
    weakCompositionCount 0 0 = 1 := by
  simp [weakCompositionCount]

@[simp] theorem weakCompositionCount_zero_succ (t : Nat) :
    weakCompositionCount 0 (t + 1) = 0 := by
  simp [weakCompositionCount]

/-- Matching product law for a fixed total: p=n/(n+t). -/
def matchedGeometricP (n t : Nat) : Rat :=
  (n : Rat) / ((n : Rat) + (t : Rat))

def matchedGeometricR (n t : Nat) : Rat :=
  (t : Rat) / ((n : Rat) + (t : Rat))

def matchedProductVectorMass
    (n t : Nat) (xs : List Nat) : Rat :=
  matchedGeometricP n t ^ xs.length *
    matchedGeometricR n t ^ xs.sum

/--
All length-n product atoms of total mass t have exactly the same mass.  This
is the finite algebraic core of the conditioned-geometric representation.
-/
theorem matchedProductVectorMass_of_length_sum
    {n t : Nat} {xs : List Nat}
    (hlen : xs.length = n) (hsum : xs.sum = t) :
    matchedProductVectorMass n t xs =
      matchedGeometricP n t ^ n *
        matchedGeometricR n t ^ t := by
  simp [matchedProductVectorMass, hlen, hsum]

theorem matchedProductVectorMass_constant_on_total
    {n t : Nat} {xs ys : List Nat}
    (hxlen : xs.length = n) (hxsum : xs.sum = t)
    (hylen : ys.length = n) (hysum : ys.sum = t) :
    matchedProductVectorMass n t xs =
      matchedProductVectorMass n t ys := by
  rw [matchedProductVectorMass_of_length_sum hxlen hxsum,
    matchedProductVectorMass_of_length_sum hylen hysum]

/--
Exact finite conditioning core: every product-law atom in the fixed-total
weak-composition fibre has the same mass.
-/
theorem matchedProductVectorMass_uniform_on_compositions
    {n t : Nat} {xs ys : List Nat}
    (hx : IsWeakComposition n t xs)
    (hy : IsWeakComposition n t ys) :
    matchedProductVectorMass n t xs =
      matchedProductVectorMass n t ys :=
  matchedProductVectorMass_constant_on_total
    hx.1 hx.2 hy.1 hy.2

/--
Exact conditioned probability of one fixed local k-vector of total mass s,
expressed as completion count divided by the total stars-and-bars count.
The k<n and s<=t hypotheses are kept as explicit finite guards.
-/
def conditionedLocalVectorMass
    (n t k s : Nat) : Rat :=
  if k < n ∧ s <= t then
    (weakCompositionCount (n - k) (t - s) : Rat) /
      (weakCompositionCount n t : Rat)
  else
    0

def matchedProductLocalVectorMass
    (n t k s : Nat) : Rat :=
  matchedGeometricP n t ^ k *
    matchedGeometricR n t ^ s

/-- Exact finite conditioned/product likelihood ratio for one local vector. -/
def localLikelihoodRatio
    (n t k s : Nat) : Rat :=
  conditionedLocalVectorMass n t k s /
    matchedProductLocalVectorMass n t k s

theorem conditionedLocalVectorMass_of_supported
    {n t k s : Nat} (hk : k < n) (hs : s <= t) :
    conditionedLocalVectorMass n t k s =
      (weakCompositionCount (n - k) (t - s) : Rat) /
        (weakCompositionCount n t : Rat) := by
  simp [conditionedLocalVectorMass, hk, hs]

namespace LeftPath

/--
Thin genuine-path corollary for the finite probability interface:
regeneration occupancy + explicit seed coordinate caps + explicit runaway caps
produce the same genuine certified front proved in Session 13.
-/
theorem leftBranch_regeneration_cappedSeed_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j runLen : Nat)
    (descent amplification descentCaps amplificationCaps : List Nat)
    (h :
      j + 1 + (descent ++ amplification).length + runLen + 1 < n)
    (mu : Nat) (M D : Int) (budget : Nat)
    (hprev :
      (leftBranch n hn j (by omega)).branchMessage C = some M)
    (hmu : 1 <= mu)
    (hMlo : -(mu : Int) < M)
    (hMhi : M <= 2 * (mu : Int))
    (hXlo :
      2 * (mu : Int) + 2 - M <=
        (C (leftBranch n hn (j + 1) (by omega)).root : Int))
    (hXhi :
      (C (leftBranch n hn (j + 1) (by omega)).root : Int) <=
        4 * (mu : Int) - M)
    (hD : 4 <= D)
    (hseedValues :
      leftBlockValues C (j + 1)
          (descent ++ amplification).length (by omega) =
        descent ++ amplification)
    (hseedCert :
      ExplicitDeepSeedEvent mu D descentCaps amplificationCaps)
    (hdescent : CoordwiseLe descent descentCaps)
    (hamplification : CoordwiseLe amplification amplificationCaps)
    (hrunCaps :
      CoordwiseLe
        (leftBlockValues C
          (j + 1 + (descent ++ amplification).length)
          runLen (by omega))
        (runawayCaps D runLen))
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D runLen) :
    ∃ z : Int,
      (leftBranch n hn
        (j + 1 + (descent ++ amplification).length + runLen)
        (by omega)).branchMessage C =
        some z ∧
      CertifiedFront budget z := by
  have hmuInt : (1 : Int) <= (mu : Int) := by
    exact_mod_cast hmu
  have hseedBlock :
      UniformDeepSeedBlock
        (mu : Int) (2 * (mu : Int)) D
        (leftBlockValues C (j + 1)
          (descent ++ amplification).length (by omega)) := by
    rw [hseedValues]
    exact
      cappedSeed_uniformDeepSeedBlock
        hseedCert hdescent hamplification
  have hrun :
      RunawayBlock D
        (leftBlockValues C
          (j + 1 + (descent ++ amplification).length)
          runLen (by omega)) :=
    runawayBlock_of_coordwise_runawayCaps hD hrunCaps
  exact
    leftBranch_regeneration_seed_runaway_to_front
      hn C j (descent ++ amplification).length runLen h
      (mu : Int) M D budget hprev hmuInt hMlo hMhi
      hXlo hXhi hD hseedBlock hrun htarget

end LeftPath

namespace RightPath

/-- Right-oriented counterpart of the left capped-seed front corollary. -/
theorem rightBranch_regeneration_cappedSeed_runaway_to_front
    {n : Nat} (hn : 0 < n) (C : TreeStack.Configuration (Fin n))
    (j runLen : Nat)
    (descent amplification descentCaps amplificationCaps : List Nat)
    (h :
      j + 1 + (descent ++ amplification).length + runLen + 1 < n)
    (mu : Nat) (M D : Int) (budget : Nat)
    (hprev :
      (rightBranch n hn j (by omega)).branchMessage C = some M)
    (hmu : 1 <= mu)
    (hMlo : -(mu : Int) < M)
    (hMhi : M <= 2 * (mu : Int))
    (hXlo :
      2 * (mu : Int) + 2 - M <=
        (C (rightBranch n hn (j + 1) (by omega)).root : Int))
    (hXhi :
      (C (rightBranch n hn (j + 1) (by omega)).root : Int) <=
        4 * (mu : Int) - M)
    (hD : 4 <= D)
    (hseedValues :
      rightBlockValues C (j + 1)
          (descent ++ amplification).length (by omega) =
        descent ++ amplification)
    (hseedCert :
      ExplicitDeepSeedEvent mu D descentCaps amplificationCaps)
    (hdescent : CoordwiseLe descent descentCaps)
    (hamplification : CoordwiseLe amplification amplificationCaps)
    (hrunCaps :
      CoordwiseLe
        (rightBlockValues C
          (j + 1 + (descent ++ amplification).length)
          runLen (by omega))
        (runawayCaps D runLen))
    (htarget :
      (budget : Int) + 2 <= runawayThreshold D runLen) :
    ∃ z : Int,
      (rightBranch n hn
        (j + 1 + (descent ++ amplification).length + runLen)
        (by omega)).branchMessage C =
        some z ∧
      CertifiedFront budget z := by
  have hmuInt : (1 : Int) <= (mu : Int) := by
    exact_mod_cast hmu
  have hseedBlock :
      UniformDeepSeedBlock
        (mu : Int) (2 * (mu : Int)) D
        (rightBlockValues C (j + 1)
          (descent ++ amplification).length (by omega)) := by
    rw [hseedValues]
    exact
      cappedSeed_uniformDeepSeedBlock
        hseedCert hdescent hamplification
  have hrun :
      RunawayBlock D
        (rightBlockValues C
          (j + 1 + (descent ++ amplification).length)
          runLen (by omega)) :=
    runawayBlock_of_coordwise_runawayCaps hD hrunCaps
  exact
    rightBranch_regeneration_seed_runaway_to_front
      hn C j (descent ++ amplification).length runLen h
      (mu : Int) M D budget hprev hmuInt hMlo hMhi
      hXlo hXhi hD hseedBlock hrun htarget

end RightPath

end ProbStack
