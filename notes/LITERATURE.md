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

- Marine Goibert, Alessandro Cloninger, Grégoire Leclercq, and Stephan
  Clémençon, **Robust Consensus in Ranking Data Analysis** (ICML 2023).
  Develops breakdown functions for ranking medians and robust bucket-ranking
  alternatives. This is the closest known comparison point for the Hasse
  uniqueness radius.
  <https://proceedings.mlr.press/v202/goibert23a.html>

## Johnson-Lindenstrauss and privacy

- Jeremiah Blocki, Avrim Blum, Anupam Datta, and Or Sheffet, **The
  Johnson-Lindenstrauss Transform Itself Preserves Differential Privacy**
  (FOCS 2012). Proves privacy for JL transforms under bounded rank-one changes
  and lower singular-value conditions.
  <https://arxiv.org/abs/1204.2136>

