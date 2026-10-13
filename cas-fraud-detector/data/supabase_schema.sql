-- CAS Fraud Detector — Supabase Schema
-- Run this in Supabase SQL Editor before importing CSVs

CREATE TABLE IF NOT EXISTS claims (
    "CLM_ID"             TEXT PRIMARY KEY,
    "AT_PHYSN_NPI"       TEXT,
    "DESYNPUF_ID"        TEXT,
    specialty            TEXT,
    "HCPCS_CD"           TEXT,
    "ICD9_DGNS_CD_1"     TEXT,
    amount_billed        NUMERIC,
    "CLM_PMT_AMT"        NUMERIC,
    pm_score             NUMERIC,
    structural_score     NUMERIC,
    semantic_score       NUMERIC,
    temporal_score       NUMERIC,
    xgb_score            NUMERIC,
    if_score             NUMERIC,
    cas_score            NUMERIC,
    oar_alert            INTEGER,
    oar_confidence       NUMERIC,
    n_signals            INTEGER,
    is_fraud             INTEGER,
    fraud_type           TEXT,
    fraud_narrative      TEXT,
    "PRVDR_STATE_CD"     TEXT,
    service_hour         INTEGER,
    submission_lag       INTEGER,
    flow_length          INTEGER
);

CREATE TABLE IF NOT EXISTS providers (
    "AT_PHYSN_NPI"       TEXT PRIMARY KEY,
    specialty            TEXT,
    n_claims             INTEGER,
    fraud_rate           NUMERIC,
    cas_score            NUMERIC,
    avg_pm_score         NUMERIC,
    avg_amount           NUMERIC,
    n_alerts             INTEGER,
    "PRVDR_STATE_CD"     TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
    id                   UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    "CLM_ID"             TEXT REFERENCES claims("CLM_ID"),
    "AT_PHYSN_NPI"       TEXT REFERENCES providers("AT_PHYSN_NPI"),
    status               TEXT DEFAULT 'pending',
    n_signals            INTEGER,
    oar_confidence       NUMERIC,
    fraud_narrative      TEXT,
    created_at           TIMESTAMPTZ DEFAULT now()
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_claims_npi ON claims("AT_PHYSN_NPI");
CREATE INDEX IF NOT EXISTS idx_claims_alert ON claims(oar_alert);
CREATE INDEX IF NOT EXISTS idx_claims_signals ON claims(n_signals);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_providers_cas ON providers(cas_score DESC);
