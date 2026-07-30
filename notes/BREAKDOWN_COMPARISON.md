# Exact comparison with ranking breakdown functions

## Status and convention

This note gives a **proved finite specialization** and an exact implementation.
Its novelty is unconfirmed. Throughout,

```text
TV(p,q) = ||p-q||_1 / 2.
```

That convention is essential. Goibert, Calauzènes, Irurozki, and Clémençon
(ICML 2023) use `1/2 ||p-q||_1` in their Equation (4), but Appendix C.2,
Equation (33), bounds the full `L1` change by the TV budget. Those two displayed
normalizations differ by a factor of two. The comparison below is derived
independently under the standard half-`L1` convention.

## Two perturbation models

Let `x` be a nonempty empirical profile of size `n`, let `p_x=x/n`, and assume
that `sigma` is its unique Kemeny optimum. For `tau != sigma`, set

```text
gap_x(tau) = C_x(tau) - C_x(sigma)
d_tau      = d_K(sigma,tau)
mu(x)      = min_tau gap_x(tau) / (n d_tau).
```

The repository's cover model adds or removes one whole ballot and may change
the sample size. Its exact integer radius is therefore

```text
R(x) = ceil(n mu(x)).
```

The continuous contamination model keeps total probability one and moves
fractional mass. Define its zero-plus boundary by

```text
b_TV(p_x) = inf {
    TV(p_x,q):
    sigma is not the unique Kemeny optimum under q
}.
```

The infimum is also the threshold for a strict output change: in this finite
linear problem, a strict crossing can approach the tie boundary arbitrarily
closely.

## Exact TV formula

Fix a competitor `tau` and define

```text
f_tau(rho) = d_K(rho,tau) - d_K(rho,sigma)
g_tau      = E_p[f_tau] = gap_x(tau)/n.
```

The reverse triangle inequality gives

```text
-d_tau <= f_tau(rho) <= d_tau.
```

The lower endpoint is attained at `rho=tau`; the upper endpoint is attained at
`rho=sigma`. Let `Q_tau(u)` be the decreasing quantile of `f_tau(rho)` when
`rho` has law `p_x`. Then the exact TV distance to the halfspace where `tau`
ties `sigma` is

```text
b_tau = inf {
    t >= 0:
    integral_0^t (Q_tau(u) + d_tau) du >= g_tau
}.
```

Consequently,

```text
b_TV(p_x) = min_{tau != sigma} b_tau.
```

**Proof.** A TV move of size `t` removes `t` probability mass and adds `t`
mass. For a fixed `t`, the greatest possible reduction of `E[f_tau]` removes
mass in decreasing order of `f_tau` and adds it at its minimum `-d_tau`.
The state `tau` has enough receiving capacity for every unit removed outside
it. The displayed integral is exactly that maximum reduction. The original
optimum loses uniqueness exactly when at least one competitor's expectation
reaches zero. Taking the first crossing and then the minimum over competitors
proves both formulas.

The implementation performs the quantile integral with exact rational
arithmetic by sorting the finitely many coefficient levels.

## The sharp factor-two bridge

Since `Q_tau(u)+d_tau <= 2d_tau`,

```text
b_tau >= gap_x(tau)/(2n d_tau),
b_TV(p_x) >= mu(x)/2.
```

Equality holds if a competitor attaining `mu(x)` has at least
`gap_x(tau)/(2n d_tau)` empirical mass on coefficient level
`f_tau=d_tau`. A simpler sufficient condition is

```text
mu(x) <= 2 p_x(sigma),
```

because `sigma` lies on that top coefficient level. Under this condition,
moving `mu(x)/2` mass from `sigma` to the reverse of `sigma` attains the lower
bound. Hence

```text
b_TV(p_x) = mu(x)/2,
R(x)      = ceil(2n b_TV(p_x)).
```

The last identity is numerical, not an identification of adjacencies:
add/remove-one-ballot covers and fixed-mass TV contamination remain different
perturbation models.

## What happens to the ICML 2023 expression

At attack amplitude `delta -> 0+`, the inner comparison set in Goibert et
al.'s Theorem 3.1 contains only the original unique optimum. Their displayed
Kemeny upper expression therefore simplifies exactly to

```text
epsilon_plus(0+) = mu(x).
```

Their explicit attack removes `epsilon/2` mass from `sigma` and adds it to the
reverse ranking. Under standard TV, that attack has budget `epsilon/2`, not
`epsilon`. Thus, when their mass condition holds, the construction itself
gives the sharper standard-TV value `mu(x)/2`, matching the independent lower
bound above.

Appendix C.2 writes `||q_+ - q_-||_1 <= epsilon` under
`TV(p,q) <= epsilon`. In fact,

```text
||q_+ - q_-||_1 = ||p-q||_1 = 2 TV(p,q).
```

This is the precise factor-of-two discrepancy. We make no claim here about a
full correction of their general positive-`delta` or bucket-ranking results.

## Exact finite audit

`scripts/run_breakdown_comparison.py` checks all 2,232 uniquely optimized
three-candidate profiles of sizes one through eight:

- zero cover-radius identity failures;
- zero violations of `b_TV >= mu/2`;
- all 2,232 cases attain `b_TV=mu/2`.

The script also records a four-candidate, ten-ballot profile where the
inequality is strict:

```text
mu(x)       = 1/15
mu(x)/2     = 1/30
b_TV(p_x)  = 1/20.
```

Thus the factor-two equality is sharp under its sufficient condition but is
not universal.

## Source

Morgane Goibert, Clément Calauzènes, Ekhine Irurozki, and Stephan Clémençon,
“Robust Consensus in Ranking Data Analysis: Definitions, Properties and
Computational Issues,” ICML 2023.
<https://proceedings.mlr.press/v202/goibert23a.html>
