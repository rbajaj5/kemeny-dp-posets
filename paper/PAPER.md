# Cover-Graph Stability and Smooth Sensitivity for Kemeny Rank Aggregation

**Ravi Andrew Bajaj** and **Alexander Burns**

Correspondence: Ravi Andrew Bajaj, `rbajaj5@jh.edu`

Research note, 29 July 2026

> **Status.** The propositions in this note are proved below and accompanied by
> executable finite verification. Their novelty relative to the complete
> literature has not been certified. In particular, the exact integer
> cover-distance should be compared carefully with existing breakdown
> functions for ranking medians before making a priority claim.

## Abstract

We place finite ranking profiles in the componentwise multiset poset and
observe that its undirected Hasse graph is exactly the add/remove-one-record
adjacency graph of unbounded differential privacy. This viewpoint turns
instance stability into a cover-distance question. For a profile with a unique
Kemeny optimum \(\sigma\), we prove an exact formula for the minimum number of
cover moves required to destroy uniqueness:

\[
R(x)=\min_{\tau\ne\sigma}
\left\lceil
\frac{C_x(\tau)-C_x(\sigma)}{d_K(\sigma,\tau)}
\right\rceil .
\]

We also prove exact formulas for the one-step local sensitivity of the scalar
optimal Kemeny score and derive a \(\beta\)-smooth upper bound for the
Kendall-metric local sensitivity of a deterministic Kemeny selector. The
repository computes exact smooth sensitivity of the scalar score by certified
Hasse-shell search, implements the corresponding one-dimensional approximate
DP release, and exhaustively checks the finite identities for all profiles of
at most four ballots over three candidates. Finally, we explain how the
three-voter NP-hardness of exact Kemeny aggregation constrains
sample-and-aggregate designs and provide a non-private center-of-attention
utility prototype.

## 1. Introduction

Kemeny rank aggregation chooses a ranking minimizing the sum of Kendall
distances to the input ballots. Two issues are immediate in private data
analysis. First, the selected ranking can change discontinuously after a
single ballot is added or removed. Second, exact Kemeny aggregation is
computationally hard; Peters proves NP-hardness even for three input rankings.

The differential-privacy survey of Dwork emphasizes three tools relevant here:
global and local sensitivity, smooth upper bounds on local sensitivity, and
geometric dimension reduction. The supplied slide deck additionally
foregrounds covering relations and Hasse diagrams. We use those ideas
literally: a database of ballots is a finite multiset, a one-record change is a
cover move, and the full privacy neighborhood is a Hasse shell.

This note makes four contributions:

1. it identifies the exact profile cover graph and its metric;
2. it derives exact local-sensitivity identities for the scalar optimal score;
3. it proves an exact cover-distance certificate for a unique Kemeny ranking
   and a smooth upper bound derived from that certificate; and
4. it supplies executable exact verification and a computationally explicit
   sample-and-aggregate design constraint.

The claims are mathematical propositions, not yet claims of bibliographic
novelty.

## 2. Preliminaries

Let \([m]\) be the candidate set and \(S_m\) the set of all linear rankings.
For \(\pi,\sigma\in S_m\), let \(d_K(\pi,\sigma)\) be Kendall distance. Its
diameter is

\[
D=\binom m2.
\]

A profile is a count vector \(x\in\mathbb N^{m!}\), indexed by rankings. Its
Kemeny score at output \(\sigma\) and its optimal value are

\[
C_x(\sigma)=\sum_{\pi\in S_m}x_\pi d_K(\pi,\sigma),
\qquad
\operatorname{OPT}(x)=\min_{\sigma\in S_m} C_x(\sigma).
\]

We use unbounded-DP adjacency: two profiles are adjacent when one is obtained
from the other by adding or removing one ballot.

## 3. Profiles as a graded poset

Order \(\mathbb N^{m!}\) componentwise. The rank of profile \(x\) is its number
of ballots, \(|x|_1\).

**Proposition 1 (cover graph).** A profile \(y\) covers \(x\) precisely when
\(y=x+e_\pi\) for some \(\pi\in S_m\). Consequently, the undirected Hasse graph
is the unbounded-DP adjacency graph and

\[
d_H(x,y)=\lVert x-y\rVert_1.
\]

**Proof.** A componentwise increase is a cover exactly when one coordinate
increases by one. Thus each undirected edge adds or removes one ballot. Every
path from \(x\) to \(y\) must make at least
\(\sum_\pi|x_\pi-y_\pi|\) unit coordinate changes. Deleting surplus ballots
and adding deficient ballots attains this bound. \(\square\)

This identifies local sensitivity with behavior on incident Hasse edges and
smooth sensitivity with an exponentially discounted maximum over Hasse
shells.

## 4. Sensitivity of the optimal value

**Proposition 2 (global sensitivity).** A fixed score \(C_x(\sigma)\) and the
scalar \(\operatorname{OPT}(x)\) have global sensitivity at most \(D\). The
bound is tight for \(\operatorname{OPT}\).

**Proof.** Adding or removing ballot \(\pi\) changes \(C_x(\sigma)\) by
\(d_K(\pi,\sigma)\in[0,D]\). A pointwise minimum of \(D\)-Lipschitz functions
is \(D\)-Lipschitz. For tightness, start with one ballot \(\pi\), whose optimal
value is zero, and add its reverse. For every output \(\sigma\), the two
distances sum to \(D\), so the new optimal value is \(D\). \(\square\)

Define the score excess

\[
g_x(\sigma)=C_x(\sigma)-\operatorname{OPT}(x).
\]

**Proposition 3 (exact one-step changes).** Adding ballot \(\rho\) changes the
optimal value by

\[
\operatorname{OPT}(x+e_\rho)-\operatorname{OPT}(x)
=\min_\sigma\left[g_x(\sigma)+d_K(\rho,\sigma)\right].
\]

If \(x_\rho>0\), removing one copy changes it by

\[
\operatorname{OPT}(x)-\operatorname{OPT}(x-e_\rho)
=\max_\sigma\left[d_K(\rho,\sigma)-g_x(\sigma)\right].
\]

The local sensitivity of \(\operatorname{OPT}\) is the maximum of these
quantities over all additions and valid removals.

**Proof.** Substitute
\(C_{x+e_\rho}(\sigma)=C_x(\sigma)+d_K(\rho,\sigma)\), minimize, and subtract
\(\operatorname{OPT}(x)\). For removal,
\[
\operatorname{OPT}(x-e_\rho)-\operatorname{OPT}(x)
=\min_\sigma[g_x(\sigma)-d_K(\rho,\sigma)],
\]
and negating a minimum gives the stated maximum. \(\square\)

## 5. Exact distance to loss of uniqueness

Suppose \(\sigma\) is the unique Kemeny optimum at \(x\). For
\(\tau\ne\sigma\), write

\[
\Delta_x(\tau)=C_x(\tau)-C_x(\sigma)>0.
\]

**Theorem 4 (exact uniqueness radius).** The minimum Hasse distance from \(x\)
to a profile at which \(\sigma\) is no longer uniquely optimal is

\[
R(x)=\min_{\tau\ne\sigma}
\left\lceil\frac{\Delta_x(\tau)}{d_K(\sigma,\tau)}\right\rceil.
\]

If the optimum is already non-unique, define \(R(x)=0\).

**Proof.** A cover move involving ballot \(\pi\) changes the gap against
competitor \(\tau\) by

\[
\pm\left[d_K(\pi,\tau)-d_K(\pi,\sigma)\right].
\]

The reverse triangle inequality bounds the magnitude by
\(d_K(\sigma,\tau)\). Hence \(k\) cover moves can reduce
\(\Delta_x(\tau)\) by at most \(k\,d_K(\sigma,\tau)\). The gap therefore
remains positive whenever
\[
k<
\left\lceil\frac{\Delta_x(\tau)}{d_K(\sigma,\tau)}\right\rceil.
\]

For tightness, add \(k\) copies of the competitor ranking \(\tau\). Each
addition raises \(C(\sigma)\) by \(d_K(\sigma,\tau)\) and leaves \(C(\tau)\)
unchanged, reducing the gap by exactly this amount. At the ceiling, \(\tau\)
ties or beats \(\sigma\). Minimizing over competitors proves the formula.
\(\square\)

The denominator matters: the second-best score alone need not determine the
first destabilizing competitor. A more distant ranking can close a larger
score gap faster per added ballot.

## 6. A smooth bound for ranking-output sensitivity

Let \(\kappa(x)\) be a deterministic Kemeny selector with any fixed
tie-breaking rule, and measure output change by \(d_K\). Define

\[
B_\beta(x)=D\exp\{-\beta\max(R(x)-1,0)\}.
\]

**Theorem 5 (smooth upper bound).** \(B_\beta\) is a \(\beta\)-smooth upper
bound on the local sensitivity of \(\kappa\).

**Proof.** If \(R(x)\ge2\), every neighbor remains inside the same
unique-optimum region, so every neighbor has selected output \(\sigma\) and
the local sensitivity is zero. If \(R(x)\le1\), then \(B_\beta(x)=D\), the
diameter of the output space, and therefore bounds local sensitivity.

It remains to prove smoothness. Within one unique-optimum region, \(R\) is the
graph distance to that region's complement and changes by at most one across
an edge. If adjacent unique profiles have different optima, each has radius
one because its neighbor lies outside its own region. A tied endpoint has
radius zero. Thus the clipped quantity \(\max(R-1,0)\) changes by at most one
on every edge, giving
\[
B_\beta(x)\le e^\beta B_\beta(y)
\]
for adjacent \(x,y\). \(\square\)

This theorem supplies a smooth sensitivity bound, not by itself a complete
private mechanism for a discrete ranking output. A mechanism still needs an
admissible output perturbation or embedding and a utility analysis.

## 7. Exact scalar smooth sensitivity

For the scalar optimal value, define

\[
SS_\beta(x)=
\max_y LS_{\operatorname{OPT}}(y)e^{-\beta d_H(x,y)}.
\]

The implementation explores complete Hasse shells. After shell \(k\), every
unseen term is at most

\[
D e^{-\beta(k+1)}
\]

by Proposition 2. Search terminates exactly when this certified tail cannot
exceed the best observed term.

For \(\varepsilon>0\) and \(0<\delta<1\), the implemented one-dimensional
Nissim–Raskhodnikova–Smith calibration uses

\[
\alpha=\varepsilon/2,\qquad
\beta=\frac{\varepsilon}{2\log(2/\delta)}
\]

and releases

\[
\operatorname{OPT}(x)+\frac{SS_\beta(x)}{\alpha}Z,
\qquad Z\sim\operatorname{Laplace}(1).
\]

This releases the scalar optimal score, not a ranking.

## 8. Computation and the three-voter barrier

The repository implements exact Kemeny enumeration for small candidate sets,
cover relations, local sensitivity, certified scalar smooth sensitivity, the
uniqueness radius, and a pure-DP exponential-mechanism baseline.

Peters's three-voter hardness theorem makes one sample-and-aggregate pitfall
precise: after computing block estimates, using their exact Kemeny median as a
generic combining step is already NP-hard once there are three aggregate
rankings. Nissim, Raskhodnikova, and Smith instead give a center-of-attention
construction based on pairwise metric distances. We implement the constrained
utility-side center

\[
\arg\min_{z\in\{z_1,\ldots,z_q\}}
\min\{r:\#\{i:d_K(z,z_i)\le r\}\ge
\lfloor(q+s)/2\rfloor+1\}.
\]

The current pipeline shuffles ballots, computes exact Kemeny outputs on
complete blocks, and applies this center. It is explicitly a utility
prototype: privacy requires completing and proving the sampling-influence and
admissible-noise stages.

## 9. Exhaustive verification

The test suite checks the identities independently on every profile with
three candidates and at most four ballots. This covers 210 profiles. Among
them, 126 have unique optima. The observed uniqueness-radius histogram is

\[
\{0:84,\ 1:60,\ 2:54,\ 3:6,\ 4:6\}.
\]

The exact local-sensitivity histogram for the scalar optimal value is

\[
\{0:1,\ 2:44,\ 3:165\}.
\]

For three unanimous \(ABC\) ballots, the uniqueness radius is three and the
ranking selector has zero one-step local sensitivity. At \(\beta=0.7\), the
smooth upper bound is \(3e^{-1.4}\approx0.7398\), below the global diameter
three. These are finite computational observations, not asymptotic claims.

## 10. Relation to prior work and open questions

Hay, Elagina, and Miklau introduced differentially private rank aggregation.
Alabi et al. studied private rank aggregation in central and local models, and
Hillebrand et al. subsequently improved private algorithms. Goibert et al.
study robustness and breakdown functions for ranking medians. The first
bibliographic task is to determine whether Theorem 4 is equivalent to, a
discrete specialization of, or distinct from their contamination-radius
formulation.

The Johnson–Lindenstrauss direction is geometric but incomplete. Pairwise
preference vectors embed rankings into \(\{-1,+1\}^D\), with Kendall distance
proportional to their Hamming distance. Random projection can preserve
Euclidean geometry of a fixed finite family, and some JL transforms satisfy
differential privacy under additional spectral assumptions. Neither fact
alone preserves the transitivity constraint or yields a private Kemeny
mechanism. A valid result needs to control projection distortion, privacy
adjacency, and postprocessing back into the linear-order polytope together.

Concrete open problems are:

1. compare Theorem 4 exactly with the ICML 2023 breakdown function;
2. compute or approximate \(R(x)\) without enumerating \(m!\) rankings;
3. turn Theorem 5 into an end-to-end ranking-output mechanism;
4. complete the center-of-attention privacy and utility analysis; and
5. determine whether JL dimension reduction improves any end-to-end
   rank-aggregation privacy/utility bound after enforcing transitivity.

## References

1. C. Dwork. “Differential Privacy: A Survey of Results.” TAMC, 2008.
   [Microsoft Research PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2008/04/dwork_tamc.pdf).
2. K. Nissim, S. Raskhodnikova, and A. Smith. “Smooth Sensitivity and
   Sampling in Private Data Analysis.” STOC, 2007.
   [Author PDF](https://people.csail.mit.edu/asmith/PS/stoc321-nissim.pdf).
3. M. Hay, L. Elagina, and G. Miklau. “Differentially Private Rank
   Aggregation.” SDM, 2017.
   [Author PDF](https://people.cs.umass.edu/~miklau/assets/pubs/dp/hay17differentially.pdf).
4. D. Peters. “Kemeny Rank Aggregation is NP-Hard for Three Voters.” 2026.
   [arXiv:2607.25540](https://arxiv.org/abs/2607.25540).
5. D. Alabi et al. “Private Rank Aggregation in Central and Local Models.”
   ICML, 2022. [arXiv:2112.14652](https://arxiv.org/abs/2112.14652).
6. L. Hillebrand et al. “Improved Differentially Private Algorithms for Rank
   Aggregation.” 2026.
   [arXiv:2511.11319](https://arxiv.org/abs/2511.11319).
7. M. Goibert et al. “Robust Consensus in Ranking Data Analysis: Definitions,
   Properties and Computational Issues.” ICML, 2023.
   [PMLR](https://proceedings.mlr.press/v202/goibert23a.html).
8. J. Blocki et al. “The Johnson-Lindenstrauss Transform Itself Preserves
   Differential Privacy.” FOCS, 2012.
   [arXiv:1204.2136](https://arxiv.org/abs/1204.2136).

## Acknowledgments

OpenAI Codex provided computational and editorial assistance. It is not an
author.
