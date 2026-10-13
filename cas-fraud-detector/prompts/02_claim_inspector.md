# Prompt 02 — Claim Inspector

> Paste this after the Command Center is working and connected to Supabase.

```
Add the Claim Inspector page. When a user clicks a claim from the alerts
table, navigate to this detail view showing:

- Header with CLM_ID, provider NPI, specialty, and alert status badge
- A radar chart (Recharts) with 3 axes: Structural Score, Semantic Score,
  Temporal Score, showing the claim's pm_score decomposition
- Three score cards showing XGBoost score, IF score, and PM score with
  color gradients (green < 0.3, amber 0.3-0.6, red > 0.6)
- A CAS score indicator for the provider
- The fraud_narrative text displayed in a highlighted card
- Claim details: CPT code, diagnosis, amount billed vs paid, service hour,
  submission lag, flow length
- Action buttons: Mark as Investigating, Confirm Fraud, Dismiss
```
