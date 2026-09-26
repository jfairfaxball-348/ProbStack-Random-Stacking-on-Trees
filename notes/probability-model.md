# Probability model

## Uniform weak compositions

For fixed `n>=1` and `t>=0`, the sample space is

\[
\mathcal D_{n,t}=\{(c_1,\ldots,c_n)\in\mathbb Z_{\ge0}^n:\sum_i c_i=t\},
\qquad |\mathcal D_{n,t}|=\binom{n+t-1}{t}.
\]

Every element has equal probability.  The stars-and-bars sampler in
`prob_stack/configurations.py` samples separator sets uniformly and hence
samples this law exactly.

This is not the multinomial model obtained by independently assigning each of
`t` labeled pebbles to a uniform vertex.  The older probabilistic-pebbling
literature explicitly distinguishes these models.

## Exact conditioned-geometric representation

There is a useful exact product representation.  Let `X_1,...,X_n` be i.i.d.
geometric random variables on `{0,1,2,...}` with

\[
\Pr[X_i=k]=p(1-p)^k,\qquad 0<p<1.
\]

For any weak composition `c` of `t`,

\[
\Pr[(X_1,\ldots,X_n)=c]=p^n(1-p)^t,
\]

which depends only on the total `t`.  Therefore

\[
(X_1,\ldots,X_n)\mid \sum_iX_i=t
\]

is **exactly uniform** on `\mathcal D_{n,t}`, for every choice of `p`.
Choosing `p=n/(n+t)` gives unconditioned mean `t/n` per coordinate.  This
identity is exact; only later steps that remove or approximate the conditioning
would be asymptotic.

The conditioning event has probability

\[
\Pr\left[\sum_iX_i=t\right]
=\binom{n+t-1}{t}p^n(1-p)^t.
\]

## Path score recurrence

Label the path `1,...,n`.  Let `L_i` be the TreeStack message from the prefix
`{1,...,i}` across the edge `i -> i+1`; define `R_i` symmetrically.  Ignoring
only the categorical EMPTY bookkeeping in the notation, the nonempty recurrence
is

\[
L_i=F(C_i+L_{i-1}),\qquad R_i=F(C_i+R_{i+1}),
\]

with EMPTY persisting exactly while the corresponding side contains no pebble.
Then

\[
S_i=C_i+L_{i-1}+R_{i+1}
\]

using zero contribution for EMPTY, and stackability is equivalent to
`max_i S_i > 0`.

This one-dimensional dynamical representation, coupled with the exact
conditioned-geometric model above, is the current analytic starting point.
