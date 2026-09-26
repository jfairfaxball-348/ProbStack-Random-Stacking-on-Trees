# Problem statement

## Primary object

For a deterministic tree `T` on `n` vertices and total mass `t`, sample a
configuration uniformly from all weak compositions of `t` into `n` parts and
write

\[
p_T(t)=\Pr[C\text{ is stackable}].
\]

The first sequence is `P_n`.  The aim is to determine the asymptotic behaviour
of `p_{P_n}(t)` without assuming monotonicity or forcing conventional threshold
language.

TreeStack supplies the deterministic equivalence

\[
C\text{ stackable on }T
\iff \max_r S_r(C)>0.
\]

Thus the random problem is the joint law of the correlated rooted scores.

## Finite sanity facts

- `t=0`: no positive stacked configuration exists, so `p_T(0)=0` under the
  source definition of stacked support size one.
- `t=1`: every configuration is already stacked, so `p_T(1)=1`.
- `t=2`: a two-pebble configuration is stackable iff both pebbles start at one
  vertex.  If they start at distinct vertices there is no legal move.  Hence
  `A_T(2)=n` and `p_T(2)=2/(n+1)` for every `n`-vertex tree.
- Minimal coordinatewise failure of upward closure: on `P_2`, `(1,0)` is
  stackable but `(1,1) >= (1,0)` is not.
- Aggregate probability is therefore not globally monotone in `t`; on `P_2`
  the values at `t=1,2,3` are `1, 2/3, 1`.

## Questions

The central questions are whether a high-density recovery scale exists in a
suitable growing regime, what its order is, and whether the transition is
sharp, broad, or has a nontrivial limiting profile.  The initial computations
also motivate separate study of the location/depth of the low-density trough.
