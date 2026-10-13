# Architecture Overview

## System layers

The CAS Fraud Detector operates in two layers:

### Detection layer (backend — not in this repo)

A Python pipeline that processes Medicare Part B event logs through three modules:

1. **M1 — Data generation:** Synthetic claims inspired by CMS DE-SynPUF (50,000 claims, 800 providers, 5 fraud profiles)
2. **M2 — Process Mining:** Inductive Miner discovers normative Petri nets per specialty; Token Replay evaluates structural fitness; semantic and temporal layers complete the triple conformance check
3. **M3 — ML + CAS:** XGBoost (supervised), Isolation Forest (unsupervised), and CAS features (temporal drift, entropy, phase transitions) feed into the O-A-R pipeline

### Interface layer (this repo)

A web application built on Lovable that consumes the pipeline's output through Supabase and presents it to auditors, investigators, and compliance officers.

## Data flow

```
Pipeline (Python, local)
    ↓ generates CSVs
Supabase (cloud)
    ↓ serves via API
Lovable app (React + Tailwind)
    ↓ renders
User (SIU auditor, compliance officer)
```

## O-A-R Pipeline

```
Observe  → Receives 3 signals (PM, XGBoost, IF)
Assess   → Weighs severity with CAS score amplification
Respond  → Triggers alert with adaptive thresholds
```

When all 3 signals agree: 100% precision (zero false positives).

## CAS Dimensions

| Dimension | Measures | CAS property |
|---|---|---|
| CAS-1: Temporal drift | Behavioral change over time | Adaptation |
| CAS-2: Entropy | Distribution concentration (CPT, Dx, beneficiaries) | Emergence |
| CAS-3: Phase transitions | Regime changes in provider behavior | Non-linearity |
| CAS-4: Adaptive thresholds | Dynamic detection sensitivity per provider | Feedback |

## Medallion data architecture

```
Bronze (raw claims) → Silver (triple scoring) → Gold (alerts + FWE)
```

Compatible with Delta Lake / ACID transactions for production deployment.
