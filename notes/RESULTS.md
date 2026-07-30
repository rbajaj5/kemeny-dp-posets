# Cover-Graph Stability and Smooth Sensitivity for Kemeny Aggregation

## Status

This is an executable research note. Claims marked **Proved** have proofs below
and are checked exhaustively for every profile of up to four ballots over three
candidates. The positioning against prior literature is not a claim of novelty.
In particular, the integer stability radius is closely related to breakdown
functions for ranking medians and needs a careful equivalence comparison.

## 1. The profile poset

Fix `m` candidates and let `S_m` be the set of all rankings. A profile is a
finite multiset of rankings, equivalently a vector

```text
x in N^(m!).
```

Order profiles componentwise. Profile `y` covers `x` exactly when

```text
y = x + e_pi
```

for one ranking `pi`. The undirected Hasse graph is therefore exactly the
add/remove-one-ballot adjacency graph used by unbounded differential privacy.
Its path metric is

```text
d_H(x, y) = ||x - y||_1.
```

This makes the slide deck's covering-relation viewpoint operational: local
sensitivity lives on Hasse edges, while smooth sensitivity discounts entire
Hasse shells.

**Proved.** The statements follow directly from the componentwise order on
`N^(m!)`: each cover changes one coordinate by one, and any path between two
count vectors must perform at least their L1 difference in unit coordinate
changes. That lower bound is attained by deleting surplus counts and adding
deficient counts.

## 2. Baseline sensitivity

Let `d` be Kendall distance and

```text
D = choose(m, 2)
C_x(sigma) = sum_pi x_pi d(pi, sigma)
OPT(x) = min_sigma C_x(sigma).
```

**Proved.** For a fixed output ranking `sigma`, `C_x(sigma)` has global
sensitivity `D`. The scalar `OPT(x)` also has global sensitivity at most `D`.

**Proof.** Adding or removing one ballot changes a fixed score by a value in
`[0,D]`. If every function in a family is `D`-Lipschitz, their pointwise
minimum is also `D`-Lipschitz.

The bound is tight. For example, adding the reverse of the sole unanimous
ranking to a one-ballot profile changes `OPT` from `0` to `D`.

### Exact local sensitivity from one score landscape

Let

```text
g_x(sigma) = C_x(sigma) - OPT(x).
```

**Proved.** The change caused by adding ballot `rho` is exactly

```text
OPT(x + e_rho) - OPT(x)
  = min_sigma [g_x(sigma) + d(rho, sigma)].
```

For an existing ballot `rho`, the change caused by its removal is exactly

```text
OPT(x) - OPT(x - e_rho)
  = max_sigma [d(rho, sigma) - g_x(sigma)].
```

Taking the maximum of these expressions over possible additions and valid
removals gives `LS_OPT(x)`. The code computes this expression and checks it
against explicit neighbor enumeration on every three-candidate profile with up
to four ballots.

**Proof.** Substitute
`C_(x+e_rho)(sigma)=C_x(sigma)+d(rho,sigma)` into the definition of `OPT` and
subtract `OPT(x)`. The removal identity follows similarly from
`C_(x-e_rho)(sigma)=C_x(sigma)-d(rho,sigma)`.

## 3. Exact Hasse distance to loss of a unique Kemeny optimum

Assume `sigma` is the unique Kemeny optimum at profile `x`. For every
competitor `tau != sigma`, define

```text
gap_x(tau) = C_x(tau) - C_x(sigma) > 0.
```

### Proposition (Proved)

The exact distance in the profile Hasse graph to a profile where `sigma` is no
longer uniquely optimal is

```text
R(x) = min_{tau != sigma}
       ceil(gap_x(tau) / d(sigma, tau)).
```

Set `R(x)=0` when the optimum is already non-unique.

### Proof

For one cover step that adds or removes ballot `pi`, the competitor gap changes
by

```text
+/- [d(pi, tau) - d(pi, sigma)].
```

The reverse triangle inequality bounds its magnitude by `d(sigma,tau)`.
Consequently, after `k` Hasse steps, the gap against `tau` can fall by at most
`k d(sigma,tau)`. If

```text
k < ceil(gap_x(tau) / d(sigma,tau)),
```

the gap remains positive.

The bound is attained: add `k` copies of the competitor ranking `tau`.
Every such addition reduces its gap against `sigma` by exactly
`d(sigma,tau)`. At the displayed ceiling, `tau` ties or beats `sigma`.
Taking the minimum over competitors proves the formula.

### Interpretation

This is an integer, finite-sample analogue of a breakdown radius. It is sharper
than using only the second-best score gap because competitors farther from the
optimum can close their gap faster per added ballot.

## 4. A smooth upper bound for ranking-output sensitivity

Let `kappa(x)` be a deterministic Kemeny selector using any fixed tie-breaking
rule, and measure output changes in Kendall distance. Its global sensitivity is
at most `D`, but it can be zero on stable profiles.

For a unique profile, let `R(x)` be the radius above; for a tied profile set it
to zero. Define

```text
B_beta(x) = D exp(-beta max(R(x)-1, 0)).
```

### Proposition (Proved)

`B_beta` is a beta-smooth upper bound on the local sensitivity of `kappa`.

### Proof sketch

- If `R(x) >= 2`, every neighbor still has the same unique optimum, so local
  sensitivity is zero.
- If `R(x) <= 1`, `B_beta(x)=D`, which bounds any Kendall change.
- Within a region having the same unique optimum, `R` is distance to the
  region's complement and changes by at most one across a Hasse edge.
- An edge crossing between optimum regions has radius at most one at both
  endpoints; an edge incident to a tied profile is handled by the clipping.

Therefore the exponent changes by at most `beta` on every edge, giving

```text
B_beta(x) <= exp(beta) B_beta(y)
```

for neighboring profiles.

This is a sensitivity result, not yet a complete discrete-output mechanism.
One path is to embed a ranking as its pairwise-preference vector, add
smoothly-calibrated vector noise, and postprocess back to a ranking. Exact
nearest-ranking postprocessing is another feedback-arc/Kemeny problem, so
efficient approximation and utility analysis remain open.

## 5. Exact smooth sensitivity of the scalar optimal score

For the scalar `OPT`, the code computes

```text
SS_beta(x) = max_y LS_OPT(y) exp(-beta d_H(x,y))
```

by complete Hasse-shell search. The search is exact when it stops: after shell
`k`, every unseen contribution is at most

```text
D exp(-beta (k+1))
```

because `D` is the global sensitivity. Once this tail is no larger than the
best observed contribution, no unseen profile can improve the maximum.

`release_optimum_score` then instantiates the one-dimensional Laplace
calibration from Nissim, Raskhodnikova, and Smith (2007):

```text
alpha = epsilon / 2
beta  = epsilon / (2 log(2/delta))
release = OPT(x) + SS_beta(x)/alpha * Laplace(1).
```

This mechanism releases the **optimal score**, not an optimal ranking.

## 6. Where the 2026 three-voter hardness result enters

Nissim-Raskhodnikova-Smith explicitly note that medians in permutation spaces
can be NP-hard and replace the metric median in sample-and-aggregate with an
efficient center-of-attention aggregator based only on pairwise distances.
Peters (2026) sharpens the computational obstruction: exact Kemeny aggregation
is NP-hard already for three rankings.

That gives a concrete design constraint for private sample-and-aggregate:

- exact Kemeny on three or more subaggregate rankings cannot be the generic
  polynomial-time combining step unless P=NP;
- the center-of-attention aggregator remains efficient because Kendall
  distances are efficient;
- block estimators may use exact two-voter Kemeny, Borda/footrule, or a Kemeny
  approximation, followed by center-of-attention.

The repository does not yet claim a new end-to-end utility theorem for this
pipeline. It now includes an executable utility prototype:

```text
random ballot blocks
  -> exact small-block Kemeny outputs
  -> constrained center-of-attention under Kendall distance.
```

The final center is always one of the block outputs and is computed using only
their pairwise distances. No privacy claim attaches to this prototype until the
sampling influence and admissible-noise steps are implemented and analyzed.

## 7. Johnson-Lindenstrauss direction

Dwork's 2008 survey uses Johnson-Lindenstrauss projection to preserve angles
for halfspace-query utility before private release. A ranking has a natural
pairwise sign-vector embedding in dimension `D`, where L1 distance corresponds
to Kendall distance.

An open direction is to project a finite candidate family of such embeddings
to lower dimension, privately estimate or select there, and postprocess to a
transitive ranking. What is currently justified:

- random projection can preserve Euclidean geometry of a fixed finite family;
- later work shows some JL transforms themselves provide DP under additional
  spectral and adjacency assumptions;
- neither fact alone proves a private, utility-preserving Kemeny mechanism.

The transitivity constraint and the mismatch between Euclidean distortion and
Kendall/L1 objectives are the main technical obstacles.

## 8. Computational observations

Run:

```bash
python scripts/run_experiments.py
```

The generated results exhaust all profiles with three candidates and zero to
four ballots. They verify the uniqueness-radius proposition by a separate BFS
oracle in the test suite and record:

- uniqueness and tie frequencies;
- exact local sensitivity of `OPT`;
- local sensitivity of the selected ranking;
- the smooth radius bound at `beta=0.7`;
- exact scalar smooth sensitivity for representative profiles.

These observations are finite checks, not asymptotic theorems.
