from __future__ import annotations
import pandas as pd
import numpy as np

REQUIRED_METRICS = [
    'market_id','market_name','zone','latitude','longitude','stall_count',
    'stall_density_per_100m','electrical_wiring_risk','exit_access_score',
    'fuel_storage_risk','hydrant_access_score','crowding_index',
    'inspection_overdue_days','recent_incident_count_90d','fire_extinguisher_coverage_pct'
]
REQUIRED_HISTORY = ['market_id','inspection_date','inspection_score','electrical_wiring_risk','fuel_storage_risk','exit_access_score','hydrant_access_score']


def validate_schema(df: pd.DataFrame, required: list[str]) -> tuple[bool, list[str]]:
    missing = [c for c in required if c not in df.columns]
    return not missing, missing


def _clip(s, lo=0.0, hi=100.0):
    return pd.to_numeric(s, errors='coerce').fillna(0).clip(lo, hi)


def score_markets(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    # Pressure scores: higher = greater concern, except access/coverage metrics.
    density = _clip(x['stall_density_per_100m'], 0, 120) / 120 * 100
    wiring = _clip(x['electrical_wiring_risk'])
    exits = 100 - _clip(x['exit_access_score'])
    fuel = _clip(x['fuel_storage_risk'])
    hydrant = 100 - _clip(x['hydrant_access_score'])
    crowd = _clip(x['crowding_index'])
    overdue = _clip(x['inspection_overdue_days'], 0, 365) / 365 * 100
    incidents = _clip(x['recent_incident_count_90d'], 0, 10) / 10 * 100
    extinguishers = 100 - _clip(x['fire_extinguisher_coverage_pct'])

    weights = {
        'density': .16, 'wiring': .16, 'exits': .14, 'fuel': .14,
        'hydrant': .12, 'crowd': .10, 'overdue': .07, 'incidents': .06,
        'extinguishers': .05
    }
    score = (
        density*weights['density'] + wiring*weights['wiring'] + exits*weights['exits'] +
        fuel*weights['fuel'] + hydrant*weights['hydrant'] + crowd*weights['crowd'] +
        overdue*weights['overdue'] + incidents*weights['incidents'] + extinguishers*weights['extinguishers']
    ).clip(0, 100)
    x['fire_risk_score'] = score.round(1)
    x['risk_level'] = pd.cut(x['fire_risk_score'], [-0.01,24.99,49.99,74.99,100.01], labels=['Low','Moderate','High','Critical'])
    x['risk_level'] = x['risk_level'].astype(str)
    x['primary_driver'] = pd.DataFrame({
        'Stall density': density, 'Electrical wiring': wiring, 'Exit access': exits,
        'Fuel storage': fuel, 'Hydrant access': hydrant, 'Crowding': crowd,
        'Inspection overdue': overdue, 'Recent incidents': incidents,
        'Extinguisher coverage': extinguishers
    }).idxmax(axis=1)
    return x


def summary(scored: pd.DataFrame) -> dict:
    return {
        'markets': int(len(scored)),
        'avg_score': float(scored['fire_risk_score'].mean()) if len(scored) else 0.0,
        'high_critical': int(scored['risk_level'].isin(['High','Critical']).sum()),
        'critical': int((scored['risk_level']=='Critical').sum()),
        'inspection_overdue': int((pd.to_numeric(scored['inspection_overdue_days'], errors='coerce').fillna(0) > 30).sum()),
        'avg_stall_density': float(pd.to_numeric(scored['stall_density_per_100m'], errors='coerce').mean()) if len(scored) else 0.0,
    }
