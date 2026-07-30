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

The formal write-up is [`paper/PAPER.md`](paper/PAPER.md). Supporting proof
notes, literature positioning, limits, and proposed research directions are in
[`notes/RESULTS.md`](notes/RESULTS.md). This is a research scaffold, not a
peer-reviewed novelty claim.

## What runs

- exact Kemeny enumeration for small candidate sets;
- cover-graph parents, children, distances, and finite Hasse diagrams;
- exact local sensitivity of the optimal Kemeny score;
- exact smooth sensitivity of that scalar score by certified shell search;
- the uniqueness-radius formula plus exhaustive verification;
- a global-sensitivity exponential-mechanism baseline;
- the one-dimensional Nissim-Raskhodnikova-Smith smooth-sensitivity release
  for the optimal score;
- exact block Kemeny outputs and the efficient NRS center-of-attention in
  Kendall space as a non-private sample-and-aggregate utility prototype;
- reproducible CSV/JSON experiments and an SVG Hasse diagram.

## Quick start

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/run_experiments.py
python scripts/generate_hasse.py
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

## Authorship and assistance

The research note is co-authored by Ravi Andrew Bajaj and Alexander Burns.
Ravi's verified contact address is `rbajaj5@jh.edu`; no address is published
for Alexander because one has not been verified. OpenAI Codex provided
computational and editorial assistance and is not an author.
