#!/usr/bin/env python3
"""Run every bundled scenario and print a summary table (test automation helper)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scenarios import SCENARIOS  # noqa: E402
from validator.pipeline import ValidationPipeline  # noqa: E402


def main() -> None:
    rows: list[tuple[str, str, str]] = []
    for name in SCENARIOS:
        rel_log, rel_cfg = SCENARIOS[name]
        pipe = ValidationPipeline(
            project_root=ROOT,
            log_files=[ROOT / rel_log],
            config_dir=ROOT / rel_cfg,
        )
        r = pipe.run()
        agg = r.get("aggregate_status", "?")
        rc = r.get("module_6_diagnosis", {}).get("root_cause", "")[:80]
        rows.append((name, agg, rc))
    w = max(len(x[0]) for x in rows)
    print(f"{'scenario'.ljust(w)}  status  root_cause")
    for name, agg, rc in rows:
        print(f"{name.ljust(w)}  {agg:4}  {rc}")


if __name__ == "__main__":
    main()
