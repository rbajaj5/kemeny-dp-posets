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

## What runs

- exact Kemeny enumeration for small candidate sets;
- exact subset-DP Kemeny optimization in `O(m^2 2^m)` time;
- cover-graph parents, children, distances, and finite Hasse diagrams;
- exact local sensitivity of the optimal Kemeny score;
- exact smooth sensitivity of that scalar score by certified shell search;
- the uniqueness-radius formula plus exhaustive verification;
- a global-sensitivity exponential-mechanism baseline;
- the one-dimensional Nissim-Raskhodnikova-Smith smooth-sensitivity release
  for the optimal score;
- exact block Kemeny outputs and the efficient NRS center-of-attention in
  Kendall space as a non-private sample-and-aggregate utility prototype;
- three-voter JL, private-learning, and market-priority experiments;
- exact triangular Y-game connectivity and majority reduction;
- exact small-board pivotality, outcome radii, and binary smooth sensitivity;
- exact majority-circuit size and repeated connectivity-versus-circuit timings;
- reproducible CSV/JSON experiments and SVG Hasse diagrams for both profile
  and coloring cover relations.

## Quick start

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/run_experiments.py
python scripts/run_three_voter_applications.py
python scripts/run_market_microstructure.py
python scripts/run_hex_y.py --exhaustive-max 6
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
ranking medians by Goibert et al. (ICML 2023). The exact integer cover-distance
formula here should be compared carefully with that continuous contamination
model before any novelty claim is made.

## Sources

- [Dwork, *Differential Privacy: A Survey of Results* (2008)](https://www.microsoft.com/en-us/research/wp-content/uploads/2008/04/dwork_tamc.pdf)
- [Nissim, Raskhodnikova, and Smith, *Smooth Sensitivity and Sampling in Private Data Analysis* (2007)](https://people.csail.mit.edu/asmith/PS/stoc321-nissim.pdf)
- [Hay, Elagina, and Miklau, *Differentially Private Rank Aggregation* (2017)](https://people.cs.umass.edu/~miklau/assets/pubs/dp/hay17differentially.pdf)
- [Alabi et al., *Private Rank Aggregation in Central and Local Models* (2022)](https://arxiv.org/abs/2112.14652)
- [Hillebrand et al., *Improved Differentially Private Algorithms for Rank Aggregation* (2026)](https://arxiv.org/abs/2511.11319)
- [Peters, *Kemeny Rank Aggregation is NP-Hard for Three Voters* (2026)](https://arxiv.org/abs/2607.25540)
- [Carroll, *Informationally Robust Trade and Limits to Contagion* (2016)](http://individual.utoronto.ca/carroll/robustlemons.pdf)
- [Karlin and Peres, *Game Theory, Alive*](https://math.uchicago.edu/~shmuel/Modeling/Peres%20and%20Wilson%2C%20Game%20Theory%20Alive.pdf)
- [Hou et al., *Kolmogorov-Arnold Networks: A Critical Assessment*](https://arxiv.org/abs/2407.11075)
- [Critch and Tsimerman, *A Taxonomy of Omnicidal Futures Involving Artificial Intelligence*](https://arxiv.org/abs/2507.09369)
- [Jaffe and Liu, *A Mathematical Picture Language Program*](https://doi.org/10.1073/pnas.1710707114)

## Authorship and assistance

The research note is co-authored by Ravi Andrew Bajaj and Alexander Burns.
Ravi's verified contact address is `rbajaj5@jh.edu`; no address is published
for Alexander because one has not been verified. OpenAI Codex provided
computational and editorial assistance and is not an author.
