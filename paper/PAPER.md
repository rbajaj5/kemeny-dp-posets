# Cover-Graph Stability and Smooth Sensitivity for Kemeny Rank Aggregation

**Ravi Andrew Bajaj** and **Alexander Burns**

Correspondence: Ravi Andrew Bajaj, `rbajaj5@jh.edu`

Research note, updated 30 July 2026

> **Status.** The propositions in this note are proved below and accompanied by
> executable finite verification. Their novelty relative to the complete
> literature has not been certified. The exact zero-plus comparison with the
> closest ranking-breakdown work is now included, with an explicit
> total-variation normalization audit and no priority claim.

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

Writing the corresponding normalized margin as \(\mu(x)\), we independently
derive the exact zero-plus breakdown problem under
\(\operatorname{TV}(p,q)=\|p-q\|_1/2\). Its value \(b_{\rm TV}\) satisfies
\(b_{\rm TV}\ge\mu/2\), with equality under a transparent empirical-mass
condition; in that case \(R(x)=\lceil2|x|b_{\rm TV}\rceil\). This exposes a
factor-of-two normalization mismatch in the closest ICML 2023 analysis while
keeping continuous contamination distinct from add/remove cover adjacency.

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

As a separate finite-model extension, we place complete two-color Y-game
boards in a Boolean-lattice Hasse graph. The known three-cell majority
reduction preserves the global Y winner. For any nonconstant total binary
query on a Hamming graph, we prove that its exact smooth sensitivity is
determined by distance to the opposite outcome, and we verify the Y
specialization exhaustively through triangular boards of side six.

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

Following Jaffe and Liu, we distinguish a diagrammatic language \(L\), a
target mathematical reality \(R\), and a simulation \(S:L\to R\). Here a
Hasse diagram is not itself a privacy theorem: the simulation must prove that
its edges are precisely database adjacencies and that its path metric is the
claimed database distance. The same discipline applies later to coloring
diagrams, ranking-vector embeddings, and market encodings.

This note makes six contributions:

1. it identifies the exact profile cover graph and its metric;
2. it derives exact local-sensitivity identities for the scalar optimal score;
3. it proves an exact cover-distance certificate for a unique Kemeny ranking
   and a smooth upper bound derived from that certificate;
4. it derives the exact finite zero-plus TV contamination problem and a
   factor-explicit bridge to the integer cover radius;
5. it supplies executable exact verification and a computationally explicit
   sample-and-aggregate design constraint; and
6. in a separate Hex/Y model, it gives an exact Boolean-output
   smooth-sensitivity identity and exhaustive majority-reduction checks.

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

### Continuous zero-plus contamination

Let \(n=\sum_\pi x_\pi\), let \(p_x=x/n\), and define

\[
\mu(x)=
\min_{\tau\ne\sigma}
\frac{\Delta_x(\tau)}
     {n\,d_K(\sigma,\tau)}.
\]

Theorem 4 is equivalently \(R(x)=\lceil n\mu(x)\rceil\). Now use the standard
total-variation convention
\(\operatorname{TV}(p,q)=\|p-q\|_1/2\), and define

\[
b_{\rm TV}(p_x)=
\inf\{\operatorname{TV}(p_x,q):
\sigma\text{ is not the unique Kemeny optimum under }q\}.
\]

For a competitor \(\tau\), put

\[
f_\tau(\rho)=d_K(\rho,\tau)-d_K(\rho,\sigma),
\qquad
g_\tau=\mathbb E_{p_x}f_\tau
=\frac{\Delta_x(\tau)}n.
\]

Let \(Q_\tau(u)\) be the decreasing quantile of \(f_\tau(\rho)\) under
\(\rho\sim p_x\), and write \(d_\tau=d_K(\sigma,\tau)\).

**Proposition 4.1 (exact zero-plus TV breakdown).** The TV distance to the
boundary where \(\tau\) ties \(\sigma\) is

\[
b_\tau=
\inf\left\{t\ge0:
\int_0^t\bigl(Q_\tau(u)+d_\tau\bigr)\,du\ge g_\tau\right\},
\]

and

\[
b_{\rm TV}(p_x)=\min_{\tau\ne\sigma}b_\tau
\ge\frac{\mu(x)}2.
\]

If a competitor attaining \(\mu(x)\) has at least
\(\Delta_x(\tau)/(2nd_\tau)\) empirical mass on the coefficient level
\(f_\tau=d_\tau\), equality holds. In particular,

\[
\mu(x)\le2p_x(\sigma)
\quad\Longrightarrow\quad
b_{\rm TV}(p_x)=\frac{\mu(x)}2
\quad\text{and}\quad
R(x)=\left\lceil2n b_{\rm TV}(p_x)\right\rceil.
\]

**Proof.** A TV move of size \(t\) removes \(t\) mass and adds \(t\) mass.
For fixed \(t\), the greatest reduction of \(\mathbb E f_\tau\) removes mass
from decreasing coefficient levels and adds it at the minimum
\(-d_\tau\), attained at \(\rho=\tau\). This is exactly the displayed
quantile integral. A competitor reaches the Kemeny boundary precisely when
its expectation reaches zero, proving the minimization formula. Reverse
triangle inequality gives
\(-d_\tau\le f_\tau\le d_\tau\), so each unit of TV reduces the expectation
by at most \(2d_\tau\). Hence
\(b_\tau\ge g_\tau/(2d_\tau)\), and minimization gives the lower bound.
Enough mass at the upper endpoint permits transport directly from that level
to the lower endpoint and attains the bound. Since \(\rho=\sigma\) is an
upper-endpoint state, the stated empirical-mass condition is sufficient.
\(\square\)

At attack amplitude \(\delta\to0^+\), the displayed upper expression in
Goibert et al.'s Theorem 3.1 simplifies to \(\mu(x)\). Their construction
removes \(\epsilon/2\) mass from the original median and adds it to its
reverse, so its standard TV is \(\epsilon/2\). Their Equation (4) explicitly
uses half-\(L^1\) TV, but Appendix C.2, Equation (33), bounds the full
\(L^1\) difference by the same TV budget. The factor-two mismatch explains
why the construction yields \(\mu/2\), not \(\mu\), in the present convention.
This note does not claim a general correction for positive attack levels or
bucket rankings.

The identity is conditional, not universal. An exact four-candidate,
ten-ballot profile in `results/breakdown_comparison.json` has
\(\mu/2=1/30\) and \(b_{\rm TV}=1/20\). The numerical bridge also does not
identify the two perturbation models: TV moves fractional mass at fixed total
probability, whereas a cover move adds or removes an integer ballot.

### Exact stability witnesses by subset dynamic programming

Theorem 4 need not be evaluated by enumerating all \(m!\) rankings. After
finding a selected optimum \(\sigma\), define the distance-stratified score
profile

\[
F_x(d)=
\min_{\tau:\,d_K(\sigma,\tau)=d} C_x(\tau),
\qquad 0\le d\le D.
\]

For \(S\subseteq[m]\), let \(A(S,d)\) be the minimum partial Kemeny cost of an
ordering of \(S\) whose Kendall distance from \(\sigma|_S\) is \(d\). Write
\(q(a,b)\) for the number of ballots placing \(a\) before \(b\), and set

\[
r_\sigma(a,S)=
\left|\{b\in S\setminus\{a\}:
        \sigma\text{ places }a\text{ before }b\}\right|.
\]

Conditioning on the last candidate \(a\) gives the recurrence

\[
A(S,d)=
\min_{a\in S}
\left[
A(S\setminus\{a\},d-r_\sigma(a,S))
+\sum_{b\in S\setminus\{a\}}q(a,b)
\right],
\]

with \(A(\varnothing,0)=0\) and infeasible states assigned infinity.

**Proposition 4.2 (distance-stratified certificate).** The full-set DP values
satisfy \(A([m],d)=F_x(d)\). If \(\sigma\) is unique, then

\[
\min_{d\ge1}F_x(d)
\]

is the second-best score and

\[
R(x)=\min_{d\ge1}
\left\lceil\frac{F_x(d)-\operatorname{OPT}(x)}d\right\rceil.
\]

A parent-pointer witness at a minimizing distance is a ranking whose repeated
addition attains the radius. With precomputed transitions, the DP uses
\(O(mD2^m)\) time and \(O(D2^m)\) numeric states plus parent pointers.

**Proof.** If \(a\) is last in an ordering of \(S\), each
\(b\in S\setminus\{a\}\) is placed before \(a\). The new Kemeny disagreements
are exactly the ballots counted by \(q(a,b)\). The new inversions relative to
\(\sigma\) are exactly those pairs for which \(\sigma\) places \(a\) before
\(b\), counted by \(r_\sigma(a,S)\). Removing the last candidate is a
bijection between feasible full states and the recurrence's predecessor
states, so induction on \(|S|\) proves \(A([m],d)=F_x(d)\). The two displayed
conclusions then follow from the definitions and Theorem 4. Adding \(R(x)\)
copies of the returned competitor reduces its gap by
\(R(x)d_K(\sigma,\tau)\), proving witness attainment. \(\square\)

For the five-ballot profile

\[
(ABC,ABC,ABC,BCA,CAB),
\]

the unique optimum \(ABC\) has cost \(4\), and
\(F_x(1),F_x(2),F_x(3)=(7,8,11)\). The second-best witness \(ACB\) has gap
three and attack radius three, whereas \(BCA\) has the larger gap four but
Kendall distance two and attack radius two. This is a strict finite example
showing why the distance denominator cannot be discarded.

The recurrence and proof are contributions of this executable note only in
the limited sense that they are established here. Their novelty relative to
the parameterized and exact Kemeny literature has not been determined.

### A sharp consequence for three voters

The exact formula yields a stronger bound whenever at least one input ballot
differs from the unique optimum.

**Corollary 4.3 (non-unanimous radius bound).** In any metric 1-median problem
with \(n\ge3\) input records, if the optimum \(\sigma\) is unique and the
profile is not unanimous at \(\sigma\), then

\[
R(x)\le n-2.
\]

For exactly three voters, the radius is therefore exactly one at every unique
non-unanimous profile. A unanimous three-voter profile has radius three.

**Proof.** Choose an input record \(\rho\ne\sigma\), and distinguish that copy
from the other \(n-1\) records. Its competitor gap satisfies

\[
\begin{aligned}
C_x(\rho)-C_x(\sigma)
&=-d(\rho,\sigma)
  +\sum_{\pi\ne\rho}\bigl(d(\pi,\rho)-d(\pi,\sigma)\bigr)\\
&\le -d(\rho,\sigma)+(n-1)d(\rho,\sigma)\\
&=(n-2)d(\rho,\sigma),
\end{aligned}
\]

where the inequality is the triangle inequality. Uniqueness makes the gap
positive. Substituting competitor \(\tau=\rho\) in Theorem 4 gives
\(R(x)\le n-2\). When \(n=3\), the positive integer radius is one. If all three
records equal \(\sigma\), every competitor \(\tau\) has gap
\(3d(\sigma,\tau)\), so Theorem 4 gives radius three. \(\square\)

This metric argument is computationally agnostic: Peters's theorem says
finding the three-voter Kemeny optimum is NP-hard as the candidate count grows,
while the corollary characterizes the optimum's cover stability once it is
known.

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

For exactly three voters, Corollary 4.1 makes this particular bound
degenerate away from unanimity: it equals the global diameter \(D\) at every
non-unanimous unique profile and at every tied profile, while a unanimous
profile receives the smaller value \(D e^{-2\beta}\). Thus a more informative
three-voter mechanism would need a finer statistic than distance to loss of
uniqueness alone.

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

Write \(r_{\rm in}\) for the displayed input-restricted radius and
\(r_{\rm all}\) for the minimum radius when the center may be any ranking.

**Proposition 8.1 (input-center approximation).** In every metric space,

\[
r_{\rm all}\le r_{\rm in}\le2r_{\rm all}.
\]

The factor two is sharp in Kendall space. The full set of input centers
attaining \(r_{\rm in}\) is equivariant under a common relabeling of
candidates, although lexicographically selecting one minimizer is not.

**Proof.** The first inequality follows by domain inclusion. A radius
\(r_{\rm all}\) ball contains the target number of input points. Choose one
such input point as a new center. Triangle inequality places every point in
the same witness set within radius \(2r_{\rm all}\) of it. For sharpness, use
the two three-candidate rankings \(ABC\) and \(BCA\): either input center has
radius two, while \(BAC\) has radius one. Common relabeling preserves all
Kendall distances and therefore maps the minimizing set equivariantly.
\(\square\)

For two-ballot blocks, either input is an exact Kemeny optimum by triangle
inequality. The implementation returns the lexicographically smaller input in
linear input time. It also supplies Borda as a polynomial-time option for
larger blocks and validates every ballot before shuffling, including ballots
that would fall in an incomplete discarded block.

The exact finite audit checks 8,581 center certificates through seven points
in the three-candidate space. It finds zero witness, approximation, or
minimizer-set equivariance failures and 986 sharp factor-two cases. It also
checks all 612 ordered two-ballot profiles through four candidates with zero
optimality failures. Borda attains exact Kemeny cost on 2,712 of the 3,002
three-candidate profiles through eight ballots; the largest observed cost
ratio is \(3/2\), which is not asserted as a general bound.

Lexicographic resolution is intentionally labeled non-neutral. On the
candidate-symmetric multiset containing every ranking equally often, no
deterministic single-ranking output can be invariant under every candidate
relabeling. The certificate therefore exposes the complete minimizing set for
set-valued or explicitly randomized downstream use.

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

The dedicated application script additionally exhausts all three-voter
profiles for three, four, and five candidates. It checks 56, 2,600, and
295,240 multiset profiles, respectively. In all three atlases, every unique
non-unanimous profile has radius one and the only radius-three profiles are
the \(m!\) unanimous profiles, as Corollary 4.1 requires.

## 10. A robust market-design application

Carroll studies a bilateral accept/reject game for one fixed deal under
uncertainty about the agents' information structure. Under his Condition B,
the simple consent mechanism achieves the optimal robust guarantee. That
single-deal result has no ranking-aggregation stage, so the Peters theorem does
not apply to it directly.

Carroll's Section 5.3 asks about multiple alternative deals and leaves that
extension open. Consider a two-stage mechanism that first ranks candidate
proposals using three priority lists and then submits the selected proposal to
bilateral accept/reject. The three rankings might come from a buyer, seller,
and regulator, or from price, time, and size priorities on a set of orders.

**Proposition 6 (market-priority hardness).** Suppose distinct orders receive
separate price, time, and size rankings, and a composite priority rule minimizes
total Kendall distance to those three rankings. Computing the exact composite
ranking is NP-hard in the number of orders.

**Proof.** Any three rankings can be encoded by assigning distinct prices in
the order of the first ranking, timestamps in the order of the second, and
sizes in the order of the third. An exact composite-priority solver would
therefore solve an arbitrary three-voter Kemeny instance. Peters's theorem
gives the result. \(\square\)

The radius dichotomy then says that a unique non-unanimous composite has cover
radius one. This applies to adding or removing a priority source, not to a
small numeric perturbation of an order attribute.

The hardness is domain-dependent. For one-dimensional proposal prices and
three single-peaked stakeholder rankings, pairwise majority is transitive and
the generic feedback-arc obstruction disappears. In 500 synthetic trials at
each of 5, 8, 10, and 12 proposals, every single-peaked instance had a unique
Kemeny ranking and no majority cycle. With independent price, time, and size
rankings, the observed majority-cycle rates were 0.350, 0.760, 0.914, and
0.986. These are computational illustrations, not equilibrium or welfare
claims; finite-sample intervals are reported in the experiment artifact.

A Carroll-style economic extension must specify how proposal selection changes
the prior over bilateral values, the allowed cross-proposal information
structures, strategic reporting in the ranking stage, and equilibrium
selection. The present proposition establishes a computational boundary for a
candidate selection layer; it does not extend Carroll's robust welfare theorem.

## 11. A Hex/Y local-to-global extension

This section is deliberately separate from the rank-aggregation theorems.
Karlin and Peres describe the following reduction for the game of Y. A
complete two-color triangular hex board has a unique monochromatic connected
component meeting all three sides. Replacing each cell of a board of side
\(n-1\) by the majority color of its corresponding triangle of three adjacent
cells in the side-\(n\) board preserves the winner. Iteration reaches one cell.
This is a known combinatorial-game result, not a contribution of this note.

The reduction also gives an exact monotone ternary-majority circuit. Its depth
is \(n-1\), and its number of gates is

\[
\sum_{k=1}^{n-1}\frac{k(k+1)}2
=\frac{(n-1)n(n+1)}6
=\binom{n+1}{3}.
\]

This representation is exact on the Boolean domain; it is not a learned
smooth approximation.

The cover geometry supplies a new application of the same sensitivity
language. Let \(T_n\) be the cells and represent a coloring by its blue subset
\(B\subseteq T_n\). Covers in the Boolean lattice \(2^{T_n}\) add one blue
cell; the undirected Hasse graph joins colorings differing at one cell, and
its metric is Hamming distance. Let \(w(B)\in\{0,1\}\) be the unique winner and

\[
R_Y(B)=\min\{|B\mathbin{\triangle}B'|:w(B')\ne w(B)\}.
\]

In picture-language terms, the local rewrite is sound because the winner maps
commute:

\[
w_{n-1}\circ M_n=w_n.
\]

Thus repeated picture reduction is complete for the specific winner query.
No completeness claim is made for arbitrary connectivity, influence, or
probability questions.

**Proposition 7 (exact binary smooth sensitivity).** For any nonconstant total
binary query on a Hamming graph, including \(w\),

\[
SS_\beta(B)=
\exp\{-\beta\max(R_Y(B)-1,0)\}.
\]

**Proof.** The local sensitivity is one exactly on the set \(\Pi\) of pivotal
inputs. Along a shortest path from \(B\) to the opposite output, the
penultimate input is pivotal, so \(d(B,\Pi)\le R_Y(B)-1\). Conversely, a
pivotal input at distance \(d\) has an opposite-output neighbor at distance at
most \(d+1\), so \(R_Y(B)\le d+1\). Hence
\(d(B,\Pi)=R_Y(B)-1\). Maximizing
\(e^{-\beta d(B,B')}LS(B')\) therefore gives the displayed identity.
\(\square\)

This is a general Boolean-function specialization of smooth sensitivity, and
no novelty claim is made. It does not by itself make exact winner release
private: adjacent pivotal colorings have different deterministic outputs.

The implementation found zero unique-winner or reduction failures for every
board through side six, including all \(2^{21}=2{,}097{,}152\) colorings at
side six. Exact uniform-random-cell pivotal probabilities for sides one
through five were

\[
1,\quad 0.5,\quad 0.3125,\quad 0.22109375,\quad 0.16826171875.
\]

Monte Carlo estimates at larger sizes suggest threshold sharpening as the
blue-cell probability moves away from one half; these finite observations are
not an asymptotic theorem. The full counts, Wilson intervals, outcome-radius
histograms, and implementation details appear in `notes/HEX_Y.md` and
`results/hex_y.json`.

The occurrence of three inputs in the local majority gate does not invoke
Peters's hardness theorem. A fixed binary majority gate is constant-size,
whereas Peters concerns a Kemeny median of three arbitrary permutations as
the candidate count grows. The common structure is the cover-radius question,
not computational complexity.

## 12. Benchmark-validity extensions

Two small exact laboratories record evaluation distinctions that apply to
future computational work but do not alter the Kemeny or privacy theorems.

First, the grounded Button Game of Gessler et al. has hidden bit
\(b\in\{0,1\}\), sender button \(a\), and observed bulb
\(\ell=2a+b\). Parity decodes \(b\) independently of \(a\). A receiver that
learns parity only for one button and uses a fixed guess elsewhere has
self-play accuracy one and off-diagonal cross-play accuracy one half; covering
all buttons restores accuracy one. This is a state-coverage failure.

Coverage cannot solve every coordination problem. Consider the two
ungrounded encoders \(e_0=(0,1)\) and \(e_1=(1,0)\). Both cover both messages.

**Proposition 8 (binary convention obstruction).** A paired encoder-decoder
has uniform-bit accuracy one, a crossed pair has accuracy zero, and every
fixed deterministic decoder has mean accuracy one half under a uniform choice
of encoder. One labeled interaction identifies the active bijective encoder.

**Proof.** A paired decoder is the inverse and the crossed inverse flips both
bits. Across the two encoders, each observed message corresponds once to each
hidden bit, so a fixed guess is correct in exactly half the encoder-bit cases.
The equality or inequality of one observed message and its revealed bit
distinguishes identity from flip. \(\square\)

Second, following Kong, Ram, and Yu, the implementation reports oracle-match
rate, longest labeled oracle-consistent chain, first failure in original game
plies, and perfect-trace rate separately. An exact Chomp oracle uses

\[
g(s)=\operatorname{mex}\{g(s'):s'\in N(s)\},
\]

and labels moves from \(g(s)\ne0\) as optimal precisely when they reach Grundy
zero. Exhaustion of all 923 nonempty partition states in a \(6\times6\) box
finds 875 winning labeled states. The exact policy matches all 875. A
largest-bite negative control matches only 10, or \(2/175\), and has no
perfect trace on the 25 full rectangular starts with side lengths two through
six. This is an implementation check, not an AlphaZero reproduction.

The PIKS analysis of Bona-Pellissier et al. supplies a compatible caution:
ordinary value convergence and linear-operator consistency are distinct
claims. Its universal-consistency theorem depends on RKHS density, bounded
linear operators, compatible sampling, bounded data and features, and a
regularization regime. Transitivity of finite rankings is not such a
differential operator, so no PIKS theorem is imported. Future Kemeny
heuristics should nevertheless report objective regret and structural
validity separately.

## 13. Relation to prior work and open questions

Hay, Elagina, and Miklau introduced differentially private rank aggregation.
Alabi et al. studied private rank aggregation in central and local models, and
Hillebrand et al. subsequently improved private algorithms. Goibert et al.
study robustness and breakdown functions for ranking medians. Proposition 4.1
now gives the exact zero-plus comparison under standard half-\(L^1\) TV:
the cover radius is a discretized normalized margin, continuous breakdown is
an exact mass-transport problem, and the factor-two bridge holds under a
sufficient endpoint-mass condition. Novelty remains unconfirmed.

The Johnson–Lindenstrauss direction is geometric but incomplete. Pairwise
preference vectors embed rankings into \(\{-1,+1\}^D\), with Kendall distance
proportional to their Hamming distance. Random projection can preserve
Euclidean geometry of a fixed finite family, and some JL transforms satisfy
differential privacy under additional spectral assumptions. Neither fact
alone preserves the transitivity constraint or yields a private Kemeny
mechanism. A valid result needs to control projection distortion, privacy
adjacency, and postprocessing back into the linear-order polytope together.

Concrete open problems are:

1. compare subset DP with ILP and fixed-parameter Kemeny oracles;
2. turn Theorem 5 into an end-to-end ranking-output mechanism;
3. complete the center-of-attention privacy and utility analysis;
4. determine whether JL dimension reduction improves any end-to-end
   rank-aggregation privacy/utility bound after enforcing transitivity; and
5. compare the Y pivotality data with rigorous influence and sharp-threshold
   results for monotone Boolean functions.

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
7. M. Goibert, C. Calauzènes, E. Irurozki, and S. Clémençon. “Robust
   Consensus in Ranking Data Analysis: Definitions, Properties and
   Computational Issues.” ICML, 2023.
   [PMLR](https://proceedings.mlr.press/v202/goibert23a.html).
8. J. Blocki et al. “The Johnson-Lindenstrauss Transform Itself Preserves
   Differential Privacy.” FOCS, 2012.
   [arXiv:1204.2136](https://arxiv.org/abs/1204.2136).
9. G. Carroll. “Informationally Robust Trade and Limits to Contagion.”
   *Journal of Economic Theory* 166, 2016, 334–361.
   [Author PDF](http://individual.utoronto.ca/carroll/robustlemons.pdf).
10. E. Budish, P. Cramton, and J. Shim. “The High-Frequency Trading Arms
    Race: Frequent Batch Auctions as a Market Design Response.” *Quarterly
    Journal of Economics* 130(4), 2015, 1547–1621.
    [DOI](https://doi.org/10.1093/qje/qjv027).
11. A. R. Karlin and Y. Peres. *Game Theory, Alive*. American Mathematical
    Society, 2017.
    [Author PDF](https://math.uchicago.edu/~shmuel/Modeling/Peres%20and%20Wilson%2C%20Game%20Theory%20Alive.pdf).
12. A. M. Jaffe and Z. Liu. "A Mathematical Picture Language Program."
    *Proceedings of the National Academy of Sciences* 115(1), 2018, 81-86.
    [DOI](https://doi.org/10.1073/pnas.1710707114).
13. K. De, H. Mittal, P. Dey, and N. Misra. "Parameterized Aspects of
    Distinct Kemeny Rank Aggregation." 2023.
    [arXiv:2309.03517](https://arxiv.org/abs/2309.03517).
14. T. Gessler et al. "OvercookedV2: Rethinking Overcooked for Zero-Shot
    Coordination." ICLR, 2025.
    [arXiv:2503.17821](https://arxiv.org/abs/2503.17821).
15. B. Kong, T. Ram, and T. Y. Yu. "AlphaZero in Sparsely Rewarded Games:
    Limits and Auxiliary Supervision." 2026.
    [arXiv:2607.08984](https://arxiv.org/abs/2607.08984).
16. J. Bona-Pellissier, G. Meanti, M. Santacesaria, and L. Rosasco. "PIKS:
    Universal Physics-Informed Kernel Methods." 2026.
    [arXiv:2607.27062](https://arxiv.org/abs/2607.27062).

## Acknowledgments

OpenAI Codex provided computational and editorial assistance. It is not an
author.
