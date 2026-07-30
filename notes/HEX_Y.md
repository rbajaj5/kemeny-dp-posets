# Hex/Y Majority Reduction, Hasse Geometry, and Sensitivity

## Status

| Item | Status |
|---|---|
| Every complete two-color triangular board has exactly one Y winner | **KNOWN** |
| Three-cell majority reduction preserves that winner | **KNOWN; IMPLEMENTED** |
| Boolean-lattice cover model for one-cell recoloring | **STANDARD; FORMALIZED HERE** |
| Exact binary-winner smooth-sensitivity formula | **PROVED; GENERAL BOOLEAN-FUNCTION SPECIALIZATION** |
| Exhaustive checks through side 6 | **COMPUTATIONAL** |
| Pivotality and biased-color simulations | **COMPUTATIONAL** |

No novelty is claimed for the Y theorem or its reduction. The source is
Karlin and Peres, *Game Theory, Alive*, together with the fuller proof supplied
for this project.

## 1. Board and winner

Write

```text
T_n = {(q,r): q >= 0, r >= 0, q+r < n}.
```

Two cells are adjacent when their axial-coordinate difference is one of

```text
(1,0), (-1,0), (0,1), (0,-1), (1,-1), (-1,1).
```

The sides are `q=0`, `r=0`, and `q+r=n-1`. A color has a Y when one of its
connected components meets all three sides.

Represent a coloring by the subset `B` of blue cells. The set of all colorings
is the Boolean lattice `2^(T_n)`. Its directed covers are

```text
B < B union {v},
```

and its undirected Hasse graph joins exactly the colorings differing at one
cell. Consequently its graph distance is Hamming distance
`|B symmetric_difference B'|`. This is the natural substitution-adjacency
model for a private-data interpretation of cell colors.

## 2. Majority reduction

For each output cell `(q,r)` in `T_(n-1)`, define its color to be the majority
of the three input cells

```text
(q,r), (q+1,r), (q,r+1).
```

These input cells are pairwise adjacent. This coordinate choice is a rotation
of the book's arrow-shaped construction.

The known Y-game argument proves that a monochromatic Y exists before the
reduction if and only if one of the same color exists after it. In one
direction, paths in the original Y map to overlapping majority triangles.
In the reverse direction, a path of overlapping majority-color triangles can
be lifted: a majority triangle supplies two connected cells of that color,
and two consecutive triangles can be joined through their intersection or
through the connected cells in their symmetric difference. Repeating the
reduction leaves one cell, whose color is therefore the unique winner.

The executable model checks both colors separately; it does not assume the
theorem when testing the reduction.

## 3. Exact sensitivity on the coloring Hasse graph

Let `w(B)` be the binary winner and define the outcome radius

```text
R(B) = min {|B symmetric_difference B'| : w(B') != w(B)}.
```

Because the winner is total, `R(B) >= 1`. The one-step local sensitivity of
the numeric query `w` is either zero or one. Let `Pi` be the set of pivotal
colorings, those with local sensitivity one.

**Proposition.** For every coloring,

```text
distance(B, Pi) = R(B) - 1.
```

**Proof.** On a shortest Hamming path from `B` to the opposite outcome, the
penultimate vertex is pivotal, so the left side is at most `R(B)-1`. Conversely,
if a pivotal coloring is at distance `d`, one more edge reaches the opposite
outcome, so `R(B) <= d+1`. Thus `d >= R(B)-1`. Both inequalities are exact.

It follows directly from the definition that the exact beta-smooth
sensitivity of this nonconstant binary query is

```text
SS_beta(B) = exp(-beta * max(R(B)-1, 0)).
```

This mirrors the repository's Kemeny uniqueness-radius bound, but the logical
status is different: here the formula is exact because local sensitivity is
binary. It is a general fact about nonconstant total Boolean functions on a
Hamming graph, not a Hex-specific novelty claim.

Releasing the exact deterministic winner is not differentially private at a
pivotal cover. The formula is a sensitivity calculation, not a complete
privacy mechanism; any release still needs a valid noise distribution,
calibration theorem, and output interpretation.

## 4. Results

Full enumeration produced no unique-winner or reduction-invariance failures:

| Side | Cells | Colorings | Blue wins | Yellow wins | Failures |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 2 | 1 | 1 | 0 |
| 2 | 3 | 8 | 4 | 4 | 0 |
| 3 | 6 | 64 | 32 | 32 | 0 |
| 4 | 10 | 1,024 | 512 | 512 | 0 |
| 5 | 15 | 32,768 | 16,384 | 16,384 | 0 |
| 6 | 21 | 2,097,152 | 1,048,576 | 1,048,576 | 0 |

For uniform random colorings, the exact probability that flipping a uniformly
random cell changes the winner was:

| Side | Pivotal flip probability |
|---:|---:|
| 1 | 1.000000 |
| 2 | 0.500000 |
| 3 | 0.312500 |
| 4 | 0.221094 |
| 5 | 0.168262 |

The exact outcome-radius histograms were:

| Side | Histogram `radius: colorings` |
|---:|---|
| 1 | `1: 2` |
| 2 | `1: 6, 2: 2` |
| 3 | `1: 50, 2: 12, 3: 2` |
| 4 | `1: 806, 2: 196, 3: 20, 4: 2` |
| 5 | `1: 25,892, 2: 6,230, 3: 614, 4: 30, 5: 2` |

At color probability `p=0.5`, complement symmetry gives an exact blue-win
probability of one half. The 2,000-trial estimates were 0.4965, 0.4915,
0.5195, and 0.4905 at sides 8, 12, 16, and 24. At `p=0.4`, the observed
blue-win rate fell from 0.1795 to 0.0355 over the same sizes; at `p=0.6`, it
rose from 0.8045 to 0.9545. This suggests finite-size threshold sharpening,
but is not an asymptotic percolation theorem.

Each Monte Carlo row in `results/hex_y.json` records the successes, trial
count, standard error, Wilson 95% interval, and the same plug-in Berry-Esseen
shape diagnostic used by the market experiments.

## 5. What “three” does and does not connect

Both constructions use three inputs, but in different senses:

- Y reduction applies a fixed constant-size majority gate to three binary
  cell colors.
- Peters's theorem concerns a Kemeny median of three arbitrary permutations,
  with a candidate set whose size grows.

Therefore the Y reduction does not imply or inherit three-voter Kemeny
hardness. The useful commonality is structural: both invite a cover-radius
analysis of how a three-input aggregation outcome changes under one atomic
input change.

The majority map also need not preserve Hasse distance. One input cell can
belong to as many as three reduction triangles, so a single cover step can
alter several cells on the next level. Winner preservation is a topological
invariant, not a nonexpansiveness statement.

The complete reduction is an exact monotone majority circuit of depth `n-1`.
At level `k`, it evaluates `k(k+1)/2` gates, so its total size is
`choose(n+1,3)`. The
[`KAN/Hex assessment`](KAN_HEX_ASSESSMENT.md) explains why this exact
discontinuous circuit is a better present model than an unbenchmarked
B-spline surrogate.

## 6. Computation

```bash
python -m unittest discover -s tests -v
python scripts/run_hex_y.py --exhaustive-max 6 --trials 2000
```

The side-6 exhaustive run finished in about 33 seconds on the available CPU.
An NVIDIA GPU was detected, but the workload did not justify installing or
adding a GPU dependency. Larger sweeps should first use bit-parallel batching;
GPU acceleration becomes relevant only after that baseline is measured. The
script also compares direct connectivity with the exact majority circuit on
identical boards using repeated median timings.

After caching all board geometries, the circuit and connectivity algorithms
had zero mismatches. The circuit/direct median-time ratio increased from 4.47
at side 8 to 15.17 at side 24. These timings are machine-dependent; they show
that the reduction is presently more useful as a proof architecture than as a
throughput optimization.

The generated side-two
[`artifacts/hex_y_hasse_n2.svg`](../artifacts/hex_y_hasse_n2.svg) shows the
entire coloring lattice. Its purple cover edges are precisely the winner-
changing one-cell recolorings.

## Sources

- Anna R. Karlin and Yuval Peres,
  [*Game Theory, Alive*](https://math.uchicago.edu/~shmuel/Modeling/Peres%20and%20Wilson%2C%20Game%20Theory%20Alive.pdf),
  section on Hex and Y.
- The project-specific fuller path-lifting proof supplied with the requested
  simulation task.
