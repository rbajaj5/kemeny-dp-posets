# Loop Equations: Source Assessment and Finite-Poset Transfer

## Verdict

Bourgade and Huang prove a genuine local-to-global characterization theorem,
but it is a theorem about random point processes, Nevanlinna functions, and
the full bulk or edge loop-equation hierarchy. It does not imply a new Kemeny,
differential-privacy, market, or Hex theorem.

The useful transfer to this repository is methodological:

1. identities must be accompanied by a uniqueness argument;
2. approximate identities require quantitative control of their error and
   exceptional events;
3. a linearized system can have many branches, so boundary or asymptotic data
   must select the intended one; and
4. a full hierarchy can characterize a law even when low-order summaries do
   not.

The fourth point has an exact finite-poset counterpart. This note proves that
counterpart by standard Möbius inversion and makes it executable.

## 1. What the source proves

Let `s` be a particle-generated Nevanlinna function whose poles form a locally
finite point configuration on the real line.

- Theorem 1.5: for rational `beta_RMT > 0`, the full bulk loop hierarchy in
  Assumption 1.4 uniquely identifies the Sine-beta point process.
- Theorem 1.11: under the analogous edge hierarchy in Assumption 1.10, it
  uniquely identifies the Airy-beta point process.
- Theorems 1.9 and 1.12: approximate hierarchies, with their stated uniform
  moment error bounds on high-probability events, give vague convergence to
  those processes.
- Conjecture 1.13, not a theorem, removes the rationality restriction.

The rationality assumption enters the proof through balanced exponential
observables and the deformed Calogero-Moser-Sutherland system. The paper says
the characterization itself is expected for every positive beta, but proves
it only for rational beta.

The applications include a loop-equation proof of fixed-energy bulk
universality for real Wigner matrices and bulk universality for random
`d`-regular graphs in the regime `d >> (log N)^24`. The latter exponent is
explicitly not claimed to be optimal.

Appendix F makes the equilibrium-statistical-mechanics connection precise.
Under its count-discrepancy estimate (F.4), Proposition F.4 shows that a
one-dimensional logarithmic point process satisfying the distributional
equilibrium BBGKY hierarchy has the bulk loop hierarchy and therefore is
Sine-beta for rational positive beta. The appendix also explains algebraically
how boundary jumps of the loop equations recover the pointwise BBGKY equation
away from collision diagonals; it notes that a fully rigorous converse must be
formulated with local test functions and limits.

## 2. What the supplied excerpts add

The excerpts identify three proof obligations that an abstract summary can
hide.

### 2.1 Resolvent cancellation

Equations (2.43)-(2.45) differentiate the resolvent observable
`G_ij(z) M_p`, sum over matrix entries, and express the result using
`m_N`, its derivative, and divided differences. Substitution cancels the
leading `E[m_N(z)^2 M_p]` term. Equations (2.48)-(2.50) then pass to
microscopic variables and absorb the remaining `1/N` term into the stated
moment-controlled error.

This is the algebraic hinge that produces the approximate bulk hierarchy. A
generic slogan about integration by parts would miss the cancellation and the
normalization on which it depends.

### 2.2 Good-event and bad-event control

The Gronwall step (2.31)-(2.33) propagates a resolvent bound from imaginary
height `N^(-1+gamma)` down to a smaller height `s`, giving a polynomial
bound. In the random-regular-graph application, the proof separately controls
the good event and its complement. Equation (2.83) combines the trivial
polynomial resolvent bound with
`Pr(Omega_N^c) <= exp(-(log N)^2)`, so the bad-event contribution is still
`o_N(1)` for each fixed hierarchy order `p`.

Thus a small formal residual is not enough. The proof also needs uniform
integrability, tightness or local-law control, and an exceptional-event bound
strong enough to dominate the worst permitted observable.

### 2.3 Branch selection

Linearization does not itself prove uniqueness. The deformed CMS system has
`2^(n+m)` local asymptotic branches indexed by sign patterns. Proposition 8.4
constructs shifted rays that stay in their half-planes, avoid collisions, and
give uniform square-root growth. Proposition 8.5 turns the edge equations
along those rays into a radial block system with a spectral separation. The
asymptotics then select the physical branch.

The repository-level lesson is precise: an equation solver, local rewrite, or
small residual does not identify the intended object unless the admissible
class and branch-selection data are stated.

## 3. Exact finite profile-poset characterization

Fix a maximum database size `N` and a finite ranking space with `d` rankings.
Let

```text
P_N = {x in nonnegative integers^d : sum(x) <= N}
```

with coordinatewise order. This is the finite lower ideal of the multiset
profile poset through level `N`. Let `X` be a random element of `P_N`, and
define the full upper-set hierarchy

```text
Z(x) = Pr[X >= x] = sum_{y >= x} p(y).
```

**Proposition.** The values `Z(x)` for all `x` in `P_N` uniquely determine
the probability mass function `p`.

**Proof.** Process the states in decreasing rank. At a maximal state,
`p(x) = Z(x)`. Once all strict upper states have been recovered,

```text
p(x) = Z(x) - sum_{y > x} p(y).
```

Descending induction recovers every mass exactly. This is finite-poset
Möbius inversion. The Hasse diagram suffices because `y >= x` is precisely
reachability by upward cover steps.

This proposition is standard incidence-algebra theory specialized to the
profile poset. No novelty claim is made.

## 4. Why low-order summaries are insufficient at three voters

Use three candidates, so a profile has six ranking coordinates. Consider two
laws supported on the three-voter layer:

```text
Law A: X = (1,1,1,0,0,0) with probability 1.

Law B: X = (2,1,0,0,0,0) with probability 1/2,
       X = (0,1,2,0,0,0) with probability 1/2.
```

Both have expected profile `(1,1,1,0,0,0)`, so first moments do not identify
the law. The upper-set query at `(2,1,0,0,0,0)` separates them: it has
probability zero under Law A and one half under Law B.

The executable audit covers all 84 profiles through three ballots, linked by
168 upward covers. It reconstructs a nontrivial rational law with zero exact
error and verifies the three-voter first-moment collision.

## 5. Relation to the existing program

| Object | Local or hierarchical data | What identifies the target | Status |
|---|---|---|---|
| Bourgade-Huang bulk process | Full loop hierarchy plus Nevanlinna structure | Concentration, linearization, asymptotics, and uniqueness | **KNOWN SOURCE THEOREM** |
| Bounded random profile | All upper-set probabilities | Exact finite Möbius inversion | **PROVED; STANDARD SPECIALIZATION** |
| Unique Kemeny optimizer | Score gaps against every competitor | Exact cover-radius formula | **PROVED IN REPOSITORY** |
| Y-game winner | Majority-triangle rewrites | Known path lifting and reduction | **KNOWN; IMPLEMENTED** |
| Finite simulation residual | Selected probes only | Nothing without a separate completeness theorem | **DIAGNOSTIC ONLY** |

The table records a shared proof pattern, not a theorem transfer between
domains.

## 6. Notation and claim boundaries

- `beta_RMT` is the random-matrix inverse-temperature/symmetry parameter.
- `beta_SS` is the exponential decay parameter in smooth sensitivity.

They are unrelated despite using the same Greek letter in their source
literatures.

The finite-poset hierarchy is not a differential-privacy mechanism. Publishing
all upper-set probabilities of a private random profile could disclose the
entire law; any release would require its own adjacency, sensitivity, and
mechanism analysis.

The source also does not show that Kemeny rankings, market order books, Hex
boards, or game histories have Sine-beta or Airy-beta statistics.

## 7. Reproduction

```bash
python scripts/run_profile_law_hierarchy.py
python -m unittest tests.test_law_hierarchy -v
```

The machine-readable output is
`results/profile_law_hierarchy.json`.

## Source

- Paul Bourgade and Jiaoyang Huang,
  [*Loop Equations Characterize Random Matrix Statistics*](https://arxiv.org/abs/2607.07617),
  arXiv:2607.07617v1, 8 July 2026.
