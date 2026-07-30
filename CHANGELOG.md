# Changelog

## 0.7.0 - 2026-07-30

- Added exact center-of-attention certificates, including the full minimizing
  input-center set and an unrestricted small-instance oracle.
- Proved and exhaustively checked the sharp factor-two input-center
  approximation in Kendall space.
- Added a linear-time exact two-ballot Kemeny shortcut and a polynomial-time
  Borda block estimator.
- Checked 8,581 center certificates, 612 ordered two-ballot profiles, and
  3,002 Borda profiles; recorded deterministic lexicographic non-neutrality
  instead of hiding it.
- Fixed validation so an invalid ballot in a discarded incomplete block is
  rejected before shuffling.
- Regenerated the sample-and-center experiment under the explicit new
  two-ballot selector.

## 0.6.0 - 2026-07-30

- Added an exact rational mass-transport computation of zero-plus Kemeny
  breakdown under standard half-`L1` total variation.
- Proved `b_TV >= mu/2`, the sufficient equality condition
  `mu <= 2p(sigma)`, and the conditional bridge
  `R=ceil(2n b_TV)`.
- Audited Goibert et al. (ICML 2023) and documented the factor-two mismatch
  between Equation (4) and Appendix C.2 without extending the correction claim
  beyond the strict-ranking zero-plus setting.
- Checked all 2,232 uniquely optimized three-candidate profiles through eight
  ballots and added a four-candidate example where `b_TV > mu/2`.
- Corrected the ICML paper's author names in the literature map.

## 0.5.0 - 2026-07-30

- Added an exact subset DP stratified by Kendall distance from the selected
  optimum.
- Added second-best score, exact uniqueness-radius, and constructive
  repeated-ballot witnesses without factorial enumeration.
- Proved the distance-stratified recurrence and its `O(m D 2^m)` running-time
  bound, with novelty explicitly unconfirmed.
- Matched the certificates against factorial enumeration on every one of the
  2,600 four-candidate, three-voter profiles.
- Exhausted 3,002 three-candidate profiles through size eight and recorded 84
  strict examples where a larger-gap, more distant competitor destabilizes
  faster than every second-best competitor.

## 0.4.1 - 2026-07-30

- Added a source-checked research-policy note for Tagore's untitled section 26
  of *The Fugitive-III*, often circulated as "A Wrong Man in Workers'
  Paradise."
- Corrected the supplied transcript's bibliographic ambiguity: the underlying
  English work is in *The Fugitive* (1921), not *Gitanjali*.
- Distinguished non-instrumental exploration from claim certification and
  added five concrete criteria for useful automated research increments.
- Updated the quiet-public-program core to include the exact Boolean, Y-circuit,
  and finite-poset hierarchy results.

## 0.4.0 - 2026-07-30

- Audited Bourgade and Huang's random-matrix characterization theorem using
  the full manuscript and supplied excerpts on Gronwall control, resolvent
  cancellation, exceptional events, and asymptotic branch selection.
- Added the exact upper-set probability hierarchy and finite-poset Möbius
  inversion for bounded random profiles.
- Reconstructed an exact rational law on all 84 profiles through three ballots
  with zero error.
- Added a three-voter example showing that first moments do not identify a
  profile law, while the full hierarchy separates the two laws.
- Kept the random-matrix beta parameter distinct from the smooth-sensitivity
  beta parameter and made no cross-domain theorem claim.

## 0.3.0 - 2026-07-30

- Proved the `n-2` radius bound for unique non-unanimous metric medians and
  the exact three-voter radius dichotomy.
- Exhausted all three-voter profiles through five candidates.
- Added exact exponential-mechanism distributions and exhaustive DP audits.
- Added pairwise sign embeddings and JL preservation experiments.
- Added an exact subset-DP Kemeny solver using `2^m` states.
- Added the price/time/size market-priority hardness encoding.
- Added structured single-peaked and unrestricted market experiments.
- Added finite-sample Bernoulli summaries and the public research policy.
- Added a triangular Hex/Y engine, the known majority reduction, and exhaustive
  certification through all 2,097,152 side-six colorings.
- Proved and tested the exact binary-winner smooth-sensitivity formula on the
  coloring Boolean lattice; added pivotality and biased-color simulations.
- Added a source-assessment boundary that uses the supplied TUFT manuscript
  only as a local-to-global heuristic.
- Derived the exact `choose(n+1,3)` majority-circuit size and added repeated
  same-input benchmarks against direct connectivity.
- Added a KAN/Hex assessment: no spline-model claim is made for a discrete
  combinatorial target without resource-controlled baselines.
- Added an AI-risk governance note separating scenario taxonomy, priority
  aggregation, empirical probability, and real-world deployment.
- Added a Jaffe-Liu picture-language transport audit for the Hasse, Hex, JL,
  market, topology, and governance simulations.

## 0.2.0 - 2026-07-29

- Added the co-authored formal research note.
- Added the center-of-attention sample-and-aggregate utility prototype.
- Corrected smooth-sensitivity calibration to
  `beta = epsilon / (2 log(2/delta))`.

## 0.1.0 - 2026-07-29

- Published the profile-poset implementation, exact sensitivity calculations,
  uniqueness-radius theorem, finite experiments, tests, and Hasse diagram.
