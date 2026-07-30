# Three-Ranking Kemeny Rules in Robust Market Design

## Scope

Gabriel Carroll's *Informationally Robust Trade and Limits to Contagion*
studies two agents deciding whether to accept one fixed deal. The paper gives a
tight robust prediction across unknown information structures and, under its
Condition B, shows that the simple bilateral accept/reject mechanism is
robustly optimal.

Kemeny aggregation does **not** enter that single-deal theorem. The connection
starts in Carroll's Section 5.3, which asks what happens with multiple possible
deals and leaves the problem open. A natural two-stage extension is:

1. rank or select the candidate proposals;
2. submit the chosen proposal to the two agents for bilateral acceptance.

The first stage can receive three rankings—for example, buyer, seller, and
regulator rankings of candidate deals, or price, time, and size rankings of
orders. The second stage remains Carroll's consent game.

## A market-priority hardness corollary

Consider distinct orders on one side of a book. Give every order three
distinct attributes:

- price, ranked from more aggressive to less aggressive;
- arrival time, ranked from earlier to later; and
- size, ranked from larger to smaller.

Suppose a composite priority rule returns a ranking minimizing total Kendall
distance to these three attribute rankings.

**Proposition (proved by encoding).** Computing this exact composite order
priority is NP-hard in the number of orders.

**Proof.** Take any three rankings from a three-voter Kemeny instance. Assign
strict prices in the order of the first ranking, strict timestamps in the
order of the second, and strict sizes in the order of the third. The induced
price, time, and size priority lists are exactly the three input rankings.
An exact composite priority solver would therefore solve every three-voter
Kemeny instance. Peters proves that problem NP-hard. \(\square\)

This is a statement about a hypothetical symmetric Kemeny composite. Actual
exchanges commonly impose lexicographic price-time rules, so the proposition
does not claim that ordinary order matching is NP-hard.

## Stability of the composite rule

The metric radius dichotomy applies immediately:

- if the three priority rankings agree, the unique consensus has cover radius
  three;
- if they do not agree but have a unique Kemeny consensus, its radius is one;
  and
- if the Kemeny optimum is tied, its radius is zero.

Thus an exact, non-unanimous three-criterion composite has no cover buffer
against adding one new priority source. The current smooth-sensitivity bound
also collapses to the global Kendall diameter in that case.

## Structure can remove the obstruction

Carroll's multiple-proposal example is a set of possible prices. If three
stakeholders have single-peaked rankings on this one-dimensional price line,
their pairwise majority relation is transitive. The Kemeny optimum is then the
majority ranking and can be obtained without solving a generic feedback-arc
problem.

The distinction is important:

- one-dimensional, single-peaked proposal menus can be tractable;
- multidimensional market-design alternatives or independently assigned
  price/time/size priorities can encode unrestricted rankings and inherit the
  Peters obstruction.

## Computational experiment

`scripts/run_market_microstructure.py` compares the two domains. It uses a
subset dynamic program with `2^m` states, avoiding factorial enumeration while
remaining exponential in accordance with the worst-case hardness result.
Each row contains 500 independent synthetic instances. Rates are accompanied
by standard errors, Wilson 95% intervals, and a plug-in Berry-Esseen
third-moment diagnostic in the machine-readable output.

### Independent price, time, and size priorities

| Orders | Majority-cycle rate | Unique Kemeny rate | Consensus is an input ranking |
|---:|---:|---:|---:|
| 5 | 0.350 | 0.788 | 0.484 |
| 8 | 0.760 | 0.598 | 0.060 |
| 10 | 0.914 | 0.512 | 0.026 |
| 12 | 0.986 | 0.370 | 0.004 |

As the number of orders rises, majority cycles become typical and the selected
consensus rarely equals any of the three criteria. Every unique
non-unanimous instance has cover radius one, as proved.

### Single-peaked price menus

For 5, 8, 10, and 12 proposals, all 2,000 generated instances had:

- no majority cycle;
- a unique Kemeny ranking; and
- a selected consensus equal to one of the three input rankings.

This is a computational check of a structured domain, not a new proof of the
classical single-peaked majority theorem.

The absence of cycles in 500 trials per row has a Wilson 95% upper endpoint of
approximately 0.0076; it is evidence consistent with the structural theorem,
not a proof derived from simulation.

## What would constitute a Carroll-style economic result

The current work proves a computational boundary for a proposed selection
layer; it does not prove an equilibrium or welfare theorem. A genuine
multiple-proposal extension should specify:

1. how each proposal changes the prior distribution of bilateral values;
2. which information structures are allowed across proposals;
3. whether proposal rankings are reports, signals, or designer objectives;
4. strategic incentives in the ranking stage;
5. whether agents can coordinate on the best equilibrium after selection; and
6. the robust welfare criterion before and after adding the selection layer.

One tractable starting point is to compute Carroll's robust guarantee
separately for each fixed proposal and then study structured rankings of those
guarantees. This preserves the paper's single-deal theorem proposal by
proposal. A joint mechanism that endogenously chooses the proposal requires a
new robust-design theorem.

## Sources

- Gabriel Carroll, [*Informationally Robust Trade and Limits to
  Contagion*](http://individual.utoronto.ca/carroll/robustlemons.pdf),
  Journal of Economic Theory 166 (2016), 334–361.
- Dominik Peters, [*Kemeny Rank Aggregation is NP-Hard for Three
  Voters*](https://arxiv.org/abs/2607.25540), 2026.
- Eric Budish, Peter Cramton, and John Shim,
  [*The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market
  Design Response*](https://doi.org/10.1093/qje/qjv027), QJE 2015.

## Reproduction

```bash
python scripts/run_market_microstructure.py
```

Machine-readable output is in `results/market_microstructure.json`.
