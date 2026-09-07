# FireWatch — Street-Market Fire Safety Inspector

Privacy-conscious, local-first fire-risk screening for street-market areas using stall density, electrical wiring, exits, fuel storage, hydrant access, crowding, incidents, extinguisher coverage, and inspection history.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 validate_project.py
python3 -m pytest -q
python3 run.py
```

Open the localhost URL printed by `run.py`.

## Local data
- `data/sample_market_metrics.csv`
- `data/sample_inspection_history.csv`

## Responsible use
Scores are comparative screening indicators. They do not certify fire safety, code compliance, emergency readiness, or evacuation safety.
