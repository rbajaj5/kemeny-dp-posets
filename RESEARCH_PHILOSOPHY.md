# Research Philosophy: A Quiet Public Program

This repository is intended to remain public, cumulative, and technically
checkable without treating every increment as an announcement.

## A "cuspidal core" analogy

Harish-Chandra's philosophy of cusp forms organizes broad representation
theories around irreducible cuspidal or discrete building blocks, with more
general objects obtained through induction. We use that only as an
organizational analogy:

- the **core** consists of short proved structural statements;
- **induced applications** transport the core into differential privacy,
  learning, random projection, sample-and-aggregate, and market design;
- an application must state the extra assumptions introduced during that
  transport; and
- computational evidence is not promoted into the core.

The current core is:

1. the profile Hasse graph equals add/remove-one-ballot adjacency;
2. the exact uniqueness-radius formula;
3. the `n-2` non-unanimous metric-median bound and three-voter radius
   dichotomy;
4. the resulting smooth upper bound; and
5. the price/time/size hardness encoding;
6. exact binary-query smooth sensitivity on finite Hamming graphs;
7. the exact Y majority circuit derived from the known reduction; and
8. finite-poset law reconstruction by the full upper-set hierarchy; and
9. distance-stratified subset-DP stability certificates.

The analogy is not a mathematical claim about cusp forms or representations.
It is a rule for keeping a growing research program intelligible.

## Useful uselessness

Tagore's untitled section 26 of *The Fugitive-III*, often circulated as "A
Wrong Man in Workers' Paradise," introduces art into a society that recognizes
only immediately useful work. The patterns on a water pitcher have no stated
purpose, yet they reveal attention and preference that the society's schedule
could not represent.

The repository takes this as permission to explore questions before their
utility is known. It does not take it as permission to publish unsupported
claims. Exploration may begin with a pattern, analogy, or failed experiment;
certification still requires a correct source, a defined target, a proof or
reproducible computation, and an explicit status label.

The dedicated [source and policy note](notes/TAGORE_USELESS_WORK.md) also
corrects a bibliographic ambiguity in the supplied transcript: the English
piece is in *The Fugitive* (1921), not *Gitanjali*.

## Local rules and global invariants

The supplied Topological Unified Field Theory manuscript prompted a useful
question about local structure and global invariants. It is not used here as
evidence for any physical or mathematical result; the repository's
[source assessment](notes/TUFT_SOURCE_ASSESSMENT.md) explains that boundary.

The rigorous model is instead the game of Y. Its three-cell majority
coarse-graining preserves a global three-side connectivity winner all the way
to one cell. This is exactly the kind of local-to-global statement the program
can use: finite definitions, an independent proof, exhaustive checks, and an
explicit account of what the reduction does not preserve. In particular,
winner preservation does not imply preservation of Hasse distance, privacy,
or Kemeny computational complexity.

## Picture language and theorem transport

Jaffe and Liu's distinction between a picture language `L`, a target reality
`R`, and a simulation `S: L -> R` supplies a rule for cross-field work:
an identity in `L` becomes a theorem in `R` only after the generating picture
relations are shown to be sound under `S`.

The repository's [transport audit](notes/PICTURE_LANGUAGE.md) now applies this
test to profile Hasse diagrams, coloring Hasse diagrams, the Y majority
rewrite, pairwise ranking embeddings, the market encoding, and heuristic
topology language. This replaces resemblance-based analogy with explicit
commuting maps and documented failure points.

## Tail statements and finite evidence

Sheffield's probability lecture emphasizes that a tail event is unchanged by
finitely many observations, and that independent tail events obey a zero-one
law. It also recalls the strong law of large numbers. These ideas impose a
useful separation:

- a theorem must survive changes to any finite collection of experiment rows;
- a long-run Monte Carlo convergence statement is different from the reported
  finite sample; and
- a repository history is evidence of provenance, not evidence that a theorem
  is true.

Vershynin's Berry-Esseen exposition makes the complementary finite-sample
point: a central-limit approximation needs a quantitative error term. For
every Bernoulli market experiment, the repository therefore records:

- successes and trials;
- the empirical rate and standard error;
- a Wilson 95% interval; and
- the plug-in standardized third-moment ratio divided by `sqrt(n)`.

The last quantity omits the theorem's absolute constant and substitutes an
estimate for the unknown Bernoulli parameter. It is labeled as a diagnostic,
not presented as a rigorous coverage guarantee.

## Priority and publication

The repository follows these rules:

1. Keep derivations, executable checks, and corrections in public commits.
2. Maintain `PROVENANCE.md`, `CHANGELOG.md`, and `CITATION.cff`.
3. State the closest known prior result beside every possible contribution.
4. Use `PROVED`, `KNOWN`, `COMPUTATIONAL`, `CONJECTURE`, and `OPEN`
   consistently.
5. Do not call a result novel until a bibliography-level comparison has been
   completed.
6. Correct errors in place and describe the correction in the changelog.
7. Do not submit to arXiv merely to amplify an incomplete research program.
   A later archival paper should be driven by a coherent theorem package and a
   completed prior-art audit.

Public Git history helps establish when text and code were available, but it
is not by itself a definitive adjudication of mathematical priority.

## Analysis is not deployment

The repository's synthetic mechanisms and games do not authorize autonomous
action in markets or other institutions. The
[AI-risk governance note](notes/AI_RISK_GOVERNANCE.md) uses the
Critch-Tsimerman taxonomy to keep scenario classification separate from
probability estimation, mechanism selection, and real-world deployment.
Public availability is provenance and reproducibility, not permission to
execute a mechanism against people or infrastructure.

## Sources for the organizing analogy

- Scott Sheffield, [18.175 Lecture 10: Zero-one laws and maximal
  inequalities](https://math.mit.edu/~sheffield/175/Lecture10.pdf).
- Roman Vershynin, [*A Friendly Proof of the Berry-Esseen
  Theorem*](https://arxiv.org/abs/2602.06234).
- James Arthur, [*Harish-Chandra: A
  Memoir*](https://publications.ias.edu/sites/default/files/harish2.pdf),
  especially the discussion of his sustained cumulative program and philosophy
  of cusp forms.
- Anna R. Karlin and Yuval Peres,
  [*Game Theory, Alive*](https://math.uchicago.edu/~shmuel/Modeling/Peres%20and%20Wilson%2C%20Game%20Theory%20Alive.pdf),
  for the Hex/Y local-majority reduction.
- Arthur M. Jaffe and Zhengwei Liu,
  [*A Mathematical Picture Language Program*](https://doi.org/10.1073/pnas.1710707114),
  for the language/reality/simulation distinction.
- Rabindranath Tagore,
  [*The Fugitive*](https://www.gutenberg.org/ebooks/7971), section 26 of
  *The Fugitive-III*, for the distinction between exploration and compulsory
  utility.
