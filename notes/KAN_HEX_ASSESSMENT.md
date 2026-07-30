# Kolmogorov-Arnold Networks and the Hex/Y Laboratory

## Decision

Do not train a Kolmogorov-Arnold Network merely because the Y proof is a
layered local-to-global computation. The current target is discrete,
combinatorial, and discontinuous, while the supplied critical assessment
locates KANs' most credible advantages in smooth symbolic regression and
scientific function approximation.

The useful action is to expose and benchmark the exact architecture already
provided by the Y theorem.

## Exact majority-circuit representation

Let

```text
maj(x,y,z) = 1{x+y+z >= 2}.
```

The side-`n` to side-`n-1` reduction applies one such gate for every cell of
the smaller board. Repeating the reduction computes the unique Y winner.
Therefore the winner has a monotone ternary-majority circuit with

```text
depth = n - 1
size  = sum_{k=1}^{n-1} k(k+1)/2
      = (n-1)n(n+1)/6
      = choose(n+1, 3).
```

This is an exact representation, not a learned approximation. The formula is
a direct corollary of the known majority reduction.

One majority gate could be written as an outer threshold applied to the sum of
three identity edge functions, which is superficially KAN-like. That
observation adds no approximation or complexity result: the outer map is
discontinuous, the inputs are Boolean, and the full circuit's overlapping
dependencies carry the real structure.

## What the supplied assessment changes

Hou et al. emphasize four evaluation rules relevant here:

1. distinguish a representation theorem from the implemented architecture;
2. do not assume smooth-function success transfers to discrete optimization
   or combinatorial solving;
3. compare under both resource and computational-cost controls; and
4. use multiple seeds or repeats rather than a single point estimate.

Accordingly, `scripts/run_hex_y.py` compares direct connectivity search with
the exact majority circuit on the same pre-generated boards, reports
mismatches, and uses the median of repeated timings. The timing ratio is
labeled machine-dependent and is not used as a complexity theorem.

With 1,000 unbiased boards per size and five timed repeats, the cached
standard-library implementations produced:

| Side | Gates per board | Mismatches | Circuit/direct median time |
|---:|---:|---:|---:|
| 8 | 84 | 0 | 4.47x |
| 12 | 286 | 0 | 7.18x |
| 16 | 680 | 0 | 9.36x |
| 24 | 2,300 | 0 | 15.17x |

This machine-dependent result favors direct bitset connectivity for bulk
evaluation. The majority circuit remains valuable as a constructive
winner-preservation certificate and a local-to-global object of study.

A future learned-surrogate experiment is admissible only if it includes:

- the exact circuit and a conventional MLP or tree baseline;
- equal parameter and FLOP/latency budgets;
- held-out board sizes, not only held-out colorings at one size;
- multiple seeds and uncertainty summaries;
- accuracy on near-boundary colorings stratified by exact outcome radius; and
- wall-clock training and inference cost.

Until that comparison exists, adding KAN and GPU dependencies would increase
complexity without advancing the proved Hex results.

## Source

- Yuntian Hou, Tianrui Ji, Di Zhang, and Angelos Stefanidis,
  [*Kolmogorov-Arnold Networks: A Critical Assessment of Claims, Performance,
  and Practical Viability*](https://arxiv.org/abs/2407.11075), arXiv:2407.11075.
