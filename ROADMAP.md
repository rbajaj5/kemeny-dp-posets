# Research roadmap

## Immediate

- Compare the exact empirical cover radius formally with the ICML 2023
  breakdown function at attack amplitude `delta -> 0+`.
- Replace factorial enumeration with an ILP or fixed-parameter oracle for score
  gaps and the minimum gap-to-distance ratio.
- Prove utility bounds for pairwise-vector smooth perturbation followed by a
  transitive ranking projection.

## Sample-and-aggregate

- Implement two-voter exact block Kemeny and approximate larger-block
  estimators.
- Implement the Nissim-Raskhodnikova-Smith center-of-attention on Kendall
  space.
- Identify distributional conditions under which block rankings concentrate
  around the full Kemeny optimum.
- Compare against the 2022 and 2026 worst-case DP algorithms.

## Geometry

- Test sparse JL embeddings of pairwise ranking vectors.
- Quantify when Euclidean distortion controls Kendall utility.
- Study whether low-dimensional tournament structure permits efficient
  transitive postprocessing.

## Formal verification

- Port the uniqueness-radius proposition to Lean.
- Reuse the public Kemeny hardness formalization where definitions align.

