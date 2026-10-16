# SheBuilds Season 4 — Battle Plan

**Proyecto:** CAS Fraud Detection — Medicare Part B  
**Kickoff:** 15 de octubre  |  **Deadline:** 17 de octubre, 9PM PT  
**Estado:** Preparación (todo lo de abajo se hace ANTES del 15)

---

## A. LO QUE YA TIENES (confirma que está listo)

- [ ] `cas_fraud_pipeline.py` funcional (corre en ~32s, genera 5 CSVs)
- [ ] `synpuf_event_log.csv` — 318,616 eventos
- [ ] `synpuf_claim_meta.csv` — 50,000 claims
- [ ] `synpuf_providers.csv` — 800 proveedores
- [ ] `synpuf_pm_scored.csv` — claims con pm_score (3 capas)
- [ ] `synpuf_oof_results.csv` — resultados OOF + O-A-R + narrativas
- [ ] PDF de propuesta matemática
- [ ] PDF de resumen ejecutivo
- [ ] PDF briefing para abogada de PI
- [ ] Diagramas de arquitectura (PNG): tres capas + OAR + Delta Lake

---

## B. SUBMISSION — TEXTOS LISTOS PARA PEGAR

### B1. Nombre del proyecto
```
CAS Fraud Detector
```

### B2. One-line description (máx ~120 caracteres)
```
Fraud detection for healthcare claims using Process Mining, ML, and Complex Adaptive Systems theory.
```

### B3. Longer description (para el portal de submission)
```
CAS Fraud Detector applies a novel triple-conformance checking method
(structural + semantic + temporal) combined with Complex Adaptive Systems
theory to detect fraud in Medicare Part B carrier claims.

The system integrates three independent detection signals — Process Mining
conformance (Inductive Miner + Token Replay), supervised ML (XGBoost), and
unsupervised anomaly detection (Isolation Forest) — through an Observe-Assess-
Respond pipeline with adaptive thresholds per provider.

Key results on a 50,000-claim synthetic dataset (SynPUF-inspired):
• ROC-AUC: 0.9959 | Recall: 93.8% | FWE Reduction: 98.2%
• 100% precision when all 3 signals agree (1,227 cases, zero false positives)
• CAS score identifies high-risk providers at 2.5x the general fraud rate

Built from an interdisciplinary perspective combining sociology (complex
systems theory) with ML engineering for healthcare InsurTech.
```

### B4. Categoría sugerida
```
Health / InsurTech / FinTech (elegir la que esté disponible en el portal)
```

### B5. Screenshots necesarios
- [ ] Command Center (dashboard principal con KPIs)
- [ ] Claim Inspector (detalle de un caso con radar chart + narrativa)
- [ ] Provider Profiler (perfil de riesgo por NPI)
- [ ] (Opcional) Process Explorer si da tiempo

---

## C. SUPABASE — ESTRUCTURA DE DATOS

Cuando abras Lovable el día 15, lo primero es conectar Supabase.
Estas son las tablas que necesitas crear:

### Tabla: `claims`
Fuente: `synpuf_oof_results.csv` (las columnas más importantes)

| Columna | Tipo | Descripción |
|---|---|---|
| CLM_ID | text (PK) | ID del claim |
| AT_PHYSN_NPI | text | NPI del proveedor |
| DESYNPUF_ID | text | ID del beneficiario |
| specialty | text | Especialidad médica |
| HCPCS_CD | text | Código CPT |
| ICD9_DGNS_CD_1 | text | Código diagnóstico |
| amount_billed | numeric | Monto facturado |
| CLM_PMT_AMT | numeric | Monto pagado |
| pm_score | numeric | Score PM (3 capas) |
| structural_score | numeric | Capa A |
| semantic_score | numeric | Capa B |
| temporal_score | numeric | Capa C |
| xgb_score | numeric | Score XGBoost |
| if_score | numeric | Score Isolation Forest |
| cas_score | numeric | Score CAS compuesto |
| oar_alert | integer | 0 o 1 |
| oar_confidence | numeric | Confianza O-A-R |
| n_signals | integer | 0-3 |
| is_fraud | integer | Ground truth |
| fraud_type | text | Tipo F1-F5 |
| fraud_narrative | text | Narrativa explicable |
| PRVDR_STATE_CD | text | Estado del proveedor |
| service_hour | integer | Hora del servicio |
| submission_lag | integer | Días de submission |
| flow_length | integer | Pasos en el flujo |

### Tabla: `providers`
Fuente: derivar de `synpuf_oof_results.csv` agrupando por NPI

| Columna | Tipo | Descripción |
|---|---|---|
| AT_PHYSN_NPI | text (PK) | NPI |
| specialty | text | Especialidad |
| n_claims | integer | Total claims |
| fraud_rate | numeric | Tasa de fraude |
| cas_score | numeric | CAS score |
| avg_pm_score | numeric | pm_score promedio |
| avg_amount | numeric | Monto promedio |
| n_alerts | integer | Total alertas O-A-R |
| PRVDR_STATE_CD | text | Estado |

### Tabla: `alerts`
Fuente: filtrar `synpuf_oof_results.csv` donde oar_alert = 1

| Columna | Tipo | Descripción |
|---|---|---|
| id | uuid (PK) | Auto-generado |
| CLM_ID | text | FK a claims |
| AT_PHYSN_NPI | text | FK a providers |
| status | text | pending / investigating / confirmed / dismissed |
| n_signals | integer | 0-3 |
| oar_confidence | numeric | Confianza |
| fraud_narrative | text | Narrativa |
| created_at | timestamp | Auto |

---

## D. PROMPTS PARA LOVABLE — COPIAR Y PEGAR

### D1. Prompt inicial (crea la estructura completa)
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

### D2. Prompt para Claim Inspector
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

### D3. Prompt para Provider Profiler
```
Add the Provider Profiler page. Show a searchable list of providers from
the providers Supabase table. When selected, show:

- Provider header: NPI, specialty, state, total claims, CAS score badge
- A gauge or progress bar for CAS score (0 to 1, colored by risk level)
- Stats row: fraud rate, average amount billed, alert count
- A bar chart of the provider's claims by fraud type
- A comparison line: "This provider's CAS score is higher than X% of
  providers in the same specialty"
```

### D4. Prompt para página About
```
Add an About page that explains the methodology. Include:

- A section titled "How it works" with a brief explanation of the three
  detection layers: Conformance (Process Mining), Supervised (XGBoost),
  and Unsupervised (Isolation Forest)
- A section titled "CAS Framework" explaining the four CAS dimensions:
  Temporal Drift, Emergence (entropy), Phase Transitions, and Feedback
- A section titled "O-A-R Pipeline" explaining Observe-Assess-Respond
- Keep it concise, professional, and accessible to non-technical users
- Add a footer note: "Built for SheBuilds Season 4"
```

---

## E. ORDEN DE CONSTRUCCIÓN (prioridades)

El criterio de los jueces es: originalidad, utilidad, ejecución/diseño,
y potencial futuro. Construye en este orden:

1. **Prompt D1 — Command Center** (es lo primero que ven los jueces)
2. **Conectar Supabase** y cargar datos reales de tus CSVs
3. **Prompt D2 — Claim Inspector** (tu killer feature: radar + narrativa)
4. **Prompt D3 — Provider Profiler** (demuestra CAS score en acción)
5. **Prompt D4 — About** (contexto metodológico para los jueces)
6. **Pulir diseño** — colores, responsive, detalles visuales
7. **Publicar** y verificar que la URL funciona
8. **Screenshots** para el submission
9. **Llenar el formulario** de submission con los textos de sección B

Si el tiempo se acaba después del paso 3, ya tienes lo esencial.
El Command Center + Claim Inspector son suficientes para ganar.

---

## F. DATOS PARA SUPABASE — SCRIPT DE PREPARACIÓN

Antes del 15, prepara un script que convierta tus CSVs en las 3 tablas
de Supabase. Corre esto en tu Mac para generar los archivos listos:

```python
import pandas as pd

df = pd.read_csv("synpuf_oof_results.csv")

# Tabla claims: tomar columnas relevantes
claims_cols = ["CLM_ID","AT_PHYSN_NPI","DESYNPUF_ID","specialty",
    "HCPCS_CD","ICD9_DGNS_CD_1","amount_billed","CLM_PMT_AMT",
    "pm_score","structural_score","semantic_score","temporal_score",
    "xgb_score","if_score","cas_score","oar_alert","oar_confidence",
    "n_signals","is_fraud","fraud_type","fraud_narrative",
    "PRVDR_STATE_CD","service_hour","submission_lag","flow_length"]
available = [c for c in claims_cols if c in df.columns]
df[available].to_csv("supabase_claims.csv", index=False)

# Tabla providers: agregar por NPI
prov = df.groupby("AT_PHYSN_NPI").agg(
    specialty=("specialty","first"),
    n_claims=("CLM_ID","count"),
    fraud_rate=("is_fraud","mean"),
    cas_score=("cas_score","first"),
    avg_pm_score=("pm_score","mean"),
    avg_amount=("amount_billed","mean"),
    n_alerts=("oar_alert","sum"),
    PRVDR_STATE_CD=("PRVDR_STATE_CD","first"),
).reset_index()
prov.to_csv("supabase_providers.csv", index=False)

# Tabla alerts: solo claims con alerta
alerts = df[df["oar_alert"]==1][["CLM_ID","AT_PHYSN_NPI",
    "n_signals","oar_confidence","fraud_narrative"]].copy()
alerts["status"] = "pending"
alerts.to_csv("supabase_alerts.csv", index=False)

print(f"claims: {len(df):,} rows")
print(f"providers: {len(prov):,} rows")
print(f"alerts: {len(alerts):,} rows")
print("Archivos listos para importar en Supabase.")
```

---

## G. DEMO VIDEO (opcional pero recomendado)

Si te da tiempo, graba un video de 60-90 segundos:
- 10s: qué problema resuelve
- 20s: Command Center en vivo, mostrar KPIs
- 20s: click en un claim, mostrar radar chart + narrativa
- 15s: Provider Profiler, mostrar CAS score
- 15s: resultado clave — "100% precision con 3 señales, cero falsos positivos"
- 10s: cierre — "Built with CAS theory, Process Mining, and ML"

---

## H. DÍA DE SUBMISSION — CHECKLIST FINAL

- [ ] App publicada en Lovable (URL funcional)
- [ ] Verificar que la URL carga correctamente en otro navegador
- [ ] Project name: CAS Fraud Detector
- [ ] One-line description pegada (sección B2)
- [ ] Longer description pegada (sección B3)
- [ ] Categoría seleccionada
- [ ] Screenshots subidos (mínimo 3)
- [ ] Demo video subido (si lo grabaste)
- [ ] Formulario guardado ANTES de las 9PM PT del 17 de octubre
