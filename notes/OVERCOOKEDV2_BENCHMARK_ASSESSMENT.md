# State Coverage Versus Coordination

## Source and scope

Tobias Gessler, Tin Dizdarevic, Anisoara Calinescu, Benjamin Ellis,
Andrei Lupu, and Jakob Foerster, **OvercookedV2: Rethinking Overcooked for
Zero-Shot Coordination**, ICLR 2025, [arXiv:2503.17821](https://arxiv.org/abs/2503.17821).

The paper argues that some cross-play failures in the original Overcooked
benchmark are state-coverage failures rather than evidence of a hard
coordination problem. State augmentation nearly closes those gaps. It then
introduces environments with asymmetric information, stochasticity, grounded
communication, and test-time feedback, where exhaustive state coverage need
not resolve incompatible behavior.

This repository does not reproduce the Overcooked reinforcement-learning
experiments. It implements two exact finite games that isolate the distinction.
Neither game is a Kemeny, differential-privacy, or market theorem.

## Grounded Button Game

Appendix A.1 of the source defines a Button Game. Alice observes a hidden bit
\(b\in\{0,1\}\), chooses one of \(N\) buttons \(a\in\{0,\ldots,N-1\}\), and
lights bulb

\[
\ell=2a+b.
\]

Bob can recover the hidden bit from \(\ell\bmod 2\), independently of Alice's
button convention.

**Proposition 1 (coverage artifact).** Suppose a brittle receiver learned the
parity rule only for a single training button \(j\), and makes a fixed guess on
every unseen button. Under a uniform hidden bit, its accuracy against a sender
using button \(i\) is

\[
\Pr(\widehat b=b)=
\begin{cases}
1,&i=j,\\
\frac12,&i\ne j.
\end{cases}
\]

If state augmentation covers every button, the same receiver family attains
accuracy one against every sender button.

**Proof.** On the covered button, bulb parity equals \(b\). On an uncovered
button, the receiver's fixed guess agrees with a uniform bit with probability
one half. Covering all buttons removes the second case. \(\square\)

The `N=10` audit checks all 20 grounded bulb states and all 100 sender/training
button pairs. The exact self-play/cross-play matrix has ones on the diagonal
and one halves off the diagonal. Full state coverage makes every entry one.

## An ungrounded protocol counterexample

Coverage is not sufficient when observations have no partner-independent
semantics. Let a sender encode \(b\) using either convention

\[
e_0=(0,1),\qquad e_1=(1,0).
\]

Both conventions use both messages, so each has complete message coverage.

**Proposition 2 (coverage does not resolve conventions).**

1. A decoder paired with its encoder has accuracy one.
2. A decoder paired with the opposite encoder has accuracy zero.
3. Every fixed deterministic decoder has mean accuracy exactly one half under
   a uniform choice between the two encoders and a uniform hidden bit.
4. One labeled interaction identifies which of the two bijective conventions
   is active, after which future accuracy is one.

**Proof.** The paired decoder is the encoder's inverse; the crossed inverse
flips both hidden bits. Across the identity and flipped encoders, each message
is associated once with bit zero and once with bit one. A fixed guess for that
message is therefore right in exactly one of those two cases. Finally, one
observed pair `(message, revealed bit)` distinguishes identity from flip.
\(\square\)

The audit exhausts both encoders, all four deterministic decoders, and both
possible labeled feedback cases for each encoder.

## Benchmark rule adopted here

Before interpreting an empirical failure as coordination difficulty, record:

1. whether train and test states differ;
2. whether augmentation over those states closes the gap;
3. whether observations have a grounded, partner-independent decoding;
4. whether multiple fully covered conventions remain mutually incompatible;
5. what test-time feedback is available.

In Kemeny experiments, lexicographic tie resolution and candidate labels can
act like conventions. Relabeling tests are therefore required separately from
profile-coverage tests. This analogy changes evaluation practice only; it
does not import an Overcooked theorem into rank aggregation.

## Reproduction

```bash
python scripts/run_coordination_audit.py
python -m unittest tests.test_coordination -v
```

The exact output is in
[`results/coordination_audit.json`](../results/coordination_audit.json).
