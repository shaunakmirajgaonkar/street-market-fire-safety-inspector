import pandas as pd
from firewatch_engine import score_markets

def make_row():
    return pd.DataFrame([{
        'market_id':'X1','market_name':'Demo','zone':'Z','latitude':1.0,'longitude':2.0,'stall_count':100,
        'stall_density_per_100m':80,'electrical_wiring_risk':70,'exit_access_score':40,'fuel_storage_risk':60,
        'hydrant_access_score':45,'crowding_index':75,'inspection_overdue_days':120,'recent_incident_count_90d':2,
        'fire_extinguisher_coverage_pct':55}])

def test_score_range():
    s=score_markets(make_row())
    assert 0 <= float(s.fire_risk_score.iloc[0]) <= 100

def test_risk_label_exists():
    s=score_markets(make_row())
    assert s.risk_level.iloc[0] in {'Low','Moderate','High','Critical'}

def test_primary_driver_exists():
    s=score_markets(make_row())
    assert isinstance(s.primary_driver.iloc[0], str) and s.primary_driver.iloc[0]
