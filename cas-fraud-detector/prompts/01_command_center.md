# Prompt 01 — Command Center

> Copy and paste this into Lovable on kickoff day (October 15).

```
Build a fraud detection dashboard for Medicare Part B healthcare claims
called "CAS Fraud Detector". Connect to Supabase.

The app has a dark professional theme with a sidebar navigation containing:
Command Center, Claim Inspector, Provider Profiler, and About.

Use shadcn/ui components, Recharts for charts, and Tailwind CSS.
The color palette should feel clinical and trustworthy: deep navy (#0C2340)
as primary, teal (#0F6E56) for positive indicators, coral (#993C1D) for
alerts, and amber (#854F0B) for warnings.

The Command Center (main page) shows:
- 4 KPI cards at the top: Total Claims (50,000), Active Alerts (count where
  oar_alert=1), FWE Total ($1,430,591), FWE Reduction (98.2%)
- A bar chart showing alerts by fraud type (F1-F5)
- A donut chart showing signal distribution (n_signals: 0,1,2,3)
- A sortable table of the 20 most recent alerts with columns: CLM_ID,
  Provider NPI, Amount, Signals, Confidence, Status, with color-coded
  severity badges

Data comes from Supabase tables: claims, providers, alerts.
```
