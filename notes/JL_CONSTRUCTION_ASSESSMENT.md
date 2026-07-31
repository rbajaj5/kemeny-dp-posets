# Independent-Column JL Constructions on Ranking Geometry

## Scope and status

Yingru Li's *Simple, unified analysis of Johnson-Lindenstrauss with
applications* (arXiv:2402.10232v4) gives one proof framework for several
independent-column random projections. Proposition 8 includes both:

- binary-coin columns, equivalently a dense Rademacher matrix scaled by
  `1/sqrt(output_dimension)`; and
- columns drawn independently and uniformly from the output unit sphere.

This repository implements both constructions and compares them on the exact
pairwise-sign geometry of all rankings on five candidates. Li's proposition is
a **KNOWN SOURCE THEOREM**. The ranking comparison is **MONTE CARLO**. No
novelty, differential-privacy, or projected-Kemeny theorem is claimed.

## 1. The source result used

For either construction and one fixed vector `x`, Proposition 8 supplies the
sufficient condition

```text
output_dimension >= 64 epsilon^-2 log(2/delta)
```

for squared-norm distortion at most `epsilon` with probability at least
`1-delta`, in the source's parameter range. Proposition 24 applies the same
fixed-vector estimate to a finite family by a union bound:

```text
output_dimension >=
    64 epsilon^-2 log(2 * finite_set_size / delta).
```

The spherical implementation normalizes independent isotropic Gaussian
vectors. Rotational invariance makes each normalized vector uniform on the
sphere. Coordinates inside a column are dependent; the columns themselves
are independent. That distinction is the point of the source's
independent-column analysis.

The source develops a high-dimensional Hanson-Wright inequality to handle
these dependent coordinates. The repository uses the resulting proposition
but does not independently verify the full concentration proof or endorse its
novelty claim.

## 2. Exact ranking map

For a ranking `sigma`, let `v_sigma` record the sign of every unordered
candidate comparison. With

```text
D = choose(candidate_count, 2),
```

the map is exact:

```text
||v_sigma - v_tau||_2^2 = 4 Kendall(sigma, tau).
```

For five candidates, `D=10`, there are `120` rankings and `7,140` unordered
ranking pairs. Applying Li's explicit bounds at `epsilon=0.4` and
`delta=0.05` gives:

| Guarantee target | Sufficient output dimension | Original dimension |
|---|---:|---:|
| One fixed difference vector | 1,476 | 10 |
| All 7,140 ranking differences by a union bound | 5,025 | 10 |

These sufficient bounds are deliberately conservative and do not certify
dimension reduction for this small complete ranking family. The identity map
in dimension 10 preserves the geometry exactly.

## 3. Matched finite experiment

`scripts/run_jl_construction_audit.py` generates both constructions with fixed
seeds. At each output dimension it measures all 7,140 pairs in 16 independent
projection trials and the identity-versus-reverse difference vector in 2,048
independent trials.

The table reports the mean fraction of ranking pairs whose squared-norm
distortion is at most `0.4`, followed in parentheses by the empirical failure
rate for the fixed vector.

| Output dimension | Binary coin | Spherical columns |
|---:|---:|---:|
| 2 | 0.329 (0.698) | 0.326 (0.673) |
| 8 | 0.659 (0.409) | 0.633 (0.389) |
| 16 | 0.827 (0.217) | 0.831 (0.243) |
| 32 | 0.938 (0.078) | 0.919 (0.092) |
| 64 | 0.993 (0.015) | 0.988 (0.013) |

Only one of the 16 binary-coin trials at dimension 64 preserved every pair
within `epsilon`; none of the spherical trials did. Dimensions above 10 are
included to show concentration, not as dimension reduction. The explicit
Proposition 8 tail bound is still capped at one throughout this tested range,
so these rows are empirical behavior rather than confirmations of a
nontrivial numerical upper bound. The small experiment also gives no basis
for claiming that either construction uniformly dominates the other.

## 4. What this does not prove

### Argmin preservation

Approximate preservation of all pairwise ranking distances is stronger than
necessary in some directions and insufficient by itself in another: a Kemeny
optimizer is selected by a score comparison. Preserving the selected ranking
requires a distortion error smaller than the relevant profile-level score
margin. The earlier three-voter experiment checks such margin certificates
and finds no certificate violations, but many tested profiles are outside the
certified regime.

### Privacy

Li's paper is a concentration result, not a differential-privacy mechanism.
The privacy theorem of Blocki, Blum, Datta, and Sheffet requires a separately
defined matrix adjacency relation and spectral hypotheses. Neither independent
columns nor a JL norm guarantee alone makes the output private. A ranking
mechanism would still need:

1. a precise neighboring-profile map into the projected object;
2. a privacy proof for that released object;
3. control of optimization and transitivity after projection; and
4. an end-to-end utility statement.

### Novelty

The code adds an independently reproducible comparison and a source-exact
dimension calculator. It does not establish that either item is new in the
literature.

## Reproduction

```bash
python -m unittest tests.test_geometry -v
python scripts/run_jl_construction_audit.py
```

Machine-readable output is in `results/jl_construction_audit.json`.

## Sources

- Yingru Li, [*Simple, unified analysis of Johnson-Lindenstrauss with
  applications*](https://arxiv.org/abs/2402.10232).
- Jeremiah Blocki, Avrim Blum, Anupam Datta, and Or Sheffet,
  [*The Johnson-Lindenstrauss Transform Itself Preserves Differential
  Privacy*](https://arxiv.org/abs/1204.2136).
