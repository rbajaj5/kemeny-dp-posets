# AI-Risk Taxonomy: Governance Boundary and Social-Choice Application

## Source use

Critch and Tsimerman give a five-part taxonomy of possible AI-involved
omnicide according to whether lethal intent exists and, if so, whether its
earliest seat is a state, institution, individual, or AI system. They present
scenarios to support prevention, not as inevitabilities or calibrated
forecasts.

This repository uses that work only for two purposes:

1. to distinguish **scenario classification** from empirical probability; and
2. to define an open, high-level social-choice application for ranking
   preventive priorities.

No harmful scenario is simulated, operationalized, or assigned a probability.

## A possible rank-aggregation layer

Suppose several stakeholders each rank a fixed, high-level menu of mitigations
or oversight priorities. A Kemeny rule could aggregate those rankings.
Peters's result immediately supplies the worst-case computational warning:
exact Kemeny aggregation remains NP-hard even with three stakeholder rankings
as the number of ranked items grows.

That observation does **not** show that Kemeny is an appropriate governance
rule. Any real application would still have to justify:

- who is represented and who is missing;
- whether ordinal ranks discard unacceptable differences in severity,
  tractability, evidence quality, or urgency;
- how conflicts of interest and strategic reports are handled;
- whether assessor privacy is substantively needed;
- whether minority vetoes or rights constraints override a median ranking;
  and
- how an aggregate ranking relates to an authorized human decision.

With only five high-level taxonomy categories, exact computation is trivial;
the hard part is normative and epistemic. The repository therefore records
this as an **OPEN APPLICATION**, not a policy recommendation.

## Safety and deployment boundary

The current code:

- enumerates finite rankings and game boards;
- runs synthetic market-priority and coloring experiments;
- does not connect to exchanges, robots, weapons, laboratories, or production
  decision systems;
- does not autonomously act on people or institutions; and
- does not infer or publish catastrophe probabilities.

Future work must preserve a human authorization boundary between analysis and
external action. A public commit is provenance for code and claims, not
permission to deploy a mechanism.

## Source

- Andrew Critch and Jacob Tsimerman,
  [*A Taxonomy of Omnicidal Futures Involving Artificial
  Intelligence*](https://arxiv.org/abs/2507.09369), arXiv:2507.09369.
