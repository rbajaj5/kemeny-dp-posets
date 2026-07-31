# Zero-Mass Counterexample Source Assessment

## Source and result

Long Li and Mingchen Xia, **A counterexample to the zero-mass conjecture**,
[arXiv:2607.26549](https://arxiv.org/abs/2607.26549), 2026.

For a plurisubharmonic function \(u\) with an isolated singularity at the
origin, the comparison theorem gives

\[
\nu(u,0)^n\leq \tau(u,0),
\]

where \(\nu(u,0)\) is the Lelong number and \(\tau(u,0)\) is the residual
Monge-Ampere mass. Thus positive Lelong number forces positive residual mass.
The zero-mass conjecture asked whether the converse zero statement held:

\[
\nu(u,0)=0\quad\Longrightarrow\quad\tau(u,0)=0.
\]

Li and Xia construct an explicit negative plurisubharmonic function on the
unit polydisc in \(\mathbb C^2\) with an isolated pole, continuous
\(e^u\), zero Lelong number, and

\[
\operatorname{MA}(u)=\delta_0.
\]

They extend the example to every complex dimension \(n\geq2\). This
repository records the theorem as a source result; it does not independently
verify the pluripotential-theoretic proof.

## This is not the Bieberbach conjecture

The Bieberbach conjecture, [proved by de
Branges](https://doi.org/10.1007/BF02392821), concerns a normalized injective
holomorphic function of one complex variable,

\[
f(z)=z+\sum_{k\geq2}a_kz^k,
\]

and the coefficient bounds \(|a_k|\leq k\).

A plurisubharmonic function is instead a several-complex-variable potential
whose restriction to each complex line is subharmonic. Lelong numbers measure
singularity strength, while the nonlinear complex Monge-Ampere measure
records mass concentration. The subjects share the broad umbrella of complex
analysis but the conjectures, invariants, and proof methods are different.
No Bieberbach coefficient theorem is used here.

## Proof architecture in the source

The two-dimensional construction uses

\[
F_\varepsilon(z,w)
=\left(\frac12w^2,\frac12z^2+\varepsilon w\right).
\]

Each map is finite of degree four with zero fiber \(\{0\}\). For a rapidly
decreasing positive sequence \(\varepsilon_j\), the compositions

\[
H_j=F_{\varepsilon_j}\circ\cdots\circ F_{\varepsilon_1}
\]

have degree \(4^j\). The quadratic terms create the exponentially growing
topological degree, while the linear term preserves a nonzero derivative in
the direction \(e_2=(0,1)\).

At finite stage the paper defines

\[
q_j=2^{-j}\log\lVert H_j\rVert_\infty.
\]

The surviving linear term gives minimum component vanishing order one, hence

\[
\nu(q_j,0)=2^{-j}.
\]

Homogeneity of the two-dimensional Monge-Ampere operator and the degree
formula give

\[
\operatorname{MA}(q_j)
=(2^{-j})^2\,4^j\delta_0
=\delta_0.
\]

These finite stages alone are not a counterexample because their Lelong
numbers are positive. The source then:

1. truncates with \(V_j=\max\{q_j,-4^j\}\);
2. proves \(V_{j+1}\leq V_j\);
3. shows the cutoff cores shrink to the origin;
4. uses Demailly's sweeping formula and monotone continuity to obtain
   \(\operatorname{MA}(u)=\delta_0\) for \(u=\lim_jV_j\); and
5. constructs directional witness points to prove \(\nu(u,0)=0\), a step
   needed because Lelong numbers need not pass continuously to a decreasing
   limit.

The higher-dimensional result uses a maximum construction and a
Monge-Ampere product identity.

## Executable boundary

The repository checks the exact degree normalization for stages 1 through 20:

- `degree(H_j) = 4^j`;
- the potential scale is `2^-j`;
- the normalized mass is exactly one at every stage;
- the Lelong number is exactly `2^-j`; and
- the mass-to-Lelong ratio is `2^j`, reaching `1,048,576` at stage 20.

This is an exact arithmetic audit of the finite-stage formula in Proposition
3.2. It does not numerically establish plurisubharmonicity, weak convergence
of Monge-Ampere measures, continuity of \(e^u\), isolation of the limiting
pole, or the limiting Lelong number.

```bash
python scripts/run_zero_mass_scaling_audit.py
python -m unittest tests.test_zero_mass_scaling -v
```

The output is
[`results/zero_mass_scaling_audit.json`](../results/zero_mass_scaling_audit.json).

## Relevance to the Kemeny project

The transferable lesson is about one-sided inequalities, not complex
geometry. A lower bound from a coarse local invariant need not be reversible
without additional structure.

This repository already has a precise ranking analogue of that caution:

\[
b_{\rm TV}\geq \mu/2
\]

does not imply universal equality. Equality needs an endpoint-mass condition,
and an explicit four-candidate profile makes the inequality strict. Likewise,
first moments do not determine a random-profile law even though the complete
upper-set hierarchy does.

These are analogous proof disciplines only. Li-Xia's construction proves no
Kemeny, differential-privacy, voting, game, or market result.

## AI provenance

The paper acknowledges that an initial idea was constructed by a Rethlas
agent using `gpt-5.6-sol`, after which the authors developed the simpler
published construction and mathematical proof. The acknowledgment supports
transparent assistance provenance; it does not make an AI system an author
or independently validate the theorem.

## Status

`SOURCE THEOREM; FINITE-STAGE FORMULAS EXACTLY AUDITED; ANALYTIC LIMIT NOT
INDEPENDENTLY VERIFIED; NO TRANSPORTED THEOREM`.
