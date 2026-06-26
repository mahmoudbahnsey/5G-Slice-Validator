"""Orchestrates validation modules and produces an aggregate report dict."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml

from parser.engine import LogParserEngine
from validator.config_consistency import validate_config_consistency
from validator.core_health import check_core_health
from validator.diagnosis import analyze
from validator.pdu_session import validate_pdu_session
from validator.registration import validate_registration


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


class ValidationPipeline:
    def __init__(
        self,
        project_root: str | Path | None = None,
        log_files: list[str | Path] | None = None,
        ping_ok: bool | None = None,
        config_dir: str | Path | None = None,
    ):
        self.root = Path(project_root or Path(__file__).resolve().parent.parent)
        self.config_dir = Path(config_dir) if config_dir else (self.root / "configs")
        self.logs_dir = self.root / "logs"
        self.log_files = [Path(p) for p in (log_files or [])]
        self.ping_ok = ping_ok

    def default_logs(self) -> list[Path]:
        if self.log_files:
            return self.log_files
        preferred = self.logs_dir / "scenario_success.log"
        if preferred.exists():
            return [preferred]
        cand = sorted(self.logs_dir.glob("*.log"))
        return cand[:1] if cand else []

    def run(self) -> dict[str, Any]:
        logs = self.default_logs()
        parser_engine = LogParserEngine(logs)
        bundle = parser_engine.parse()

        health = check_core_health(self.config_dir)
        reg = validate_registration(bundle)
        pdu = validate_pdu_session(bundle, ping_ok=self.ping_ok)
        cfg = validate_config_consistency(self.config_dir)

        diag = analyze(health, reg, pdu, cfg, bundle)

        def health_dict() -> dict[str, Any]:
            return {
                "mode": health.mode,
                "components": health.components,
                "notes": health.notes,
            }

        report: dict[str, Any] = {
            "project": "5G Slice Validator",
            "config_dir": str(self.config_dir),
            "logs": [str(p) for p in logs],
            "module_1_core_health": health_dict(),
            "module_2_registration": {
                "status": reg.status,
                "steps": reg.steps,
                "reason": reg.reason,
            },
            "module_3_pdu_session": {
                "status": pdu.status,
                "has_ip": pdu.has_ip,
                "session_active": pdu.session_active,
                "reachable_upf": pdu.reachable_upf,
                "reason": pdu.reason,
                "details": pdu.details,
            },
            "module_4_config_consistency": {
                "overall": cfg.overall,
                "checks": [asdict(c) for c in cfg.checks],
            },
            "module_5_parser_summary": {
                "causes_mm": bundle.causes_mm,
                "causes_sm": bundle.causes_sm,
                "ip_addresses": bundle.ip_addresses,
                "events": bundle.events[:20],
            },
            "module_6_diagnosis": asdict(diag),
            "aggregate_status": self._aggregate(reg.status, pdu.status, cfg.overall, health.components),
        }
        return report

    @staticmethod
    def _aggregate(
        reg_s: str,
        pdu_s: str,
        cfg_s: str,
        components: dict[str, str],
    ) -> str:
        if any(v == "DOWN" for v in components.values()):
            return "FAIL"
        if cfg_s == "FAIL" or reg_s == "FAIL" or pdu_s == "FAIL":
            return "FAIL"
        if cfg_s == "WARN" or reg_s == "WARN" or pdu_s == "WARN":
            return "WARN"
        return "PASS"


def report_to_json(report: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
