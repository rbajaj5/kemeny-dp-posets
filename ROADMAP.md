# Research roadmap

## Immediate

- Compare the exact empirical cover radius formally with the ICML 2023
  breakdown function at attack amplitude `delta -> 0+`.
- Compare subset DP with an ILP or fixed-parameter oracle.
- Prove utility bounds for pairwise-vector smooth perturbation followed by a
  transitive ranking projection.

## Recently completed

- Extended subset DP with exact distance-stratified score gaps, a second-best
  witness, the uniqueness radius, and a constructive repeated-ballot attack.
- Exhaustively checked those certificates against factorial enumeration for
  all 2,600 four-candidate, three-voter profiles.
- Exhausted 3,002 three-candidate profiles of sizes one through eight and
  found 84 cases where a larger-gap, more distant competitor destabilizes
  faster than every second-best competitor.

## Sample-and-aggregate

- Implement two-voter exact block Kemeny and approximate larger-block
  estimators.
- Implement the Nissim-Raskhodnikova-Smith center-of-attention on Kendall
  space.
- Identify distributional conditions under which block rankings concentrate
  around the full Kemeny optimum.
- Compare against the 2022 and 2026 worst-case DP algorithms.

## Geometry

- Extend the dense JL experiment to sparse transforms and neutral tie-breaking.
- Quantify when Euclidean distortion controls Kendall utility.
- Study whether low-dimensional tournament structure permits efficient
  transitive postprocessing.

## Formal verification

- Port the uniqueness-radius proposition to Lean.
- Reuse the public Kemeny hardness formalization where definitions align.

## Law-characterizing hierarchies

- Quantify how many upper-set queries are needed to identify restricted
  families of random-profile laws, rather than releasing the full zeta table.
- Study noisy Möbius inversion and the amplification of query error.
- If any hierarchy is released from private profile data, derive its
  sensitivity and privacy mechanism separately; exact invertibility is a
  disclosure warning, not a privacy guarantee.
- Do not treat finite residual checks as a characterization without an
  admissible-class and uniqueness theorem.

## Hex/Y sensitivity

- Derive or bound the outcome-radius distribution beyond side five without
  enumerating the full coloring hypercube.
- Compare exact pivotality with rigorous influence and sharp-threshold bounds
  for monotone Boolean functions.
- Quantify the expansion of Hamming perturbations under repeated overlapping
  majority reduction.
- Add bit-parallel CPU and then GPU batches only when profiling shows that
  exhaustive or Monte Carlo throughput is the bottleneck.
- If learned winner surrogates are tested, compare KAN, MLP/tree, and the exact
  circuit under matched parameter and latency budgets, multiple seeds, and
  radius-stratified held-out sizes.

## Market design

- Compute Carroll's robust guarantee proposal by proposal on a finite
  price/deal menu.
- Characterize domains where those robust-guarantee rankings are
  single-peaked or otherwise structured.
- Specify strategic reporting and equilibrium selection in a genuine
  multiple-proposal mechanism.
- Test randomized, pro-rata, and batch queue-allocation domains without
  confusing synthetic ranking criteria with actual exchange rules.
