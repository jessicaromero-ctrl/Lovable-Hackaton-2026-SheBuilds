# CAS Fraud Detector

**Fraud detection interface for Medicare Part B healthcare claims using Process Mining, Machine Learning, and Complex Adaptive Systems theory.**

Built for [SheBuilds Season 4](https://lovable.dev/shebuilds) on Lovable.

---

## What is this

CAS Fraud Detector is an interactive dashboard that visualizes the results of a fraud detection pipeline applied to Medicare Part B carrier claims. The interface allows auditors and investigators to explore alerts, inspect individual claims, and profile providers by risk level.

The detection engine behind this interface combines three independent signals:

- **Conformance checking** (Process Mining — Inductive Miner + Token Replay) with a novel triple-layer approach: structural, semantic, and temporal conformance
- **Supervised classification** (XGBoost) with provider-level behavioral features
- **Unsupervised anomaly detection** (Isolation Forest) with entropy-based features

These signals feed into an **Observe-Assess-Respond (O-A-R) pipeline** with adaptive thresholds informed by a **Complex Adaptive Systems (CAS) score** per provider.

## Key results

| Metric | Value |
|---|---|
| ROC-AUC (XGBoost OOF) | 0.9959 |
| Recall (O-A-R pipeline) | 93.79% |
| Precision (3 signals) | 100.0% |
| FWE Reduction | 98.24% |
| Δ CAS (fraud vs normal) | 0.1357 |

50,000 synthetic claims · 800 providers · 5 fraud profiles · 31.7s execution time

## Interface screens

| Screen | Purpose |
|---|---|
| **Command Center** | KPIs, alert distribution, signal breakdown, recent alerts table |
| **Claim Inspector** | Per-claim detail with radar chart, 3 scores, CAS context, narrative |
| **Provider Profiler** | Per-provider risk profile, CAS score, specialty comparison |
| **About** | Methodology explanation for non-technical users |

## Repository structure

```
cas-fraud-detector/
├── README.md                  ← This file
├── docs/
│   ├── ARCHITECTURE.md        ← System architecture overview
│   └── METHODOLOGY.md         ← CAS framework and triple conformance
├── prompts/
│   ├── 01_command_center.md   ← Lovable prompt for main dashboard
│   ├── 02_claim_inspector.md  ← Lovable prompt for claim detail
│   ├── 03_provider_profiler.md← Lovable prompt for provider view
│   └── 04_about.md            ← Lovable prompt for methodology page
├── data/
│   ├── README.md              ← Data dictionary and schema
│   └── supabase_schema.sql    ← Supabase table definitions
├── screenshots/               ← App screenshots for submission
└── .github/
    └── CODEOWNERS             ← Repository ownership
```

> **Note:** This repository contains interface resources, documentation, and design assets. The detection pipeline (Python code, algorithms, mathematical formulations) is maintained separately and is not included in this repository.

## Interdisciplinary perspective

This project approaches fraud detection from the perspective of Complex Adaptive Systems theory (von Bertalanffy, Holland, Kauffman), applying concepts from sociology and complexity science to the engineering problem of healthcare fraud. The core insight: fraud is not a static pattern to detect — it is a dynamic, adaptive phenomenon where agents co-evolve with their regulatory environment.

## Built with

- [Lovable](https://lovable.dev) — AI-powered app builder (interface)
- [Supabase](https://supabase.com) — Backend (database, auth)
- [Recharts](https://recharts.org) — Data visualization
- [shadcn/ui](https://ui.shadcn.com) — UI components

## Author

Developed as an independent research project. Not affiliated with any university thesis or commercial product.

## License

All rights reserved. This work is protected by copyright. No part of this repository may be reproduced, distributed, or used without explicit written permission from the author.
