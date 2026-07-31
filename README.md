# Kemeny DP Posets

**Authors:** Ravi Andrew Bajaj and Alexander Burns

An executable research note connecting three ideas:

1. rank-profile adjacency as a covering relation in a graded multiset poset;
2. Kemeny-optimum stability measured by distance in that Hasse graph; and
3. local and smooth sensitivity for differentially private rank aggregation.

The main proved observation is an exact certificate for a **unique** Kemeny
ranking. If `sigma` is the unique optimum for profile `P`, define

```text
gap_P(tau) = cost_P(tau) - cost_P(sigma).
```

Under add/remove-one-ballot adjacency, the exact Hasse distance at which
`sigma` can cease to be uniquely optimal is

```text
R(P) = min_{tau != sigma} ceil(gap_P(tau) / Kendall(sigma, tau)).
```

This turns the score-gap landscape into an instance-specific robustness
certificate. It also yields a beta-smooth upper bound for the Kendall-metric
local sensitivity of a deterministic Kemeny selector:

```text
B_beta(P) = choose(m, 2) * exp(-beta * max(R(P) - 1, 0)).
```

For the empirical law `p=P/|P|`, define

```text
mu(P) = min_{tau != sigma}
        gap_P(tau) / (|P| Kendall(sigma,tau)).
```

The repository now computes the exact zero-plus contamination breakdown under
the standard convention `TV(p,q)=||p-q||_1/2`. It proves

```text
R(P) = ceil(|P| mu(P))
b_TV(p) >= mu(P)/2.
```

When `mu(P) <= 2p(sigma)`, the second relation is an equality and
`R(P)=ceil(2|P|b_TV(p))`. The [comparison note](notes/BREAKDOWN_COMPARISON.md)
also identifies a factor-of-two normalization inconsistency between Equation
(4) and Appendix C.2 of the closest ICML 2023 paper. This is a comparison of
two distinct perturbation models, not a claim that Hasse adjacency equals TV.

The distance-stratified subset DP computes the complete profile

```text
F_P(d) = min_{tau: Kendall(sigma, tau) = d} cost_P(tau)
```

in `O(m D 2^m)` time after transition precomputation, where
`D = choose(m, 2)`. It returns the second-best ranking, the exact radius, and
a constructive competitor whose repeated addition makes the selected optimum
lose uniqueness. This avoids factorial enumeration while remaining
exponential, as the three-voter hardness result requires.

A further proved corollary is especially sharp at the Peters boundary:
every unique, non-unanimous three-voter profile has `R(P)=1`, whereas every
unanimous three-voter profile has `R(P)=3`. Thus computational hardness and
cover stability separate cleanly: finding the optimum is hard in the candidate
count even though its three-voter stability radius has only this dichotomy.

The formal write-up is [`paper/PAPER.md`](paper/PAPER.md). Supporting proof
notes, literature positioning, limits, and proposed research directions are in
[`notes/RESULTS.md`](notes/RESULTS.md). Dedicated application notes cover the
[`PDF's three-voter directions`](notes/THREE_VOTER_APPLICATIONS.md) and
[`robust market design`](notes/MARKET_MICROSTRUCTURE.md). A separate
[`Hex/Y laboratory`](notes/HEX_Y.md) formalizes the coloring Boolean lattice,
the majority reduction, pivotality, and exact binary smooth sensitivity.
The [`TUFT source assessment`](notes/TUFT_SOURCE_ASSESSMENT.md) records the
strict heuristic-only boundary for the latest supplied source. This is a
research scaffold, not a peer-reviewed novelty claim.

The [`KAN/Hex assessment`](notes/KAN_HEX_ASSESSMENT.md) applies the supplied
critical KAN survey as an evaluation guardrail: it derives and benchmarks the
exact majority circuit instead of assuming that smooth spline models help on
a discontinuous combinatorial target. The
[`AI-risk governance note`](notes/AI_RISK_GOVERNANCE.md) keeps scenario
taxonomy separate from probability claims and deployment.

The [`picture-language transport audit`](notes/PICTURE_LANGUAGE.md) follows
Jaffe and Liu's separation of language `L`, target reality `R`, and simulation
`S`. It records exactly which Hasse, Hex, JL, and market diagrams transport
proved statements and which remain heuristic.

The [`loop-equations source assessment`](notes/LOOP_EQUATIONS_ASSESSMENT.md)
uses Bourgade and Huang's uniqueness proof as a guardrail for local-to-global
claims. Its executable finite analogue shows that the full upper-set
probability hierarchy on a bounded profile poset determines a random-profile
law exactly by Möbius inversion, while first moments do not, even on the
three-voter layer. No random-matrix or privacy theorem is inferred.

The [`Tagore source and policy note`](notes/TAGORE_USELESS_WORK.md) protects
room for exploratory work whose use is not yet known, while keeping the
proof-and-provenance threshold unchanged. It also identifies the supplied
story as section 26 of *The Fugitive-III*, rather than *Gitanjali*.

The [`sample-and-center audit`](notes/SAMPLE_AGGREGATE_AUDIT.md) proves the
sharp factor-two input-center lemma, implements a linear-time exact
two-ballot shortcut and a Borda block option, and exhaustively tests metric
witnesses, relabeling, approximation, and invalid-remainder validation. It
does not claim an end-to-end private mechanism.

The [`OvercookedV2 benchmark assessment`](notes/OVERCOOKEDV2_BENCHMARK_ASSESSMENT.md)
separates state-coverage failures from incompatible conventions with two
exact finite games. The
[`AlphaZero oracle assessment`](notes/ALPHAZERO_ORACLE_ASSESSMENT.md) adds
generic move-level oracle metrics and an exact small-board Chomp laboratory.
The [`PIKS assessment`](notes/PIKS_SOURCE_ASSESSMENT.md) adopts the narrower
discipline of measuring fit and structural residual separately while
documenting why no RKHS/PDE consistency theorem transfers here.

The [`zero-mass counterexample assessment`](notes/ZERO_MASS_SOURCE_ASSESSMENT.md)
checks Li and Xia's exact finite-stage degree normalization while leaving the
pluripotential-theoretic limiting argument to the source. It also explains
why plurisubharmonic functions and the zero-mass conjecture are distinct from
the one-variable Bieberbach coefficient problem.

## What runs

- exact Kemeny enumeration for small candidate sets;
- exact subset-DP Kemeny optimization in `O(m^2 2^m)` time;
- distance-stratified subset DP for score-gap and instability witnesses;
- exact zero-plus standard-TV breakdown and cover-radius comparison;
- cover-graph parents, children, distances, and finite Hasse diagrams;
- exact local sensitivity of the optimal Kemeny score;
- exact smooth sensitivity of that scalar score by certified shell search;
- the uniqueness-radius formula plus exhaustive verification;
- a global-sensitivity exponential-mechanism baseline;
- the one-dimensional Nissim-Raskhodnikova-Smith smooth-sensitivity release
  for the optimal score;
- exact block Kemeny outputs and the efficient NRS center-of-attention in
  Kendall space as a non-private sample-and-aggregate utility prototype;
- exact attention certificates, a two-ballot Kemeny shortcut, and Borda block
  outputs with exhaustive component audits;
- three-voter JL, private-learning, and market-priority experiments;
- exact triangular Y-game connectivity and majority reduction;
- exact small-board pivotality, outcome radii, and binary smooth sensitivity;
- exact majority-circuit size and repeated connectivity-versus-circuit timings;
- exact upper-set transforms and Möbius inversion for laws on bounded profile
  posets, including a three-voter first-moment counterexample;
- exact grounded-coverage and ungrounded binary-protocol coordination games;
- exact oracle-match, longest-chain, first-failure, and perfect-trace metrics;
- a memoized exact Chomp Grundy oracle and exhaustive states through a
  six-by-six bounding box;
- exact finite-stage degree, Lelong-number, and normalized-mass scaling for
  the supplied zero-mass counterexample source;
- reproducible CSV/JSON experiments and SVG Hasse diagrams for both profile
  and coloring cover relations.

## Quick start

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/run_experiments.py
python scripts/run_three_voter_applications.py
python scripts/run_subset_dp_certificates.py
python scripts/run_breakdown_comparison.py
python scripts/run_sample_aggregate_audit.py
python scripts/run_market_microstructure.py
python scripts/run_hex_y.py --exhaustive-max 6
python scripts/run_profile_law_hierarchy.py
python scripts/run_coordination_audit.py
python scripts/run_oracle_consistency_audit.py
python scripts/run_zero_mass_scaling_audit.py
python scripts/generate_hasse.py
python scripts/generate_hex_hasse.py
```

The code uses only the Python standard library.

## Research status

The repository deliberately separates:

- `PROVED`: statements proved in the note and checked exhaustively on small
  instances;
- `KNOWN`: prior results with citations;
- `COMPUTATIONAL`: finite experiments;
- `CONJECTURE` or `OPEN`: directions that still require proof.

The closest prior robustness work is the breakdown-function analysis of
ranking medians by Goibert et al. (ICML 2023). The repository now gives the
exact zero-plus comparison under standard half-`L1` TV, including the
factor-two bridge and its limits. Novelty is still unconfirmed.

## Sources

- [Dwork, *Differential Privacy: A Survey of Results* (2008)](https://www.microsoft.com/en-us/research/wp-content/uploads/2008/04/dwork_tamc.pdf)
- [Nissim, Raskhodnikova, and Smith, *Smooth Sensitivity and Sampling in Private Data Analysis* (2007)](https://people.csail.mit.edu/asmith/PS/stoc321-nissim.pdf)
- [Hay, Elagina, and Miklau, *Differentially Private Rank Aggregation* (2017)](https://people.cs.umass.edu/~miklau/assets/pubs/dp/hay17differentially.pdf)
- [Alabi et al., *Private Rank Aggregation in Central and Local Models* (2022)](https://arxiv.org/abs/2112.14652)
- [Hillebrand et al., *Improved Differentially Private Algorithms for Rank Aggregation* (2026)](https://arxiv.org/abs/2511.11319)
- [Peters, *Kemeny Rank Aggregation is NP-Hard for Three Voters* (2026)](https://arxiv.org/abs/2607.25540)
- [De et al., *Parameterized Aspects of Distinct Kemeny Rank Aggregation* (2023)](https://arxiv.org/abs/2309.03517)
- [Goibert et al., *Robust Consensus in Ranking Data Analysis* (2023)](https://proceedings.mlr.press/v202/goibert23a.html)
- [Carroll, *Informationally Robust Trade and Limits to Contagion* (2016)](http://individual.utoronto.ca/carroll/robustlemons.pdf)
- [Karlin and Peres, *Game Theory, Alive*](https://math.uchicago.edu/~shmuel/Modeling/Peres%20and%20Wilson%2C%20Game%20Theory%20Alive.pdf)
- [Hou et al., *Kolmogorov-Arnold Networks: A Critical Assessment*](https://arxiv.org/abs/2407.11075)
- [Critch and Tsimerman, *A Taxonomy of Omnicidal Futures Involving Artificial Intelligence*](https://arxiv.org/abs/2507.09369)
- [Jaffe and Liu, *A Mathematical Picture Language Program*](https://doi.org/10.1073/pnas.1710707114)
- [Bourgade and Huang, *Loop Equations Characterize Random Matrix Statistics*](https://arxiv.org/abs/2607.07617)
- [Tagore, *The Fugitive*, section 26 of *The Fugitive-III*](https://www.gutenberg.org/ebooks/7971)
- [Gessler et al., *OvercookedV2: Rethinking Overcooked for Zero-Shot Coordination*](https://arxiv.org/abs/2503.17821)
- [Kong, Ram, and Yu, *AlphaZero in Sparsely Rewarded Games: Limits and Auxiliary Supervision*](https://arxiv.org/abs/2607.08984)
- [Bona-Pellissier et al., *PIKS: Universal Physics-Informed Kernel Methods*](https://arxiv.org/abs/2607.27062)
- [Li and Xia, *A counterexample to the zero-mass conjecture*](https://arxiv.org/abs/2607.26549)

## Authorship and assistance

The research note is co-authored by Ravi Andrew Bajaj and Alexander Burns.
Ravi's verified contact address is `rbajaj5@jh.edu`; no address is published
for Alexander because one has not been verified. OpenAI Codex provided
computational and editorial assistance and is not an author.
