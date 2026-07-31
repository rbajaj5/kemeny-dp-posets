# Strong Outcomes Versus Oracle-Consistent Play

## Source and claim boundary

Brent Kong, Tejas Ram, and Tony Yue Yu, **AlphaZero in Sparsely Rewarded
Games: Limits and Auxiliary Supervision**,
[arXiv:2607.08984](https://arxiv.org/abs/2607.08984), 2026.

The paper evaluates AlphaZero-style agents on Connect Four and Chomp using
exact oracles. It separates empirical play strength from perfect play and
reports:

- pooled oracle-match rate;
- the longest chain of oracle-consistent labeled decisions;
- the first non-oracle game ply;
- the fraction of traces with no labeled oracle error; and
- oracle agreement on randomly sampled states, not only standard-start
  rollouts.

Its AlphaZero Auxiliary Loss adds an oracle-derived policy loss without
changing search. The reported experiments show substantial but nonuniform
improvement. In particular, perfect standard-start traces do not establish
perfect behavior over arbitrary sampled positions.

This repository does **not** reproduce AlphaZero, MCTS, neural training,
Connect Four, or the paper's numerical results.

## Exact finite implementation

The repository adds a small exact Chomp engine. A state is a nonincreasing
tuple of positive row lengths. The upper-left poisoned square is excluded
from safe moves, so `(1,)` is terminal and losing. For every state \(s\),

\[
g(s)=\operatorname{mex}\{g(s'):s'\text{ is a safe successor of }s\}.
\]

A winning state has \(g(s)\ne0\), and its oracle-optimal moves are precisely
the successors with Grundy number zero. Losing states have no labeled
oracle-best move. This follows standard Sprague-Grundy theory and is not a
new theorem.

The generic trace evaluator uses `None` for such unlabeled plies. It filters
them from match and chain denominators but retains original zero-based game
indices for first failure. A trace with no labeled decisions is reported as
ineligible, not vacuously perfect.

## Exact audit

The finite audit includes:

- all 923 nonempty partition states inside a \(6\times6\) box;
- all 875 winning, oracle-labeled states among them; and
- deterministic self-play from each of the 25 full rectangular boards with
  2 through 6 rows and columns.

The lexicographic oracle policy:

- matches the oracle on all 875 labeled states;
- has pooled match rate one and perfect-trace rate one; and
- realizes the oracle-predicted starting winner on all 25 full boards.

A deliberately simple largest-bite negative control:

- matches on only 10 of 875 labeled states, exactly \(2/175\);
- has pooled full-trace match rate \(1/2\);
- fails at ply zero and has no perfect trace on all 25 starts; and
- realizes the oracle-predicted starting winner on none of those starts.

The negative control is not offered as a strong learned policy. Its role is
to test the metric implementation against a clearly non-oracle policy.

## Consequence for this repository

Approximation ratio, sampled utility, exact optimality, and structural
constraint preservation are different measurements. Future heuristic Kemeny
experiments should therefore report at least:

1. exact-optimum agreement wherever the exact oracle is feasible;
2. score regret even when the selected ranking is not exact;
3. first failure and failure-shell information for sequential procedures;
4. standard-start and independently sampled-state results; and
5. explicit unlabeled or tied cases rather than silently scoring them.

These are evaluation rules. They do not imply that oracle supervision makes a
procedure private, efficient, neutral, or universally consistent.

## Reproduction

```bash
python scripts/run_oracle_consistency_audit.py
python -m unittest tests.test_chomp tests.test_oracle_eval -v
```

The exact output is in
[`results/oracle_consistency_audit.json`](../results/oracle_consistency_audit.json).
