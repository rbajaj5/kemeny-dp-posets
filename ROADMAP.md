# Research roadmap

## Immediate

- Compare subset DP with an ILP or fixed-parameter oracle.
- Prove utility bounds for pairwise-vector smooth perturbation followed by a
  transitive ranking projection.

## Recently completed

- Implemented Li's binary-coin and independent-column spherical JL
  constructions and explicit sufficient-dimension calculator.
- Compared both constructions on all 7,140 five-candidate ranking pairs and
  separated fixed-vector, finite-family, argmin, and privacy claims.
- Audited the exact finite-stage scaling in Li-Xia's zero-mass construction
  through stage 20 and separated it from the analytic limiting theorem.
- Documented why the zero-mass and Bieberbach conjectures are distinct, and
  retained only the one-sided-implication proof discipline.
- Separated state coverage from convention incompatibility with exact grounded
  and ungrounded binary coordination games.
- Added exact oracle trace metrics and a memoized Chomp Grundy laboratory;
  exhausted 923 states in a six-by-six box and 25 full-game starts.
- Adopted separate reporting of empirical outcome, oracle consistency, and
  structural residual; documented why PIKS does not supply a Kemeny theorem.
- Proved the sharp factor-two input-center approximation, exposed the complete
  relabeling-equivariant minimizer set, and documented why lexicographic
  resolution is not neutral.
- Added an exact linear-time two-ballot Kemeny shortcut, a polynomial-time
  Borda block option, and validation of every ballot before shuffling.
- Exhausted 8,581 center certificates, 612 ordered two-ballot profiles, and
  3,002 Borda profiles with zero theorem-bound failures.
- Derived the exact zero-plus standard-TV breakdown by finite mass transport,
  proved `b_TV >= mu/2`, and identified the sufficient equality condition
  `mu <= 2p(sigma)`.
- Proved the factor-explicit bridge `R=ceil(2n b_TV)` under that condition and
  documented the normalization mismatch between Equation (4) and Appendix
  C.2 of Goibert et al. (ICML 2023).
- Exhausted all 2,232 uniquely optimized three-candidate profiles through
  eight ballots and recorded a strict four-candidate counterexample to
  universal half-margin equality.
- Extended subset DP with exact distance-stratified score gaps, a second-best
  witness, the uniqueness radius, and a constructive repeated-ballot attack.
- Exhaustively checked those certificates against factorial enumeration for
  all 2,600 four-candidate, three-voter profiles.
- Exhausted 3,002 three-candidate profiles of sizes one through eight and
  found 84 cases where a larger-gap, more distant competitor destabilizes
  faster than every second-best competitor.

## Sample-and-aggregate

- Identify distributional conditions under which block rankings concentrate
  around the full Kemeny optimum.
- Compare against the 2022 and 2026 worst-case DP algorithms.
- Report exact-optimum agreement, score regret, failure shells, relabeling,
  and independently sampled profiles rather than one aggregate utility alone.

## Benchmark validity

- Test state augmentation before labeling a cross-play gap as coordination.
- Randomize or symmetrize arbitrary candidate-label and tie conventions, then
  test cross-convention behavior explicitly.
- For learned or heuristic game policies, pair outcome rates with exact-oracle
  match, longest consistent chain, first failure, and sampled-state coverage.
- Treat auxiliary structural penalties as new algorithms requiring their own
  approximation, neutrality, and privacy analyses.

## Geometry

- Extend the dense binary and spherical JL audit to sparse transforms and
  neutral tie-breaking.
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
