# PIKS Source Assessment

## Source

Joachim Bona-Pellissier, Giacomo Meanti, Matteo Santacesaria, and Lorenzo
Rosasco, **PIKS: Universal Physics-Informed Kernel Methods**,
[arXiv:2607.27062](https://arxiv.org/abs/2607.27062), 2026.

This is a 60-page statistics/machine-learning paper about regression with
linear differential constraints. It is not a paper about voting, Kemeny
aggregation, differential privacy, finite cover graphs, Hex, or combinatorial
game oracles.

## What the paper proves

PIKS minimizes a regularized empirical objective with two data sources:

\[
\frac1n\sum_i(u(x_i)-y_i)^2+
\frac1m\sum_j(Du(z_j)-w_j)^2+
\lambda\lVert u\rVert_H^2,
\]

where \(H\) is an RKHS and \(D\) is a linear operator. The paper gives a
closed-form operator expression for the unique regularized minimizer.

Its universal-consistency theorem is conditional on five groups of
hypotheses, including:

1. bounded point-evaluation functionals for \(D\) on the RKHS;
2. compatible bounded embeddings into the two sampled \(L^2\) spaces;
3. density of the RKHS in the target function space, which is stronger than
   ordinary \(L^2\) universality in the Sobolev setting;
4. bounded target values and noise; and
5. bounded ordinary and operator features.

Both sample sizes tend to infinity and the regularization sequence must obey
\(\lambda\to0\) and
\(\log N/(\lambda^3N)\to0\), where \(N=\min(n,m)\). The conclusion is
simultaneous \(L^2\) convergence of function values and operator values,
including in a misspecified setting. Finite-sample rates require a further
operator source condition. Stronger Sobolev convergence for PDEs additionally
uses PDE-specific stability or elliptic regularity.

## What transfers and what does not

One methodological point transfers: value fit and structural consistency
should be measured separately. This reinforces the oracle audit's separation
of empirical outcomes from invariant-preserving decisions.

No PIKS theorem transfers to this repository:

- the set of linear orders is finite and nonconvex, not an RKHS dense in a
  Sobolev target space;
- transitivity is not the linear differential operator in the theorem;
- profile adjacency is not physical collocation sampling;
- smooth sensitivity is not Tikhonov regularization; and
- a finite residual penalty would not imply privacy or universal consistency.

It would be possible to design a new kernel method on pairwise-comparison
vectors and penalize a separately defined transitivity residual. That would
be a new model requiring its own approximation, projection, privacy, and
neutrality analysis. The present increment does not implement it because the
source supplies no valid theorem bridge and the repository already has exact
finite baselines for the relevant combinatorial questions.

## Status

`METHODOLOGICAL ASSESSMENT; NO TRANSPORTED THEOREM; NO PIKS REPRODUCTION`.
