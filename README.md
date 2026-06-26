# 5G Slice Validator

Python toolkit that checks **5G SA** configuration consistency (DNN, TAC, S-NSSAI), analyzes **Open5GS** and **UERANSIM** logs, classifies **NAS/SM causes**, infers **root cause**, and exposes results in a **Streamlit** dashboard with **JSON/Markdown** reports.

## Requirements

- Python 3.10+
- Dependencies: `pip install -r requirements.txt`

## Quick start

```bash
# Run validation (default: logs/scenario_success.log + configs/)
python main.py

# Bundled demos
python main.py --scenario success
python main.py --scenario wrong_dnn
python main.py --scenario wrong_tac
python main.py --scenario wrong_slice
python main.py --scenario smf_down

# Outputs
#   reports/last_run.json
#   reports/last_run.md
```

## Dashboard

```bash
streamlit run dashboard/app.py
```

Use the sidebar to pick a scenario and **Run validation now**, or load `reports/last_run.json`.

## Tests

```bash
python -m pytest tests -q
```

## Layout

See `configs/`, `logs/`, `parser/`, `validator/`, `dashboard/`, `reports/`, and `scenarios.py` for demo mappings.

## Production notes

- Set `configs/runtime_probe.yaml` to `mode: systemd` on Linux to probe real Open5GS units (requires `systemctl`).
- Replace demo logs under `logs/` with captures from your lab.

## Report for submission

Use `reports/FINAL_REPORT_TEMPLATE.md` as the skeleton for your course final report.
