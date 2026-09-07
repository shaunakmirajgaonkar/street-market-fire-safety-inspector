import pandas as pd
from pathlib import Path
from firewatch_engine import REQUIRED_METRICS, REQUIRED_HISTORY, score_markets, validate_schema
root=Path(__file__).parent
m=pd.read_csv(root/'data/sample_market_metrics.csv'); h=pd.read_csv(root/'data/sample_inspection_history.csv')
ok1,miss1=validate_schema(m,REQUIRED_METRICS); ok2,miss2=validate_schema(h,REQUIRED_HISTORY)
assert ok1 and ok2, (miss1,miss2)
s=score_markets(m)
assert s['fire_risk_score'].between(0,100).all()
assert len(s)==24 and len(h)==192
print('PASS: FireWatch street-market fire-safety screening')
print(f'Markets: {len(s)}')
print(f'History rows: {len(h)}')
print(f'Risk range: {s.fire_risk_score.min():.1f}-{s.fire_risk_score.max():.1f}')
print(f'High/Critical: {int(s.risk_level.isin(["High","Critical"]).sum())}')
