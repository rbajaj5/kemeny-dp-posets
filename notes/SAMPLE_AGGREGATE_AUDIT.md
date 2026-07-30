# Sample-and-center finite audit

## Status

This note tests the utility-side components of sample-and-aggregate. It does
**not** claim that the implemented pipeline is differentially private. The
center lemma below is a standard metric argument; the finite counts are exact
computations, not novelty claims.

## 1. Center certificates

Given metric points `z_1,...,z_q`, a step `s`, and

```text
k = floor((q+s)/2) + 1,
```

define the radius of a proposed center `z` as its `k`-th smallest distance to
the input multiset. Let

```text
r_in  = minimum radius over input points,
r_all = minimum radius over the full metric space.
```

The implementation now returns an `AttentionCertificate` containing the
selected input center, `r_in`, `k`, and the complete set of minimizing input
centers.

### Proposition: sharp metric factor two

For every finite metric input,

```text
r_all <= r_in <= 2 r_all.
```

**Proof.** The first inequality is immediate because the input points are a
subset of all possible centers. Let a center of radius `r_all` contain `k`
input points, and choose any one `z_i` among those points. By the triangle
inequality, every one of the same `k` points lies within distance `2 r_all` of
`z_i`. Thus an input-restricted center has radius at most `2 r_all`.

The constant is sharp already in the three-candidate Kendall space. For the
two points `ABC` and `BCA`, with `k=2`, the best input center has radius two,
while `BAC` has radius one.

## 2. Relabeling and deterministic resolution

Kendall distance is invariant under a common relabeling of candidates.
Therefore the **set** of minimum-radius input centers is relabeling
equivariant. The exact audit finds zero violations.

The implementation chooses the lexicographically first minimizer when a
single deterministic ranking is required. That selector is not neutral. This
is not merely an implementation accident: if the input multiset contains
every ranking equally often, it is invariant under every candidate
relabeling, but no single linear ranking is fixed by every relabeling. A
deterministic resolute and fully neutral selector cannot exist on that
symmetric input.

The certificate exposes the full minimizer set so downstream work can use a
set-valued result or an explicitly randomized tie-break. No privacy or
neutrality claim attaches to the lexicographic selector.

## 3. Exact two-ballot blocks

For two ballots `a,b`, the triangle inequality gives

```text
d(a,z) + d(z,b) >= d(a,b)
```

for every ranking `z`, with equality at either endpoint. Hence returning the
lexicographically smaller of the two input ballots is an exact Kemeny
solution and avoids factorial enumeration.

The audit checks all 612 ordered pairs for three and four candidates. There
are zero optimum failures and zero input-support failures. The shortcut
differs from the old factorial selector on 246 pairs because both choose
valid optima but resolve the often-large two-ballot optimum set differently.

## 4. Polynomial-time larger blocks

`borda_ranking` provides a polynomial-time block estimator when exact Kemeny
is undesirable beyond two ballots. Borda's general approximation guarantee
is prior work; this repository only audits its finite behavior.

Across all 3,002 nonempty three-candidate profiles through eight ballots:

- Borda attains the exact optimum cost on 2,712 profiles;
- there are zero violations of the known factor-five bound; and
- the largest observed cost ratio is `3/2`, first attained by
  `BAC:1 CBA:2`.

The observed `3/2` is not claimed as a general bound.

## 5. Exhaustive center results

For every three-candidate point multiset of sizes two through seven and every
admissible step, the audit checks 8,581 certificates:

- zero input-center failures;
- zero target-count failures;
- zero factor-two-bound failures;
- zero minimizer-set relabeling failures;
- 986 sharp factor-two cases; and
- 17,129 lexicographic-selector failures among 51,486 relabeling checks.

The last count is a diagnostic of deterministic tie-breaking, not a failure
of the metric-center construction.

## 6. Validation correction and privacy boundary

Earlier code validated only ballots that landed in complete blocks after
shuffling. An invalid ballot in the discarded remainder could therefore
escape validation. The block partitioner now validates every ballot before
shuffling, and the regression test places an invalid ballot precisely in such
an input.

The tested utility pipeline is

```text
validated random blocks
  -> exact two-ballot / exact enumerated / Borda block outputs
  -> input-restricted center certificate.
```

An end-to-end private sample-and-aggregate mechanism still needs a precise
record-to-block influence argument, a private admissible-radius test or noise
stage, and a utility theorem under a stated distributional condition.

## Reproduction

```bash
python scripts/run_sample_aggregate_audit.py
python -m unittest tests.test_sample_aggregate -v
```

Machine-readable output is in `results/sample_aggregate_audit.json`.
