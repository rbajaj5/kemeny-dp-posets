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
| K1 | The three-cell majority reduction preserves the unique Y-game winner. | KNOWN; IMPLEMENTED | 0.3.0 | Karlin and Peres, *Game Theory, Alive*. |
| C1 | Exact atlases through five candidates and three voters. | COMPUTATIONAL | 0.3.0 | Exhaustive verification of P5. |
| C2 | JL preservation, sample-and-center, and exponential-mechanism experiments. | COMPUTATIONAL | 0.3.0 | Dwork survey, NRS07, and Blocki et al. |
| C3 | Structured versus unrestricted synthetic market-priority experiments. | COMPUTATIONAL; NO ECONOMIC EQUILIBRIUM CLAIM | 0.3.0 | Carroll's multiple-proposal open direction; market-design literature. |
| C4 | Unique Y winner and majority-reduction invariance on every triangular board through side six; exact radii through side five. | COMPUTATIONAL | 0.3.0 | Finite exhaustive check of K1 and P7. |
| C5 | Repeated same-input timing comparison of direct Y connectivity and the exact majority circuit. | COMPUTATIONAL; MACHINE-DEPENDENT | 0.3.0 | Hou et al. fair-evaluation recommendations. |
| C6 | Exact rational-law reconstruction on all 84 profiles through three ballots; a pair of distinct three-voter laws with equal first moments is separated by the full hierarchy. | EXACT COMPUTATIONAL | 0.4.0 | Finite check of P9 and low-order non-identification. |
| C7 | Distance-stratified certificates match factorial enumeration on all 2,600 four-candidate, three-voter profiles; among 3,002 three-candidate profiles through size eight, 84 have a larger-gap competitor that destabilizes faster than every second-best competitor. | EXACT COMPUTATIONAL | 0.5.0 | Finite audit of P3 and P10. |
| A1 | Kemeny aggregation could combine stakeholder rankings of high-level risk-mitigation priorities. | OPEN APPLICATION; NO PROBABILITY OR POLICY CLAIM | 0.3.0 | Critch-Tsimerman scenario taxonomy; social-choice caveats. |
| A2 | Language/reality/simulation ledger for every cross-domain diagram. | METHODOLOGICAL AUDIT; NO NEW DOMAIN THEOREM | 0.3.0 | Jaffe-Liu picture-language program. |
| A3 | Loop-equation proof audit separating identities, error control, and branch selection; no random-matrix theorem is transported to Kemeny or privacy. | METHODOLOGICAL AUDIT | 0.4.0 | Bourgade-Huang characterization theorems. |
| A4 | Non-instrumental exploration is permitted, but certification still requires correct sources, defined maps, evidence, and status labels. | RESEARCH POLICY; NO MATHEMATICAL CLAIM | 0.4.1 | Tagore, *The Fugitive-III*, section 26. |

## Corrections

- Version 0.2.0 corrected the one-dimensional NRS Laplace calibration from
  `log(1/delta)` to `log(2/delta)`.

## Authorship

The research note is authored by Ravi Andrew Bajaj and Alexander Burns.
OpenAI Codex supplied computational and editorial assistance and is not an
author.
