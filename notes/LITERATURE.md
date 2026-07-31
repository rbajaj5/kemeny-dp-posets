# Literature map

## Foundations used

- Cynthia Dwork, **Differential Privacy: A Survey of Results** (TAMC 2008).
  The source of the slide deck's cover-adjacency discussion, halfspace/JL
  example, and private-learning survey.
  <https://www.microsoft.com/en-us/research/publication/differential-privacy-a-survey-of-results/>

- Kobbi Nissim, Sofya Raskhodnikova, and Adam Smith, **Smooth Sensitivity and
  Sampling in Private Data Analysis** (STOC 2007). Defines local and smooth
  sensitivity, instance-calibrated noise, sample-and-aggregate, and an
  efficient center-of-attention for general metric spaces. The paper explicitly
  mentions NP-hard medians in permutation spaces.
  <https://people.csail.mit.edu/asmith/PS/stoc321-nissim.pdf>

- Cynthia Dwork, Ravi Kumar, Moni Naor, and D. Sivakumar, **Rank Aggregation
  Methods for the Web** (WWW 2001). Establishes foundational Kemeny and
  footrule aggregation results and the earlier constant-voter hardness result.
  <https://doi.org/10.1145/371920.372165>

## Private rank aggregation

- Michael Hay, Liudmila Elagina, and Gerome Miklau, **Differentially Private
  Rank Aggregation** (SDM 2017). Gives private Borda, private quicksort, and
  exponential-mechanism/rejection-sampling approaches. It observes that a
  single vote can completely change an optimum in the worst case.
  <https://people.cs.umass.edu/~miklau/assets/pubs/dp/hay17differentially.pdf>

- Daniel Alabi, Badih Ghazi, Ravi Kumar, and Pasin Manurangsi, **Private Rank
  Aggregation in Central and Local Models** (AAAI 2022). Gives
  distribution-independent polynomial-time upper and lower bounds.
  <https://arxiv.org/abs/2112.14652>

- Quentin Hillebrand, Pasin Manurangsi, Vorapong Suppakitpaisarn, and Phanu
  Vajanopath, **Improved Differentially Private Algorithms for Rank
  Aggregation** (AAAI 2026). Improves central-model Kemeny PTAS errors and
  studies private footrule aggregation.
  <https://arxiv.org/abs/2511.11319>

The two most recent algorithmic papers do not appear to use smooth sensitivity;
their guarantees are worst-case and distribution-independent. This statement is
based on a text search and needs a full bibliography-level audit before being
used as a novelty claim.

## Complexity and robustness

- Dominik Peters, **Kemeny Rank Aggregation is NP-Hard for Three Voters**
  (2026). Resolves the 25-year open case and supplies the sharp computational
  boundary used in this repository's sample-and-aggregate discussion.
  <https://arxiv.org/abs/2607.25540>

- Koustav De, Harshil Mittal, Palash Dey, and Neeldhara Misra,
  **Parameterized Aspects of Distinct Kemeny Rank Aggregation** (2023).
  Studies enumeration of distinct optimal and approximate Kemeny rankings
  under several parameters, including the candidate count and
  Kendall-distance-based parameters. It is the closest source identified in
  the targeted search for the distance-stratified certificate, but it does
  not by itself establish that the repository recurrence or robustness
  readout is novel.
  <https://arxiv.org/abs/2309.03517>

- Morgane Goibert, Clément Calauzènes, Ekhine Irurozki, and Stephan
  Clémençon, **Robust Consensus in Ranking Data Analysis** (ICML 2023).
  Develops breakdown functions for ranking medians and robust bucket-ranking
  alternatives. At attack amplitude `delta -> 0+`, its displayed Kemeny upper
  expression is the repository's normalized margin `mu`. Under standard
  half-`L1` TV, the paper's explicit attack has budget `mu/2`, and the
  repository proves this is exact under the paper's sufficient mass condition.
  Equation (4) and Appendix C.2 use incompatible factor-two normalizations;
  `notes/BREAKDOWN_COMPARISON.md` records the precise comparison.
  <https://proceedings.mlr.press/v202/goibert23a.html>

## Johnson-Lindenstrauss and privacy

- Yingru Li, **Simple, unified analysis of Johnson-Lindenstrauss with
  applications** (2024). Proposition 8 gives the explicit fixed-vector
  sufficient dimension `64 epsilon^-2 log(2/delta)` for both binary-coin and
  independent-column spherical projections. Proposition 24 applies a finite
  union bound. These are concentration results, not privacy or Kemeny argmin
  theorems.
  <https://arxiv.org/abs/2402.10232>

- Jeremiah Blocki, Avrim Blum, Anupam Datta, and Or Sheffet, **The
  Johnson-Lindenstrauss Transform Itself Preserves Differential Privacy**
  (FOCS 2012). Proves privacy for JL transforms under bounded rank-one changes
  and lower singular-value conditions.
  <https://arxiv.org/abs/1204.2136>

## Robust trade and market design

- Gabriel Carroll, **Informationally Robust Trade and Limits to Contagion**
  (Journal of Economic Theory 2016). Gives tight welfare-loss bounds for a
  two-agent, single-fixed-deal accept/reject game across arbitrary information
  structures. Section 5.3 identifies multiple proposals and double auctions as
  substantially harder open extensions. The Kemeny application in this
  repository attaches only to that multiple-proposal selection stage.
  <http://individual.utoronto.ca/carroll/robustlemons.pdf>

- Eric Budish, Peter Cramton, and John Shim, **The High-Frequency Trading Arms
  Race: Frequent Batch Auctions as a Market Design Response** (QJE 2015).
  Provides the microstructure motivation for batch rather than serial order
  processing. It does not use Kemeny aggregation.
  <https://doi.org/10.1093/qje/qjv027>

## Characterizing probability laws by hierarchies

- Paul Bourgade and Jiaoyang Huang, **Loop Equations Characterize Random
  Matrix Statistics** (2026). For rational positive beta, proves that the full
  microscopic bulk and edge loop-equation hierarchies uniquely identify the
  Sine-beta and Airy-beta point processes, respectively, and turns approximate
  hierarchies with uniform error control into convergence criteria. The
  repository imports only the proof discipline and a separate finite-poset
  Möbius-inversion analogue.
  <https://arxiv.org/abs/2607.07617>

## Hex/Y and heuristic-only topology source

- Anna R. Karlin and Yuval Peres, **Game Theory, Alive**. The Hex/Y section
  gives the unique-winner theorem and the recursive local majority reduction.
  The repository formalizes it in axial coordinates and connects the coloring
  Boolean lattice to local and smooth sensitivity.
  <https://math.uchicago.edu/~shmuel/Modeling/Peres%20and%20Wilson%2C%20Game%20Theory%20Alive.pdf>

- Jenny Lorraine Nielsen, **The Topological Unified Field Theory on the
  Complex Hopf Fibration** (listed as forthcoming). This is retained only as a
  heuristic prompt about local-to-global topology. No physical claim from it
  is used. See `notes/TUFT_SOURCE_ASSESSMENT.md`.
  <https://philpapers.org/rec/NIETTU>

- John Reimer Morales, **Closing the Gaps on TUFT: Where the Mathematics Ends
  and the Unification Claim Begins**. This critical review distinguishes a
  classifying-space core from unestablished bridges to physical unification.
  <https://philpapers.org/rec/REICTG>

- Yuntian Hou, Tianrui Ji, Di Zhang, and Angelos Stefanidis,
  **Kolmogorov-Arnold Networks: A Critical Assessment of Claims, Performance,
  and Practical Viability**. Its warnings about discrete combinatorial targets,
  resource-controlled baselines, repeated runs, and the gap between a theorem
  and an implemented architecture govern the repository's decision not to
  treat the Y majority circuit as evidence for a KAN advantage.
  <https://arxiv.org/abs/2407.11075>

- Andrew Critch and Jacob Tsimerman, **A Taxonomy of Omnicidal Futures
  Involving Artificial Intelligence**. This is used only as a scenario
  classification and governance prompt. It supplies neither empirical
  probabilities nor a market, privacy, or social-choice theorem.
  <https://arxiv.org/abs/2507.09369>

- Arthur M. Jaffe and Zhengwei Liu, **A Mathematical Picture Language
  Program** (PNAS 2018). Distinguishes a picture language `L`, a target
  mathematical reality `R`, and a simulation `S: L -> R`; asks when
  computations can be performed completely in the picture language. The
  repository uses this as a soundness audit for transporting diagrammatic
  identities, not as a claim that its diagrams form a TQFT.
  <https://doi.org/10.1073/pnas.1710707114>

## Research practice and non-instrumental exploration

- Rabindranath Tagore, **The Fugitive** (1921), section 26 of
  *The Fugitive-III*. The untitled prose-poem is often circulated as "A Wrong
  Man in Workers' Paradise." It is used here only to distinguish open-ended
  exploration from certification. It supplies no mathematical premise.
  <https://www.gutenberg.org/ebooks/7971>

## Benchmark validity and structural supervision

- Tobias Gessler, Tin Dizdarevic, Anisoara Calinescu, Benjamin Ellis, Andrei
  Lupu, and Jakob Foerster, **OvercookedV2: Rethinking Overcooked for
  Zero-Shot Coordination** (ICLR 2025). Separates state-coverage artifacts
  from coordination problems involving asymmetric information, grounded
  communication, stochasticity, and test-time feedback. The repository
  exactly audits the paper's grounded Button Game and a separate ungrounded
  binary convention counterexample.
  <https://arxiv.org/abs/2503.17821>

- Brent Kong, Tejas Ram, and Tony Yue Yu, **AlphaZero in Sparsely Rewarded
  Games: Limits and Auxiliary Supervision** (2026). Distinguishes strong
  empirical outcomes from exact oracle-consistent play in Connect Four and
  Chomp. The repository implements its trace-metric definitions and a separate
  exact small-board Chomp oracle, not its AlphaZero experiments.
  <https://arxiv.org/abs/2607.08984>

- Joachim Bona-Pellissier, Giacomo Meanti, Matteo Santacesaria, and Lorenzo
  Rosasco, **PIKS: Universal Physics-Informed Kernel Methods** (2026). Proves
  simultaneous value and linear-operator consistency under RKHS density,
  boundedness, sampling, and regularization hypotheses. Only the diagnostic
  separation of fit from structural residual is retained; no PDE/RKHS theorem
  is transported to Kemeny aggregation.
  <https://arxiv.org/abs/2607.27062>

## Complex-analysis counterexample discipline

- Long Li and Mingchen Xia, **A counterexample to the zero-mass conjecture**
  (2026). Constructs an isolated plurisubharmonic singularity with zero Lelong
  number and unit residual Monge-Ampere mass in every complex dimension at
  least two. The repository audits only the exact two-dimensional finite-stage
  scaling `degree = 4^j`, `scale = 2^-j`, mass one, and Lelong number `2^-j`.
  The decreasing truncation and analytic limit remain source results. This is
  unrelated to the Bieberbach coefficient theorem.
  <https://arxiv.org/abs/2607.26549>
