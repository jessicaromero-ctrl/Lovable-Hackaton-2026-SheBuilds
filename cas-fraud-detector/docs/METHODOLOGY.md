# Methodology — CAS Framework and Triple Conformance

## Epistemological foundation

This project models healthcare fraud as a **Complex Adaptive System** rather than a static pattern. Drawing from General Systems Theory (von Bertalanffy, 1968) and Complexity Theory (Holland, 1995; Kauffman, 1993), the framework recognizes four properties of fraud:

- **Adaptation:** Fraudulent agents modify their behavior over time to evade detection
- **Emergence:** Fraud patterns emerge from interactions between agents, not from isolated actors
- **Non-linearity:** Small quantitative changes in behavior can signal qualitative strategy shifts
- **Feedback:** The detection system itself alters the behavior of the agents it observes

## Triple conformance checking

Unlike conventional single-layer conformance (structural only), this system evaluates three dimensions:

### Layer A — Structural fitness (Token Replay)

Evaluates whether the claim's process flow matches the normative Petri net discovered per specialty.

### Layer B — Semantic fitness (CPT-specialty coherence)

Evaluates whether the billed CPT code is semantically consistent with the provider's medical specialty, considering expected CPTs, forbidden CPTs, complexity deviation, and amount ratio.

### Layer C — Temporal fitness (Process timestamps)

Evaluates submission lag patterns, service hour anomalies, and flow completeness.

### Combined pm_score

```
pm_score = 0.45 × (1 − fitness_A) + 0.35 × semantic_B + 0.20 × temporal_C
```

Result on synthetic dataset: Δ = 0.2586 (fraud mean: 0.2758 vs normal mean: 0.0172).

## CAS Score

A composite metric quantifying how "adaptively suspicious" a provider's behavior is:

```
CAS(a) = 0.40 × rank(drift_composite) + 0.30 × rank(1 − diversity) + 0.30 × rank(regime_score)
```

Providers with high CAS score have 2.5× the fraud rate of the general population.

## Detection by fraud type

| Type | Description | Recall |
|---|---|---|
| F1 Severe upcoding | CPT 99213 billed as 99215 | 98.3% |
| F2 Phantom billing | Services never rendered | 100.0% |
| F3 Unbundling | Single procedure fragmented | 99.2% |
| F4 Surgical upcoding | Office visit billed as surgery | 100.0% |
| F5 Mild upcoding | CPT 99213 billed as 99214 | 23.3% |

## Interdisciplinary contribution

This work applies sociological frameworks (complex systems theory) to an engineering problem (fraud detection in ML), demonstrating that adaptive behavioral features improve detection beyond traditional static approaches.
