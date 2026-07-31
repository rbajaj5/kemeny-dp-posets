# Result and Provenance Ledger

This ledger records what the repository claims and what it does not claim.
Version labels identify the first public repository increment containing each
item. Git history supplies the exact timestamps.

| ID | Statement or artifact | Status | First version | Closest comparison |
|---|---|---|---|---|
| P1 | Profile multiset covers equal unbounded-DP add/remove adjacency; Hasse distance is `L1`. | PROVED | 0.1.0 | Standard multiset-poset and DP adjacency definitions. |
| P2 | Exact local-sensitivity formulas for scalar optimal Kemeny cost. | PROVED | 0.1.0 | Nissim-Raskhodnikova-Smith smooth sensitivity; private rank aggregation literature. |
| P3 | Exact distance to loss of a unique Kemeny optimum is the minimum ceiling of gap divided by Kendall distance. | PROVED; NOVELTY UNCONFIRMED | 0.1.0 | Goibert et al. breakdown functions for ranking medians. |
| P4 | `D exp(-beta max(R-1,0))` is a smooth upper bound for deterministic Kemeny selection. | PROVED; MECHANISM INCOMPLETE | 0.1.0 | General smooth-bound framework of Nissim et al. |
| P5 | A unique non-unanimous `n`-record metric median has radius at most `n-2`; at three records the radius is one, while unanimity gives radius three. | PROVED; NOVELTY UNCONFIRMED | 0.3.0 | General metric-median robustness and breakdown literature. |
| P6 | Exact Kemeny composition of price, time, and size priority rankings is NP-hard. | PROVED BY ENCODING | 0.3.0 | Peters's three-voter hardness theorem. |
| P7 | For a nonconstant total binary query on a Hamming graph, exact smooth sensitivity is `exp(-beta max(R-1,0))`, where `R` is distance to the opposite output. | PROVED; GENERAL BOOLEAN-FUNCTION SPECIALIZATION | 0.3.0 | Direct specialization of Nissim-Raskhodnikova-Smith smooth sensitivity. |
| P8 | The recursive Y reduction is a monotone ternary-majority circuit of depth `n-1` and size `choose(n+1,3)`. | PROVED COROLLARY OF KNOWN REDUCTION | 0.3.0 | Karlin-Peres majority reduction. |
| P9 | The full upper-set probability hierarchy on a bounded finite profile poset uniquely determines the random-profile law. | PROVED; STANDARD SPECIALIZATION | 0.4.0 | Finite-poset zeta transform and Möbius inversion. |
| P10 | A subset DP stratified by Kendall distance computes the exact second-best score, uniqueness radius, and a constructive destabilizing competitor in `O(m D 2^m)` time. | PROVED; NOVELTY UNCONFIRMED | 0.5.0 | Exact and parameterized Kemeny dynamic programming. |
| P11 | Under standard half-`L1` TV, zero-plus Kemeny breakdown is an exact finite mass-transport problem, is at least `mu/2`, and equals `mu/2` under the sufficient condition `mu <= 2p(sigma)`; then `R=ceil(2n b_TV)`. | PROVED SPECIALIZATION; NOVELTY UNCONFIRMED | 0.6.0 | Goibert et al. Theorems 3.1-3.2, with an explicit factor-two normalization audit. |
| P12 | An input-restricted center containing a target number of metric points has optimum radius between one and two times the unrestricted optimum; the factor two is sharp in Kendall space. | PROVED; STANDARD METRIC LEMMA | 0.7.0 | Nissim-Raskhodnikova-Smith center-of-attention construction. |
| P13 | Returning either input ballot is an exact two-ballot Kemeny solution by triangle inequality. | PROVED; STANDARD METRIC FACT | 0.7.0 | Metric 1-median and Kemeny aggregation basics. |
| P14 | In the two-convention ungrounded binary protocol game, paired accuracy is one, crossed accuracy is zero, every fixed decoder averages one half, and one labeled interaction identifies the convention. | PROVED FINITE TOY MODEL; NO KEMENY/DP CLAIM | 0.8.0 | OvercookedV2 grounded communication and test-time protocol motivation. |
| K1 | The three-cell majority reduction preserves the unique Y-game winner. | KNOWN; IMPLEMENTED | 0.3.0 | Karlin and Peres, *Game Theory, Alive*. |
| K2 | In finite Chomp, Sprague-Grundy recursion labels a winning move exactly by transition to Grundy zero. | KNOWN; IMPLEMENTED | 0.8.0 | Standard Sprague-Grundy theory; Kong-Ram-Yu oracle evaluation. |
| K3 | In Li-Xia's finite stages, `degree(H_j)=4^j`, scale `2^-j`, normalized two-dimensional Monge-Ampere mass one, and Lelong number `2^-j`. | KNOWN SOURCE FORMULAS; IMPLEMENTED | 0.8.1 | Li-Xia Proposition 3.2. |
| C1 | Exact atlases through five candidates and three voters. | COMPUTATIONAL | 0.3.0 | Exhaustive verification of P5. |
| C2 | JL preservation, sample-and-center, and exponential-mechanism experiments. | COMPUTATIONAL | 0.3.0 | Dwork survey, NRS07, and Blocki et al. |
| C3 | Structured versus unrestricted synthetic market-priority experiments. | COMPUTATIONAL; NO ECONOMIC EQUILIBRIUM CLAIM | 0.3.0 | Carroll's multiple-proposal open direction; market-design literature. |
| C4 | Unique Y winner and majority-reduction invariance on every triangular board through side six; exact radii through side five. | COMPUTATIONAL | 0.3.0 | Finite exhaustive check of K1 and P7. |
| C5 | Repeated same-input timing comparison of direct Y connectivity and the exact majority circuit. | COMPUTATIONAL; MACHINE-DEPENDENT | 0.3.0 | Hou et al. fair-evaluation recommendations. |
| C6 | Exact rational-law reconstruction on all 84 profiles through three ballots; a pair of distinct three-voter laws with equal first moments is separated by the full hierarchy. | EXACT COMPUTATIONAL | 0.4.0 | Finite check of P9 and low-order non-identification. |
| C7 | Distance-stratified certificates match factorial enumeration on all 2,600 four-candidate, three-voter profiles; among 3,002 three-candidate profiles through size eight, 84 have a larger-gap competitor that destabilizes faster than every second-best competitor. | EXACT COMPUTATIONAL | 0.5.0 | Finite audit of P3 and P10. |
| C8 | Exact TV computations on all 2,232 uniquely optimized three-candidate profiles through size eight have zero cover-identity or half-margin-bound failures; a four-candidate profile witnesses strictness above `mu/2`. | EXACT COMPUTATIONAL | 0.6.0 | Finite audit of P11. |
| C9 | 8,581 center certificates have zero factor-two or minimizer-equivariance failures; 612 ordered two-ballot profiles have zero optimum failures; Borda's largest observed ratio on 3,002 profiles is `3/2`. | EXACT COMPUTATIONAL; NO PRIVACY CLAIM | 0.7.0 | Finite audit of P12-P13 and the known Borda approximation. |
| C10 | The ten-button grounded game has exact brittle self/cross-play accuracies one and one half; complete button coverage restores one; both binary conventions, all four fixed decoders, and all feedback cases verify P14. | EXACT COMPUTATIONAL; NO RL CLAIM | 0.8.0 | OvercookedV2 Button Game and benchmark diagnosis. |
| C11 | Exact Chomp evaluation covers 923 states in a six-by-six box, including 875 labeled winning states, plus 25 full-game starts; the oracle is exact everywhere and the largest-bite negative control matches `2/175` sampled labeled states. | EXACT COMPUTATIONAL; NO ALPHAZERO CLAIM | 0.8.0 | Kong-Ram-Yu trace and sampled-state oracle metrics. |
| C12 | Exact rational arithmetic verifies K3 through stage 20: mass remains one, Lelong numbers strictly decrease, and the mass-to-Lelong ratio reaches `2^20`. | EXACT ARITHMETIC AUDIT; NO ANALYTIC-LIMIT CLAIM | 0.8.1 | Finite-stage mechanism in Li-Xia. |
| A1 | Kemeny aggregation could combine stakeholder rankings of high-level risk-mitigation priorities. | OPEN APPLICATION; NO PROBABILITY OR POLICY CLAIM | 0.3.0 | Critch-Tsimerman scenario taxonomy; social-choice caveats. |
| A2 | Language/reality/simulation ledger for every cross-domain diagram. | METHODOLOGICAL AUDIT; NO NEW DOMAIN THEOREM | 0.3.0 | Jaffe-Liu picture-language program. |
| A3 | Loop-equation proof audit separating identities, error control, and branch selection; no random-matrix theorem is transported to Kemeny or privacy. | METHODOLOGICAL AUDIT | 0.4.0 | Bourgade-Huang characterization theorems. |
| A4 | Non-instrumental exploration is permitted, but certification still requires correct sources, defined maps, evidence, and status labels. | RESEARCH POLICY; NO MATHEMATICAL CLAIM | 0.4.1 | Tagore, *The Fugitive-III*, section 26. |
| A5 | State coverage, convention compatibility, oracle consistency, and aggregate outcome are reported as distinct benchmark properties. | METHODOLOGICAL AUDIT | 0.8.0 | Gessler et al.; Kong, Ram, and Yu. |
| A6 | Value fit and structural residual should be measured separately, but PIKS's RKHS/PDE consistency theorem does not transfer to finite ranking transitivity. | METHODOLOGICAL AUDIT; NO TRANSPORTED THEOREM | 0.8.0 | Bona-Pellissier et al. |
| A7 | A one-sided lower bound from a coarse local invariant is not treated as reversible without additional structure; the Li-Xia theorem is recorded without transport to Kemeny or privacy. | METHODOLOGICAL AUDIT | 0.8.1 | Li-Xia zero-mass counterexample; strictness in P11. |

## Corrections

- Version 0.2.0 corrected the one-dimensional NRS Laplace calibration from
  `log(1/delta)` to `log(2/delta)`.
- Version 0.7.0 corrected block validation so invalid ballots cannot escape
  checking by landing in an incomplete discarded block.
- Version 0.8.0 tightened oracle-flag validation so integer `1` is not
  silently accepted as a Boolean annotation.

## Authorship

The research note is authored by Ravi Andrew Bajaj and Alexander Burns.
OpenAI Codex supplied computational and editorial assistance and is not an
author.
