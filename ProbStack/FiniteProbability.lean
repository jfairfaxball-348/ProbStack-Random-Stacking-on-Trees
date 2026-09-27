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

/--
Runaway caps read directly from the Session-13 deterministic thresholds.
For positive D, Int.toNat (D/4) is exactly floor(D/4).
-/
def runawayCaps : Int → Nat → List Nat
  | _, 0 => []
  | D, k + 1 =>
      Int.toNat (D / 4) :: runawayCaps (runawayNext D) k

def runawayProductMass (mu : Nat) (D : Int) (k : Nat) : Rat :=
  geometricCapProduct mu (runawayCaps D k)

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

end ProbStack
