#!/usr/bin/env python3
"""5G Slice Validator — CLI entry (validation + reports)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reports.generator import write_markdown_report  # noqa: E402
from scenarios import SCENARIOS  # noqa: E402
from validator.pipeline import ValidationPipeline, report_to_json  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="5G SA slice & registration validation toolkit (Open5GS + UERANSIM artifacts)."
    )
    p.add_argument(
        "--scenario",
        choices=list(SCENARIOS.keys()),
        help="Use bundled demo log + matching scenario config directory.",
    )
    p.add_argument(
        "--logs",
        nargs="*",
        help="Explicit log file paths (relative to project root or absolute).",
    )
    p.add_argument(
        "--config-dir",
        type=str,
        default=None,
        help="Directory containing ue.yaml, gnb.yaml, amf.yaml, subscriber.yaml, runtime_probe.yaml.",
    )
    p.add_argument(
        "--ping-ok",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=None,
        help="Optional: pass-through ping result for UPF reachability (true/false).",
    )
    p.add_argument(
        "--json-out",
        type=str,
        default="reports/last_run.json",
        help="Write full JSON report to this path.",
    )
    p.add_argument(
        "--markdown-out",
        type=str,
        default="reports/last_run.md",
        help="Write human-readable Markdown report.",
    )
    p.add_argument("--quiet", action="store_true", help="Suppress printing summary to stdout.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    log_paths: list[Path] = []
    cfg_dir: Path | None = None

    if args.scenario:
        rel_log, rel_cfg = SCENARIOS[args.scenario]
        log_paths = [ROOT / rel_log]
        cfg_dir = ROOT / rel_cfg
    if args.logs:
        log_paths = [Path(x) for x in args.logs]
    if args.config_dir:
        cfg_dir = Path(args.config_dir)

    pipe = ValidationPipeline(
        project_root=ROOT,
        log_files=log_paths or None,
        ping_ok=args.ping_ok,
        config_dir=cfg_dir,
    )
    report = pipe.run()

    json_path = Path(args.json_out)
    if not json_path.is_absolute():
        json_path = ROOT / json_path
    md_path = Path(args.markdown_out)
    if not md_path.is_absolute():
        md_path = ROOT / md_path

    report_to_json(report, json_path)
    write_markdown_report(report, md_path)

    if not args.quiet:
        agg = report.get("aggregate_status", "?")
        diag = report.get("module_6_diagnosis", {})
        print(f"Aggregate: {agg}")
        print(f"Root cause: {diag.get('root_cause', '')}")
        print(f"JSON: {json_path}")
        print(f"Markdown: {md_path}")

    return 0 if report.get("aggregate_status") in ("PASS", "WARN") else 1


if __name__ == "__main__":
    raise SystemExit(main())
