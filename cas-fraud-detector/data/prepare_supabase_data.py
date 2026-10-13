"""
Prepara los CSVs para importar en Supabase.
Corre este script en tu Mac ANTES del kickoff.

Uso:
    python prepare_supabase_data.py

Input:  synpuf_oof_results.csv (en la misma carpeta o ruta que indiques)
Output: supabase_claims.csv, supabase_providers.csv, supabase_alerts.csv
"""

import pandas as pd
import os

# Ajusta esta ruta si tu CSV está en otro lugar
RESULTS_PATH = os.path.join(
    os.path.expanduser("~"),
    "Desktop", "Masters", "Fraud Pipeline", "synpuf_oof_results.csv"
)

def main():
    print("Leyendo synpuf_oof_results.csv...")
    df = pd.read_csv(RESULTS_PATH)
    print(f"  → {len(df):,} claims cargados")

    out_dir = os.path.dirname(os.path.abspath(__file__))

    # ── Claims ────────────────────────────────────────────
    claims_cols = [
        "CLM_ID","AT_PHYSN_NPI","DESYNPUF_ID","specialty",
        "HCPCS_CD","ICD9_DGNS_CD_1","amount_billed","CLM_PMT_AMT",
        "pm_score","structural_score","semantic_score","temporal_score",
        "xgb_score","if_score","cas_score","oar_alert","oar_confidence",
        "n_signals","is_fraud","fraud_type","fraud_narrative",
        "PRVDR_STATE_CD","service_hour","submission_lag","flow_length",
    ]
    available = [c for c in claims_cols if c in df.columns]
    claims = df[available]
    claims.to_csv(os.path.join(out_dir, "supabase_claims.csv"), index=False)
    print(f"  → supabase_claims.csv ({len(claims):,} rows)")

    # ── Providers ─────────────────────────────────────────
    prov = df.groupby("AT_PHYSN_NPI").agg(
        specialty=("specialty", "first"),
        n_claims=("CLM_ID", "count"),
        fraud_rate=("is_fraud", "mean"),
        cas_score=("cas_score", "first"),
        avg_pm_score=("pm_score", "mean"),
        avg_amount=("amount_billed", "mean"),
        n_alerts=("oar_alert", "sum"),
        PRVDR_STATE_CD=("PRVDR_STATE_CD", "first"),
    ).reset_index()
    prov["fraud_rate"] = prov["fraud_rate"].round(4)
    prov["avg_pm_score"] = prov["avg_pm_score"].round(4)
    prov["avg_amount"] = prov["avg_amount"].round(2)
    prov["n_alerts"] = prov["n_alerts"].astype(int)
    prov.to_csv(os.path.join(out_dir, "supabase_providers.csv"), index=False)
    print(f"  → supabase_providers.csv ({len(prov):,} rows)")

    # ── Alerts ────────────────────────────────────────────
    alert_cols = ["CLM_ID","AT_PHYSN_NPI","n_signals",
                  "oar_confidence","fraud_narrative"]
    avail_a = [c for c in alert_cols if c in df.columns]
    alerts = df[df["oar_alert"] == 1][avail_a].copy()
    alerts["status"] = "pending"
    alerts.to_csv(os.path.join(out_dir, "supabase_alerts.csv"), index=False)
    print(f"  → supabase_alerts.csv ({len(alerts):,} rows)")

    print(f"\nArchivos listos en: {out_dir}")
    print("Importa estos 3 CSVs en Supabase el día del kickoff.")


if __name__ == "__main__":
    main()
